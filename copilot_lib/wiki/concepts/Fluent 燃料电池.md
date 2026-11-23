---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - fuel-cell
  - pemfc
  - addon-module
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 燃料电池

## 摘要

User's Guide 2026 R1 Part III / Chapter 33 "Modeling Fuel Cells"（PDF pp. 3537–3634，三节）。三个 add-on 燃料电池模块：①**PEMFC Model**——聚合物电解质膜燃料电池（可含微孔层），**新的推荐模型**；②**Fuel Cell and Electrolysis Model**（即 Resolved Electrolyte 模型）——PEMFC（低/高温）、SOFC、SOEC 通用；③**SOFC With Unresolved Electrolyte Model**——固体氧化物燃料电池。理论见 Theory Guide 对应三篇（Chapter 20）。**本页全章完成（批次 96–98，pp. 3537–3634）：33.1 PEMFC、33.2 Fuel Cell and Electrolysis、33.3 SOFC with Unresolved Electrolyte 三模块全节。**电化学器件的 GUI 内置版见 [[Fluent 电势场与电化学]]（Ch.31 的 Electrochemical Devices，与本章 add-on 模块是两套体系）。

## 33.1 PEMFC 模型（pp. 3537–3584）

### 33.1.1 概览与限制（p. 3538）

- 组成：若干 UDF + 图形界面；**电位场按 UDS 求解**；毛细压力、溶解水含量、流道液饱和也各为 UDS；催化层电化学反应以源项建模，其余参数经界面输入；支持并行。
- **限制**：各向异性组分扩散率选项与 PEMFC 模型不兼容。

### 33.1.2 几何定义（p. 3538）

网格须含九区：阳极流道、阳极气体扩散层（GDL）、阳极微孔层（MPL，可选）、阳极催化层、膜（固体）、阴极催化层、阴极 MPL（可选）、阴极 GDL、阴极流道；如有则标认：阳/阴极集流体（固体）、冷却流道。

### 33.1.3–33.1.4 安装与加载（pp. 3538–3539）

- 随标准安装位于 `addons/pemfc`（UDF 库 + 预编译 Scheme 库）；**须先设置/读入有效 case** 才能加载。
- 两种加载：①Physics ribbon → Models 组 More → **PEM Fuel Cell Model...**；②TUI `define/models/addon-module` → 模块号 **9**（本列表 0–9：1 MHD、2 Fiber、3 Fuel Cell and Electrolysis、4 SOFC with Unresolved Electrolyte、5 Population Balance、6 Adjoint、7 Single Potential Battery、8 MSMD Battery、9 PEM Fuel Cell）。加载时装入 Scheme 库（GUI/TUI）与 UDF 库。

### 33.1.5 工作流（pp. 3539–3540）

十步：启动（**必须 3D 双精度**，仅 3D 可用）→ 读 case/网格 → 缩放 → PEM Fuel Cell Model 对话框定义参数 → 材料属性 → 操作条件 → 边界条件 → 计算 → 存盘 → 后处理。**对话框简化输入但不取代边界条件界面**——先用对话框完成主体设置、再做边界条件收尾。

### 33.1.6 设置（pp. 3540–3577）

启用：Setup → Models → PEM Fuel Cell → Edit，勾 Enable PEMFC。八组输入（模型选项/参数/阳极/电解液/阴极/高级/求解控制/报告）。**默认值取自文献**（Theory Guide Bibliography 编目）。

#### 33.1.6.1 Model 选项卡（pp. 3542–3547）

- **Options**：**Joule Heating**（欧姆热，能量源项附加项，见 Theory Guide Table 20.1）；**Reaction Heating**（电化学反应热）；**Electrochemistry Sources**（只关心基本流场时可关——也可先关得初始流场再开）；**Butler-Volmer Rate**（默认；关则用 Tafel 近似 Eq 20.7/20.8）；**Liquid Phase**（液相输运；默认启用）；**Multicomponent Diffusion**（全多组分扩散 Eq 20.47，否则默认 Eq 20.45）；**Anisotropic E-cond. in GDL/MPL**（多孔电极纤维结构导致跨面电导比面内小数量级——启用后固体材料的 Electrical Conductivity 不再使用，改为 Create/Edit Materials 中 UDS Diffusivity 选 **defined-per-uds** 并为 UDS-0 选 anisotropic/orthotropic/cyl-orthotropic 三者之一设值）；**Effective P-Cond. in MEA**（按离子导体体积分数与迂曲度算电解液相电导 Eq 20.48；关闭则取常数）；**Use Half-Cell Potentials**（Nernst 方程算阴阳极半电池电位 Eq 20.13/20.14；关闭则阳极半电池置零、阴极取 Parameters 页 V_Open 常数开路电压）；**Cathode Particle Model**（阴极颗粒模型）；**Compute Liquid in Channels**（解流道液饱和方程 UDS-4、黏性阻力作动量源项；默认关闭）；**Include Dynamic Head**（流道动压，Eq 20.35）；**Knudsen Diffusion**（Knudsen 扩散进有效气体扩散率，Eq 20.47）；**Temperature Dependent Jref**（默认启用——参考交换电流密度温度依赖 Eq 20.9/20.10，可为阴阳极催化层分别给 Activation Energy 与 Reference Temperature for J_ref）；**N2 Crossover**（默认关；氮跨膜通量，需在 Parameters 设 N2 Crossover factor）；**Ice Phase**（仅瞬态、默认关；冰相 Eq 20.41，需给 Desublimation/Sublimation Rate）；**W-Diff Model** 二选——**Wu**（Eq 20.51）或 **Wang**（Eq 20.52）。
- **Electrical System Setup** 三法：**Set Up in B.C. Panels**（用 BC 面板的 UDS0 电位边界）；**Specify Total Voltage**（BC 面板 UDS0 被忽略——阳极 tab 自动置零、阴极 tab 加固定 Total Voltage；常量或表达式）；**Specify Total Current**（阳极 tab 置零、阴极 tab 加恒流通量 = Total Current ÷ Electrolyte Projected Area（Reports 页设定））。
- **Under-Relaxation Factors** 四项：**Liquid-Vapor**（毛细压力方程 Eq 20.33 的显式源项——通常需小值才收敛）、**Disv'd-Vapor/Liquid**（Eq 20.25 源项）、**Osmotic Drag Source**（Eq 20.25 左端项）、**GDL Liquid Removal**（GDL-流道界面液态水外流 Eq 20.35）。
- **Automatic Settings**：**F-cycle for All Equations**——全方程多重点火 F 循环（覆盖 Advanced Solution Controls 的逐方程设置）；**PEMFC 计算的最佳实践**。

#### 33.1.6.2 Parameters 选项卡（pp. 3547–3551）

- **Electrochemistry**（阴阳极各一组）：**J_ref**（参考交换电流密度，Eq 20.9/20.10）、**C_ref**（参考浓度，1 kgmol/m³，Eq 20.5/20.6）、**Con. Exponent**（浓度依赖指数）、**Exch. Coeff. (a)/(c)**（传递系数）、**Std. State E0**（可逆电位——仅 Use Half-Cell Potentials 开）、**Entropy**（反应熵）、**V_Open**（常数开路电压——仅半电池关时）、**I_leak**（泄漏电流密度 A/m²；总泄漏电流 = I_leak × 电解液投影面积，Eq 20.55–20.57——泄漏使电池发电变少，低燃料/空气利用率时尤甚；也可用 `Leakge_Current()`（原文拼写照录）UDF 给总泄漏电流）、**Std.Temp. for U0 (K)** 与 **Std. Press. for U0 (Pa)**（Nernst 标准态，仅半电池开）。
- **Reference Diffusivity**（仅 Multicomponent Diffusion 关时；组分质量扩散率 Eq 20.45）。
- **Liquid Phase** 组（Liquid Phase 开时）：Expon't Diff_gas（Eq 20.45 多相）、Expon't J_ref（液堵反应面修正 Eq 20.38）、Expon't K_rel（相对渗透率 Eq 20.31）、Expon't Liq_coverage（相变速率 Eq 20.26/20.27）、Liq.-Disv'ed Phase（液-溶解相质量交换速率常数 Eq 20.27）、Liquid Density 与 Liq.Thermal Cond.（多孔介质有效导热按式 33.1 混合）、Liq. Diff. in Chan.（Eq 20.39；Compute Liquid In Channel 开）、V_liq/V_gas in Chan.（流道液气速比 Eq 20.40；同前）。
- **Other Parameters**：Gas-Disv'ed Phase（气-溶解相交换速率常数 Eq 20.26）、Mod. Coef. OSM_drag（默认 **1.0**，Eq 20.53 电渗透拖曳系数泛化）、Eq.W. Cont. at a=1（水活度 1 的平衡水含量，Eq 20.28）、Eq.W. Cont. at s=1（饱和 1 的平衡水含量；Liquid Phase 开）、N2 Crossover Factor（Eq 20.23）、Desublimation Rate 与 Sublimation Rate（Eq 20.42；Ice Phase 开）。

#### 33.1.6.3 Anode 选项卡（pp. 3551–3560）

五种 Zone Type（电堆建模时同类区**必须整组选择**；Update Cell Zones 默认开——条件应用于 Zone(s) 全部所选区，需逐区设则关）：

- **Current Collector**：选区 + 固体材料；**Electrical Conductivity 在对话框中只能取常量**（其值 = 固相电位的扩散率）。
- **Flow Channel**：选区即可。
- **Porous Electrode**（GDL）：材料 + **Porosity**（Eq 20.45）、**Absolute Permeability**（Eq 20.30；**只支持各向同性**——Fluid 对话框各向异性黏性阻力设置被忽略）、**H-phobic Contact Angle**（Eq 20.36）、**Bruggeman Coef.**（Eq 20.45）、**Water Removal Coef.**（Eq 20.35）、Leverett 三系数 a/b/c（默认 **1.417/2.12/1.263**，Eq 20.37）、Condensation/Evaporation Rate Coeff.（Eq 20.34）、Pore Size（平均孔径，Eq 20.108）。
- **TPB Layer (Catalyst)**：多孔电极全参数 + **Surface/Volume Ratio**（活性比表面积，Eq 20.5）+（Effective P-Cond. in MEA 开）Protonic Conduction Coefficient（Eq 20.49）/Protonic Conduction Exponent（Eq 20.48）/Ionomer Tortuosity/Ionomer Volume Fraction/Activation Energy for P-Cond +（Temperature Dependent Jref 开）Activation Energy 与 Reference Temperature for J_ref + Leverett/冷凝蒸发/孔径。
- **Micro Porous Layer**（可选）：多孔电极参数减 Water Removal Coef.（即 Porosity/渗透率/接触角/Bruggeman/Leverett 三系数/冷凝蒸发/孔径）。

#### 33.1.6.4 Electrolyte 选项卡（pp. 3560–3561）

膜**只能按固体区建模**，但允许溶解水、液态水/毛细压力与离子电流通过。参数：**Equivalent Weight**（Eq 20.26/20.27）、Protonic Conduction Coefficient/Exponent、**Water Diffusivity Coefficient**（Eq 20.50）、Activation Energy for P-Cond（Effective P-Cond 开时）、Absolute Permeability（Eq 20.30）。

#### 33.1.6.5 Cathode 选项卡（pp. 3561–3565）

与阳极同法（集流体/流道/多孔电极/MPL 照搬）。催化层（TPB Layer）差异：Surface/Volume Ratio 用 Eq 20.6、J_ref 温度依赖用 Eq 20.10；**Cathode Particle Model 开时额外三参数**——Prod. Of O2 Solubility and Diffusivity（Eq 20.16）、Radius of Catalyst Particle、Cathode Ionomer Resistance（Eq 20.15）。

#### 33.1.6.6 Electrical Tabs 选项卡（p. 3565）

指定 Anode/Cathode Tabs——施加电位（UDS0）边界条件的外部壁面（方法由 Model 选项卡 Electrical System Setup 决定）。

#### 33.1.6.7 Advanced 选项卡（pp. 3565–3572）

- **Contact Resistivity**：选界面面区设 Resistivity；**只作用于 wall 与 porous-jump 类型界面**；porous jump 与 wall/wall-shadow 界面上逐面施加——**只在界面一侧设置，否则电阻加倍**；**Use First Value for All** 可把第一区的值用于全部。
- **Coolant Channel**（可选）：选区 + Coolant Density；勾 **Enable Coolant Modeling** 自动创建混合物材料 `pem+cool-mixture`（hydrogen/oxygen/water-vapor/coolant-liquid/nitrogen）——该混合物只在冷却流道内质量分数为 1.0、不影响其他流体区；其余混合物属性自动设 ideal-gas-mixing-law；再到 Create/Edit Materials 设 coolant-liquid 其余属性；冷却流道进出口用标准边界条件。
- **Stack Management**（电堆）：**单电池无需设置**。"燃料电池单元"= 电堆中单电池的全部区；Create 新建单元（默认名）、选中可 Modify（区集合自动回填 Zone(s) 列表）或 Delete（**删除时确保电气连通性完好**）。**Match Zone Name Pattern** 支持 `*`/`?` 通配批量选区——电堆 10–100 单元 × 每单元 ≥9 区易达数百 cell zone，建议给网格区按电池编号命名再用模式匹配。
- **Degradation（材料化学退化，独立模型）**：Advanced Setup → Degradation → Setup... → 勾 **Degradation Model**——自动创建混合物材料 `degradation-membrane`（可查改组分与反应、也可自建退化混合物）；选 Mixture Material、从 Available Species 选退化组分并在 Initial Concentration 给初值（**首次运行建议给全组分初值**）；给 Temperature、Time Step、Stop Time。启用后**自动加 UDS-5**——溶解相 OH 自由基摩尔浓度，只在催化层与膜区求解；其源项来自两个电化学反应（Eq 33.2/33.3，平衡电位 **0.695 V** 与 **1.76 V**；速率 Eq 33.4/33.5，参考电流密度 **0.01 A/m²** 与 **10⁻⁵ A/m²**；式中膜密度/当量/水含量参与）。流程：初始化并跑完 PEMFC 仿真 → 重开 Degradation Model 对话框 → **Calculate Initial Conditions**（按 PEMFC 结果估 OH 初值）→ **Calculate Degradation** 跑独立退化模型 → Species to Plot 选组分 Plot 看时间历程，可调参重跑。

#### 33.1.6.8 Customized UDFs 选项卡（pp. 3572–3573）

勾 **Customize PEMFC Module** → **Module Compilation Tool...** → Compiled Customized Addon Module 对话框——**Copy User-Modifiable File to the Working Directory**（自动从安装目录拷贝：PEMFC 用 `pemfc_user.c`、Fuel Cell and Electrolysis 用 `pem_user.c`、SOFC 用 `constit.c`）或 Browse 自带源文件 → **Create Customized Addon Library**。

#### 33.1.6.9 Reports 选项卡（pp. 3573–3576）

- **Create Monitors**：运行时自动写七个监控 .out 文件——`cell-voltage.out`、`mean_h2.out`/`min_h2.out`（阳极流体区 H2 摩尔分数均值/最小）、`mean_o2.out`/`min_o2.out`（阴极 O2）、`total-current-anode.out`/`total-current-cathode.out`；**Monitor Frequency** 设写入间隔（如 10 = 每 10 迭代更新）。
- **Inlet Condition Calculator**：输入 Ref. Current Density、Ref. Membrane Area、阳极/阴极的 Temperature（°C）/Relative Humidity（%）/Pressure（Pa）/Stoichiometry（基于总电流）→ **Compute Inlet Conditions** 输出阳极 Mdot（kg/s）/T（K）/Y_h2/Y_h2o 与阴极 Mdot/T/Y_h2o/Y_o2/Y_n2——**只是换算辅助，仍需手填入对应 BC 对话框**；结果基于整电池/电堆总参考电流——**多个相同入口时须把总流量均分**。

#### 33.1.6.10 自动挂接的 UDF（pp. 3576–3577，Table 33.1）

点 OK/Apply 后自动挂接：density（DEFINE_PROPERTY，冷却混合物密度，仅 Advanced 启用冷却时）；diff/cond（DEFINE_DIFFUSIVITY，混合物质量扩散率/UDS 扩散率）；uds_flux；source_s/source_m（催化区 UDS-0 电位/UDS-1 质子电位源项）；source_h2/source_o2（阴阳极催化层组分源）；source_h2o/source_mass（全流体区）；source_lambda（催化层与膜水含量源）；source_energy；source_liquid（多孔层与催化层毛细压力 UDS-2 源）；source_chan_liq（流道液饱和源）；source_momentum（流道动量源）；initialize（DEFINE_INIT）；adjust（每迭代）；unsteady（瞬态 UDS）；write/read_sec_hdf（DEFINE_RW_HDF_FILE）；pem_lib_load（DEFINE_EXECUTE_ON_LOADING）；exec_at_end；set_new_stack_voltage/current 与 get_old_stack_voltage/current（DEFINE_ON_DEMAND）；list_pemfc_udf（列出所用 UDS/UDM）；report_current（报告总电流）；aniso_econd（DEFINE_ANISOTROPIC_DIFFUSIVITY，仅 Anisotropic E-cond. in GDL/MPL 开时）。**DEFINE_SOURCE 与模型设置不一致时控制台告警**——关闭再重开对话框点 OK/Apply 可恢复默认源项设置。

### 33.1.7 边界条件（pp. 3577–3579）

- **阳极入口**：质量流量、温度、方向指定方法、质量分数（h2、h2o）；启用冷却流道时 **coolant 组分须设 0**；**UDS-4（流道水饱和）设 0**。
- **阴极入口**：同上（o2、h2o、n2；coolant 0；UDS-4 = 0）。
- **冷却入口**（如有）：质量流量、温度、方向；**coolant 质量分数设 1**；UDS-4 = 0。
- **压力出口（全部）**：设合理的回流（backflow）条件。
- **阳极端子**：温度（或热流）；Set Up in B.C. Panels 法时在 Wall 对话框 UDS 选项卡把 Electric Potential（UDS-0）设为**地电位 0——无论阴极端子用电压还是电流条件，阳极端子都必须锚零**。
- **阴极端子**：温度；UDS-0 设 Specified Value（电压 V）或 Specified Flux（电流密度 A/m²）——**阴极侧 UDS-0 通量符号取负**（电流/正电荷离开阴极端子）。

### 33.1.8 求解指南（p. 3579）

- 恒电位边界：从接近开路电压的电池电压算起，逐步降低电压求后续稳态解；恒电流边界：从低电流算起逐步升高。
- 收敛困难时：把物种与两个电位方程的多重网格循环改 **F-cycle + BCGSTAB 稳定化**；物种与 UDS 方程的多重网格终止判据可能需调小（数值在文本层缺失未照录）；**电堆仿真两电位方程终止判据可再调小**。
- 初始化后前约 **5–10 次迭代**关掉 Joule Heating 与 Reaction Heating，让两个电位从初值调整到物理值，避免极端电化学反应/电流破坏解。

### 33.1.9 后处理（pp. 3579–3580）

- **UDS 分配**（Table 33.2）：UDS 0 Electric Potential（固相电位 V）、UDS 1 Protonic Potential（膜相电位 V）、UDS 2 Capillary Pressure、UDS 3 Water Content、UDS 4 Liquid Saturation in Channels。
- **UDM 分配**（Table 33.3）：UDM 0–3 电流通量密度 X/Y/Z/模（A/m²）、UDM 4 Ohmic Heat Source、UDM 5 Reaction Heat Source（W/m³）、UDM 6 Overpotential（V）、UDM 7 Evaporation to Vapor（kg/m³·s，Eq 20.30）、UDM 8 Osmotic Drag Coefficient、UDM 9 Water Activity、UDM 10 Equilibrium Water Content、UDM 11/12 Absorption from Vapor/Liquid（kg/m³·s，Eq 20.25）、UDM 13 Transfer Current（A/m³）、UDM 14 Liquid Saturation in Porous Media、UDM 15 GDL Liquid Removal、UDM 16 Osmotic Drag Source、UDM 17 Capillary Pressure（Pa）、UDM 18 Pressure Gradient Source。
- 清单查看：Execute On Demand 对话框下拉或 TUI 敲 `list_pemfc_udf`。

### 33.1.10 用户可访问函数（pp. 3581–3584，pemfc_user.c）

可改属性公式：Get_P_sat（水蒸气饱和压 Eq 20.54）、Water_Activity（Eq 20.29）、Osmotic_Drag_Coefficient（Eq 20.53）、Membrane_Conductivity（Eq 20.48）、Water_Content_Diffusivity（Eq 20.50）、Gas_Diffusivity（Eq 20.45）、MCD_Gas_Diffusivity（多组分修正）、Compute_Js（Leverett J(s)–s 关系 Eq 20.36）、Capillary_P_Diffusivity（Eq 20.30）、Water_Content、Anode/Cathode_AV_Ratio（Eq 20.5/20.6）、Anode/Cathode_J_TransCoef、Open_Cell_Voltage（Eq 20.11/20.12）、Leakage_Current（Eq 20.55–20.57）、resistance_in_channel（流道动量阻力随液饱和）。`Set_UDS_Names`/`Set_UDM_Names` 可重命名 UDS/UDM（单位不可改；STRING_SIZE 固定于 pemfc.h 不可改）——**载入旧 case 时检查体/面监视器引用的 UDS 名是否仍正确**。另有（节尾跨至 p. 3585 顶部）：Phase_Change_const（改气液相变速率常数）、Equilibrium_Water_Content(act, sat)（改平衡水含量计算，Eq 20.28）、Dissolved_Water_Masstransfer（溶解水-水汽/液水传质速率 mt_gd/mt_ld/dS，Eq 20.25）、Phase_Change（水汽-液水传质速率，Eq 20.25）。

## 33.2 Fuel Cell and Electrolysis 模型（pp. 3585–3617）

### 33.2.1 概览与限制（pp. 3585–3586）

UDF + 图形界面；电位场按 UDS 求解；液态水饱和与水含量各为 UDS；催化层电化学反应以源项建模；支持并行。**限制**：各向异性组分扩散率选项不兼容。（33.1.10 的 pemfc_user.c 函数清单末尾四个函数跨在本节首页 p. 3585 顶部，已并入上节。）

### 33.2.2 几何定义（p. 3586）

七区（**无微孔层**）：阳极流道、阳极 GDL、阳极催化层、膜、阴极催化层、阴极 GDL、阴极流道；如有则标认：阳/阴极集流体、冷却流道。

### 33.2.3–33.2.5 安装/加载/工作流（pp. 3586–3588）

`addons/fuelcells`；须先有有效 case；ribbon **Fuel Cell & Electrolysis Model...** 或 TUI addon-module 模块号 **3**。工作流十步（与 PEMFC 同；**无 3D 双精度强制表述**）。默认已启用 PEMFC 模型，可改选 SOFC 或 SOEC。对话框不取代 BC 界面。

### 33.2.6 设置（pp. 3588–3610）

- **Model 选项卡**：模型三选 **PEMFC / SOFC / SOEC**。选项（**几乎全部默认开**）：**High Temperature PEM**（高温 PEMFC；不开=低温模型）；Joule Heating（Eq 20.85 欧姆项）；Reaction Heating（含传递电流×过电位积）；Electrochemistry Sources（要关掉模块全部影响须连同 **Membrane Water Transport 与 Multiphase** 一起关）；Butler-Volmer Rate（默认；关= Tafel Eq 20.72）；Membrane Water Transport（跨膜水输运；仅低温 PEMFC 可用）；Multiphase（GDL 近似液态输运；仅低温）；Multicomponent Diffusion（Eq 20.92，否则默认 Eq 20.90）；Anisotropic E-cond in GDL/MPL（同 PEMFC 三选项 defined-per-uds + UDS-0 anisotropic/orthotropic/cyl-orthotropic；此时电解液固体材料的 Electrical Conductivity 被忽略）；Knudsen Diffusion（Eq 20.92）。
- 低温 PEMFC 的 **URF**：**Saturation Source**（Eq 20.87 饱和源项通常需欠松弛）与 **Water Content**（Eq 20.98）。
- **Automatic Settings**：**Enable Smooth Partition**（并行时用 Metis 分区 + Laplace 光顺）；**F-cycle for All Equations**（同 PEMFC）。
- **Parameters 选项卡**：阴阳极各——Ref. Current Density（Eq 20.69/20.70）、Ref. Concentration、Concentration Exponent、Exchange Coefficient (a)/(c)、**Open-Circuit Voltage**（Eq 20.74）、**Leakage Current**（总泄漏电流 A，Eq 20.102–20.107；也可用 `Leakge_Current()`（拼写照录）UDF）；另——Reference Diffusivities（Multicomponent Diffusion 开则不需要）、Pore Blockage for Gas Diffusion（Eq 20.90 多相）、**Pore Blockage for Transfer Current**（液堵反应面，修正式 20.69–20.72）、Exponent for relative permeability（Eq 20.88）。
- **符号约定告诫**：电解等耗电装置常规把负电压接阴极；Fluent 反其道——**负电压接阳极、阴极保持正电**（电解与燃料电池共用同一套架构）。手册与界面中的 anode/cathode 均按供电装置的惯例解释。
- **Anode/Cathode 选项卡**：四种 Zone Type——Current Collector（电导率仅常量）、Flow Channel、Porous Electrode（材料 + **Porosity + Viscous Resistance** + Contact Angle（Eq 20.89 多相）+ Pore Size（Eq 20.108）——注意此处给黏性阻力而非绝对渗透率）、TPB Layer (Catalyst)（多孔电极全参 + Surface/Volume Ratio，Eq 20.69/20.70）；电堆同类区整组选、Update Cell Zones 默认开。
- **Electrolyte 选项卡**：低温 PEMFC 专属参数——Equivalent Weight（Eq 20.96）、Protonic Conduction Coefficient/Exponent（Eq 20.94）。**膜可建模为流体区或固体区**（区别于 PEMFC 模块的仅固体）；PEMFC 下水与离子电流仍可穿过。
- **Advanced 选项卡**：Contact Resistivity（同 PEMFC——仅 wall 与 porous-jump、逐面施加单侧设置、Use First Value for All）；Coolant Channel——直接给 Density/Heat Capacity/Thermal Conductivity/Viscosity 四属性，勾 **Enable Coolant Channel(s)** 后混合物加入 coolant 组分；Stack Management——燃料电池单元 Create/Modify/Delete 与 Match Zone Name Pattern 同 PEMFC，另加 **Suggest Stack Setup** 自动识别电堆单元（要求 Anode/Electrolyte/Cathode 选项卡已给集流体/多孔电极/TPB 催化层区信息、Electrolyte 给膜区、Advanced 给冷却流道、Reports 给外部接触面；**输入不全或设计非常规时结果可能不准，点 OK/Apply 前须自行核验**）。
- **Customized UDFs**：同 PEMFC 编译流程（源文件 pem_user.c）。
- **Reports 选项卡**：**Electrolyte Projected Area**（MEA 投影面积，仅用于算平均电流密度；可用 Projected Surface Areas 对话框算）；**External Contact Interface(s)**（阴阳极外部接触面）——用于报告电池电压：恒电位=两给定值之差；恒电流=解的一部分。

### 33.2.7 集流体建模（pp. 3610–3611）

UDS 现可在固体区求解——集流体可用**固体区、流体区或多孔介质区**建模。用流体区代替固体集流体时自动置零速度并切断组分输运；用固体区则需**在固体区激活 UDS-0（电位）求解**并在材料中设 Electrical Conductivity——**重要：UDS Diffusivity 必须设为 user-defined（cond::fuelcells），不要用 defined-per-uds**（与 PEMFC 模块的 GDL/MPL 各向异性设法相反）。

### 33.2.8 边界条件（pp. 3612–3613）

与 PEMFC 基本相同，差别：入口置零的是 **UDS-2（Water Saturation）**（而非 UDS-4）；冷却入口 coolant 质量分数 1；压力出口设合理回流；阳极端子 UDS-0 接地；阴极端子 UDS-0 设电压或电流密度通量（**符号为负**，SI 单位）。

### 33.2.9 求解指南（p. 3613）

与 33.1.8 相同：恒电位从近开路电压起步、恒电流从低电流起步；F-cycle + BCGSTAB；终止判据数值文本层缺失；前 5–10 迭代关 Joule/Reaction Heating。

### 33.2.10 后处理（pp. 3613–3614）

- **UDS**（Table 33.4）：UDS 0 Electric Potential、UDS 1 Protonic Potential、**UDS 2 Water Saturation**、UDS 3 Water Content。
- **UDM**（Table 33.5）：UDM 0–3 电流通量密度 X/Y/Z/模、UDM 4 Ohmic/UDM 5 Reaction Heat Source、UDM 6 Overpotential、UDM 7 Phase Change Source、UDM 8 Osmotic Drag Coefficient、UDM 9 Liquid Water Activity、UDM 10 Membrane Water Content、UDM 11 Protonic Conductivity（1/ohm·m）、UDM 12 Back Diffusion Mass Source、UDM 13 Transfer Current、UDM 14 Osmotic Drag Source。查看用 list_pemfc_udf。
- **注意**：存于 UDM 的场变量用对应变量做后处理，**不建议直接后处理 UDM 本身**；CFD-Post 查看先导出 .cdat；旧 case 监视器 UDS 名核对。

### 33.2.11 用户可访问函数（pp. 3615–3617，pem_user.c）

Get_P_sat（Eq 20.101）、Water_Activity（Eq 20.99）、Water_Content（Eq 20.98）、Osmotic_Drag_Coefficient（Eq 20.95）、Membrane_Conductivity（Eq 20.94）、**Electrolyte_Conductivity**（Eq 20.93，仅 SOFC/Electrolysis）、Water_Content_Diffusivity（Eq 20.97）、Gas_Diffusivity（Eq 20.90）、MCD_Gas_Diffusivity（Eq 20.92）、Saturation_Diffusivity（Eq 20.86）、Anode/Cathode_AV_Ratio、Anode/Cathode_J_TransCoef、Open_Cell_Voltage（Eq 20.74）、Leakage_Current、Set_UDS_Names/Set_UDM_Names（STRING_SIZE 固定于 pem.h）。另有（节尾跨至 p. 3618 顶部）：传递电流函数（输出阴阳极体积传递电流 source 及其对活化损失的偏导 *dRade/*dRcde，Eq 20.69/20.70）与 Thermal_ctk_pemfc（把 Porous Jump 对话框中多孔区热接触电阻常数改为随位置变化的值）。

## 33.3 SOFC With Unresolved Electrolyte 模型（pp. 3618–3634）

### 33.3.1–33.3.3 限制/安装/加载（pp. 3618–3620）

**限制**：各向异性组分扩散率选项不兼容。`addons/sofc`；须先有有效网格/case；ribbon **SOFC Model with Unresolved Electrolyte...** 或 TUI addon-module 模块号 **4**；树项 Setup → Models → SOFC (Unresolved Electrolyte)，勾 **Enable SOFC Model**。

### 33.3.4 设置流程与自动配置（pp. 3620–3623）

**3D 双精度、仅 3D**。启用模型时自动应用：Pressure-Based 稳态求解器（Absolute 速度公式）、能量方程、层流黏性模型、组分输运（Volumetric reactions；Inlet Diffusion **关**、Diffusion Energy Source 开、Full Multicomponent Diffusion 开、Thermal Diffusion 开）、全方程 AMG **F-cycle**、并行 **Metis 分区 + Laplace 光顺**。自动创建材料：混合物（h2o/o2/h2/n2；导热与黏度 ideal-gas-mixing-law；**Mass Diffusivity 用 `diffusivity::sofc` UDF、UDS Diffusivity 用 `E_Conductivity::sofc` UDF**）与四种固体材料（anode-collector-default、anode-default、cathode-collector-default、collector-default）。**注意**：支持电解质材料的 shell conduction（横向导热），但**不支持电解质内类似的横向导电**。考虑 H2/CO 电化学时混合物须含 CO 与 CO2。随后：边界/操作条件 → 残差收敛判据**全方程设 1e-08** → 默认值初始化。
- **UDM 分配**（Table 33.6）：UDM-0 Interface Current Density（A/m²，**守恒通电量**——电解液面面积分=总电流；电场求解时在电解液面算出）、UDM-1 Nernst Potential、UDM-2 Activation Overpotential（原文拼写照录）、UDM-3 Volumetric Ohmic Source（W/m³）、UDM-4/5/6 电流密度 x/y/z 分量（**单元中心值、非守恒**——受电导与几何影响可能与 UDM-0 不符，类似速度插值质量通量的固有差异）、UDM-7 Electrolyte Voltage Jump、UDM-8 Electrolyte Resistivity（**线性化量，无物理意义**）、UDM-9 Effective Electric Resistance、UDM-10/11 阴/阳极 Activation（分列的活化极化）、UDM-12 Electrochemical Source（W/m³）、UDM-13 Current Density Magnitude。
- **UDS**：仅 UDS-0 Electric Potential（V）。UDM 不直接后处理（用对应变量）；CFD-Post 用 .cdat 导出。

### 33.3.5 SOFC Model 对话框五选项卡（pp. 3623–3632）

- **Model Parameters**：选项——**Enable Electrolyte Conductivity Submodel**（电解质离子电导随温度变化，Eq 33.6，**仅 1073–1373 K 有效**）；**Enable Volumetric Energy Source**（导电区欧姆热——电位场收敛到一定程度**之前保持关闭以免拖慢收敛，之后手动打开**）；**Enable Surface Energy Source**（排除电化学反应热与全部可逆过程的给热——**必须始终开启**）；**Enable Knudsen Diffusion**（孔隙 Knudsen 数远大于 10 时有用，Eq 20.108）；**Enable Species Sources**（**必须始终开启**）；**Enable Electrolysis Mode**（SOFC 反转：由水蒸气产氢氧——Total System Current 须给负值（正值自动内部变号）；Converge to Specified System Voltage 须大于开路电压）；**Disable CO Electrochemistry**（燃料含 CO 但不参与电化学时勾；与电解模式互斥）。
- **Current Under-Relaxation Factor 建议设 0.3 或 0.2**（初期对大电流波动极敏感）。
- Electrical/Electrolyte 参数：**Total System Current**；**Converge to Specified System Voltage**（改给定电压）；**Set Individual Electrical Boundary Condition from Boundary Conditions Task Page**（逐集流边界直接给电流密度或电压，可多种类型混用）；**Leakage Current Density**（氧化剂渗漏+短路电流总和；温度相关实现改 constit.c 的 `Leakage_Current_Density(real T)` 后自编 sofc UDF 库）。
- **Automatic AMG Settings**：**F-Cycle for All Equations** 默认启用（推荐；可在 Advanced Solution Controls 调整）。
- **Electrochemistry 选项卡**：**Constant Exchange Current Densities**——阳极默认 **1e+10 A**、阴极默认 **100 A**（Butler-Volmer Eq 20.121）；**Mole Fraction Reference Values**（H2/O2/H2O 默认 1 moles/moles，Eq 20.122–20.124）；**Concentration Exponents**（H2/H2O/O2 默认 **0.5**，Eq 20.123/20.124 的计量因子指数）；**Butler-Volmer Symmetry Factors**——两反应的 Anodic/Cathodic Transfer Coefficient 默认 **0.5**（正逆反应对称假设；若要改对称因子或有其他速率限制反应，建议同步考虑改浓度指数）；**Temperature Dependent I_0**（勾选后按电极给速率系数 **A、B**，Eq 20.125）。
- **Electrolyte and Porous Zones 选项卡**：选 **Anode Electrolyte** 与 **Cathode Electrolyte** 界面区；**Tortuosity Zones and Values**——多孔区迂曲度（孔隙效应使质量扩散系数按 Eq 33.7 缩减；**典型 2–4、可更高**；无标准测量手段，实验测或调参匹配）；勾 Knudsen 扩散时设 **Knudsen Diffusion Zones and Pore Sizes**（每多孔区有效孔半径，Eq 20.108）。
- **Electric Field 选项卡**：**Conducting Zones and Conductivities**（导电区+电导率）；**Contact Surfaces and Resistance**（接触面+电阻）；**Voltage Tap Surface**（接地表面，φ=0）；**Current Tap Surface**（引出电流的表面，被赋值）。
- **Customized UDFs 选项卡**：编译 constit.c 定制（流程同 33.1.6.8）。

### 33.3.6 用户可访问函数（pp. 3632–3633，constit.c）

Nernst（Eq 20.117，含 DNDY 输出）、Activation（解 Eq 20.122 求活化过电位，含 dA_di）、Resistivity(T)（常数或 Eq 33.6）、Leakage_Current_Density(T)、Solve_Butler_Volmer_NR（Newton-Raphson 解 Eq 20.122）、CONDUCTIVITY_CELL（导电区组 ID **1–5** 查表、非导电区返回 0）、CONTACT_RESIST_FACE（接触电阻组 ID **1–3**、非接触面返回 0）、h2_co_split_func（H2/CO 分配因子，Eq 20.141，可覆写）。

**Ch.33 全章完成（pp. 3537–3634）。**

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3537–3634（批次 96–98，2026-10-20，pypdf layout 模式提取；p. 3634 为仅含页脚的空页）。
- Theory Guide Chapter 20 各式（20.5–20.141 引用到者）与 Eq 33.1–33.7 公式体未提取，按引用记录变量与语义；33.1.8/33.2.9 中多重网格终止判据的数值在文本层缺失未照录。
- Figures 33.1–33.42（对话框截图）与 Table 33.1–33.7（表内容照录）为图形/表格元素；Table 20.1 式号引用未展开。
- 版本敏感：add-on 模块编号（本章列表 0–9，与 Ch.26 MPM 章所载 0–10 列表不同——以加载时实际显示为准）、默认值（OSM_drag 1.0、Leverett 三系数、OH 反应电位/参考电流密度、监视频率）以 2026 R1 为准。
- 相关页面：[[Fluent 电势场与电化学]]（Ch.31 内置 Electrochemical Devices）、[[Fluent 电池模型]]（Ch.32 add-on 电池模块）。
