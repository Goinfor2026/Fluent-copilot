---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - conventions
  - documentation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 手册排版与数学约定

## 摘要

User's Guide 2026 R1 Part III 开头 "Using This Manual"（PDF pp. 913–916）规定手册的两类约定：排版约定（GUI/文本命令字体、mini flow chart 符号、File 菜单的斜杠写法）与数学约定（向量/张量记号、∇ 算子的用法）。解析手册中的操作路径与公式时以此为准。

## 排版约定（PDF pp. 913–915）

- **字体区分**：GUI 项与文本接口命令用不同字型，如 "Iso-Surface dialog box"（GUI）对 `surface/iso-surface`（文本命令）。
- 文本接口字型也用于展示屏幕实际内容（区别于叙述文本）；此语境下**用户输入通常加粗**。手册示例给出 `solve/initialize/set-fmg-initialization` 的 FMG 初始化交互片段（提示值如层数 [5]、各级残差缩减 [0.001]、循环数 [10]/[50] 等，其中 "100" 为用户输入）。
- **Mini flow chart**（小型流程图）引导经 ribbon 或树到达具体选项/对话框/task page；Table 8 符号含义：看 ribbon、看树、双击打开 task page、从 task page 选择、右键前一项。示例：
  - `Domain → Mesh → Transform → Translate...` = 选 Domain ribbon 页 → Mesh 组内点 Transform → 选 Translate...
  - `Setup → Models → Viscous Model → Realizable k-epsilon` = 展开 Setup 与 Models 分支，右键 Viscous，在子菜单选 Realizable k-epsilon。
  - `Setup → Boundary Conditions → velocity-inlet-5` = 打开对应 task page。
- mini flow chart 通常伴随对话框/命令说明或屏幕插图出现。
- **File ribbon 的行内引用用 "/"**：如 `File/Write/Case...` 表示点 File ribbon 页并在 Write 子菜单选 Case...（打开 Select File 对话框）。

## 数学约定（PDF pp. 915–916）

- 尽可能地：矢量用上箭头（如速度矢量）；**粗体保留给线性代数意义上的向量与矩阵**（如单位矩阵）。
- 算子 ∇（grad/nabla/del）表示量对所选坐标系所有方向的偏导；笛卡尔坐标下定义见手册式 (10)。用法：
  - 标量的梯度是向量（各分量为偏导，式 (11)）；
  - 矢量的梯度是二阶张量（式 (12)），通常写作并矢形式（式 (13)）；
  - 矢量的散度 = ∇ 与矢量的内积（式 (14)）；
  - 算子 ∇·∇ 通常写作 ∇²（Laplacian，式 (15)）；它与 ∇∇ 表达式（式 (16)）不同。
- **例外**：Theory Guide 湍流章的 Reynolds 应力按惯例用笛卡尔张量记号；该章部分速度分量写作 u、v、w 而非带方向下标的形式。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）"Using This Manual"，PDF pp. 913–916；条目 1–2 至此完成。
- **公式 (10)–(16) 为图形/公式元素，文本提取缺失，本页只转述其文字含义，不引用公式本体**；需要公式原式时须视觉核对原页。
- FMG 交互示例中的默认值（层数 5、残差缩减 0.001、循环数 10/50）照录手册示例文本；它们是示例中的提示值，不应视为全局默认设置说明。
- mini flow chart 符号表（Table 8）的图形符号未摄取，仅记录其文字含义。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 启动与批处理自动化]]（TUI/journal 交互与本文的屏幕输入约定相关）
- [[index]]
