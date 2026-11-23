---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags:
  - Ansys Fluent
  - engine-ignition
  - spark-model
  - knock
  - ignition-delay
  - crevice-model
  - in-cylinder
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 发动机点火模型

## 摘要

User's Guide 2026 R1 Part III / Chapter 22 "Modeling Engine Ignition"（PDF pp. 2671–2684，共 3 节）讲内燃机点火三模型。**本页全章完成（批次 73，pp. 2671–2684）**：22.1 火花模型（多火花、kernel 半径/起始时刻/能量、R14.5 兼容）、22.2 自燃模型（SI 爆震 Knock 与柴油机滞燃期 Ignition Delay，Hardenburg/Douaud/Generalized 三关联式）、22.3 缝隙模型（纯 TUI 的 ring pack 设置、crev.out 输出与绘图）。

## 22.1 火花模型（Spark Model，pp. 2671–2674）

- 适用语境：预混与部分预混燃烧模型（含 Species Transport）；可模拟**单个或多个火花**。
- **使用步骤**：①General 页 Time 选 **Transient**；②Species Model 选反应模型——**Species Transport + Reactions 勾 Volumetric**，或 **Premixed Model（C Equation 或 G Equation）**；此后 Models 任务页与 Models 树出现 **Spark Ignition**。**Important：读入 R14.5 case 文件时默认回退到 R14.5 火花模型——打开 Spark Ignition 对话框或用 TUI `define/models/species/spark-model` 切换到当前模型；同一 TUI 命令也可退回 R14.5 模型**。
- ③Setup → Models → Species → Spark Ignition → Edit 打开对话框定义火花；④**Number of Sparks 最多 16 个**；⑤用 **On** 选项选择启用哪些火花；⑥火花 Name（可保留默认）；⑦**Define...** 打开 Set Spark Ignition 对话框设参数。
- **火花参数**（Set Spark Ignition 对话框）：**Spark Location**——火花中心 X/Y/Z 坐标 + 火花核（kernel）**Initial Radius**；**Spark Parameters**——**Start Time 与 Duration**；**Important：开启 In-Cylinder 模型时 Start Time 按曲轴角度输入（Duration 仍为秒）**；Start Time 对一个完整发动机循环有效，**后续循环按 Eq 14.30（p. 1961）启用火花**（火花起始曲轴角代入）；**Energy**（可选正值——模拟火花核内更高温升；能量在火花持续期内均匀分布；**点燃燃烧并不需要此能量**——火花模型本身控制 kernel 生长与燃烧推进，故默认 0；额外输入会把 kernel 温度抬到燃烧过程之上）；**Flame Speed Model** 下拉选择（见 Theory Guide Spark Model Theory）。

## 22.2 自燃模型（Autoignition Models，pp. 2674–2677）

- 两类：**SI 发动机爆震（knock）模型**与**柴油机滞燃期（ignition delay）模型**；源于缸内反应流化学动力学。
- **使用步骤**：①Transient；②Species Model 选反应模型——兼容 **Species Transport**（须另勾 Volumetric）、**Premixed Combustion**、**Partially Premixed Combustion**（**后两者仅压力基湍流**）；③Setup → Models → Species → Autoignition → Edit——**Species Transport → 只能选 Ignition Delay Model；Premixed → 只能选 Knock Model；Partially Premixed → 两者皆可选**。
- **Ignition Delay Model 参数**（两种关联式）：**Hardenburg**——典型用于重型柴油机；参数 Pre-Exponential、Pressure Exponent、Activation Energy、**Cetane Number**（十六烷值）；Species Transport 下从下拉选 Fuel Species。**Generalized**（Theory Guide Eq 10.9）——参数 Pre-Exponential、Temperature Exponent、Activation Energy、**RPM Exponent**、Pressure Exponent、**Equivalence Ratio Exponent**、**Octane Number**、**Octane Number Exponent**；Fuel Species 同上。默认值见 Theory Guide "Default Values of the Variables in the Hardenburg Correlation"。
- **Knock Model 参数**（两种关联式）：**Douaud**——SI 发动机爆震；参数 Pre-Exponential、Pressure Exponent、**Activation Temperature**、Octane Number、Octane Exponent（Theory Guide Eq 10.8）。**Generalized**（Eq 10.9）——与滞燃期模型所需参数相同。

## 22.3 缝隙模型（Crevice Model，pp. 2677–2683）

- 模拟活塞环组缝隙中的质量泄漏（实验光机发动机示例 [38]）。**设置纯经 TUI**：
  1. `define/models` → `crevice-model?` → yes 启用。
  2. `crevice-model-controls` 逐项输入（括号内为默认值）：**Cylinder bore (m)** [0.1]；**Piston to bore clearance (m)** [3.0e-5]；**Piston crevice temperature (K)** [400]；**Piston sector angle (deg)** [360]；**Ring discharge coefficient** [0.8]；**Pressure in crankcase (exit pressure) (Pa)** [101325]；**Write out crevice data to a file?** [no]（文件名默认 crev.out）；随后列出可用壁面线程——指定 **Leaking wall**（泄漏壁）与 **Shared boundary**（共享边界）；确认线程；**Solve crevice model?**；**Number of rings**；逐环输入 **Width / Thickness / Spacing / Land Length / Top Gap / Middle Gap / Bottom Gap**（示例默认：宽 0.00375、厚 0.0015、间距 0.008、岸长 0.00391、上/中/下间隙 6e-5/4e-5/6e-5）；最后显示环组内**初始压力**（n+2 个，示例 3 环 5 个压力）。
  3. **多环快捷法**：只设一个环 → 再次调用 `crevice-model-controls` 改环数——**第一环几何自动复制到后续各环**，其余走默认。
  4. `(crevice-summary)` 命令打印缝隙模型摘要（n-rings、各环 width/thickness/mass/spacing/land-length/三间隙、piston-temperature、sector-angle、mid-gap-cd、exit-pressure、线程、unit-roundoff、bore-clearance、write?/output-file/solve?/enabled?、pressures 列表）。
- **22.3.2 求解细节**：缝隙模型源项欠松弛因子在 Solution Controls 任务页——**Crevice Model Sources 默认 0.8**（对倒拖/motored 发动机模拟效果良好）；启用后照常求解（Controls → Initialization → Run Calculation）。
- **22.3.3 后处理**：缸内质量对比图（有/无缝隙模型）——**缝隙质量流失率 ∝ 缸内与曲轴箱压力差**；质量流失的效果 = **峰值压力按缸内总质量损失比例下降**。
- **22.3.3.1 缝隙输出文件**：顶环岸压力定义为缸压（环岸单元压力）；中间压力随时可用 `(crevice-summary)` 查看；勾选数据文件输出后，**每个新时间步开始时把缝隙中间压力打印到 crev.out**。文件格式：`# crank (deg) data-press[0…N] total_mdot`——第一列 = 当前流动时间（或曲轴角）；其后各列 = 各环压力（含缝隙单元面压力与缝隙出口定义压力）；**末列 = 过顶环的质量流量**；格式适配 Gnuplot（www.gnuplot.info）。
  - **读回 Fluent 绘图**：把每列拆成单独文件，文件头三行格式——`"Title"` / `"X-Label" "Y-Label"` / `0 0 0 0`（标题与标签用双引号，第三行四个零），随后为数据行；手册给出 Linux `cat` + `tail +2 crev.out | awk '{print $1, $3} >> …'` 示例生成 crev_col_1_3.dat.h5，经 **Plot Data Sources 对话框**（p. 5514）读入绘制 XY 图；**Windows 用户可直接把 crev.out 导入 Excel 绘图**。
  - 行为：初始瞬态（网络内流动稳定）后，环缝隙压力**跟随缸压形态**，幅值由环组几何控制。

## 证据与适用条件

- 页码：pp. 2671–2683 为正文；**p. 2684 为空白版权页**。目录范围 pp. 2671–2684 全部覆盖，**Ch.22 全章完成**。
- **公式**：本章无编号公式；引用 Theory Guide Eq 10.8/10.9 与 User's Guide Eq 14.30（In-Cylinder 周期执行条件，已在 [[Fluent 滑移与动网格]] 记录）未展开。
- Figures 22.1–22.10（对话框截图与曲线示例）为图形元素未摄取；crevice-model-controls 交互提示与 (crevice-summary) 输出、crev.out 样例行已照录。
- 默认值（16 火花上限、Crevice Model Sources 0.8、ring pack 几何默认值与示例值）为 2026 R1 手册记载，随版本可能变化。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]
- [[Part III - Solution Mode]]
- [[Fluent 缩阶湍流燃烧模型]]（火花/自燃模型的载体——预混与部分预混模型；Ch.21）
- [[Fluent 滑移与动网格]]（In-Cylinder 与 Dynamic Mesh Events、Eq 14.30；Ch.14）
- [[index]]
