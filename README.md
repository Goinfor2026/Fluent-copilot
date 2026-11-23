# Fluent Copilot

帮工程师使用 ANSYS Fluent 的本地 AI 副驾驶:聊天式操控 Fluent 会话、检索本地知识库(摄取自官方 User's Guide / Tutorial Guide 2026 R1)、解读转录与报错,支持拖入 PDF/Word/Excel/日志提问。

![tech](https://img.shields.io/badge/UI-assistant--ui-blue) ![tech](https://img.shields.io/badge/backend-FastAPI-green) ![platform](https://img.shields.io/badge/platform-Windows10%2F11-lightgrey)

## 安装(普通用户)

1. 到 [Releases](../../releases) 下载最新的 `FluentCopilot-x.x-win64.zip`
2. 解压到任意**可写**目录(如 `D:\FluentCopilot`;装 C 盘任意位置也行,用户数据会自动落到 `%APPDATA%\FluentCopilot`)
3. 双击 `FluentCopilot.exe`——右侧弹出聊天面板,系统托盘出现蓝色 F 图标

**首次使用**:窗口里点橙色引导条(或输入框底部 `⚙ 模型菜单 → API 设置…`),选择供应商(智谱/DeepSeek/Kimi/阿里通义等 8 家预设),粘贴你的 API Key,保存即可开始对话。

使用要点:

| 操作 | 方式 |
|---|---|
| 收起/唤回面板 | `Esc` 收起;托盘 F 图标左键唤回;右键有退出/启动 Fluent |
| 切换模型 | 输入框底部 `⚙ 模型 ▾` |
| 对话历史 | 顶栏 `记录`,支持搜索/恢复/删除 |
| 拖文件提问 | 支持 `.trn/.jou/.py/.log/.csv/.md/.json` 文本类与 `.pdf/.docx/.xlsx`(提取文字,扫描版 PDF 除外) |

**连接 Fluent**:本机装有 ANSYS Fluent 时,Copilot 启动会自动拉起官方 Launcher(需 `-sifile` 支持);或先用 `fluent.exe -sifile=%TEMP%\fluent-copilot\serverinfo.txt` 启动 Fluent,Copilot 会自动附着。未装 Fluent 时知识库/文档问答功能不受影响。

## 系统要求

- Windows 10/11 x64(需 WebView2 运行时,系统一般自带)
- 可选:ANSYS Fluent 2024+(`C:\Program Files\ANSYS Inc` 等常见路径自动发现,也可在 config.toml `[fluent] fluent_exe` 指定)
- 任一 OpenAI 兼容 LLM 服务的 API Key

## 从源码构建

```bash
# 后端
python -m venv .venv && .venv\Scripts\pip install -r requirements.txt
# 前端(仅开发改 UI 时需要;打包用已构建产物)
cd frontend && npm install && npm run build && cd ..
# 打包便携版(产物 build/FluentCopilot-1.1-win64.zip)
.venv\Scripts\pip install pyinstaller
.venv\Scripts\pyinstaller build/FluentCopilot.spec --noconfirm --distpath build/dist --workpath build/work
```

日常开发:改后端跑 `smoke_test.py` / `server_smoke.py`;改前端 `npm run dev` + `python -m fluent_copilot.server --dev`。

## 架构速览

- **单进程**:FastAPI(uvicorn,127.0.0.1:8765)+ pywebview 侧边栏窗口(WebView2)+ 托盘
- **前端**:React + [assistant-ui](https://www.assistant-ui.com) 官方组件,ZCode 风格暗色主题
- **后端**:手写 agent 循环(流式 SSE),Fluent 经 [ansys-fluent-mcp](https://github.com/ansys/pyfluent-mcp) 附着,知识库直读 Obsidian vault(`copilot_lib/`,66 页)
- **隐私**:所有数据(配置/对话历史/日志)留在本机;LLM 仅在你提问时调用你所配置的服务

## License

MIT
