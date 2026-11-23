"""配置加载与路径解析。

两种运行形态:
- 开发:项目根 = 包上级目录,config/logs/data 都在项目内(CWD 优先)。
- 打包(PyInstaller frozen):程序与只读资源在 exe 目录(vault/dist 随包分发);
  用户数据(config.toml/logs/data)优先写在 exe 相邻目录(便携模式),
  若不可写(如装进 Program Files)则回退 %APPDATA%/FluentCopilot。
首次启动(打包形态)自动生成默认 config.toml,引导用户在界面里填 API Key。
"""

from __future__ import annotations

import os
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

_API_KEY_ENV = "FLUENT_COPILOT_API_KEY"

DEFAULT_CONFIG_TEMPLATE = """# Fluent Copilot 配置。密钥也可用环境变量 FLUENT_COPILOT_API_KEY。

[llm]
provider = "zhipu"
base_url = "https://open.bigmodel.cn/api/paas/v4/"
model = "glm-4.6"
# 模型选择器候选列表(切换在输入区底部,下一轮对话生效)
models = ["glm-4.6", "glm-4.5", "glm-4.5-air", "glm-4-flash"]
api_key = ""

[knowledge]
vault_path = '{vault_path}'

[fluent]
sifile_dir = '%TEMP%/fluent-copilot'
# fluent.exe 路径留空则自动在常见安装位置发现
fluent_exe = ''

[app]
log_dir = '{log_dir}'
max_tool_rounds = 30
threads_dir = '{threads_dir}'

[server]
host = '127.0.0.1'
port = 8765
"""


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def app_root() -> Path:
    """程序与只读资源根:打包后 exe 所在目录;开发时项目根。"""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def bundle_root() -> Path:
    """随包分发的只读资源根(onedir 下 PyInstaller 把 datas 放在 _internal)。"""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", sys.executable))
    return Path(__file__).resolve().parent.parent


def user_root() -> Path:
    """用户可写数据根:便携优先(exe 相邻),不可写则 %APPDATA%/FluentCopilot。"""
    if is_frozen():
        beside = app_root()
        probe = beside / ".write-test"
        try:
            probe.touch()
            probe.unlink()
            return beside
        except OSError:
            pass
        appdata = Path(os.environ.get("APPDATA") or Path.home()) / "FluentCopilot"
        appdata.mkdir(parents=True, exist_ok=True)
        return appdata
    return Path(__file__).resolve().parent.parent


@dataclass
class Config:
    llm_base_url: str
    llm_model: str
    llm_models: list[str]
    api_key: str
    vault_path: Path
    sifile_dir: Path
    fluent_exe: str
    log_dir: Path
    max_tool_rounds: int
    server_host: str
    server_port: int
    threads_dir: Path


def _config_candidates() -> list[Path]:
    if is_frozen():
        return [user_root() / "config.toml"]
    return [Path.cwd() / "config.toml", Path(__file__).resolve().parent.parent / "config.toml"]


def _ensure_first_run_config() -> None:
    """打包形态首次启动:生成默认 config.toml(资源路径按打包布局预填)。"""
    if not is_frozen():
        return
    target = _config_candidates()[0]
    if target.is_file():
        return
    u = user_root()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        DEFAULT_CONFIG_TEMPLATE.format(
            vault_path=str(bundle_root() / "copilot_lib"),
            log_dir=str(u / "logs"),
            threads_dir=str(u / "data" / "threads"),
        ),
        encoding="utf-8",
    )


def load_config(path: str | Path | None = None) -> Config:
    _ensure_first_run_config()

    candidates = (
        [Path(path)] if path else _config_candidates()
    )
    raw: dict = {}
    for c in candidates:
        if c.is_file():
            with open(c, "rb") as f:
                raw = tomllib.load(f)
            break

    def sub(table: str) -> dict:
        return raw.get(table, {})

    def expand(p: str) -> Path:
        return Path(os.path.expandvars(os.path.expanduser(p))).resolve()

    u = user_root()
    frozen = is_frozen()
    api_key = sub("llm").get("api_key") or os.environ.get(_API_KEY_ENV, "")
    model = sub("llm").get("model", "glm-4.6")
    models = [str(m) for m in sub("llm").get("models", [])] or [model]
    if model not in models:
        models.insert(0, model)
    return Config(
        llm_base_url=sub("llm").get("base_url", "https://open.bigmodel.cn/api/paas/v4/"),
        llm_model=model,
        llm_models=models,
        api_key=api_key,
        vault_path=expand(
            sub("knowledge").get("vault_path", str(bundle_root() / "copilot_lib" if frozen else "./copilot_lib"))
        ),
        sifile_dir=expand(sub("fluent").get("sifile_dir", "%TEMP%/fluent-copilot")),
        fluent_exe=str(sub("fluent").get("fluent_exe", "")),
        log_dir=expand(sub("app").get("log_dir", str(u / "logs" if frozen else "./logs"))),
        max_tool_rounds=int(sub("app").get("max_tool_rounds", 30)),
        threads_dir=expand(
            sub("app").get("threads_dir", str(u / "data" / "threads" if frozen else "./data/threads"))
        ),
        server_host=sub("server").get("host", "127.0.0.1"),
        server_port=int(sub("server").get("port", 8765)),
    )


def _t(s: str) -> str:
    """TOML 基本字符串转义(与 JSON 转义集一致)。"""
    import json

    return json.dumps(s, ensure_ascii=False)


def save_config(cfg: Config, path: str | Path | None = None) -> Path:
    """把配置写回 config.toml(按固定模板重生成,含注释)。"""
    candidates = [Path(path)] if path else _config_candidates()
    target = next((c for c in candidates if c.is_file()), candidates[0])
    models = ", ".join(_t(m) for m in cfg.llm_models)
    content = f"""# 本文件不进 git(见 .gitignore)。密钥也可改用环境变量 FLUENT_COPILOT_API_KEY。

[llm]
provider = "glm"
base_url = {_t(cfg.llm_base_url)}
model = {_t(cfg.llm_model)}
# 模型选择器候选列表（切换在输入区底部，下一轮对话生效）
models = [{models}]
api_key = {_t(cfg.api_key)}

[knowledge]
vault_path = {_t(str(cfg.vault_path))}

[fluent]
sifile_dir = {_t(str(cfg.sifile_dir))}
fluent_exe = {_t(cfg.fluent_exe)}

[app]
log_dir = {_t(str(cfg.log_dir))}
max_tool_rounds = {cfg.max_tool_rounds}
threads_dir = {_t(str(cfg.threads_dir))}

[server]
host = {_t(cfg.server_host)}
port = {cfg.server_port}
"""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return target
