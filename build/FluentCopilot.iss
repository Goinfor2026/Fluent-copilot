; Fluent Copilot Inno Setup 安装器脚本(留档:网络受限时未编译,后续可补)
; 编译:ISCC.exe FluentCopilot.iss(需安装 Inno Setup 6+)
; 产物:build/FluentCopilot-Setup-1.1.exe

#define MyAppName "Fluent Copilot"
#define MyAppVersion "1.1"
#define MyAppExeName "FluentCopilot.exe"

[Setup]
AppId={{8F3B6C2A-1D4E-4F5A-9B7C-FLUENTCOPILOT01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\FluentCopilot
DefaultGroupName=Fluent Copilot
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=.
OutputBaseFilename=FluentCopilot-Setup-{#MyAppVersion}
SetupIconFile=fluent.ico
Compression=lzma2/max
SolidCompression=yes
ArchitecturesInstallIn64bitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Files]
Source: "dist\FluentCopilot\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加任务:"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "立即启动 Fluent Copilot"; Flags: nowait postinstall skipifsilent
