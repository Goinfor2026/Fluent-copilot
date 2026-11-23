---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - gpu-solver
  - native-gpu
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent GPU 求解器

## 摘要

User's Guide 2026 R1 Part III / Chapter 38 "Using the Fluent Native GPU Solver"（PDF pp. 3905–3974，14 节）。**本页全章完成（批次 106–107，pp. 3905–3974）：38.1–38.14 全 14 节——平台与启动、重映射与异步输出、支持特性全清单（模型/材料/求解器/DPM/边界条件与表达式表）、监视器与报告定义、EnSight DVS 导出、Arm 部署、限制清单、疑难排除、性能排查。**GPU 求解器为原生 GPU 版 Fluent——较传统多核 CPU 计算最高 **5 倍**速度。

## 38.1–38.2 引言与支持的 GPU/驱动（pp. 3905–3906）

- 原生 GPU 求解器，单/多 GPU（Fluent Launcher 或命令行指定）；GPU 高带宽内存适合计算密集型流动。
- **NVIDIA**：CUDA **12.8+**、驱动 **570+**；最低硬件 **Pascal** 代；驱动不兼容时须升级（`nvidia-smi` 检查；下载 developer.nvidia.com/cuda-downloads）。**AMD**：ROCm **6.0+**（更新见 amd.com ROCm hip-sdk）。

## 38.3 基本流程（p. 3906）

CPU 解算模式的许多特性 GPU 求解器尚不支持——设置必须遵守支持特性（38.9）与限制（38.10）。八步：定目标 → Launcher/命令行指定 GPU → 读 3D 网格或 case（±data）→ 设模型/材料/单元区/边界/报告定义 → 设计算活动 → 计算（稳态/瞬态流程同 CPU 求解器，p. 3778/3782）→ 检查保存结果 → 视需要修改设置。

## 38.4 启动（pp. 3906–3911）

- **Launcher**：Capability Level 须选 **CFD Enterprise 或 CFD HPC Ultimate**（**GPU 求解器仅此两许可级**）；Solution + **Native GPU Solver** 选项；多 NVIDIA GPU 时勾选要用的 GPU ID（`nvidia-smi` 查 ID；**每增加一个 GPU 需一个额外 CPU 进程**）；指定 AMD GPU 只能命令行（`-gpu=1,2,4`）；CPU Processes ≥ GPU 数（仅用于设置与后处理）；可直接选 Case/Case and Data/Mesh/Journal 启动。**性能建议**：GPU 数与 CPU 数相同起步；大算例可多用 CPU（前后处理）但不做 GPU-Remapping 会有性能损失。
- **命令行**：Windows 先运行安装目录 `fluent\ntbin\win64` 下 setenv.exe；Linux 图形驱动自动选（需要时 `-setenv="HOOPS_PICTURE=<driver>"`）。`nvidia-smi` 列出 GPU（ID 0–7）。启动命令：`fluent 3d -t<n> -gpu`（单精度）；**3ddp** 双精度；**3ddp -gpu_hybrid_precision** 混合精度（性能与内存优于双精度）。`<n>` 语义：单 GPU 机 = 仅 CPU 进程数；多 GPU 且 n < GPU 数 = n CPU + n GPU（按 nvidia-smi 顺序取）；n ≥ GPU 数 = n CPU + 全部 GPU。**LSF/PBS/Slurm 调度**：`-scheduler=<scheduler>` + **-scheduler_gpn=<x>**（每节点 GPU 数）与 -t（总 GPU 数）联合指定多节点（例：-t32 -scheduler_gpn=16 = 两节点各 16 进程）。手动指定 GPU：`-gpu=ID,...`。
- **38.4.3 CPU/GPU Remapping**：默认**一对一**映射（每 CPU 分区对应一个 GPU 实例；建议 CPU 数 = GPU 数以免 GPU 内存过载）。**多对多重映射**（Launcher Parallel Settings 的 **GPU Remap** 选项或命令行 **-gpu_remap**）把全部 CPU 分区分配给同一机器内独占 GPU 的进程——减少跨机数据传输/网络开销时有益。**不支持**：DPM 或声学模型启用时（启用即回退一对一）；与 **-gpu_async** 同用且 case 有需要 GPU 数据下载的 Execute Commands 时。
- **38.4.4 异步输出（-gpu_async）**：改善后处理监视、动画渲染、自动存 case/data、自动导出数据时的求解性能。CPU/GPU 负载比 1 时增益最大；**Cortex 收敛判定时 GPU 求解器（迭代更多）一并宣布收敛**，Cortex 追平数据并补做后处理（两种收敛声明都打印）。**限制**：与 -gpu_remap 同用且 case 有需下载 GPU 数据的 Execute Commands 时不支持；**仅 Intel MPI（-mpi=intel）支持**——Microsoft MPI 与 Open MPI 不支持。

## 38.5–38.8 退出/GUI/CPU 进程/case 读入（pp. 3912–3913）

- 退出：File → Exit 或右上角按钮（确认框）。
- GUI 与 Fluent Solution Mode 相同，**不支持的特性在 GUI 中隐藏**。
- **CPU 进程用于设置与后处理**：大算例（大量 cell zone）可用多 CPU 进程并行缩短设置与后处理时间；读入网格后按 Mesh Partitioning and Load Balancing（p. 4546）分区；**开始计算时设置用分区合并为每 GPU 一个分区**。
- **读入 CPU 求解器 case**：Fluent 尝试**转换**不支持的特性、不可转换的**默认禁用**，控制台打印转换/禁用表（例：WFGC on→off、残差缩放 global→local、初始化参考框 relative→absolute）。启动计算时若有残留不支持项（如无效报告字段）会列明细并停止，直至处理。应确保 case 只含 GPU 求解器支持的特性。

## 38.9 支持的特性（pp. 3913–3940+）

一般要求：单块或多块 NVIDIA GPU（共享/分布式内存）；单/双精度；多 CPU 进程做设置与后处理；多对多重映射可用；**仅 3D**；网格拓扑支持 polyhedral/hexahedral/tetrahedral/pyramid/prism 与悬挂节点网格。
- **38.9.1 模型**：
  - **CHT**（含各向异性固体；**Loosely Coupled CHT 不支持**）；**DO 辐射**（可与非绝热 FGM 燃烧组合）；**S2S 辐射**；**Shell Conduction**（限制：半透明边界不支持、与多相不支持、与 FGM 燃烧不支持——原文拼写照录 combusion）。
  - **组分输运**（体积反应或无反应）：Finite-Rate/No TCI 与 Eddy-Dissipation 湍流-化学交互；Stiff Chemistry Solver 与 None-Direct Source 化学求解器；层流/EDC/PDF 输运可在分区权重选项卡开 Stiff Chemistry 促进负载均衡。
  - **FGM 火焰面流形模型**；**可压流**。
  - **湍流**：Laminar；Standard 与 Realizable k-ε；**GEKO（Wall Distance Free 公式）与 k-ω SST**（两者支持代数转捩与曲率修正、表格化近壁处理）；**LES**（亚格子 Smagorinsky-Lilly 与 WALE；选项 Near-Wall-RANS-Layer（WMLES——主体 LES + 近壁代数 RANS；近壁处理默认基于 r+ 的调和混合壁面函数）与 Use 2nd Cell Off A Wall Quantities（自动判断回退第一格））；**SBES**（仅配 k-ω 族）；代数转捩；曲率修正；适用模型的 Viscous Work。
  - **FW-H 声学**（专节 p. 2753）；**海绵层声学**（**仅支持单个海绵层**——多个激活时只模拟第一个、其余忽略）。
  - **叶轮机械**：整叶轮与多排；TRS 滑移网格；FR 多旋转参考系；多排周期扇区（含 Periodic Instancing，FR 与 TRS 均可）。
  - **38.9.1.1 电势模型**：仅固体区；壁面电压/电流密度（时变值、接触电阻）；耦合边界（含接触电阻）；Joule 热（含分区 joule heating）。
  - **38.9.1.2 电池模型**：CHT Coupling 求解法；Joule Heat in Passive Zones 能量源；**电池 ROM 工具包**（p. 3494）；热滥用模型（一方程 Arrhenius 型、四方程、N 方程、内部短路反应）。
  - **38.9.1.3 DPM**：**仅瞬态颗粒追踪**（流求解器稳态/瞬态皆可）；瞬态流动时颗粒在注入 Start/Stop Time 窗口内每个流动时间步开始时注入——**DPM 包由 CPU Fluent 求解器生成后上传 GPU，颗粒求解器执行时不会重新生成**（surface 注入的 Randomize Starting Points 给随机初始位置但每次注入不变）。与连续相交互：单向/双向（Interaction with Continuous Phase）；耦合时源项进动量/能量/组分——FGM（非）绝热时为混合分数源、详细组分模型（组分输运+体积反应）时为直接组分源；耦合控制——DPM Iteration Interval（一个流动时间步内多次追踪）与 Update DPM Sources Every Flow Iteration。注入类型五种：single/group/surface（面心随机分布）/file（**仅稳态**）/cone（全类型）。颗粒类型：Massless/Inert/Droplet。直径分布：uniform/rosin-rammler。物理模型（多为 injection 级）：拖曳仅 **spherical**；破碎仅 **SSD**（气动液滴破碎——不生成子液滴、改父液滴直径与包内液滴数守恒质量；默认参数 Critical We = 6、Core B1 = 1.73、Xi = -0.1、Target NP = 10，Set Injection Properties 可调）；对流换热；重力/浮力；湍流扩散仅 discrete-random-walk（**Number of Trys 固定 1、Time Scale Constant 固定 0.15**）。**蒸发/沸腾条件**：颗粒类型 Droplet、单组分材料、启用组分输运或非绝热 FGM、仅 convection/diffusion-controlled 汽化模型、蒸发/沸腾切换按材料蒸气压；**Pressure Dependent Boiling 与 Temperature Dependent Latent Heat 为 GPU 求解器专属选项**；**"DPM Laws" 概念不可用**；蒸发组分 Binary Diffusivity 可 constant/piecewise-polynomial/**film-averaged**（默认 1/3 规则、Averaging Coefficient 可在 0–1 任取）。
- **38.9.2 材料属性**：Density——piecewise-linear/piecewise-polynomial/polynomial/ideal-gas/incompressible-ideal-gas/boussinesq/constant；Cp——constant/piecewise-linear/piecewise-polynomial/polynomial/kinetic-theory/mixing-law；导热——constant/piecewise-linear/piecewise-polynomial/polynomial/kinetic-theory/**cyl-orthotropic/orthotropic/anisotropic**（CHT 各向异性固体）/**mass-weighted-mixing-law**；粘度——constant/piecewise-linear/piecewise-polynomial/polynomial/kinetic-theory/sutherland/mass-weighted-mixing-law；分子量/标准态焓/标准态熵/参考温度——constant；质量扩散率——constant dilute approximation/kinetic-theory；电导率——constant/piecewise-linear/piecewise-polynomial/polynomial/**expression**。
- **38.9.3 求解器设置**：**压力基 + 绝对速度公式**，稳态与瞬态。压力-速度耦合：**Coupled（仅稳态）** 或 segregated **SIMPLE/SIMPLEC**——Coupled（稳态）支持 CFL-based 与 pseudo transient（Global Time Step）两种时间步进；Flux Type——Rhie-Chow momentum based（默认）或 distance based（Optimized LES Numerics 时自动激活）。空间离散：梯度 **Least Squares Cell Based**；流动方程一阶/二阶；压力另可 Linear 与 Body Force Weighted；LES/SBES 时动量与能量可用 **Bounded Central Differencing**（可调 Boundedness）与动量 **Low Diffusion Central**（可调 Diffusion Coefficient 与 Shield BL Distance）。不可压瞬态：一阶/二阶隐式与 Bounded Second Order Implicit 瞬态格式——二阶类格式有 **Use limiter in time** 选项（改善瞬态热仿真的有界性）；瞬态 CHT 开能量时 Run Calculation 出现 **Specify Solid Time Step Size**；Coupled + Pseudo Time Off 时可设 Flow Courant Number；**Set Optimized LES Numerics** 按钮（LES 时）。支持 poor mesh numerics 与 poor mesh removal——removal TUI `solve/set/poor-mesh-robustness/poor-mesh-removal/enable? yes`（删除左旋面单元）+ `orthogonal-quality-threshold` 可调；numerics 同路径 enable + threshold。稳态支持 Data Sampling for Steady Statistics。**控制台消息 "coupled-pseudo-transient" 上下文停用提示可安全忽略**。
  - **38.9.3.1 Optimized LES Numerics**：每时间步迭代数常可降（**两步常足够**）；连续残差第二步不降时**减时间步优于加迭代**（成本相近且更准）。Solution Methods 选 LES 后出现 Set Optimized LES Numerics 按钮；激活后：URF——高质量网格可高 URF（**动量 0.95、压力 1.0 默认**；低质量网格或发散时降低）；**常密度两步/时间步、ideal gas 五步通常足够**；Low Diffusion Central 对流算子——中心格式重构速度 + 基于“常数（原文符号缺失）与解光滑度指示器”的双三阶偏置重构跳项引入迎风（Eq 38.1；**不恢复一阶迎风、非 TVD——不能捕捉激波**）；压力格式——线性重构（按单元几何加权；拉伸笛卡尔二阶、斜网格退化一阶；**与 CPU 实现不同——仍只依赖邻单元压力但非均匀网格更准**）；质量流量离散——默认 **distance-based** 通量格式（配低扩散中心对流时含 Rhie-Chow 压力耗散的面对质量流量离散按 LES 低迭代数调优）。
- **38.9.4 DPM 求解器设置**：颗粒追踪**仅 High-Res Tracking**；**重心（barycentric）插值**把速度/湍流量插到颗粒位置——密度与粘度默认取单元中心值（随位置变化时建议也插值）；数值方法不可改：颗粒位置 **trapezoidal Euler**、动量与能量 **一阶隐式 Euler**、组分与质量 **显式 Euler**；颗粒积分步长由 Step Length Factor 定；**Accuracy Control 不可用**；耦合仿真 **Linearize Source Terms** 可用（动量/能量/组分源）。
- **38.9.5 参数化研究**：支持对受支持参数的**顺序**更新（p. 4617）。
- **38.9.6 单元区与边界条件**：边界条件可定义为常量或输入参数；部分设置还可用**稳态 profile**（**质量流量与旋转壁面 Speed 不支持输入参数与稳态 profile**）。支持的边界条件：进口——velocity-inlet（超音速入流仅 ideal gas）、pressure-inlet（同）、mass-flow-inlet（同）、intake fan、inlet vent；出口——pressure-outlet（超音速出流仅 ideal gas）、mass-flow-outlet、outlet vent、exhaust fan；pressure-far-field；symmetry；壁面——无滑移、**Zero Specified Shear（自由滑移壁）**、热条件、壁厚热条件；periodic（平移/旋转）；非一致界面（流-流/流-固/固-固、旋转与平移周期性、匹配与非匹配界面）；porous jump；internal fan；**边界区单个海绵层**。不可压与可压流都支持的边界：velocity-inlet、mass-flow-inlet、mass-flow-outlet。流体单元区条件：Frame Motion（MRF）、Mesh Motion、Solid Motion、Porous Zone、源项（热/动量/组分——常量或稳态 profile）、组分反应机理、3D Fan Zone。
  - **38.9.6.1 Profiles and Expressions**：profile——**steady profiles**（求解器无关）与 **transient profiles（beta）**；表达式三类——**parametric**（依赖设计变量的数值，如 `100 [rad/s]`）、**static**（初始化时完全求值，如 `1-x^2 - y^2`；parametric 为 static 子集）、**dynamic/时变**（随求解动态求值，如 `(1-x^2 - y^2)*VolumeAve(u, ['fluid'])`、`(1-x^2 - y^2)*sin(t)`）。**注意**：下述表格之外（Species/Combustion/Radiation 等）不支持表达式与 profile——但 Combustion、Momentum、Energy、Viscous、Electric Potential 模型的**报告定义与非稳态统计**支持表达式（p. 3961）；表格中表达式支持的域仅限该节所列字段。Table 38.1（材料/单元区条件——流体：密度 parametric、导热/粘度/UDS 扩散率 all expressions + **Python UDF（beta）**、电导率 all expressions；固体：密度 parametric、导热/电导率 constant）；Table 38.2（操作条件 Gravity 三分量——constant/parametric/时变/Python UDF beta）；Table 38.3（动量单元区——Frame Motion 轴原点/方向 constant+parametric、转速 constant/parametric/时变（流体另有时变）、Mesh Motion 全字段 +Python UDF beta、源项 constant/all profiles/all expressions/Python UDF、Fixed Values 仅 constant、3D Fan 与 Porous Zone 仅 constant）；Table 38.4（动量边界条件——Velocity Inlet 各方向定义方式的逐字段可用类型，**表格自 p. 3933 起、跨至下段**）。

## 38.9.6（续）Table 38.4–38.13 摘要（pp. 3941–3955）

- **Table 38.4（动量边界条件，续）**：Velocity Inlet 各定义方式逐字段——Magnitude/Normal：常量/all profiles/all expressions，Supersonic/Initial Gauge Pressure 常量/parametric；Cartesian 与 Cylindrical 的 Velocity Magnitude 同上、Flow Direction 常量/steady profiles/static expression（Local Cylindrical 为 spatial profiles）、Axis Origin/Direction（邻单元区或本地）常量/parametric；**Intake Fan/Inlet Vent/Outlet Vent/Exhaust Fan**——Gauge Total Pressure（constant/all profiles/all expressions）、Supersonic/Initial Gauge Pressure（constant/parametric）、Flow Direction（constant/spatial profiles/static expressions）、Axis Origin/Direction（constant/parametric）、**Pressure Jump / Loss Coefficient / Pressure Profile Multiplier**（constant + polynomial/piecewise-linear 等函数式）；**Wall（Moving Wall）**——Translational 与 Rotational 的 Speed/Direction/轴原点/方向、Components 三分量：constant/parametric/**时变表达式**。**注意三条**：同一速度分量组不能 profile 与 expression 混用；一分量给 transient profile 则其余两分量也须 transient profile；Axis 与 Origin 须 constant 或 parametric。
- **Table 38.5（能量单元区）**：Source Terms Energy——constant/all profiles/all expressions/Python UDF（beta）；Fixed Values Temperature——**不支持**。**Table 38.6（能量边界）**：各进出口 Total/Backflow Total Temperature（constant/all profiles/all expressions ±Python UDF）；Wall——Heat Flux、Wall Thickness（constant）、Heat Generation Rate、Temperature、HTC、Free Stream Temperature、External Radiation Temperature、External Emissivity（均 constant/all profiles/all expressions）。
- **Table 38.7（黏性模型单元区）**：全部 N/A。**Table 38.8（黏性模型边界）**：各进口/远场的 k/ε/ω（constant/all profiles/all expressions）与 Turbulent Intensity/Length Scale/Viscosity Ratio/Hydraulic Diameter（constant/all expressions）；Pressure Outlet N/A。**Table 38.9–38.13**（组分、电势单元区/边界、VOF 边界）同 pattern 逐字段列出。
- **38.9.6.2 DPM 边界条件**：支持 inlet/outlet/wall/symmetry/（非）一致平移或旋转周期界面；进口/出口/壁面的颗粒边界类型 **reflect/escape/trap**；**非一致界面非重叠区的壁面只支持 reflect**（Wall DPM 选项卡可设该区恢复系数）。

## 38.9.7 解算监视器与报告定义（pp. 3956–3961）

- 注意：用监视器/报告定义时开 **-gpu_async** 提升性能；**Iso-clips、Zone surfaces、Quadric-surfaces 三类自定义面上不能建监视器**；不支持变量的报告定义在运行时输出 **0 值**（求解器未运行时手动 Compute 则在 CPU 上正确求值）。
- 报告定义可建于既有边界面或 Point/Plane/Line/Iso-surface；**支持基于报告定义值的收敛条件（Convergence Conditions）**；稳态与非稳态监视器的 plot/print/write 均支持。类型：**Force**（Drag/Lift/Moment/Force）、**Flux**（Mass Flow Rate/Total Heat Transfer Rate/Electric Current Rate）、**Surface**（Area/Area-Weighted Average/Facet Average/Facet Max/Min/Flow Rate/Integral/Mass Flow Rate/Volume Flow Rate/Mass-Weighted Average/Sum/Standard Deviation/Uniformity Index 两式/Vertex Average/Min/Max）、**Volume**（Mass-Average/Mass Integral/Mass/Max/Min/Volume/Volume-Average/Volume Integral/Sum）、**Expression**（仅限网格中实际存在并被求解器使用的边界面与单元区——自定义面与点不支持）。**告诫**：内部区上只有 Mass Flow Rate 能正确报告（其余为 0）——需要其他量的内部报告改用 plane surface。
- 支持的场变量类别：Pressure（静/动/总/压力系数）、Density、Velocity（三分量/Q Criterion Normalized/Lambda 2）、Temperature（静/总/总能/总焓/焓）、Turbulence（k/ε/湍流粘度/ω）、Materials（导热/层流粘度/Cp/分子粘度）、Wall Fluxes（近壁 HTC/壁面剪切应力/总表面热流/Yplus HTC）、Wall Statistics（Mean Heat Flux）、Species（质量分数/平均混合分数/进展变量及其方差族）、Radiation（入射辐射/吸收/散射系数/六种辐射通量）、Mesh（x/y/z 坐标）、Potential（电位/Joule 热源/三个电位梯度）。
- **38.9.7.1 DPM 后处理**：Mass-in-domain 监视（当前颗粒质量 kg 或变化率 kg/s）；Injected/Escaped/Evaporated-mass 监视——**按流动求解器时间步给出质量或流量**（与 CPU 求解器在追踪期内积分的定义不同）；颗粒采样仅在面区与用户定义平面（后处理曲面/平面不支持）；**所有注入的颗粒都被采样——Sample Trajectories 的 Release From Injections 选择被忽略**；Pathlines 可显示但**由 CPU 求解器计算**。
- **38.9.7.2 表达式与报告定义/非稳态统计**：表达式可直接输入/用命名表达式/引用既有报告定义/组合；支持域——坐标（单元与面质心 x/y/z）、时间（Time/Flow-Time/Delta-Time）、流动热力（密度/五种压力/静温/速度三式/比总焓/比总能）、材料（MolecularMass/SpecificHeatCapacity/MachNumber/SpeedOfSound）、湍流（k/ε/k 生成/四种粘度导热/Prandtl 两式）、反应与燃烧（进展变量族/FiniteRateSource/TurbulentFlameSpeedSource/混合分数族/组分三式/TFMOmega/反应热/放热率/NOx 三式/层流火焰速度厚度/TFM 增厚与效率因子）、电磁（电位及梯度/电导率/三向电流与模/Joule 热源）、多相（VOF 的 Density/DensityAll/Volumefraction）、UDS（UDS/UDSDiff）。**Table 38.14 支持的运算与函数**——Operators（+−*/、** 与 ^ 幂、比较与不等）、Conditional（AND/IF/NOT/OR/XOR）、双曲六函数、数学（abs/ceil/erf/erfc/exp/floor/log/log10/pow/sqrt/trunc）、Reduction（Area/AreaAve/AreaInt/Average(Weight=None|Area|Volume|Mass|MassFlowRate)/Centroid/Count/CountIf/MassAve/MassFlowAve/MassFlowAveAbs/MassFlowInt/MassInt/Maximum/Minimum/PressureForce/Sum(Weight)/SumIf/Volume/VolumeAve/VolumeInt）、三角九函数。**Table 38.15 科学常数仅四个**——PI、e、R（8.314472 J K⁻¹ mol⁻¹）、g（9.8066502 m s⁻²）。表达式报告定义引用的既有报告定义须为：Flux 的 Mass Flow Rate；Surface 的 Area/Area-Weighted Average/Facet Average/Facet Max/Min/Flow Rate/Integral/Sum；Volume 的全部。
- **Table 38.9–38.13**（组分/电势/VOF 边界条件等）沿用 constant/all profiles/all expressions 逐字段 pattern（摘要）。

## 38.9.8 EnSight DVS 导出（pp. 3965–3967）

与 CPU 求解器的差异：导出更快；**只能导单元中心、不能导节点**；**不能导自定义面**；计算中导出**只能建一个导出定义**；导出文件中的变量名可能与 CPU 版不同（体积分数与相属性等）。事后导出：File/Export/Solution Data... → File Type 选 **EnSight DVS** → 选 Cell Zones/Surfaces/Quantities → Write...；TUI `file/export/ensight-dvs`（标量条目以 q 结束；示例照录）。瞬态中自动导出：File/Export/During Calculation/Solution Data...（Export Data Every 下拉 + 文件名）或 TUI `file/transient-export/ensight-dvs`（示例照录：每 2 时间步、前缀 myfile）。自动导出时同样建议开 -gpu_async；与 CPU 版相同的限制——重复面不能导出、所选单元区相邻面区自动纳入。**重要**：开始 EnSight DVS 自动导出前必须建好全部所需报告定义——导出开始后不能再建/删报告定义（EnSight 需要完整残差与报告定义历史）。

## 38.9.9 Arm 上运行（p. 3967）

支持 NVIDIA GPU + Arm 计算节点：向 Ansys 支持申请 **Fluent for Arm（aarch64）与 Client** 两个包，解 tar 后按序运行 `Fluent_install-lnarm64-26.1.0.sh` 与 `Client_install-lnarm64-26.1.0.sh`（同一安装路径）；推荐 **Rocky Linux 8.9 / RHEL 8.8 / 9.3**（前置库 libICE/libnsl2/libSM/pcre2-utf16）；再设环境。

## 38.10 GPU 求解器限制（pp. 3968–3971）

- 不支持的模型/设置在 GUI 中隐藏或名称加 **Unsupported**；**TUI 仍可设置（为 journal 兼容）**——TUI 启用的不支持项被列为 ignored/converted/unsupported；CPU case 通常可跑、不支持项同样标注。
- **DO 辐射限制**：不支持 Solar Load、DO/Energy Coupling、Wall Temperature (Thin) 后处理、表达式/UDF 辐射属性；**方向索引 GPU 与 CPU 不一致**——方向变量后处理 GPU/CPU 对比可能有差异。
- **不支持单独的壁面湍流 Prandtl 数**（默认用 Energy Prandtl 数）；**Workbench 环境不可用**。
- 报告定义间隔是残差 reporting interval 的倍数（如 reporting 5 × 导出 3 步 = 实际每 15 步才收到数据）——**GPU vs CPU 性能对比建议 reporting interval 20**（`/solve set report-interval 20`）。
- **圆柱坐标 profile（含旋流进口）不支持**；监视器与报告定义必须在初始化或计算前定义；稳↔瞬切换可能需重定义报告定义。
- 非一致界面质量流量监视符号可能错误（-1 代 1）；静止壁的 Dynamic Pressure 报告（输出参数式）会给出错误的非零值。
- **热效应 case 用稳态解初始化瞬态在解能量方程时不正确**——按 38.11 流程过渡；**混合初始化 + 远场压力边界可能不收敛或在出流面产生非物理初速——改用标准初始化**。
- 指定剪切壁只支持**零剪切应力**（并自动移除该壁湍流壁面函数效应——同 CPU 的 specified-zero-shear-alternative-treatment）。
- **封闭域（无压力边界）+ 不可压 + 非瞬态**：CPU 把最近参考位置单元压力置零，GPU 改为**保持初始压力的体积平均**——CPU/GPU 解之间存在压力偏移（此类流动压力水平本任意，但可能影响非封闭体的力积分）。
- **二阶瞬态重启**：重启后第一个时间步用一阶 Backward Euler；**GPU 解转回 CPU 求解器重启**：GPU 解中算过"可压材料 + 能量方程"时不能正确重启。
- 流动方程关闭时其他方程继续更新但**残差不更新**；Linear 压力格式与 CPU 不同（仍只依赖邻单元压力、非均匀网格更准）；CHT 固体 + coupled pseudo-transient 稳态——固体隐式伪时间步为无穷（同 CPU 默认但 GPU 无 GUI 覆盖项）；**GPU 稳态默认不用 coupled pseudo-transient**（GUI 可选）；**组分最多 20 种**。
- 表达式为**显式**（用上一场变量）；周期/对称区及任何内部区（fan/interior/porous jump/radiator/RANS-LES interface/双侧壁）不支持表达式；**表达式只支持有限单位集**（温度 K/C/R/F、角度 rad/deg/rev、rpm、浓度 kmol/mol/lbmol、时间 Hz/s/sec/min/h、长度 m/cm/mm/km/in/ft、fraction 与 %、功率 W/hp、压力 Pa/atm、力 N/lbf/kgf/dyn/dyne/tonf/ozf/pdl、质量 kg/g/lbm/lb/slug、能量 J/kgf·erg/kWh/BTU/cal/kcal、速度 mph、体积 gal/l、电压 V/A/S——照录）。
- **compressible-liquid 密度法的流体混合物不兼容组分输运**；**FGM 不兼容多孔介质与 frame motion**。
- **38.10.1 DPM 限制**：稳/瞬态流动求解器皆可但**颗粒只能瞬态**；颗粒采样不能按注入区分（GUI 子集被忽略）；**仅限静止网格**——不支持非一致界面；**零厚度壁（baffle）勿与 DPM 同用**（壁附近结果不准）；GUI 限制为支持项但 **TUI 无限制——建议用 GUI 设置 DPM 以免误启不支持项；经 TUI 启用不支持项可能崩溃并完全丢失数据**。

## 38.11 稳态转瞬态（p. 3971）

常规四步：按稳态设置 → 算稳态解 → General 任务页改 Transient → 算瞬态解（规避 38.10 所述热效应初始化限制）。

## 38.12 疑难排除（pp. 3971–3972）

五步：①核对模型/边界/求解器设置均在支持清单内（读入 case 时确认转换完成）；②线性求解 Diverged/Stalled（AMG (energy/solver/solve) It n, Diverged.）——提高 AMG verbosity 观察残差史（残差先降后滞=未必是设置问题；持续上升=非线性收敛差、解不可靠）；**coupled 求解器可对耦合流动系统在 Advanced Solution Controls 开 BCGSTAB 稳定化**；③降 URF——SIMPLE 稳态建议 **压力 0.2、动量 0.4、全部湍流量 0.4**（可能减慢收敛）；④空间离散二阶改一阶（对湍流精度损失可忽略）；⑤检查并改善网格质量/左旋面——重建或 `/mesh/repair-improve/improve-quality`。

## 38.13 性能问题排查（pp. 3972–3973）

单 GPU：`nvidia-smi` 确认 GPU 空闲模式；`/solve set report-interval 20`（推荐 20）；残差图异常时开 AMG verbosity 查线性求解是否正常走满 50 个最大循环。多 GPU 在此之上：**每 GPU 至少 200 万单元**（过小算例多 GPU 反而慢）；`/parallel/partition/print-active` 查负载均衡——不佳则 `/parallel/partition/method metis` + `/parallel/partition/use-stored-partitions`；`/parallel/bandwidth` 与 `/parallel/latency` 查 GPU 间通信——**最优带宽 5 GB/s、延迟 1e-6**（解读见 p. 4580）。

## 38.14 GPU 内存占用（p. 3974）

GPU 内存消耗取决于 case 规模……（节起于 p. 3974 末行，正文跨至下章前——本章至 p. 3974 止，实际内容极短，照此记录）。

**Ch.38 全章完成（pp. 3905–3974）。**

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3905–3940（批次 106，2026-10-20，pypdf layout 模式提取）。
- Eq 38.1（低扩散中心算子面重构）公式体未提取，按语义记录；Table 38.1–38.4 摘要照录（Table 38.4 跨段，续于批次 107）；SSD 参数、DPM 固定数值格式、材料属性清单照录。
- Figures 38.1–38.2（映射示意）及对话框截图为图形元素未摄取；nvidia-smi 示例输出照录。
- 版本敏感：CUDA 12.8/驱动 570/ROCm 6.0、许可级（CFD Enterprise/HPC Ultimate）、模块命令与路径（v261）以 2026 R1 为准。
- 相关页面：[[Fluent 求解器使用]]（CPU 求解器对照）、[[Fluent 离散相模型（DPM）]]（DPM 细节）、[[Fluent 电池模型]]（ROM 工具包）。
