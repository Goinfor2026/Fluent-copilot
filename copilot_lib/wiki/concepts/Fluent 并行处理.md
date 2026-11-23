---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - parallel
  - mpi
  - partitioning
  - load-balancing
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 并行处理

## 摘要

User's Guide 2026 R1 Part III / Chapter 44 "Parallel Processing"（PDF pp. 4525–4584，八节）与 Chapter 45 "Running Ansys Fluent on Arm Compute Nodes"（PDF pp. 4585–4588，五节）。**摄取状态：Ch.44–45 全章完成（批次 121–123，pp. 4525–4588）。**

## 44.1 并行处理引言（pp. 4525–4527）

- 架构：Fluent + **host 进程**（不存网格/解数据，只经 **cortex** 解释图形接口命令）+ 一个或多个 **compute node** 进程。并行时网格与数据拆成**分区（partitions）**、每区分配给一个计算节点——分区数 ≤ 可用处理器数；**扩展性（scalability）**：节点增多求解时间下降，但超过某点后网络通信占比上升、并行效率降低——**系统规模要匹配**。
- 通信拓扑：host 经 socket 连到 **compute-node-0**（专用节点），由其分发到其余节点；节点间全互联，靠消息传递库（如 **MPI**）完成数组收发、同步与全局操作（如全域求和）；节点到 host 的通信只能经 compute-node-0 且须全部节点同步。所有进程有唯一整数 ID。
- **44.1.1 推荐流程**：Launcher 选 case → 指定进程数启动 → 复查/必要时重新分区（p. 4571；也可在串行或并行求解器手动分区，见 44.5）→ 计算（性能检查见 44.8）。**告诫：异构集群（操作系统或处理器家族差异）下 MPI 实现限制可能非最优甚至失败——谨慎使用**。

## 44.2 经 Fluent Launcher 启动并行（pp. 4528–4537）

Parallel (Local Machine) 设 **Solver Processes > 1** 即并行。**Parallel Settings 选项卡**：
- **Interconnects**——默认设置推荐（SMP 用共享内存；Windows 自动选最佳；Linux 可选 ethernet / **ethernet.efa** / infiniband / infiniband.ofed / infiniband.psm3，详见 Tables 44.4–44.6）。
- **MPI Types**——随架构而异（Tables 44.1–44.6）；**interconnect 与 MPI 兼容性由用户负责，不兼容输入时 Launcher 回退默认值**。
- **Run Types**——**Shared Memory on Local Machine**（本机共享内存并行）或 **Distributed Memory on a Cluster**（跨机分布式）：Machine Names 直接列表（逗号/空格分隔，长列表不推荐）或 **File Containing Machine Names**（hosts 文件；不在工作目录须全路径——否则报 `Error: file "hosts.txt" does not exist!`）。**rank 分配默认按机器连续块、块尽量均衡**——`machine X:Y` 语法控制每机块大小（Y 为该机进程块数）；全轮转分配设块大小为 1（machine1:1,machine2:1,...）。
- **GPU Remap**（需 Home 选项卡已开 Native GPU Solver——见 [[Fluent GPU 求解器]]）；**Select IP Interface**（等价 `-host_ip=host:ip`——多机分布式且安全软件掐断 socket 报 `The fl process could not be started.` 时，优选给 Fluent 加白名单，否则选合适 IP 接口）。
- **44.2.1 调度器选项（Scheduler 选项卡）**：Windows 64 + MSMPI → **Microsoft Job Scheduler**（Compute Cluster Head Node Name——在头节点上运行则留空；**Start When Resources are Available** 等 Fluent 到资源就绪再启动）。Linux（或 Windows 勾 Use Remote Linux Nodes）四选——
  - **LSF**：可开 Use Checkpointing（Checkpointing Directory 默认当前目录 + Interval of Automatic Checkpointing 分钟间隔）。
  - **SGE**：SGE qmaster（默认 localhost）/ SGE Queue / SGE pe（留空用默认）；或 SGE Configuration File。
  - **PBS Professional**、**Slurm**：Slurm 有 Account、Custom Option、**Processes Per Node**、**GPUs Per Node**（需 Native GPU Solver）。
  - 部分调度器通用选项：**Submission Host**（本机不能提交作业时指定提交主机；LSF/PBS/Slurm）、**Queue**（Slurm 为分区名；LSF/PBS/Slurm）、**Node Only**（Cortex 与 host 先启动、只把并行节点进程提交给调度器）、**Tight Coupling**（SGE/PBS——Linux 原生远程节点访问机制）、Slurm/SGE 默认独占模式（环境变量 `FL_SCHEDULER_EXCLUSIVE=0` 关闭）、LSF/PBS 的 `FL_SCHEDULER_PPN`（每节点进程数）与 `FL_SCHEDULER_GPN`（每节点 GPU 数，需 GPU 求解器）。**Linux 调度器下图形性能差**：改 Cortex 运行机器——Graphics Rendering Machine 三选（First Allocated Node——不可与 Node Only 同用 / Current Machine / Specify Machine）；**Tight Coupling 在 Cortex 于作业提交后启动（非 Node Only 默认）并经 Current/Specify Machine 运行时不生效**；Exceed onDemand 用 Current/Specify Machine 须设 `CORTEX_PRE=ssrun`（例：`CORTEX_PRE=/opt/Exceed_connection_server_13.8_64/bin/ss-run`）。Microsoft HPC Pack 2008+ 另有 Job Template / Node Group / Processor Unit（Core/Socket/Node）选项。Launcher 不含部分命令行调度器选项（stderr/stdout 文件——见 p. 208）。
- **44.2.2 远程 Linux 机器附加选项（Remote 选项卡）**：勾 **Use Remote Linux Nodes** → Remote Fluent Root Path（如 `path/ansys_inc/v261/fluent`）+ Remote Working Directory；Remote Spawn Commands——**SSH**（默认；须免密 SSH）或 Other 兼容远程 shell；Use Remote Cluster Head Node 指定连接的远程节点（不填用机器清单第一台；SGE/PBS/Slurm 下由 Submission Host/qmaster 承担）。命令行等价选项照录：`-nodepath=`、`-node0=`、`-nodehomedir=`、`-rsh=`（默认 ssh.exe、不得等待密码输入）。**cygwin 混合启动有已知问题——用 cmd.exe**。**混合 Windows/Linux + UDF 两注意**：主机上打开读写的文件远程节点不可见（需主机/节点间手工传输）；**同一会话不能加载多个 UDF 库**——变通：多 UDF 编进同一库。
- **44.2.2.1 远程 Linux 机器的调度器设置**：LSF（Use Checkpointing/Directory/Interval）、SGE（qmaster 默认 localhost、Queue 留空用默认、pe 留空用默认并行环境）、PBS Professional、Slurm（Account/Custom Option/Processes Per Node/GPUs Per Node）；通用——Submission Host 与 Queue（LSF/PBS/Slurm）。**重要**：远程 Linux + 作业排队等资源时 **GUI 保持打开直到资源可用并开始运行**。图形性能差可经 `-scheduler=<scheduler>` + `-gui_machine=<hostname>` 或 Scheduler 选项卡指定 Cortex 机器；Slurm 下动态派生（meshing↔solution，p. 228）也需此指定。

## 44.3 Windows 上启动并行（pp. 4538–4543）

命令行语法：`fluent <version>-t <nprocs> [-p <interconnect>] [-mpi=<mpi_type>] [-cnf=<hosts>]`——version = 2d/3d/2ddp/3ddp；`-t` 进程数（有 -cnf 时用 hosts 清单前 n 台；CCS 除外）；`-p` 互连（缺省 ethernet）；`-mpi=`（缺省 Intel MPI，**>64 逻辑核用 Microsoft MPI**；推荐默认）；`-cnf=` hosts 文件（不选则本机；不在当前目录须全路径；**文件名不能含空格**；hosts 条目**末尾必须空行**；多处理器机器可重复列出以占多核；`machine X:Y` 块分配同 44.2）。例：`fluent 3d -t4 -cnf=hosts.txt`。Tables 44.1–44.3 照录：win64 互连 = ethernet（默认）/infiniband；MPI = msmpi（SHM 与 HPC 调度器；>64 核默认）与 intel（DMM；<64 核默认）；InfiniBand 仅 msmpi。**44.3.1.1 Microsoft Job Scheduler**：`-ccp <head-node-name>`（CCS 包；例 `fluent 3d -t2 -ccp head-node-name`）；**Intel MPI 不支持 Microsoft Job Scheduler**；MS-MPI 自动选最佳互连。进阶：①先请求资源再启动（`job new /scheduler:... /numprocessors:2 /rununtilcanceled:true` → `job submit ...` → `job view` → `fluent 3d -t2 -ccp head-node-name jobid=<job-id>`，可复用直至 `job cancel`）；②`-ccp head-node-name jobid=-1` 延迟启动待资源分配（Cancel 清理退出）；③**XML 模板文件**作业（照录模板骨架——SoftwareLicense/Max-Min Processors/Runtime/IsExclusive/Tasks 的 CommandLine 指向共享目录 fluent.exe + `-i bs1.jou`；`job submit /jobfile:job1.xml`；**journal 必须在运行结束时退出 Fluent**）；④无 GUI 批模式（`job submit /scheduler:... /numprocessors:2 /workdir:... fluent.exe 3d -t2 -i bs1.jou`；CCP 或 CCP client 工具的机器都可提交、版本须一致）。

## 44.4 Linux 上启动并行（pp. 4543–4546）

GUI 同 44.2。命令行语法同 Windows：`fluent <version>-t <nprocs> [-p <interconnect>] [-mpi=<mpi_type>] [-cnf=<hosts>]`——`-p` 缺省**自动选最佳互连**；`-mpi` 缺省用该互连默认（推荐）；hosts 文件规则同前（也可直接 `-cnf=machine1,machine1,machine2`）。例：`fluent 3d -t4 -pinfiniband -cnf=fluent.hosts`。**告诫**：无加速图形的集群上 Fluent 可能不接受键盘输入——设环境变量 `QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb`。
- **44.4.2 Secure Shell 客户端设置**：见 p. 4546 段（跨入下批，届时补记）。
- Linux 平台 Tables 44.4–44.6（互连/MPI/架构对照，p. 4545）照录要点见原文表（跨机以太网、EFA、InfiniBand 各系 MPI）。

## 44.5 网格分区与负载均衡（pp. 4546–4576）

### 44.5.1 概览（pp. 4546–4548）

并行求解器须把网格分区到各处理器。**推荐：读入未分区网格时自动分区**（44.5.2）；也可在串行或并行求解器手动分区（44.5.3/44.5.4）。**自适应过程中单元相对分布保持——自适应后无需手动重分区**（Load Distribution，p. 4575）。串行设置再分区的路径要求主机内存够读入网格；网格过大可直读并行求解器自动分区后再设置。**Fluent Meshing 并行建网**：meshing 模式的分区在节点数相同时读入求解器保留；**不均衡的四面体/棱柱网格读入时会自动重分区**（无论节点分布差异）。
- **44.5.2 自动分区**：Parallel → General → **Auto Partition...**——Case File 选项开（默认）= 按 case 文件已有分区；关掉后：Method 下拉（见 Partition Methods p. 4564）、**Across Zones**（默认开——允许分区跨区界；关掉会过度细粒化损性能、**对 Metis 无效**）、Principal/Cartesian Axes 法可开 **Pre-Test**（p. 4570）→ 读 case。**默认 Metis + Laplace smoothing**（相邻高拉伸单元归组，显著改善收敛与扩展性）。**架构感知重分区**：读 case 时自动执行——**跨机通信降 >5% 即采用新映射**并打印（例：`inter-node communication reduction by architecture-aware remapping: 47%`；实际求解提速可能略低）。**44.5.2.1 高级自动分区偏好**：Preferences → General → Advanced Partitioning Method For Better Convergence 两选——**Laplace Auto-Partition**（2023 R2+ 写的 case、Metis 法直接用 case 内单元组信息；Metis 默认）与 **Laplace Auto-Repartition**（2023 R2 前的 case、重分区+迁移时生成组信息；任意法可用）。**44.5.2.2 分区中报告**：过程信息打印控制台；完成后可经 Partitioning and Load Balancing 对话框出报告——**Print Active/Stored Partitions** 打印各分区 ID/单元数/面数/界面数/界面-面比与 min/max 变差（解读见 p. 4571）。
- **44.5.3 手动分区与负载均衡**：自动分区为推荐做法；分区后可检查（p. 4571）与重分区。**44.5.3.1 指南**：①默认 **Metis** 分区（多数问题最佳；Cartesian Axes 为低内存替代）；②查分区统计——**目标：最小化分区边界面数比的最大值，同时保持负载均衡；Mean cell count deviation 衡量最大负载不均**；不满意换他法。
- **44.5.4 Partitioning and Load Balancing 对话框**（Parallel → General → Partition/Load Balance...）：
  - **Partitioning**：Method 选法；Number of Partitions（**必须能被进程数整除**）；Reporting Verbosity；Across Zones（默认开，Metis 无效）；**Metis 的 Laplace Smoothing**（防分区边界穿过高长宽比单元区、改善流动与 CHT 收敛扩展性）+ **Cutoff Aspect Ratio**（≈分区边界允许的最大长宽比）；**Reordering Method** 二选——**Architecture Aware**（默认；计入系统架构与网络拓扑重映射；**单机不可用**）或 **Reverse Cuthill-McKee**（最小化节点连接矩阵带宽、不涉架构）——初载 case 后点 **Reorder** 重排分区，报告更优映射与跨机通信改进潜力（显著如 >5% 则点 **Use Stored Partitions** 采用；大传输或写 case 重读亦可；已重排或单机则无改进并打印；**重排特定于当前并行配置——机器数变化须重做**）。
  - **Optimization 选项卡**：**Merge 与 Smooth** 两优化法（勾选 + Iterations 上限；0 = 不限直至满足判据）；Principal/Cartesian Axes 的 Pre-Test。
  - **Zones/Registers**：默认全选全域分区；可给所选区/register **指定分区 ID**（0 到 N−1）——梯度已知高处标区并给同 ID 防止分区边界穿过（助收敛）；并行下并行没有的网格操作工具也可借指定 ID 使工具可用（并行跑时设好后点 **Use Stored Partitions** 生效；示例见 p. 4558）。
  - **Weighting 选项卡**（分区前设权重改善负载均衡与总体性能；可依赖 Fluent timers 设权或改 User Specified；或用 **model-weighted partitioning** 按单元数与所用模型自动计权）：**Faces per Cell**（混合/多面体网格有益；User Specified 时 = 面数 + Additional Cell Weight，默认启用、附加权重默认 **2**）；**Solid Zones**（默认有固体区时启用；相对流体权重通常 <1——model-weighted 默认 **0.1**；**固体单元数须在总数 30–70% 内否则 model-weighted 不计固体**）；**VOF**（geo-reconstruct 自由面重建不均衡——仅 VOF+几何重构可用）；**DPM**、**ISAT table lookup**、**Stiff Chemistry** 权重（续下段）。

## 44.5.4（续）Weighting 选项卡余项（pp. 4556–4558）

- **DPM 权重**：DPM 颗粒相对连续相的权重（需已定义 injections；**至少跑过一步带颗粒追踪的计算后才可用**——显示 Particle Tracks 不改变权重）。计算耗时按每单元 DPM 步数统计（DPM Steps per Cell 变量可用于等值线/矢量图）；重分区后权重在下一次追踪前重置。**倾向沿颗粒主导路径分区**以减少跨界通信，但须兼顾其他模型（尤其连续相）负载——model weighting 提供整体平衡手段。**Hybrid Optimization**：DPM 混合优化分区权重法——先按模型权重切域、跨机器分区、机内再按核数分区（混合并行 DPM 法用多线程平衡机内负载）；同时均衡各分区单元数与各机颗粒数；**也适用于 DEM 碰撞模型**。
- **ISAT 权重**：Stiff-chemistry 的 Laminar/EDC/PDF Transport 模型下平衡 ISAT 表查找负载——每节点自建表、无跨节点消息传递，部分节点可能只有空气常温单条目→负载不均；动态负载均衡把单元从高载节点迁往低载节点。User Specified 值 = ISAT 占总计算量的比例。**注意：ISAT 与 Stiff Chemistry 权重同时启用时只用 Stiff Chemistry**。
- **Stiff Chemistry 权重**：平衡反应积分负载（Laminar/EDC/PDF transport 可用；**直接积分（非 ISAT）时推荐**）；Fluent 用 **flame sensor**（基于全部组分源项之和的归一化量）表示反应积分负载以均匀分布；启用后 Species... 类别出现 Flame sensor 场变量。User Specified 可设 Stiff Chemistry Weight Ratio。
- **Model-weighted partitioning**（Metis 专属）：目标 = 同时平衡单元总数与所选模型耗时——把每个启用模型当约束、自动加单元数基础约束、自动计算并平衡各约束权重。用法：选 Metis + Weighting 选项卡勾相应模型（VOF/DPM/ISAT/Stiff Chemistry 的 User Specified 与 Value 不相关）+ 确认 TUI `parallel/partition/set/model-weighted-partition` 默认开；Reporting Verbosity 设 2 可看各约束细节。
- **动网格**：remeshing/smoothing 时单元迁移使分区界面皱化、负载恶化——对话框有 **Auto Repartition**（默认；按界面面比例与负载自动判定最合适重分区间隔）与 **Repartition Interval**（强制重分区的时间步/迭代间隔；0 = 不重分区）。**注意：动网格 + remeshing 时并行更新的网格与串行（或不同节点数）略有差异——解有极小差别**。
- 步骤 8–9：**Partition** 执行；**Use Stored Partitions** 使新存储分区成为活动分区（active 用于当前计算；stored = 最近一次分区、存 case 时使用）。
- **44.5.4.1.1 示例**（Region register 指定分区 ID 全流程照录——两分区 case、region register 标区、设 ID 0 → 打印 Collective Partition Statistics → Use Stored Partitions 迁移到计算节点（输出逐分区表）→ 显示网格 → 再设 ID 1 → 再 Use Stored；串行同理）。
- **44.5.4.1.2 区内/寄存器内分区**：可对子域用不同分区法（圆柱腔用 Cylindrical Axes、矩形管用 Cartesian Axes）——不同 cell zone 逐区选法；同区内用 cell register 划分后再分。**注意：Metis 不支持区内/register 内分区**；动网格应用中每区存储其分区方法、重分区沿用。
- **44.5.4.1.3 分区中报告**：默认打印分区数/耗时/min-max 变差；Verbosity 2 另打印方法与逐分区明细；0 只报分区数与耗时。Print Active/Stored Partitions 随时重显报告。**再次强调：Use Stored Partitions 才激活存储分区**。
- **44.5.4.1.4 重置**：Default/Reset 按钮恢复默认或最近保存设置。

## 44.5.4.2 负载均衡（pp. 4561–4564）

- 并行目的 = 缩短周转时间，三途径：更快机器、更快互连、**更好负载均衡**。专用同构资源上的均衡是重点；非专用异构资源需在分区时指定负载分布（44.5.7）。默认假设每单元计算量相同——实际未必：六面体比四面体贵、有颗粒追踪的单元更贵、ISAT 组分单元耗时差异大。精确逐单元计时太贵且不可靠——改为**按模型聚合计时**（Weighting 选项卡）。运行时失衡也会动态发生（自适应/网格运动、非稳态颗粒迁移）——**动态负载均衡已实现**：按 CPU 耗时加权的模型权重迁移单元，改善 DPM/VOF/单元类型（详见 p. 4562 起正文）。

## 44.5.5 网格分区方法（pp. 4564–4569）

三目标：**各分区单元数相等、最小化分区界面数（减边界面积）、最小化分区邻居数**（减少网络与路由竞争；启动消息传递开销贵的网络环境尤重）。方案用**二分（bisection）或 METIS** 算法递归应用到子域——分区数无需为 2 的幂；按可用计算单元数创建。
- **Partition Methods 十七选（照录）**：**Cartesian Axes**（坐标二分、沿最长方向垂直切）；**Cartesian Strip**（限定父域最长方向切——常减少邻居数）；**Cartesian X/Y/Z-Coordinate**；**Cartesian R Axes** 与 **Cartesian RX/RY/RZ-Coordinate**（到笛卡尔轴最短径向距离；仅 3D）；**Cylindrical Axes / Cylindrical R/Theta/Z-Coordinate**（仅 3D）；**Metis**（Karypis-Kumar 多层级图分区——粗化→分区→反粗化；支持 model-weighted 多约束：自动分区时固体区默认 0.1 权重、手动可自控各权重；** METIS 分区可借虚拟多边形面连接性跨越非一致界面**——改善负载均衡并减少分区界面单元）；**Polar Axes / Polar R/Theta-Coordinate**（仅 2D）；**Principal Axes**（主轴方向二分 = 惯量/矩分区；**Fluent 默认二分法**）；**Principal Strip / Principal X/Y/Z-Coordinate**；**Spherical Axes / Spherical Rho/Theta/Phi-Coordinate**（仅 3D）。最有效选择因问题而异——可试不同方法（指南见 p. 4551）。
- **44.5.5.2 优化**：二分垂直最长方向启发式不总给出最小界面——**Pre-Testing**（44.5.5.3）自动选向；迭代优化两法——**Smooth**（跨分区交换单元最小化界面面积）；**Merge**（消除 orphan cluster——孤儿簇：组内每单元至少一面在界面上的单元组；**劣化多重网格性能、增加通信成本**）。两法开销较低。
- **44.5.5.3 预测试（Pre-Testing）**：Principal/Cartesian Axes 法可在正式二分前测试各方向（默认关；关=垂直最长方向切）。点 Partition 或自动分区读网格时自动进行——**测试所有坐标方向选界面最少者**。**代价：2D 分区耗时 ×3、3D ×4**。
- **44.5.5.4 分区过滤器**：File → Import → Partition → **Metis...**——对未分区网格先 METIS 分区再读入（分区数=进程数）；**要求主机内存足够跑过滤器**（不足则在内存够的机器上跑：`utility partition <input> <count> <output>` 手动分区后读分区网格）；**Metis Zone...** 可逐 cell zone 分区（少 cell zone case 的负载均衡有用）。

## 44.5.6 检查分区（pp. 4571–4575）

- **44.5.6.1 分区统计解读**：Print Active/Stored Partitions 输出两表（4 分区示例照录）。**active vs stored**：初载时相同；重分区产生 stored——**Use Stored Partitions 才把 stored 变 active**（active 用于当前计算、stored 存 case）——便于在 A 机分区、B 机求解。逐分区表字段：P（分区 ID）、Cells、I-Cells（界面单元数）、Cell Ratio、Faces、I-Faces、Face Ratio、Neighbors、Load（相对负载，见 44.5.7）；集体表字段：Cell/Face Count、Mean deviation、Partition boundary cell/face count 与 ratio、Partition neighbor count、Partition Method、Stored Partition Count。分区 ID 读 case 时直接对应计算节点 ID；**分区数多于节点数且整除时按块映射**（ID 0 到 n−1 → 节点 0……）。**目标重申：最小化 Partition boundary face count ratio 最大值、保持负载均衡；Mean cell count deviation 为负载不均度量**。**overset 附加表**：已初始化的 overset 网格多一张 Solve-cells/Dead-cells/Ext donors 统计表（overset cell marks 见 p. 1278）。
- **44.5.6.2 图形检查**：Contours 对话框——Cell Info... 类别选 **Active Cell Partition / Stored Cell Partition**、**关 Node Values**（须先初始化才能用 Contours）。

## 44.5.7 负载分布（p. 4575）

处理器速度差异大时用 `parallel/partition/set/load-distribution` 指定负载分布——例：三节点一快两慢 → 负载向量 (2 1 1)（分区 0 单元数两倍）；**须让 compute node 0 在快机上启动**（分区 0 映射到节点 0）。替代：开负载均衡让 Fluent 自动分辨节点负载差。

## 44.5.8 疑难（p. 4575–4576）

`#AMG# Warning: The global matrix size (...) is too large...` 提示分区问题。可能原因与对策：①固体区导致某分区流体单元过少——**用 Metis + Solid Zones weighting + model-weighted partitioning**（固液权重如 0.1）；②设置了负载分布导致分区过小——用 load-distribution 命令把各分区值改回 1；③shell conduction 等模型设置封装单元导致粗化困难——换分区法或开全局粗化检查：`(rpsetvar 'amg/parallel/global-check-coarsening? #t)`；④耦合壁被 shell conduction 与 S2S 模型封装——**关闭增强封装回退 16.0 前例程**：`define/models/shell-conduction/enhanced-encapsulation?`。

## 44.6 线程控制（pp. 4576–4577）

Thread Control 对话框（Parallel → General → Thread Control...）控制每机最大线程数三选：**Number of Node Processes on Machine**（默认 = 每机 Fluent 节点进程数）；**Number of Cores on Machine**（= 操作系统报告核数——多线程部分占主导时充分利用资源；例：单元少而颗粒多时每机单节点进程 + 全核）；**Fixed Number**（手动定值；一般不推荐）。

## 44.7 检查网络连通性（p. 4577）

Parallel → Network → **Connectivity...**——Print 打印指定 compute node 的主机名/架构/PID/所选节点 ID（星号标记）及与其相连的机器（host 进程 ID 恒为 host；节点从 node-0 编号；全互联；节点 0 连 host）。

## 44.8 检查与改进并行性能（pp. 4577–4584）

- **44.8.1 Parallel Check**：Parallel ribbon 的 **Check**——检查五项：CPU 核过载、CPU 降频（throttled）、系统内存占用过高、有更快互连可用、分区不均（载入有效网格时）。
- **44.8.2 性能检查（performance meter）**：恒启用——Parallel → Timer → **Usage** 显示统计（472 迭代示例照录）；**Reset** 清历史。统计语义：**Average wall-clock time per iteration**；**Global reductions per iteration**（全局规约 = 全进程集合操作把向量约化为标量，如求和/最大——数量取决于算法与问题，无法从其他量推算）；**Global reductions time per iteration**；**Message count per iteration**（点对点收发数——**关系通信延迟影响**；高计数在高延迟互连（Ethernet 比 InfiniBand 高延迟）下更伤性能；总数为全处理器合计）；**Data transfer per iteration**（字节；**关系带宽影响**——随规模/分区数/物理复杂度增长）；**LE solves per iteration**（线性系统数——依赖物理与算法、与网格尺寸无关；压力基≈输运方程数）；**LE wall-clock time per iteration** 与占比；**AMG cycles per iteration**；Relaxation sweeps/exchanges；LE early protections（stall/divergence）；Total SVARS touched；Time-step updates 与耗时；Total wall-clock time；Simulation wall-clock time。
- **44.8.3 优化并行求解器**：
  - **44.8.3.1 增大 Reporting Interval**：减少残差打印/监视通信——Run Calculation 任务页改 Reporting Interval；**告诫：每个 report interval 内无法中断迭代**。
  - **44.8.3.2 加速 DO 辐射计算**：加速 DO 求解器更快（即使多花迭代，总时间更短）——`define/models/radiation/do-acceleration?` 启用；**强制一阶迎风 + 显式松弛 1.0（忽略 Solution Methods 的 DOM 离散选择）**。**44.8.3.2.1 不兼容清单**（启动时自动回退标准 DO 并打印冲突信息）：Shells、轴对称、Eulerian 多相、UDF DOM 源、UDF 发射率权重、辐射孔隙率缩放、Pixelated interior、非各向同性散射相函数、非参与介质、非一致界面。
- **44.8.4 清 Linux 文件缓存（pp. 4583–4584）**：Linux 文件缓存满会显著降性能（串行亦有、大规模并行尤甚、**AMD 处理器常见**）——I/O 活动日积月累；会话退出后 OS 不立即释放（除非 malloc 失败）；并行分配内存可能落到不同 NUMA 域、显著影响性能。解法（先确认相关机器空闲）：①启动加 **`-cflush`** 选项（单独操作冲洗缓存、耗时数分钟、**无需 root**）；②启动后读 case 前在控制台或 journal 执行 **`(drop-cache)`**（瞬时清 pagecache/dentries/inodes；**需 sudo 权限执行 `/sbin/sysctl vm.drop_caches=3`**）。

**Ch.44 全章完成（pp. 4525–4584）。**


## Ch.45 在 Arm 计算节点上运行（pp. 4585–4588）

- **范围**：支持 64 位 Arm 架构扩展（**aarch64**）+ **Armv8.2-A** 扩展；Arm 版**完全运行于 Arm 系统、仅支持批模式（batch only）**——无 UI 与图形；工作流见 Figure 45.1。**不支持 Windows**。
- **45.1 安装**：向 Ansys 支持索取 Fluent for Arm 包（aarch64 安装包）→ `tar xf Fluent_install-lnarm64-26.1.0-<BID>.tar`（<BID> = build ID）→ `sh Fluent_install-lnarm64-26.1.0.sh` 按提示安装 → 设置环境。**推荐 OS：Rocky Linux 8.9*、RHEL 8.8*/9.3*（* 前置库：libICE、libnsl2、libSM、pcre2-utf16）**。
- **45.2 MPI**：包内提供 **Open MPI 4.1.8**——默认且唯一可用 MPI。
- **45.3 启动**：仅命令行，如 `fluent 3ddp -i fluid_flow.jou`——**默认即 `-g`**（无图形/GUI）。
- **45.4 调度器**：可用 **Slurm** 替代手工 hosts 文件——`fluent 3ddp -i fluid_flow.jou -scheduler=slurm`；用 *Running Fluent Using a Load Manager* 手册的标准选项。
- **45.5 已知限制清单（照录）**：GUI；图形与批图像渲染；Fluent Launcher；Meshing 模式；meshing-to-solver 工作流中的 CAD 导入；FMU；EnSight DVS 格式解数据导出；Monte Carlo（MC）辐射模型；动网格 RBF 光顺；叶轮机引导工作流中 .gtm→.def 转换；**解释型 UDF**；CFF S2S 格式 view factor 文件；**参数化研究（parametric studies）**；fe2ram 过滤器；Design Tool 约束法选 Enhanced 的伴随几何修改；几何参数化（Design 选项卡 Parameterize and Explore...）；Intel MKL；**全部 linx64 beta 特性**（原文如此）；各向异性网格自适应（beta）；Integrations：CGNS 导出（VKI）、EnSight、FENSAP-ICE、System Coupling、Icepak；Add-ons：ROM、PCB Model；Workspaces：Fluent Icing、Fluent Aero、Polyflow、Fluent Post-Analysis。


## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 4525–4555（批次 121，2026-10-20，pypdf layout 模式提取）。
- Tables 44.1–44.3 照录；Tables 44.4–44.6（Linux 互连/MPI 对照）提及结构、原文表为准；XML 模板与示例命令照录。
- Figures 44.1–44.8（架构图与对话框截图）为图形元素未摄取。
- 版本敏感：默认 MPI（Intel MPI / >64 核 MS-MPI）、v261 路径、2023 R2 Laplace 分界、model-weighted 0.1 与 30–70% 规则以 2026 R1 为准。
- 相关页面：[[Fluent GPU 求解器]]（GPU Remap/-scheduler_gpn）、[[Fluent 求解器使用]]（分区对收敛的影响）。
