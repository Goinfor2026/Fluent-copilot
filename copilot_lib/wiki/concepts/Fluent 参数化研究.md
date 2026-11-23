---
type: concept
created: 2026-10-22
updated: 2026-10-23
tags:
  - Ansys Fluent
  - parametric-studies
  - design-points
  - optislang
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 参数化研究（Parametric Studies）

## 摘要

User's Guide 2026 R1 Part III / Chapter 47 "Performing Parametric Studies"（PDF pp. 4617 起，12 节）。**摄取状态：全章完成（批次 125–126，pp. 4617–4684，47.1–47.12 全部十二节）。**

在 Fluent 界面内对含输入/输出参数的 case 直接做参数化研究——Parametric 选项卡初始化后可：增删设计点（design points）、配置作业提交（远程/本地多种方式）、监视解状态（transcript/残差/监视图）、访问各 DP 与整个研究的仿真报告（见 [[Fluent 仿真报告]]）、用 optiSLang 定义管理设计点并导出数据、用改造后的 Outline View（Case View + Parametric Study View）与 Project View 查看文件。首次初始化会提示创建专用 project 文件管理输入/输出（详见 47.12，待摄取）。**注意：参数化 TUI 在 CFD Pro 许可级别下只读。**

## 47.1 前提（p. 4618）

- 通常需已定义输入/输出参数的 .cas 文件；也可先读 case、初始化研究、再补参数。
- **所有后处理图像、绘图与量必须在更新"Base DP"设计点之前就加入设计点并配好其报告**。
- 自动 DOE 创建需安装 optiSLang（不一定要许可证）。

## 47.2 限制（pp. 4619）

- 导出 PowerPoint 报告时 XY plot 的描述不随之导出。
- 顺序更新 + 捕获报告数据时，报告相关 state 文件写到项目文件夹当前仿真目录（非报告文件夹）；不注册进项目，可忽略/删除。
- Windows 保存项目 Save As Copy 在项目目录路径 >170 字符时可能出问题。
- **Meshing 模式不支持参数**。
- 录制 journal 不捕获 Parametric Study 窗口与 Project View 的图形交互。
- 基准会话以 distributed 模式启动时不能本地并发更新。
- optiSLang 创建的设计点不能在无 GUI 的 Linux 批模式下更新。
- PPT 导出的长 named expression 表不自动跨页拆分（同 [[Fluent 仿真报告]] 46.1.1）。
- 多个 report definition monitor 合入单个报告文件时，DP 表右键菜单监视图可能缺部分 monitor——每个 monitor 数据放独立报告文件可避免。
- 项目名过长/目录过深会因路径长度限制出问题（Windows 约 256 字符）。
- 中止 optiSLang 优化的设计点批处理时，已完成的 DP 也可能被标为 failed——optiSLang 服务器不保留已完成 DP 的输出。

## 47.3–47.4 入门与 Ribbon（pp. 4619–4621）

四步：①打开 case、定义参数；②Parametric Ribbon → Study → **Initialize**（准备文件、激活其余功能区；提示建项目文件）；③用 Ribbon 或 Outline View 建研究，更新设计点生成各 DP 的解与结果；④分析（Fluent 内逐点分析或生成参数化仿真报告、跨 DP 比较）。

Ribbon 分组：**Study**（Initialize/Duplicate）；**Design Point**（手动/自动新建，入 DP 表；CSV **Import.../Export...**）；**Simulation Report**（base case、current case、含全部 DP 的整个研究三类报告）；**Update Options**（Sequential/Concurrent、Update Current/Update All、**Automatic Report Settings**；**CFD Pro 许可不可并发**）；**Update Status**（状态汇总 + Refresh Status）；**optiSLang Capabilities**（导出）；**Comparison Plot**（跨 DP 比较图）。

## 47.5 Automatic DP Report Settings（pp. 4621–4622）

对话框设置只作用于 DP 表勾了 **Capture Simulation Report Data** 的设计点；**随项目持久保存**。两组：

- **Automatically Generate Design Point Reports**：DP 更新时自动生成完整 DP 报告（不开则只捕获参数化报告所需最少数据）；开启后可选导出 **HTML**（存 DP 目录、压缩版注册进项目）、**PDF**（存 DP 目录、注册）、**PowerPoint .pptx**（存 DP 目录、注册）。
- **Automatically Generate Parameteric Report**（原文拼写照录）：当前批 DP 更新结束时自动生成参数化报告（单 DP → 更新完即出；多 DP → 全部跑完；优化研究 → 优化结束后）；最适一次性提交大量 DP。开启后可选 **Ensure All Report Data is Up to Date**（先把与 DP Report Settings 脱节的 DP 报告重新生成再出参数化报告）与 **Export HTML**（存项目仿真目录、压缩版注册）。

## 47.6 Outline View（pp. 4622–4624）

拆两视图：**Case View**（当前加载 DP 的 case/data 设置；base DP 为当前且处于 cleared 状态时可在此改 base 再重跑研究）；**Parametric Study View**（输入/输出参数、DP 表、参数化报告、绘图；右键菜单可切换当前研究、初始化 DP 数据、复制/删除/重命名研究）。当前研究加粗显示，信息显示在同名 Parametric Study 窗格。

## 47.7 设计点表（pp. 4624–4650）

DP 表默认在 Parametric Study View 显示，提供：输入/输出参数值（数值型，字符串误入自动高亮）；**Write Data** 开关（新 DP 默认关，须手动开或设 Write Data by Default 偏好）；**Capture Simulation Report Data** 开关；运行状态；列隐藏/显示定制。

- **47.7.1 定制列**：Select Visible Columns 图标或单元格右键 Manage Visible Columns → Set Visible Columns 对话框（全选/全清图标；OK 保存）。
- **47.7.2 更新**：Update Current / Update All；Update Options 选 **Sequential**（默认，当前会话依次更新标为 Needs Update/Interrupted/Queued 的 DP；中断 = Stop 按钮；Update All 中断时询问只停当前 DP 还是全部）或 **Concurrent**（新开 batch 会话、journal 驱动、沿用当前模式；**CFD Pro 不可用**——用 CFD Pro 打开曾配过并发/远程的项目会警告并转顺序更新）。远程更新有 **180 秒刻意延迟**（计算完成到结果可用/状态刷新）。
  - **Concurrent 要点**：适用于分布式内存机或同机共享内存；**base case 是所有 DP 更新的基础**——case 有 base 之外的改动时可新建研究/重置当前研究/丢弃改动；点 Update 后状态变 Queued；分布式内存把全部待更 DP 一次性发远程集群按机器可用性更新（Refresh Status 刷新）；状态为 Queued/Queued in Fluent/Updating... 时右键有 Stop Selected Design Point Update、Stop All Updating in Concurrent Session、Show Status in Web Browser（HPC Web 门户）；Updating... 时另有 Show 看 transcript/残差/监视图；可设 Enable Auto Refresh of the Status of the Design Point 偏好。提交后即可关基准会话：**共享内存机 Update All 后可关**；**分布式内存机基准会话应保持到全部更新完——提前关会删共享上下文，未启动的远程会话改耗常规求解器许可而非参数化许可**。默认并发会话耗标准 Fluent solver 许可。
  - **47.7.2.1.1 Concurrent Settings 对话框**（与 Ansys Cloud Burst Compute 对话框高度相似，www.cloud.ansys.com）：Remote（默认；可 Submit to Ansys Cloud Burst 直提云）或 Local + License Details；可提交到 Ansys HPC Platform Service 监视。分布式内存并发的前提是部署配置好 HPC Platform Service endpoint 与 HPC Configurations。
    - **47.7.2.1.1.1 Remote**：①Cluster Details——URL/Username/Password、Connect and Save（仅非云提交）；②Job Details Per Design Point——同云作业字段（云提交时 Use GPU Solver/Start Web Server/HPC licensing 选项不可用）；Capability Level：Cloud Burst 默认 **CFD Enterprise**，否则可选 CFD HPC Ultimate（仅本地集群）/CFD Enterprise/CFD Premium；本地并发会话沿用基准会话能力级别（License Type = Solver Licenses 时照搬；= HPC Parametric 时按 Shared HPC Licensing 规则递增）；**一个 DP 一个会话（一对一），并行更新多 DP**；Number of CPU Processes 定每 DP 核数，节点数由 Number of CPUs Per Node 与 CPU Processes 推出；新会话节点数同基准会话；③License Details（见下）；④Output Files Details 同云；⑤Save Settings。**Licensing Calculator** 打开 Ansys Parametric Licensing Calculator 网页算许可需求。**注意：参数化研究按指定数签出 optiSLang 许可，即使实际用不了那么多**。**2024 R1 起 HPC 服务证书不再打包于 `\v241\RSM\bin\HPCServices\certificates` 文件夹——连本地并发 DP 更新都须先生成 SSL 证书**。
    - **47.7.2.1.1.2 Local**：本地并发；可自定义每 DP 的 CPU 进程数与并发 DP 数、许可选项、启动 Fluent web server 或用 GPU solver；同样 License Details + Save Settings + Licensing Calculator。
    - **47.7.2.1.1.3 License Details**：**Solver Licenses**（标准 Fluent 许可）；**HPC Parametric**（按 optiSLang License Type：None → 标准 HPC 参数化许可；CFD Premium/CFD Enterprise/CFD HPC Ultimate → Ansys optiSLang 许可并选数量）。
    - **47.7.2.1.1.4/5 监视**：提交后经 Ansys HPC Platform 表格化查看云项目与作业、逐项目看详情。
  - **47.7.2.1.2 本地并发 GPU 更新**：GPU 求解器（见 [[Fluent GPU 求解器]]）本支持顺序参数化更新；Concurrent Settings 勾 **Use GPU Solver** 可本地并发（单台共享内存机 + 一块以上 GPGPU、研究在此机初始化）。**多 GPU 时一个 DP 独占一块 GPU（不共享）**——按 GPU 逐个派生 DP；例：launcher 选 4 GPU + 4 并发 DP → 一一对应；**DP 多于 GPU 时才有共享**。
  - **47.7.2.2/3**：Update Current / Update All 均可在 Ribbon 或 Parametric Study View 右键（Parametric Studies/Design Point Table → Update Current / Update All）。
- **47.7.3 添加 DP**：**Manual**（改输入参数值；Manual 选项 + Add Design Point；右键同）或 **Auto (with optiSLang)**（Add Design Points... → Create Design Points Using optiSLang 对话框）。
  - **47.7.3.2.1 Create DOE**：**Sampling Type**——默认可用 Koshal Linear、Koshal quadratic、Full Factorial、Full combinatorial、Central composite、Star Points；**optiSLang Pro 许可另加** D-optimal linear/quadratic/customizable、Plain Monte Carlo、Latin Hypercube Sampling、Advanced LHS、Space filling LHS、Sobol Sequence。Number of Samples/Levels（随类型，部分只读限值）；部分类型设计数未知 → 只读 **Number of Designs** 字段 + **Calculate** 按钮由 optiSLang 算。变量表：Name/Unit/Current Value/Active/**Lower Bound/Upper Bound（仅这两可编辑，默认 Current Value ±10%；取消 Active 后上下限=Current Value 作默认）**；Delete Existing Design Points 可选；Create Design Points 执行。**optiSLang 定位：按 AWP_ROOT → OPTISLANG_EXE → OPTISLANG_HOME 顺序查找**（同机/同目录/AWP_ROOT 通常可直接检得）。TUI：`parametric-study/design-points/auto-create/`。
  - **47.7.3.2.2 Create DOE and Optimize（需 optiSLang Pro 许可）**：Parameters Table 同上；**Criteria** 表（Objective + Add Objective / Constraint + Add Constraint；Name/Type/Expression/Criteria——约束用 <= 或 >=、目标用 MIN 或 MAX——/Limit；右键 Type 单元格 Delete）；**Optimization Options**：AMOP 或 One-Click（各带默认设置或 Configure Settings）；**Run Optimization Study**——Fluent 与 optiSLang 互通互建互更 DP；顺序跑用界面右下 Stop，并发跑用 Ribbon **Stop Optimization**。结果表：AMOP 含目标/约束列、违反约束 DP 红色高亮；OCO 最优设计绿色高亮。进一步分析用 optiSLang Capabilities 的 Data Export（Open OMDB in Postprocessor / Export Optimization Results into CSV）。重开已定义优化的项目再进此对话框会从 optiSLang 取回设置并可再看结果表。中止批处理 → 已成功 DP 也标 failed（服务器不留输出）。TUI：`parametric-study/design-points/auto-create/optimize/`。
    - **47.7.3.2.2.1 AMOP 设置**：Settings（**Refinement Type** Global——全局采样加点 / Local——在预期改进最大处加点；Maximum Number of Samples）；Start Iteration（Use Start Designs Only——以现有 DP 起步、不足补足/超用全部；Sampling Type——初始迭代可用全部 DOE 方案；Number of Samples）；Refinement（Global 型：Sampling Type 仅随机采样方案 + Number of Samples；Local 型：Importance of Sample Density / Importance of Local CoP（局部近似误差大处）/ Importance of Optimization Criteria（单/多目标在预期目标改进最大处、仅约束在预期可满足处加点）/ Number of Samples per Iteration；Consider Failed Designs——失败设计位置计入或忽略密度估计）；Convergence Criteria（**Target CoP**——所选响应的最小 Prognosis 系数达标即收敛；Maximum Iterations——含初始与细化迭代；Stagnation Iterations——单目标局部准则细化中的停滞停止数）。原文印刷：`Tn the local approach`（应为 In，照录）。
    - **47.7.3.2.2.2 One-Click（OCO）设置**：Maximum Number of Design Evaluations；Use MOP（用 MOP 加速收敛省评估次数——评估便宜时关掉）；Seed Value（随机成分算法的种子）；无改进 N 次评估后停止；每迭代固定评估数（不填则逐迭代可变；**上限 999**）；Use Start Designs Only。
- **47.7.4 DP 操作（右键菜单）**：Set As Current（载入当前会话；无数据则显示 Set As Current (No Data)）；Update Selected Design Point；Delete Design Point；Duplicate Design Point（复制输入参数值；一次仅单 DP）；Clear Data and Edit Values（删生成数据）；Show（Transcript/Monitor plots/Residual plots）；Change Status To（Needs Update ↔ Do Not Update）；Generate/Export Simulation Reports...（开 Generate DP Reports 对话框）；View Simulation Report（Fluent 内/浏览器）；Generate Parametric Report；View Parametric Report（Fluent 内/浏览器）。
- **47.7.5 Generate DP Reports 对话框**：对表中选中 DP 生成/导出；**未开 Write Data 的选中 DP 跳过**；**只能在已更新且有数据文件的 DP 上生成**。设置不持久、一次性；默认值取自 Automatic DP Report Settings。只做必要操作：已生成且最新的报告跳过重生成、已导出且未重生的不再导出（控制台通知）。**Regenerate Existing Report**（强制全部重生成；默认只给无报告或已过时者生成；Export HTML/PDF/PPTX 同 47.5 存储规则）与 **Automatically Generate Parameteric Report**（原文拼写照录；Ensure All Report Data is Up to Date + Export HTML）。自动生成 DP 报告选项在此不出现——完整生成每份 DP 报告更符合此场景，最少数据捕获只用于更新期省时。
- **47.7.6 CSV 导入/导出**：**Import** 注意事项——与现有 DP 数据匹配时询问覆盖或追加；Name 列忽略（命名由 Fluent 管理）；Units 列忽略（只导数值，与当前 case 单位不符时警告）；**无论 CSV 中状态如何，导入后全部置 Needs Update**；列标题必须与输入参数名完全一致否则该列弃用（Write Data、Capture Simulation Report Data 两列除外）；缺这两列时按默认初始化（Write Data 关、Capture Report Data 开），或用 Write Data by Default 偏好。**Export** 写出全部列全部数据。
- **47.7.7 网格变形（mesh morphing）**：勾 Update Options 的 **Update Mesh Morphs** 执行 Design Ribbon Parameterize and Explore 里定义的变形；有输入参数挂在变形定义上时，**更新参数值之后、解初始化之前**执行变形。**告诫：网格变形只能经此勾选框或 Calculation Activities 任务页的 Automatically Initialize and Modify Case 选项执行**。
- **47.7.8 DP 流程细节与 case 改动**：
  - **Base DP 开始更新时**：复制当前 case 作为 "base case"（DP 报告模板保留以备重置）；**之前对 case 的一切改动（新等值线、新参数、设置修改等）被此副本捕获、作用于后续全部 DP**；打开 transcript；工作目录切到初始 DP。**必须在此之前初始化并定义全部想捕获的后处理量，并配好 base case 的 DP 报告设置**。
  - **Base DP 完成时**：写该 DP 的 case 与 data（勾上下文菜单 **Use Base Data** 则把该 DP 数据赋给 base case）；捕获报告数据；关 transcript。
  - **其余 DP 开始更新时**：检查解完成后 case 是否被改——有则提示新建研究/丢弃改动/重置研究并用这些改（保证 DP 一致性）；随后加载 base case、套新参数、按要求初始化或读 Base DP 数据、继续计算。
  - **其余 DP 完成时**：按要求捕获报告数据与写 data；更新状态；关 transcript。
  - 注意：**所有输入/导出文件用相对路径**（写入当前 DP 文件夹）；用数据文件初始化时（如 Automatic Solution Initialization and Case Modification 对话框的 Use Solution Data From File），研究重置时间步/迭代/残差但用实际解数据。
  - **47.7.8.1 初始化 DP 数据（p. 4650 起，续下段）**：可用当前 case 设置、base DP 数据或先前更新的 DP 初始化——经 Parametric Study View 右键菜单选择。

## 47.7.8.1（续）初始化数据三选项（pp. 4651–4652）

- **Case Settings**（把 DP 数据赋给 case 设置）；**Base Data**（赋给 base case）；**Previous Updated**（赋给上一个已更新 DP 的数据）。Previous Updated 行为随更新方式：**Sequential**——链式 DP1→DP2→DP3（无前序数据时退回 case settings）；**Concurrent (Local)**——取最近更新的 DP 信息用于所有提交 DP；**Concurrent (Remote)**——**不支持**（全部 DP 同时提交远程集群）。三选项仅在更新 base DP 之前/之后可用。**注意：启用 Previous Updated 时 Fluent 无视 Write Data 开关、总为 DP 写数据**。

## 47.7.8.2 复用 case 文件（pp. 4652–4653）

上下文菜单 **Read Case Before Each Design Point Update**：仅适用于**顺序更新 + 只改操作条件参数 + 无网格变化（动网格/变形/自适应）**的研究。**Yes（默认）**——每次读 case；**No**——复用已加载 case 直接初始化。三场景行为表（照录要点）：①Case Settings 初始化：Yes = 读 base case → 套参数 → 初始化 → 解；No = 套参数 → 初始化（即使会话中已载 data）→ 解。②Base Data 初始化：Yes = 读 base case → 读 base DP 数据 → 套参数 → 解；No = 读 base DP 数据 → 套参数 → 解。③Previous Updated：Yes = 读上一 case/data（仅并发需要读——顺序的已在会话中）→ 套参数 → 解；No = 套参数 → 解。

## 47.7.8.3–47.7.8.4 case 改动管理（pp. 4653–4654）

- **47.7.8.3**：base DP 已最新时，增删输入/输出参数或改设置后切其他 DP 为当前——提示新建研究/丢弃改动/重置研究并采用改动。
- **47.7.8.4**：更新期间对 base case 的显式改动（DP 表输入变量之外）——同样提示，且新建/重置时可勾 **Automatically proceed with design point updates** 继续更新。该对话框在 base DP 更新后两种场景再出现（增删参数；改设置后切当前 DP）——此时无自动继续选项。

## 47.8 监视与查看 DP 更新状态（pp. 4654–4657, 4661）

- DP 表 Status 列 + Ribbon Update Status；**Show Summary...** 打开 Count of Design Points Based on Status 对话框，十种状态计数：**Needs Update、Do Not Update、Queued in Fluent、Queued in Cluster、Updating...、Updated、Updated: Converged、Updated: Not Converged、Failed、Interrupted**。
- 任一 DP 处于 Updating/Queued 状态时：Ribbon 的 Duplicate 禁用；Sequential/Concurrent 单选禁用；Study 树右键 Set As Current、Duplicate 禁用；对应 TUI 亦禁用。
- **Refresh Status** 手动刷新；可设自动刷新偏好（47.10）。右键 DP 名 → **Show:** 查看 transcript/monitors/residuals（限已更新 DP，多标签呈现；Figures 47.9–47.11）。
- **残差图告诫**：为使残差图真实反映跨 DP 的解进程，把 Residual Monitors 对话框的 Iterations to Plot 与 Iterations to Store 设为当前求解设置下可能的最大迭代数（每时间步最大迭代 × 时间步数）。
- **47.8.4 图形定制**：绘图右键菜单——X/Y 轴（linear/log、范围、网格线数、标签格式、加变量）；向数据集加文件；加曲线、改曲线类型/颜色；改标题。

## 47.8.1–47.8.2 optiSLang 导出与可视化（pp. 4657–4659）

- **前提**：多于一个已更新 DP。Ribbon → optiSLang Capabilities → **Data Export** 下拉：**Export Designs**（生成 optiSLang 兼容输出文件）；**Go to optiSLang**（仅当 DOE 由 optiSLang 创建且 optiSLang 项目在仿真目录时可用——把 `*.opf` 复制到工作目录并打开；**注意 optiSLang 与 Fluent 无连接，optiSLang 中的改动不回传 Fluent**）；**Open Designs in Postprocessor**（默认当前仿真目录的兼容输出文件开 optiSLang 后处理器）；**Open OMDB in Postprocessor**（优化研究——载入 optiSLang Monitoring Database，含全部设计输入/响应，可出多种图表）；**Export Optimization Results into CSV**。TUI：`parametric-study/design-points/auto-create/` 下 `export-designs`、`go-to-optislang`、`open-designs-in-optislang-postprocessor`。
- **47.8.2 Data Visualization** 工具：交互图（点击一处图其他图联动；可放大；存 .png）；交互 Design Table（点击联动）；Axes 下拉换第一/第二轴变量；Designs 调显示的 DP 值数量、绘图数据存 CSV。

## 47.8.3 参数化比较图（pp. 4659–4661）

**Parametric Plots** 对话框（双击 Parametric Study View 的 Plots 节点；或 Ribbon Comparison Plot → Create New；或 Plots 右键 New...）：①命名；②X Axis/Y Axis 下拉选输入/输出参数；③Create 入 plots 树并显示。例：进口温度 vs Design Point（Figure 47.13）。

## 47.9 DP 报告与参数化报告（pp. 4662–4677）

- 入口：Simulation Report Outline 任务页 Current Report 选 **Design Point Settings** 或 **Parametric Report**；或 Ribbon Simulation Report 类别（Base Design Point Report Settings / Parametric Report）；或 Parametric Study View 的 Parametric Reports 节点。报告设置与标准仿真报告（[[Fluent 仿真报告]] Ch.46）同源。
- **47.9.1 DP 报告**：双击 Design Point Report Settings 节点或 Ribbon → 任务页（Current Report = Design Point Settings）→ **Save Settings** 后作用于全部 DP 报告（Options 恢复默认）。**告诫：必须在更新相关 DP 之前保存 DP 报告设置**。节构成同标准报告，差异点：Geometry and Mesh 含 **Mesh Size** 小节；Named Expressions 可定制细节含 **Definition/Value/Unit/Used In/Description**（默认全选）。保存的设置应用于全部 DP；更新时逐 DP 生成；Current Report 下拉可逐 DP 定制。Generate/View/Export（PDF/standalone HTML/PPT）同标准流程。
- **47.9.1.3.1 DP 报告过时**：DP 设置更新后报告过时——View 按钮与 Options 菜单、DP 表右键 View Parametric Report 选项、Study 树右键、报告窗口标题处出现 **"(out of date)"** 标签。
- **47.9.2 参数化报告**：设置节构成——Report Settings（Layout/Image/Theme 同标准）+ **Image Slider View Settings**（standard/comparison/both 滑块视图）；Header；**Design Point Table** 节（输出参数 **Conditional Formatting**：Active 开关；Coloring Style **Solid**（Color By Z-Score 或 Value Range——Above Minimum/Below Maximum/Between Min&Max）或 **Gradient**（Z-Score 或 Magnitude）；颜色 Red/Green/Blue）；**Base Case Simulation Setup**（Solver Settings + Physics 含 Reference Values）；**Parametric Plots**（可设 Layout）；图形对象（Named Expressions/Mesh/Contours/Vectors/Pathlines/LICs/XY Plots/Scenes/自定义视图）。Named Expressions 细节：Definition/Unit/Used In/Description。**注意：参数化报告的 named expressions 表不含作为输入参数的表达式**（其定义随各 DP 输入值变、写死会误导；值在报告 DP 表中）；**单个 DP 报告则包含**（单 case 语境下静态定义合理）。
- **47.9.2.3 结果比较**：滑块三式——standard（单标签、滑块逐 DP 看）；comparison（两结果并排各带滑块）；both。比较工具（Figure 47.17）：**Pan**（配合缩放平移）、**Grid**（网格线）、**Probe**（读 X/Y 坐标与 RGB 值；**不能与 Pan 或 Grid 同时用**）、**Pin**（配合 Probe，双击留下标记并在比较图底部报值）——配合滑块可查不同 DP 同一位置。XY plot 跨 DP 比较：图内过滤器显隐 DP 数据、按输入参数值过滤；活动过滤器列于图区顶部、一键移除复位。**注意：HTML 导出保留动态 XY 比较；PPT/PDF 导出仅静态截图**。
- **47.9.2.4.1 PPT 导出增强**：DP 表以嵌入式 Excel 图标呈现（双击在 Excel 打开另存）；带过滤器的绘图可登记特定版本入 PPT——调好过滤器后点图下 **Add To Pending Microsoft PowerPoint Export**，可加多版并命名，列于 Export Settings for Microsoft PowerPoint，Remove Plot From Export 移除、Print Plot Details 打印详情；带滑块图像（比较图/等值线/矢量等）同法登记/移除（Remove Image From Export / Remove Image Comparison From Export）。
- **47.9.2.4.2 参数化报告过时**三情形：DP 设置有更新；有带报告数据的新 DP 更新；已生成的 DP 报告被判过时。生成参数化报告时若存在过时 DP 报告数据，提示是否先更新——Yes 先更新再生成；No 带过时数据生成并标 "(out of date)" 直至重生成。

## 47.10 偏好设置（pp. 4677–4678）

File → Preferences → **Parametric Study** 类别。**Design Point Update Options**：Write Data by Default；Capture Simulation Report Data by Default；Save Project After Every Design Point Update；Auto Refresh of Design Point Status；**Auto Refresh Interval**（默认 10 秒、最小 5 秒）。**Layout Options**：Show Current Case Parameters；Show Parametric Study View。

## 47.11 当前 case 参数表（p. 4678）

启用 Show Current Case Parameters 后显示当前 case 的输入/输出参数表（名称、值、单位）。

## 47.12 文件管理（pp. 4679–4683）

- **47.12.1 Projects**：参数化研究用项目文件 **`*.flprj`** 组织多套 case/data。**47.12.1.1** File → Parametric Project 菜单打开/保存/**归档**项目。**47.12.1.2 Project View**（界面视图列表选择）总览项目文件——Write Data 开启的 DP 才有输出文件可见；更新期间生成的 `.out` 等文件无论 Write Data 与否都可见；Name 旁右键 → **Select Columns...**（Project 对话框）定制列；Preferences 开 Automatic Transcript 则每 DP 另出 transcript。
- **47.12.2 DP 文件**：设当前 DP 或更新 DP（含改 Write Data 开关）时**工作目录切到该 DP 目录**——后续文件存于此；更新生成的文件注册进项目、显示于 Project View 对应 DP 下。**注意：初始化研究后新建的动画定义，Animation Definition 对话框 Storage Directory 置 '.' 且禁改——动画文件存入当前 DP 目录；研究初始化前已存在的动画定义不受影响**。顺序更新时会在此仿真目录多产一个未注册文件——无害，可忽略/删除。
- **47.12.3 轻量项目（lightweight）**：项目 Select File 对话框取消 **Load Current Case and Data** 打开——不载 case/data，Fluent 从项目文件取参数化信息；仍可 Sequential/Concurrent 更新 DP、可用 optiSLang 自动加 DP。

**Ch.47 全章完成（pp. 4617–4684；p. 4684 空白页）。**


## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1，Chapter 47（自 p. 4617），批次 125 段 1（pp. 4617–4650），SHA-256 校验一致；段 2（47.7.8.1 续–47.12）待后续批次。
- Figures 47.1–47.8 及各界面截图记图形元素，未复制图像；字段名/菜单项照录；原文拼写 `Parameteric Report`（应为 Parametric）、`dependant`、`Tn the local approach` 均照录并标注。
- 许可行为（CFD Pro 限制、Cloud Burst 默认 CFD Enterprise、optiSLang 许可签出）为 2026 R1 描述，跨版本可能变化；证书路径 `\v241\RSM\bin\...` 中 v241 为原文所示版本目录名。
