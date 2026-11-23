---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags:
  - Ansys Fluent
  - pollutant
  - nox
  - soot
  - sncr
  - decoupled-detailed-chemistry
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 污染物生成模型

## 摘要

User's Guide 2026 R1 Part III / Chapter 23 "Modeling Pollutant Formation"（PDF pp. 2685–2724，共 3 节）讲污染物生成三模型。**本页全章完成（批次 74，pp. 2685–2724）**：23.1 NOx（解耦后处理流程、四路径——热力/快速/燃料/N2O 中间体、多燃料流与 N 源、UDF 速率、SNCR/Reburn 还原、湍流相互作用 PDF 模式）、23.2 Soot（一步/两步、Moss-Brookes 与 Hall 扩展、矩方法 MoM 含聚集模型、前驱物关联式）、23.3 Decoupled Detailed Chemistry（稳态流场 + 详细机理后处理慢生成痕量污染物）。

## 23.1 NOx 生成（pp. 2685–2702）

### 23.1.1.1 解耦分析概览与推荐流程（pp. 2685–2686）

- NOx 浓度一般很低——对流场、温度、主燃烧产物影响可忽略 → **NOx 模型最有效的用法是作为主燃烧计算的后处理器**。推荐八步：①照常算燃烧问题（**Important：预混燃烧模型与 NOx 模型不兼容**；**要用 SNCR → 必须先在主燃烧计算中把 NH3 或尿素 CO(NH2)2 作为流体物种加入并定义相应的 species 注入**）；②启用 NOx 模型（Setup → Models → Species → NOx → Edit）并设参数；③进出口定义 NO（及必要的 HCN/NH3/N2O）边界条件；④（仅稳态）Equations 对话框关掉除 NO（及 HCN/NH3/N2O）外全部变量；⑤（仅瞬态）Run Calculation 页选 **Postprocess Pollutants** 并调 Max Post Iterations/Time Step；⑥迭代至 NO（及所解组分）残差 < **1e-6**；⑦照常绘图/报告；⑧需要时另存 case & data。

### 23.1.1.2 启用路径（pp. 2686–2688）

- Formation 页 Pathways：**Thermal NOx / Prompt NOx / Fuel NOx / N2O Intermediate**（N2O 选项在启用前三者之一后才出现）。**Important：非预混燃烧模型下，Fuel NOx 仅当 DPM 也启用时可用**。平均 NO 生成速率直接由流场平均浓度与温度计算。

### 23.1.1.3 定义燃料流（pp. 2688–2690）

- 燃料 NOx 最多**三条燃料流**、每流可选**多个 N 源**。多流构型：固体+液体燃料同贡献；两三种不同含氮量/参数的固体燃料（煤混烧、煤-生物质混燃）；两三种液体燃料；气体 + 固体（或液滴）；**一种含 N 固体燃料 + 另一种不含 N 的反应固体颗粒**（如炉内喷钙、水泥窑煅烧）——指定活跃 N 燃料源即可、无需多流。
- 设置：Fuel Streams 组定 Number of Fuel Streams（≤3）；逐流（Fuel Stream ID 箭头切换）：Fuel tab 选 **Fuel Type**；Liquid 或 Solid → 从 **Fuel Sources** 清单选 N 源——Solid：燃烧颗粒材料（用于煤燃料 NOx 生成速率模型的 char 燃尽率与挥发分释放率；**不贡献 NOx 的材料务必取消选择**）；Liquid：液滴/多组分颗粒材料（决定液体燃料 NOx 模型的燃料释放率）；同时模拟 Prompt NOx → 从 Fuel Species 清单选燃料物种（**每流 ≤5 个、全部流合计 ≤10**；各流可分别定义 Fuel Carbon Number 与 Equivalence Ratio——在 Prompt 页改）；Gas → 从 Fuel Species 选材料（气相燃料 NOx 的平均极限反应速率；Prompt 沿用同一选择）。**Important：气相燃料选项仅在启用 species 模型时可用；读 14.5 及更早版本 case/data（多 injection 材料）→ 自动初始化各 injection 材料的燃料 N 源并在流动迭代开始时执行一次 DPM 迭代；读早于 14.5 的多燃料流 case → 须复查设置并重选 N 源**。

### 23.1.1.4 NOx 速率 UDF（pp. 2690–2691）

- Formation 页 User-Defined Functions 组从 **NOx Rate** 下拉挂编译 UDF；**UDF Rate 组**（各路径页如 Fuel tab）可选 **Add to Fluent Rate**（默认——UDF 速率加到标准速率）或 **Replace Fluent Rate**（替换）；**Tmax Option 选 user-defined** 可用 UDF 给温度 PDF 积分上限 Tmax 自定义值。

### 23.1.1.5 热力 NOx 参数（p. 2691）

- Thermal 页 [O] Model（及 [OH] Model）三法：**equilibrium / partial-equilibrium / instantaneous**（用预测的 O 和/或 OH 浓度）。**Important：尿素模型使用 [OH] 模型**。UDF Rate 同前。

### 23.1.1.6 快速 NOx 参数（p. 2691）

- 按 Theory Guide Eqs 9.26/9.28；逐流设 **Fuel Carbon Number**（每燃料分子碳原子数）与 **Equivalence Ratio**（**Eq 23.1**，公式体未提取）；UDF Rate 同前。

### 23.1.1.7 燃料 NOx 参数（pp. 2692–2694）

- Fuel 页逐流设置；Fuel Type 三选一（Solid/Liquid/Gas；**Gas 仅 Species Transport 启用时可选**）；UDF Rate 同前。
- **气相与液体燃料**：N Intermediate 选 **hcn / nh3 / hcn/nh3/no**；**Fuel N Mass Fraction**（kg N/kg 燃料）；**Conversion Fraction**（燃料 N 转化为中间体和/或产物 NO 的总质量分数；**默认 1**——剩余 N 假定转化为气相氮气、对气相氮总质量分数影响极小、无需解氮物种）；hcn/nh3/no → **Partition Fractions**（转化后的燃料 N 中变为 hcn 与 nh3 的分数，NO = 余量；**HCN 与 NH3 均设 0 = 全部燃料 N → NO；HCN 设 0、NH3 设 1 = 等价于直接选 nh3 中间体**）。气/液燃料预测用 Theory Guide Eqs 9.31/9.32（HCN）或 9.42/9.43（NH3）。**Important：定义多条液体燃料流有限制（见燃料流定义节）**。
- **固体（煤）燃料**：预测用 Theory Guide Eqs 9.55/9.56（HCN）或 9.62/9.63（NH3）。输入：N Intermediate；**Volatile N Mass Fraction**（挥发分含氮质量分数）+ 挥发分 Conversion Fraction（+ 分配分数）；**Char N Conversion** 下拉：**no / hcn / nh3 / hcn/nh3/no**（选 hcn 或 nh3 的前提是 N Intermediate 也选了同一物种）；**Char N Mass Fraction** + char Conversion Fraction（+ 分配分数）；**BET Surface Area**（颗粒 BET 内孔表面积，见 Theory Guide）。**Important：多条固体燃料流有限制**。挥发分与 char 含氮质量分数由 **Eqs 23.2–23.7** 确定（公式体未提取；变量：燃料氮释放率 kg/s、挥发分/char 释放率 kg/s、挥发分或 char 含氮分数、daf 煤总氮分数、char 氮占总氮分数、daf 煤挥发分/char 质量分数）。

### 23.1.1.8 N2O 路径参数（pp. 2694–2695）

- N2O Path 页，**N2O Model** 两法：**quasi-steady**（**Important：不解 N2O 输运方程，但每迭代更新 N2O——其残差恒为 0，迭代打印零属正常**）；**transported-simple**（N2O 加入污染物物种清单、经输运方程解质量分数）。原子 O 浓度按热力 NOx 的 [O] Model 计算；未选 Thermal 路径时可为 N2O 单独指定 [O] Model（同三选项）。UDF Rate 同前。

### 23.1.1.9 NOx Reburn（pp. 2695–2696）

- Reduction 页 Methods 勾 **Reburn** → Reburn 页：**instantaneous [CH]**（**Important：问题定义中必须包含 CH、CH2、CH3 物种**）或 **partial-equilibrium**（选 **Reburn Fuel Species 最多 6 个**；指定 **Equivalent Fuel Type**：ch4/ch3/ch2/ch——甲烷再燃燃料对应 ch4；煤挥发分组分如 hv_vol 须按挥发分组成查 **C/H 比** 选最接近的 CH/CH2/CH3/CH4 [92]）。

### 23.1.1.10 SNCR 参数（pp. 2696–2698）

- 前置：物种清单含 **nh3**（氨水还原）和/或 **co<nh2>2**（尿素还原）。Reduction 页勾 SNCR → SNCR 页：
  - **Injection Method = gaseous**：氨或尿素作为气相污染物物种从喷射位置加入（用于 NOx 后处理时须把该物种作为气相物种加入并设进口质量分数——**在主燃烧计算之前**）。
  - **Injection Method = liquid**：氨作为液相污染物物种；尿素以水溶液喷射时也选 liquid；**须启用 DPM 并把尿素或氨设为材料**。Note：**全部颗粒类型（液滴、燃烧、多组分）均与 SNCR 兼容**。后处理用须把 NH3 同时作为气相与液相物种、定义液滴氨颗粒喷射位置、设气相氨为蒸发物种（与主燃烧计算同时进行）。尿素为升华固体、通常以水溶液喷射 → 在 Create/Edit Materials 定义尿素固体属性；**假定水在尿素升华前蒸发完；升华过程按煤的单速率脱挥发模型模拟——用户供升华速率（s⁻¹）并在 injection 属性中指定含水量**。
  - **SNCR Reagent Species**：nh3 或 co<nh2>2。
  - **非预混 + 液相还原剂**：设 **Reagent Fraction in Stream**（还原剂流中还原剂质量分数；余为水）；PDF 启用二次流时**默认二次流即还原剂流**——改指主流用 `define/models/nox-parameters/nox-chemistry`（在 Injection Method 提示后的 PDF Stream ID 输 0）。
  - **尿素分解**（Reagent Species = co<nh2>2）：**rate-limiting decomposition**（默认；按 Theory Guide Table 9.3 两步尿素分解过程速率算源项）或 **user-specified NH3 Conversion**（假定尿素瞬间分解为氨与 HNCO 的给定比例；NH3 Conversion = 瞬间生成的 NH3+HNCO 混合物中 NH3 的摩尔分数；余量转 HNCO；此情形无尿素源项）。

### 23.1.1.11 湍流参数（pp. 2698–2700）

- Turbulence Interaction Mode 页 **PDF Mode**：**temperature**（只温度脉动）；**temperature/species**（温度 + 所选物种质量分数脉动，出现 Species 下拉）；**mixture fraction**（混合分数脉动；**仅非预混与部分预混**）。**Important：同时模拟多种污染物时，NOx 与 Soot 对话框的 PDF Mode 选择必须一致（一处选 mixture fraction 则处处选）**。mixture fraction 法：瞬时温度/浓度取自 PDF 查表（混合分数与焓的函数）；卷积所用 PDF 与平均流场计算相同（单混合分数 beta；双混合分数 beta 或 double delta）；**Note：选 mixture fraction 时 NOx 速率在第一次 NOx 迭代先验制表（控制台显示 Performing Pollutant PDF integrations...）**。
- temperature / temperature/species 下的参数：**PDF Type**——beta（Theory Guide Eq 9.108）或 gaussian（Eq 9.111）；**PDF Points**——beta/高斯函数直方积分点数（**默认 10 为最小值**——先以最小值算到收敛，再逐步增大（如 20–25）至目标污染物不再变化；增点提精度也增耗时）；**Temperature Variance**——**algebraic**（默认；Eq 9.114 近似式）或 **transported**（Eq 9.113；更准更贵）；**Tmax Option**——**global-tmax**（默认 = 流场最高温）/ **local-tmax**（局部单元平均温 × Tmax Factor）/ **specified-tmax**（给定 Tmax）/ **user-defined**（配 NOx Rate UDF）；**Species**（temperature/species 时出现——决定哪个物种质量分数进入 NOx 生成计算）。**Important：物种方差恒用代数式（Eq 9.114）**。

### 23.1.1.12 边界条件与求解策略、后处理（pp. 2700–2702）

- **边界条件**：进口设 **Pollutant NO Mass Fraction**（及必要的 Pollutant HCN/NH3/N2O Mass Fraction）；默认 0 或按系统给非零值。
- **求解策略**：①（可选）DPM 开启时把 **DPM Iteration Interval 设 0**（解 NOx 期间不做 DPM 迭代）；②Equations 关掉除 NO（及 HCN/NH3/N2O）外全部方程；③NO（等）欠松弛**建议 1.0**（不收敛则调低）；④残差收敛判据降为 **1e-6**；⑤迭代至 NO/HCN/NH3 浓度场不再演化。
- **后处理变量**（NOx... 类）：Mass/Mole fraction of Pollutant **no / hcn / nh3 / n2o / urea / hnco / nco**（hcn/nh3 限相应燃料 NOx 模型；n2o 限 N2O 中间体模型；urea/hnco/nco 限 SNCR 尿素喷射）；对应 Density；**Rate of no（各路径）** 与 Rate of hcn/nh3/n2o/urea/hnco/nco；**RMS of Temperature**（PDF Mode 选 temperature 或 temperature/species 时）；另有各路径（Thermal/Prompt/Fuel/N2O Path/SNCR）的 NO 速率可绘图。

## 23.2 Soot 生成（pp. 2702–2722）

### 概览与流程（p. 2703）

- **烟灰质量分数较大（如 10%）或涉及辐射效应时，须把烟灰作为主燃烧解的一部分计算（不像 NOx 那样后处理）**。流程：①照常设置（**限制：全部烟灰模型与预混燃烧不兼容；一步与两步模型仅湍流可用**）；②启用 Soot 模型（Setup → Models → Species → Soot → Edit）；③进口设 soot（及非一步模型的 nuclei）边界条件；④soot/nuclei 欠松弛**默认 0.9**（不收敛调低）；⑤迭代至 soot/nuclei 残差 < **1e-6**；**Note：启用 Soot-Radiation Interaction 时，烟灰方程（soot、nuclei 及 tar 物种）必须与燃烧解一起求解（不可作污染物后处理）；其他污染物仍可后处理**；⑥检查；⑦保存。

### 23.2.1.1 一步模型（pp. 2704–2705）

- Model 选 **One-Step**；Species Definition：**Fuel 与 Oxidant** 下拉（非预混混合燃料流选最合适物种作 Fuel；最主要氧化组分如 O2 作 Oxidant）；Options：**Soot-Radiation Interaction**；Process Parameters：**Stoichiometry for Soot Combustion**（Eq 9.120 质量化学计量；**默认 2.6667 = 纯碳 + O2**）、**Stoichiometry for Fuel Combustion**（**默认 3.6363 = 丙烷 + O2**）；Modeling Parameters（Eqs 9.117/9.119/9.120）：**Soot Formation Constant**（kg/(n·m·s)）、**Equivalence Ratio Exponent**、**Equivalence Ratio Minimum/Maximum**（**仅当 min < max 才解 Eq 9.117；当量比出界视为不生成烟灰**）、**Activation Temperature of Soot Formation Rate**、**Magnussen Constant for Soot Combustion**。默认值为丙烷燃料值 [33, 170]，对宽范围碳氢燃料有效。

### 23.2.1.2 两步模型（pp. 2706–2708）

- Model 选 **Two-Step**；**Important：两步 Tesner 模型只能配 eddy-dissipation 湍流-化学相互作用**。Species Definition、Soot-Radiation Interaction、两个化学计量同一步模型。Process Parameters 另有 **Mean Diameter of Soot Particle 与 Mean Density of Soot Particle**（算 Eq 9.123 烟灰颗粒质量；默认取自 [96]）。Modeling Parameters（Eqs 9.119/9.120/9.123/9.125/9.126）：**Limiting Nuclei Formation Rate**（低于此值不含分支-终止项）、**Nuclei Branching-Termination Coefficient**、**Nuclei Coefficient of Linear Termination on Soot**、**Pre-Exponential Constant of Nuclei Formation**、**Activation Temperature of Nuclei Formation Rate**、**Alpha/Beta for Soot Formation Rate**、**Magnussen Constant for Soot and Nuclei Combustion**。默认值 = Magnussen & Hjertager [96]（乙炔火焰）值、g0 取 Tesner [165] 原值；**丙烷燃料（非乙炔）建议某参数取 3.5e8** [5]（参数名在提取中缺失）；最佳结果须按具体系统经验值修改两参数。

### 23.2.1.3 Moss-Brookes 与 Moss-Brookes-Hall（pp. 2708–2716）

- Model 选 **Moss-Brookes** 或 **Moss-Brookes-Hall**。注：Moss-Brookes 原为甲烷火焰提出、经修改前驱物与表面生长物种可用于高碳氢；**MB-Hall 适用于高碳氢燃料（如煤油），且仅当 C2H2、C6H6、C6H5、H2 在气相物种清单中时可选**。
- **Species Definition**：**Precursor from = species-list**（清单中有合适前驱物时）→ 选 **Soot Precursor** 与 **Surface Growth** 物种；Moss-Brookes 可选 **c2h2 / c2h4 / c6h6**；都没有（eddy-dissipation 常见）或要用别的前驱物关联式 → 曲线拟合（见 user-correlation）。
- **Turbulence Interaction Mode**：PDF Mode——**none**（忽略湍流、层流烟灰速率）/ temperature / temperature/species / **mixture fraction**（非预混与部分预混；**推荐——结果与精度最好**）。**Important：与 NOx 对话框的 PDF Mode 选择必须一致**。mixture fraction 法瞬时量取自 PDF 表、卷积 PDF 同平均流场（beta / beta 或 double delta）；**Note：烟灰速率在第一次 soot 迭代先验制表（Performing Pollutant PDF integrations...）**。temperature 系参数与 NOx 相同（PDF Type beta/gaussian、PDF Points 默认 10 起步增至 20–25、Temperature Variance algebraic/transported、Tmax Option 四选、Species 代数方差恒定）。
- **Process Parameters**：**Mass of Incipient Soot Particles**（Eqs 9.131/9.133；**Brookes & Moss 取 144 kg/kmol（12 碳原子）；Hall 扩展取 1200 kg/kmol（100 碳原子）**）；**Mean Density of Soot Particle**（**B&M 1800 kg/m³ [29]；Hall 2000 kg/m³ [62]**）。
- **Soot Oxidation Model**：**Fenimore-Jones**（B&M 原用）或 **Lee extended**（在 Fenimore-Jones 的 OH 氧化之外**再加分子氧氧化**）。
- **Modeling Parameters**：**[OH] Model**（推荐 **instantaneous**——仅当 OH 在物种清单且由燃烧模型计算；**partial-equilibrium** 需要场内有 O 自由基浓度）；**[O] Model**（[OH] 选 partial-equilibrium 时必设：equilibrium / partial-equilibrium / instantaneous）。
- Soot-Radiation Interaction 同前。**Note：氧化速率缩放参数（Theory Guide Eq 9.131）在 Fluent 中恒为 1——用 `define/models/soot-parameters` 可改；调低会减少烟灰氧化**。
  - **23.2.1.3.1 烟灰氧化速率 UDF**：User Defined Oxidation Rate 下拉挂编译 UDF（DEFINE_SOOT_OXIDATION_RATE）。
  - **23.2.1.3.2 烟灰前驱物浓度 UDF**：Species Definition 组 User Defined Precursor 下拉（DEFINE_SOOT_PRECURSOR）。
  - **23.2.1.3.3 user-correlation 物种定义**：可接受前驱物 C2H2、C6H6、C2H4；清单中都没有时 **Precursor from = user-correlation（物种缺失时唯一选项）**——Fluent 由氧化剂质量分数与指定燃料物种贡献的 C/H 算混合分数，前驱物质量分数 = 该混合分数的用户定义函数。设置：①Fuel species + **Fuel Carbon Number 与 Fuel Hydrogen Number**（混合分数计算用）；②**Molecular Weight of Precursor**（默认乙炔值）；③**Precursor Correlation**：**piecewise-polynomial（默认）**——**Important：默认分段多项式仅对甲烷扩散火焰（空气与燃料初温均 290 K、乙炔为前驱物）有效**；自定义关联式应由层流火焰let剖面曲线拟合而来（剖面可用 Species Model 稳态火焰let或平衡化学生成，或第三方软件）；分段多项式把火焰let剖面按混合分数分段、每段前驱物质量分数按 **Eq 23.8** 的多项式（公式体未提取；系数个数 n、混合分数 f）；**Eq 23.9 为 Fluent 默认分段多项式（3 段；系数未提取）**；④piecewise-polynomial + Edit... → **Piecewise-Polynomial Profile 对话框**：**Ranges 最多 3 段**；每段 Minimum/Maximum 混合分数 + **Coefficients 个数（至多 8 个；1 个 = 0 阶常数、2 个 = 1 阶线性…）** + 系数值；**Important：段必须从最低混合分数起按序定义——求解器不会排序**；⑤**constant**：直接给常数。

### 23.2.1.4 矩方法（Method of Moments，pp. 2716–2721）

- Model 选 **Method of Moments**；**Number Of Moments**（矩输运方程数；**默认 3 适用面广，至多 6**）。
- **Soot Nucleation Model**：**Use Precursor**（默认；定义前驱物物种）或 **Specify Mechanism**（提供成核速率、把成核定义为前驱物间反应——有成核速率数据时更准）。
  - Use Precursor：Soot Precursor 清单（列出全部可用前驱物）选一个或多个——**必须是碳氢物种；Fluent 用动理学计算前驱物间聚并成核速率**；**Sticking Coefficients...** 逐前驱物设粘附系数——**动理学双前驱物碰撞算出的成核速率一般极大、会致数值误差**；**Important：粘附系数默认值按前驱物分子量计算；小前驱物可用更小值；指引见 Theory Guide Nucleation**。
  - Specify Mechanism：**Set Nucleation Mechanism...** → Mechanism 对话框：**Number of nucleation reactions**（单步或多步）；每反应设反应物物种 + 化学计量系数 + 速率指数 + **Arrhenius Rate 参数**（Pre-Exponential Factor、Activation Energy、Temperature Exponent）；**Note：只需输反应物——指定成核反应的主产物恒为烟灰核、其余产物不计入成核速率**。
- **Enable Aggregation Model**（烟灰聚集）：额外解同等数量的**颗粒矩输运方程**。参数：**Critical diameter**（聚并模式由共聚并切换为聚集聚并的烟灰粒径阈值）；**Fractal Dimension**（聚集分形结构参数；**1.7–2.0 对聚集聚并效果良好**）。**Note：聚集模型下 MoM 倾向高估烟灰产量**——部分因颗粒矩线性插值（改二次插值可克服），另因 **Fluent 目前忽略烟灰计算中乙炔的消耗**（乙炔在表面生长中被消耗而气相场冻结不知情 → 表面生长偏高 → 产率偏高）。
- **Soot Surface Growth Options**：**Soot Density**；表面生长与氧化按 **HACA 机理**（反应速率与步骧用默认值、无需用户输入——**唯烟灰位点密度除外**）；**Note：表面反应速率可用 `define/models/soot-parameters` 指定/编辑；Important：烟灰位点密度恒以每 cm² 位点数为单位（与 Fluent 单位制无关）**。
- **Process Parameters**：**Mean Density of Soot Particle** 与 **Normalization Parameter for Moments**——矩的绝对值可超 1e20，为减数值误差**解归一化烟灰矩：M_normalized = M_actual / Normalization Parameter**；默认值通常够用，矩值过高/过低时可调。
- **Modeling Parameters**：**[OH] Model**（instantaneous 尽可能推荐——仅当 OH 在物种清单且参与燃烧；partial-equilibrium 需场内有 [O]）；**[O] Model**（OH 未选 instantaneous 时可用：equilibrium / partial-equilibrium / instantaneous）。

### 23.2.1.5–23.2.1.6 烟灰边界条件与报告（pp. 2721–2722）

- **边界条件**：进口设 **Soot Mass Fraction** 与（非一步模型）**Nuclei mass concentration**；默认 0 或按系统给值。
- **报告量**（Soot... 类）：Mass/Mole fraction of Soot、Soot Density、Soot Volume fraction、Rate of Soot、Normalized Concentration of Nuclei 与 Rate of Nuclei（一步模型不可用）、**Rate of Soot Mass Nucleation / Surface Growth / Oxidation / Nucleation / Coagulation**（仅 MB 与 MB-Hall）、**Soot Surface Area / Soot Mean Diameter / Normalized soot moments**（仅 MoM）、**Normalized Soot Aggregation Moments / Average Number of Particles in Soot Aggregate / Primary Particle Diameter**（仅 MoM + 聚集）。

## 23.3 Decoupled Detailed Chemistry 模型（pp. 2722–2724）

- 用途：**在稳态流场上用详细化学动力学机理后处理慢生成痕量污染物**。流程：
  1. 用 Species Transport / 非预混 / 部分预混 / PDF Transport 算稳态燃烧问题；**建议先存 case & data（启用 DDC 后难以回到原设置）**。
  2. Setup → Models → Species → **Decoupled Detailed Chemistry → Edit** 启用（前提：已选非预混或部分预混模型；Species Transport 或 PDF Transport 则已启用反应）。
  3. **Import CHEMKIN Mechanism...** 导入详细机理（导入对话框同 20.1.1.3.2）；导入后对话框展开——**Original Species** 清单 = 初始机理（获得稳态解所用）的物种；**Pollutant Species** 清单 = 导入详细机理的物种；**两机理共有的物种只列在 Original Species、不可作污染物物种**。
  4. 选 **Pollutant Species** 点 **Apply**——污染物通常是慢生成（远离化学平衡）、质量分数极小；Fluent 创建 **pollutant-mixture** 材料并**启用 Species Transport + Stiff Chemistry Solver**；导入机理中非污染物、非原 combustion 模型物种**按单元温度用化学平衡计算**；除所选污染物外全部输运方程禁用。**Note：未识别为污染物且不参与污染物间反应的物种被剔除；导入机理中不含任何污染物物种的反应也被剔除**。
  5. **Integration Parameters...** 设 ISAT 参数——**ISAT Error Tolerance 建议 1e-5；Max. Storage 设为可用 RAM 的较大比例**（ISAT 详见 20.3.1）。
  6. 进口定义全部污染物边界条件（通常为 0）。
  7. 迭代至收敛；8. 照常后处理污染物质量分数；9. 需要时另存 case & data。

## 证据与适用条件

- 页码：pp. 2685–2724 全部覆盖（p. 2724 为章尾正文页），**Ch.23 全章完成**。
- **公式**：Eq 23.1（快速 NOx 当量比式）、23.2–23.7（挥发分/char 含氮分数确定）、23.8–23.9（前驱物分段多项式及默认式）公式体未提取，按周边文字记录结构、变量与语义；两步模型的某默认参数名（3.5e8）在提取中缺失。
- Figures 23.1–23.14（对话框截图）为图形元素未摄取；正文引用的 Theory Guide 式号（9.x 系列、8.45）与 Table 9.3 未展开。
- 默认值（Conversion Fraction 1、PDF Points 10、Crevice 无关、soot/nuclei 欠松弛 0.9、氧化缩放参数 1、B&M/Hall 起始烟灰质量 144/1200 kg/kmol 与密度 1800/2000 kg/m³、MoM 3 矩至多 6、分形维 1.7–2.0、DDC ISAT 1e-5、NOx 欠松弛 1.0 与残差 1e-6、燃料物种 5/流与 10 总、再燃燃料 6 种）为 2026 R1 手册记载，随版本可能变化。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]
- [[Part III - Solution Mode]]
- [[Fluent 组分输运与有限速率化学]]（CHEMKIN 导入与 ISAT、Coal Calculator 的 Fuel NOx 默认设置；Ch.20）
- [[Fluent 缩阶湍流燃烧模型]]（非预混/部分预混的 mixture fraction PDF 模式前提；Ch.21）
- [[Fluent 发动机点火模型]]（Knock/Ignition Delay；Ch.22）
- [[index]]
