"""transcript watcher：定位并读取当前 Fluent 会话的 .trn 文件。

不依赖 pyfluent 的 transcript 流（那是给监控 UI 的空转发）——.trn 文件是
Fluent 自己写出的地面真相，未附着时也可用（只读降级模式的基础）。

定位策略：psutil 找 fluent*.exe 进程的工作目录（trn 写在启动时的 cwd），
兜底扫描候选目录里最新的 fluent-*.trn。
"""
from __future__ import annotations

import re
from pathlib import Path

_ERROR_PAT = re.compile(r"error", re.I)
_WARNING_PAT = re.compile(r"warning", re.I)
_COMMAND_PAT = re.compile(r"^\s*(>|\()")
_EMPTY = re.compile(r"^\s*$")


class TranscriptWatcher:
    def __init__(self, extra_dirs: list[Path] | None = None):
        self._extra_dirs = [Path(d) for d in (extra_dirs or [])]
        self._path: Path | None = None
        self._offset = 0  # poll() 的增量读取偏移

    # ------------------------------------------------------------------ 定位

    def locate(self, refresh: bool = False) -> Path | None:
        """返回当前会话的 .trn 路径；切换到新文件时重置增量偏移。"""
        if self._path and self._path.exists() and not refresh:
            return self._path

        candidates: list[Path] = []
        try:
            import psutil

            for proc in psutil.process_iter(["name"]):
                name = (proc.info["name"] or "").lower()
                if name.startswith("fluent"):
                    try:
                        candidates.append(Path(proc.cwd()))
                    except Exception:
                        pass
        except ImportError:
            pass
        candidates.extend(self._extra_dirs)
        candidates.extend([Path.cwd(), Path.home()])

        best: tuple[float, Path] | None = None
        for d in dict.fromkeys(candidates):  # 去重保序
            try:
                files = list(Path(d).glob("fluent-*.trn"))
            except OSError:
                continue
            for f in files:
                try:
                    mtime = f.stat().st_mtime
                except OSError:
                    continue
                if best is None or mtime > best[0]:
                    best = (mtime, f)

        if best is None:
            return None
        found = best[1]
        if found != self._path:
            self._offset = 0  # 新会话的 trn，从零开始
        self._path = found
        return self._path

    # ------------------------------------------------------------------ 读取

    @staticmethod
    def _decode(data: bytes) -> str:
        """中文 Windows 上 Fluent 会混写本地编码（GBK），乱码行用 replace 兜底。"""
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("gbk", errors="replace")

    def poll(self, max_lines: int = 200) -> list[str]:
        """增量返回自上次调用以来的新行（未来做主动通知时用）。"""
        path = self.locate()
        if path is None:
            return []
        size = path.stat().st_size
        if size < self._offset:
            self._offset = 0  # 文件被截断/轮转
        if size <= self._offset:
            return []
        with open(path, "rb") as f:
            f.seek(self._offset)
            data = f.read()
        self._offset = size
        lines = [l for l in self._decode(data).splitlines() if not _EMPTY.match(l)]
        return lines[-max_lines:]

    def read(
        self,
        what: str = "tail",
        max_lines: int = 50,
        max_chars: int = 5000,
    ) -> dict:
        """读取 transcript。what: tail=最近若干行；errors/warnings/commands=按类型过滤全文件。"""
        path = self.locate()
        if path is None:
            return {
                "error": "未找到 .trn 文件（Fluent 可能未运行，或启动目录无法定位）",
                "hint": "确认 Fluent 正在运行；也可告诉我它从哪个目录启动的",
            }
        lines = self._decode(path.read_bytes()).splitlines()
        nonempty = [l.rstrip() for l in lines if not _EMPTY.match(l)]

        if what == "tail":
            selected = nonempty[-max_lines:]
        elif what == "errors":
            selected = [l for l in nonempty if _ERROR_PAT.search(l)][:max_lines]
        elif what == "warnings":
            selected = [l for l in nonempty if _WARNING_PAT.search(l)][:max_lines]
        elif what == "commands":
            selected = [l for l in nonempty if _COMMAND_PAT.match(l)][:max_lines]
        else:
            selected = nonempty[:max_lines]

        text = "\n".join(selected)
        return {
            "file": str(path),
            "total_lines": len(nonempty),
            "what": what,
            "count": len(selected),
            "content": text[:max_chars],
            "truncated": len(text) > max_chars,
        }


_default: TranscriptWatcher | None = None


def _default_watcher() -> TranscriptWatcher:
    global _default
    if _default is None:
        _default = TranscriptWatcher()
    return _default
