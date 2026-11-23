"""工具注册表：三大部分（知识库/Fluent/转录）对 agent 的统一暴露形式。

每个工具 = 一个 Python 函数 + 一段 OpenAI function schema。
新增能力 = 在这里注册，agent 和其他模块零改动。

Fluent 工具是 async 的（底层是 pyfluent-mcp 官方异步后端）；
知识库/转录工具保持同步，dispatch_async 会用 to_thread 卸载，避免阻塞事件循环。
"""
from __future__ import annotations

import asyncio
import inspect
import json
from typing import Any, Callable

_REGISTRY: dict[str, tuple[Callable, dict]] = {}


def tool(name: str, description: str, params: dict) -> Callable:
    def deco(fn: Callable) -> Callable:
        _REGISTRY[name] = (fn, {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": params,
            },
        })
        return fn

    return deco


def openai_schemas() -> list[dict]:
    return [schema for _, schema in _REGISTRY.values()]


def names() -> list[str]:
    return list(_REGISTRY)


def _parse_args(arguments_json: str) -> tuple[dict[str, Any] | None, str | None]:
    """解析参数 JSON；出错返回 (None, 错误信息)。"""
    if not arguments_json or not arguments_json.strip():
        return {}, None
    try:
        args = json.loads(arguments_json)
        return (args if isinstance(args, dict) else {}, None)
    except json.JSONDecodeError as exc:
        return None, f"invalid arguments: {exc}"


def dispatch(name: str, arguments_json: str) -> str:
    """同步分发（仅限同步工具；async 工具会报错）。agent 主路径走 dispatch_async。"""
    if name not in _REGISTRY:
        return json.dumps({"error": f"unknown tool: {name}"}, ensure_ascii=False)
    fn, _ = _REGISTRY[name]
    if inspect.iscoroutinefunction(fn):
        return json.dumps(
            {"error": f"tool {name} is async; use dispatch_async"}, ensure_ascii=False
        )
    args, err = _parse_args(arguments_json)
    if err:
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        return json.dumps(fn(**args), ensure_ascii=False, default=str)
    except Exception as exc:
        return json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False)


async def dispatch_async(name: str, arguments_json: str) -> str:
    """异步分发：async 工具直接 await，同步工具 to_thread 卸载。

    永远返回字符串（出错也返回错误 JSON，喂回给模型）。
    """
    if name not in _REGISTRY:
        return json.dumps({"error": f"unknown tool: {name}"}, ensure_ascii=False)
    fn, _ = _REGISTRY[name]
    args, err = _parse_args(arguments_json)
    if err:
        return json.dumps({"error": err}, ensure_ascii=False)
    try:
        if inspect.iscoroutinefunction(fn):
            result = await fn(**args)
        else:
            result = await asyncio.to_thread(fn, **args)
        return json.dumps(result, ensure_ascii=False, default=str)
    except Exception as exc:
        return json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Fluent 工具（基于 pyfluent-mcp 官方后端，async）
# ---------------------------------------------------------------------------

async def _get_mcp_async() -> "FluentMCPBackend | dict":
    """取后端单例；未连接则自动按 sifile 附着。失败返回 error dict（与后端同型）。"""
    from fluent_copilot.fluent.mcp_backend import FluentMCPBackend
    from fluent_copilot.config import load_config

    cfg = load_config()
    backend = FluentMCPBackend.get_default()
    if not backend.is_connected:
        sifile = FluentMCPBackend.discover_sifile(cfg.sifile_dir)
        if sifile is None:
            return {"error": "未找到 Fluent 会话（无 sifile）。请先通过 start-fluent-copilot.bat 启动 Fluent。", "connected": False}
        try:
            await backend.connect_via_sifile(cfg.sifile_dir)
        except Exception as exc:
            FluentMCPBackend.reset_default()
            return {"error": f"连接失败: {exc}", "connected": False}
    return backend


@tool(
    "get_fluent_state",
    "获取本机 Fluent 会话的当前状态。返回连接状态、求解器信息、物理模型设置等。"
    "这是了解当前仿真配置的主要入口。",
    {
        "type": "object",
        "properties": {
            "paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "要读取的 settings 路径列表，为空则返回默认全局状态"
                               "（求解器类型/能量模型/粘性模型/边界条件等）",
            }
        },
        "required": [],
    },
)
async def get_fluent_state(paths: list[str] | None = None) -> dict:
    """读取 Fluent 会话状态（基于 pyfluent-mcp）。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    state = await mcp.get_state(paths=paths)
    status = mcp.get_status()
    solver = await mcp.get_solver_status()
    return {
        "session_status": status,
        "solver_status": solver,
        "settings_state": state,
    }


@tool(
    "execute_fluent_code",
    "在 Fluent 会话中执行 Python 代码（沙箱安全环境）。"
    "可用变量：solver（求解器对象）、session（会话对象）。"
    "适用于：初始化求解、修改边界条件、运行迭代、读取结果等操作。"
    "代码会在执行前经过安全校验（禁止系统调用/文件操作等危险操作）。",
    {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "要执行的 Python 代码，例如："
                               "'solver.solution.initialize.hybrid_initialize()' 或 "
                               "'solver.solution.run_calculation.iterate(iter_count=100)'",
            }
        },
        "required": ["code"],
    },
)
async def execute_fluent_code(code: str) -> dict:
    """在 Fluent 沙箱中执行代码（基于 pyfluent-mcp）。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    validation = await mcp.validate_code(code)
    if validation.get("status") == "error":
        return {
            "error": "代码安全校验未通过",
            "detail": validation.get("message") or validation.get("stderr") or "未知原因",
        }
    return await mcp.run_code(code)


@tool(
    "search_fluent_api",
    "搜索 Fluent Settings API schema。当你不确定某个设置的路径或名称时使用。"
    "例如搜索 'boundary' 可找到所有边界相关设置，搜索 'viscous' 找到粘性模型设置。",
    {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词，如：boundary, viscous, energy, pressure",
            }
        },
        "required": ["query"],
    },
)
async def search_fluent_api(query: str) -> dict:
    """搜索 Fluent API（基于 pyfluent-mcp）。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    return {"results": await mcp.find_api(query=query)}


@tool(
    "get_fluent_context",
    "写代码前必须先用这个工具确认路径!一次批量返回若干 settings 路径的"
    "激活状态、当前值、可选值和子对象名,是避免路径错误的关键。"
    "不确定路径结构、拿不到命名对象的真实名字时,把候选路径传进来查。",
    {
        "type": "object",
        "properties": {
            "paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "要核实的 settings 路径列表,如 "
                               "['setup/boundary_conditions', 'setup/models/energy']",
            }
        },
        "required": ["paths"],
    },
)
async def get_fluent_context(paths: list[str]) -> dict:
    """批量路径消歧(激活状态+当前值+可选值+子对象名,一次往返)。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    return await mcp.get_targeted_context(paths_to_check=paths)


@tool(
    "get_fluent_help",
    "获取指定 Fluent 设置路径的详细帮助文档。"
    "用于了解某个设置的具体含义、可选值、单位等信息。",
    {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Fluent settings 路径，例如："
                               "'setup/boundary_conditions/velocity_inlet' 或 "
                               "'setup/models/viscous'",
            }
        },
        "required": ["path"],
    },
)
async def get_fluent_help(path: str) -> dict:
    """获取 Fluent API 帮助（基于 pyfluent-mcp）。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    return await mcp.get_help(path=path)


@tool(
    "list_fluent_objects",
    "列出 Fluent 会话中的命名对象（边界条件、cell zone、surface、材料等）。"
    "用于了解当前 case 中定义了哪些对象及其名称。",
    {
        "type": "object",
        "properties": {},
        "required": [],
    },
)
async def list_fluent_objects() -> dict:
    """列出 Fluent 命名对象（基于 pyfluent-mcp）。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    return await mcp.list_named_objects()


@tool(
    "summarize_fluent_setup",
    "生成当前 Fluent 仿真的完整设置摘要。包括：求解器类型、物理模型、"
    "材料属性、边界条件、网格信息等。适合快速了解整体配置。",
    {
        "type": "object",
        "properties": {},
        "required": [],
    },
)
async def summarize_fluent_setup() -> dict:
    """生成 Fluent 仿真摘要（基于 pyfluent-mcp，等价 Report > Summary）。"""
    mcp = await _get_mcp_async()
    if isinstance(mcp, dict):
        return mcp
    return await mcp.summarize_setup()


# ---------------------------------------------------------------------------
# 操作配方库(自动沉淀的已验证代码,越用越准)
# ---------------------------------------------------------------------------

def _recipes_path() -> "Path":
    from fluent_copilot.config import load_config

    return load_config().threads_dir.parent / "recipes.jsonl"


def append_recipe(intent: str, code: str) -> None:
    """沉淀一条已验证配方(相同代码去重)。由 agent 在代码执行成功后调用。"""
    import time as _time

    p = _recipes_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    code = code.strip()
    if p.is_file():
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    if json.loads(line).get("code", "").strip() == code:
                        return
                except Exception:
                    continue
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(
            {"ts": _time.strftime("%Y-%m-%dT%H:%M:%S"), "intent": intent[:200], "code": code},
            ensure_ascii=False,
        ) + "\n")


@tool(
    "search_fluent_recipes",
    "搜索历史操作配方——过去在本机验证成功过的 execute_fluent_code 代码片段。"
    "写操作代码前先查这里:命中则直接复用/微调配方(对象名仍需与当前会话核对),"
    "未命中再走 search_fluent_api/get_fluent_context 发现流程。",
    {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "意图关键词,如:进口温度、迭代、能量方程、残差",
            }
        },
        "required": ["query"],
    },
)
def search_fluent_recipes(query: str) -> dict:
    p = _recipes_path()
    if not p.is_file():
        return {"recipes": [], "note": "配方库还是空的"}
    hits = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            hay = (r.get("intent", "") + "\n" + r.get("code", "")).lower()
            if any(k in hay for k in query.lower().split()):
                hits.append(r)
    hits = hits[-5:]  # 最新的优先保留
    for r in hits:
        if len(r.get("code", "")) > 800:
            r["code"] = r["code"][:800] + "…"
    return {"recipes": hits[::-1], "note": f"命中 {len(hits)} 条,复用前核对对象名"}


# ---------------------------------------------------------------------------
# 知识库工具（Obsidian vault：copilot_lib）
# ---------------------------------------------------------------------------

@tool(
    "search_wiki",
    "在本地 Fluent 知识库（Obsidian vault，摄取自官方 User's Guide/Tutorial Guide）中"
    "按关键词搜索页面，返回标题、相关度评分和摘要。",
    {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词，如：周期性边界、残差、GPU 求解器"},
            "top_k": {"type": "integer", "description": "返回条数，默认 5"},
        },
        "required": ["query"],
    },
)
def search_wiki(query: str, top_k: int = 5) -> dict:
    from fluent_copilot.knowledge.vault import _default_vault

    return {"results": _default_vault().search(query, top_k)}


@tool(
    "read_wiki_page",
    "读取知识库中一整页内容（含来源标注与 [[wikilink]]）。"
    "可通过 wikilinks 字段里的标题继续调用本工具跳转阅读。",
    {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "页面标题，来自 search_wiki 结果或 wikilinks 字段"},
            "max_chars": {"type": "integer", "description": "正文最大长度，默认 6000"},
        },
        "required": ["title"],
    },
)
def read_wiki_page(title: str, max_chars: int = 6000) -> dict:
    from fluent_copilot.knowledge.vault import _default_vault

    return _default_vault().read(title, max_chars)


# ---------------------------------------------------------------------------
# Transcript 工具（.trn 文件）
# ---------------------------------------------------------------------------

@tool(
    "read_transcript",
    "读取当前 Fluent 会话的 transcript（.trn 文件，记录了会话中的全部命令、"
    "输出、警告和错误）。用户报告仿真出错、结果异常、想复盘操作时用这个工具。"
    "what=tail 返回最近的行；errors/warnings/commands 全文件过滤对应类型的行。",
    {
        "type": "object",
        "properties": {
            "what": {
                "type": "string",
                "enum": ["tail", "errors", "warnings", "commands"],
                "description": "读取内容，默认 tail",
            },
            "max_lines": {"type": "integer", "description": "最多返回行数，默认 50"},
        },
        "required": [],
    },
)
def read_transcript(what: str = "tail", max_lines: int = 50) -> dict:
    from fluent_copilot.transcript.watcher import _default_watcher

    return _default_watcher().read(what=what, max_lines=max_lines)
