---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - rom
  - designxplorer
  - addon-module
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 降阶模型（ROM）

## 摘要

User's Guide 2026 R1 Part III / Chapter 36 "Creating Reduced Order Models (ROMs)"（PDF pp. 3699–3708，四节）。**本页全章完成（批次 101，pp. 3699–3708）**：用独立 Fluent 会话定义降阶模型，供 Ansys Workbench（经 Ansys DesignXplorer）生产使用——ROM 是全模型的数学近似，改输入立即得解；创建流程（add-on 模块 11、输入/输出参数、变量与区选择）、在 Fluent 中求值与后处理、结果导出 Profile、限制清单。更多 ROM 理论见 DesignXplorer User's Guide。

## 36.1 定义 ROM（pp. 3699–3701）

- **ROM Production**：独立 Fluent 设好 ROM case，读入 Workbench 的 Fluent；**ROM Consumption**：导出为 **FMU 2.0 文件或 ROMZ 文件**消费（详见 DesignXplorer User's Guide）。
- **2026 R1 适用范围**：仅**稳态、牛顿流体、无激波（Ma<1）、无辐射**。
- 构建步骤：
  1. 控制台输 `define/models/addon-module/11` 启用 ROM add-on 模块（**模块号 11**）。
  2. 初始化 case 或读入 data 文件。
  3. 为关注量创建**输入参数**（材料属性、入口速度、压力等均可；3D ROM 系统中可再取消不需要的参数；**参数过多需更多快照维持精度**——数量指引：Low 1–2、Medium 3–6、High >7、Very high >15）。
  4. 创建**至少一个输出参数**（对 ROM 无影响，用于 DesignXplorer 更新设计点时监控；理想上含 ROM 选中的变量；派生量做法：custom field function → 报告定义（Surface/Volume Report）→ 勾 **Create Output Parameter**）。
  5. 启用 **Reduced Order Model**（Setup → Models → Reduced Order Model → Edit）。
  6. 选 **Variables 与 Zones** 点 Add>>（自定义场函数也可选；Selected for ROM 列表可 Delete 移除）。**告诫**：选太多变量/区会得到更大的文件（大模型尤甚——可只选能充分捕捉物理的小区）；**必须选中与输入/输出参数对应的变量**（如输出参数为 Mass Flow Rate 则必须选 Velocity）。
  7. 核对 Selected for ROM 列表 → OK。

## 36.2 在 Fluent 中求值 ROM（pp. 3701–3705）

可查看：Contours、Vectors、Pathlines、XY Plots、面/体积分报告。流程（Workbench 环境）：
1. Workbench 中右键 **ROM Builder cell → Export ROM** 生成 **romz** 文件（**不能导入同一 Workbench 实例中生产该 3D ROM 的 Fluent 系统**）。
2. 右键 **Fluent Setup cell → Import ROM → Browse** 导入 romz。
3. 工具栏 **Update Project** 求解 → 双击 Solution cell 启动 Fluent。
4. 打开 Reduced Order Model 对话框（Setup → Models → ROM → Edit）→ **Evaluate 选项卡**：列出 ROM 全部参数与各变量允许的取值范围 → 输入值（范围内）→ **Evaluate**。
- 后处理：Contours 对话框——**关闭 Node Values**（ROM 在单元中心求值）；Contours of 选 **ROM Cell Functions...**（**仅在 Evaluate 选项卡点过 Evaluate 后出现**）→ 第二下拉选 ROM 变量 → 面列表已过滤为 ROM 求值面 → Save/Display。
- **Fluent 内 ROM 后处理限制**：求值后不能继续 ROM 解；导出解数据不含 ROM 快照数据；Flux/Force Reports 与报告定义对 ROM 求值变量不可用；在 Fluent 内求值 ROM 时 Design of Experiments 的输出参数不更新。

## 36.3 导出 ROM 结果（p. 3706）

ROM 标量输出可经 **Write Profile** 对话框导出为 Profiles：Workbench 的 Fluent 走 File → Export → Profile...；独立 Fluent 走 File → Write → Profile...——在 Values 与 Surfaces 列表选 ROM cell functions 与应用面。

## 36.4 ROM 限制（pp. 3707–3708）

与 DesignXplorer 文档的 ROM Limitations and Known Issues 一并看待：
- 启用 ROM 前**至少一个输入参数 + 一个输出参数**；**界面（interface）区不可用于 ROM**；3D ROM **不支持几何参数更新**；**只能为稳态算例创建**；**燃烧与辐射模型不支持**；**经 Fluent 的参数化优化不支持**；**动/变形网格不支持**；必须选中与输入/输出参数对应的变量。
- 报告定义：**Expression 与 User-Defined 报告定义对 ROM 变量不可用**（但可创建包含 ROM 变量报告定义的命名表达式）；**不建议用 Mass-Weighted Average、Vertex Average、Vertex Minimum/Maximum**（ROM 数据只在单元面中心与单元中心）——改用 **Area-Weighted Average、Facet Average、Facet Minimum/Maximum**。
- 以下报告定义类型**不支持输出参数**：User Defined、Expression、Flux Report、Surface Report—Flow Rate。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3699–3708（批次 101，2026-10-20，pypdf layout 模式提取）。
- 输入参数数量指引、模块号 11、Evaluate 交互流程以 2026 R1 为准；DesignXplorer 侧行为未摄取（指向其 User's Guide）。
- Figures 36.1–36.2（对话框截图）为图形元素未摄取。
- 相关页面：[[Fluent 电池模型]]（Ch.32 的 Battery ROM Tool Kit——LTI/SVD 电池热 ROM，与本章 DesignXplorer ROM 是两套体系）、[[Fluent 表达式语言]]（命名表达式）。
