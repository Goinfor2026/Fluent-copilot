---
type: source
created: 2026-10-15
updated: 2026-10-27
source_kind: manual
status: in-progress
author:
  - H. Ito
  - T. Maeda
  - A. Nakano
  - A. Kato
  - T. Yoshida
version: "2026 R1"
source_path: "../../../Ansys_Fluent_Tutorial_Guide_2026_R1.pdf"
ingest_object: "C:\\Users\\Goinfor\\Downloads\\Ansys_Fluent_Tutorial_Guide_2026_R1.pdf"
sha256: "8347db738ddd8d1e60ea63567d9887ee0f1461f122f8fd5b87eff99edc288d4d"
url: ""
tags:
  - Ansys Fluent
  - CFD
  - tutorial
---

# Ansys Fluent Tutorial Guide 2026 R1

## 内容与范围

PDF 元数据标题为 *Fluent Tutorials*，作者列为 H. Ito、T. Maeda、A. Nakano、A. Kato 和 T. Yoshida，版本标记为 2026 R1。共 1454 页，书签 655 条，目录包含 36 个教程章节，覆盖：

- 流动、后处理、网格、可压缩流、传热和参数分析；
- 涡轮机械、滑移网格、重叠网格与动态网格；
- 组分输运、燃烧、辐射、喷雾和多相流；
- 固化、烧蚀、流固耦合、电池、电解和 GPU 外流场。

## 摄取身份与副本警告

- **摄取对象（2026-10-27 起）**：用户指定的下载副本 `C:\Users\Goinfor\Downloads\Ansys_Fluent_Tutorial_Guide_2026_R1.pdf`，SHA-256 `8347db738ddd8d1e60ea63567d9887ee0f1461f122f8fd5b87eff99edc288d4d`。本页与各教程知识页引用的 PDF 页码均指该副本。
- vault 上一级目录另有一份同名 PDF（约 70 MB，SHA-256 `d889ce44e2e459cdc87a95a6efcd4bfcb9d6a4f2e6f39e0ef2d5d46eabb35f79`）。两副本页数（1454）与章标题一致，但书签定位自 Ch.14 后段起错位约 2 页，抽样比对 p.616 起正文内容不同（如 p.621、p.1001），属**不同文件版本**。按仓库规则两副本不合并进度、不混用页码；此前只做过元数据/目录登记，未基于旧副本摄取正文，故无结论作废。

## 已检查章节

| 章 | PDF 页码（Downloads 副本） | 状态 | 知识页 |
|---|---:|---|---|
| Ch.12 Using the Frozen Rotor Method | 517–534 | 完成（批次 TG-1，2026-10-27） | [[Fluent 教程12 Frozen Rotor 方法]] |
| Ch.13 Turbomachinery Setup and Analysis Using the Turbo Setup Workflow | 535–572 | 完成（批次 TG-2，2026-10-27） | [[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]] |
| Ch.14 Modeling Blade Row Interaction using Steady-State and Transient Simulations | 573–618 | 完成（批次 TG-3，2026-10-27） | [[Fluent 教程14 叶排交互稳态与瞬态仿真]] |
| Ch.15 Using Sliding Meshes | 619–664 | 完成（批次 TG-4，2026-10-27） | [[Fluent 教程15 滑移网格]] |

Ch.1–11（pp. 33–516）与 Ch.16–36（pp. 665–1454）尚未摄取。全章起止页按书签确定（本章起始页至下一章起始页前一页）。用户指定的四批任务（Ch.12–15，批次 TG-1–TG-4）已于 2026-10-27 全部完成；无活动批次。

## 关键结论

教程为版本相关的端到端操作示例；各章的具体设置、参数与结果见上表所列知识页。此处只记录覆盖范围。综合性的模型机理（如 frozen rotor/MRF、turbo 界面、滑移网格）以 User's Guide 各知识页为准，教程页负责提供可复现的案例参数。

## 来源与限制

- 摄取对象：下载副本（见上），此处 vault 不保存该文件本体。
- 教程指南是版本相关的操作示例；用于实际项目时需确认安装版本、许可、模型假设及边界条件。
- 教程正文大量使用截图（对话框/云图），文本提取只覆盖文字；涉及图内数值的结论一律以文字陈述为准，未从图中读数。

## 关联页面

- [[index]]
- [[Fluent Copilot 知识仓库]]
- [[Fluent 教程12 Frozen Rotor 方法]]、[[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]]、[[Fluent 教程14 叶排交互稳态与瞬态仿真]]、[[Fluent 教程15 滑移网格]]

## 尚未处理

- Ch.1–11、Ch.16–36 正文逐章摄取；选定章节后按目录顺序推进，续接依据见 `ingest-state.md` 的"来源二"区块。

