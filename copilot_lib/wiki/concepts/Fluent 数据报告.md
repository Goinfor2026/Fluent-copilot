---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - reporting
  - report-definitions
  - monitors
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 数据报告

## 摘要

User's Guide 2026 R1 Part III / Chapter 42 "Reporting Alphanumeric Data"（PDF pp. 4325–4394，15 节）。**本页全章完成（批次 116–117，pp. 4325–4394）：42.1–42.15 全 15 节——报告约定、报告定义九类型、报告文件/绘图/滑动平均、输出参数、通量/力/投影面积/面积分/体积分/效率计算、直方图/DPM/S2S 报告、参考值、case 摘要与系统资源报告。**离散相报告工具另见 p. 2938。

## 42.1 报告约定（p. 4325–4326）

- **2D**：所有积分量按**单位深度**（默认 1 m）计算——仅在 Reference Values 任务页改 **Depth**；**深度值不受 Set Units 单位切换影响**（默认 1 m，改单位为 cm 后值即 1 cm）。DPM 与流体质量流量恒按 1 m 深度模型假设并相应缩放（参考深度 0.5 m → 体积积分中的质量流量减半）。
- **轴对称**：所有积分量按 **2π 弧度（完整 360°）** 计算。

## 42.2 监视与报告解数据（pp. 4326–4360）

**报告定义（Report Definition）** = 在每次迭代/时间步末计算指定量的对象；多个定义可打印到控制台、写入单一报告文件、或绘入同一窗口；用于监视收敛、验证网格无关性、记录时间历程；可做 surface/volume/force/moment/flux 积分运算。定义建好后加入 report file（一文件多定义）；report plot 同窗绘多定义；一定义可入多文件/多图。**注意**：2019 R3 前建的 Expression 报告定义现在显示为 Custom Report Definitions 且可能无法求值——用 Expression Report Definition 对话框重建。

### 42.2.1 创建报告定义（pp. 4326–4350）

入口多处：ribbon `Solution → Reports → Definitions → New → <类型>`；树 Report Definition 分支右键；图形窗口右键（网格显示且选中面/体时）；Report Definitions 对话框 New 下拉。Apply 按钮保存输入、Reset 恢复。**通用步骤**（以 Surface 为例）：
1. **Name**。
2. **Per Surface / Per Zone**（逐面/逐区报告而非净值）——**与 Average Over > 1 不兼容**（净值不反映平均设定；Compute/表达式/输出参数显示的是净值）；要用 Average Over ≥2 就逐面/逐区各建定义。
3. **Average Over**（>1 的正整数 = 打印/绘制/写入**滑动平均**而非瞬时值；不足 N 步时对已有值取平均）。**增大后出现 Retain Instantaneous Values 选项**——勾上则报告文件同时存平均值与瞬时值（保留日后改 Average Over 的灵活性）；**计划将来改 Average Over 就至少从 2 起步**。
4. Create 组的 **Report File 与 Report Plot 默认自动启用**（偏好 Simulation → Report Definitions → **Automatically Plot and File** 控制）；要把所有定义写进单一文件就从 Report Files 列表选既有文件。
5. **Create Output Parameter**（可选；Per Surface/Per Zone + 多选面时输出参数只给单一合并值）。
6. **Report Type** 选积分方法（surface 类型清单见 42.2.1.1）。
7. Custom Vector 类须在 Custom Vectors 组定义矢量。
8. **Field Variable**（质量/体积流量类除外）；多相时按需选 Phase。**注意**：任意变量×任意报告类型的组合未必物理有意义；**多相的质量流量只能用 Mass Flow Rate 积分——勿用 Flow Rate 积分 Volume Fraction（结果错误）**。
9. 选 Surfaces/区。10. OK 创建。

**Report Definitions 对话框**复查/修改既有定义；**瞬态自动创建的 flow-time、delta-time、iters-per-timestep 三个定义不可导出或复制**。

- **42.2.1.1 Surface 报告**：Report Type 十七选——Integral、Standard Deviation、Flow Rate、Mass Flow Rate（非场）、Volume Flow Rate（非场）、Area-Weighted Average、Mass-Weighted Average、Sum、Uniformity Index（Mass/Area Weighted）、Facet Average/Minimum/Maximum、Vertex Average/Minimum/Maximum、Custom Vector Based Flux / Custom Vector Flux（非场）/ Custom Vector Weighted Average。数据须配 Report File/Report Plot（已包含的定义在文件/图中高亮；取消勾选 OK 即从该文件/图移除）。
- **42.2.1.2 Volume 报告**：Report Type 十选——Volume（非场）、Sum、**Sum*2Pi（仅 2D 轴对称）**、Max、Min、Volume Integral、Volume-Average、Mass Integral、Mass-Average、Mass（非场）。Per Zone 同前；**Cell Zones 列表包含表达式体积（expression volumes）**——**cell registers 虽出现在列表但不能用于 volume 报告定义**。
- **42.2.1.3 Force/Moment 报告**（Drag/Lift/Moment/Force 四对话框，一次只能开一个、同类可多定义）：监视力系数可提前停算省时（系数常先于残差三个量级收敛——**此时还要核查质量流量与换热率确保守恒**）。**前提：先在 Reference Values 任务页填参考值**（力系数用参考面积/密度/速度；力矩系数再加参考长度）；Tip——Report Output Type 选 **Drag Force / Lift Force 可报告未缩放的力值**。专用步骤：Per Zone；Drag/Lift/Force 给 **Force Vector** XYZ（Drag 默认 (1,0,0) 单位向量、Lift 默认单位向量另一方向——原文符号占位）；Moment 给 **Moment Center**（默认 (0,0,0)）与 **Moment Axis**（默认 z 向单位向量）；选壁面区；OK；改设置双击树中定义。
- **42.2.1.4 Flux 报告**：类型十一选——Mass Flow Rate、Total Heat Transfer Rate、Total Sensible Heat Transfer Rate、Radiation Heat Transfer Rate、Pressure Work Rate、Viscous Work Rate、Film Mass Flow Rate、Film Heat Transfer Rate、DPM Mass Source、DPM Enthalpy Source、DPM Sensible Enthalpy Source。**注意**：**内部区的 Mass Flow Rate 必须勾 Per Zone 才有值，否则报 0**（例：10 个内部区的连续流体域逐区求和会得 10 倍真实质量流量，故不逐区时报 0）；**通量只能在边界上算——不能在 plane/point/iso 等用户自定义面上**；开 Create Output Parameter 时输出参数会显示源项贡献（如适用）。
- **42.2.1.5 Mesh 报告**：**Cell Count**（单元区内单元数）与 **Face Count**（边界面区面数）——自适应/动网格 remeshing 场景有用；Per Zone 同前；选区；OK。
- **42.2.1.6 Aerodamping（Travelling Wave Method）报告**：Solution → Reports → Definitions → New → Aeromechanics Report → Aerodamping (Travelling Wave Method)...——多主叶时勾 **Per Zone**（按动网格区逐叶算阻尼，一个动网格区含一主叶 ± 分裂叶）；**Integrate Over** = 计算阻尼值的积分时间步数（**建议 = 每周期时间步数**——Run Calculation 任务页可见该数；改变每周期步数时需同步改此设置）。详见气动阻尼（叶颤振）p. 2036。
- **42.2.1.7 DPM 报告**：类型七选——**Injected Mass**（仅瞬态追踪；注入域内总 DPM 质量）、**Mass in Domain**（仅瞬态；域内现存总质量）、**Mass in Fluid**（仅瞬态；自由流颗粒质量——**需 wall-film 边界条件**）、**Mass in Film**（仅瞬态；壁面液膜中的质量——需 wall-film）、**Escaped Mass**（经指定边界离开域的质量）、**Evaporated Mass**（所选 injection 的总蒸发质量——含完全蒸发颗粒与其他颗粒的蒸发部分；瞬态追踪含域内现存颗粒）、**Penetration Length**（仅瞬态；穿透长度 m）。专用步骤：Escaped Mass 按注入统计需启用 TUI `report/dpm-zone-summaries-per-injection`（此时出现 Injections 列表）→ 选 injections → 选出口边界；Penetration Length 可设 **Particles Mass Fraction** 与 User-Specified Origin and Direction；瞬态追踪时六种质量类报告可勾 **Show Mass Flow/Change Rate**（默认）报流量而非总质量。**重要**：瞬态追踪中要按 injection 选 Escaped Mass，须在**首批颗粒注入前**启用上述 TUI 命令，否则数值可能不一致。
- **42.2.1.8 User Defined 报告**：两步——①用 **`DEFINE_REPORT_DEFINITION_FN`** 宏写函数（参数为函数名、返回 real；函数体任意合法 C；可用全部 UDF API，含所有报告定义的最近求值与设为 UDF 内使用的输入参数当前值）并编译加载；②User Defined Report Definition 对话框从 Function 下拉挂接。
- **42.2.1.9 Expression 报告**：用报告定义组合数学运算生成新定义（如进出口面加权压差）或对单一定义施加表达式函数/规约操作。步骤：先建所用 Report Definition(s) → Definition 框右侧下拉选定义/变量/函数组合，或直接输入表达式（**用花括号 `{}` 引用对象（报告定义/cell register）时自动建议禁用，必须手写对象的显示名**）→ OK。详见 Fluent Expressions Language（p. 1059）。

### 42.2.2 报告文件与报告绘图（pp. 4351–4360）

- 概念：Report Files/Plots = 报告定义集合，按指定间隔写入单一文件或绘入图形窗口；稳态按迭代、瞬态可按迭代或时间步。**同一 Report Plot 中的定义必须同单位**。文件格式照录：`"<name>"` / `"Iteration"|"Timestep" "<defs...>"` / 数据行。可打印到控制台；可对特定计算停用（Active 勾选）并再启用。Automatically Plot and File 偏好控制新定义默认启用。
- **42.2.2.1 创建 Report File**（Solution → Monitors → Report Files → New...）：树中名称 + Active 勾选；Available Report Definitions → **Add>>**；File Name——**Linux 告诫：文件名首字母为 "n" 或 "t" 时路径可能成 `\nreport-file-0.out` 被解释为隐藏文件**；**Get Data Every** 频率——**瞬态且定义设了 Average Over 时必须选 time-step 或 flow-time；选 iteration 则用瞬时值**；（可选）**Write Instantaneous Values**（保留改 Average Over 的灵活性）；OK。Report File Definitions 对话框（右键 Report Files → Edit...）查看/编辑；**Edit Report File** 对话框改单文件。
- **42.2.2.2 创建 Report Plot**（Solution → Monitors → Report Plots → New...）：名称 + Active；Add>> 定义；Plot Title 与 Y-Axis Label；频率（Average Over 注意同上）；（可选）**Plot Instantaneous Values**（平均值旁叠加瞬时值）；OK。**默认新会话重绘旧 report plot 只显示 1000 点**——Preferences → Simulation → Report Definitions → **Report Plot Data History Size** 调大。Report Plot Definitions / Edit Report Plot 对话框编辑；开始迭代后图显示于图形窗口，关窗后右键 Outline View 中该 report plot → Plot 重显示。
- **42.2.2.3 滑动平均监视**：改 Average Over 可平滑或暴露波动。流程：建定义 → Average Over ≥2 起步（确保报告文件启用 Write Instantaneous Values；**报告间隔 >1 时出现 Retain Instantaneous Results 勾选框——要保留日后改间隔的能力必须勾着**）→ 确认 Report Plot/File 启用或入既有 → OK。日后重开定义对话框改 Average Over 即可（关联 report plot 重绘时生效）；Report Plot 勾 **Plot Instantaneous Values** 叠加瞬时值（Figure 42.22）；新会话仍可叠加的前提 = Report File 开 **Write Instantaneous Values**。
- **42.2.2.4 清除文件与绘图历史**：不动对象、不清定义——树中右键 Report Files/Report Plots 下对应名称 → **Clear Data**。

## 42.2.2（续）Clear Data 补充（p. 4361）

右键 report file → Clear Data 会**从系统删除该文件**（继续迭代后重建同名新文件）；report plot → Clear Data 只清内存数据（再迭代后重显）。

## 42.3 创建输出参数（pp. 4361–4363）

输出参数 = 各类报告生成的单值，用于跨 case 对比或供 mesh morpher/optimizer 最小化函数使用。可来自：通量、力、面积分/体积分、Surface/Volume/Drag/Lift/Moment/Force/Flux/Cell Count/Face Count/Aerodamping/DPM/User Defined/Expression 报告定义、**命名表达式**。入口：User Defined ribbon → Field Functions → **Parameters...**（Parameters 对话框；Input Parameters 由 p. 1358 步骤填充）；Output Parameters 组 Create 下拉 → From Report Definitions... 打开 Report Definitions 对话框。**告诫**：Per Surface/Per Zone + 多选面 + Create Output Parameter = 单一合并值输出参数；**此类定义的 Average Over 必须为 1**——>1 配 Per Surface/Zone 给出无效合并净值。Output Parameters 列表可 **Edit...**（重开报告对话框改定义）；More 下拉——Delete、Rename、**Print to Console / Print All to Console**、**Write... / Write All...**。

## 42.4 边界通量报告（pp. 4363–4373）

Results → Reports → Fluxes → Edit...（Flux Reports 对话框）。Options 九选：**Mass Flow Rate**；**Total Heat Transfer Rate**（热通量 + 压力功 + 焓对流 + （压力基）黏性功之和，用户源项计入总平衡；**太阳辐射的热量单列 Total Solar Source**）；**Total Sensible Heat Transfer Rate**；**Radiation Heat Transfer Rate**（体积辐射源净通量在 Net Radiation Source 字段）；**Pressure Work Rate**（仅能量方程 + Absolute 速度公式 + Fluid 区开 Frame/Mesh Motion；只计流体侧）；**Viscous Work Rate**（仅能量方程 + 压力基）；**Film Mass Flow Rate / Film Heat Transfer Rate**（仅 EWF 模型，见 [[Fluent Eulerian 壁面液膜]]）；**Electric Current Rate**（仅电位方程启用）。步骤：Options → **Boundaries 选边界区**（Filter Text 过滤；**通量只能在边界算，不能在 plane/point/iso 等自定义面**）→（可选）**Save Output Parameter...**（存 case 后读入会生成等价报告定义）→ **Compute**——逐区显示 + **Net Results** 合计（Fluid 对话框设了质量/能量源时，其积分值列入 **User Source** 并加进 Net Results）。**重要——两侧同流体的内部区通量**：面法向面积向量可能在读网格时定义不一致导致通量不准——**先把区 Type 改为 wall 再改回 interior**（强制重定向量）再报告；只选内部区时净质量流量可能显示 0（内部边界不计入净进出流）。通量按求解器原样计算——**天然比 Surface Integrals 的 Flow Rate 更准**。
- **42.4.2 反应流**：须启用 Species Model 才出现 Total Sensible 选项。两口径——**Total Heat Transfer Rate** = 总焓通量（热焓 + （开 Volumetric Reactions 时）组分生成焓；**反应流中的守恒量**）；**Total Sensible Heat Transfer Rate** = Eq 5.5 总能通量（**非守恒量**——反应热单列 **Heat of Reaction Source**（多反应求和；放热为正、吸热为负））。两个 Net Result 都小 = 能量平衡好；能量/组分未全收敛时两者可能不同——继续迭代。**非预混/部分预混**：Heat of Reaction Source = 两者净值之差；Heat of Reaction 场函数不可用。
- **42.4.3 含颗粒（DPM）**：颗粒注入贡献单列并计入净平衡——Mass Flow Rate 报 **DPM Mass Source**；Total Heat 报 **DPM Enthalpy Source**；Total Sensible 报 **DPM Sensible Enthalpy Source**；P1/DO 开 Particle Radiation Interaction 时 Radiation Heat Transfer Rate 报 **DPM Radiation Source**。**告诫**：DPM + 反应流时 Heat of Reaction Source 只报连续相均相反应热；**颗粒反应（如焦炭燃烧）热在 DPM Sensible Enthalpy Source**。Lagrangian wall film 颗粒：Net Results 的总换热率 = Wall Film Heat Flux 场变量的面积分。
- **42.4.4 多相**：按相与混合相分别报告（视模型）；逐相源项进各相 User Source；**相间传质/传热在各相报告中表现为不平衡——检查总体平衡要选 mixture 相**（报告含所有相的通量与源之和）。多相 + 化学反应的 Total Sensible 约定：选含气相反应的相 → Heat of Reaction Source 只含该相反应；选 mixture → 为所有气相反应 + 非均相反应热之和。
- **42.4.5 DDPM**：各相同 42.4.4；离散（DDPM）相另报**域内通量**——Mass Flow Rate 报 **DDPM In-domain Mass Rate**、Total Heat 报 **DDPM In-domain Heat Rate**（计入域内注入与域内消失的颗粒；仅限指派给 discrete phase 的颗粒）。未指派的 DPM injection 照旧报 DPM source。示例报告照录（表面注入进 inlet 通量、域内 single injection 进 In-domain Rate、净质量近零）。**DDPM 限制**：读旧 data 后需先跑一步（稳态一迭代/瞬态一时间步）更新 In-domain 量；同时存在指派与未指派 injection 的旧 case 须重跑才能得到正确 DPM source；纯后处理功能不影响解；**入流边界注入的再注入（reinjected）颗粒不计入边界通量——计入 In-domain 流率以保质量平衡**。
- **42.4.6 电位求解器**：Electric Current Rate；Total Heat Transfer Rate 开 Include Joule Heating 时域内总 Joule 热单列 **Joule Heat Source** 并计入 Net Results。
- **42.4.7 其他体积源**：报告的平衡只含边界通量 + DPM 源 + 用户源——**不含其他体积源（如换热器模型换热）**，故收敛解可能显示不平衡 = 该体积源值。Radiation 报告的 Net Radiation Source = 发射 − 吸收的体积辐射源。

## 42.5 边界上的力（pp. 4373–4377）

Results → Reports → Forces → Edit...（Force Reports 对话框）：对所选壁面区计算沿指定向量的力、绕指定中心/轴的力矩、**压力中心坐标**（如翼型升阻比与压力中心）。Options 三选——**Forces**（Force Vector XYZ；**某分量为零时相应另两坐标之一可固定**）/ **Moments**（Moment Center XYZ + Moment Axis XYZ）/ **Center of Pressure**（2D 定义线、3D 定义面——固定一个坐标值：Coordinate 选轴 + Value）；Wall Zones 选区（可含 porous 区）；（可选）Save Output Parameter；**Print** 打控制台或 **Write...** 存文件。Forces 输出压力力/黏性力/总力与各系数（逐区 + 净值）；Moments 另给指定轴向分量；Center of Pressure 输出**压力力矩为零的坐标**（示例照录：翼型 Y=10 线上 X=0.41267981）。**Center of Pressure 不能存为输出参数**（是坐标组）。**重要：力/力矩系数依赖 Reference Values 任务页输入——必须填恰当参考值**。

## 42.6 投影面积计算（pp. 4377–4378）

Projected Surface Areas 对话框（Results → Reports → Projected Areas → Edit...）——算所选面沿 X/Y/Z 轴的投影面积（仅 3D）。步骤：Projection Direction 选轴 → 选 Surfaces → 设 **Min Feature Size**（要分辨的最小几何特征长度；不确定就用默认起步）→ **Compute**（结果在 Area 框与控制台）→ **精度提升**：把 Min Feature Size 减半重算，直至面积不再变化（或到内存上限）。

## 42.7 面积分（pp. 4378–4381）

Surface Integrals 对话框（Results → Reports → Surface Integrals → Edit...）：Report Type 二十一选（Area / Area-Weighted Average / Custom Vector Based Flux / Custom Vector Flux / Custom Vector Weighted Average / Facet Average/Minimum/Maximum / Flow Rate / Integral / Mass Flow Rate / Mass-Weighted Average / Standard Deviation / Sum / Uniformity Index（Mass/Area Weighted）/ Vertex Average/Minimum/Maximum / Volume Flow Rate）；Custom Vector 类定义矢量；多相选 Phase；非面积/流量类选 Field Variable；选 Surfaces；（可选）Save Output Parameter（**存 case 后读入生成等价报告定义**）；**Compute**（结果进数值框与控制台；Net = 所选面合计）；Write... 存文件。**注意**：质量平均偏向高速区（跨面质量多处）；**此处 Flow Rate 不如 Flux Reports 准**；**零面积面推荐 Facet/Vertex 平均**；**均匀性指数**（1 = 最均匀）——area-weighted 捕捉量的变化（如组分浓度）、mass-weighted 捕捉通量变化（如组分通量）。

## 42.8 体积分（pp. 4381–4382）

Volume Integrals 对话框（Results → Reports → Volume Integrals → Edit...）：Report Type 九选——**Volume / Sum / Sum*2Pi（仅 2D 轴对称）/ Maximum / Minimum / Volume Integral / Volume-Average / Mass / Mass Integral / Mass-Average**；非 Volume/Mass 类选 Field Variable；多相选 Phase；Cell Zones 选区（**列表含表达式体积；cell registers 不可用于体积分**）；（可选）Save Output Parameter；Compute（Net = 所选区合计）；Write... 存文件。

## 42.9 效率计算（pp. 4382–4385）

- **42.9.1 Device Efficiency**：Results → Reports → **Efficiency...**（Device Efficiency 对话框；控制台 `/report/efficiency`）——Inlets/Outlets 选面（列表只含支持类型）；**Type**：Isentropic 或 Polytropic；**Process**：Expansion 或 Compression；**Ratio**：Total to Total / Total to Static / Static to Static；可基于对话框输入定义命名表达式（Define；Expression Manager... 查看）；解已初始化/计算时 **Compute** 出值；Display 显示所选面。适用于各类可压贯通装置（扩压器/喷管/阀门等；叶轮机另有 Turbo Report 对话框——默认 Total-to-Total 恒 Cp/γ 等熵与多变效率；**Device Efficiency 的一般公式经 `/report/efficiency/use-in-turbo-report?` 用于 Turbo Report**；理想气恒 Cp 时两法几乎一致、其他工况只有 Device Efficiency 法合适）。
- **42.9.2 命名表达式法**：Named Expressions → New——**Functions → Reduction** 下 **EfficiencyIsentropic 与 EfficiencyPolytropic** 函数；Inlets/Outlets 参数可取混合类型多位置（多位置合并为平均后的单一入流/出流；cut-plane、iso-surface 与面组可用）；Process（Expansion/Compression）与 Ratio（TotaltoTotal/TotaltoStatic/StatictoStatic）参数。
- **42.9.3 限制**：仅可压流——理想气、单组分 real gas、湿蒸汽（Wet Steam）；支持位置清单照录（Pressure/Velocity Inlet、Pressure/Mass-Flow Outlet、Pressure-far-field、Inlet/Outlet Vent、Intake/Exhaust Fan、Interior、Interface、Cut-plane、Iso-surface、面组）；多进出口归并为平均单流股。

## 42.10 直方图报告（p. 4386）

控制台文本直方图（图形版见 41.11.8）——Histogram 对话框（Results → Plots → Histogram → Edit...）同流程但点 **Print**；输出区间计数与百分比（示例照录）。

## 42.11 离散相报告（p. 4386）

颗粒状态（位置/速度/直径/温度/质量流量）经 Sample Trajectories / Compute Erosion 对话框写到各边界与平面（2D 线）的文件——详见 Sampling of Trajectories（p. 2978）等。

## 42.12 S2S 信息（p. 4386）

查看区到区角系数与辐射发射值——S2S Information 对话框（详见 p. 2307）。

## 42.13 参考值（pp. 4386–4389）

控制派生物理量与无量纲系数计算所用的参考值（**仅用于后处理**）。用途——力系数：参考面积/密度/速度（压力力计算另用参考压力）；力矩系数：再加参考长度；Reynolds 数：长度/密度/粘度；压力与总压系数：压力/密度/速度；熵：密度/压力/温度；表面摩擦系数：密度/速度；换热系数：参考温度；叶轮机效率：比热比。
- **42.13.1 设置**：Setup → Reference Values 任务页——手动输入或 **Compute From** 选边界区按其条件计算（**依边界类型只有部分参考值会被设置；长度与面积须手动**）。可设量：Area、Density、Enthalpy、Length、Pressure、Temperature、Velocity、dynamic Viscosity、Ratio Of Specific Heats、Yplus for Heat Transfer Coefficient；2D 另有 **Depth**（报告通量/力与面积分/体积分相关量；**单位独立于 Length 设置**——报告前核对数值与单位）。
- **42.13.2 参考区**：多参考系/滑移网格时 Reference Zone 下拉选区——使速度（与总压、温度等）相对该区运动显示（详见 p. 1831）。

## 42.14 case 设置摘要报告（pp. 4389–4391）

- **42.14.1 Modified Settings Summary**：快速复查当前 case 的**非默认设置**表——树右键 Setup → List Modified Settings（子分支亦可，列表缩减）或 Solution ribbon（Run Calculation 组）Input Summary 下拉选 List Modified Settings；表随图形窗口打开为标签页；双击任一条目打开对应对话框修改；改设置后点 **refresh** 更新、点写按钮存文件。
- **42.14.2 Summary Report**：Solution → Run Calculation → **Input Summary...**（Input Summary 对话框）——Report Options 勾 Models / Boundary Conditions / Solver Controls / Material Properties → **Print** 到控制台或 **Save...** 存文本文件。

## 42.15 系统资源使用（pp. 4391–4394）

Parallel ribbon（System 组）**CPU Info** 下三报告（示例表照录）：
- **42.15.1 处理器信息**（CPU Info）：每台有计算进程的主机一行——Sock x Core（插座×核数、是否超线程）、Clock (MHz)、Load 负载、System Mem Total/Available (GB)；合计行。另有 **GPU Info**（CUDA 可见 GPU、runtime/driver 版本、每卡 SM 数/频率/显存）。
- **42.15.2 内存信息**（Memory Usage）：按节点与按主机两表——Virtual/Resident Mem Usage 的 Current/Peak (GB) 与 Page Faults（Windows：virtual = private bytes、resident = working set）。用于规划 Fluent 作业与机器、诊断性能问题。
- **42.15.3 进程与模型计时器**（Time Usage）：CPU Time Usage（User/Kernel/Elapsed）+ **Model Timers**（Host 与计算节点）+ **Performance Timer**（472 迭代示例照录——每迭代平均墙钟时间、全局规约次数与耗时、消息数、数据传输量、LE 求解次数与耗时占比、AMG 循环数、松弛扫描数、时间步更新等；Simulation wall-clock time 合计）。求解器计时说明见 Checking Parallel Performance（p. 4578）。

**Ch.42 全章完成（pp. 4325–4394）。**

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 4325–4360（批次 116，2026-10-20，pypdf layout 模式提取）。
- 42.1 的 Depth 与轴对称角度数值在文本层为符号占位（按惯例 1 m 与 2π，未照录具体符号）；报告文件格式与 Linux 隐藏文件告诫照录。
- Figures 42.1–42.22（对话框截图）为图形元素未摄取。
- 版本敏感：默认行为（Automatically Plot and File、1000 绘图点、Average Over 默认 1）与 2019 R3 前 Expression 定义的迁移告诫以 2026 R1 为准。
- 相关页面：[[Fluent 求解器使用]]（收敛条件用报告定义）、[[Fluent GPU 求解器]]（GPU 监视器限制）、[[Fluent 燃料电池]]（Reports 选项卡）。
