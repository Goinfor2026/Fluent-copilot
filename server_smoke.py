# -*- coding: utf-8 -*-
"""服务层冒烟测试：headless 起 FastAPI，验证 /api/status、/api/tools、/api/chat SSE 闭环。

用法：.venv\\Scripts\\python server_smoke.py
"""
import json
import sys
import threading
import time

import httpx
import uvicorn

from fluent_copilot.config import load_config
from fluent_copilot.server.app import create_app

PORT = 8766


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    cfg = load_config()
    app = create_app(cfg)
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    )
    threading.Thread(target=server.run, daemon=True).start()

    base = f"http://127.0.0.1:{PORT}"
    with httpx.Client(base_url=base, timeout=240.0) as client:
        for _ in range(50):  # 等服务就绪
            try:
                client.get("/api/status")
                break
            except httpx.ConnectError:
                time.sleep(0.1)

        r = client.get("/api/status")
        assert r.status_code == 200, r.text
        status = r.json()
        assert {"fluent_ready", "sifile", "model", "busy"} <= set(status), status
        print(f"[status] {status}")

        r = client.get("/api/tools")
        tool_names = [t["name"] for t in r.json()]
        assert len(tool_names) == 9, tool_names
        print(f"[tools] {tool_names}")

        question = "在知识库里查一下'周期性边界'是什么，两三句话概括即可。"
        events = []
        current = None
        with client.stream(
            "POST", "/api/chat", json={"messages": [{"role": "user", "content": question}]}
        ) as resp:
            assert resp.status_code == 200, resp.read()
            for line in resp.iter_lines():
                if not line.startswith("data: "):
                    continue
                ev = json.loads(line[len("data: "):])
                events.append(ev["type"])
                if ev["type"] == "text_delta":
                    current = (current or "") + ev["content"]
                elif ev["type"] == "final":
                    current = ev["content"]
                elif ev["type"] == "error":
                    print(f"[error-event] {ev}")

        assert events[-1] == "done", events
        assert "text_delta" in events or "final" in events, events
        assert "error" not in events, events
        kinds = sorted(set(events))
        print(f"[chat] 事件种类: {kinds}（共 {len(events)} 条）")
        print(f"[chat] 回答预览: {current[:150]}...")
        print("PASS")


if __name__ == "__main__":
    main()
