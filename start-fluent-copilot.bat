@echo off
rem Fluent Copilot 启动器：弹出官方 Fluent Launcher 对话框，正常配置点 Start 即可。
rem 唯一区别：会话启动时开启 gRPC server 并把连接信息写入 %TEMP%\fluent-copilot\，
rem 供 Copilot 随时附着（connect_to_fluent）。关闭 Fluent 时连接文件会被自动清理。
setlocal
if not exist "%TEMP%\fluent-copilot" mkdir "%TEMP%\fluent-copilot"
start "" "C:\ANSYS2026\ANSYS Inc\v261\fluent\ntbin\win64\fluent.exe" -sifile="%TEMP%\fluent-copilot\serverinfo.txt"
endlocal
