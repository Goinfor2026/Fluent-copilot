---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags:
  - Ansys Fluent
  - aeroacoustics
  - fw-h
  - wave-equation
  - broadband-noise
  - kirchhoff
  - sponge-layer
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 气动噪声模型

## 摘要

User's Guide 2026 R1 Part III / Chapter 24 "Predicting Aerodynamically Generated Noise"（PDF pp. 2725–2770，共 5 节）讲气动噪声计算。**本页全章完成（批次 75，pp. 2725–2770）**：24.1 三类方法概览（直接法、FW-H 积分法、波动方程法、宽带噪声源模型）、24.2 FW-H 声学模型（源面/接收器、ASD/CGNS 导出、on-the-fly、FFT 频带分析、GPU 求解器）、24.3 声学波动方程模型（源掩模与粘性海绵层、Kirchhoff 远场积分）、24.4 宽带噪声源模型、24.5 密度基海绵层。

## 24.1 概览（pp. 2725–2728）

- 三类方法：**直接法**、**混合法**（FW-H 积分 + 波动方程有限体积求解两种）、**宽带噪声源模型**。
- **24.1.1 直接法**：声波生成与传播都由流体方程直接求解——需时间精确解（DNS/URANS/LES 等黏性湍流方程）；**数值精度、网格（一直到接收器）、无反射边界要求高**；远场（如翼型数百弦长）计算代价不可行；**近场可行**（如舱内噪声——主要来自局部水动压力/pseudo sound）；通常解可压缩形式；仅低亚音速 + 近场伪声时可用不可压——**不可压处理无法模拟共振与反馈现象**。
- **24.1.2 FW-H 积分法**：中远场噪声预测；近场流动由 URANS/DES/SAS/SDES/SBES/LES 求得，经波动方程解析积分解预测声音（Lighthill 声类比；**FW-H 形式为其最一般形式 [46]——单极/偶极/四极声源**）；**时域积分形式**：在指定接收位置直接算声压时间历程（面对面积分）；需源（发射）面上的时间精确压力/速度/密度；**源面可为不可渗透壁面或内部（可渗透）面**——后者计及被包围的四极贡献；宽带与音调噪声均可预测；**支持多源面与多接收器；源数据可保存备用或"on-the-fly"边算边出声，或两者兼用；FFT 后处理算 SPL 与功率谱**。**重要限制：仅适用于声向自由空间传播——不能预测管道内或壁面封闭空间内的噪声传播**。
- **24.1.3 波动方程法**：低 Mach 数 aeroacoustics 混合仿真——不可压流动模型算声源、微分波动方程算传播；由 Ewert & Schroeder 声扰动方程 [44] 在**常密度假设**下导出。优点：①适用面比 FW-H 广（不限于开放空间）；②工作流简单——同一域同一网格瞬态联合仿真、无跨软件文件交换、无声源插值。
- **24.1.4 宽带噪声源模型**：无明显音调、声能连续分布的宽带噪声——用 RANS 统计湍流量 + 半经验关联式 + Lighthill 声类比定位声源。源模型：**Proudman 公式、射流噪声源模型、边界层噪声源模型、线性化 Euler 方程（LEE）源项、Lilley 方程源项**——量化单位面积/体积对总声功率的局部贡献、诊断主要噪声生成区域；**不预测接收器处的声音**；无需瞬态解（只要平均速度场、k、ε）——**计算资源需求最少**。

## 24.2 FW-H 声学模型（pp. 2728–2754）

- 两步流程：①时间精确流场解（获取源面上压力/速度/密度时间历程）；②用源数据算接收器声压信号。**Important：单一运动参考系的稳态模拟也可用 FW-H——运动噪声源产生的厚度与载荷噪声按 FW-H 积分计算（Theory Guide Eqs 11.5/11.6），其中表面压力时间导数项置零**。Fluent 用"**forward-time projection**"处理发射-接收时延——支持"on-the-fly"边算边出声。
- **流程七步**：①收敛流场解（瞬态算到"统计定常"——含主要流变量的统计不再随时间变化；监测特征点判断）；②启用 FW-H（Setup → Models → Acoustics → Edit）；③指定源面及源数据采集/保存选项（**稳态单 MRF：旋转面 zone 作为源面**）；④指定接收器；⑤瞬态继续算足够长时间并保存源数据；⑥计算并保存声压信号（Solution → Run Calculation → Acoustic Signals...）；⑦后处理（Results → Plots → FFT）。时间步长应小到能解析模型网格与湍流模型可复现的最小流动特征时间尺度。
- **24.2.1.1 模型常数**（Acoustics Model 对话框 Model Constants）：**Far-Field Density**（远场密度，Theory Guide Eq 11.1）；**Far-Field Sound Speed**（远场声速）；**Free Stream Velocity 与 Direction**（勾 **Convective Effects** 后出现——**Important：所有绕体外流强烈建议启用并正确设置**）；**Reference Acoustic Pressure**（SPL dB 计算参考声压；默认值在提取中缺失——24.2.6 节明确频带 SPL 用的标准声学参考压为 **2×10⁻⁵ Pa**）；**Number of Time Steps Per Revolution** 与 **Number of Revolutions**（仅稳态单 MRF——旋转 zone 转一圈的等效时间步数与模拟圈数）；**Source Correlation Length**（**2D 流动结果算声时必填**——FW-H 积分沿深度方向按相同源数据在该长度上积分）。默认值适用于大气常压空气声传播。
- **24.2.1.2 on-the-fly**：勾 **Compute Acoustic Signals Simultaneously**——不写源数据文件、逐步算声压信号，省大量磁盘；噪声计算相对瞬态流动的内存与耗时占比可忽略——**可单独用，也可与源数据导出并用**（后者用于判断信号何时统计定常、何时可停）；每时间步控制台打印 "Computing sound signals at x receiver locations..."；仅 FW-H 启用时可用。
- **24.2.1.3 源数据文件**：源数据采集是声学计算最耗时部分——**建议同时保存源数据**（可对新/追加接收器复用）。勾 **Export Acoustic Source Data in ASD Format** 或 **CGNS Format**（或都勾）；保存的流动变量按求解器选项（可压/不可压）与源面类型（壁/可渗透面）而异（**Table 24.1 的表体内容在提取中缺失**）。
  - **24.2.1.3.1 不启用 FW-H 导出 ASD（供 SYSNOISE）**：仍须指定源面（SYSNOISE 需要 .index 与 .asd 文件）；可用流体 zone 作发射源导出四极源——`define/models/acoustics/export-volumetric-sources?` → yes；SYSNOISE 还需源 zone 质心数据（`write-centroid-info` 导出）；风扇噪声可用柱坐标导出（`cylindrical-export?` → yes；默认笛卡尔）；**不需要声学模型参数与接收器；Compute Acoustic Signals Simultaneously 与 Acoustic Signals... 不可用**。
  - **24.2.1.3.2 不启用 FW-H 导出 CGNS（供 Simcenter 3D Acoustics）**：非可渗透面；Acoustics Sources 对话框 **Number of Time Steps per File 默认 1**；**限制：不能同时为多个不同转速旋转壁导出**（全部不转、或同轴同速；选不一致会导致声学结果错误——用户自行保证）；文件：网格数据 `<prefix>_mesh.cgns` + 每时间步解数据 `<prefix>_<timestep>.cgns`（含壁面面元心处静压），存于 `<directory_name>/<prefix>` 目录；四极源：`define/models/acoustics/export-volumetric-sources-cgns?` → yes（文件 `<prefix>_Q_mesh.cgns` 与 `<prefix>_Q_<timestep>.cgns`）。
- **24.2.2 源面**：Define Sources... → Acoustic Sources 对话框；可选多个发射面——**类型不限于壁面：内部面与滑移界面（静止与旋转）均可**。**Important：多源面用于分辨各面贡献——仅当面间声学相互作用可忽略时结果有效；任何源面不得包围其他源面**（FW-H 无法计及内表面对声音的遮挡 → 内面贡献被高估）。内部面作源面须预先生成且两侧 cell zone ID 不同，并**正确指定四极源所在的内部 cell zone**（决定声传播方向；弹出 Interior Cell Zone Selection 对话框）；滑移界面同理。**Important：选了可渗透面（内部面或滑移界面）后，被其包围的、发声的其他壁面不得再选**——on-the-fly 时声压被重复计入。
  - **24.2.2.1 保存源数据**：File Name（如 acoustic_examplexxxx.asd——xxxx 为全局时间步索引；另有 acoustic_example.index 索引文件）；**Write Frequency**（每 N 个时间步写一次；一般默认 1）；**Number of Time Steps per File**（分文件——如 100 则每文件 100 步；用于剔除尚未统计定常的初始段）；Apply 后生成索引文件。**Important：源数据可能占大量磁盘——ASD 选项启用时选源面时会打印每时间步磁盘需求**。
- **24.2.3 接收器**：Define Receivers... → Acoustic Receivers 对话框（Acoustic Sources/Acoustic Signals 对话框的 Receivers... 按钮亦可）；**Moving Receivers**——速度大小与方向作用于全部接收器；位置解释为"声发射起始时刻"的起点：on-the-fly 时 = Compute Acoustic Signals Simultaneously 激活的物理时刻；读文件时 = 首个所选源数据文件的物理时刻；**Important：换用不同源数据文件会因发射时刻起点不同而得到不同接收器位置**。Number of Receivers + 各接收器 X/Y/Z 坐标；**接收器应距声源合理距离（模型适合远场），可在计算域之外**；每接收器可设 Signal File Name 根名——**扩展名固定 .ard**；默认 receiver-1.ard 等。
- **24.2.4 时间步长**：隐式双时间步进——可每步写源数据或按频率因子放粗；**声学分析可复现的最高频率由所采集源数据的时间步长决定**；密度基显式（Explicit Transient Formulation）由 CFL 定步长 → FW-H 启用时可用**自适应时间步进**：Run Calculation 页设 **Time Step Size for Acoustic Data Export**——采样用恒定时间间隔，求解器在不违反 CFL 的前提下调整步长保证该间隔有数据（避免插值）。
- **24.2.5 后处理**：FFT 能力（FFT Postprocessing，p. 4301）与 Ansys Sound 分析（p. 4311）。
  - **24.2.5.1 写声学信号**：on-the-fly 数据存于内部缓冲——Acoustic Signals 对话框勾 **Write Acoustic Signals** 点 Write，逐接收器写出 receiver-N.ard。
  - **24.2.5.2 读非稳态声源数据算声**：Acoustic Signals 对话框流程：①选 Read Unsteady Acoustic Source Data Files；②Load Index File...（.index）；③在 Source Data Files 清单选 .asd 文件（**数量不限但只能选连续文件**）；④Active Source Zones 选源区；⑤Receivers 选接收器（可 Receivers... 追加）；⑥**Compute/Write**——逐接收器存 receiver-N.ard。**Important：同时启用 ASD 导出与 on-the-fly 时，须先 Write Acoustic Signals 再做 Read 计算——先 Read 会把 on-the-fly 数据从缓冲冲掉；做声学计算时随手存 case & data（on-the-fly 信号会存入 .dat）；写完 on-the-fly 数据后改接收器文件名再做 Read 计算，避免覆写**。计算与写声压信号**仅 FW-H 启用时可用**。
    - **24.2.5.2.1 信号自动修剪（auto-pruning）**：默认开启——保存前裁掉源信息不完整的信号首尾（源数据自 t0 制表到 tN；接收器自 Eq 24.1 时刻起收到最早信号（含最短源距），但直到 Eq 24.2 时刻才收到最远点贡献；尾部同理 Eqs 24.3–24.4；公式体未提取）；`define/models/acoustics/auto-prune` 可关闭——但应只用完整数据。
  - **24.2.5.3 静压时间导数**：**Surface dpdt RMS**（Acoustics... 类）——仅当壁面同时被标记为声源时可用（FW-H）。
  - **24.2.5.4 FFT**：Fourier Transform 对话框 Load Input File... 选 .ard；信号还在内存时用 **Process Receiver** 直接处理。
- **24.2.6 声源源 FFT：频带分析与表面压力谱导出**：瞬态仿真期间把声源面 zone 全部面元的瞬时表面压力时间历程写入 ASD 文件——主用途是 FW-H 求解器输入；**还可计算与可视化谱特性：单个 Fourier 模式 = 复幅值；频带 = 表面压力级 SPL（dB）与压力时间导数的量纲化功率谱密度 PSD**；支持恒定带宽与比例带宽（倍频程、1/3 倍频程）。**Note：此处 SPL 指 Surface Pressure Level（表面压力级），非声压级**。谱数据还可把流动压力复幅值表面场导出为 CGNS——作为分布激振力供 **Ansys Mechanical 谐响应分析**（Mechanical 侧导入功能 FLUREAD；用 Mechanical 声学波动方程求解器可做频域仿真，如外部湍流引起的车内噪声）。
  - **24.2.6.1 使用**：Run Calculation 页 **Acoustic Sources FFT...** 按钮出现条件——**3D 瞬态 + 启用 ASD 导出**。对话框四页：①**Read ASD Files**——Active Source Zones 与 Source Data Files 清单；Load Index File...（ASCII，含源区与 ASD 文件名清单）；Read 后控制台报告总步数/时间范围/步长；②**Compute FFT Fields**——Spectral Resolution 组显示统计特性（取决于采样率与信号长度）；**Clip Time to Range**（Min/Max 裁剪）+ Re-Estimate Spectral Resolution；Window Function（与单信号 FFT 相同选项；默认全信号 + Hanning 窗）；Compute 开始计算。**存储区（storage area）**：压力历程与谱场存于动态分配大内存数组——**Overwrite Signals by Spectra** 启用 = 谱取代原信号（重算须 Clean Up Entire Storage Area + 重读）；禁用 = 保留信号（Clean Up Only FFT Results 后可反复重算）；用完建议释放。**Point Probes for Time Signals**——在已读面上建点探针（Domain → Surface → Create → Point；探针取最靠近点面的面元心）；Print Coordinates；**Extract Signals** 输出 ASCII（默认 .dat，File Name 加前缀）供 Fourier Transform 对话框（Process File Data）分析；③**FFT Surface Variables**——由谱场创建 Fluent 变量（仅在已算 FFT 的壁面上非零；可用于云图——变量带 asfft 限注（Table 43.21）或导出 CFD-Post）。Modes/Frequency Bands：**Set of Modes**（逐模态——复幅值实部/虚部成对）；频带三种：**Octave Bands / 1/3 Octave Bands（标准技术倍频程）/ Constant Width Bands（自定义等距）**。Spectrum Property（频带）：**SPL 场（dB；默认参考压 2×10⁻⁵ Pa，可在 Acoustic Model 对话框改 Reference Acoustic Pressure）与 dp/dt 的量纲 PSD 场（单位 pressure²/time²）**。Create 时各频带的**面平均**带滤波 RMS 压力脉动以 dB 打印到控制台（先面平均后转 dB）；PSD 同理；仅打印谱覆盖到的频带；**Write Area-Avg Data** 写 ASCII XY 文件（建议 .xy 后缀）；**Plot Area-Avg Data** 画柱状图。容量：SPL 与 PSD 覆盖全部倍频程/1/3 倍频程带 + **至多 20 个恒定带宽** + **至多 20 个单频**的实/虚幅值；倍频程变量名含中心频率（如 "SPL for Octave Band at 250Hz (dB)"）；自定义频变量编号 0–19、Create 时控制台打印频率对照表；超 20 个分批处理 + Remove Selected Variables；两个 Clean Up 按钮同时删除已建变量；④**Write CGNS Files**——Processed Source Zones 选导出面；**Reduce Frequency Series**（Min/Max + Number of Frequencies to Skip——**慎用：宽带谱幅值依赖频率分辨率，跳频人为粗化分辨率且幅值不会自动重标**）；**Number of Frequencies per File**（谱可达数千频率 × 密集面网格 → 数据量大；总量 ≈ ASD 文件总量）；File Name（如 wall_pressure_spectrum → 生成 wall_pressure_spectrum.cgns（含网格 + 指向其余文件的 CGNS links）、_1.cgns、_2.cgns… 与 .flst（ASCII 频率清单）；**向 Mechanical 导入只需指定第一个文件**）；留空则命名 cgns、1.cgns…。**Important：File Name 不要带相对路径**（links 含路径 → 文件搬迁前不可读）；**Windows 下 CGNS 库对多 links 文件在网络盘上 I/O 极慢——导出与 Mechanical 导入都强烈建议本地盘/USB 盘**。
- **24.2.7 FW-H 与 GPU 求解器**：工作流同 CPU；**源数据文件扩展名 .asdg（非 .asd）**、按网格分区各写一个文件（并行输出加速）；**不能在 GPU 会话续写 CPU 导出**；载入 CPU 建的 FW-H 设置到 GPU 会话 → 索引文件不得含 .asd 行——推荐在 GPU 会话重访 FW-H 模型并在 Acoustic Sources 与 Acoustic Model 两对话框点 Apply（重建索引与求解器设置；接收器无需重设）。**限制**：①不支持 on-the-fly；②导出与声信号计算期间**不得更改网格分区**（定好分区后先把 case 写盘重读、再开始导出——确定面元的最终排序）；③不支持旋转参考系转子的稳态 FW-H；④.asdg 可用于静压场 FFT——但单独 GPU 会话做 FFT 时分区须与导出会话一致。

## 24.3 声学波动方程模型（pp. 2754–2764）

- **适用**：低 Mach 湍流的 scale-resolving 模拟（LES、SBES、DES、SAS）；**背景流体的密度与声速恒定——温度/组分不均匀引起的显著变化不允许**；建议读 Theory Guide "Preventing Non-Physical Reflections of Sound Waves"。**仅瞬态 + 二阶或有界二阶隐式时间格式；不支持 2D 轴对称**。启用：TUI `/define/models/acoustics/wave-equation?`；选项菜单 `/define/models/acoustics/wave-equation-options`。**Artificial Viscosity Factor for Sponge Layer** = Theory Guide Eq 11.13 的参数 C；人工黏度基准级经 `sponge-layer-base-level` 改；远场参数经 `/define/models/acoustics/far-field-parameters`。
- **24.3.1 源掩模与海绵区**：Acoustics Region 组；几何两法（可组合）：①**UDF**——`DEFINE_SOURCE_MASK(名, c, t)` 与 `DEFINE_SPONGE_LAYER(名, c, t)`（每模拟各仅一个；返回单个实数填充 SV_SOUND_MODEL_SRC_MASK / SV_SOUND_SPONGE）；②**基本形状**（长方体、圆柱、球）——先建 **Region 型 cell register**（Solution → Cell Registers → New → Region...），再在 Acoustics Model 对话框点 **Basic Shapes...** 把 register 加入源掩模或海绵层几何并逐形状设过渡厚度；**Note：register 一经用于定义，后续编辑/删除不影响已指定的几何**；TUI 菜单 `wave-equation-options/basic-shapes/`。可视化：Acoustics… 组的 **Sound WaveEq Model Source Mask** 与 **Sound Sponge Layer Marker** 场变量（直接输出存储变量）。**Note：本节海绵层属波动方程模型、基于黏度；压力基可压流另有基于密度的海绵层（24.5）**。
- **24.3.2 求解控制**：Solution Controls 页多出 **Acoustics Wave Equation Solver Controls** 框：**Relative Convergence Criterion 与 Max Iterations/Time Step** 控制隐式波动方程求解器的子迭代（源于 Eq 11.11 基本 Laplac 项离散的显式偏斜修正与人工黏度项）；每次子迭代 AMG 线性解器把残差范数降 0.1 倍（rp 变量 `acoustics-waveeq/amg-alpha`）；三参数最优值与网格质量相关、默认值未来版本可能调整。TUI `/solve/set/acoustics-wave-equation-controls/`（`/expert` 子菜单可为低质量网格设欠松弛——正常不建议）。
- **24.3.3 初始化**：波动方程在时间相关流动解发展**之后**启用——声学场需**单独初始化**（声源项随时间 ramping，Eq 11.11）。Solution Initialization 页出现 **Sound Potential** 场（**初值恒保持 0**）与 **Initialize Acoustics...** 按钮 → Acoustics Initialization 对话框设 ramping 时间步数；声学场可随时单独重初始化（不影响继续的瞬态流动解）；TUI `/solve/initialize/init-acoustics-options`。**Note：在未初始化的设置上启用波动方程 → 整体初始化会连带初始化声学且 ramping 时长为 0——须单独重初始化声学；DEFINE_INIT 型 UDF 不能用于初始化波动方程模型——改用 DEFINE_ON_DEMAND**。
- **24.3.4 后处理**（Acoustics… 组）：**Sound Pressure**（主要实际量；经 Eq 11.12 与声势相连；因数值微分比声势场粗糙）、**Sound Potential**（主解变量）、**Sound DP/Dt**（声压时间导数 = 主变量的二阶导；可能多噪声）、**Sound WaveEq Model Source**（原始源项）、**Sound WaveEq Model Source Smoothed**（时间滤波后）、**Sound WaveEq Model Source Mask**、**Sound Sponge Layer Marker**；也可用 Ansys Sound Analysis 对话框。**Note：Source 与 Source Smoothed 不含源掩模与 ramping 效应——要看施加后的源场用高级输出场 Sound WaveEq Source（`/solve/set/advanced/retain-temporary-solver-mem` yes 启用）**。
- **24.3.5 Kirchhoff 积分模型**：3D + 波动方程模型下可用；Acoustics Model 对话框勾 **Remote Receivers** → 出现 Kirchhoff Integral Options 子框。**Integration Surface...** 列出现有面——最有用的两类：**二次曲面**（Domain → Surface → Create → Quadric）与**等值面**；**当前只能选一个面**作积分面。**Define Receivers...** 打开与 FW-H 相同的 Acoustic Receivers 对话框——**两模型共享接收器、无需设两遍**；Kirchhoff 信号扩展名固定 **.ark**。**Write Signals** 把远场接收器信号写 ASCII——**恒自动修剪**；信号太短（不含完整声压数据）则不写并告警。**Important：Moving Receivers 仅 FW-H 支持（Kirchhoff 忽略）；两模型的信号在内存与 data 文件中分开存储（可同时用、可对比），但 ASCII 文件共用用户根名、以扩展名区分（.ard / .ark）**。**Kirchhoff 目前仅 "on-the-fly" 模式**（每时间步后算下一组信号样本）；FW-H 的 read-and-compute 模式使同一瞬态仿真可同时服务 FW-H 与波动方程（含 Kirchhoff）：①选 Wave Equation + 勾 Export Acoustic Source Data in ASD Format 与 Remote Receivers；②Define Sources... 指定 FW-H 积分面；③Integration Surface... 指定 Kirchhoff 积分面；④瞬态中每步解波动方程 + Kirchhoff 推进远场接收信号 + FW-H 导出 ASD；结束后 Write Signals；⑤切到 FW-H 模型 → Run Calculation → Acoustic Signals... 用 ASD 文件算 FW-H 信号。TUI：`wave-equation-options/` 下 basic-shapes/、remote-receivers-options/、remote-receivers?、source-mask-udf、sponge-layer-base-level、sponge-layer-factor、sponge-layer-udf、time-filter-source?；`remote-receivers-options/` 下 integration-surface、write-signals。

## 24.4 宽带噪声源模型（pp. 2764–2766）

- 流程三步：①算稳态或非稳态 RANS 解；②启用宽带噪声模型（Setup → Models → Acoustics → Edit → **Broadband Noise Sources**）；③后处理噪声源（Contours）。
- **24.4.1.1 模型常数**：Far-Field Density 与 Far-Field Sound Speed（同 FW-H）；**Reference Acoustic Power**（Theory Guide Eq 11.19；声功率 dB 输出参考值；默认值提取缺失；**2D 单位 W/m²、3D 单位 W/m³**）；**Number of Realizations**（SNGR 法算 LEE 与 Lilley 方程平均源项的样本数；**默认 200**）；**Number of Fourier Modes**（Theory Guide Eq 11.39；构造湍流速度场及其导数以算 LEE/Lilley 源项；**默认 50**）。
- **24.4.2 后处理**（Acoustics... 类）：Acoustic Power Level (dB)、Acoustic Power、Jet Acoustic Power Level (dB) 与 Jet Acoustic Power（**仅轴对称模型**）、Surface Acoustic Power Level (dB)、Surface Acoustic Power、Lilley's Self-/Shear-/Total-Noise Source、LEE Self-/Shear-/Total-Noise X-Source、Y-Source、Z-Source（**Z 系列仅 3D**）；亦可用 Ansys Sound Analysis 对话框。

## 24.5 密度基海绵层（pp. 2767–2769）

- 用途：**压力基求解器的单相可压瞬态模拟**中消除边界区非物理压力波反射——把邻近边界 zone 的一层域指定为海绵层，层内密度从求解器值按**二次混合函数**混向用户指定的远场值（ramping 长度自海绵层内边界向边界延伸、越靠边界远场值权重越大）。**是黏度基海绵层（仅波动方程模型可用）与边界声学波模型（NRBC 等）之外的替代方案**。**Note：不支持多相模型**。
- **设置六步**：①General 页 Solver Type = **Pressure-Based**；②Time = **Transient**；③Create/Edit Materials 定义可压缩流体（ideal-gas / real gas / compressible-liquid）；④**Physics → Models → Acoustics → Sponge Layers...** → Manage Sponge Layers 对话框 → **New...** → Sponge Layer 对话框：Name；**Far-Field Density**（建议用整个仿真中边界处的平均密度）；**Ramping Distance**（密度从求解值过渡到远场值的距离；**建议为 Total Thickness 的 80–100%**）；**Total Thickness**（从所选边界到海绵层内边界的距离；**建议至少为预期压力波波长的 2 倍**）；**Boundary Zones** 选应用边界；OK（可重复建多个；**新建的层自动激活**）。Fluent 按单元到海绵层边界 zone 的距离标记单元；**多个激活层重叠时打印警告，并把重叠区单元划给内边界最远的那层**。Manage 对话框可 Edit / Activate / Deactivate / Delete。⑤建议在边界附近设静压 XY 图解算动画以检验反射消除效果。⑥初始化后可后处理（Mesh... 类）：**Sponge Layer Distance**（层内单元到内边界的距离；内边界 0 → 边界 zone 处等于层厚、线性变化）、**Sponge Blending Function**（0 = 用求解器密度，1 = 用远场值）。

## 证据与适用条件

- 页码：pp. 2725–2769 为正文；**p. 2770 为空白版权页**。目录范围 pp. 2725–2770 全部覆盖，**Ch.24 全章完成**。
- **公式**：Eqs 24.1–24.4（auto-pruning 起止时刻）公式体未提取，按周边文字记录语义（含最短源距与声速）；Reference Acoustic Pressure 与 Reference Acoustic Power 的默认数值、Table 24.1 源数据表体在提取中缺失（参考压 2×10⁻⁵ Pa 经 24.2.6 节交叉确认）。
- Figures 24.1–24.24（对话框截图与曲线示例）为图形元素未摄取；正文引用的 Theory Guide 式号（11.1–11.19、8.45）与 Eq 41.15 未展开。
- 默认值（Write Frequency 1、Number of Time Steps per File 1、PDF 无关、Hanning 窗、参考压 2×10⁻⁵ Pa、20 频带/20 模态上限、SNGR 200 样本/50 Fourier 模态、海绵层 ramping 80–100% 厚度与 ≥2 倍波长、AMG 残差降 0.1 倍、Sound Potential 初值 0）为 2026 R1 手册记载，随版本可能变化。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]
- [[Part III - Solution Mode]]
- [[Fluent 湍流模型设置]]（LES/DES/SAS/SBES 等 scale-resolving 模型；Ch.16）
- [[Fluent Cell Zone 与边界条件设置]]（NRBC 边界声学波模型对照；Ch.8）
- [[Fluent 叶轮机械流动]]（旋转参考系源面；Ch.15）
- [[index]]
