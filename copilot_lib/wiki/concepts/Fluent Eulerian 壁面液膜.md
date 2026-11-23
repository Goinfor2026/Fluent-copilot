---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - eulerian-wall-film
  - ewf
  - dpm-coupling
  - vof-coupling
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent Eulerian 壁面液膜（EWF）

## 摘要

User's Guide 2026 R1 Part III / Chapter 30 "Modeling Eulerian Wall Films"（PDF pp. 3355–3380，共 7 节）。**本页全章完成（批次 91，pp. 3355–3380）**：Eulerian Wall Film（EWF）模型预测壁面薄液膜的生成与流动——限制清单、工作流、模型选项（动量/能量/标量/DPM 耦合/相耦合/尖角处理）、求解控制（时间/空间离散、膜时间步）、壁面 Wall Film 选项卡六组边界/初始/源项/相变/接触角/DPM/VOF 交互设置、EWF-VOF 耦合流程与后处理变量全集。理论见 Theory Guide "Eulerian Wall Films"（Chapter 17，式号 17.x 由本章引用）；壁面液膜边界条件另见 Wall Film Conditions for Walls（p. 1532）。

## 30.1 限制（pp. 3355–3356）

- **仅 3D**。许多模型（如 VOF 多相流、辐射）**未经 UDF 修改边界条件前无法与液膜模型正确交互**。
- **隔板（零厚度壁）交接处的液膜行为可能非物理**（wall/wall-shadow 局部拓扑）——孤立液膜壁面不得共享公共边，慎用。
- 液膜**只能单组分**，不能多组分。
- **不兼容**：非一致界面、Overset 网格、网格操作（fuse/zone extrusion/zone type change/zone activation 等；**cell/face separation 与 cell/face merge 兼容**）、**运动/变形网格与旋转/平移参考系**（但**运动或旋转的边界**兼容）、Lagrangian Wall Film（LWF）模型——EWF 启用后 Wall 对话框 DPM 选项卡的 wall-film 选项不再出现在 Discrete Phase BC Type 下拉中。

## 30.2 使用工作流（pp. 3356–3357）

1. 先启用并设置与 EWF 兼容的其他模型 → 2. 启用 EWF 并设模型选项（部分选项需相应模型先启用）→ 3. 设求解控制 → 4. 逐壁面设 Wall Film 边界条件 → 5. 必要时**先解流场**再开液膜 → 6. 初始化并求解（液膜可随流场一起初始化，或在已有流场上从 Eulerian Wall Film 对话框 Model Options and Setup 选项卡初始化）→ 7. 检查结果。
- 求解过程中的网格/区域操作：**Make Polyhedra**——模型与条件先禁用、转换后自动启用，液膜数据全部丢弃；**cell zone Merge/Separate**——禁用后需手动重新启用，数据丢弃；**face zone Merge/Separate**——模型保持启用，但涉壁面的液膜条件禁用需手动启用、操作后须重新初始化，数据丢弃。
- **网格自适应兼容**：自适应过程中液膜数据保留；但 VOF 耦合转变判据等设置可能需随网格分辨率调整。
- **重要**：在 Fluent 中修改网格前必须先禁用 EWF；保存修改后的网格后重新启用并重新初始化。

## 30.3 模型选项（pp. 3357–3364）

启用：Setup → Models → Eulerian Wall Film → Edit（Figure 30.1/30.2）。Model Options and Setup 选项卡：

- **Solution Options**：
  - **Solve Momentum**：关时膜速度固定为现值；开时在 Momentum Options 组选解法。**Solve Energy**（Eq 17.3）；**Solve Scalar**（被动标量 Eq 17.38，配合 Scalar Diffusivity）。
  - **DPM Coupling**（需 DPM 模型启用）：颗粒-液膜交互，设置在 DPM Interaction 选项卡。
  - **Phase Coupling**（需 VOF/Eulerian/Mixture（含滑移速度）多相模型或组分模型启用）：液膜-气相组分相变、二次相收集效率、EWF-VOF 交互，设置在 Phase Interaction 选项卡。
  - **Treat Sharp Edge**：设 **Sharp Edge Angle**——边角小于该角度时膜边按边界边处理（**液膜脱离**而非绕过）；与 DPM 同用时按分离边处理。
- **Momentum Options**（Solve Momentum 启用时）：
  - **Analytical Solution**：由外流剪切与重力解析求膜速度（Theory Guide "Obtaining Film Velocity Without Solving the Momentum Equations"）。
  - **Momentum Equation**（Eq 17.2）可选五项：**Gravity Force**（重力沿壁分量加速）、**Surface Shear Force**（外流方向加速）、**Pressure Gradient**（逆外压梯度，如机翼前缘高压把均一膜推向翼面低压区）、**Spreading Term**（向薄处铺展；**需同时选 Pressure Gradient 与 Gravity**）、**Surface Tension**（**需选 Pressure Gradient**）。
- **Material Options**：Film Material 选择；Solve Momentum 启用时可设液膜 **Surface Tension**；Solve Scalar 时设 Scalar Diffusivity。液膜材料类型必须为 **Fluid、Droplet Particle 或 Inert Particle (fluid)**；密度/粘度/比热/导热/蒸发温度/蒸气饱和压力可用 constant、polynomial（含 piecewise linear/piecewise polynomial）、compressible liquid（仅流体密度）、user-defined（**流体比热不可 UDF**）、default-method（蒸气饱和压力）。
- **DPM Interaction 选项卡**（DPM Coupling 启用时）：
  - **Particle Splashing**（飞溅选项在 Wall 对话框 Wall Film 选项卡设）；
  - **Source Smoothing**：对 DPM 撞击源项光顺以抑制点状源分布；**默认 smoothing level 2、smoothing factor 0.5**，TUI `define/models/eulerian-wallfilm/model-options` 调整；
  - **Edge Separation** + Separation Parameters：Critical Weber Number、Critical Angle、Separation Model、**Random Separation**（新生成颗粒沿分离边随机取位置）；
  - **Particle Stripping** + Stripping Parameters：Critical Shear Stress、Diameter Coefficient、Mass Coefficient。
  - **与 DPM 联用三要点**：①DPM Coupling 用于成膜时**至少建一个 injection**；②injection 材料**属性必须与膜材料相同**，且名称须含膜材料名加连字符后缀（如膜材料 water-liquid → injection 材料 water-liquid-particle）；③启用 Edge Separation/Particle Stripping 时**自动创建** injection `ewf-strip-sep-injection` 与自动命名材料 `<film_material_name>-pcle` 跟踪分离/剥离颗粒。
- **Phase Interaction 选项卡**（Phase Coupling 启用时；Figure 30.2）：
  - **Phase Change**：选 Film Vapor Material；**用作膜材料的二次相不能是组分混合物**；仅组分模型启用时可用；相变参数在 Wall 对话框 Wall Film 选项卡。
  - **Phase Accretion**：Phase Concentration + Phase Velocity；计算壁面二次相收集效率；仅 Eulerian 或 Mixture（含滑移速度）时可用。
  - **VOF Coupling**：Transition Base 选 **Volume Fraction**（膜液体体积/邻近单元膜壁体积之比）或 **Height Fraction**（膜半厚/邻近单元中心高度之比）。
- **Solve Wall Film** 开关：跳过液膜求解但保留变量与设置。液膜**必须先用 Initialize 按钮初始化**才能求解。TUI：`define/models/eulerian-wallfilm/model-options`。

## 30.4 求解控制（pp. 3364–3367）

Solution Method and Control 选项卡（Figures 30.3/30.4）：

- **Discretization**：时间离散四选项——**First Order Explicit、High Order Explicit（默认阶数 2，可升 3/4：TUI `define/models/eulerian-wallfilm/solution-options` → High Order Explicit [yes] → Explicit Scheme Order (2-4) 输入阶数）、First Order Implicit、Second Order Implicit**；空间离散 Continuity/Momentum/Energy/Scalar 均 **First Order Upwind / Second Order Upwind**。
- **Maximum Thickness**：超限处从液膜移除材料以限制膜厚。
- **Coupled Solution**（Solve Momentum 时）；选 Surface Tension 后可开 **Curvature Smoothing**（Smoothing Level/Factor）。
- **稳态算例**（模型本身永远瞬态）：设膜专属 **Time Step**，或选 **Adaptive Time Stepping**（Max Courant Number、Initial Time Step、时间步 Increase Factor 与 Decrease Factor——**两者都必须大于 1**）。
- **瞬态算例**：**Per Flow Iterations**（每个流动时间步内第一次迭代即调用膜求解，之后按该间隔；输入 0 = 在时间步末调用）；**Sub-Time Steps per main flow time step** 或 Adaptive Time Stepping（同上三参数）；**Reporting Interval**（首尾子步总是报告）。
- **隐式（一/二阶）专属**：**Sub-Iteration Stop** 阈值、**Sub-Iterations** 次数、子迭代 Reporting Interval（首尾总是报告）。
- **DPM Coupling 时**：**Film Steps per DPM Step**（隔多少膜步算一次 DPM）与 **Relaxation Factor**——仅当 DPM 对话框 **Interaction with Continuous Phase 关闭**时可用。

## 30.5 边界/初始/源项条件（pp. 3368–3376）

Wall 对话框 **Wall Film 选项卡**，选 **Eulerian Film Wall** 将壁面指定为膜壁（液膜方程只在膜壁求解）。与对称/周期边界相连的膜边按对称/周期处理；**未与其他膜壁/对称/周期相连的膜边按液膜出口处理**（液体离开膜壁）。六个子选项卡：

- **Boundary Type**（Figure 30.5）：
  - **Boundary Condition**（向液膜域引入质量/动量/能量/标量）：Film Mass Flux、X/Y/Z-Momentum Flux、Incoming Film Temperature、Film Passive Scalar Flux；动壁可选 **Relative Film Momentum Flux**（相对膜壁的动量通量；需 Wall 选 Moving Wall 或 Fluid 选 Frame Motion）。
  - **Initial Condition**：Film Height、X/Y/Z-Velocity、Film Temperature、Film Passive Scalar；动壁可选 **Relative Initial Film Velocity**。
  - 两类通用：**Flow Momentum Coupling** 勾选 = 液膜与气流在界面共享速度（双向耦合）；不勾 = 仅单向（气流影响膜、膜不影响主流）。
- **Source Terms**（仅 Initial Condition 时可用；Figure 30.6）：勾 **User Source Terms** 后可设膜连续性/动量/能量/标量方程附加源——Mass Flux、X/Y/Z-Momentum Flux、**Heat Flux**、Scalar Flux。**注意**：膜能量源是与膜质量通量相伴的热流，须与质量源配套使用；纯热流（无质量）应走 Wall 对话框 Thermal 选项卡的流动热边界；两种通量都计入 flux 报告。
- **Phase Change**（Figure 30.7；需 EWF 对话框勾 Phase Change）：启用 **Film Phase Change** 并选模型——**diffusion-balance**（设 Condensation Constant 与 Vaporization Constant）；**wall-boundary-layer**（无需输入）；**user-defined**（Condensation Rate 与 Vaporization Rate，常量/参数/profile UDF；**必须为正值，单位 kg/s**）。
- **Surface Contact**（Figure 30.8；需初始条件 + EWF 对话框选 Surface Tension）：勾 **Film Contact Angle** 启用**部分润湿模型**，参数三件——**Mean Contact Angle**（0–180°；profile UDF 须返回弧度值）、**Relative Standard Deviation**（0–50%）、**Contact Angle Force Beta**（0–10，Eq 17.29）。
- **DPM Interaction**（Figure 30.9；需 DPM Coupling）：颗粒-壁面撞击模型三选——**stanton-rutland**；**kuhnke**（参数 Ra——计算 Eq 12.255 的壁面平均粗糙度；Rz——飞溅颗粒反射角分布 Eq 12.267；Critical Temperature Factor——Eq 12.245 撞击 regime 转变温度）；**stochastic kuhnke**（Rz——插值干燥壁飞溅临界 We 的壁面粗糙度长度；Upper Deposition Limit Offset——Eq 12.270；Deposition Delta T——Eq 12.271；Laplace Number Constant——Eq 12.272；Partial Evaporation Ratio——蒸发飞溅 regime 撞击液滴即时蒸发质量分数）。可用 `DEFINE_IMPINGEMENT`/`DEFINE_FILM_REGIME`/`DEFINE_SPLASHING_DISTRIBUTION` UDF（**UDF 设置覆盖所选撞击模型**）。勾 Particle Splashing 后可选 **DPM Wall Splash** 并设 **Number of Splashed Particles**；勾 Edge Separation 后可选 **Allow Boundary Separation**（允许在不相连的内部膜壁边界分离）。
- **VOF Interaction**（Figure 30.10；需 Phase Interaction 选项卡勾 VOF Coupling）：启用 **Film/VOF Transition & Criteria** 并设 **Relaxation Factor**（0–1，**默认 0.5**）。Film to VOF 与 VOF to Film 判据为 0–1 的分数值（Volume Fraction 或 Height Fraction 基准）；**Film to VOF 判据必须大于 VOF to Film 判据**；由判据算加权膜厚阈值。**膜→VOF**：膜厚超 Film-to-VOF 阈值或超 Maximum Thickness；**VOF→膜**：等效膜厚低于 VOF-to-Film 阈值。阈值在设置生效时与模型初始化时打印到控制台。判据取值越高越易不稳，可能需更小松弛因子。

## 30.6 EWF 与 VOF 多相模型耦合（p. 3377）

流程：①启用并设置 EWF 与 VOF → ②EWF 对话框勾 Phase Coupling → ③Phase Interaction 选项卡勾 VOF Coupling → ④Transition Base 选 Volume Fraction 或 Height Fraction → ⑤Wall 对话框 Wall Film 选项卡 → ⑥在 VOF Interaction 选项卡启用 Film VOF Coupling 并设耦合参数。

## 30.7 后处理（pp. 3377–3379）

- 变量类别（按启用选项条件出现）：**Film Thickness、Film Mass**；Film Temperature/Film Surface Temperature（Solve Energy）；Film X/Y/Z-Velocity、Velocity Magnitude、Film Surface X/Y/Z-Velocity、Surface Velocity Magnitude；Film Passive Scalar（Solve Scalar）；Film Density（非恒密度）；**Film Effective Pressure**；Film Coverage（Solve Momentum）；**Film Courant Number、Film Weber Number**；Film Stripped Mass/Diam（Particle Stripping）；Film DPM Mass/Energy/X/Y/Z-Momentum Source（DPM Coupling，能量源另需 Solve Energy）；Film Separated Mass/Diam/Separation Rate（Edge Separation）；**Film Phase Change Rate**（Phase Change）；**Film Outflow Mass**；Film Secondary Phase Mass/Collection Coef（Phase Accretion）；Film VOF Equivalent/Total Equivalent Thickness、Volume Fraction/Total Equivalent Volume Fraction、Height Fraction/Total Equivalent Height Fraction、Film VOF Mass Exchange/Exchanged Mass（VOF Coupling）。定义见 Field Function Definitions（p. 4395）。
- **通量报告**：Results → Reports → Fluxes——EWF 启用时多出 **Film Mass Flow Rate** 与 **Film Heat Transfer Rate**（适用于进出口等域边界与壁面）。注意：能量通量报告**只计外部边界换热**，不含气液界面换热、相变换热与膜-DPM 交互换热。TUI：`report/fluxes/film-mass-flow`、`report/fluxes/film-heat-transfer`（提示输入边界面 zone ID 与是否存文件）。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3355–3380（批次 91，2026-10-20，pypdf layout 模式提取；p. 3380 为仅含页脚的空页）。
- Theory Guide Eq 17.2/17.3/17.29/17.38 与 Eq 12.245–12.273（Kuhnke 族）公式体未提取，按引用记录变量与语义；Momentum Options 五项与 Eq 17.2 右端各项的对应关系照录（Spreading/Surface Tension 项的符号位置在文本层缺失，按功能语义记录）。
- Figures 30.1–30.10（对话框截图）为图形元素未摄取；TUI 提示串照录（原文含 "Excplicit" 拼写瑕疵，按原样记录）。
- 版本敏感：默认值（smoothing level 2/factor 0.5、松弛因子 0.5、High Order Explicit 阶数 2）以 2026 R1 为准。
- 相关页面：[[Fluent 离散相模型（DPM）]]（wall-film 撞击边界、LWF 对比）、[[Fluent 多相流模型]]（VOF 耦合背景）。
