---
type: concept
created: 2026-10-18
updated: 2026-10-18
tags:
  - Ansys Fluent
  - hypersonic
  - DBNS
  - two-temperature
  - rarefied
  - ablation
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 高超声速流动

## 摘要

User's Guide 2026 R1 Part III / Chapter 18 "Modeling Hypersonic Flow"（PDF pp. 2393–2426，共 10 节）讲高超声速流动建模。**本页全章完成（批次 65，pp. 2393–2426，覆盖 18.1–18.10）**：高超声速现象与 DBNS 定位、High Speed Numerics（HSN）、有限速率化学与非平衡离解（预定义混合物清单）、Gupta 曲线拟合输运性质、双温度模型、稀薄气体部分滑移与温度跳变、壁面部分催化边界条件、壁面烧蚀模型与最佳实践。

## 18.1–18.2 引言与 High Speed Numerics（pp. 2393–2395）

- **现象**（18.1）：**Mach 5 以上通常称高超声速**（无明确定义、文献略有差异）；典型应用：导弹、火箭、运载器、进入/再入舱体。强激波 + 波后大温升——**振动与电子激发内能模态被激活；更高 Mach（总焓更高）→ 气体离解直至电离**；化学反应该离解/复合/交换/电离；**流动时间尺度与内能弛豫/化学反应时间尺度同阶 → 局部热化学非平衡**；还有辐射、无线电黑障、低密度效应、壁催化、壁烧蚀——**多学科问题**。**DBNS（密度基求解器）特别适合高能高超声速**（连续-动量-能量强耦合；设置与理论见 p. 3739 与 Theory Guide）。
- **HSN**（18.2）：密度基内置定制数值设置——稳定并加速高超声速收敛。Solution Methods 任务页启用或 `solve/set/high-speed-numerics/enable? yes`。**默认 adaptive 模式：数值随捕获的激波强度按比例调整**——适合一般激波主导问题、多道不同强度且相互作用的激波。**expert 子菜单**（默认自适应不够时）：`solve/set/high-speed-numerics/expert` → 输 0–5 单数字按 Mach 分档：**0 = Mach < 0.7 Disabled（用常规默认）；1 = 0.7–1.4 Transonic；2 = 1.4–2.5 Low-Supersonic；3 = 2.5–4.5 High-Supersonic；4 = ≥ 4.5 Hypersonic；5 = Adaptive（默认，适用面最宽）**——1–4 档稳定化逐级增强、兼顾快收敛与精度。**与 Roe-FDS 和 AUSM 通量格式兼容；可与 CASM（拉伸网格收敛加速）联用**。瞬态可用，但**激波在移动（行波激波、跨声速振荡翼型）时常不需要；激波位置先变后稳时可用**。**Pressure Discontinuity Sensor** 场变量（Pressure... 类）经 `solve/set/high-speed-numerics/visualize-pressure-discontinuity-sensor? yes` 开启——二元标识（单元邻近压力不连续 = 1）；**只显示激波最强部分而非整个激波系**（激波常比显示的长）。**Note：HSN 不支持不可压流——密度必须启用理想气体定律**。

## 18.3–18.4 有限速率化学离解与 Gupta 曲线拟合（pp. 2396–2398）

- **化学非平衡**（18.3）：**Damkohler 数 Da = 特征流动时间 / 化学时间**——Da ≈ 0 化学冻结、Da ≫ 1 化学平衡、**高超声速 Da ≈ 1 → 局部化学非平衡**。激波层高温发生反应：**1 atm 空气：O₂ 2000 K 开始离解、4000 K 完成；N₂ 4000 K 开始、9000 K 完成；更高温电离生成离子与自由电子**。气体组成预测重要（强烈影响输运性质）。**用 Finite Rate Chemistry（p. 2451）；化学求解器选 Stiff 或 None-Direct Source——密度基推荐 None-Direct Source**（化学源项与组分质量方程强耦合）。前置：定义组分组与化学机理。**预定义混合物**：
  - **地球（T < 10,000 K）**：`air-2species-nitrogen`（N₂ + N，氮离解反应；纯氮实验）；`air-5species-park93`（N₂、O₂、NO、N、O；Park 93 机理 [115]）。
  - **地球（T > 10,000 K，弱电离）**：组中定义离子与自由电子 → Fluent 经**振动-电子能量变化**计及电离、并提供电离流输运性质方法（双温度 Theory Guide）：`air-11species-park93`（N₂、O₂、NO、N、O、N₂⁺、O₂⁺、NO⁺、N⁺、O⁺、e⁻；Park 93）；`air-11species-gupta`（同组分；Gupta 机理 [59]）。
  - **火星/金星**：`mars-5species-mckenzie`（CO、O₂、C、O、CO₂；Mckenzie）；`mars-8species-park`（+N₂、N、NO；Park）；**`mars-venus-16species-johnston`**（CO₂、CO、N₂、O₂、NO、C、N、O、CN、C₂、C⁺、O⁺、NO⁺、O₂⁺、CO⁺、e⁻；Johnston [75]——**需解析电离时用它**）。
  - **土卫六**：`titan-13species-gokcen`（CH₄、CH₃、CH₂、CH、C₂、H₂、CN、NH、HCN、N、C、H、N₂；Gokcen [55]）；**`titan-21species-gokcen`**（+Ar、N₂⁺、CN⁺、N⁺、C⁺、H⁺、Ar⁺、e⁻——**需解析电离时用它**）。
  - **默认属性方法**：单温度模型——**air 混合物默认 gupta-curve-fit、其余 kinetic-theory**；双温度模型——**全部混合物默认 blottner-curve-fit + eucken-relation**。
- **Gupta 曲线拟合**（18.4，[59]）：单温度默认方法；**适用温度至 30,000 K**。**Eq 18.1**（组分黏度与导热的对数线性拟合——静温 T 与组分相关系数 A–E；公式体未提取）；**离子与电子：系数在电子极限压力下取值；其他电子压力乘修正项（Eq 18.2**，p_e 为电子压力；公式体未提取）。**仅可用于四种 air 混合物**（其余缺数据）。导入后在材料中把组分 Viscosity / Thermal Conductivity 分别设为 **gupta-curve-fit-viscosity / gupta-curve-fit-conductivity**（图 18.1）；Edit... 查看系数（图 18.2）。

## 18.5 双温度模型（pp. 2399–2412）

- 模拟高超声速**热非平衡**——能量弛豫过程；比单温度模型对流场预测更好。**Note：需附加特性许可**（联系 Ansys 代表）。
- **使用步骤**（18.5.1）：①General 选 **Density-Based**；②**Energy 对话框同时开 Energy Equation 与 Two-Temperature Model**；③材料定义——启用后 Density/Cp/Thermal Conductivity/Viscosity 自动选中相应模型；**Cp 方法：nasa-9-piecewise-polynomial（默认，p. 1676）或 Boltzmann-kinetic-theory**；非数据库复制时：Viscosity → Edit... 填 **Blottner Curve Fit** 对话框（Theory Guide Blottner/Eucken/Constant Lewis）；**Characteristic Vibrational Temperature：单原子/双原子 → constant（给值）；三原子 → vibrational-modes（在 Multiple Vibrational Modes 对话框给每模态振动温度与简并度）**。Note：混合物流动建议先逐分子定义材料、再用组分输运建混合物（如空气 = 氮 + 氧材料）。④混合物：**Species Transport 模型**（导入合适混合物；**Reactions 选 Volumetric；Chemistry Solver：None-Direct Source（推荐）或 Stiff Chemistry Solver**）；Reactions 对话框可逐反应给 **Control Exponent**；混合物材料方法——**Thermal Conductivity 与 Viscosity：ideal-gas-mixing-law（默认）/ gupta-mixing-law；Mass Diffusivity：constant-lewis-number（默认，常数 1.4）/ gupta-mixing-law**；**gupta-mixing-law 的碰撞截面系数已为四种 air 混合物备好**（Change/Create 后经 cross-section-multicomponent 方法查看）。**Note：Stiff 求解器支持 Direct integration；Stiff 不支持 ISAT、Dynamic Mechanism Reduction、Chemistry Agglomeration；推荐 None-Direct Source**。⑤cell zone 的 Material Name 选该流体；⑥混合物在各边界 Species 页给分子分数；⑦边界条件：**边界上假设定域热力学平衡、温度在热页给**；⑧**Pressure Far-Field 与 Velocity Inlet：勾 Thermodynamic Non-Equilibrium Boundary 可给振动-电子温度 ≠ 平动-转动温度**；⑨双面耦合墙：**Coupled 热条件——墙内外两侧均假设定域热力学平衡**；⑩Solution Methods 的 **Two-Temperature Model** 下拉选空间离散格式；⑪Solution Controls 给 **Two Temperature Model 欠松弛因子**；可在 Equations 对话框取消勾 Two Temperature Model 暂停振动-电子能量方程；⑫残差监视器可基于 **vib-ele-energy** 判收敛；⑬后处理变量（**Two Temperature Model... 类**）：Translational-Rotational Temperature（Theory Guide Eq 5.23 的 T；= Temperature... 类的 Static Temperature）、Vibrational-Electronic Temperature（同式 T_v）、Internal Energy（平转 + 振电之和；= Temperature... 类的 Internal Energy）、Translational-Rotational Energy、Vibrational-Electronic Energy（均为 Theory Guide Eq 5.38 之和）、Translational-Rotational over Vibrational-Electronic Temperature（比值）、Vibrational-Electronic Conductivity / Specific Heat（混合物）、Mass-Averaged Relaxation Time（平动-振动弛豫时间质量平均）、Frozen Sound Speed（按平转热容比定义，公式符号未提取）、Dissociation Vibration Source（化学反应引起的振动-电子能量变化，Theory Guide Eq 5.28）。**Note：Temperature... 类的 Total Temperature 定义已调整——计入振动-电子能量贡献；假设定域热平衡、总温由总焓算出**。

## 18.6–18.7 稀薄气体：部分滑移与温度跳变（pp. 2412–2415）

- **部分滑移**（18.6）：稀薄区有限摩擦不足以让气体完全黏附壁面 → 出现切向速度分量；**Maxwell 模型 [98] Eq 18.3**（滑移速度由法向剪应力张量沿壁的切向投影给出；平均自由程 λ **Eq 18.4**；σ 为动量适应系数——公式体均未提取）。**适用性按 Knudsen 数 Kn = λ/L（Anderson [10] 三区分类）：< 0.01 连续区 → 无滑移壁；0.01–0.2 过渡区 → 部分滑移壁；> 0.2 自由分子区 → 连续介质假设失效**。**密度基自带 Knudsen 数计算器**——按特征长度与进口边界面积平均流动量算 Kn：`/define/boundary-conditions/knudsen-number-calculator`。启用：Wall 对话框 **Shear Condition 选 Partial Slip for Rarefied Gases**（图 18.19）+ 给 **Momentum Accommodation Coefficient**。**Note：仅密度基求解器、仅层流**。
- **温度跳变**（18.7）：稀薄区壁面处气体温度 ≠ 规定壁温——**Eq 18.5**（由热流向量与热适应系数给出；公式体未提取）。**选了部分滑移剪切条件后温度跳变边界条件自动启用**（动量页）；给 **Thermal Accommodation Coefficient**。双温度模型启用时振动-电子能量也加跳变边界条件（**Nompelis 等 [109] Eq 18.6**）——给 **Vibrational-electronic Accommodation Coefficient**。**Note：仅密度基 + 层流；随部分滑移自动启用；不支持壁厚与热生成；只适用于规定温度的墙——热流、耦合边界与共轭传热不适用**。

## 18.8 部分催化壁边界条件（pp. 2415–2419）

- 高超声速中原子复合通常在壁面占主导——扩散到壁的原子反射或复合成分子；**密度基提供部分催化边界条件（地球大气飞行 [105]）**。**Eq 18.7**（与 Boltzmann 常数、O/N 原子质量、扩散系数、壁温及 O/N 复合系数相关；公式体未提取）。**γ = 撞壁原子中复合的比例：0 = 非催化壁；1 = 完全催化壁；介于其间 = 部分催化**（图 18.21）。复合系数两法：**一般表面材料 → 常数值；热防护系统（TPS）→ 三种经验公式：Kolodziej [83]（Eq 18.8）、Zoby [179]（Eq 18.9）、Scott [141]（Eq 18.10）**（公式体未提取）。步骤：①前置：密度基 + Species Model 的 Mixture Material 为四种 air 混合物之一；②墙 **Species 页选 Partially Catalytic Wall**（图 18.23）；③选 **Recombination Coefficients For General Materials**（直接给 n 与 o 的复合系数）或 **Recombination Model for Thermal Protection System**（航天飞机 TPS 实验数据的温度相关系数；下拉 Kolodziej (Air) / Zoby (Air) / Scott (Air)）。

## 18.9 壁面烧蚀（pp. 2419–2422）

- 热防护：表面涂**烧蚀材料**——表面反应剥蚀带走大量热、保持表面低于熔点；烧蚀改变外形轮廓 → 对（超）高超声速气动影响显著。**Fluent 烧蚀模型同时考虑表面反应的热质传递与几何变化引起的动网格运动**。**Note：需附加特性许可；烧蚀模型仅用于瞬态仿真**。模型两选：
  - **Vielle 模型 [6]**：经验式算烧蚀后退率 ṡ (m/s)——**Eq 18.11**（绝对压力与用户参数 a、n；公式体未提取）；计及烧蚀对计算域的气动响应；可再计质量与热传递——按烧蚀材料密度 ρ_s 与组分质量分数 Y_i 经 **Eq 18.12** 算各组分注入质量流量 ṁᵢ（公式体未提取）。
  - **Surface Reaction 模型**：计及烧蚀面上的表面反应（质量+热传递）；后退率 **Eq 18.13**（由烧蚀材料密度 ρ_s 与表面刻蚀率 ṇ 给出——ṇ = Theory Guide Eq 7.83 表面沉积率的负值；公式体未提取）。
- 后退率用于确定网格运动速度。**步骤**：①启用 **Ablation Dynamic Mesh Coupling**（Setup → Models → Ablation → Edit——图 18.25 标题在手册中误印为 "The Perforated Walls Dialog Box"；启用后 Wall 对话框出现 Ablation 页）；②要计表面反应：Species Model 开 Species Transport + **Wall Surface**（Reactions 组框）；每个墙在 Species 页开 Reaction——**流固之间的烧蚀须在耦合墙的流体侧开**；③每个烧蚀墙在 **Ablation 页的 Ablation Model 下拉**（流固烧蚀同样在流体侧）选：**none（默认）** / **Vielle's model**（给 Parameter A 与 Parameter n；要质量热传递再开 **Species Flux** + Ablative Material Density + Species Mass Fraction） / **Surface Reaction**（给 Ablative Material Density；**仅当 Species Model 开了 Wall Surface 且墙 Species 页开了 Reaction 才可选**）。选任一模型点 Apply 后 **Fluent 自动：启用 Dynamic Mesh 模型；Mesh Methods 组开 Smoothing 与 Remeshing 并在 Mesh Method Settings 启用相关方法；建与墙同名的动网格区、Motion Attributes 的 Mesh Motion UDF/Profile 设为 ablation**。**Note：自动动网格设置未必适合具体工况**——如流固间运动墙上的烧蚀须给固体区建用 **RBF 光顺**的 deforming 区（p. 1894）。**建议：先跑定常、再开烧蚀模型、以收敛的定常解为瞬态起点**。

## 18.10 最佳实践（pp. 2422–2425）

- **气体属性设置**（18.10.1）按最高温度三档：**T_max < 1000 K → 单温度模型、忽略化学反应；air 材料 + nasa-9-piecewise-polynomial 比热 + kinetic-theory 黏度与导热**。**1000–10,000 K → 可能热化学非平衡：开双温度模型 + air-5species-park93 / mars-5species-mckenzie / mars-8species-park93 混合物 + 体积反应**。**> 10,000 K → 部分电离：双温度 + air-11species-park93 或 air-11species-gupta + 体积反应**。
- **求解器设置**（18.10.2）：**密度基 + 隐式格式；启用 HSN；非结构/扭曲/偏斜网格 → Green-Gauss Node-Based 梯度；含拉伸单元（边界层）→ e-CASM（p. 3743）；核查解限值（p. 3759）——默认最高温度对高超声速极端加热可能过低 → 解被削顶、残差停滞；反应流选 None-Direct Source 化学求解器（p. 2455）；收敛困难时：CFL 5 → 1；正性速率限值（p. 3761）0.2 → 0.1 或 0.05；开启 HOTR 高阶项欠松弛；先一阶格式、流动发展后切二阶（p. 3714）**。
- **初始化**（18.10.3）：**FMG 初始化（p. 3771）是高超声速一流的初场手段**——在 Standard Initialization（p. 3766）之后施加；改进初场使 Fluent 可直接以二阶格式起步。可调：**粗网格层数默认 5（< 10 万单元小案例 → 3 或 4）；CFL 默认 0.75（高超声速 → 0.5 或 0.25 增稳健性）；每层迭代数加倍/四倍补偿低 CFL；viscous FMG 选项（p. 3773）——发展边界层与等温壁换热效应；species-reaction FMG 选项（p. 3773）——空气离解/高速燃烧的有限速率反应；verbosity 监视 FMG 收敛**。**目视检查 FMG 初场：间断（虽被强抹平）应出现在预期位置、压力温度量程合理；FMG 发散 → 核查 Standard Initialization 初值 + 采用上述设置**。
- **监视与后处理**（18.10.4）：残差演化判收敛（p. 3834）——强间断、复杂物理、强耦合热化学使残差难以深而快收敛 → **增监视量：气动载荷（升阻力）；进出口质量通量平衡；等温壁总热流；域内压力/温度/Mach 最大值；双温度：振动-电子温度最大值；湍流：最大湍流黏度比；反应流：反应与生成组分的体积平均**。监视量应稳定到渐近定常态——振荡解须继续迭代。解的分析：**可视化压力场检查所有激波（沿壁与对称边界尤其、必要时加显示面）；检查波后量（温升、振电模态激发、新组分生成）；检查表面量（等温壁总热流、催化壁组分混合物）；湍流查壁法向 y⁺；灰黑 colormap 看 Schlieren 云图（必要时调量程；场函数定义 p. 4395）**。激波前沿应光滑规则、无明显欠冲/过冲；总热流云图不应有明显振荡。据此可改进网格（强梯度处聚集、兴趣区加密）——**网格自适应（p. 3975）尤其气动自适应（p. 3989）可自动化**。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.18；本页覆盖批次 65（pp. 2393–2426，18.1–18.10），2026-10-18 读取。**Ch.18 全章已摄取完毕**（p. 2426 为章尾空白页）。
- **公式体未提取**：Eq 18.1–18.13（Gupta 拟合与电子压修正、Maxwell 滑移、平均自由程、温度跳变、振电跳变、部分催化复合率与三个 TPS 经验式、Vielle 后退率、注入质量流量、Surface Reaction 后退率）公式体均为图形对象，仅按周边文字记录变量与语义，未杜撰形式；Frozen Sound Speed 的定义式符号未提取。Figures 18.1–18.25 为图形元素未摄取。
- **手册原文瑕疵一处**：p. 2420 图 18.25 标题印作 "The Perforated Walls Dialog Box"，正文实指 Ablation Dynamic Mesh Coupling Model 对话框——已如实记录。
- 本页数值（Mach 5 分界、空气离解温度 2000/4000/9000 K、Gupta 适用 30,000 K、Lewis 数默认 1.4、Kn 阈值 0.01/0.2、HSN 的 0–5 档 Mach 分档、FMG 默认层数 5 与 CFL 0.75 及高超声速建议、CFL 5→1、正性限值 0.2→0.1/0.05、γ = 0/1 语义等）为原文正文数值。
- **两项模型需附加特性许可**：双温度模型与烧蚀模型（联系 Ansys 代表）。部分滑移/温度跳变/部分催化/烧蚀/双温度均**仅密度基求解器**；部分滑移与温度跳变仅层流。
- 引用的参考文献编号（[6][10][55][59][75][83][98][105][109][115][141][179]）与跨章链接（密度基设置 p. 3739、CASM p. 3743、解限值 p. 3759、正性限值 p. 3761、一阶二阶 p. 3714、FMG p. 3771/3773、残差监视 p. 3834、RBF 光顺 p. 1894、NASA-9 p. 1676、有限速率化学 p. 2451/2455、场函数 p. 4395、自适应 p. 3975/3989）仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 湍流模型设置]]（密度基求解器、HOTR、Green-Gauss Node-Based 梯度）
- [[Fluent 物理属性]]（组分输运、NASA-9 多项式、kinetic-theory 输运性质）
- [[Fluent 滑移与动网格]]（烧蚀联动的动网格/光顺/重划）
- [[index]]
