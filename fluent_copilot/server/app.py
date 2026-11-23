"""FastAPI 应用：Web UI 的全部后端端点。

- POST /api/chat        SSE 流式聊天（自有极简事件协议，前端 adapter 消费）
- GET  /api/status      Fluent 就绪状态 / 模型名 / 忙碌位
- GET  /api/tools       已注册工具清单（空状态展示用）
- POST /api/launch-fluent   拉起官方 Fluent Launcher（-sifile）
- POST /api/open-trajectory 用记事本打开 trajectory.jsonl
- /                    生产模式托管 frontend/dist

事件协议（SSE data 行，UTF-8 JSON）：
  {"type":"text_delta","content":str}
  {"type":"tool_call","id":str,"name":str,"arguments":str}
  {"type":"tool_result","id":str,"name":str,"result":str,"ok":bool}
  {"type":"final","content":str}
  {"type":"cancelled"} | {"type":"error","message":str} | {"type":"done"}
"""
from __future__ import annotations

import asyncio
import json
import logging
import subprocess
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from fluent_copilot.config import Config, bundle_root, load_config
from fluent_copilot.core import tools
from fluent_copilot.core.agent import Agent, CancelledError
from fluent_copilot.core.llm_gateway import LLMGateway
from fluent_copilot.fluent.mcp_backend import FluentMCPBackend
from fluent_copilot.knowledge.vault import Vault

logger = logging.getLogger(__name__)

# 常见 Ansys 安装根(发现顺序),fluent.exe 相对路径 v*/fluent/ntbin/win64/
_ANSYS_ROOTS = [
    r"C:\Program Files\ANSYS Inc",
    r"C:\Program Files\ANSYS",
    r"C:\ANSYS2026\ANSYS Inc",
    r"D:\Program Files\ANSYS Inc",
    r"D:\ANSYS Inc",
]


def find_fluent_exe() -> Path | None:
    """在常见安装位置发现最新版本的 fluent.exe。"""
    for root in _ANSYS_ROOTS:
        base = Path(root)
        if not base.is_dir():
            continue
        versions = sorted(
            (d for d in base.glob("v*") if d.name[1:3].isdigit()),
            key=lambda d: d.name,
            reverse=True,
        )
        for v in versions:
            exe = v / "fluent" / "ntbin" / "win64" / "fluent.exe"
            if exe.is_file():
                return exe
    return None


FLUENT_EXE: Path | None = None  # 启动时按 config 覆盖或自动发现

FRONTEND_DIST = bundle_root() / "frontend_dist" if bundle_root().joinpath("frontend_dist").is_dir() else bundle_root() / "frontend" / "dist"

# 预置供应商(OpenAI 兼容端点)。models 只是顺手默认,设置对话框里可增删。
PROVIDER_PRESETS: list[dict] = [
    {
        "id": "zhipu",
        "name": "智谱 GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "models": ["glm-5.3", "glm-4.6", "glm-4.5", "glm-4.5-air", "glm-4-flash"],
    },
    {
        "id": "dashscope",
        "name": "阿里云通义（DashScope）",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/",
        "models": ["qwen3-max", "qwen-plus", "qwen-max", "qwen-turbo"],
    },
    {
        "id": "deepseek",
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1/",
        "models": ["deepseek-chat", "deepseek-reasoner"],
    },
    {
        "id": "moonshot",
        "name": "月之暗面 Kimi",
        "base_url": "https://api.moonshot.cn/v1/",
        "models": ["kimi-k2-0905-preview", "moonshot-v1-128k", "moonshot-v1-8k"],
    },
    {
        "id": "siliconflow",
        "name": "硅基流动 SiliconFlow",
        "base_url": "https://api.siliconflow.cn/v1/",
        "models": ["deepseek-ai/DeepSeek-V3.2-Exp", "Qwen/Qwen3-235B-A22B-Instruct"],
    },
    {
        "id": "openai",
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1/",
        "models": ["gpt-5.2", "gpt-5", "gpt-4o"],
    },
    {
        "id": "openrouter",
        "name": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1/",
        "models": ["openai/gpt-5.2", "anthropic/claude-sonnet-4.5", "deepseek/deepseek-chat"],
    },
    {"id": "custom", "name": "自定义", "base_url": "", "models": []},
]


def _match_provider(base_url: str) -> str:
    """按 base_url 反查预置供应商 id,查不到算 custom。"""
    norm = (base_url or "").strip().rstrip("/").lower()
    for p in PROVIDER_PRESETS:
        if p["id"] != "custom" and p["base_url"].rstrip("/").lower() == norm:
            return p["id"]
    return "custom"


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


def maybe_launch_fluent(cfg: Config) -> dict:
    """若无 sifile 且本机装有 Fluent,拉起官方 Launcher 对话框(-sifile 模式)。"""
    if FluentMCPBackend.discover_sifile(cfg.sifile_dir) is not None:
        return {"launched": False, "reason": "已有 Fluent 会话（sifile 存在）"}
    global FLUENT_EXE
    if FLUENT_EXE is None:
        FLUENT_EXE = (
            Path(cfg.fluent_exe)
            if cfg.fluent_exe and Path(cfg.fluent_exe).is_file()
            else find_fluent_exe()
        )
    if FLUENT_EXE is None or not FLUENT_EXE.exists():
        return {
            "launched": False,
            "reason": "未找到 fluent.exe:请在 config.toml 的 [fluent] fluent_exe 填写路径,或手动启动 Fluent 并加 -sifile 参数",
        }
    cfg.sifile_dir.mkdir(parents=True, exist_ok=True)
    subprocess.Popen(
        [str(FLUENT_EXE), f"-sifile={cfg.sifile_dir / 'serverinfo.txt'}"],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    return {"launched": True}


class AppState:
    """进程级共享状态：配置、agent 单例、忙碌位。"""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        Vault.default_root = cfg.vault_path
        self.gateway = LLMGateway(cfg)
        self.agent = Agent(
            self.gateway,
            max_rounds=cfg.max_tool_rounds,
            trajectory_file=cfg.log_dir / "trajectory.jsonl",
        )
        self.busy = False


def create_app(cfg: Config | None = None, state: AppState | None = None) -> FastAPI:
    cfg = cfg or load_config()
    if state is None:
        state = AppState(cfg)
    elif state.cfg is not cfg:
        state = AppState(cfg)

    app = FastAPI(title="Fluent Copilot", docs_url=None, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # 聊天（SSE）
    # ------------------------------------------------------------------
    @app.post("/api/chat")
    async def chat(request: Request):
        if state.busy:
            return StreamingResponse(
                iter([_sse({"type": "error", "message": "Copilot 正忙，请等当前回答完成。"}),
                      _sse({"type": "done"})]),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
            )
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "invalid json"}, status_code=400)
        messages = body.get("messages")
        if not isinstance(messages, list) or not messages:
            return JSONResponse({"error": "messages 不能为空"}, status_code=400)
        if messages[-1].get("role") != "user":
            return JSONResponse({"error": "messages 末条必须是 user"}, status_code=400)

        history = [dict(m) for m in messages[:-1]]
        user_input = str(messages[-1].get("content") or "")
        queue: asyncio.Queue[dict] = asyncio.Queue()
        cancelled = False

        def emit(event: dict) -> None:
            queue.put_nowait(event)

        async def runner() -> None:
            nonlocal cancelled
            try:
                await state.agent.arun(
                    history,
                    user_input,
                    emit=emit,
                    is_cancelled=lambda: cancelled,
                )
            except CancelledError:
                emit({"type": "cancelled"})
            except asyncio.CancelledError:
                emit({"type": "cancelled"})
            except Exception as exc:
                logger.exception("agent arun failed")
                emit({"type": "error", "message": f"{type(exc).__name__}: {exc}"})
            finally:
                emit({"type": "done"})

        async def stream():
            nonlocal cancelled
            state.busy = True
            task = asyncio.create_task(runner())
            try:
                while True:
                    try:
                        event = await asyncio.wait_for(queue.get(), timeout=1.0)
                    except asyncio.TimeoutError:
                        if await request.is_disconnected():
                            cancelled = True
                            continue
                        continue
                    yield _sse(event)
                    if event["type"] == "done":
                        break
            except asyncio.CancelledError:
                cancelled = True
                raise
            finally:
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except (asyncio.CancelledError, Exception):
                        pass
                state.busy = False

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )

    # ------------------------------------------------------------------
    # 状态 / 工具清单
    # ------------------------------------------------------------------
    @app.get("/api/status")
    async def status():
        sifile = FluentMCPBackend.discover_sifile(state.cfg.sifile_dir)
        return {
            "fluent_ready": sifile is not None,
            "sifile": str(sifile) if sifile else None,
            "model": state.gateway.model,
            "models": state.cfg.llm_models,
            "busy": state.busy,
            "configured": bool(state.gateway.api_key),
        }

    @app.post("/api/model")
    async def set_model(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "invalid json"}, status_code=400)
        model = body.get("model")
        if model not in state.cfg.llm_models:
            return JSONResponse(
                {"error": f"未知模型：{model}（可用：{state.cfg.llm_models}）"},
                status_code=400,
            )
        old = state.gateway.model
        state.gateway.model = model
        logger.info("model switched: %s -> %s", old, model)
        return {"model": model}

    # ------------------------------------------------------------------
    # API 设置（LLM 端点 / 密钥 / 模型列表）
    # ------------------------------------------------------------------
    @app.get("/api/providers")
    async def providers():
        return PROVIDER_PRESETS

    @app.get("/api/settings")
    async def get_settings():
        return {
            "provider": _match_provider(state.cfg.llm_base_url),
            "base_url": state.cfg.llm_base_url,
            "api_key": state.cfg.api_key,
            "model": state.gateway.model,
            "models": state.cfg.llm_models,
        }

    @app.post("/api/settings")
    async def save_settings(request: Request):
        if state.busy:
            return JSONResponse({"error": "Copilot 正忙，请等当前回答完成后再改设置"}, status_code=409)
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "invalid json"}, status_code=400)

        base_url = str(body.get("base_url") or "").strip().rstrip("/")
        api_key = str(body.get("api_key") or "").strip()
        models = [str(m).strip() for m in body.get("models") or [] if str(m).strip()]
        model = str(body.get("model") or "").strip()

        if not base_url.startswith(("http://", "https://")):
            return JSONResponse({"error": "API 地址必须以 http(s):// 开头"}, status_code=400)
        if not api_key:
            return JSONResponse({"error": "API Key 不能为空"}, status_code=400)
        if not models:
            return JSONResponse({"error": "模型列表至少要有一个模型"}, status_code=400)
        if model not in models:
            model = models[0]

        # 先校验再应用：热更新网关（下一轮生效），再写回 config.toml
        state.gateway.update(base_url, api_key, model)
        state.cfg.llm_base_url = base_url
        state.cfg.api_key = api_key
        state.cfg.llm_model = model
        state.cfg.llm_models = models
        try:
            from fluent_copilot.config import save_config

            path = save_config(state.cfg)
            logger.info("settings saved -> %s (model=%s, models=%s)", path, model, models)
        except Exception as exc:
            logger.exception("save_config failed")
            return JSONResponse(
                {"error": f"已热生效但写回 config.toml 失败：{exc}", "model": model},
                status_code=500,
            )
        return {"ok": True, "model": model, "models": models}

    @app.get("/api/tools")
    async def list_tools():
        return [
            {"name": s["function"]["name"], "description": s["function"]["description"]}
            for s in tools.openai_schemas()
        ]

    # ------------------------------------------------------------------
    # 本机动作
    # ------------------------------------------------------------------
    @app.post("/api/launch-fluent")
    async def launch_fluent():
        return maybe_launch_fluent(state.cfg)

    @app.post("/api/open-trajectory")
    async def open_trajectory():
        path = state.cfg.log_dir / "trajectory.jsonl"
        path.touch(exist_ok=True)
        subprocess.Popen(["notepad", str(path)])
        return {"opened": True, "path": str(path)}

    # ------------------------------------------------------------------
    # 对话历史(data/threads/{id}.json)
    # ------------------------------------------------------------------
    import re
    import time as _time

    _TID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")

    def _threads_dir() -> Path:
        d = Path(state.cfg.threads_dir)
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _thread_path(tid: str) -> Path:
        if not _TID_RE.match(tid):
            raise ValueError(f"非法线程 id:{tid}")
        return _threads_dir() / f"{tid}.json"

    @app.get("/api/threads")
    async def list_threads():
        out = []
        for p in _threads_dir().glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                out.append({
                    "id": data.get("id") or p.stem,
                    "title": data.get("title") or "(无标题)",
                    "updated_at": data.get("updated_at") or _time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "message_count": len(data.get("messages") or []),
                })
            except Exception:
                continue
        out.sort(key=lambda t: t["updated_at"], reverse=True)
        return out

    @app.get("/api/threads/{tid}")
    async def get_thread(tid: str):
        try:
            p = _thread_path(tid)
        except ValueError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)
        if not p.is_file():
            return JSONResponse({"error": "对话不存在"}, status_code=404)
        return json.loads(p.read_text(encoding="utf-8"))

    @app.post("/api/threads")
    async def upsert_thread(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "invalid json"}, status_code=400)
        tid = str(body.get("id") or "")
        if not _TID_RE.match(tid):
            return JSONResponse({"error": "非法线程 id"}, status_code=400)
        messages = body.get("messages")
        if not isinstance(messages, list):
            return JSONResponse({"error": "messages 必须是数组"}, status_code=400)
        now = _time.strftime("%Y-%m-%dT%H:%M:%S")
        p = _thread_path(tid)
        existing = {}
        if p.is_file():
            try:
                existing = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                existing = {}
        record = {
            "id": tid,
            "title": str(body.get("title") or existing.get("title") or "(无标题)")[:64],
            "created_at": existing.get("created_at") or now,
            "updated_at": now,
            "messages": messages,
        }
        p.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "id": tid}

    @app.delete("/api/threads/{tid}")
    async def delete_thread(tid: str):
        try:
            p = _thread_path(tid)
        except ValueError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)
        if p.is_file():
            p.unlink()
        return {"ok": True}

    # ------------------------------------------------------------------
    # 知识沉淀(把对话答案写成 vault 页,search_wiki 立即可命中)
    # ------------------------------------------------------------------
    @app.post("/api/knowledge")
    async def save_note(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "invalid json"}, status_code=400)
        title = str(body.get("title") or "").strip()[:60]
        question = str(body.get("question") or "").strip()
        answer = str(body.get("answer") or "").strip()
        if not title or not answer:
            return JSONResponse({"error": "标题和解答不能为空"}, status_code=400)

        notes_dir = state.cfg.vault_path / "wiki" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r'[\\/:*?"<>|#^\[\]]+', "_", title).strip().rstrip(".")
        if not safe:
            return JSONResponse({"error": "标题包含非法字符"}, status_code=400)
        path = notes_dir / f"{safe}.md"
        i = 2
        while path.exists():
            path = notes_dir / f"{safe}-{i}.md"
            i += 1
        content = (
            f"# {title}\n\n"
            f"## 问题\n\n{question or '(见解答)'}\n\n"
            f"## 解答\n\n{answer}\n\n"
            f"> 来源:Copilot 对话沉淀 {_time.strftime('%Y-%m-%d %H:%M')}\n"
        )
        path.write_text(content, encoding="utf-8")
        logger.info("knowledge note saved -> %s", path)
        return {"ok": True, "path": str(path)}

    # ------------------------------------------------------------------
    # 前端静态托管(生产模式;dist 存在才挂载)
    # ------------------------------------------------------------------
    if FRONTEND_DIST.is_dir():
        app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

        @app.get("/")
        async def index():
            return _file_response(FRONTEND_DIST / "index.html")

    return app


def _file_response(path: Path):
    from fastapi.responses import FileResponse

    return FileResponse(path, media_type="text/html")
