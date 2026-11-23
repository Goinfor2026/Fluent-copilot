---
type: project
created: 2026-10-27
updated: 2026-10-27
tags:
  - Ansys Fluent
  - CFD
  - tutorial
  - frozen-rotor
  - 泵
  - 叶轮机械
sources:
  - "[[Ansys Fluent Tutorial Guide 2026 R1]]"
---

# Fluent 教程12 Frozen Rotor 方法

## 摘要

Tutorial Guide 2026 R1 第 12 章（PDF pp. 517–534）：用 **Frozen Rotor 方法**对带无叶片蜗壳（vaneless volute）的离心泵做稳态流动仿真，评估泵性能并计算扬程（head）。核心演示点：经 turbo 模型建立 **No Pitch-Scale（NPS）界面**、旋转/静止壁面的运动描述、表达式驱动的扬程报告，以及从稳态 frozen rotor 到瞬态 rotor-stator 的转换路径。

## 问题描述（12.3，p. 517）

- 离心泵 + 蜗壳；叶轮 **5 叶片**，转速 **1450 RPM**（绕 z 轴）。
- 蜗壳出口质量流量 **90 kg/s**；入口表压总压 **0 Pa**。
- 目标：确定泵扬程（流体的整体压力增加）。

## 设置要点（12.4，pp. 518–531）

**准备与网格**（12.4.1–12.4.2）：`pump_volute.msh.h5`；Solution 模式、3D、**双精度**、4 进程并行；读网格后在 Domain → Mesh → Units 中把 **angular-velocity 单位改为 rev/min**。

**模型与材料**（12.4.3–12.4.4）：湍流模型保留默认 **k-omega SST**——教程给出的理由：相比其他两方程模型，SST 能有效预测叶轮机械中的流动分离，从而准确评估泵性能；材料从 Fluent 数据库复制 **water-liquid (h2o \<l>)**。

**Cell Zone Conditions**（12.4.5，p. 521–522）：
- `impeller`（fluid, id=36）：材料 water-liquid；**Frame Motion**；Rotation-Axis Direction (0,0,1)；Rotational Velocity **1450 rpm**。叶轮相对绝对参考系旋转，默认绕 z 轴即为正确旋转。
- `volute`（fluid, id=2）：材料 water-liquid；蜗壳在绝对参考系中静止，**无需设置运动**；轴方向同 (0,0,1)。

**边界条件**（12.4.6，pp. 522–523）：
- `impeller-hub`（wall, id=3）：Moving Wall → Rotational；默认即相对 impeller 流体域速度为 0（随叶轮转）。
- `inblock-shroud`（wall, id=14）：Moving Wall → **Absolute** + Rotational——该壁面相对**绝对参考系**静止（速度 0）。与 hub 的差别在于运动参照（Relative 到流体域 vs Absolute 到绝对系）。
- `inlet`（pressure-inlet, id=15）：Supersonic/Initial Gauge Pressure = **-100 Pa**（用作初始压力）。
- `outlet`：网格读入时该出口被 Fluent 自动识别为 mass-flow-inlet（id=11），须先把 Type 改为 **mass-flow-outlet** 再重命名为 outlet，Mass Flow Rate = **90 kg/s**。

**Turbo 界面**（12.4.7，pp. 523–524）：Domain → Turbomachinery 启用 Turbo Models；创建名为 `nps` 的 turbo interface：Zone-1 = interface-impeller-outlet，Zone-2 = interface-volute-inlet，勾选 General Turbo Interface，Pitch-Change Types 选 **No Pitch-Scale**——NPS 用于把 360° 界面连接到另一 360° 界面（单通道对全环时才需要 pitch-scale，本例两侧都是整圈）。
**顺序陷阱**：Perform Mesh Check 必须放在创建 mesh interface **之后**，否则检查失败（Fluent 报 interface 缺失）；检查时确认 minimum volume 为正。

**求解**（12.4.8，pp. 525–531）：
- Methods：Gradient = **Green-Gauss Node Based**；启用 **High Order Term Relaxation**（其余默认）。
- 报告定义三个：`p-out`（Outlet 面质量加权平均**总压**）、`p-in`（Inlet 面同）、`p-blade`（blade 面**静压**积分）。
- 扬程表达式（Report Definitions → New → Expression）：

  ```
  ({p-out} - {p-in}) / (998.2[kg/m^3] * 9.81[m/s^2])
  ```

  命名 `head`，勾选 Report Plot 与 Print to Console；表达式里可直接用 Report Definitions 下拉插入已建报告定义。
- 初始化：**Hybrid Initialization** → More Settings：Reference Frame = **Absolute**；勾选 **Use Specified Initial Pressure on Inlets**。
- 运算：Time Scale Factor = **10**，200 次迭代；运行中同时监控残差与 head 收敛历史（Figure 12.2）。

## 结果与后处理（12.4.9，pp. 531–534）

- Report Definitions 中选 `head` 与 `p-blade` 点 Compute：**扬程 ≈ 20.7 m**，叶片静压积分 **≈ 5650 Pa·m²**。
- 三组云图：出口速度幅值（Filled、关 Global Range，看出口流动均匀性）；壁面静压（Banded 着色，看全域压力递增）；叶片+轮毂面静压（blade、impeller-hub、inblock-hub，Banded）。

## 稳态 → 瞬态 rotor-stator（12.5 Summary，p. 534）

稳态 frozen rotor 结果可按三步转为瞬态 rotor-stator 仿真：
1. 求解器切换为 **Transient**；
2. impeller cell zone 里点 **Copy to Mesh Motion**，把运动从 Frame Motion 改为 Mesh Motion；
3. Run Calculation 中输入 Time Step。

Further Improvements：可变化叶轮转速、出口流量等参数研究泵性能。教程另提供配套设置/求解/后处理视频，但提取文本中视频 URL 为空（PDF 内为链接图形），URL 缺失已记录。

## 证据与适用条件

- 依据：[[Ansys Fluent Tutorial Guide 2026 R1]] Ch.12 全章（PDF pp. 517–534，2026 R1 Downloads 副本，SHA-256 `8347db…`）。
- 版本敏感：GUI 路径、界面名与默认值均按 2026 R1；id 号（impeller id=36 等）是本例网格特有的。
- 扬程公式为教程给的工程式（压差除以 ρg），密度 998.2 kg/m³、g=9.81 m/s² 为硬编码常数，非 Fluent 自动单位换算。
- 理论背景见 [[Fluent 运动参考系]]（Frozen Rotor/MRF）、[[Fluent 叶轮机械流动]]（turbo 界面与 pitch-change）；表达式语法见 [[Fluent 表达式语言]]；报告定义见 [[Fluent 数据报告]]；瞬态转换对应 [[Fluent 滑移与动网格]] 的滑移网格方法。

## 关联页面

- [[Ansys Fluent Tutorial Guide 2026 R1]]（来源记录）
- [[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]]、[[Fluent 教程14 叶排交互稳态与瞬态仿真]]、[[Fluent 教程15 滑移网格]]（同系列叶轮机械教程）
- [[Fluent 运动参考系]]、[[Fluent 叶轮机械流动]]、[[Fluent 表达式语言]]、[[Fluent 数据报告]]、[[Fluent 滑移与动网格]]
