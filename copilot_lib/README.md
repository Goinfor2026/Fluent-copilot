# Fluent Copilot 知识仓库

这个仓库按“原始资料 → 持续维护的 Wiki → 维护规则”三层组织，供 Fluent Copilot 项目积累 Ansys Fluent、CFD 工作流和产品实现相关知识。

## 开始使用

1. 将资料放入 `raw/inbox/`，或把仓库内已有文件登记到 `wiki/sources/`。原始资料始终保留原样。
2. 告诉 Codex：**请摄取 `raw/inbox/文件名`**。它会先读取 [[ingest-state]] 和来源记录，核对上次进度后再继续，把可核验结论整合进 Wiki。
3. 从 [[index]] 浏览主题、项目与来源；`log.md` 记录每次摄取、问答归档和巡检。
4. 所有后续维护遵循本目录的 [[AGENTS]]。

## 目录

- `raw/`：只读的原始资料和附件。
- `wiki/`：经过整理、互相链接并带来源的知识页面。
- `templates/`：新来源和主题页面模板。
- `index.md`：内容目录。
- `log.md`：按日期追加的维护日志。
- `ingest-state.md`：跨会话/跨智能体检查点，记录来源身份、逐章完成页段与下一续接位置。
- `INGEST_PROMPT.md`：每次只摄取一章的可复制提示词。
- `AGENTS.md`：知识库结构和工作流程规则。

## 当前起点

已登记一份 Ansys Fluent Tutorial Guide 2026 R1（1454 页）。目前只读取其 PDF 元数据和目录，尚未逐章摄取或验证技术结论；详见 [[Ansys Fluent Tutorial Guide 2026 R1]]。原 PDF 保存在仓库上一级目录，因此没有复制或改动它。
