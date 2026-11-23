"""桌面壳：pywebview 侧边栏窗口 + pystray 系统托盘。

窗口形态复刻旧版 PySide6 面板：440px 宽、屏幕高 92%、贴右缘垂直居中、
无边框置顶。顶栏拖拽由前端 shell.ts 调 js_api.move_by 实现（不用 easy_drag，
以免拖拽与文本选中冲突）；Esc 收起 = hide，托盘负责唤回与退出。
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Callable

import webview

from fluent_copilot.config import Config
from fluent_copilot.fluent.mcp_backend import FluentMCPBackend

logger = logging.getLogger(__name__)

PANEL_WIDTH = 440

STATUS_COLORS = {
    "idle": (82, 82, 91),     # #52525b
    "ready": (245, 158, 11),  # #f59e0b
    "busy": (59, 130, 246),   # #3b82f6
}
STATUS_TOOLTIPS = {
    "idle": "Fluent Copilot（Fluent 未检测到）",
    "ready": "Fluent Copilot（Fluent 会话已就绪）",
    "busy": "Fluent Copilot（思考中…）",
}


def _make_tray_image(status: str):
    """托盘图标：蓝底圆 + 白色 F + 状态色点。"""
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 2, 62, 62], fill=(37, 99, 235, 255))  # #2563eb
    d.text((22, 14), "F", fill=(255, 255, 255, 255))
    color = STATUS_COLORS.get(status, STATUS_COLORS["idle"])
    d.ellipse([44, 44, 61, 61], fill=color + (255,), outline=(15, 15, 15, 255), width=3)
    return img


class ShellApi:
    """暴露给前端 JS 的桥（window.pywebview.api.*）。"""

    def __init__(self, window_provider: Callable[[], "webview.Window | None"], state: dict):
        self._window_provider = window_provider
        self._state = state

    def hide_window(self) -> None:
        win = self._window_provider()
        if win:
            self._state["visible"] = False
            win.hide()

    def move_by(self, dx: float, dy: float) -> None:
        win = self._window_provider()
        if not win:
            return
        try:
            win.move(int(win.x + dx), int(win.y + dy))
        except Exception as exc:  # 拖拽不因异常中断
            logger.debug("move_by failed: %s", exc)


def run_shell(
    url: str,
    cfg: Config,
    is_busy: Callable[[], bool],
    launch_fluent: Callable[[], None],
) -> None:
    """启动主窗口 + 托盘，阻塞直到窗口关闭。"""
    import pystray

    screen = webview.screens[0]
    height = int(screen.height * 0.92)
    x = screen.width - PANEL_WIDTH
    y = max(0, (screen.height - height) // 2)

    state: dict = {"win": None, "visible": True}
    api = ShellApi(lambda: state["win"], state)

    win = webview.create_window(
        title="Fluent Copilot",
        url=url,
        js_api=api,
        width=PANEL_WIDTH,
        height=height,
        x=x,
        y=y,
        resizable=False,
        frameless=True,
        on_top=True,
        easy_drag=False,
        background_color="#0f0f0f",
    )
    state["win"] = win

    # ---------------- 托盘 ----------------
    def current_status() -> str:
        if is_busy():
            return "busy"
        sifile = FluentMCPBackend.discover_sifile(cfg.sifile_dir)
        return "ready" if sifile is not None else "idle"

    def toggle_window(icon=None, item=None) -> None:
        w = state["win"]
        if w is None:
            return
        if state["visible"]:
            state["visible"] = False
            w.hide()
        else:
            state["visible"] = True
            w.show()

    def quit_app(icon=None, item=None) -> None:
        icon.stop()
        w = state["win"]
        if w is not None:
            try:
                w.destroy()
            except Exception:
                pass

    menu = pystray.Menu(
        pystray.MenuItem("打开聊天框", toggle_window, default=True),
        pystray.MenuItem("启动 Fluent（Launcher）", lambda icon, item: launch_fluent()),
        pystray.MenuItem("退出", quit_app),
    )
    status = current_status()
    icon = pystray.Icon(
        "fluent-copilot",
        icon=_make_tray_image(status),
        title=STATUS_TOOLTIPS[status],
        menu=menu,
    )

    def poll_status() -> None:
        last = status
        while True:
            time.sleep(3)
            cur = current_status()
            if cur != last:
                last = cur
                icon.icon = _make_tray_image(last)
                icon.title = STATUS_TOOLTIPS[last]

    threading.Thread(target=poll_status, daemon=True).start()
    threading.Thread(target=icon.run, daemon=True).start()

    logger.info("shell window: %sx%s at (%s,%s) -> %s", PANEL_WIDTH, height, x, y, url)
    webview.start()  # 阻塞主线程直到窗口销毁
    icon.stop()
