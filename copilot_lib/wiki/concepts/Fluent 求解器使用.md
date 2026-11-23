---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - solver
  - pressure-based
  - density-based
  - amg
  - nita
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 求解器使用

## 摘要

User's Guide 2026 R1 Part III / Chapter 37 "Using the Solver"（PDF pp. 3709–3904，24 节）。**本页全章完成（批次 102–105，pp. 3709–3904）：37.1–37.24 全 24 节——求解器选型、离散、压力基/密度基设置、AMG/FAS、解限值、梯度限制器、初始化三法、稳态/瞬态与自适应时间步进、伪时间方法、远程与云计算、收敛监视与条件、自动初始化、动画、case 检查、收敛稳定性与 Solution Steering。**理论见 Theory Guide "Solver Theory"。

## 37.1 求解器总览（pp. 3709–3713）

- **两大求解器**：pressure-based（传统用于不可压/弱可压）与 density-based（为高速可压设计；implicit/explicit 两种公式——**隐式稳定性更宽故稳态收敛快、显式省内存**）。两者现已都适用宽范围流动，但密度基出身使其对高速可压流动（激波分辨率）有精度优势。
- **压力基两种算法**：segregated（方程顺序求解）与 coupled（动量+连续方程耦合求解——**收敛显著更快、内存更多**）。选型考虑：模型可用性、给定流动条件的求解器性能、网格规模与内存。
- **模型可用性清单**：**仅压力基**——空化、VOF、Mixture 多相、Eulerian 多相、非预混/预混/部分预混燃烧、Composition PDF、Soot、Rosseland 辐射、熔化/凝固、shell conduction、浮动操作压力、Fixed Variable 选项、多孔介质物理速度公式、流向周期流动指定质量流量；**仅密度基**——Wet Steam 多相模型。
- **选求解器**：General 任务页（Setup → General）。通用流程 11 步：①（压力基）选压力-速度耦合 → ②选空间离散格式（+压力插值格式）→ ③（压力基）选多孔介质速度法 → ④选梯度选项 → ⑤设 URF → ⑥（密度基显式）设 FAS 多重网格 → ⑦按所用模型章节建议调整 → ⑧开监视器 → ⑨初始化 → ⑩开始计算 → ⑪收敛困难时查 Convergence and Stability（p. 3888）。**前三项默认值适合多数问题**。

## 37.2 空间离散格式选择（pp. 3713–3722）

- **梯度三选**（Solution → Methods 的 Gradient 下拉）：Green-Gauss Cell Based、Green-Gauss Node Based、Least Squares Cell Based。粘性项自动二阶；**默认**：单相（两求解器）流动方程与全部标量方程二阶迎风、**湍流量一阶迎风**；**多相流动方程默认一阶迎风**。
- **一阶 vs 二阶**：流动与网格对齐（矩形管道层流+四边形/六面体网格）一阶可接受；斜穿网格一阶增大数值扩散（numerical diffusion）——tri/tet 网格流动永不对齐，**一般用二阶**；一阶收敛更好但精度差（tri/tet 上尤甚）。多数算例可直接二阶起步；高马赫数初场差时可先一阶几步再切二阶（或用 FMG 初始化从二阶起步）；二阶收敛困难时试一阶。
  - **一阶-高阶混合因子**：TUI `solve/set/numerics` → blending factor（0–1）——0 退化为一阶、1 恢复完全高阶；<1（典型 0.75 或 0.5）使对流更扩散、稳定原本不稳定的解；**前提是 Solution Methods 中该变量已选高阶格式**。
- **其他格式**：**QUICK**（仅四边形/六面体网格；混合网格中只对 quad/hex 单元生效、其余单元二阶迎风）与**三阶 MUSCL**（全网格类型）对旋转/旋流可能更准——一般二阶足够。**Bounded Central Differencing 与 Central Differencing** 仅限 LES/DES/SAS/SBES/SDES 湍流模型；central differencing 只在网格足够细（局部 **Peclet 数 < 1**，Eq 37.1 = ρuL/Γ）时使用；BCD 的 Boundedness 可给常量或表达式；VOF 另有 modified HRIC。
- **压力插值格式**（压力基）：多数单相用 Second Order；**PRESTO!** 推荐高旋流数、高 Rayleigh 数自然对流、高速旋转流、强弯曲域——网格尺寸敏感时可用 `solve/set/advanced/boundary-presto-treatment?` **只在流动边界（含壁面/进口/出口）施加 PRESTO!**；**Body Force Weighted** 推荐大体积力问题；**Eulerian 多相默认 PRESTO!**（multi-fluid VOF 非迭代求解器：斜网格 Second Order 更稳、大体积力+斜网格 BFW 更稳）；**VOF/Mixture：PRESTO!（默认、最全面）或 Modified Body Force Weighted**（对网格与时间步尺寸不敏感；推荐非迭代求解器与大体积力；可用于 BFW 严重受限的高粘旋转流）。
- **密度插值格式**（压力基单相可压）：二阶迎风默认；一阶更稳但抹平激波——**含激波可压流用二阶迎风或 QUICK（quad/hex/混合网格推荐全变量含密度用 QUICK）**；MUSCL 任意网格减小数值扩散。多相时密度格式作用于可压相、不可压相用算术平均。
- **HOTR（高阶项松弛）**：改善高阶离散的启动与整体求解行为、防收敛停滞——**替代"先一阶后二阶"策略**；Solution Methods 开 High Order Term Relaxation；Options 对话框：Type——**Standard**（默认，对流+扩散项都松弛）/ **Convection Only**（只松弛对流项——可能加深加速收敛，如稳态叶轮机械 SST k-ω）；范围——**Flow Variables Only**（默认：速度分量/压力/能量/密度/湍流量（不含 Reynolds 应力）/体积分数）或 **All Variables**（每个高阶离散变量都松弛）；**Relaxation Factor 默认稳态 0.25、瞬态 0.75**（所有方程同一因子）。**限制**：NITA 开启时不可用；瞬态可用但需增加每时间步迭代数以保证原收敛判据；选 QUICK 的方程不做欠松弛。
- **User Inputs**：Solution Methods 每个标量方程下拉——First Order Upwind / Second Order Upwind / QUICK / Third-Order MUSCL /（LES 系模型动量）Bounded Central Differencing（默认）或 Central Differencing；压力插值 Standard/PRESTO!/Linear/Second Order/Body Force Weighted/Modified Body Force Weighted——**PRESTO! 低阶公式**：`solve/set/numerics` → limit high-order terms for PRESTO! pressure scheme? yes——**压力基耦合算法下 PRESTO! 不收敛或压力场出现非物理振荡（wiggles）时稳定用**；Density 格式仅可压流出现；VOF 体积分数格式五选——Geo-Reconstruct/CICSAM/Modified HRIC/Compressive/QUICK；组分可逐个设或勾 **Set All Species Discretizations Together** 统一；Default 按钮恢复默认。**告诫：壁面附近阶梯式棱柱网格勿将 node-based 梯度与 MUSCL 同用**。

## 37.3 压力基求解器设置（pp. 3722–3738）

### 37.3.1 压力-速度耦合

- **segregated 四种**：SIMPLE、SIMPLEC、PISO、Fractional Step（FSM，仅 NITA 瞬态）；**Coupled**。segregated 每迭代快、coupled 迭代数少——**稳态一般推荐 coupled**；瞬态 coupled 最稳健（大时间步尤甚），小时间步 SIMPLEC/PISO/NITA 总时间可能更快。稳态与瞬态默认选择不同（切换后不一定保留所选）。
- 欠松弛机制：pseudo time method（瞬态 coupled 不可用）或 Courant 数（仅 coupled）。**Coupled + pseudo time 为以下默认**：稳态、单相、无电池/燃料电池模型、无熔化凝固模型。
- **SIMPLE vs SIMPLEC**：SIMPLE 为瞬态默认；**SIMPLEC 压力修正 URF 可设 1.0 加速**——高斜率网格可能不稳，此时增加斜率修正迭代、用保守 URF（至 0.7）或改 SIMPLE；复杂流动（湍流/附加模型）只有当收敛受压力-速度耦合限制时 SIMPLEC 才有优势，否则两者相当。
- **PISO**：**带 neighbor correction 强烈推荐所有瞬态**（大时间步尤甚——动量与压力 URF 可 1.0 仍稳定）；LES（小时间步）用 PISO 反而贵，考虑 SIMPLE/SIMPLEC；稳态无优势。**斜率修正**推荐高畸变网格稳态/瞬态都用；仅 skewness correction 时动量+压力 URF 之和为 1（如压力 0.3/动量 0.7）；两者同用则按 neighbor 建议全给 ~1.0；高畸变网格可关闭默认的 Skewness-Neighbor Coupling。
- **FSM**：NITA 下比 PISO 略省；VOF 类问题可能不如 PISO 稳；极复杂问题（动网格/滑移界面/VOF）压力松弛可降到 0.7–0.8。
- **Coupled**：单相稳态更稳健高效；**NITA 不可用**；**porous jump 边界条件下 coupled 可能出现调参无效的收敛问题——改用 segregated**。
- 设置：PISO 的 Skewness/Neighbor Correction 迭代默认各 1（置 0 关闭该项）；Skewness-Neighbor Coupling 默认开（更经济略欠稳健）；SIMPLEC 斜率修正迭代默认 0；**增强斜率修正公式** TUI `solve/set/advanced/skewness-correction-enhanced`（SIMPLEC/PISO 且有斜率修正迭代时生效——极斜网格提高稳健性；若降稳则降 URF、（PISO）关 S-N 耦合；不影响收敛解精度）；**Local Time Step** pseudo 方法（SIMPLE/SIMPLEC/PISO）→ Pseudo Time Courant Number 默认 **5**；Coupled 瞬态或 pseudo Off → **Flow Courant Number 默认 200** + Explicit Relaxation Factors（动量/压力默认 **0.5**）——极斜网格可降 0.25；AMG 立即发散 = CFL 过高需降（**低于 10 不建议——不如用 segregated**）；多数瞬态 coupled：CFL 大至 1e7、显式松弛 1.0；Global Time Step pseudo 方法 → 设 Pseudo Time Explicit Relaxation Factors。

### 37.3.2 质量通量类型（Flux Type）

- **Rhie-Chow: momentum based**（动量系数加权高阶速度插值 + RC 压力梯度修正——多数工况）与 **Rhie-Chow: distance based**（距离加权）；**Auto Select 默认开**——仅"瞬态 + SRS 模型 + 可压流体 + 自适应网格（手工自适应/预置自动判据/hexcore 或 poly-hexcore 含悬挂节点）"组合自动选 distance based。时间步计算后自动选择不会因补设自适应而改变；改变时间离散/材料可压性/湍流模型类型时可能切换（有 Information 对话框提示）。手动控制需关 Auto Select。**湿蒸汽以外的多相模型无此列表、固定用 momentum based**。

### 37.3.3 欠松弛因子

- 压力基所有方程都有 URF；密度基只有顺序求解的方程（湍流等标量）有。默认近最优——强非线性问题（某些湍流、高 Rayleigh 自然对流）初期宜调小。**良好实践：默认起步；前 4–5 迭代残差持续上升则降 URF**。改 URF 前先存 data 文件；给算法几步适应；残差跳几个量级 → 停止、回最近好档。粘度与密度逐迭代欠松弛；焓公式（非预混燃烧）温度更新也欠松弛。Default 按钮显示默认值。**失稳/发散时把压力/动量/k/ε 降至约 0.2/0.5/0.5/0.5**（SIMPLEC 通常无需降压力）；密度-温度强耦合（极高 Rayleigh 数自然/混合对流）再欠松弛温度方程和/或密度；弱耦合（常密度）温度 URF 可 1.0；其他标量（旋流、组分、混合分数与方差）起步可降至 0.8。组分 URF 可 Set All Species URFs Together 统一。**coupled 算法最优性能：提高标量方程（如湍流）松弛因子至默认之上**。

### 37.3.4 非迭代求解器（NITA）控制

- 用途：瞬态提速；多相准稳态也可用非迭代多相求解器得稳态解。设置：Solution Methods →（不选 Coupled）→ 勾 **Non-Iterative Time Advancement** → 压力速度耦合方案：单相或 VOF/Mixture——Fractional Step 或 PISO（PISO 的 Neighbor Correction 可设、skewness correction 自动以压力方程收敛为目标）；**Eulerian 多相——只能 Phase Coupled SIMPLE**。LES 可开 **Accelerated Time Marching**（非反应、常密度：Max. Corrections 压力 0/其余 1、耦合改 Fractional Step、压力多重网格 F-Cycle+终止判据 0.01；**限制：Eulerian 多相不可用、不适合可压/变密度、动量建议用 BCD 而非 CD**）。
- 显式松弛：Solution Controls 的 Non-Iterative Solver Relaxation Factors 列表；失稳对策——单相：压力松弛降至 0.7–0.8 + 减小时间步；多相：显式压力松弛可降至 0.5（差网格尤其有益）、其余变量 0.8–1.0、可压多相密度 0.5–0.8、传质工况汽化质量 0.5–0.8。
- **Advanced Solution Controls（Expert 选项卡）**：**Max. Corrections**（每方程子迭代硬上限）、**Correction Tolerance**（当前子迭代残差/首个子迭代残差之比阈值）、**Residual Tolerance**（最后一个子迭代的 AMG 循环持续到残差/时间步初始残差低于该值）——默认为二阶精度设计；Residual Tolerance 默认适合单元 CFL 1–10（CFL<<1 应调小、CFL>>1 可能因舍入达不到需调大）；可后处理显示 Cell Courant Number。
- **Hybrid NITA**（VOF/Mixture）：Solution Methods → NITA Options → **Hybrid NITA**——**Aggressive（默认，每时间步 2 个外迭代）/ Conservative（3 个）**；设置自动优化一般无需改。**Instability Detector**（发散时启用）：Maximum CFL 默认 **25**、Maximum Velocity Magnitude 默认 **1000 m/s**——超限视为不稳定事件、该时间步增加外迭代并内部调整。高级控制 TUI `solve/set/multiphase-numerics/advanced-stability-controls/hybrid-nita/`：set-cfl-type（Global/Interfacial）；initial-outer-iterations（默认前 5 个时间步各 5 外迭代；大于 outer-iterations 时覆盖之）；unstable-event-outer-iterations（默认 5）；outer-iterations（复杂工况可增——耗时增加；残差报告每外迭代显示两个残差）。
- **策略**：一般不要改 NITA 显式松弛因子与专家控制（不当收敛会积累误差）；发散时——开不稳定性探测器并调参、Hybrid NITA 用 Conservative、压力松弛降至 0.5、减时间步、强方程间耦合（传质/可压/高粘）用 Conservative、Mixture 滑移速度可单独给显式松弛。NITA 专家命令：`solve/set/nita-expert-controls/set-verbosity`（子迭代诊断）、`skewness-neighbor-coupling`（PISO 时启用 S-N 耦合）。
- **模型兼容性**：兼容——无粘（ ideal gas 除外）、层流、全部湍流模型（含 LES/DES）、S2S 辐射、传热、非反应组分输运、一般可压（多数亚音速与部分跨音速）、VOF（多数应用）、Mixture、Eulerian、相变（凝固熔化）、多孔介质（各向同性阻力）、Multi-Fluid VOF、多相 RSM；可能有不稳定/不准——RSM、MDM（原文如此）、非牛顿流体、跨音速航天、反应组分与各类燃烧（含 PDF）；**不兼容**——S2S 以外辐射模型、DPM/spark/crevice、UDS 输运、porous jump、各向异性多孔、RSM 湍流模型、浮动操作压力。**PRESTO! + NITA 比迭代式更不稳——可能需更小时间步**；瞬态精度非重点（一阶时空）或 NITA 收敛向稳态时，可在 Expert 选项卡把压力以外方程的 Max. Corrections 设 1 省时。

### 37.3.5 方程顺序

瞬态压力基可设方程求解顺序：`solve/set/equation-ordering`——standard（默认）或 **optimized-for-volumetric-expansion**（密度强烈依赖热效应/化学组成时推荐，如燃烧）；多相模型下不可用。

### 37.3.6 动量离散修正形式

默认启用修正形式（Correction Form）——大源项方程数值更稳、单精度可行性更高、coupled 求解器更快更稳、与密度基 coupled 更一致。可经 `solve/set/advanced/correction-form` 关闭（**未来版本将移除该命令**）。

## 37.4 密度基求解器设置（pp. 3739–3749）

Solution Methods 可选：Formulation（Implicit/Explicit）、Flux Scheme（Roe-FDS/AUSM/Low Diffusion Roe-FDS）、空间离散精度、稳态加速选项（**Pseudo Time Method 仅隐式**；CASM）、High-Speed Numerics；瞬态——一阶/二阶隐式（显式公式另有显态瞬态式）。Solution Controls：显式——Courant 数、FAS 多重网格层级、残差光顺；隐式——Courant 数；两者——其他方程（湍流等）URF。

### 37.4.1 Courant 数

- CFL 是时间步进主控（时间步 ∝ CFL，Theory Guide Eq 23.89）；CFL 尽量大（许可范围内）收敛快。
- **显式**：多级格式理论上稳定至 CFL ≈ 2.5（实际常更低——非线性）；默认 **1.0**，一般不超过 **2.0**；发散时降——起动可低至 **0.1–0.5**，起动瞬态消退后再升。
- **隐式**：理论无条件稳定、非线性限制实际；默认 **5.0**，可视复杂度升至 10/20/100 甚至更高；起动期可低、随进程升高。**coupled AMG 自检测多重网格发散**：自动降 CFL 重试该迭代（**最多 5 次**），成功后恢复原值并打印消息。
- **CFL 报告定义**：密度基隐式稳态自动创建（solution steering 或防发散激活时跟踪用）；右键 Include In → Report Plots/Files 画图/存文件。
- 设置：Solution Controls；Formulation 切 Explicit/Implicit 时 CFL 自动置 1/5。

### 37.4.2 对流通量类型

**Roe-FDS**（默认、多数工况推荐）；**AUSM**（接触与激波间断精确解析、更不易 Carbuncle 现象）；**Low Diffusion Roe-FDS**（SRS 湍流模型 + 隐式时可用；降低湍流计算耗散；**仅亚音速**）。注意：SRS 模型和/或声学计算推荐 **Roe-FDS + 流动方程 BCD**（比 Low Diffusion Roe-FDS 更稳健且同样准确；非 SRS 用户需先 `solve/set/advanced/show-all-discretization-schemes` 才能选到 BCD）。

### 37.4.3 拉伸网格收敛加速（CASM）

密度基隐式稳态、高度拉伸各向异性网格（外流气动）——Solution Methods 勾 **Convergence Acceleration For Stretched Meshes**。TUI `solve/set/convergence-acceleration-for-stretched-meshes/` 设 **CFL 乘子截断**（默认 **100**；收敛困难时降到 50/20/10）。机理：局部单元 CFL 按单元长宽比放大（至截断值）——远离壁面（长宽比≈1）即用户 CFL、近壁拉伸单元成倍放大；**典型 CFL 5–10 即可**（无需标准法的大 CFL）。默认显式松弛 0.5（`solve/set/advanced/explicit-underrelaxation-value` 可调）。保守化手段：降 CFL、降显式松弛、降乘子截断。**非常激进——良好初场至关重要，推荐 FMG 初始化**。**与 Pseudo Time Method 互斥**（二选一）。优势尤见于低 y+（≈1）拉伸网格；会改变所选通量格式的数值耗散——监测载荷可能与不开时略有差异。
- **增强 CASM**：TUI 中第一问答 no、第二问 **Use enhanced CASM formulation? yes**——长宽比公式在高长宽比网格更稳健、对流动拓扑变化更敏感、与初场无关；显式欠松弛默认 **0.75**；提示信息：强烈建议 FMG 初始化、最大收益在流动与网格拉伸对齐时。

### 37.4.4 高速数值（High-Speed Numerics）

密度基内置定制数值设置，稳定并加速高速流动收敛（详见 p. 2394）。

### 37.4.5 局部欠松弛防发散（Divergence Prevention）

局部发散征兆：个别单元温度/压力反复触及 Solution Limits 上下限（控制台告警）——先核查尺寸/边界条件/物性，可用场变量 cell register 标记触限单元。设置正确仍发散时启用防发散：`solve/set/divergence-prevention/enable?` yes → Fluent 识别局部发散单元并冻结其压力/温度（URF 型因子置 0）、对其他变量欠松弛——**默认其他变量欠松弛因子 0.1**（无效则将因子向 0 减小）。注意：仅小比例单元触限可继续算；比例较高建议从初始化重启。

### 37.4.6 显式松弛

密度基隐式改善某些工况稳态收敛：`solve/set/advanced/explicit-underrelaxation-value` 输 0–1。

### 37.4.7 FAS 多重网格

**仅密度基显式公式**（隐式 AMG 恒开）。几乎总有益——计算前设非零粗网格层级。**不能与显式时间步进同用**（粗网格修正破坏细网格时间精度）。层级数：多数问题 **4 或 5** 起步；大 3D 可加（受内存限制——每层需额外内存）；疑似多重网格致收敛问题则减层。达到只含 1 单元的粗层即提前停止。设置：Solution Controls 的 Multigrid Levels 或 Advanced Solution Controls → Multigrid 选项卡 Max Coarse Levels（两者联动）；层级在首次迭代时创建——迭代一步后用 Domain → Info → Size 查各层单元数。
- **残差光顺**：隐式残差光顺（Jacobi 迭代）放宽时间步限制、可提 CFL——Iterations 默认 0（关）；设 1+ 后填 Smoothing Factor：**0.5 因子 + 2 道 Jacobi 通常足以让 CFL 翻倍**。

### 37.4.8 轴对称流动的轴稳定化

提高 axis 边界附近稳定性与精度——高速轴对称钝体尤其有用；开 high-speed-numerics 时自动启用；TUI `solve/set/axisymmetric/axis-stabilization?` yes 手动开。

## 37.5 代数多重网格（AMG）参数（pp. 3749–3758）

多数情况无需干预。默认：**flexible cycle 用于除压力修正外的所有方程**（压力修正用 V cycle）；flexible cycle 通常在细层做 5–10 次松弛、少访问粗层——不足则增大细层最大松弛数或改 V cycle。压力基 segregated：压力修正 V cycle、**最大循环数默认 30**——不足改 W cycle（Multigrid 选项卡 Fixed Cycle Parameters 的 Max Cycles 可加大；W cycle 效率可能下降）。压力基 coupled 与密度基隐式：**流动修正默认 F cycle**；密度基显式流动修正默认 V cycle。

- **37.5.1 循环类型逐方程**（Multigrid 选项卡下拉 Flexible/V/W/F）：segregated——压力 V、能量 F、其余 flexible；coupled——流动与能量 F、其余标量 flexible；密度基两公式标量均 flexible。
- **37.5.2 终止与残差缩减参数**：flexible cycle——**Restriction criterion**（残差缩减容差，Eq 23.131；决定何时访问更粗层；值越大粗层访问越少）与 **Termination criterion**（Eq 23.132；决定何时回更细层）。V/W/F cycle——Termination 决定细层是否再来一个循环；Restriction 不使用。
- **37.5.3 稳定化方法**：AMG 分片常数插值。固定型循环（F/V/W；密度基流动修正除外）可改稳定化方法——**BCGSTAB、RPM、GMRES**（BCGSTAB/GMRES 可带预条件；比 AMG 更稳更稳健）。适用：强离对角系数系统（如多相空化）；并行中 AMG 收敛可用 BCGSTAB/GMRES 预条件改善。**建议先试 BCGSTAB——GMRES 更稳健但内存与耗时更高**。能量方程常驻 BCGSTAB：Preferences → Simulation → **BCGSTAB for Energy Equation**。压力基 segregated 不可压另有 **CG**（共轭梯度，仅压力方程；对称矩阵；常配 AMG 预条件；内存与浮点运算少于 BCGSTAB；LES/NITA 中压力修正占总计算量大头）。检测到 AMG/BCGSTAB/CG 发散时自动以备用方法迭代一次并提示 "equation is being stabilized"——流动相关方程反复出现该提示说明需修改 Solution Methods/AMG 控制。
- **37.5.4 其他 AMG 参数**（Scalar Parameters vs Coupled Parameters——密度基隐式与压力基 coupled 才有 Coupled Parameters）：
  - **Fixed Cycle Parameters**：Pre-Sweeps/Post-Sweeps——scalar 默认 0 前/1 后（少数情况 pre 增至 1–2）；coupled 默认 3 后/0 前；压力基 coupled + pseudo time 时 scalar 也 3 后。**告诫**：固体导热含各向异性/极高导热系数时 AMG+V cycle 可能因默认 post=1 发散——增加 post-sweeps（压力基 segregated）；**并行运行能量方程建议用 Fixed F-cycle**。
  - **Coarsening Parameters**：**Max Coarse Levels**（建到最粗层只剩 3 个方程为止；调低省内存但迭代增多；**0 = 关闭 AMG**）；**Coarsen by**（每粗单元聚合的细单元数——scalar 典型 2–10、Gauss-Seidel 默认 2 性能最好内存最多；coupled 及 pseudo time 下 scalar 默认 4(2D)/8(3D)（ILU）；非必要勿调）。**随 smoother 调整：ILU → Post-Sweeps 3 + Coarsen by 8；Gauss-Seidel → Post-Sweeps 1 + Coarsen by 2**。粗化选项（可单用或组合）：**Conservative Coarsening**（默认开——按系数强度与并行分区调优粗化）；**Aggressive Coarsening**（更激进粗化率——AMG 默认发散时试；Coarsen by > 2 或高核数时更有益）；**Laplace Coarsening**（默认关——用 Laplace 系数评估邻居强度；粗层不随解演化改变→更稳、高核数时省时）。
  - **Smoother Types**：**Gauss-Seidel**（最简单——压力基 segregated 推荐）与 **ILU**（更耗 CPU、块耦合系统光顺更好——压力基 coupled 与密度基隐式）；scalar 默认 Gauss-Seidel、coupled 默认 ILU（coupled + pseudo time 时 scalar 也用 ILU）。
  - **Flexible Cycle Parameters**：Max Fine Relaxations / Max Coarse Relaxations。
  - **Verbosity**：Multigrid 选项卡设 1–2 → 跑一次迭代 → 控制台输出方程名/容差/每循环或松弛后残差/各层方程数（verbosity 2 含层级大小；verbosity 1 仅名/容差/残差；cycle/relaxation 0 的残差为多重网格前的初始残差）。
  - **Default/Reset 按钮**恢复默认或找回改动。
- **37.5.5 FAS 多重网格参数**（仅密度基显式）：收敛"卡住"（细长管道类——压力信息传播慢）→ Multigrid Levels 设 0 关多重网格；**"industrial-strength" FAS**——收敛极慢时用：增大各层 pre/post 迭代数（Pre-Sweeps 试 10）、层间完全修正传递、插值修正不平滑——**非常激进：只在解已良好起步后使用**（过早用会把严重错误的值快速传播回去、致不稳）；总迭代数减少但每循环耗时大增（更少更长的迭代）；参数在 Multigrid 选项卡 FAS Multigrid Controls。

## 37.6 解限值（pp. 3759–3762）

Solution → Controls → Limits...：Fluent 对**绝对压力、静温、湍流量**设限（防零/负/过大），Eulerian 双精度隐式体积分数矩阵解另设最小体积分数（防矩阵奇异）。一般无需改默认；变量反复触限（告警）→ 检查尺寸/边界条件/物性，可用场变量 cell register 标记触限单元；仅在有明确理由时改限值（如域温确超 5000 K——需同步定义高温物性；体积分数需低于安全限 1e-08 的核化/微量污染物场景——调低限可能不稳）。
- **绝对压力限仅对 ideal-gas 或 real-gas-* 密度法的流体材料生效**；compressible-liquid 或 UDF 可压流体——压力限只保证密度为正、不限制压力值本身。密度基解 T/P 逼近限值时可用 divergence prevention（见 37.4.5）而非改限。
- **37.6.1 变量限值**：Minimum/Maximum Absolute Pressure、Minimum/Maximum Temperature、Minimum Turb. Kinetic Energy、Minimum Turb. Dissipation Rate、Maximum Turb. Viscosity Ratio（湍流粘度/层流粘度比超限则限制 μ_t）；Eulerian 与 Mixture 双精度隐式体积分数——Minimum Vol. Frac. for Matrix Solution；显式体积分数模型与 VOF 用 Multiphase Model 对话框的 Volume Fraction Cutoff。注意：**Eulerian 对动量/湍流/能量/组分/UDS 方程都用解限值，VOF 与 Mixture 只对组分与 UDS**。
- **37.6.2 Positivity Rate Limit**（密度基）：控温度下降速率——默认 **0.2**（单次迭代温度降幅不超 20%；超限则该单元时间步缩短并打印 "time step reduced" 告警——该步长对该单元所有变量生效）；反复告警 = 设置有问题。**高速流能量方程发散时降到 0.05 或 0.02 可能有帮助**。开 High-Speed Numerics 时该限也作用于压力更新（另有压力受限单元数告警）。
- **37.6.3** Default/Reset 按钮恢复默认。

## 37.7 多级时间步进参数（pp. 3762–3764）

密度基显式的 Multi-Stage 选项卡（Advanced Solution Controls）。**非熟谙多级格式者勿改**。默认：稳态 **3 级**（系数 0.2075/0.5915/1.0）、非稳态 **4 级**（0.25/0.3333/0.5/1.0）；级数超过 5 需 TUI `solve/set/multi-stage`。每级 Coefficient ∈ (0,1)、**末级必须为 1**；每级可勾 **Dissipation** 与 **Viscous**（不勾则"冻结"沿用上一级值）——粘性应力**应始终在第一级计算**、后续级逐级评估更稳健但更耗时；稳态最终解与粘性项评估层级无关。Default/Reset 按钮同前。

## 37.8 梯度限制器（pp. 3764–3765）

默认 **Standard** limiter；Advanced Solution Controls → Expert 选项卡 Spatial Discretization Limiter Type 三选——**Standard / Multidimensional / Differentiable**（TUI `solve/set/slope-limiter-menu`，default/multi-dimensional/differentiable）。每种限制器三种**限制方向**：**Cell to Face**（默认，单元面心求限制值）；**Cell to Cell**（相邻单元质心连线上求——正交网格等价于默认；光滑场变化时斜网格上数值耗散更低）；**Cell to Node**（单元顶点求——比默认更保守、强梯度非结构网格上单调性与稳健性更好，**特别适合拉伸/斜/高长宽比单元**；overset 网格与 multidimensional 限制器不可用）。**Limiter Filter**（Standard 与 Differentiable 可用，Multidimensional 不可用）：保持主流变量高阶精度——抑制小数值噪声引发的限制器介入、保留真实间断/大梯度（激波/边界层）处的限制；基于局部单元变化量与全域平均变化量之比；勾 **Apply Limiter Filter** 启用（默认只作用于主流与湍流变量）；可改善残差表观收敛。

## 37.9 初始化（pp. 3765–3771）

初场必须提供；**某些问题必须精心给初值**（超音速风洞类比——不初始化到超音速就会壅塞保持亚音速）。两途径：①全流场初始化（Standard / FMG / Hybrid 三法）；②patch 选定值。**patch 前必须先全场景初始化**。**重要**：使用 UDRGM、UDF 自定义密度、或解相关表达式时——用 Hybrid 初始化或 Compute from 特定区之前，必须先做一次 **Compute from 不选区的标准初始化**（解决"初值依赖物性/表达式、物性/表达式依赖解"的循环依赖）。
- **37.9.1 标准初始化**：Solution Initialization 任务页——Initialization Method 选 Standard；初值三来源：Compute from 选区（按该区边界条件算）、all-zones（全边界平均）、手输；单相组分输运可用 Species 按钮选边界组分显示；Reference Frame——Absolute 或 Relative to Cell Zone（**默认 relative**；大域旋转时 relative 更好）；Initialize 确认覆盖已有数据。初值随 Initialize 保存（重开页面可见）；Reset 按钮回到"已保存"值。
- **37.9.2 Patch 选定单元**：Patch 对话框（Solution → Initialization → Patch...）——选变量 → 选 Zones to Patch 和/或 Registers to Patch → 常量值 / **表达式**（命名表达式或 Expression Editor；列表未显示时切换变量再切回、单位需匹配）/ **场函数**（Use Field Function）；速度 patch 同样有绝对/相对参考框选择（默认 relative）。**Patch 不影响迭代/时间步计数**。**shell 区**（开 shell conduction 并算过后）出现在列表为 `shell : <wall-name>`——**只能 patch 温度且各层同值**。Workbench 中打的 patch 不会在后续自动求解更新时自动执行——需在 Automatic Solution Initialization and Case Modification 对话框 Case Modification 选项卡的 Original Settings 命令列表加 `/solve/patch`。Register 用法：cell register（物理位置/单元体积/梯度/变量等值面等标记单元）可在一个单元区内局部 patch；场函数可 patch 非常数值。**求解中途也可 patch**——只改所选变量、保留其余数据（如冷流解 → patch 高温 → 继续燃烧计算）；配合分步求解策略（p. 3889）。
- **37.9.3 边界 profile 内存冲洗**：解相关边界 profile 的场景重初始化可能不干净（边界值残留上次信息）——TUI `/solve/initialize/enable-profile-memory-flushing` 启用后下次初始化时边界 profile 值被冲洗重算（**默认关**——解无关 profile 不需要）。

## 37.10 FMG 初始化（pp. 3771–3774）

旋转机械、扩张/螺旋管道等复杂流动——更好的初始解加速收敛，FMG 以最小代价提供近似初始解。前提：已完成标准或 hybrid 初始化、或有有效流场数据（读 data）。TUI `solve/initialize/set-fmg-initialization` 定制：多重网格层级数（**默认 5；10 万单元以下小算例建议降 3–4**）；逐层残差缩减（默认 0.001）与每层循环数（默认 100/200/400/800/800/800——**粗层多做、细层少做**；Level 0 = 原始网格）；FMG 迭代 Courant 数（**默认 0.75**）；verbose（默认 yes——逐层监视）。执行：`solve/initialize/fmg-initialization` → Enable FMG initialization? yes。verbose 输出逐层信息与 FAS 循环收敛史（每 10 个 FAS 循环或达循环数时打印归一化残差）。
- **收敛策略**：粗层多算细层少算；目标是低成本好初场——避免不合理的收敛容差；不收敛 → 增加各层 FAS 循环数；发散 → 降 FMG Courant 数（默认可能过激进）。**湍流务必先做含合理湍流量（k、ε）的标准初始化**（按入口或全边界平均）——不现实的湍流初值会让细层前几步收敛困难、抵消 FMG 收益。
- **密度基附加选项——粘性 FMG**：默认 FMG 用无粘 Euler 方程；`solve/initialize/set-fmg-options/viscous-terms?` yes 可加 N-S 粘性项——初始化阶段即发展边界层、减轻起动瞬态；湍流方程不解但粘性项计入有效粘度（含湍流粘度贡献）——自由流初始化的湍流粘度常不足以发展边界层，**默认湍流粘度比 100**（`solve/initialize/set-fmg-options/set-turbulent-viscosity-ratio` 可改）。

## 37.11 Hybrid 初始化（pp. 3774–3778)

**单相稳态的默认初始化方法**（多相/非稳态默认 Standard；两类在任何工况都可用）。一般只需点 Initialize；More Settings... 打开 Hybrid Initialization 对话框三区：
- **General Settings**：Number of Iterations（默认 **10**——解 Laplace 方程初始化速度与压力；复杂高曲率几何若达不到 1e-06 收敛容差可加）；Explicit Under-Relaxation Factor（默认 **1**；标量残差振荡难达 1e-06 时减小，也可加迭代数）；Reference Frame（默认 Relative to Cell Zone）；Initialization Options——**Use Specified Initial Pressure on Inlets**（用进口 Supersonic/Initialization Gauge Pressure 解压力 Laplace 方程，否则用内置配方）；**Use External-Aero Favorable Settings**（速度势线性 patch——外流气动如机翼/汽车加速 Scalar Equation-0 收敛、改善速度初猜）；**Maintain Constant Velocity Magnitude**（用速度势得流向但保持常速度模——不可压外流、多孔介质、窄通道防大速度）。
- **Turbulence Settings**：默认域平均湍流参数；取消 Average Turbulent Parameters 则按局部流动参数算 k/ε 等。
- **Species Settings**：默认次生组分零分数初始化；勾 Specify Species Parameters 可指定（仅 Select Boundary Species 选中的边界组分出现）。
- **策略**：一般无需调整；不满意时用对话框选项或再叠加 patch（如 UDS 被初始化为 0 后可 patch）；可配合 UDF 初始化。**多孔介质仿真推荐标准初始化**——默认 Hybrid 不计多孔介质属性、可能给出不真实的初始速度场；多孔介质用 Hybrid 只能配 Maintain Constant Velocity Magnitude。

## 37.12 稳态计算（pp. 3778–3782）

Run Calculation 任务页（Solution → Run Calculation）：压力基 coupled 或密度基隐式选了 **Global Time Step** pseudo 方法时先设 Pseudo Time Settings 组（见 p. 3815，批次 104）；所有算例给 **Number of Iterations**（从迭代 1 起算或从当前数据继续）。**Reporting Interval**（默认 1）控制收敛监视器打印/绘图频率——**也控制收敛检查频率**（如收敛于 40 步但间隔 50 则会多算 10 步才报收敛；**只影响残差收敛检查，不影响报告定义收敛检查**）。Calculate 启动；进度条旁 **Stop** 在最近安全点中断，控制台 **Ctrl+C** 亦可。
- **37.12.1 更新 UDF profile 与命名表达式**：Profile Update Interval（默认 1，每 N 迭代更新一次——profile 计算昂贵时可调大）。
- **37.12.2 重置数据**：重新初始化即可从头开始。
- **37.12.3 稳态数据采样（Data Sampling for Steady Statistics）**：名义稳态但振荡/准瞬态的仿真——采样生成行为更好的平均值与趋势。Run Calculation 勾 Data Sampling for Steady Statistics + Sampling Interval；**Sampling Options 对话框法**（先可建 custom field function；得 **mean/RMS/RMSE**，Steady Statistics... 类别后处理）；**Zone-Specific Sampling Options 对话框法**（另得 **min/max/moving average**，变量带 -dataset 后缀）。**矢量模量统计两法算法不同**：Sampling Options = 平均的模（magnitude of mean），Zone-Specific = 模的平均（mean of magnitude）——结果可有差异。Reset Statistics 初始化/重置统计（不重置则继续累计）。**壳面上不采集统计**。

## 37.13 瞬态计算（pp. 3782–3811）

应用：涡脱落等周期现象、可压充排、瞬态导热、瞬态混合反应；**趋于失稳的稳态问题（Rayleigh 数近过渡区）也可用瞬态积分逼近稳态**。
- **37.13.1 输入**：General 勾 Transient → 模型与边界条件 →（可选显式瞬态）`solve/set/fast-transient-settings/rk2` 启用二段 Runge-Kutta（Number of Stages 2、系数 0.5/1；发散则降 CFL（<1）+（隐式）提高每步最大迭代；再次执行可关闭恢复默认多级格式）→（可选）Statistic 监视器打印 flow-time 或 delta-time 列 →（可选）Drag/Lift/Moment/Surface 报告定义监视时变力系数 → 设初值（初始化或读稳态 data）→ **Autosave**（Calculation Activities）定期存盘（亦可导出解与颗粒历史、设动画、Execute Commands）→ 时间推进参数：
  - **隐式（First/Second/Bounded Second Order Implicit）**：Run Calculation——Type 选 **Fixed**（Method：**User-Specified** 给 Number of Time Steps + Time Step Size；**Period-Based / Frequency-Based**——叶轮机械或周期行为按 Period/Frequency + Time Steps per Period + Total Periods 自动换算；**in-cylinder 动网格只能 User-Specified**，按曲轴转速与转角步长算）或 **Adaptive**（Method 三选——**CFL-Based** / **Error-Based** / **Multiphase-Specific**，见下）。完全隐式无稳定性判据，但为正确解析瞬态 Δt 至少比系统最小时间常数小一个量级；**每时间步理想迭代数 5–10**——明显更多则 Δt 过大、只有几步则可增大；起动瞬态快——前 5–10 步用保守小 Δt 再渐增；周期问题按周期定 Δt（rotor/stator 每叶频 20 步、涡脱落每周期 20 步）；算后用 **Cell Convective Courant Number** 云图验证——敏感瞬态区 Courant 数不宜超 **20–40**。Duration Specification Method——**Total/Incremental 的 Time 或 Time Steps** 四选（total 计入已算部分、incremental 忽略已算部分）；**Adaptive 前建议先做几个固定步**（脉冲起动的伪离散误差会干扰自适应导致极小步长——Number of Fixed Time Steps + Initial Time Step Size（须在 min/max 之间，起动时 Courant 数保持近 1 或给定值较低者））；重新初始化已跑过自适应的 case 会沿用 case 中保存的时间步。**Error-Based 收敛不完全时下一步自动减步**（不低于最小步长）而非保持/增大。Max Iterations/Time Step（提前达标则进下一步）；Time Step Size Update Interval（自适应法隔多少步更新步长）；Settings... 打开 Adaptive Time Stepping 对话框设 min/max 步长与变化因子；**提示**：要精确结束于指定总时长就把最小步长逐步调小。**自动网格自适应联动**：CFL-Based 与 Multiphase-Specific 自动使用重算步长（初始固定步之后）；Error-Based 或动态/滑移网格下的任何自适应法不使用（控制台告警——偏差大时应修改设置保证时间精度）；Extrapolate Variables 开启或 overset+VOF 时不重算。自定义自适应：`DEFINE_DELTAT` UDF → Type 选 User-Defined Function。**Extrapolate Variables**（可选）：Taylor 外推下一步解作内迭代初猜、降低绝对残差水平——**NITA（压力基）与密度基显式不可用**；密度基不可压流建议关闭压力外推（`solve/set/transient-controls/extrapolate-eqn-vars/pressure` → no）。Report Simulation Status 打开 Simulation Status 对话框。**时间统计采样**：Data Sampling for Time Statistics + Sampling Interval（如 5 = 每 5 个结果进样）；Sampled Time 显示采样时长（变步长时各样本按当前时间步加权）；**DPM 量只在颗粒穿过单元时采样**（样本数存于 Accum DPM Parcels in Cell）；**Sampling Interval 不作用于运行时 DFT**（DFT 每时间步后累加、累加时长固定——用 Samples to Complete 估算进度；标准统计可任意长）；移动单元区内采时间统计无意义；壳面不采集；Reset Statistics 同前；两对话框（Sampling Options 与 Zone-Specific）均可用（矢量模量统计差异与 -dataset 后缀同稳态）。
  - **显式瞬态**：Solution Controls 指定 **Specified Time Step**（默认；Run Calculation 给步进——稳定性受 CFL 条件限制：给定步长超稳定限（Eq 37.2，各局部时间步最小值）时告警）或关闭之改给 **Courant Number**（按 Eq 37.2 由 V/A/最大局部特征值算 Δt）。
- **37.13.2 CFL-Based Time Stepping**：**仅压力基与密度基隐式**；不可用于密度基显式、多相流、in-cylinder 动网格、声学模型、结构模型、以及经 `solve/set/second-order-time-options` 或动网格启用固定步长的二阶隐式；**存在其他控制性时间尺度（表面张力、网格变形驱动）时不宜用**。仅当流动方程启用且流动为对流主导时步长才变化。算法：每单元算时间步（可计声学/对流/粘性时间尺度——**默认只计对流速度**，适合低速不可压）、默认取全域最小值（在 min/max 内）。参数——Run Calculation 页：**Courant Number**（Eq 37.6；对流主导/波传播问题推荐近 1——越大步长越大但损收敛/稳定/精度）；Initial Time Step Size + Number of Fixed Time Steps（同前）；Adaptive Time Stepping 对话框：**Minimum/Maximum Step Change Factor**（限制逐步变化幅度平滑步长——推荐 min 0.5–0.75、max 1.2–2；**默认 0.5 与 2**）。高级 TUI `solve/set/transient-controls/cfl-based-time-stepping-advanced-options`：**最小/平均 CFL 条件**（默认最小）；**CFL type 四选**——[1] **Convective**（仅对流速度；Eq 37.3；低速不可压默认）、[2] **Convective-Diffusive**（对流+粘性时间尺度；Eq 37.4；粘性主导极低速）、[3] **Acoustic**（声速替代对流速度、忽略粘性；Eq 37.5；超音速可压且粘性不重要）、[4] **Flow**（声学+对流+粘性组合、物理特征值系统；Eq 37.6；能解析多数流动尺度但步长较不激进）。
- **37.13.3 Error-Based Time Stepping**：**仅压力基与密度基隐式**；不可用于密度基显式、二阶时间积分、in-cylinder 动网格；**Euler-Euler 多相不可用（Eulerian 开隐式体积分数除外）**。算法：预测-校正估计截断误差（显式前向 Euler 预测 → 隐式非线性迭代校正；预测与校正之差的范数 = 截断误差度量）——误差小于容差则增步、大于则减步；容差未达时**最多尝试 5 次**，仍超可回退本步以更小步长重做（截断误差 ∝ 步长）。参数——Run Calculation 页：**Error Tolerance**（默认 **0.01**；调大步长大精度降、调小反之）；Initial Time Step Size 同前（Courant 数近 1）；Adaptive Time Stepping 对话框：Minimum/Maximum Step Change Factor——按"容差/计算误差"之比调步（超容差增大；不足时增大但上限为 max 因子；满足不变；反之类推）。
- **37.13.4 Multiphase-Specific Time Stepping**：**所有隐式/显式体积分数多相模型可用（湿蒸汽除外）**；不支持 in-cylinder 动网格、声学、结构模型。默认基于对流时间尺度（Courant）——步长计算取决于界面单元的网格密度与速度；**存在其他控制性时间尺度时 Courant 尺度不合适**。算法分两档：无物理约束/动网格约束时仅对流（flux-based，Eq 37.9/37.10 全局步长）；启用 **Physics Based Constraint** 和/或 **Moving Mesh CFL Constraint**（均 **VOF 专属**）时计入八种时间尺度——对流（flux/velocity-based 及二者混合的聚合尺度）、粘性、重力、表面张力驱动、声学、网格运动驱动（flux/velocity-based 及聚合）——有效物理尺度（Eq 37.21）、有效动网格尺度（Eq 37.22）、全局尺度取两者逐单元最小（Eq 37.23）；有效全局步长受步长变化因子与 min/max 步长约束；控制台打印 **Effective Global Courant Number**。参数——Run Calculation 页：**Global Courant Number**（flux-based 定义——界面附近单元体积/流出通量和=排空时间；**默认 2**；建议：显式体积分数——瞬时解用默认 2、时均解可高于 2 但 ≤5；隐式体积分数——瞬时解一阶时间 2（推荐）、二阶时间可至 5，时均解可至 20）；Initial Time Step Size 同前；Adaptive Time Stepping 对话框：Minimum/Maximum Step Change Factor（**推荐 min 0.5–0.8、max 1.2–1.5；默认 0.8 与 1.2**）；**Moving Mesh CFL Constraint**（VOF；勾后可调 Moving Mesh Courant Number 默认 1；纯刚体运动时该参数不敏感；需 Frame Motion/Mesh Motion/Dynamic Mesh 之一）；**Physics Based Constraint**（VOF；按物理类型——粘性/声学/重力/表面张力等——计入约束）。
- **37.13.5 瞬态后处理**：与稳态相同设施；读任意时刻保存的 data 恢复该时刻（图形/数值输出自动标注当前时间值）；力/面报告定义存文件可回读绘图看时间历程；Unsteady Statistics...（离散相为 Unsteady DPM Statistics...）类别给 mean/RMS/RMSE（Zone-Specific 另有 min/max/moving average/运行时 DFT）。
- **37.13.6 运行时离散傅里叶变换（Runtime DFT）**：目的——①傅里叶幅值与相位的空间场后处理；②用 **Inverse DFT** 创建频率滤波的瞬态解动画（**2026 R1 为 beta 功能**，见 beta 手册）。适用于瞬态仿真、可作用于任意已有场变量；作为 zone-specific 时间统计采样的一部分（Solution → Run Calculation → Sampling Options (Zone Selection)）；DFT 数据按数据集组织——每个数据集 = 一个量 × 一组区 × 一个频带（Frequency Band）或单音（Single Tone）；多量同选项则各建一集。限制清单始于 p. 3811 末（正文续下段，待批次 104 补记）。

## 37.14 伪时间方法（Pseudo Time Method）（pp. 3812–3823）

隐式欠松弛形式。适用：压力基 segregated（SIMPLE/SIMPLEC/PISO）的全部计算；压力基 coupled 与密度基隐式的**稳态**计算。设置：Solution Methods → Pseudo Time Method 下拉——**Local Time Step**（仅压力基 segregated）或 **Global Time Step**（压力基 coupled / 密度基隐式；单相无电池/燃料电池/熔凝模型的压力基 coupled 默认选中）。**Local Time Step 不可用**：结构模型、多相模型、G Equation 模型（预混/部分预混燃烧）、缝隙模型、NITA；**组分输运 + 能量方程关闭时不支持**。
- **37.14.1 Local Time Step 设置**：Solution Controls 的 **Pseudo Time Courant Number**（逐单元局部伪时间步长据此算）；Pseudo Time Under-Relaxation Factors 逐方程设 URF。**推荐用 Local Time Step 获得更好收敛行为**——Courant 数调小改善收敛但降低收敛速率。
- **37.14.2 Global Time Step 设置**：
  - **Pseudo Time Explicit Relaxation Factors**（Solution Controls）逐方程设（压力基 coupled 全方程都有；密度基隐式仅顺序求解的方程有）；Default 按钮恢复。
  - **Advanced Solution Controls（Expert 选项卡）** 两手段：①给特定方程设 **Time Scale Factor**（缩放流动方程伪时间步长）替代统一全局伪时间步；②对该方程**关闭伪时间方法**改用标准稳态法（配 Under-Relaxation Factor）。默认全方程伪时间开、时间尺度因子 1——**例外：燃烧模型的组分/焓/燃烧变量方程需在 Expert 选项卡手动启用**（预混/部分预混的能量变量亦可手动启用）；**UDS 默认全部关闭**（求解前不知其物理参数与合适时间尺度，可手动开）。多相流：体积分数方程的专家选项仅在其 segregated 求解时可用（Coupled with Volume Fractions 开启时不可用）。
  - **Pseudo Time Settings（Run Calculation）**：**Fluid Time Scale** 的 Time Step Method——**User-Specified**（输 Pseudo Time Step Size，除非方程有专属步长；典型取流动全局时间尺度相关值，如特征长度/速度）或 **Automatic**（默认；内部按激活物理的时间尺度估算）——Automatic 可用 **Time Scale Factor** 调收敛（自动估算常偏保守，**提高到 3 或 10 常能加速**；少数情况降 0.3/0.1）；**Length Scale Method** 三选——**Conservative**（默认；3D 网格体积立方根/2D 面积平方根）、**Aggressive**（最大几何延展——步长更大）、**User-Specified**（直接给长度尺度——适于特定长度尺度难从整体几何判断的问题，如翼型绕流用弦长而非全域尺度）；**Verbosity** 0/1/2（1 打印伪时间步长、2 更多细节）。**Solid Time Scale** 组（仅当能量方程+固体区、多孔区启用、或熔凝模型启用时出现）：User-Specified 或 Automatic（默认）+ Time Scale Factor。其余按稳态流程。

## 37.15 使用远程资源计算（pp. 3823–3826）

Fluent 会话内向任意 HPC 支持的远程集群提交单个 Fluent 作业（Solution → Run Calculation）。**Manage Remote Resources** 对话框管理集群：Add（Resource Details——名称、URL、是否默认）/ Edit / Delete；已定义资源出现在 Run Calculation 任务页与 Ribbon 组的 **Compute Resources** 下拉——**集群信息本地缓存、Fluent 启动时读取，之后每个会话都可用**；需要认证时弹 Connect to Remote Cluster（用户名/密码）。作业提交后可在会话内跟踪（中断、删除、停止、下载文件等）。参数化研究（p. 4617）：Compute Resources 选远程集群则并发作业默认用该集群（可在 Concurrent Settings 断开改用其他）；选当前会话则并发作业集群字段留空、直接在 Concurrent Settings 填。
- **提交**：Compute Resources 选远程资源 → **Submit...** 打开 Remote Compute 对话框设作业属性 → **Submit Job**；作业详情打印到控制台并写文本文件；**Jobs on Remote Cluster** 对话框监视状态（默认每分钟刷新、可调）。字段说明与云提交共用（见 37.16.2.1–37.16.2.5）。

## 37.16 Ansys Cloud Burst Compute（pp. 3826–3834）

有 Ansys Cloud（portal.ansys.com）账户且余额为正时，可从 Fluent 界面直接把会话提交到 Ansys Cloud Burst Compute 远程运行/监视。可做：选云资源、提交求解作业、选文件（case/data/journal 等）、指定外部文件搜索位置、指定资源（精度/核数/队列等）、跟踪作业、查看历史作业、中断运行/排队作业、下载完成作业的输出文件。
- **接入前提**：公司订阅 Ansys Cloud 计划（含云算力点数池与有限用户席位）；需要 Ansys ID、公司计划成员资格（管理员添加）、云用户席位分配、池内足够点数。管理员在 admin.ansys.com 管理。Fluent 界面直接登录（Sign In 图标 → 默认浏览器认证，或 Preferences 的 Remote Compute Resources 类把 Authentication Method 从 Web Browser 改 **In-session** 会话内认证）。登录后 **Select Account To Use For Ansys Cloud Burst Compute** 对话框选账户（可查余额/小时数）→ Use Selected Account（关掉后可经 Sign-In → Account Details 重开）。
- **提交**：Compute Resources 选 **Ansys Cloud Burst** → Submit... → Ansys Cloud Burst Compute 对话框设作业属性 → Submit Job；云端监视见 portal.ansys.com。注意：提交/取回时偶发账户余额相关报错——重试通常解决；Linux 会话内认证的 GpuChannelMsg/libpng 报错为非阻塞、可忽略。
- **37.16.2.1 Job Details**：Project Name（仅云；默认 case_name-cloud-run）；Job Name（云默认 case_name-cloud-run、远程 case_name-remote-run）；Precision（Single/Double）；Number of CPU Processes（总核数）；MPI Type（随版本与架构变化）；**Queue**（连接后从可用队列选——**Fluent 自动选能运行指定核数的队列**，找不到则报错不能提交；选中队列属性打印控制台并作 tooltip）；**Interconnect Type**（默认推荐；按队列是否启用 **EFA（Elastic Fabric Adaptor）** 自动选 ethernet.efa 或 ethernet）；Use GPU Solver（原生 GPU 求解器 + Number of GPUs per Node——仅参数化并发设计点更新的远程/本地作业）；Start Web Server（用当前会话 Web Server Token 启动 web 界面——同上场景）；Show Advanced Options（云或参数化并发远程）：Number of CPUs Per Node、Maximum Execution Time (Hours)、Exclusive（仅参数化并发远程）。
- **37.16.2.2 Case Details**：作业含当前载入的 case/网格；**Upload Associated Files Only**（Fluent 探测依赖文件并在工作目录中查找——缺失会通知）或 **Upload All Files From Working Directory**；有有效 data 文件时会询问是否使用并上传。
- **37.16.2.3 Journal Details**：**Default**（按 case 设置初始化并求解的默认 journal）或 **Custom**（自选 journal）；**Automatically Generate Simulation Report** 可导出 HTML/PDF/PPT。
- **37.16.2.4 Output Files**：Keep All Output Files 或 Keep Specific Output Files（逗号分隔清单）。
- **37.16.2.5 会话内查看/管理作业**：Solution 选项卡 Remote Jobs → **View Jobs** → Jobs on Remote Cluster 对话框——按 Project Name/Job Name 选择看 Properties；Job Actions：Open Job(s) in Web Portal、Interrupt/Abort/Rerun Job(s)、Download All/Specific Files（下载为独立进程、主会话仍可用、多文件逐个顺序下载）、**Submit Remote Postprocessing Job（beta）**、Delete Job(s)/Project(s)；Filter Jobs（pending/prolog/running/evaluated/failed/timeout/aborted/all）；Refresh Mode——**Auto**（按 Refresh Interval 分钟数自动刷新；全部完成即停）或 **Manual**。
- **37.16.2.6** 云端查看：portal.ansys.com 的项目/作业表。

## 37.17 监视求解收敛（pp. 3834–3846）

监视手段：残差、统计、力值、面/体积分；升力/阻力/力矩系数、面积分、残差的打印与绘图；非稳态还可监视流逝时间。报告定义创建见 p. 4326。
- **37.17.1 残差监视**：每迭代结束算各守恒变量残差和并记录（存 data 文件）。**精度与残差下降极限**：单精度（多数机器默认）可下降约 **6 个量级**、双精度约 **12 个量级**后触 round-off 走平。
  - **压力基残差定义**：单元守恒方程不平衡度之和 = **unscaled residual**（Eq 37.27）——直接看难以判断收敛（封闭流动无进口通量可比）。两种缩放：**globally scaled**（Eq 37.28；分母为 φ 的域流量代表值——动量方程分母用单元速度模、Reynolds 应力方程用张量迹/维数）与 **locally scaled**（Eq 37.29；局部缩放）。**默认显示 global scaling**。连续方程 unscaled 定义不同（Eq 37.30）；**局部缩放默认用增强式**（Eq 37.31，逐面质量流量绝对值——与其他残差行为更一致；Compute Local Scale 开启后可经 `solve/monitors/residual/enhanced-continuity-residual?` 关掉改用 Eq 37.29）；**全局缩放对连续方程分母 = 前 5 次迭代连续残差的最大绝对值**（Eq 37.32）。**归一化**（Normalize）：残差除以前 N 迭代最大残差（Eq 37.33；默认 N=5；保证各方程初始残差为 1）；可在 Residual Monitors 对话框 Iterations 字段改 N 或手动指定 Normalization Factor；最大残差出现在 N 之后时可点 **Renormalize** 重算因子。原始（scaled+unscaled）残差与缩放因子都存 data 文件、可切换。
  - **密度基残差定义**：残差 = 守恒变量的时间变化率；**RMS 残差**（Eq 37.34，各单元残差平方均值的平方根）为耦合方程的 unscaled 报告值；顺序求解的方程（湍流等）用与压力基相同的定义。缩放同两法——global（Eq 37.35，分母前 5 迭代最大绝对值）、local（Eq 37.36，局部通量不平衡 × 单元体积）；归一化 Eq 37.37（默认 N=5，此时归一化残差等价于缩放残差）。
  - **Residual Monitors 对话框**（Solution → Reports → Residuals...）：一般只需开残差绘图 + 改收敛判据。Print to Console / Plot 开关；Plot 按钮画当前残差史。**Iterations to Store**（默认 **1000**——超限隔点丢弃留 500 再续；大量迭代会丢失早期历史，应调大；代价是内存/绘图时间/data 文件体积）。**Show Advanced Options** 后：Scale 默认开（global scaling）；**收敛判据默认能量/DO/P-1 方程 1e-06、其余 1e-03**；**Compute Local Scale** 开启后可选 Reporting Option（局部/全局缩放绘图或打印——默认绘全局；**局部缩放时每方程默认判据改为稳态 1e-05、瞬态 1e-04**）；开启后同时计算存储两种缩放残差；Preferences（Simulation）可设 Local Residual Scaling 默认绘局部；开 Compute Local Scale 后关 Scale 不会自动关（继续算两种、但只打/绘 unscaled）。Normalize 默认关；**切换 scaled/unscaled 且在归一化时必须点 Renormalize**。**收敛判据类型**（Convergence Criterion 下拉；TUI `solve/monitors/residual/criterion-type`）四选——**absolute**（默认；稳态只有 absolute 与 none；残差与给定值比较）、**relative**（本步内残差/时间步起始残差之比与给定值比较）、**relative or absolute**（满足其一即收敛）、**none**（禁用检查）。相对判据缓解绝对判据对瞬态过严的问题（如连续方程缩放因子低导致达不到绝对判据）；relative or absolute 适合某些方程在步初已很低（近稳态变量）无法再降量级的情况。**relative 类仅限非稳态压力基与非稳态密度基**；relative/relative-or-absolute 时 residual 菜单出现 relative-conv-criteria 可设；**NITA 启用时无判据可选**。逐变量 **Check Convergence** 开关与判据值修改；Monitor 列表逐变量开关（方程多时可只监视关键子集）。**Plot 参数**：Window（图形窗口 ID——残差图画在独立窗口）；**Iterations to Plot**（显示最近 n 个存储点——注意是存储点非求解迭代数，存储频率随迭代增大而降低）；Axes.../Curves... 改坐标轴与曲线属性。**残差后处理**：收敛困难时常绘残差场（等值线）定位高残差区——默认只有密度基的时间步/压力基的质量不平衡场；需更多变量时：读 case+data → `solve/set/advanced/retain-cell-residuals` → 至少迭代一次 → Residuals... 类别出现（**DO 辐射方程无残差值；提供的是 unscaled 值**）。
- **37.17.2 统计监视**：全发展周期流的压力梯度/_bulk 温度比（periodic-pressure-gradient、periodic-bulk-temperature-ratio）；非稳态的 flow-time（物理时间，初始化起为 0）；自适应时间步的 delta-time；另有 iterations-per-timestep。五个量均可建报告文件/绘图——flow-time 与 delta-time 可同图、periodic 两量可同图（Solution → Monitors → Report File/New...）。
- **37.17.3 解量监视**：已建 Report Definitions 的量（力/力矩系数、面/体积分）每迭代（稳态）或每时间步（瞬态）末计算存储形成收敛史；**可计算多迭代/步平均值**——**运行平均帮助判断振荡/不规则解是否收敛**；经 Report Files/Report Plots 打印绘图存盘（Solution → Monitors → Report Files or Report Plots）。

## 37.18 收敛条件（Convergence Conditions）（pp. 3846–3850）

基于**报告定义值**（surface/volume/lift/drag 等）设收敛条件。两个选择：①**Check For**——Solution Convergence（每时间步检查）/ Time Step Convergence（每迭代检查）；②**Choose Condition**——**All Conditions are Met**（所有激活报告定义判据与启用残差都满足才算收敛）/ **Any Condition is Met**（任一满足即收敛）。默认逻辑：报告定义判据**与**残差判据同时满足才收敛——只靠报告定义判断则清掉 Residual Monitors 中的 Check Convergence。入口：Solution → Reports → Convergence...；Active 列勾选激活/停用条件。**37.18.1 设置**：Add 选 Report Definition 建 condition；**Ignore Iterations/Time Steps Before**——前若干步波动期不检查；**Use Iterations/Time Steps**——回看步数（波动算例要足够大）；**Stop Criterion**——判据：对回看窗内各步计算 Res-m(k) = |m(n) − m(n−k)| / m(n)（k=1..Np），**最大值 < Stop Criterion 即视为收敛**；勾 **Print** 打印报告定义残差（Pres-m(n) = |m(n) − m(n−1)|/m(n)，只对前一步）。

## 37.19 计算中执行命令（p. 3850–3851）

Execute Commands 对话框（Solution → Calculation Activities → Execute Commands → New...）定义计算过程中按指定间隔执行的命令（如按梯度 cell register 自适应网格）。**注意**：存 case/data、导出瞬态解文件、导出颗粒历史数据请用 Calculation Activities 任务页的专用对话框而非命令。步骤：①勾 **Active**（可定义多条、按需启用）；②Name；③**Execute Repeatedly**——Every N + When 选 Iteration / Time Step / Flow Time / Adjoint Iteration / Design Iteration（Time Step 与 Flow Time 仅非稳态有效；Adjoint/Design Iteration 仅从 Gradient-Based Optimizer 或 Run Adjoint Calculation 对话框打开时可用）；**重要：用迭代间隔时把 Run Calculation 的 Reporting Interval 保持默认 1**；④**Execute Once**——只执行一次。

## 37.20 自动初始化与 case 修改（pp. 3855–3864）

Calculation Activities 勾 **Automatically Initialize and Modify Case**——case 从 Run Calculation 任务页、Workbench 或 batch 运行时，在初始化前/后及计算过程中自动执行文本命令。启用后 Original Settings 恒存在不可删；未初始化的 case 点 Edit 打开 **Case Modification Manager** 对话框。**Auto Initialization Method** 三选：Initialize with Values from the Case（用 Solution Initialization 页设的值——**该选项不执行 Hybrid 初始化，即使任务页选了 Hybrid**）；Use Solution Data from File（读入 data 文件作初值）；Use Existing Solution Data（相当于改值续算——迭代计数重置 0 以应用修改；无解数据时的首轮运行也用它）。**任何时候 case 初始化迭代计数都归 0**。Manager 内可编辑 **Pre-Initialization**（初始化前修改）、**Original Settings**（原始设置修改 + Iterations/Time Steps after Modification）或 **New...** 新建修改；命令用 Up/Down 排序、Copy/Delete 复制删除、Export.../Import... 导入导出 .tsv。**注意**：需要后续提示应答的命令（数字/文件名/yes-no）必须把应答一并写入——否则不执行（yes/no 问题默认按 yes）；多条命令可以 `/` 开头或换行分隔。示例流程照录：Velocity-inlet-5 算初值 → 迭代清零初始化 → 算 100 步 → CFL 设 3.5 → 再 75 步 → 湍动能改二阶迎风 + CFL 2.5 → 再 1000 步。**Original Settings 的命令在第一迭代/时间步之前应用**；关闭该选项后设置保留但不生效；启用时 Run Calculation 页的设置被忽略（Number of Iterations 变 Automatic）；已算过部分迭代后再改 Modify Case 设置会提示是否继续。

## 37.21 解算动画（pp. 3864–3875）

计算中可对 mesh（主要动网格）、contours、vectors、pathlines、particle tracks、scenes、XY plots、report plots、residuals、dashboards 建动画；按指定间隔捕获帧；算完回放、改视图（mesh/contour/vector/pathline/particle tracks）并存为图片序列或 **MP4** 视频；另有 keyframe 动画（p. 4272）。
- **37.21.1 创建 Animation Definition**（Solution → Activities → Create → Solution Animations...）：Name；**Raytracer Image**（真实感渲染）；**Record after every** + Iteration/Time Step/Flow Time 定帧频；**Storage Type** 六选——**In Memory、PPM Image、HSF File、PNG Image、JPEG Image、TIFF Image**。要点：HSF 高度压缩、可用 iOS/Android 的 HOOPS Viewer 交互查看；PPM 序列可用 ImageMagick `convert -adjoin sequence-2_00*.ppm sequence2.gif` 合成 GIF；**In Memory 不支持等值线的 Contour Lines 与 3D 样式矢量图**。Storage Directory 默认与 case 同目录（相对路径 `.`——**手动指定则为绝对路径，case 换目录不自动更新**）；可设 Animation View（Preview / Use Active）；可勾 Append File Name With（time-step/iteration/flow-time + Precision）；Animation Object 列表九类（Mesh/Contours/Vectors/Pathlines/Particle Tracks/LICs/Volumes/Scene/XY Plot/Report Plot——**勾 Raytracer 才会露出 Volumes**；选 residuals 需在 Residual Monitors 开 Plot）。**创建指南**：灯光要在计算前定义；等值线/矢量要固定色标须关 Auto Range；Scene Description 的高级场景操作不进动画帧（跨对称面镜像等视图修改会进）；带标题的动画在计算前先显示标题。
- **37.21.2 回放**（Results → Animations → Solution Animation Playback）：播放/倒放/逐帧（±1）/快进快退（Increment 跳帧）/Stop；Frame 滑块跳帧；Replay Speed 滑块调速；Start/End Frame 播片段；Playback Mode——Play Once（默认）/ **Auto Repeat**（循环）/ **Auto Reverse**（往复）；双击缓冲（Display Options 的 Double Buffering）减闪烁；HSF 与 In Memory 3D 动画可关 Use Stored View 回放中改视角；改选序列会丢失视角修改；**HSF 动画可加注解**（Annotate；可附加 Date/Version/Flowtime——显示不了的值标 <Not Available>）；删除序列——**带 Animation Definition 的序列须删定义对象**（Outline View 右键），In Memory 序列删除即永久丢失（先存盘）。
- **37.21.3 保存**三种：**Solution Animation File**——HSF/PPM 存储类型自动存 `.cxa`（帧清单）+ 每帧 `.hsf`/`.ppm`；In Memory 的 `.cxa`+`.hmf` 退出即失——Playback 对话框 Write/Record Format 选 **Animation Frames** → Write 保存（`.cxa` + 每帧 `.hmf`，存当前工作目录；可独立于 case/data 回放）；**Picture Files**——每帧一图（供 ImageMagick 等外部工具；Picture Options 设参数——勿点其 Save...，从 Playback 的 Write 出图；**AVZ 与 VRML 不支持**）；**Video File**——**MP4/AVI/FLV/MOV/MPEG**（MPEG 在 Ubuntu 不支持保存；MPEG 省盘但画质较低；Video Options **学术许可不可用**）——Video Name + 格式 + **FPS** + **Resolution**（Use Original Resolution（可 Scale）/4K/2K/WUXGA/1080p FHD/720p HD/480p SD/custom 宽×高）+ Quality + Advanced Quality Options（Bitrate Quality、**H.264** 压缩）；偏好设置存于 Preferences → Graphics → Save Video Settings（学术许可不适用）。
- **37.21.4 读取**：Playback 对话框 Read... 读回 `.cxa`——**可读入任意 Fluent 会话，无需对应 case/data**。

## 37.22 case 设置检查（Case Check）（pp. 3875–3888）

求解前 Solution → Run Calculation → **Check Case...**——无问题弹信息框；有问题打开 Case Check 对话框，按 **Mesh / Models / Boundaries and Cell Zones / Materials / Solver** 五选项卡给最佳实践建议。两种实施方式：**Automatic Implementation**（逐条 Apply 勾选 → 底部 Apply 统一自动应用——控制台通知并询问是否存 case，选 No 则退出丢失）与 **Manual Implementation**（给出操作路径自行改；每条右侧 ? 为帮助链接）。规则清单：
- **Mesh**：读入/修改网格后立即 Check；Minimum Orthogonal Quality < 0.01 → 先改善网格质量（Report Quality）；动网格算例**先 Preview Zone Motion 再 Preview Mesh Motion**（zone motion 快速验证刚体运动设置、不改网格；mesh motion 验证网格有效性——含变形与非刚体动态区； prescribed motion 的动网格必须做 mesh motion 预览）；轴对称几何有 x 轴以下节点 → 平移网格（轴对称单元体积由绕轴旋转生成、负 y 节点产生负体积）。
- **Models**：标准 k-ε → 考虑改 **Realizable k-ε**（新湍流粘度公式 + 由平均涡量涨落精确输运方程导出的 ε 输运方程）；**DO/Energy coupling 仅光学厚度 > 10 时用**；S2S 模型不给 view factor 计算的边界温度设为合理值（默认按环境 300 K）；混合平面模型 URF 设 1.0；动网格 + remeshing 时同时启用 smoothing；热力 NOx 湍流流动要设 NOx Turbulence Interaction Mode（Fluent 用 PDF 法）；Mixture + Singhal 空化 → 考虑改 **Schnerr-Sauer 或 Zwart-Gerber-Belamri**。
- **Boundaries and Cell Zones**：轴对称中心线用 **axis** 边界；**outflow 与 pressure inlet 不兼容**（改 velocity/mass-flow inlet）；**outflow 与 ideal gas 密度不兼容**（非稳态变密度也不行）；ideal gas + 非零 operating pressure 会加到表压上（注意）；**可压 ideal gas 的压力边界不要设 0**（等熵关系需要正压）；流动边界湍流参数默认值（Backflow k/ε/ω 均为 1）需复核或换 Turbulence Specification Method；shell conduction 必须给每层非零 Thickness；**VOF 进出口体积分数只能 0 或 1**；Mixture 与 Eulerian 多相**不能用 outflow**（明渠 VOF 例外）；流体区指定 Mesh/Frame Motion 时所有壁面应设 Moving Wall（Relative to Adjacent Cell Zone；绝对系静止除外）；动流体区要给非零旋转/平移速度；mass-flow-inlet 与 velocity-inlet 的默认值需复核；换热器模型必须定义多孔区（macro 单侧、dual cell 双侧）。
- **Materials**：组分输运 + 体积反应 → 各流体 Cp 用温度多项式；boussinesq 密度需非零 Density 与非零热膨胀系数；辐射模型要复核吸收系数默认值。
- **Solver**：流体边界 Mesh Motion → General 必须 **Transient**；梯度建议 **LSQ Cell-Based**（不规则非结构网格精度同 node-based、代价更低）；能量 URF 设 0.90–1.0（应用建议自动设 0.90）；VOF 压力离散建议 PRESTO!（高旋流/高 Rayleigh 自然对流/高速旋转/多孔/强弯曲域）。

## 37.23 收敛与稳定性（pp. 3888–3896）

- **37.23.1 判断收敛**：**无普适标准**——不仅看残差水平，还要监视相关积分量（阻力、换热系数等）。默认判据：全局缩放残差降至 1e-03（能量与 P-1 为 1e-06，即 1e-06——原文两处符号占位，按 37.17 默认值补全）。默认判据的局限：连续残差按前 5 迭代行为缩放——**初 guess 越好连续残差反而越高**（反直觉）；全局缩放因子依赖解水平——残差显著低于目标但解仍在变（能量方程最常见）；湍流量差初值导致高缩放因子——残差先低后升再降。**良好实践：残差持续下降（或保持低位）数十步（如 50+）再认定收敛**。局部缩放残差（稳态判据 1e-05、瞬态 1e-04）更普适（连续残差判据可按工况调）。另一常用做法：**unscaled 残差降三个量级**（用归一化实现）——但三种情况不适用：初值很好（近等温流动能量残差降不满）；非线性源项从零缓慢建立（封闭腔自然对流初动量残差近零）；变量本身处处近零（充分发展管道横截面速度为零）。**初值很差时三量级下降也不保证收敛**（k-ε 方程尤甚——好初值难给）。总之以积分量为准；未收敛可收紧判据（p. 3843）。
- **37.23.2 分步求解**：复杂问题逐项解决——传热先算等温流；湍流先算层流；反应流先算部分收敛的非反应流（可含组分混合）；离散相（液滴蒸发）先解气相。经 Solution Controls 的 **Equations 对话框**逐方程临时开关。**37.23.2.1 选方程子集**：典型流程——关能量方程算等温流场（**仅压力基可关能量；密度基能量与流动耦合求解不能单关**）→ 能量场收敛后重开；能量初场计算时可关动量与连续，能量收敛后再开；物性不随温度变则可不开流动方程。**告诫**：温度相关物性时关能量前确保全域温度值真实（否则物性失真、流场受损）；温度初始化/patch 见 p. 3765。**37.23.2.2 反应开关**：组分混合先行——完整设好含反应的 case 并保存；Species Model 关 Volumetric Reactions 只解混合 → 部分收敛后重开 → 从部分收敛数据继续；燃烧问题重启前可在预期反应区 patch 高温（p. 3768）。
- **37.23.3/37.23.4**：AMG 参数与多级参数调整见前（37.5、37.7）。
- **37.23.5 劣质网格稳健性（Poor Mesh Numerics）**：劣质网格 = 高斜/高度非正交/非凸/左旋面单元——默认启用 **poor mesh numerics** 修正（默认只作用于正交质量为 0 的单元）。读入含损坏度量的网格会有控制台告警（建议 `/mesh/check` 与 `/mesh/repair-improve/report-poor-elements`；修复见 p. 1293）。**除左旋面外的劣质网格可保二阶精度：用 warped-face gradient correction + 关闭 poor mesh numerics**（`solve/set/poor-mesh-numerics/enable?` no）。局部解修正三档：**0 阶**（坏单元解由周围好单元直接组装——误差与网格尺寸无关）、**1 阶**（局部低阶离散 + 忽略部分非正交梯度贡献——**默认**）、**2 阶**（仅从周围好单元梯度组装坏单元梯度矢量——保持网格收敛行为）。**强烈建议默认 1 阶**（精度/稳定性折中）；坏单元少可试 2 阶；全失败再试 0 阶（最稳最不准——强非线性物理区可能高度非物理）。三档只应作用于小比例单元；耗时随坏单元数线性增长（1 阶最快；0/2 阶相近）；**大比例单元被标记时建议弃网重建**。补充控制：`orthogonality-enhancing-cell-centroids?`（重定位坏单元质心增强正交性度量；全网格类型可用；提高阈值更稳但损精度；度量仅求解模式可见）；扩大作用范围的判据命令——`cell-quality-based?`（正交质量 ≤0.05，`set-quality-threshold` 可调）、`gradient-quality-based?`（按单元梯度质量判据；仅压力基；不支持周期边界；可后处理 Gradient Quality Measure——坏单元近 0、好单元近 1；等值线建议 Filled+关 Node Values）、`solution-and-quality-based?`（解与质量联合判据、按迭代/时间步频率检查；仅压力基；可后处理 Solution and Cell Quality Measure——坏单元及邻域为 1）、`register-based/`（按 cell register 指定——new/edit/delete/list/list-properties；register + frequency/（single-execution 手动或 iterations/time-steps 自动标记，自动默认每迭代）+ active? + verbosity；**手动标记后改动网格需用 active? 先 no 后 yes 重标**）；非预混/部分预混燃烧初始化或读数据时**自动创建名为 `pmn_pdf_stability_marker` 的 register 定义**（默认停用；启用可提升 PDF 表燃烧稳健性——见 p. 2632）。register 纳入 report-poor-elements 统计（含邻域、总数更大）。辅助命令：`print-poor-elements-count`（分判据打印标记数）、`reset-poor-elements?`（重置；内部网格检查识别的坏单元保留）、`turbulence-production-term?`（湍流模型专属处理——覆盖标准 k-ω/BSL/SST/GEKO 及其 SAS/DES/SBES 与代数/一方程转捩组合、Transition SST）。
- **37.23.6 Warped-Face Gradient Correction（WFGC）**：改进所有梯度法（cell/node/least-squares）的梯度精度——推荐 3D 多面体/六面体/混合网格；**读入含多面体的 3D 网格时默认启用**（向无多面体网格 append 多面体网格则需手动在 Solution Methods 开）；也适用于相邻单元体积差异巨大（悬挂节点 hex）的情形；解决高长宽比、边界层非平面面、形变严重（质心落在控制体外）单元的梯度精度退化。两模式：**fast mode**（静态网格不增梯度计算时间——GGNB+湍流模型除外；基本流动约 **+22% 内存**、不随模型增加）与 **memory saving mode**（不增内存、静/动网格迭代变慢）——**任务页启用即 fast mode；切 memory saving 用 TUI `solve/set/warped-face-gradient-correction/enable?` 并对 use fast mode? 答 no**。**WFGC 不修正左旋面单元——含左旋面必须用 poor mesh numerics**。
- **37.23.7 能量方程数值噪声滤波器**：物性剧变处（耦合壁热容、相变燃烧变量）能量场产生数值噪声，高阶离散下残留并污染解、可致发散。压力基可用噪声滤波器——在噪声区施加数学极值条件去除（略降该区精度、增稳健；噪声消除后不再施加以恢复高阶精度）。`solve/set/advanced/energy-numerical-noise-filter` 开关（**默认关**）；能量发散或非物理的疑难算例建议**从仿真开始就用**，而非从中途数据启用。

## 37.24 Solution Steering（pp. 3896–3903）

密度基隐式的专家系统——从初猜导航到收敛解、最少用户干预：用户只选流动类型与目标精度，求解器幕后调参。**仅密度基隐式稳态可用**。
- **37.24.1–37.24.2 概览与策略**：可用条件四项——Solver Type = Density Based、Formulation = Implicit、Time = Steady、数据有效（已读 data 或已初始化）。流程 = **FMG 初始化 + 两阶段**：**Stage 1**——最大稳定性导向：解从一阶精度渐进提到最高精度（用户指定、典型二阶），CFL 恒定低位；**Stage 2**——CFL 定期调整猛推收敛并防发散（定期分析残差史决定升降 CFL）。流动类型五选（无精确马赫数分界，仅指引）：**Incompressible**（常密度）/ **Subsonic**（可压 M<0.75）/ **Transonic**（0.65<M<1.2）/ **Supersonic**（1.10<M<2.5）/ **Hypersonic**（2.0<M）。
- **37.24.3 使用**：默认禁用；满足条件后 Run Calculation 勾 **Solution Steering** 展开主控——选 **Flow Type** + **Use FMG Initialization**（默认开——阶段 1/2 前做 FMG）+ **First- to Higher-Order Blending**（默认 **100%**；流方程未选二阶迎风时灰显；100% 收敛不了可降 75%/50%）+ Courant Number（只读显示当前 CFL）→ **Calculate**；亦可调迭代数或 More Settings... 自定义。**Solution Steering 对话框两选项卡**：**Steering Settings**——Explicit Under-Relaxation Factor（按所选 Flow Type 定默认，一般不改）；Stage 1 的 Duration（迭代数，CFL 用 Courant Number 组 Initial 值）；Stage 2 的 CFL 更新时机（**Immediately（默认）** 或 After N 迭代滞后）与 **Courant Number Update Interval**；Courant Number 组 **Initial/Maximum**（算法不允许超最大值，但发散时允许低于初始值）；**Linear Ramp-up**（勾选则 Stage 2 的 CFL 主动调节改为线性爬升——从 Initial 到 Maximum 按 Iterations 数；检测到发散会自动降）；Default 按钮复位。**FMG Settings 选项卡**：多重网格层数、每层循环数、FMG Courant Number——默认值由流动类型/网格规模/维度决定；Default 复位。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3709–3758（批次 102，2026-10-20，pypdf layout 模式提取）。
- Theory Guide Eq 23.x/37.1 公式体未提取，按引用记录变量与语义；个别符号占位（SIMPLEC 粘度 URF 提及的 k/ε 记号、NITA 压力松弛 0.7–0.8 后的顿号）在文本层缺失按语义记录；"MDM"（NITA 可能不稳清单）原文如此照录。
- Figures 37.1–37.12（任务页/对话框截图）为图形元素未摄取；TUI 提示串与 verbosity 样例输出照录。
- 版本敏感：默认值（CFL 1/5/200、Pseudo Time Courant 5、显式松弛 0.5/0.75、HOTR 0.25/0.75、Instability Detector 25/1000 m/s、AMG Max Cycles 30、Coarsen by 2/4/8、CASM 乘子 100）与命令可用性（correction-form 将移除）以 2026 R1 为准。
- 相关页面：[[Fluent 湍流模型设置]]（SRS 模型/BCD）、[[Fluent 多相流模型]]（多相默认离散与 NITA）、[[Fluent 熔化与凝固]]（压力基专属模型清单）。
