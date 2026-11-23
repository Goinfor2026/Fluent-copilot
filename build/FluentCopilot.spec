# -*- mode: python ; coding: utf-8 -*-
"""Fluent Copilot PyInstaller 打包配置(onedir + 窗口模式)。

用法:.venv\\Scripts\\pyinstaller build/FluentCopilot.spec --noconfirm
产物:dist/FluentCopilot/FluentCopilot.exe
"""
import os

from PyInstaller.utils.hooks import copy_metadata

block_cipher = None
project_root = os.path.abspath(os.path.join(SPECPATH, ".."))

datas = [
    (os.path.join(project_root, "frontend", "dist"), "frontend_dist"),
    (os.path.join(project_root, "copilot_lib"), "copilot_lib"),
    (os.path.join(project_root, "config.example.toml"), "."),
]

# ansys 系包在 import 时用 importlib.metadata 查版本,必须带上元数据
for _pkg in [
    "ansys-api-fluent",
    "ansys-api-platform-instancemanagement",
    "ansys-api-tools-filetransfer",
    "ansys-common-mcp",
    "ansys-fluent-core",
    "ansys-fluent-mcp",
    "ansys-platform-instancemanagement",
    "ansys-tools-common",
    "ansys-tools-filetransfer",
    "ansys-units",
    "httpx2",
]:
    try:
        datas += copy_metadata(_pkg)
    except Exception:
        pass

hiddenimports = [
    # uvicorn 动态导入
    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.http.httptools_impl",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    # 桌面壳
    "webview",
    "webview.platforms.winforms",
    "pystray",
    "pystray._win32",
    "clr",
    # 其余按 hooks-contrib 自动收集
]

a = Analysis(
    [os.path.join(SPECPATH, "run_copilot.py")],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "PySide6",
        "matplotlib",
        "IPython",
        "pytest",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FluentCopilot",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(SPECPATH, "fluent.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="FluentCopilot",
)
