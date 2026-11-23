---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags:
  - Ansys Fluent
  - non-premixed-combustion
  - premixed-combustion
  - partially-premixed
  - flamelet
  - mixture-fraction
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 缩阶湍流燃烧模型

## 摘要

User's Guide 2026 R1 Part III / Chapter 21 "Modelling of Turbulent Combustion With Reduced Order"（PDF pp. 2571–2670）讲三类缩阶湍流燃烧模型：21.1 非预混（混合分数/平衡化学/扩散火焰let）、21.2 预混、21.3 部分预混。**本页全章完成**：批次 70（2026-10-19）完成 pp. 2571–2625——21.1.1 使用步骤、21.1.2 平衡化学模型（绝热/非绝热、操作压力、二次流、经验燃料、RFL）、21.1.3 稳态/非稳态/柴油机非稳态火焰let（含内燃机推荐设置与火焰let重置）、21.1.4 流股组成（边界组分/凝聚相物种/经验输入/液体燃料/煤燃烧单双混合分数与 Coal Calculator）、21.1.5 控制参数（平衡物种排除/火焰let控制/慢化学置零）、21.1.6 火焰let计算与后处理、21.1.7 PDF 查表（AGR、全制表、稳定性、保存与后处理）、21.1.8 标准火焰let文件格式、21.1.9 Inert 模型（含 Inert EGR Reset）。批次 71（2026-10-19）完成 pp. 2626–2642——21.1.9.3 尾注、21.1.10 边界条件、21.1.11 物理属性（pdf-mixture）、21.1.12 求解策略（单/双混合分数、旧 case 启动、PDF 方程欠松弛）、21.1.13 PDF 表 Robust Numerics、21.1.14 后处理变量、21.2 预混燃烧全节（限制、C/G 方程、Zimont/Peters 火焰速度模型、初始化与后处理）。批次 72（2026-10-19）完成 pp. 2643–2670——21.3 部分预混全节（FGM 火焰let生成 premixed/diffusion/非绝热、FGM Scalar Transport、查表与 4D/5D 后处理、FGM 文件格式、火焰传播参数与方差方法、未燃属性多项式、拉伸层流火焰速度、内燃机多循环）。

## 21.1.1 使用步骤（pp. 2571–2576）

- **前置**：先启用湍流模型（Viscous Model）；非绝热还需 Energy ON（需要时加辐射模型）。
- **定义问题类型**（Species Model 对话框）：非预混/部分预混；化学描述四选——**Chemical Equilibrium / Steady Diffusion Flamelet / Unsteady Diffusion Flamelet / Diesel Unsteady Flamelet**；绝热/非绝热；二次流（**仅平衡模型**）；经验定义燃料（**仅平衡模型**）。
- **单混合分数流程六步**：①选化学描述；②绝热/非绝热；③（仅稳态火焰let）导入 flamelet 文件或 CHEMKIN 机理文件；④定义流股的化学边界组分（flamelet 导入时不适用）；⑤（仅稳态火焰let生成时）计算火焰let状态关系（组分质量分数/密度/温度 = 混合分数与标量耗散的函数）；⑥计算最终化学查表——**平均值 = Eq 8.17（或 8.25）与 8.19 的积分结果**，是平均混合分数、混合分数方差（及可能的平均焓与平均标量耗散）的函数。二次流（第二混合分数）问题：前两步同，再按 Theory Guide Eq 8.13/8.15 制瞬时属性表。

## 21.1.2 平衡化学模型（pp. 2576–2581）

- 平衡化学：组分浓度由混合分数 + 化学平衡假设确定；**含中间组分与离解反应 → 火焰温度比 Eddy-Dissipation 更真实**；可用 RFL 选项。启用：Species Model 选 Non-Premixed Combustion → Chemistry 页选 Chemical Equilibrium。
- **21.1.2.1 绝热/非绝热**：非绝热适用于——辐射或壁面换热；多个不同温度燃料进口；多个不同温度氧化剂进口；液体燃料/煤颗粒/向惰性颗粒传热。**绝热模型 = 二维查表**（标量只依赖平均混合分数与方差），不解能量方程、温度由混合分数与进出口温度直接定出；**非绝热 = 三维查表**、更耗时。
- **21.1.2.2 操作压力**：按理想气体定律算密度。非绝热可开 **Compressibility Effects**（PDF Options；适合压力时空变化大的场合；假设组分质量分数不随压力变化；**密度 Eq 21.1 = 操作压力下密度 ×（局部平均压力/操作压力）**；公式体未提取）；启用后 Species Model 的 Operating Pressure 名称改为 **Equilibrium Operating Pressure**（可与流动操作压力不同）；取值应接近系统绝对压力。
- **21.1.2.3 二次流**（Chemistry 页 Stream Options 勾 Secondary Stream）：需要二次流的情形——两种不同气体燃料；气体+液体混合燃料；气体+煤混合燃料；煤+液体燃料；**纯煤燃烧**（fuel 流 = char、secondary 流 = volatiles，比单混合分数更准）；单一燃料 + 两种不同氧化剂（oxidizer 流 + secondary 流）。**Important：二次流显著增加计算时间（多维 PDF 积分在运行时执行）——替代方案为全制表（Full Tabulation，p. 2614）**。有二次流时 PDF 表只存瞬时值，平均量运行时算。PDF 形状（Probability Density Function 下拉）：**double delta**（Theory Guide Eq 8.21）或 **beta**（Eq 8.22）。
- **21.1.2.4 经验燃料流**（Empirical Fuel Stream / Empirical Secondary Stream）：燃料组分未知时定义**元素分数而非物种**；每流输入**低位热值（Lower Caloric Value）、比热、分子量**。**Important：经验定义仅适用于完全平衡化学模型——不可与 RFL、稳态/非稳态扩散火焰let同用（需平衡计算确定燃料组成）**。**Important：经验流分子量仅在流经进口边界进入域或使用部分预混模型时需要；非预混 + 分散相来源流（煤/液体燃料）不需要**。
- **21.1.2.5 富燃可燃极限 RFL**（Rich Flammability Limit）：平衡模型下给混合分数设富限（Fuel Stream / Secondary Stream 分别指定；**经验定义燃料时不可用**）。超过富限：暂停平衡计算，按"与富限组成混合但不燃烧"计算组成；**RFL = 1.0 表示全混合分数范围做平衡**；RFL 模型对富混合物通常比平衡假设更准，且免去复平衡计算、加快查表制备；**取约两倍化学计量混合分数合适**。Secondary Stream：非燃料时 RFL 用 1；控制的是二次混合分数（非部分分数）。**Important：实验研究表明贫燃区近似热力学平衡、富燃区非平衡动力学主导——非经验定义燃料强烈建议启用 RFL** [21, 146]。

## 21.1.3 稳态与非稳态扩散火焰let模型（pp. 2581–2588）

- 启用：Species Model 选 Non-Premixed Combustion → Chemistry 页选 Steady/Unsteady Diffusion Flamelet。绝热/非绝热同 21.1.2.1；操作压力同前（Compressibility Effects 启用时改名 Equilibrium Operating Pressure）；**液体系统可用火焰let模型——PDF Options 勾 Liquid Micro-Mixing**。
- **21.1.3.3 机理文件**：自生成 flamelet 需读入 CHEMKIN 格式机理与热力学数据——Chemistry 页选 Create Flamelet + Import CHEMKIN Mechanism...；**生成 flamelet 只需气相机理 + 热力学数据库；导入机理上限 700 组分**。
- **21.1.3.4 导入 flamelet**：选 Import Flamelet；（仅稳态）File Type 选 **Standard 或 CFX-RIF** 格式；Import Flamelet File...（可单/多文件）；完成后直接跳 Table 页。
- **21.1.3.5 非稳态扩散火焰let**：**只能从已完全收敛的稳态稳态火焰let解启用**——把 case 转为非稳态、在冻结流场上后处理标记概率方程；出现 Import Flamelet File for Restart... 按钮（可从既有 case+data+非稳态 flamelet 文件续算）。Flamelet 页四个输入：**Number of Grid Points in Flamelet**；**Mixture Fraction Lower Limit for Initial Probability**（标记概率初场：高于此限为 1、低于为 0；**应大于化学计量混合分数**）；**Maximum Scalar Dissipation**（火焰let在高标量耗散下熄灭；2D/3D 模拟可能出现不现实的高 modeled 标量耗散传给 1D flamelet——用此上限限制 1D flamelet 内的瞬时标量耗散；**默认 30/s ≈ 标准温压甲烷-空气火焰的稳态熄灭标量耗散**）；**Courant Number**（标记概率方程时间步自动按此选取；默认 1 够用；判定准则 = 再小 Courant 数下非稳态火焰let平均质量分数不变）；**Number of Flamelets**（每个 flamelet 解一条标记概率方程，Theory Guide Eq 8.59）。点 **Initialize Unsteady Flamelet Probability**：初始化标记概率场、自动启用 Unsteady 求解器、禁用除 Unsteady Flamelet Probability 外全部方程、并设 Run Calculation 的 Time Step Size。**Important：不要再从树或 Solution Initialization 页初始化（做的是冻结流场上的概率场后处理，已经初始化过了）；关闭非稳态火焰let回到稳态求解时，须重新启用 Steady（General 页）并启用全部方程**。
- **21.1.3.6 柴油机非稳态层流火焰let**：**启用条件（压燃）**：Transient 求解器 + **In-Cylinder 动网格** + DPM Interaction with Continuous Phase。步骤：①Chemistry 页选 Diesel Unsteady Flamelet；②导入 CHEMKIN 机理（可含污染物生成反应）；③Boundary 页定义流股组成；④Flamelet 页——Number of Grid Points；Number of Unsteady Flamelets；（多 flamelet）经 **Set Flamelet Parameters** 打开 Unsteady Flamelet Parameters 对话框逐个设**起始时间（秒或曲轴角 CA）**——Fluent 从一个 flamelet 起算、到时自动引入新 flamelet；**Burnt Initial Flamelet** 选项（默认初态未燃；勾选后初态设为化学平衡已燃态——适用于缸内残余废气情形；**仅 case 初始化时使用**）；（可选）**Set Flamelet Fluid Zones**——flamelet 用 zone 平均压力与标量耗散逐步计算；默认全域平均，可选/取消流体 zone（**内燃机建议选缸内 zone、取消进出气 port zone**）；每时间步都重算 flamelet → **Calculate Flamelets 按钮变灰（不可预处理）**；⑤Table 页同理——PDF 表每时间步重算，Calculate PDF Table 变灰。
- **21.1.3.6.1 内燃机推荐设置**：①**至少两个 flamelet**——第一个模拟上一循环滞留已燃气体，第二个在喷油 CA 起动（Unsteady Flamelet Parameters 设）；**分段喷射（split injection）需三个及以上**；②初始化——实用中缸内总有滞留气，**建议勾 Burnt Initial Flamelet**（做定温平衡计算设已燃初态）；③**多循环**——每循环末必须重置 flamelet：定义 **Diesel Unsteady Flamelet Reset 事件**（通常在进气门打开前某曲轴角；用第一个已燃非稳态 flamelet 模拟 EGR 滞留气时推荐此法）；若用 Inert (EGR) 模型跟踪滞留惰性混合气，则定义 **Inert EGR Reset 事件**（进气门打开前 CA）。
- **21.1.3.7 重置柴油机非稳态火焰let**：两法——**Diesel Unsteady Flamelet Reset（推荐）**或 **Inert (EGR) 模型 + Inert EGR Reset**；经 Dynamic Mesh Events 对话框设置（曲轴角 + 参与流体 zone——通常只燃烧室、不含进出气 port）。**Reset 事件执行：删除全部 flamelet、引入一个状态 = 重置前全部 flamelet 概率加权平均的新 flamelet**；新循环中其余 flamelet 同前引入。**Inert EGR Reset：把所选 zone 内已燃气转为惰性、删除全部 flamelet、引入一个未燃 flamelet**。Note：Reset 选项仅在 flamelet 数 > 1 时可用。

## 21.1.4 流股组成定义（pp. 2587–2598）

- 只需指定**边界组分**（燃料、氧化剂、必要时二次流）的组成；中间与产物组分自动确定。默认边界组分清单：**ch4、h2、jet-a<g>、n2、o2**；组分名须与化学数据库格式一致（否则报错）。逐流股输入摩尔或质量分数及**进口温度**（查表与平衡计算需要）。平衡模型在 Boundary 页输组分名；**生成稳态/非稳态火焰let时边界组分清单自动 = CHEMKIN 机理全部组分、不可修改**。输入步骤：①（仅平衡）Boundary Species 输化学式 Add/Remove（List Available Species 打印 thermo.db 全部组分）；②（非平衡模型）按概览选边界组分；③Specify Species In 选 Mass Fraction（默认）或 Mole Fraction；④逐流股（Fuel/Oxid/Second）填分数——**质量↔摩尔切换时仅当各流分数和为 0 或 1 才自动换算，否则报错**；⑤Temperature：Fuel/Oxid/Second——绝热时决定所用进口温度；非绝热时**应与将设的进口热边界条件一致**（之后在 Fluent 里再设一次）；**液体燃料/煤：燃料进口温度 = 蒸发/脱挥开始温度（DPM 材料的 Vaporization Temperature）**，非绝热时仅用于调查表网格（离散焓值）；**多个不同温度燃料进口必须非绝热**，燃料温度取主导进口值。
- **21.1.4.1 边界流股组分建议**：煤的 char 用 **C(s)** 表示（**Important：区分原子碳 C 与固体碳 C(s)——原子碳仅用于经验输入法**）；经验已知成分（如 C0.9H3O0.2）用经验流选项；**硫会妨碍平衡求解器收敛（浓度小时尤甚）——只在含量可观时才纳入**。
- **21.1.4.1.1 凝聚相物种**：液/固物种可入化学计算（物种名后缀 (l)/(s)）；密度取自 **propdb.scm**（用随附 thermo.db 时）；自定义热力学库且 propdb.scm 无该物种 → **假定 1000 kg/m³**；PDF 表算完后可在 Create/Edit Materials 改凝聚相密度——改后**须重算 PDF 表**。
- **21.1.4.2 修改数据库**：缺组分可加进 **thermo.db**（格式 [81]；改标准库前先备份副本）。
- **21.1.4.3 经验流组成输入**：输 C、H、O、N、S 的**原子质量或摩尔分数** + 低位热值 + 平均比热（生成热由热值与原子组成算出；燃料进口温度与比热用于算显焓；分子量用于未燃流密度——仅进口边界或部分预混需要）。Boundary 页中该流股的物种分数输入框变灰，只剩原子分数（c、h、o、n、s）。
- **21.1.4.4 液体燃料燃烧**：DPM + 非预混联用——**燃料蒸气 = fuel 流**；液滴蒸发成为平均燃料混合分数的源；氧化剂进口混合分数 = 0；液滴按常规 DPM injection 定义（属性不受非预混模型影响）；**被要求指定蒸发气的气相物种（Evaporating Species）时选燃料混合物中最大组分**——该物种仅用于计算蒸发速率的扩散控制驱动力。
- **21.1.4.5 煤燃烧**：三种方案——①**双混合分数**（fuel 流 = char【一般 100% C(s)】、secondary 流 = volatiles）：**更准（挥发与 char 分开模拟），但运行时多维 PDF 积分开销显著**；②**单混合分数**（fuel 流含挥发物 + char C(s)）：**较不准，但收敛明显更快**；③煤 + 另一燃料（气/液）不同组成：煤用一个混合分数、另一燃料用第二个。
- **21.1.4.5.1 单混合分数煤组成**：**常规法**——Boundary 页列近似的物种清单（如 C3H8、CH4、CO、CO2、C(s)）与分数；手册示例：DAF 40% 挥发物（等摩尔 C3H8+CO）+ 60% char → C3H8=0.2、CO=0.2、C(s)=0.6；**煤组成一律按无灰基（DAF）定义**（即使计算中考虑灰）；灰属性经 Create/Edit Materials 选 combusting-particle 材料定义；工业分析 → 物种分数换算表示例（Volatiles 30%→C3H8 摩尔分数 0.07134 + CO 0.07134；Fixed Carbon 60%→C(s) 0.85732；Ash 10% 不入）；**水分**可作液态水 H2O(l) 或水蒸气 H2O 加入燃料组成（后者须在 DPM 材料里含对应潜热）；液态水作边界组分时要把它从排除物种清单移除（见 21.1.5.1）；**Important：煤里的水不走蒸发模型（与湿燃烧模型不同）**。**经验法**——Chemistry 页勾 Empirical Fuel Stream，输煤的低位热值与平均比热，Boundary 页输 C/H/N/S/O 原子分数（适合有元素分析时）。
- **21.1.4.5.2 双混合分数煤组成**：常规法——secondary 流定义挥发物种分数、fuel 流一般 100% C(s)；经验法——Chemistry 页勾 **Empirical Secondary Stream**（挥发流），输挥发分低位热值与平均比热 + 原子分数；手册示例表：DAF 挥发 30.4%/char 69.6%，元素 C 89.3/H 5.0/O 3.4/N 1.5/S 0.8（模拟时把 S 并入 N）→ 挥发流原子分数 C 0.24、H 0.70、O 0.03、N 0.03；**挥发分热值由煤与 char（DAF）热值推出（Eq 21.2/21.3，公式体未提取）**。
- **21.1.4.5.3 Fluent 内附加煤输入**：Set Injection Properties——**Oxidizing Species** 选氧化剂流的一个组分（char 燃尽律扩散驱动力用；默认 O2）；单混合分数：挥发+char 燃烧气相物种都由该混合分数表示；双混合分数：不指定 destination species，改指定 **Devolatilizing Stream（secondary）与 Char Stream（primary）**；煤+另一燃料：煤流同时作为 Devolatilizing 与 Char Stream。Create/Edit Materials——**Vaporization Temperature = 燃料进口温度**（控制脱挥开始；Boundary 页燃料温度 = 期望脱挥起始温度，保证查表覆盖温度范围）；**Volatile Component Fraction 与 Combustible Fraction** 与流股组成一致；**Burnout Stoichiometric Ratio**（每 kg char 需氧化剂量；默认 2.67 = C + O2 → CO2 假设；仅影响扩散控制燃尽速率）；**Latent Heat**（生成非预混化学定义的气相挥发物所需热量；非预混下挥发物种已基于煤总热值 → **通常设 0**；煤含水时：水定义为 H2O(L) → 潜热设 0（化学里已含汽化潜热）；定义为水蒸气 H2O → 潜热设水值 **2.25e6 J/kg × 挥发物中水质量载荷**）；**Density = 表观密度（含灰）**；char 燃烧**不需要**输 Heat of Reaction for Burnout。
- **21.1.4.5.4 煤后处理**：**DPM Evaporation/Devolatilization** = 挥发分释放速率；**DPM Burnout** = char 燃尽速率。
- **21.1.4.5.5 Coal Calculator（非预混版）**：输入同 Ch.20 版（proximate、ultimate）外加：**Secondary Stream 选项**（启用双混合分数——primary = char C(s)、经验 secondary = 挥发分）、Coal Particle Material Name（默认 coal-particle）、As-Received HCV、High Temperature Volatile Yield、Fraction of N in Char (DAF)。**OK 后自动**：设 Boundary 页经验燃料原子分数；**启用 Non-Adiabatic 模型（DPM 所需）**；经验燃料低位热值计算——DAF LCV 按式 **21.4**（由收到基 HCV 扣水分与灰调整；含水的氢分数、水与氢原子分子量、水潜热；公式体未提取）；二次流时挥发分 LCV 按式 **21.5**（由煤 LCV 与固定碳/挥发分分数；公式体未提取）；创建燃烧颗粒材料（Volatile Component Fraction + Combustible Fraction）并启用 DPM；Fuel NOx 参数设为煤流值（char N → NO；**模型本身不启用**）。随后**须在 Table 页点 Calculate PDF Table**；建 injections；收敛后可启用 NOx 模型做事后处理。

## 21.1.5 控制参数（pp. 2598–2601）

- **21.1.5.1 平衡物种的强制排除/纳入**：平衡计算自动包含全部中间/产物物种——但 **NOx 反应速率慢、不应按平衡处理**（浓度低、对密度/温度/其他组分影响小）→ 从平衡计算排除，用 NOx 后处理器（p. 2685）预测。Control 页 Species Excluded From Equilibrium：Add/Remove。反向——**强制纳入低浓度组分**（如 NOx 计算所需的 CH、CH2、CH3）：TUI `define/models/species/non-premixed-combustion` → Force Equilibrium Species to Include... 输双引号化学式（如 "ch","ch2"）；**须先设好燃料与氧化剂**。
- **21.1.5.2 火焰let控制**（稳态扩散火焰let，Control 页）：**Initial Fourier Number**——flamelet 方程（Theory Guide Eqs 8.49/8.50）首个时间步 = 显式稳定性限制的扩散时间步 × 该值（第一步内发散则调低）；**Fourier Number Multiplier**——后续每步乘子（第一步后发散则调低）；数值积分局部误差控制为 **Eq 21.6**（Relative/Absolute Error Tolerance 可指定；公式体未提取）；**收敛判据**——任一离散混合分数点上组分分数或温度的最大绝对变化 < **Flamelet Convergence Tolerance**；若振荡不收敛，超过 **Maximum Integration Time** 后停止。
- **21.1.5.3 初始非稳态火焰let的慢化学物种置零**（Eulerian 非稳态层流火焰let）：火焰let场初始化为燃烧中的稳态火焰let解以模拟点火；**慢生成物种按稳态剖面假设不准——应识别并置零**（Control 页）。默认置零清单：**NO、NO2、N2O、N、NH、NH2、NH3、NNH、HCN、HNO、CN、H2CN、HCNN、HCNO、HOCN、HNCO、HCO**，以及液态水 H2<l> 与固体碳 C<s>。

## 21.1.6 火焰let计算与后处理（pp. 2601–2609）

- **21.1.6.1 稳态扩散火焰let**（Flamelet 页参数）：**Number of Grid Points in Flamelet**（氧化剂与燃料间混合分数网格点数；flamelet 组分与温度在 Z 空间耦合隐式求解——时间/内存随点数大增）；**Maximum Number of Flamelets**（提前熄灭则实际数更少）；**Initial Scalar Dissipation**（首个 flamelet 的标量耗散，Theory Guide Eq 8.55 的 χst）；**Scalar Dissipation Multiplier**（ successive flamelet 的比值步进，用于 χ < 1）；**Scalar Dissipation Step**（χ ≥ 1 的间隔 s⁻¹）——手册示例：初值 1e-3、乘子 10、步长 5 → 生成 1e-3、1e-2、0.1、1.0、6、11、16…；**User Defined Flamelet Parameters**——挂 UDF 定制标量耗散与平均混合分数（或进度变量）网格离散；**Automated Grid Refinement（AGR）**——自适应插点：相邻点**值变化与斜率变化**都小于容差；参数 Initial/Maximum Number of Grid Points（默认值未提取）与 Maximum Change in Value/Slope Ratio（Theory Guide Eqs 8.28/8.29）。点 **Calculate Flamelets** 计算（控制台输出时间-温度-残差历程）。
- **21.1.6.2 非稳态扩散火焰let**：参数同 21.1.3.5（网格点数、混合分数下限、Maximum Scalar Dissipation 默认 30/s、Courant 数、flamelet 数）；点 Initialize Unsteady Flamelet Probability。
- **21.1.6.3 保存 flamelet 数据**：**File → Write → Flamelet...**（建 PDF 表**之前**保存；用途：改 PDF 表离散点数、绘图）。
- **21.1.6.4 flamelet 后处理**：Display Flamelets... / Display Unsteady Flamelet...；单 flamelet（如非稳态）→ **Flamelet 2D Curves** 对话框；多 flamelet → **Flamelet 3D Surfaces** 对话框：Plot Variable 选量；Plot Type = 3D Surface（可 Draw Numbers Box）或 2D Curve on 3D Surface（Write To File；X-Axis Function 选 Scalar Dissipation 或 Mixture Fraction——未选者恒定，按 Index 或 Value 切片）。

## 21.1.7 PDF 查表（pp. 2609–2619）

- Table 页参数。**AGR 启用时**：Initial/Maximum Number of Grid Points（平均混合分数、方差、平均焓的分辨率）、Maximum Change in Value/Slope Ratio（Theory Guide Eqs 8.28/8.29）、Maximum Number of Species。**Note：AGR 不可用于双混合分数**。**禁用时**：**Number of Mean Mixture Fraction Points**（平均混合分数离散点数；**自动在化学计量混合分数附近聚类**；双混合分数下为 beta PDF 的瞬时状态剖面点数）；**Number of Mixture Fraction Variance Points**（方差向变化慢、低分辨率即可；**无二次流时可用**）；**Number of Secondary Mixture Fraction Points**（有二次流时）；**Maximum Number of Species**（**上限 200**；自动选摩尔分数最大的物种入 PDF 表；**密度与比热用全部物种预算——收敛行为不受此输入影响；为控表体积只放需后处理的物种**）；**Number of Mean Enthalpy Points**（非绝热；高放热系统需更多点；**非稳态火焰let不可用**）；**Minimum Temperature**（非绝热；应低于域内最低温 **10–20 K**；非稳态火焰let不可用）；**Include Equilibrium Flamelet**（生成 χ=0 平衡 flamelet 附到库；单 flamelet 时 PDF 表 = 平衡切片 + flamelet 切片两片；**仅稳态扩散火焰let**）。点 **Calculate PDF Table**（样例输出：绝热双流 1271 点 22 组分；非绝热 strained flamelet 16810 点 17 组分）。
- **Important（单 vs 双混合分数运行时差异）**：单混合分数——PDF 表存平均值（密度/温度/比热），平衡非绝热时为三维（平均混合分数、方差、平均热损失），**每流动迭代更新属性**；双混合分数——**只存瞬时状态关系，每单元每步做 PDF 积分**，计算昂贵 → 可设为每 N 次迭代更新一次属性；或用全制表（21.1.7.1）。
- **21.1.7.1 双混合分数模型全制表**：默认 = 运行时 PDF 积分多维；可选**预计算成 4D（绝热）/5D（非绝热）表**——构建昂贵、内存/磁盘大，但运行时显著提速。TUI：`define/models/species/full-tabulation?`。**与污染物模拟的 mixture-fraction PDF Mode（Turbulence Interaction Mode）不兼容**。
- **21.1.7.2 平衡查表稳定性**：复杂化学 + 非绝热困难时**先做绝热计算**找合适输入；**经验法定义的固体/重液体燃料在富燃区可能算出极低温度并失败**（强吸热反应）→ **上调燃料热值直到可接受**，同时把期望热值与调整值之差定义为 latent heat（燃固体燃料）或 heat of pyrolysis（液体燃料），保持模拟中热值不变。
- **21.1.7.3 保存查表**：**File → Write → PDF...**（ASCII 默认；可 Write Binary Files）。
- **21.1.7.4 查表后处理**：**务必查看温度与组分表的分辨率——不足失准、过度拖慢计算**。PDF Table 对话框：Table 页 Display PDF Table... 或 **Postprocessing → Model Specific → PDF Table...**；Plot Variable：temperature/density/species mole fraction；多 flamelet 时可变 Scalar Dissipation 值（非绝热另有平均焓——表呈第四维）；Plot Type 3D Surface / 2D Curve on 3D Surface；非绝热 Surface Parameters 的 Constant Value of：单混合分数可选 **Scaled Heat Loss/Gain、Mean Mixture Fraction、Scaled Variance**（**方差按 Eq 21.7 归一化——缩放方差范围 0–0.25**；公式体未提取）；双混合分数只有 Scaled Heat Loss/Gain；Slice by Index/Value（绝热切片序号显示在 Adiabatic 栏）；2D 曲线的 X-Axis Function 按模型选（双混合分数：Fuel Mixture Fraction 或 Secondary Partial Fraction）。

## 21.1.8 标准火焰let文件（pp. 2619–2621）

- 关键字驱动格式（**大小写不敏感**；关键字不匹配须手工编辑）。支持关键字表：**HEADER**（头段）、**BODY**（主体段）、**NUMOFSPECIES**（组分数）、**GRIDPOINTS**（网格点数）、**PRESSURE**（压力）、**STRAINRATE**（物理空间生成的扩散火焰let应变率，如 CHEMKIN 生成时写出）、**STOICH_SCADIS 或 CHI**（化学计量标量耗散）、**STOICH_Z**（化学计量混合分数）、**TEMPERATURE 和 TEMP**（温度）、**MASSFRACTION-**（质量分数）、**Z**（混合分数）、**MOLEFRACTION-**（摩尔分数）。样例文件给出 Z/TEMPERATURE/massfraction-h/massfraction-o2 等段（50 网格点、60 组分示例）。
- **21.1.8.2 缺失物种**：flamelet 文件组分逐一对 thermo.db 核验——缺则报错中止导入；**加进数据库或从文件删除该物种**；**仅当该物种浓度在全剖面 ≤ 1e-3 时才可删**（删后 Fluent 中看不到其浓度、其余精度不受影响）；**删除后须同步更新 NUMOFSPECIES**；高浓度物种缺失必须补进数据库、不建议删除。

## 21.1.9 Inert 模型（pp. 2621–2625）

- **前提**：已选非预混或部分预混模型（或已读 PDF 文件）；Setup → Models → Inert → Edit；勾 **Inert Transport**。
- **组成选项**：①**Fixed H/C Ratio**——氢碳比已知时（如 CH4 输 4）；假定已燃气 = 该碳氢燃料完全化学计量燃烧产物 **CO2 + H2O + N2**；②**User Specified**——任意组成：Inert Species 加物种、输质量分数（和为 1；**Normalize Species** 按钮归一）、Remove 删、List Available Species 打印 thermo.db。
- **21.1.9.1 边界条件**：进出口设惰性示踪质量分数——进口对话框 Species 页 **Inert Stream** 字段；**0–1，1 = 全部进入域的物质来自惰性流**。
- **21.1.9.2 初始化**：模型核心假设 = **惰性流组成不随燃烧变化**——对某些稀释剂合理，**富燃燃烧（排气含燃料）不成立**；排气含燃料/氧化剂时初值设置须计及。**21.1.9.2.1 惰性分数**：Solution Initialization 页输值或 **patch**（patch 后自动按当前温度场重算焓场以反映组成变化）。**21.1.9.2.2 惰性组成**：碳氢燃料可按 H/C 比直接算——总氧化反应（Heywood [65]）**Eqs 21.8/21.9** 改写为 H/C 原子比函数，**Eq 21.10** 给出 CO2/H2O/N2 质量分数关系（公式体未提取）。
- **21.1.9.3 Inert EGR Reset**：把已燃气转为惰性——面向**部分预混 + EGR 的内燃机多循环模拟**：燃烧冲程末已燃气 progress variable = 1，与新鲜充量（c = 0）混合会立即点火，除非把滞留已燃气转为惰性。经 **Dynamic Mesh Events** 对话框设置（曲轴角——通常进气门打开前；zone——通常燃烧室）。**执行逻辑**：惰性组成 = **化学计量组成**；贫燃：化学计量惰性气与氧化剂混合；富燃：与燃料混合——**总当量比守恒**。具体：①计算化学计量混合分数（燃料与氧化剂恰好耗尽的混合分数）；②惰性物种质量分数 = 化学计量物种质量分数（**摩尔分数 < 0.01 的物种丢弃**）；③按贫/富公式设惰性质量分数与混合分数（公式体未提取；符号：惰性质量分数、混合分数、反应进度；下标 sto = 化学计量、old = 重置前；波浪号 = Favre 平均）；④**反应进度置零**；G-Equation 模型：G（距火焰前沿平均距离）设为负值。

- **21.1.9.3 尾注（p. 2626）**：EGR 重置前后组分质量分数的小误差会经比热变化改变温度——**默认 Fluent 调整焓使 EGR 重置后温度不变**；若受新混合分数的 PDF 表温度限制约束，则重置后温度 ≠ 重置前。

## 21.1.10 非预混边界条件（pp. 2626–2627）

- **21.1.10.1 混合分数边界条件**：进出口流动条件（速度/压力、湍流强度）照常定义；**不需要设组分质量分数**——改设进口的 **Mean Mixture Fraction 与 Mixture Fraction Variance**（Species 页；双混合分数另有 Secondary Mean Mixture Fraction 及其方差）。进口典型值：**燃料进口平均燃料混合分数 = 1.0、氧化剂/二次流进口 = 0.0；二次流进口二次混合分数 = 1.0、其余 = 0.0**；只在**烟气再循环（flue gas recycle）**时取 0–1 之间；**方差在进口一般取 0**。
- **21.1.10.2 进口扩散**：默认**不含**进口处混合分数的扩散输运；需要时用 `define/models/species/inlet-diffusion?` 或 Species Model 勾 **Inlet Diffusion**。
- **21.1.10.3 热边界条件**：非绝热须在进口设温度——应与 Chemistry 页查表输入**一致**（略有差异可接受；差异大时查表离散点聚集在 Chemistry 页温度范围附近，进口值落表外 → 插值不准）；壁面热边界用任意标准类型（定温/热流/外部换热系数/外部辐射）；含辐射时还要设壁面发射率。

## 21.1.11 非预混物理属性（pp. 2627–2628）

- 启用非预混后流体材料自动设为 **pdf-mixture**（混合物材料特例）；其组分 = PDF 查表创建时算出的物种，**不可直接改**；各组分的比热/分子量/生成焓取自化学数据库（不要改）；**PDF 混合物的平均密度与平均比热由查表确定**。
- **用户唯一输入 = PDF 混合物的输运性质**（黏度、导热等；Create/Edit Materials：Material Type = mixture、清单中 pdf-mixture 为唯一选择）。**输运性质可为温度函数、不可为组分函数**；实践上因湍流效应主导，连温度依赖也收益甚微。辐射属性照常设（**可用 WSGGM 组分依赖吸收系数**）。**真实气体**：启用 Compressibility Effects 后非预混可用真实气体模型（密度方法用四种真实气体模型之一）。

## 21.1.12 非预混求解策略（pp. 2628–2632）

- case 须满足 Theory Guide "Restrictions on the Mixture Fraction Approach" 的限制。
- **21.1.12.1 单混合分数**：解流场 + 平均混合分数与方差（非绝热加能量方程；层流火焰let加标量耗散）；温度与组分质量分数查表取得。
- **21.1.12.2 双混合分数**：另解平均二次部分分数及其方差；查瞬时值 → 构造燃料/二次流 PDF → 算平均值。**务必查看温度与组分表分辨率（足够而不过度）**。
- **21.1.12.3 从旧 case 启动**：读入旧 case 时与新模型不兼容的输入在启用非预混时被关闭并告警（case 物种与 PDF 文件不同 → 禁用；属性与化学数据库冲突 → 忽略）。**Important：prePDF 2 及更早的 PDF 文件不支持；PrePDF 3+ 完全兼容**。Species Model 选 Non-Premixed Combustion 点 OK → 立即弹 Select File 对话框要 PDF 文件（即 File/Write/PDF... 存的查表文件）；之后可随时 File/Read/PDF... 读入修改过的 PDF 文件。**Important：非预混仅压力基求解器 + 湍流模型激活时可用**。非绝热含压缩性 → Species Model 勾 **Compressibility Effects**（按 Eq 21.1 更新密度；非预混的压缩性**只能**在 Species Model 对话框启用——其他模型在 Create/Edit Materials 设密度方法）。
  - **21.1.12.3.1 case 读取时自动找回 PDF**：PDF 文件名存入 case 文件、读 case 时自动读 PDF。**完整目录名只有在首次经 GUI 读入（或文本接口连目录一起输入）时才保存**；否则自动读取可能失败、须手动指定——**最稳妥：首次用 GUI 或输全路径**。
- **21.1.12.4 求解**：初始化——混合分数与方差默认初值 0（**推荐，一般不要设非零**）；Run Calculation；残差报告出现 **fmean、fvar** 列（双混合分数另有 **psec、pvar**）。
  - **21.1.12.4.1 PDF 方程欠松弛**：平均混合分数与方差输运方程很稳——**默认欠松弛因子 1**（平均混合分数与二次部分分数）、**0.9**（两个方差）；残差上升再调低。
  - **21.1.12.4.2 密度欠松弛**：默认 1；收敛困难降到 0.5–1；真实气体可低至 0.1（同 Ch.20）。
  - **21.1.12.4.3 双混合分数 PDF 参数**：PDF 积分在 Fluent 内进行；**Compressibility Effects**（仅非绝热）——按系统压力变化从 PDF 表更新密度/温度/组分/焓。
- **21.1.13 PDF 表燃烧的 Robust Numerics**（p. 2632）：用 poor mesh numerics 提高鲁棒性。初始化或读 data 时自动创建 cell register **pdf_stability_marker**（标记 PDF Table Heat Loss/Gain 焓低于 PDF 表最小值的单元）与 register-based 定义 **pmn_pdf_stability_marker**（稳态每 5 迭代、非稳态每 2 时间步施加 poor mesh numerics）；**自动创建但默认停用**——运行前输 `solve/set/poor-mesh-numerics/register-based/edit pmn_pdf_stability_marker active? yes`；永久启用：Preferences → Simulation → **Robust Numerics for Combustion with PDF Tables**。默认设置可按 Manage Cell Registers（p. 4073）与 Robustness with Meshes of Poor Quality（p. 3891）编辑。
- **21.1.14 非预混后处理**（p. 2633–2634）：**Pdf... 类**——Mean Mixture Fraction、Secondary Mean Mixture Fraction、Mixture Fraction Variance、Secondary Mixture Fraction Variance、Fvar Prod / Fvar2 Prod（方差输运方程生成项）、Scalar Dissipation、PDF Table Adiabatic Enthalpy、PDF Table Heat Loss/Gain；**Species... 类**——Mass/Mole fraction、Molar Concentration、RMS species-n Mass Fraction；**Temperature... 类**——Static Temperature、RMS Temperature、Enthalpy；**Unsteady Flamelet... 类**——Probability、Mean Temperature、Mean Mass Fraction of species-n。**Important：非稳态扩散火焰let仅显示机理前 50 个物种的平均质量分数**。组分浓度由混合分数/方差场经查表导出；**绝热模拟（未解能量方程）也可后处理温度与焓——同样来自查表**。
  - **21.1.14.1 Inert 后处理**：额外变量（Inert... 类）——Inert Mass Fraction、Inert Specific Heat、Inert Density、Inert Enthalpy、Pdf Enthalpy、Pdf Fmean、Pdf Fvar、**Mass Fraction of Inert**（第 i 惰性物种质量分数 = 惰性示踪值 × Inert 对话框中该物种质量分数；公式体未提取）。

## 21.2 预混燃烧（pp. 2636–2642）

- **21.2.1 限制**：①**仅压力基求解器**；②**仅湍流亚音速**（缓燃 deflagration）；爆震/爆炸（激波后自燃）用密度基 + 有限速率模型；③**不能与污染物（soot/NOx）模型同用**——完全预混系统可改用部分预混模型（可与污染物模型同用）；④**不能用反应性离散相颗粒**（会变部分预混系统）——只允许惰性颗粒；⑤**G-Equation 模型只能配非稳态求解器**（时间追踪火焰前沿；RANS 趋稳态可时间演化至定常）。
- **21.2.2 使用步骤**：①启用预混模型（**Note：必须先选湍流模型且不能是 Spalart-Allmaras**）；②定义未燃/已燃材料物理属性；③进出口设进度变量；④初始化并 patch 进度变量；⑤求解与后处理。**Important：需要域内单个组分浓度 → 用部分预混模型，或从外部平衡/动力学分析获得未燃/已燃组成**。
- **21.2.2.2 绝热/非绝热**：Premixed Combustion Model Options 选 **Adiabatic（默认）/ Non-Adiabatic**——只影响温度计算方法（Theory Guide Eq 8.99 或 8.100）。
- **21.2.3 C/G 方程模型设置**：Premixed Model 选 **C Equation 或 G Equation** → 火焰速度模型选 **zimont 或 peters**。**非绝热**：Turbulent Schmidt Number 的值**同时用作能量的 Prandtl 数**（非绝热预混下 Viscous Model 对话框不显示 Energy Prandtl Number）——进度变量与能量（火焰推进放热）紧密相关，两输运方程须同扩散水平。
  - **21.2.3.1 Zimont 常数**（一般无需修改，默认适用面广）：Turbulent Length Scale Constant（Eq 8.81）、Turbulent Flame Speed Constant（Eq 8.79）、Stretch Factor Coefficient（Eq 8.87）、Turbulent Schmidt Number（Eq 8.72）、Wall Damping Coefficient（Eq 8.90）。
  - **21.2.3.2 Peters 常数**：**不在 GUI**（默认普适）——经 TUI 访问；**Ewald Corrector 默认启用**；Turbulent Schmidt Number 与 Wall Damping 同 Zimont。
  - **21.2.3.3 G-Equation 附加选项**：**G Equation Settings**——火焰距离方差选**输运方程或代数式**（Theory Guide Eqs 8.76/8.77）；**RANS 推荐输运方程、LES 推荐代数式**；**Flame Curvature Source**——G 方程曲率源项（Eq 8.74 末项），**默认不含**。
  - **21.2.3.4 未燃混合物属性**：流体材料按未燃混合物赋属性——含热扩散率 α（Eq 8.79；α = k/(ρ·cp)，标准条件值查燃烧手册 [85]）；**Laminar Flame Speed**（绝热/非绝热都要）：constant / UDF / **metghalchi-keck-law**；Zimont 含火焰拉伸效应：**Critical Rate of Strain**（Eq 8.88）——**默认值极高（无拉伸发生）**，要含拉伸须按燃烧器实验数据调低；**贫预混典型值 3000–8000** [181]（量纲在提取文本中缺失）；均可常数或 UDF。**绝热模型**：另设 **Adiabatic Burnt Temperature**（Eq 8.99；绝热产物温度；决定温度线性变化；常数或 UDF）。**非绝热模型**：改设 **Heat of Combustion**（单位质量燃料燃烧热；**只能常数**）与 **Unburnt Fuel Mass Fraction**（常数或 UDF）——燃烧热损失/增益进能量方程（Eq 8.101）。**密度**：Density 下拉选 **premixed-combustion** + 设 **Adiabatic Unburnt Density 与 Adiabatic Unburnt Temperature**（Eq 8.102；绝热时未燃温度还用于 Eq 8.99 算温度）。其余：黏度、比热、导热及其他联动模型属性。
  - **21.2.3.5 进度变量边界条件**：**c = 0 未燃混合物；c = 1 已燃混合物**（进出口均需设置）。
  - **21.2.3.6 进度变量初始化**：常可全域初始化 c = 1（已燃）——未燃气从进口把火焰吹回稳焰器；**更好：先初始化流场再 patch——稳焰器上游 c = 0、下游 c = 1**。
- **21.2.4 预混后处理**（Premixed Combustion... 类）：Progress Variable、Damkohler Number、Stretch Factor、Turbulent Flame Speed、Static Temperature、Product Formation Rate、Laminar Flame Speed、Critical Strain Rate、Unburnt Fuel Mass Fraction、Adiabatic Flame Temperature。**Static Temperature 与 Adiabatic Flame Temperature 仅绝热计算出现在本类**（非绝热的 Static Temperature 在 Temperature... 类）；**Unburnt Fuel Mass Fraction 仅非绝热**。**G-Equation 另有**：Mean Distance from Flame、Variance of Distance from Flame（瞬时火焰位置相对平均火焰位置的方差）。
  - **21.2.4.1 组分浓度计算**：已知未燃/已燃组成（来自单独 Fluent 或外部平衡/一维预混火焰分析）时，用**自定义场函数**合成——未燃物种浓度 = 该物种未燃质量分数 ×（1 − c）的函数、已燃物种浓度 = 已燃质量分数 × c 的函数（公式体未提取，按文字语义记录）；见 Custom Field Functions（p. 4519）。

  - **21.2.4.1 组分浓度计算**：已知未燃/已燃组成（来自单独 Fluent 或外部平衡/一维预混火焰分析）时，用**自定义场函数**合成——未燃物种浓度 = 该物种未燃质量分数 ×（1 − c）的函数、已燃物种浓度 = 已燃质量分数 × c 的函数（公式体未提取，按文字语义记录）；见 Custom Field Functions（p. 4519）。

## 21.3 部分预混燃烧（pp. 2643–2670）

- **21.3.1 限制**：非预混与预混模型的理论/假设/限制**直接适用**；单混合分数限两条进口流股（纯燃料/纯氧化剂/燃料氧化剂混合物）；双混合分数扩到三条但开销巨大。**FGM 模型仅限 c-Equation 部分预混模型**。
- **21.3.2.1 设置流程 11 步**：①读网格 + 启用其他模型（湍流、辐射等）；②启用 Partially Premixed Combustion（**Note：先选非 Spalart-Allmaras 湍流模型**）——**Premixed Model = C Equation** → State Relation 四选：Chemical Equilibrium / Steady Diffusion Flamelet / Unsteady Diffusion Flamelet（稳态模拟、从收敛的稳态扩散火焰let解出发）/ **Flamelet Generated Manifold**；**Premixed Model = G Equation** → 只有 Chemical Equilibrium 或 Steady Diffusion Flamelet；③两类部分预混模型：**薄火焰let**（平衡与扩散火焰let）vs **有限厚度火焰let**（FGM）；④FGM 还须选 Premixed Flamelet 或 Diffusion Flamelet + Premix 页的 **Turbulence-Chemistry Interaction**（Finite-Rate 与 Turbulent Flame Speed，FGM Turbulent Closure）；⑤Flamelet 页参数；⑥生成 PDF 表——**层流火焰速度函数超范围警告 → 保存 PDF 文件前手工修改分段线性点**；热扩散率计算用 Create/Edit Materials 的导热系数——**编辑导热后在 Properties 页点 Recalculate Properties 可得更准多项式**；⑦未燃材料属性——层流火焰速度自动选 **prepdf-polynomial**（PDF 表分段线性多项式）；替代：constant / UDF / metghalchi-keck-law / **laminar-flame-speed-computed** / **laminar-flame-speed-library**；⑧边界条件——平均进度变量 + 平均混合分数及方差（双混合分数另有二次部分分数及方差）；**Important（预混进口两种设法）**：(a) Boundary 页燃料组成 = 预混进口物种 → 边界设 c = 1、f = 0；(b) 燃料组成 = 纯燃料 → 设正确当量比对应的混合分数。手册示例（甲烷/空气 φ = 0.3）：(a) 燃料组成 CH4 = 0.017、O2 = 0.236、N2 = 0.747 + c = 1、f = 0；(b) 燃料组成 CH4 = 1.0 + f = 0.017、c = 0；**法 (a) 更优（火焰区点更多）**；⑨patch 初始化进度变量；⑩焓低于 PDF 表最小值的单元施 poor mesh numerics（见 21.1.13）；⑪求解与后处理（非预混的求解参数指引同样适用）。
- **21.3.2.2 导入 flamelet**：Chemistry 页 Import Flamelet + Import Flamelet File...，完成直接跳 Table 页。
- **21.3.2.3 FGM**：相对薄火焰平衡/稳态扩散火焰let的优势——**可模拟稀释导致的火焰淬熄**等；流形可用 Premixed Flamelet 或 Diffusion Flamelet 生成。**Premixed Flamelet** 的解法空间（Flamelet Solution Method）：**Progress Variable Space 或 CHEMKIN Physical Space**。FGM 状态关系下 Fluent 解反应进度变量方程（Theory Guide Eq 8.115）；**默认进度变量定义**普适于宽范围碳氢火焰（推荐）——可自定义：Boundary 页 **Set Progress Variable...** → Progress Variable Definition 对话框（物种 + 权重）：关 Use Default Progress Variable → 改权重 / Add/Remove 物种。
  - **21.3.2.3.1 预混 FGM 火焰let参数**：**Number of Grid Points in Mixture Fraction Space**（预混火焰let在全部混合分数点求解——时间随点数线性增）；**Number of Grid Points in Reaction Progress Space**（未燃→已燃；Progress Variable Space 下时间/内存随分辨率增）；**Scalar Dissipation at Stoichiometric Mixture Fraction**（预混火焰let应变率；**默认 1000/s ≈ 自由传播无应变预混火焰在化学计量混合分数的标量耗散**；仅 Progress Variable Space 可用）；User Defined Flamelet Parameters；**AGR**——Initial Number of Grid Points（默认未提取）、Maximum Number of Grid Points（**默认 64**）、Maximum Change in Value/Slope Ratio（**均默认 0.5**；Theory Guide Eqs 8.28/8.29）、**Refine flamelet based on**：Stoichiometric mixture fraction 或 Specified（须再给混合分数水平）。**Note：CHEMKIN Physical Space 下 AGR 默认**——Initial 12、Maximum 250、Value Ratio 0.5、Slope Ratio 0.1。点 Calculate Flamelets。
    - **21.3.2.3.1.1 编辑火焰let网格分布**：默认分布够用勿改；特例可 Edit... → Distribution of Points 对话框（显示 Stoichiometric f 与网格点值）→ 勾 Edit Distribution 改值；Write Grid to File...（ASCII XY plot 格式，点号+值对）与 Read Grid from File...。
  - **21.3.2.3.2 扩散 FGM**：生成类似稳态扩散火焰let；附加参数 Initial Scalar Dissipation / Scalar Dissipation Multiplier / Scalar Dissipation Step（语义同 21.1.6.1；示例 1e-3/10/5 → 1e-3、1e-2、0.1、1.0、6、11、16…）。**Note：FGM 不需要 Maximum Number of Flamelets**——Fluent 增大标量耗散直至火焰let熄灭；**Scalar Dissipation Step ≈ 对流扩散火焰let熄灭应变率的 1/20 → 约 20 个火焰let**；**最后熄灭的非稳态扩散火焰let用于建模未燃态与熄灭前最高标量耗散稳态火焰let之间的流形**；**Include Equilibrium Flamelet** 决定进度变量（Eq 8.109）算法——勾选 = 平衡计算；否则 = 以初始标量耗散火焰let解为分母计算。网格分布编辑同预混 FGM。
  - **21.3.2.3.3 非绝热 FGM 热损失**：条件——Premixed Flamelet + Non-Adiabatic + **CHEMKIN Physical Space** → Flamelet 页勾 **Nonadiabatic Flamelets**。附加参数：**Number of Grid Points in Enthalpy Space**（焓级数按参考燃料/氧化剂温度自动分布；每增一点 = 整个混合分数空间再生成一组火焰let）；**Fully Premixed FGM**——只对单个混合分数（Mixture Fraction Value for Flamelet Generation）生成非绝热火焰let；启用后混合分数网格点自动 = 1——**快且 flamelet/PDF 文件大减**（适合混合分数恒定的完全预混问题）。
- **21.3.2.4 PDF 查表**：AGR 禁用时部分预混专属参数——**Number of Mean Progress Variable Points**（由 flamelet 网格点数确定）、**Number of Progress Variable Variance Points**（方差向变化缓、低分辨率可）、Maximum Number of Species（**200 上限**；密度/比热全物种预算）、Number of Mean Enthalpy Points（非绝热）、Minimum Temperature（非绝热；低于系统最低温 10–20 K）。**Note：AGR 禁用时表参数网格分布可编辑**——Mean mixture fraction（可勾 **Use Flamelet Distribution** 用 FGM flamelet 网格）、Progress variable variance、Mean fraction variance；**Mean progress variable 只可查看不可编辑**。AGR 启用时：Initial/Maximum Number of Grid Points（平均混合分数/方差/焓 + FGM 的进度变量与方差）、Max Change in Value/Slope Ratio、Maximum Number of Species。**Note：AGR 不可用于双混合分数**。
  - **FGM Scalar Transport**：为选定物种质量分数（FGM 标量）解附加输运方程——点 **FGM Scalar Transport** → Select Transported Scalars 对话框 Add/Remove；流动边界的 Species 页设 Scalar Mass Fractions；求解中解输运方程 + **从 PDF 表取预计算的平均反应速率**。**Note：必须在算 PDF 表之前选定 FGM 输运标量（表算完后改定义须重导/重生成 flamelet）**；**标量方程不反馈流动/混合物属性 → 稳态模拟可作后处理模式解**（如污染物生成）——Equations 对话框先取消 FGM Scalar Transport、流场收敛后再勾回。点 Calculate PDF Table。
  - **21.3.2.4.1 FGM 查表后处理**：PDF 表**绝热 4 维**（平均混合分数、平均反应进度变量、混合分数方差、进度变量方差）、**非绝热 5 维**（+焓）；固定两个以上自变量画 2D 曲线与 3D 曲面；流程类似 21.1.7.4，附加：绝热——3D 曲面 = Volume Parameters 固定第一参数（Index 或 Value）+ Surface Parameters 固定第二参数 → 对余下两维画图；2D 曲线 = 再在 Curve Parameters 选 X-Axis Function + Constant Value of Independent Parameter 固定最后参数；非绝热——先定 **Enthalpy Slice**（热损失/增益为第五维、以焓级表示；**默认固定在绝热级**——显示 "Enthalpy Slice, Adiabatic = slice number"；**低于绝热级 = 热损失、高于 = 焓增益**），再按绝热步骤。
- **21.3.2.5 FGM 标准文件**：关键字表——HEADER、BODY、NUMOFSPECIES、GRIDPOINTS、PRESSURE、TEMPERATURE 和 TEMP、MASSFRACTION-、Z、MOLEFRACTION-、**PREMIX_CHI**（预混火焰let标量耗散）、**REACTION_PROGRESS**（反应进度）、**PREMIX_YCDOT**（反应进度源项）。**Note：FGM 格式对预混与扩散火焰let相同；与稳态扩散层流火焰let标准格式不同**。样例文件另出现 **PREMIX_STOICH_SCADIS** 关键字（头段示例；未列入支持关键字表——照录）。
- **21.3.2.6 预混火焰传播参数**（PDF 表生成后，Premixed 页）：**Turbulent Flamelet Speed Model**——Flame speed Model 选 zimont（参数同 21.2.3.1）或 peters（同 21.2.3.2）；**SBES 湍流模型 + C Equation 预混**时另有 **Turbulent Length Scale Constant (RANS)** 与 **Turbulent Flame Speed Constant (RANS)**（RANS 区常数）。**FGM 附加**：**Turbulence-Chemistry Interaction**——进度变量方程（Eq 8.115）源项方法：**Finite-Rate**（Eq 8.116，从 PDF 表算源项）或 **Turbulent Flame Speed**（Eq 8.117）。**Variance Settings**——Variance Method：**transport equation**（Eq 8.118）/ **algebraic**（Eq 8.119）/ **hybrid（仅 SBES）**（Eq 8.120；代数式与输运式分区使用）；algebraic 与 hybrid 须设 **Algebraic Variance Constant**；**推荐：RANS 用输运方程、LES 用代数、SBES 用 hybrid**。
- **21.3.2.7 未燃混合物属性多项式**：PDF 表建成后自动算未燃混合物的温度/密度/热容/热扩散率——**平均混合分数的多项式函数**（Theory Guide Eq 8.129）；层流火焰速度 = 平均混合分数的**分段线性多项式**。**prepdf-polynomial 法**是对详细模拟火焰速度的曲线拟合 [57]，**适用范围**：燃料 **H2、CH4、C2H2、C2H4、C2H6、C3H8**；氧化剂空气；当量比**贫限至 1**；未燃温度 **298–800 K**；压力 **1–40 bar**——**超范围会在算表时告警 → 保存 PDF 文件前在 Properties 页改分段线性点**；laminar-flame-speed-computed / library 法自动算多项式系数、**不可修改**。**Properties 页 Partially Premixed Mixture Properties**：Adiabatic Unburnt Density、Adiabatic Unburnt Temperature、Unburnt Cp、Unburnt Thermal Diffusivity——各配 Coefficient 1–4（Quadratic of Mixture Fraction 对话框；Eq 8.129）。**prepdf-polynomial 层流火焰速度**：Piecewise Linear 对话框——混合分数与对应火焰速度 **20 点**；**首点 = 下限、末点 = 上限，限外恒等于限值**；library 法只读。**Important：在 Create/Edit Materials 用 UDF 层流火焰速度 → 分段线性拟合失效**。**二次混合分数模型启用** → 未燃属性为两个混合分数的函数（Piecewise Linear 对话框多一列二次系数）。**Non-Adiabatic Laminar Flame Speed 选项**——把层流火焰速度按非绝热效应制表入 PDF 表。
- **21.3.2.8 拉伸层流火焰速度**（FGM + 湍流火焰速度模型）：①State Relation = FGM；②火焰let与 PDF 表算完后在 Premix 页选 Turbulent Flame Speed 并设参；③Properties 页勾 **Strained Laminar Flame Speed**（**仅当 CHEMKIN 机理与热力学之外还导入了输运数据文件时出现**）；④点 **Compute Strained Laminar Flame Speed Table**（对不同混合分数点与应变率生成拉伸火焰let）；⑤非绝热拉伸火焰速度：**Number of Heat Loss Points > 1**（热损失参数，Theory Guide Eq 8.141；**默认 1 = 绝热**；>1 时按热损失参数 0.05 增量计算——如 3 点 = 0、0.05、0.1；**多数应用 < 10 点足够**）；⑥**Display Strained Flamelets...** → Flamelet 2D Curves（Flame Speed 为 Flamelet Variable；X-Axis Function 选 Strain Rate 或 Mixture Fraction；Slice by Index/Value；Plot；可 Write to File）。
- **21.3.2.9 内燃机燃烧**：全部部分预混模型可用于缸内燃烧；多循环的滞留产物与 EGR 用 **Inert 模型**（21.1.9）+ Dynamic Mesh Event（算惰性组成、已燃气转惰性、复位下一循环；见 Resetting Inert EGR p. 1967/2625）。**G-Equation 模型：这是自动模拟多缸内循环并计及跨循环滞留已燃气的唯一途径**。
- **21.3.2.10 FGM Scalar Transport 后处理**：FGM 标量的标量质量分数报告量在 **Premixed Combustion...** 类。
- **21.3.2.11 GPU 求解器 FGM 限制**：边界上 **Total Sensible Heat Transfer Rate 通量报告不可用（报 0）**；**species-n 场变量在边界报 0**（后处理可在 cell zone 内近边界建 plane surface）；**Progress Variable 及其方差在边界报 0**（同上变通）。


## 证据与适用条件

- 批次 70 覆盖 pp. 2571–2625；批次 71 覆盖 pp. 2626–2642；批次 72 覆盖 pp. 2643–2669（**p. 2670 为空白版权页）。Ch.21 全章（pp. 2571–2670）完成**。
- **公式**：Eq 21.1–21.10（批次 70 段）公式体未提取，按周边文字记录结构、变量与语义；批次 71–72 段无新编号公式（引用 Theory Guide Eqs 8.72–8.141 未展开）；批次 70 段 Inert EGR Reset 的贫/富公式与符号名未提取；21.2.4.1 组分浓度自定义场函数的公式体未提取、按文字语义记录（未燃 ×(1−c)、已燃 ×c）；FGM hybrid 方差法的分区使用对象符号未提取。
- Figures 21.1–21.51（对话框截图与示例图）为图形元素未摄取；正文引用的 Theory Guide 式号（8.13–8.25、8.28–8.29、8.49–8.59、8.72–8.102、8.109、8.115–8.120、8.129、8.141）未展开；提取缺失值：AGR 的 Initial Grid Points 默认值（预混 FGM 与扩散火焰let）、21.2 Critical Rate of Strain 默认值与量纲、SBES hybrid 方差分区符号。
- 默认值（Maximum Scalar Dissipation 30/s、Courant 1、慢化学置零清单、Maximum Species 200、Minimum Temperature 低于系统最低温 10–20 K、Burnout Stoichiometric Ratio 2.67、水潜热 2.25e6 J/kg、RFL ≈ 2× 化学计量分数、惰性物种 0.01 摩尔分数丢弃阈、PDF 方程欠松弛 1/0.9、pmn 每 5 迭代/2 时间步、贫预混 Critical Rate of Strain 3000–8000、FGM 化学计量标量耗散 1000/s、FGM AGR 64/0.5/0.5 与 CHEMKIN Physical Space 12/250/0.5/0.1、FGM 网格点编辑、Scalar Dissipation Step ≈ 熄灭应变率 1/20、热损失点增量 0.05 且 <10 点、预混进口法 (a) 优先、prepdf 拟合范围 H2/CH4/C2H2/C2H4/C2H6/C3H8·贫限–1·298–800 K·1–40 bar、Piecewise Linear 20 点）为 2026 R1 手册记载，随版本可能变化。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]
- [[Part III - Solution Mode]]
- [[Fluent 组分输运与有限速率化学]]（Coal Calculator 通用版与 CHEMKIN 导入；Ch.20）
- [[Fluent 滑移与动网格]]（Dynamic Mesh Events、In-Cylinder；Ch.14）
- [[index]]
