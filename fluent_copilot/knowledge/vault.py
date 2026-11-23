"""知识库层：直接以 Obsidian vault（copilot_lib）为知识源。

vault 规模小（几十页）时，"检索页名 → 读整页 → 沿 [[wikilink]] 跳转"
优于向量切块检索：上下文完整、零索引维护成本、vault 更新即时生效。
语料涨到数百页以上时再引入向量库（LanceDB）做混合检索。
"""
from __future__ import annotations

import re
from pathlib import Path

_FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
_WIKILINK = re.compile(r"\[\[([^\]|#]+)")


class Vault:
    # __main__ 启动时注入，供 tools.py 取默认实例
    default_root: Path | None = None

    def __init__(self, root: Path):
        self.root = root
        self._pages: dict[str, Path] = {}
        self.reload()

    def reload(self) -> int:
        """重新扫描（vault 内容变化后可调用，无索引重建成本）。"""
        self._pages.clear()
        wiki = self.root / "wiki"
        if wiki.is_dir():
            for p in wiki.rglob("*.md"):
                self._pages[p.stem] = p
        index = self.root / "index.md"
        if index.is_file():
            self._pages.setdefault("index", index)
        return len(self._pages)

    def titles(self) -> list[str]:
        return sorted(self._pages)

    def _resolve(self, title: str) -> Path | None:
        if title in self._pages:
            return self._pages[title]
        low = title.strip().lower()
        for key, path in self._pages.items():
            if key.lower() == low:
                return path
        for key, path in self._pages.items():
            if low in key.lower():
                return path
        return None

    def _text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="replace")

    def read(self, title: str, max_chars: int = 6000) -> dict:
        """读整页；返回正文（截断）、来源 frontmatter 内的 wikilink、可跳转链接。"""
        path = self._resolve(title)
        if path is None:
            return {
                "error": f"未找到页面：{title!r}",
                "hint": "先用 search_wiki 按关键词找页面标题",
            }
        text = self._text(path)
        links = sorted({m.group(1).strip() for m in _WIKILINK.finditer(text)})
        return {
            "title": path.stem,
            "content": text[:max_chars],
            "wikilinks": links[:30],
            "truncated": len(text) > max_chars,
        }

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """关键词计分检索：标题命中权重 ×3。中文按整词子串计数，无需分词。"""
        terms = [t for t in re.split(r"[\s,，、;；]+", query) if t]
        scored: list[tuple[int, str]] = []
        for title, path in self._pages.items():
            try:
                text = self._text(path)
            except OSError:
                continue
            score = 0
            for t in terms:
                tl = t.lower()
                score += 3 * title.lower().count(tl) + text.lower().count(tl)
            if score > 0:
                scored.append((score, title))
        scored.sort(reverse=True)

        results = []
        for score, title in scored[:top_k]:
            text = _FRONTMATTER.sub("", self._text(self._pages[title]))
            m = re.search(r"^#{1,2}\s*摘要\s*\n\s*(.+)", text, re.M)
            if m:
                summary = m.group(1).strip()
            else:
                summary = next(
                    (l.strip("# ").strip() for l in text.splitlines()
                     if l.strip() and not l.startswith("---")),
                    "",
                )
            results.append({"title": title, "score": score, "summary": summary[:150]})
        return results


_default: Vault | None = None


def _default_vault() -> Vault:
    global _default
    if _default is None:
        root = Vault.default_root or Path(__file__).resolve().parent.parent.parent / "copilot_lib"
        _default = Vault(root)
    return _default
