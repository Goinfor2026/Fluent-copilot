@echo off
rem Fluent Copilot 桌面版入口：pywebview 侧边栏窗口 + 托盘（并自动拉起 Fluent Launcher）。
rem 窗口用 pythonw（无控制台）；调试想看报错改用 python.exe，或加 --browser 用系统浏览器。
cd /d "%~dp0"
start "" "%~dp0.venv\Scripts\pythonw.exe" -m fluent_copilot.server
