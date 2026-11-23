"""服务入口：python -m fluent_copilot.server [--browser] [--dev]

默认模式：uvicorn（线程）+ pywebview 侧边栏窗口（主线程）+ 系统托盘，单进程。
--browser  用系统浏览器打开（调试用，无窗口/托盘）
--dev      前端连 Vite dev server（需另开 npm run dev），默认连已构建的静态页
"""
from __future__ import annotations

import argparse
import socket
import sys
import threading
import time
import traceback
import webbrowser


def main() -> None:
    parser = argparse.ArgumentParser(description="Fluent Copilot UI 服务")
    parser.add_argument("--browser", action="store_true", help="用系统浏览器而非 pywebview 窗口")
    parser.add_argument("--dev", action="store_true", help="连 Vite dev server (5173)")
    args = parser.parse_args()

    from fluent_copilot.config import load_config
    from fluent_copilot.server.app import AppState, create_app, maybe_launch_fluent

    cfg = load_config()
    cfg.log_dir.mkdir(parents=True, exist_ok=True)

    # 未捕获异常落盘（pythonw 无控制台）
    def _hook(exc_type, exc, tb):
        with open(cfg.log_dir / "ui.log", "a", encoding="utf-8") as f:
            f.write("".join(traceback.format_exception(exc_type, exc, tb)) + "\n")

    sys.excepthook = _hook

    # 所有日志(httpx/pyfluent/自研模块)统一走 root logger 落文件。
    # 注意:某依赖在 import 时已给 root 装了 StreamHandler(stderr)——pythonw 下
    # stderr=None,那正是 stderr.log 里 16 万字节 "Logging error" 洪流的源头。
    # basicConfig 对已有 handler 的 root 是空操作,必须强制清空重建。
    import logging

    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
        h.close()
    _fh = logging.FileHandler(cfg.log_dir / "app.log", encoding="utf-8")
    _fh.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    root.addHandler(_fh)
    root.setLevel(logging.INFO)
    logging.getLogger(__name__).info("=== Fluent Copilot 启动 ===")

    # pythonw 无控制台时 sys.stdout/stderr 为 None,
    # uvicorn 的日志格式器会因 sys.stdout.isatty() 崩溃——重定向兜底
    import os

    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(cfg.log_dir / "stderr.log", "a", encoding="utf-8", buffering=1)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # 端口占用检查:已有实例在跑就不重复起
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        if probe.connect_ex((cfg.server_host, cfg.server_port)) == 0:
            url = f"http://{cfg.server_host}:{cfg.server_port}/"
            print(f"[server] 端口 {cfg.server_port} 已被占用（可能已有实例）：{url}")
            webbrowser.open(url)
            return

    state = AppState(cfg)
    app = create_app(cfg, state)

    import uvicorn

    # 旧实例刚退出时端口可能短暂残留(TIME_WAIT/关闭中),绑定失败自动重试
    server = None
    for attempt in range(3):
        server = uvicorn.Server(
            uvicorn.Config(app, host=cfg.server_host, port=cfg.server_port, log_level="warning")
        )
        threading.Thread(target=server.run, daemon=True, name="copilot-uvicorn").start()
        for _ in range(100):  # 最多等 10 秒
            if server.started or server.should_exit:
                break
            time.sleep(0.1)
        if server.started:
            break
        # 没起来:可能旧实例还在收尾——等 2 秒再试,若端口已有响应直接转浏览器
        time.sleep(2)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            if probe.connect_ex((cfg.server_host, cfg.server_port)) == 0:
                print("[server] 检测到其它实例已就绪,转为浏览器打开")
                webbrowser.open(f"http://{cfg.server_host}:{cfg.server_port}/")
                return
    if not server.started:
        msg = f"服务启动失败(端口 {cfg.server_port} 无法绑定),详见 logs/app.log"
        print(f"[server] {msg}", file=sys.stderr)
        logging.getLogger(__name__).error(msg)
        try:  # pythonw 下至少弹个窗,别静默消失
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, msg, "Fluent Copilot", 0x10)
        except Exception:
            pass
        return

    url = (
        "http://127.0.0.1:5173/"
        if args.dev
        else f"http://{cfg.server_host}:{cfg.server_port}/"
    )
    print(f"[server] {url}")

    # 启动时若无 Fluent 会话，自动拉起官方 Launcher（与旧版行为一致）
    maybe_launch_fluent(cfg)

    if args.browser:
        webbrowser.open(url)
        print("[server] 浏览器模式，Ctrl+C 退出")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
        return

    from fluent_copilot.server.shell import run_shell

    run_shell(
        url,
        cfg,
        is_busy=lambda: state.busy,
        launch_fluent=lambda: maybe_launch_fluent(cfg),
    )
    print("[server] 窗口已关闭，退出")


if __name__ == "__main__":
    main()
