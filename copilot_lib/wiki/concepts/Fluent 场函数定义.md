---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - field-functions
  - field-variables
  - reference
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 场函数定义

## 摘要

User's Guide 2026 R1 Part III / Chapter 43 "Field Function Definitions"（PDF pp. 4395–4524，五节）。**本页全章完成（批次 118–120，pp. 4395–4524）：43.1–43.5 全五节——节点/单元/面值语义、速度报告选项、分类场变量表（24 表）与限制代码、字母序清单 A–M 摘录、自定义场函数创建/管理/示例。**本章为参考章——变量清单以后处理下拉列表中的显示名为准。

## 43.1 节点、单元与面值（pp. 4395–4397）

- **43.1.1 单元值（Cell Values）**：多数变量存于单元——单元内整个区域取该值。表面单元值 = 被 surface facet/line 相交或包含 surface point 的单元值（唯一确定）。边界上单元值典型 = 边界邻单元值；**face-only 函数（如 Wall Shear Stress）的单元值 = 该单元作为 c0 的面值面积加权平均**（用于后处理表面；但边界面上实际显示/使用精确面值）。
- **43.1.2 节点值（Node Values）**：显式定义或单元数据加权平均。两步计算：①全部节点初始化为周围单元值的**逆体积加权平均**；②边界节点被**边界面值简单平均**覆盖（该变量有显式边界节点值时——Table 43.2–43.21 中以 **bnv** 标注）。
  - **非网格节点的顶点值**：表面上的节点值由网格节点数据线性插值——zone surface 顶点与区节点一一对应（值相同）；非 zone surface（iso/plane 等）从被穿单元面上的网格节点插值；point/structural point surface 从所在单元全部网格节点插值。
- **43.1.3 面值（Facet Values）**：
  - **Zone surface 上的面值**：内部 facet 关联两单元（c0/c1）——取两单元值**算术平均**；**主变量**的边界 facet 值取边界条件设定值，**因变量**由邻单元值算出（要精确因变量边界值需自定义场函数以边界条件主变量显式表示，见 43.5）。
  - **后处理表面上的面值**：每 facet 关联一个单元——facet 值 = 该单元值（iso/plane/line/point/rake/quadric 等均如此）。

## 43.2 速度报告选项（pp. 4397–4399）

三种报告方式：
- **笛卡尔速度**：X/Y/Z Velocity——最常用。
- **柱坐标速度**（Axial/Radial/Tangential Velocity 等）：坐标系按工况——轴对称（转轴必为 x 轴：x 轴向、y 径向；swirl 时切向）；**2D 单单元区**：x 轴向、原点在 Fluid 对话框指定；**3D 单单元区**：转轴与原点在 Fluid 对话框；**多区**（MRF/mixing plane/sliding）：用 Reference Values 任务页 **Reference Zone** 所选"参考区"的 Fluid/Solid 对话框转轴。正向约定——径向离轴为正、轴向沿转轴矢量为正、切向按右手定则。可用分量：3D 全三个；2D 径向+切向；轴对称轴向+径向（+swirl 等价切向）。
- **相对速度**（Relative X/Y Velocity、Relative Radial Velocity 等）：基于移动参考系——MRF/mixing plane/滑移网格时用；单动系直接按动系报告；多系/混合面/滑移网格须在 Reference Values 的 Reference Zone 指定参考系（各单元区转轴在其 Fluid/Solid 对话框定义）。无动区时相对=绝对。**相对速度也用于计算滞止量（总压/总温）；Axial/Radial Coordinate 同样用上述柱坐标系定义**。

## 43.3 分类场变量表（pp. 4399–4435）

24 张类别表（Table 43.1–43.24，pp. 4403–4435；**Table 43.23/43.24 跨至 p. 4435 属批次 119 段**）：Expressions；Pressure and Density；Velocity；Temperature/Radiation/Solidification-Melting/Two-Temperature Model；Turbulence；Runtime DFT；Species/Reactions/Pdf/Premixed Combustion；NOx/Soot/Steady|Unsteady Statistics；Phases/DPM/Granular Pressure/Granular Temperature/Wall Film；Properties；Eulerian Wall Film；Sensitivities；Wall Fluxes/UDS/UDM；Cell Info and Mesh；Perforated Walls；Mesh（叶轮机专属变量）；Residuals；Derivatives；Potential；Lithium；Acoustics；Structure；Aeromechanics；Cell Registers。**模型专属变量另见各模型的后处理章节**。
- **限制代码（括注于每个变量后；照录）**：2d / 2da（2D 轴对称无旋或有旋）/ 2dasw / 3d / adj / adis（耗散稳定化伴随）/ adt（湍流伴随）/ adnn（神经网络湍流优化）/ adjtr（离线训练后）/ aen（能量伴随方程）/ ark（Aungier-Redlich-Kwong real gas）/ asfft（Acoustic Sources FFT）/ awe（声学波动方程）/ bcde（BCD+表达式有界性）/ bns（宽带噪声源）/ **bnv（边界处有节点值）** / cgq（poor mesh numerics 梯度质量判据）/ cmp（可压流）/ con（接触检测 marks 法）/ cpl（密度基）/ cr（存在 cell register）/ cv（仅单元值）/ cve（仅单元值且导出 CFF-Post）/ ddpm / des / dil（非全多组分扩散）/ dm（动网格）/ do（DO 辐射）/ dpm（耦合离散相）/ dpmean/dprms（DPM Mean/RMS Values）/ dtrm（DTRM 辐射）/ fwh（FW-H 声学）/ e（能量方程）/ echem（电化学反应）/ edc / emm（Eulerian 多相）/ ewf（EWF）/ ewt（增强壁面处理）/ fv（面值可用）/ fm（frame motion）/ gap（gap 模型）/ gran（颗粒相）/ h2o（混合物含水）/ hn（悬挂节点自适应）/ id（理想气密度）/ ke（k-ε 族）/ kklo（k-kl-ω）/ kw（k-ω 族）/ les / lwf（LWF）/ mc（Monte Carlo）/ mcv（mesh/check-verbosity 2–3）/ melt（熔化凝固）/ mix（Mixture 多相）/ mm（mesh motion）/ mp（多相）/ netm（非平衡热模型多孔区）/ nox / nv（显式节点值函数）/ nvs（显式节点值解）/ os（overset）/ p1（P-1 辐射）/ pdf（非预混）/ pmx（预混）/ ppmx（部分预混）/ r（Rosseland）/ rad（辐射换热）/ rc（有限速率反应）/ ret（retain-cell-residuals 开）/ rg（real gas）/ rsm（Reynolds 应力模型）等（其余代码在表中随用随注）。
- 表内容示例（Table 43.4 Temperature 类摘录）：Static Temperature (e, bnv, nv)、Total Temperature (e, nv)、Sensible/Total Enthalpy、Relative Total Temperature、Rothalpy (e, nv)、Fine Scale Temperature (edc)、Wall Temperature (fv, e, v)、Entropy、Total/Internal Energy、NLBF Averaged Temperature (emm)、Viscous Dissipation (e, vw) 等。Radiation 类按 r/p1/do/mc/dtrm 标注；Solidification 类 Liquid Fraction (melt)、Contact Resistivity 与 Pull Velocity 各分量（melt，轴向/径向/旋流按维度）；Two-Temperature Model 各量 (e, cpl)。
- 各类别完整逐变量清单为参考表——使用时直接查 Fluent 后处理下拉列表或 PDF 原表；本知识页记录结构与代码体系，不逐行复制（见证据与适用条件）。

## 43.3（续）表尾（p. 4435）

**Table 43.23 Aeromechanics**：Wall Work Density、Wall Power Density（strc 相关）；**Table 43.24 Cell Registers**：`<cell_register_name>`（cr）。**43.3 类别表至此全部结束。**

## 43.4 字母序场变量定义清单（前半 A–M，pp. 4435–4480）

对 Table 43.2–43.21 所列变量的逐条定义（按显示名排序；条目给出所属类别、语义与**单位量**——单位量与 Set Units 对话框 Quantities 列表一致）。**结构照录与代表性条目摘录**（完整清单为参考内容，使用时查 PDF 原文 pp. 4435–4518）：

- 通用/寄存器类：`<cell_register_name>`（cr）——register 内单元值 1（field variable register 显示场变量值）、其余 0（**显示须关 Node Values**）；`<dft-dataset-name>_<frequency>-ba-mag / -ta-mag / -ta-phase`（Runtime DFT——频带幅值（频带功率平方根）、单频幅值、单频相位（弧度 [-π,π]），见 41.13.6）。
- 几何/叶轮机坐标：Abs. Angular Coordinate、**Abs (C-H)/(H-C) Spanwise Coordinate**（机匣→轮毂 / 轮毂→机匣展向坐标，length）、**Abs Meridional Coordinate**（进出口流向子午坐标，length）、Abs Pitchwise Coordinate（周向坐标，angle）。
- 压力/密度：Absolute Pressure = 操作压力 + 表压（pressure）；Acentric Factor（ARK real gas + 组分输运的偏心因子）。
- 壁面/太阳通量：Absorbed Radiation Flux (Band-n)（半透明壁逐辐射带吸收热通量，heat-flux）；Absorbed Visible/IR Solar Flux（半透明壁或 porous jump 吸收的可见/红外太阳热通量）。
- 辐射：Absorption Coefficient——介质单位路径热辐射吸收属性（= 光子平均自由程倒数；多波段用发射率权重输出加权值；length-inverse）。
- 动网格/侵蚀：Accumulated Deformation（侵蚀耦合动网格的壁面累计位移，见 p. 2896）。
- DPM 统计：**Accum Parcels in Cell**（稳态追踪 = 上次统计重置后进入单元的轨迹累计数；瞬态 = 进入单元的 parcel 数、按颗粒在单元内驻留的流动时间步分数加权）与 **Accum Particles in Cell**（稳态 = 轨迹所代表颗粒数累加；瞬态 = 各 parcel 颗粒数、同样按时间步分数加权）（Steady|Unsteady DPM Statistics 类）。
- 湍流/声学/空气动力：Acoustic Power（声功率）等 A–M 段各条目（如 Density/Density All（多相全部相密度）、Effective Prandtl Number/Thermal Conductivity/Viscosity、Enthalpy 与 Enthalpy of species-n、Entropy、Gradient Quality Measure（poor mesh 判据，见 37.23.5）、Internal Energy、Laminar Flame Speed、Mach Number、Mass Flow Rate 等各按类别与单位量定义）。
- 本段尾部示例：**Dynamic Pressure**（Pressure 类）= ρv²/2 型动压，参考量（参考压力/密度/速度）取自 Reference Values 任务页；**Pressure Discontinuity Sensor**（Pressure 类）——单元是否邻近压力间断的二值标识（=1 间断邻近/否则 0；**只显示激波最强部分、常短于完整激波系**——High-Speed Numerics 相关，见 p. 3746）；**Pressure Hessian Indicator**（Derivatives 类）——压力分布 Hessian 近似的解误差指示（详见 39.2.1.2）。

（43.4 清单后半 M–Z 与 43.5 见批次 120。）

## 43.4（续）字母序清单后半（M–Z，pp. 4481–4519）

M–Z 段代表性条目（同前结构：类别+语义+单位量）：
- **Progress Variable / Progress Variable Variance**（Premixed Combustion）——燃烧产物归一化质量分数（Theory Guide Eq 8.109）及其方差（部分预混模型求解）。
- **PSD of dp/dt for Octave/1/3-Octave Band at x Hz、PSD of dp/dt for Const Width Band n**（Acoustics）——压力时间导数 dp/dt 的功率谱密度（标准技术倍频程/1/3 倍频程中心频率 x 或用户恒带宽 n 的积分值）；在 Acoustic Sources FFT 对话框计算（流程见 p. 2744；PSD 计算配方见 p. 4307；单个 dp/dt 谐波幅值 = 对应压力谐波幅值 × 2πf）。
- **Q Criterion Normalized / Q Criterion Raw**（Velocity）——湍流结构目视判据（Eqs 43.30–43.32：Ω 与 S 分别为涡量与应变率张量范数；Normalized 用 Reference Values 的参考长度/速度；TUI 名 q-criterion / raw-q-criterion）。
- **Radial Coordinate**（Mesh）——极坐标半径矢量的长度（转轴在 Fluid 对话框定义；length）。**Radial Pull Velocity**（熔凝）。**Radial Velocity / Radial-Wall Shear Stress**（摩擦切向力径向分量；pressure 量纲）。
- **Radiation…**：Radiation Heat Flux（控制面上辐射换热率——出域为负入域为正；heat-flux）；Radiation Intensity Normalized Std Deviation（球平均辐射强度标准差）；**Radiation Temperature** = (I/σ)^(1/4) 型式（Eq 43.33；I 为入射辐射；temperature）。
- **NOx/Soot 速率族**：Rate of NO（所有激活路径总 NO 生成率）、Rate of N2OPath/Prompt/Reburn/SNCR/Thermal/Fuel/USER NO（各路径单独，仅激活时可用）；Rate of Coagulation/Nucleation/Oxidation/Surface Growth/Soot/Nuclei/Soot Mass Nucleation（Soot 各过程速率）。
- **Rate of Reaction-n**（Reactions）——第 n 反应有效推进速率：finite-rate 模型 = Kinetic Rate；eddy-dissipation = Turbulent Rate；finite-rate/eddy-dissipation = 两者较小者；**颗粒反应 = 全局颗粒反应速率 kmol/s/m³**（由颗粒组分消耗率 Eq 7.102、分子量与单元体积换算）。
- **Reactor** 族（Species）：Reactor Net Mass Fraction of Species-n、Reactor Net Temperature、Reactor Net Zone ID（反应器网络）。
- **Reduced Temperature / Reduced Pressure**（Properties）——T/Tc 与 P/Pc（**仅 ARK real gas**）；Reflected Radiation Flux (Band-n) 与 Reflected Visible/IR Solar Flux（半透明壁反射；heat-flux）；Refractive Index（do/mc）。
- 其余 M–Z 条目（Mach Number、Mass Flow Rate 族、Mean/Mean Square Imbalance、Mesh 量、Mixture Fraction 族、NOx 浓度、Nusselt、Wall Fluxes 各量、Wall Shear Stress、Yplus/Ystar、Z Coordinate 等）同结构——按类别与单位量定义。

## 43.5 自定义场函数（pp. 4519–4524）

在求解器默认场变量基础上定义自己的场函数，用于等值线/矢量/XY 绘图等一切用变量的场合。**Custom Field Function Calculator 对话框**（Parameters & Customization → Custom Field Functions → New...）。
- **三条重要语义**：①**自定义场函数一律以 SI 单位求值与存储**——求解器变量自动转换，**常数必须自己用 SI 单位**；显式节点值不可用（节点值按邻单元平均算）。②**face 值量（表中 fv 标注）要用表达式（Fluent Expressions Language）而非场函数**——场函数不直接算面值，而是算单元值再插回表面（例如对称边界上热通量会给出非零错误值）。③**插值顺序差异**：场函数先把单元值插到节点再按定义计算；表达式按定义先算再把单元值插到节点——单元值陡梯度时两者结果可辨。
- **43.5.1 创建**：计算器按钮 + Field Functions 下拉（含求解器变量、已定义函数、**已建报告定义**）+ Select 组装 Definition（不可直接编辑；DEL 逐字符删；CE/C 全清）；**数值存储范围**照录（<1e-39 可能不准、<1e-45 结果为 0）→ New Function Name（**不得与标准场函数重名**——`display/contours` 可查预定义清单）→ **Define**（创建后加入可用场函数下拉；Manage... 打开定义管理）。计算器按钮注意：INV 先按再按 sin/cos/tan 得反三角；ABS/ln/log10（**≤0 的对数结果为 0**）；PI、e 按钮；含报告定义的函数**不能导出到文件**。
- **43.5.2 管理与保存/加载**：Field Function Definitions 对话框（右键 Custom Field Functions → Manage...，或计算器 Manage...）——查看定义（只读；改定义须删除重建）、Delete、Rename（禁重名）；**Save.../Load...** 在 case 间转移（自定义场函数文件为合法 **Scheme 函数**——也可经 File/Read/Scheme... 载入，见 p. 992）。
- **43.5.3 示例（三条照录语义）**：①静压/进口总压比（Eq 43.78——Static Pressure、进口 Gauge Total Pressure、Operating Pressure；Fluent 压力皆为相对操作压力的表压；操作压力为 0（可压计算常规）时化简为 Eq 43.79）；②**临界速度比** λ（叶轮机用，Eq 43.80）——λ 为临界速度比（同滞止条件、M=1 时的速度），γ 取 Properties 的 Specific Heat Ratio (gamma)、压力比用①所建函数（Field Functions 首下拉选 Custom Field Functions 再选该函数）；③旋流管道角动量流量（Eq 43.81）——定义 Radial Coordinate × Tangential Velocity 乘积函数，再用 Surface Integrals 对截面求积分。**重要**：含模型相关函数（如开能量方程后的温度）的场函数**仅在这些模型仍激活时才会计算**。

**Ch.43 全章完成（pp. 4395–4524）。**

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 4395–4434（批次 118，2026-10-20，pypdf layout 模式提取）。
- **证据边界**：Table 43.1–43.24 为参考性变量清单（数百行），按知识库"不复制大段原文"原则只记录结构、类别构成与限制代码体系；需要具体变量可用性时查 PDF 原表 pp. 4403–4435 或 Fluent 后处理下拉列表。
- Figures 43.1–43.2（节点值计算与柱坐标示意）为图形元素未摄取；限制代码清单照录（截取至本段所见部分）。
- 版本敏感：变量可用性与限制代码以 2026 R1 为准。
- 相关页面：[[Fluent 表面与单元寄存器]]（Facet/Vertex 赋值细节）、[[Fluent 数据报告]]（bnv 与 Boundary Values 对照）。
