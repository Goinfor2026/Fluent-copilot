---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - electric-potential
  - lithium-ion-battery
  - electrolysis
  - fuel-cell
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 电势场与电化学

## 摘要

User's Guide 2026 R1 Part III / Chapter 31 "Modeling Electric Potential Field and Electrochemistry Models"（PDF pp. 3381–3426，共 4 节）。**本页全章完成（批次 92，pp. 3381–3426）**：三大块——①电势场模型（电势方程、Joule 热、边界条件）；②精细锂离子电池模型（Butler-Volmer 动率、材料/浓度参数、老化模型 SEI 生长/析锂/正极膜生长、肿胀-FSI、专家收敛控制、报告定义）；③电化学器件（PEM/碱性电解、H2 Pump、PEM 燃料电池、SOFC/SOEC、Customized——器件类型、MEA 三种建模法、八选项卡参数、求解策略）；外加电势场/电池/电解后处理变量。理论见 Theory Guide "Electric Potential and Electrochemistry Models"（Chapter 18/20，式号 18.x/20.x 与少量 7.x 由本章引用）。电池相关的整体电池/电池包热模型（MSMD）见 [[Fluent 电池模型]]（Ch.32）。

## 31.1 电势场模型（pp. 3381–3383）

- 用途：预测电势场及其效应；可单独使用（如为 DPM 带电颗粒计算电静力）或与其他模型组合。电势求解器已与电化学反应模型集成——**启用电化学时自动启用电势求解器**；仅用电势模型时需手动启用。可在流体与固体区求解电势场。
- **限制**：不能用于带 **shell conduction** 边界条件的壁面。
- 设置：Setup → Models → Potential/Electrochemistry → Edit，勾 **Potential Equation**；启用后 Create/Edit Materials 出现 fluid/solid/mixture 材料的 **Electrical Conductivity** 属性。②需要 Joule 热进能量方程（Eq 5.1）时勾 **Include Joule Heating in Energy Equation**（该选项仅在能量方程开启时出现）。③为导电材料设 Electrical Conductivity（详见 Electrical Conductivity 节 p. 1720；可各向异性/正交各向异性/圆柱正交各向异性）。④导电壁面边界条件——Potential Boundary Condition 下拉三选：**Specified Flux**（指定 Current Density）、**Specified Value**（指定 Potential）、**Coupled**（仅双侧内部壁面；设置自动应用于 wall/wall-shadow 对的两侧；解耦时两侧可各设不同条件）。再设 **Contact Resistance**（Eq 18.3）。⑤其他边界的 Potential 选项卡默认**零电流通量**，多数问题无需改。⑥单元区可设 Fixed Values 或 Source Terms 定电位/电位源。

## 31.2 精细锂离子电池模型（pp. 3383–3396）

- 定位：模拟充放电过程的细观物理，**面向极小电极尺度**；关注整电池/电池包热行为应改用 dual potential MSMD 电池模型（p. 3428，见 [[Fluent 电池模型]]）。
- **限制**：电极区必须是固体、电解液区必须是流体；**只能全电池模拟**（正极+电解液+负极三区俱在），不支持半电池。
- 设置（Potential/Electrochemistry 对话框五选项卡；Figure 31.1–31.5）：
  1. 勾 Potential Equation（Potential 组）+ **Lithium-ion Battery Model**（Electrochemistry 组）——**启用后自动切换为瞬态求解器**。需电化学反应热时勾 Include Echem Heating in Energy Equation。
  2. **Zone Selection**：正极/电解液/负极区选择列表。
  3. **Echem Rate**：阴极与阳极的 Butler-Volmer 速率参数（Eq 18.13 各符号位）——Exchange Current Density、ce Rate Exponent、(csmax−cs) Rate Exponent、cs Rate Exponent、Anodic/Cathodic Transfer Coefficient、Equilibrium Potential（可用 `DEFINE_EC_KINETICS_PARAMETER` UDF 自定义）；可选 **Use Linearized Butler-Volmer Equation**（Eq 18.14 线性化形式）。
  4. **Material Properties**：浓度信息——Cathode cmax、Anode cmax（最大锂浓度）、Cathode/Anode Initial c（放电起始锂浓度，Eq 18.8）、Electrolyte Initial c（电解液锂离子浓度）；材料属性——**Transient Number**（锂离子迁移数，Eq 18.12）、**Activity Term**（Eq 18.12）。
  5. **Advanced**（少用模型选项与求解控制；Figure 31.4）：
     - **Physics-Based Aging Model**（老化；Figure 对话框展开 Aging Model Parameters）：**SEI Growth Parameters**——EC Conc.（电解液主体 EC 浓度，Eq 18.31）、EC Diff.、SEI Dens./SEI MW（Eq 18.34–18.37）、SEI Cond.（Eq 18.36–18.37）、Ref. Rate Const.（SEI 生成反应速率常数，Eq 18.28）、Trans. Coef. c、Eq. Potential（Eq 18.33）。**Lithium Plating**——Li Dens./Li MW（Eq 18.34–18.35）、Ref. Curr. Dens.（Eq 18.29）、Trans. Coef. c、Eq. Potential、**Frac. of Li+ Forming SEI**（沉积锂离子转化为 SEI 的份额，Eq 18.25–18.26）。**Cathode Film Growth Model**——Film Dens./Film MW/Film Cond.（Eq 18.34–18.37）、Rate Constant（Eq 18.30）。**告诫**：老化效应数百上千循环才显著，瞬态算这么多循环不现实——模型只适合**少循环看趋势**。
     - **Include Swelling Effect**（肿胀+FSI）：阳极/阴极区设 **Swell Coefficient** 与 **Reference Concentration**（肿胀中性态参考锂浓度，Eq 18.38）；自定义肿胀应变公式用 **Customize Swelling Strain** + `DEFINE_LITHIUM_SWELL_STRAIN` UDF；随后按 intrinsic FSI 流程（Ch.29，p. 3345）设置，双向 FSI 另见动网格。**注意**：此结构模型固体区仅支持 hexahedral/wedge/pyramid，**不支持多面体**（比 Ch.29 通用结构模型的单元清单更严——无四面体）。启用肿胀后 Structural Model 对话框 Li-ion Battery Effects 自动启用不可关。
     - **Expert Control Options**（低质量网格收敛困难时）：**Include Li-Migration**（默认开；关闭可改善收敛但牺牲电解液电位场精度，**最后一招**）；**Include Secondary Gradient Correction in Li-Equation** 与 **in Potential-Equation**（收敛困难时可关）。
  6. 材料：为负极/正极/电解液建材料，正确设 **Electrical Conductivity 与 Lithium Diffusivity**。
  7. 单元区条件分配材料（电极区固体、电解液区流体）。
  8. 壁面 Potential 选项卡电位边界：阳极选 **Specified Value**（默认 Potential 0 即可）；阴极用 Specified Flux 时**电流密度负值=电流流出域、正值=流入域**。**锂方程无需定义边界条件**。
  9. **收敛准则要收紧**：示例电位场 1.0e-10、锂浓度场 1e-12（Residual Monitors）。
  10. 无流动算例在 Equations 对话框禁用 Flow 与 Energy 方程。
  11. 初始化：锂与电位场按对话框输入**自动初始化**，无需额外输入。
  12. **Faradaic Interface Current 欠松弛因子**（Solution Controls）：平衡电位用常量时默认 **0.01 或更大**可用；平衡电位用 UDF 随锂浓度变化时电位-锂耦合强，可能需要小至 **0.001** 求稳定。
  13. 启用模型后**自动生成两个报告定义**：`li-ion-battery-soc`、`li-ion-battery-capacity`（可加入报告文件/图；需在 Report 选项卡正确设 0%/100% SOC 锂浓度）。
  14. 运行：Faradaic URF 低时需调大 Max Iterations/Time Step；检查阳/阴极总电流**每步充分平衡**。
  15. **Report 选项卡**：设 Anode/Cathode 的 CLI at 0% SOC 与 CLI at 100% SOC → 点 Compute——Current Report 组给出当前容量、SOC 与阳/阴极 SEI 总电流；两电流应足够接近（不匹配=未收敛，调大迭代数重跑）。用老化模型时另报**总损失锂质量与容量损失因子**。

## 31.3 电化学器件（pp. 3396–3423）

- 用途：PEM 电解、碱性电解等电解装置（Device Type 清单另含 H2 Pump、PEM Fuel Cell、SOFC、SOEC、Customized；差异在计算所用电化学）。理论见 Theory Guide "Electrochemical Devices"（Chapter 20）。
- **几何要求**：网格须含——阳极流道、阳极气体扩散层（多孔层）、阳极催化层、膜层、阴极催化层、阴极气体扩散层、阴极流道；如有则标认阳/阴极集流体（固体）。
- **工作流**：读 case/网格 → 缩放 → 启用模型 → 材料属性（collector/porous/catalyst/electrolyte 材料必须设 **Electrical Conductivity 与 Electrolyte Conductivity**——常量/分段线性/分段多项式/多项式/`DEFINE_PROPERTY` UDF；固体材料电导还可各向异性/正交各向异性/圆柱正交）→ 操作条件 → 流动边界条件（**电势边界自动设置，适合多数情况不应修改**）→ 计算 → 存盘 → 后处理。建议先在 Potential/Electrochemistry 对话框完成主体设置，再做边界条件收尾。
- **模型启用**：勾 Potential Equation + **Electrochemical Devices**——**自动启用 Mixture 多相模型（如需）与组分输运**。**多相效应只能用 Mixture 模型，VOF/Eulerian 不可用**；Customized 器件类型单相多相均可。对话框八选项卡：Model / Parameters / Anode / Electrolyte / Cathode / Electrical Tabs / Customization / Advanced。需反应热时勾 Include Echem Heating in Energy Equation。
- **Model 选项卡**（Figure 31.6）：
  - **Device Type** 七选：PEM Electrolysis、Alkaline Electrolysis、H2 Pump、PEM Fuel Cell、SOFC、SOEC、Customized。Phases 组只读显示单相/多相。
  - **MEA Layer and H2 Pump Method**：催化层+膜的建模法三选——**Resolved**（网格解析）、**Unresolved 0D**、**Unresolved 1D**。
  - **Options**：**Electrochemistry Sources**（只关心基本电位场时可关；也可先关它获得初始流场再开）；**Butler-Volmer Rate**（默认；关则用 **Tafel 近似** Eq 20.7/20.8）；**Multicomponent Diffusion**（全多组分扩散法算气体扩散系数）；**Half Cell Voltage**（Nernst 方程算阴阳极半电池电位 Eq 20.13/20.14；关则常数开路电压）；**Osmotic Drag**；**Capillary Pressure**（促催化层产气经多孔层输入流道；仅多相器件）；**Reaction Heat**；**Phase Change**（液水-水蒸气；仅多相器件）；**Water Content**（水含量输运方程 Eq 18.44/18.45；膜水合水平影响电解液电导需 `DEFINE_PROPERTY`；仅多相+resolved MEA）。
  - **Electrical System Setup** 三法：**Set Up in B.C. Panels**（用边界条件面板里设的电位边界）；**Specify Total Voltage**（指定电池/电堆总电压 V，常量或表达式——自动忽略 BC 面板电位设置，阴极 tab 电位置零、阳极 tab 加固定 Total Voltage）；**Specify Total Current**（指定总电流 A——阴极 tab 置零、阳极 tab 加恒定电流密度通量）。
- **Parameters 选项卡**（Figure 31.7；非 Customized 器件阴阳极侧可留默认）：Electrochemistry 组——**J_ref**（参考交换电流密度，Eq 20.9/20.10）、**Ea**（渗透活化能）、**T_ref**（参考温度）、**C_ref**（参考浓度，1 kg-mol/m³；PEM Electrolysis 与 H2 Pump 仅阳极、Alkaline 仅阴极可用）、**Con. Exponent**（浓度依赖指数；可用性同 C_ref）、**Exch. Coeff. a/c**（传递系数，Eq 20.5/20.6）、**Std. State E0**（可逆电位，仅 Half Cell Potentials 开时）、**Entropy**（反应熵）。Global 组——**Open Voltage**（常数开路电压赋阳极半电池电位 Eq 20.11，阴极置零；仅 Half Cell Voltage 关时）、**Standard Temperature/Pressure**（Nernst 用标准态；仅 Half Cell Voltage 开时）、**Vaporization Rate/Condensation Rate**（Eq 18.47；仅 Phase Change 开时）、**Mod. Coef. OSM_drag**（Eq 18.47 常数；**默认 PEM/碱性 1.0、H2 Pump 0.001**；仅 Osmotic Drag 开时）。
  - **Customized 器件**（Figure 31.8–31.10）：Reactions... 定义反应（总数、名称、ID、反应物/产物数与相、组分与化学计量系数/速率指数/参考浓度；Butler-Volmer 参数——Exchange Current Density、Activation Energy、Reference Temperature（Eq 7.118/7.119）、Anodic/Cathodic Transfer Coefficient（Eq 7.118）、Equilibrium Potential（Eq 7.120）、电子数）；Mechanism... 定义机理（总数、ID、名称、勾选反应）；再为阴阳极选机理并设 Open Voltage 与 Mod. Coef. OSM_drag。
- **Anode/Cathode 选项卡**（阴阳极流程相同；Figure 31.11–31.14）：四类 Zone Type——
  - **Current Collector**：选区+固体材料（默认四材料 collector-default/porous-default/catalyst-default/electrolyte-default；**默认电导率表（p. 3411）**：电导率 S/m = 1e6 / 1e4 / 1e4 / 1e-16；电解液电导率 S/m = 1e-16 / 1e-16 / 2.3677 / 2.3677）；条件应用于 Zone(s) 全部所选区，需逐区设置时关 Update Cell Zones。
  - **Flow Channel**：选区即可。
  - **Porous Electrode**（多孔层）：选区+材料+单元区参数——**Porosity**（Eq 18.39）、**Absolute Permeability x/y/z**（黏性阻力倒数，Eq 31.1 笛卡尔渗透率矢量；**模型假定笛卡尔方向指定**，改方向须在 Fluid 对话框 Porous Zone 选项卡调）、**Capillary Pressure**（leverett-function 或 `DEFINE_CAPILLARY_PRESSURE` UDF；Leverett 参数——Contact Angle（Eq 20.35）、Coeff_a 默认 **1.417**、Coeff_b 默认 **2.12**、Coeff_c 默认 **1.263**（Eq 20.37））；可 Plot Capillary Pressure 对液相体积分数作图。
  - **Catalyst Layer**：Resolved 法设置同多孔层，另加 **Surface Volume Ratio**（活性比表面积，Eq 20.5/20.6）；**Unresolved 法**三参数——Surface Volume Ratio（Eq 18.51/18.52）、**Layer Thickness**（Eq 18.51/18.52）、**Catalyst Electrolyte Conductivity**（Eq 18.50）——**未解析法下催化层与膜不划材料，必须直接指定其电解液电导**。
- **Electrolyte 选项卡**（Figure 31.15/31.17）：
  - Resolved MEA：选区+材料+Porosity（Eq 18.39）与 Absolute Permeability（Eq 8.4 黏性阻力倒数）；可选 **Species/Water Permeation**（膜两侧高压向低压的组分/液水渗透；Edit 设物种数、各物种 Permeation Rate 与 Activation Energy，Eq 18.43）。
  - Unresolved 0D/1D：选 **Anode/Cathode Electrolyte 的 wall/wall-shadow 对**（求解器据此确定电化学源加入位置）；MEA Parameters 设 **Membrane Thickness** 与 **Membrane Electrolyte Conductivity**（Eq 18.50；原文对 Membrane Thickness 的描述文字误写为"电导率"，按名称与语义记录）；同样可选 Species/Water Permeation。
- **Electrical Tabs 选项卡**（Figure 31.18）：指定 Anode/Cathode Tabs——施加电位边界条件的外部壁面（方法由 Model 选项卡 Electrical System Setup 决定）。
- **Customization 选项卡**：`DEFINE_ELECTROLYSIS_ECHEM_RATE` 与 `DEFINE_ELECTROLYSIS_RELATIVE_PERMEABILITY` UDF 自定义传递电流与相对渗透率。
- **Advanced 选项卡**（Figure 31.19）：**Contact Resistivity**——选界面面区并设 Resistivity；porous jump 与 wall/wall-shadow 界面上接触电阻率**逐面施加**，只需在界面一侧设置否则实际电阻加倍。**Membrane Species Diffusion**——启用并为各物种设 Diffusivity；**默认 1e-15 m²/s 意味着膜区不考虑组分扩散**；为稳定性建议只允许少量组分跨膜扩散。
- **求解策略**：初始化后前约 **10–20 次迭代**禁用 Include Joule Heating 与 Electrochemistry Sources，让两个电位从初值调整到物理值，避免极端电化学反应/电流破坏解。

## 31.4 后处理（pp. 3423–3425）

- **电势场**：Properties... 类别——Electrical Conductivity（**各向异性模型下显示为零**；正交各向异性热传导时电导矩阵对称，YX/ZX/ZY 分量不提供以免冗余）、Electrical Conductivity XX|YY|ZZ|XY|XZ|YZ|YX|ZX|ZY（各向异性专属）。Potential... 类别——Electric Potential、Electric Current Magnitude、Joule Heat Source、X/Y/Z Current、dPotential/dx|dy|dz。电流场矢量图选 Electric Current。
- **锂离子电池**（Lithium... 类别）：Lithium Concentration、锂质量通量矢量模与 X/Y/Z 分量、Overpotential in Li-Intercalation Reaction；老化模型专属——SEI 生长/析锂反应过电位、Li Intercalation/SEI Formation/Li-Plating/Cathode Film Reaction Rate、SEI Mass、Li-Plating Mass、Cathode Film Mass、Film Thickness；肿胀模型——Swelling Strain。锂质量通量矢量图选 Lithium Mass Flux。
- **电解**（Potential... 类别）：Electrolyte Potential、Overpotential/Transfer Current/Osmotic Drag/Water Content/Capillary Pressure（mixture only）、Water Phase Change（phases only）。
- 定义见 Field Function Definitions（p. 4395）。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3381–3426（批次 92，2026-10-20，pypdf layout 模式提取；p. 3426 为仅含页脚的空页）。
- Theory Guide Eq 5.1、7.118–7.120、8.4、18.x（18.3/18.8/18.12/18.13/18.14/18.25–18.47/18.50–18.52）、20.x（20.5–20.14/20.35/20.37）公式体未提取，按引用记录变量与语义；大量符号占位（"is ___ in Equation…"）在文本层缺失，参数语义按名称与上下文记录。
- Table（p. 3411 默认电导率）文本层完整提取照录；Figures 31.1–31.19（对话框截图）为图形元素未摄取。
- 原文疑误两处照录并标注：①Unresolved MEA 的 Membrane Thickness 描述文字误写为"电导率"；②31.3 开头称器件用于 PEM/碱性电解，但 Device Type 清单含七类。
- 版本敏感：默认值（Faradaic URF 0.01/0.001、OSM_drag 1.0/0.001、Leverett 三系数、膜扩散 1e-15 m²/s、默认材料电导率表）以 2026 R1 为准。
- 相关页面：[[Fluent 电池模型]]（Ch.32 MSMD 整电池模型）、[[Fluent 流固耦合（FSI）]]（肿胀 FSI 用 intrinsic FSI 流程）、[[Fluent 多相流模型]]（Mixture 模型背景）。
