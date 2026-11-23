# 知识索引

> Fluent User's Guide 按目录分成五个顶层主题：全手册总览 + 目录中的 Part I–IV。每轮严格只摄取一个目录章节；跨会话工作先看 [[ingest-state]]，按其中的章名和页码续接。

## Fluent User's Guide — 五个主题

### 1. 全手册总览

- [[Ansys Fluent User's Guide - 总览]]：版本、全局范围和五个主题入口。
- [[Ansys Fluent Users Guide 2026 R1]]：来源记录、摄取批次与证据边界。
- [[Ansys Fluent Users Guide 2026 R1 - 目录地图]]：从 PDF 书签生成的完整导航（4783 条书签，不代表正文已摄取）。

### 2. Part I — Getting Started

- [[Part I - Getting Started]]：基础介绍、CFD 流程与启动执行。
- [[Fluent 程序架构与能力]]：架构与双模式、APIP、程序能力、许可证级别矩阵与第三方软件版本（PDF pp. 143、145–154、174–175）。
- [[Fluent 2026 R1 已知限制]]：按类别整理的限制、缺陷编号与变通方法（PDF pp. 155–174）。
- [[CFD 仿真工作流与验证]]：分析步骤、规划、收敛及仿真结果核查（PDF pp. 177–184）。
- [[Fluent 启动与批处理自动化]]：Launcher、启动/并行/调度器选项、Journal、PyFluent 服务、批处理及运行检查点（PDF pp. 185–218）。

### 3. Part II — Meshing Mode

- [[Part II - Meshing Mode]]：引导式网格工作流、网格生成、检查和修复。
- [[Fluent 网格模式入门]]：网格化两途径、能力、-meshing 启动、双进程、GUI 组件与 TUI 总览（PDF pp. 225–258，Chapter 1 之 1.1–1.5）。
- [[Fluent 网格模式文件读写与导入]]：mesh/case/journal/transcript/domain 读写、CAD 与外部格式导入、保存图片（PDF pp. 258–284，Chapter 1 之 1.6，该章至此完成）。
- [[Fluent 引导式网格工作流]]：预置工作流、命名映射、Python journal 接口、任务机制、.wft 保存与首选项（PDF pp. 285–300，Chapter 2 完成）。
- [[Fluent 水密几何网格工作流]]：Watertight 工作流全章，涵盖几何导入、周期边界、区域/边界设置、薄体/边界层/多区/体网格和网格操作（PDF pp. 301–408）。
- [[Fluent 网格质量诊断]]：网格改进/修复、显示与检查流程、质量分布和指标定义（PDF pp. 539–604，Part II Chapter 6 完成）。
- [[Fluent 容错网格工作流]]：CAD/区域准备、泄漏与尺寸控制、包覆、表面/体网格、边界层和 overset（PDF pp. 409–524）。
- [[Fluent 2D 网格工作流]]：二维几何导入、全局/局部 sizing、MultiZone、2D boundary layers、导出与 sweep/extrude（PDF pp. 525–538）。
- [[Fluent 高级网格主题]]：CAD 装配与关联、曲率/邻近/硬软/BOI 尺寸控制与 size field（PDF pp. 605–868；Part II Chapter 7 完成）。
- [[Fluent 第三方网格导入与 fe2ram 过滤器]]：GAMBIT/TetraMesher、fe2ram 转换器与 I-deas/PATRAN/ANSYS/ARIES/NASTRAN 导入格式要求（PDF pp. 869–876；Part II Appendix A 完成）。
- [[Fluent 网格文件格式（legacy .msh）]]：节结构、类型索引、bc-type/element-type 表、Zone 节与命名规则（PDF pp. 877–892；Part II Appendix B 完成）。
- [[Fluent 快捷键与实体信息]]：Appendix C 网格窗口快捷键功能组（上下文相关）与 Ctrl+I 实体信息，附 Part II Bibliography 概览（PDF pp. 893–908；Part II 全部完成）。

### 4. Part III — Solution Mode

- [[Part III - Solution Mode]]：求解器设置、物理模型、计算、监控、后处理与参考。
- [[Fluent 手册排版与数学约定]]：排版约定与数学记号，解析手册操作路径与公式的依据（PDF pp. 913–916，Using This Manual）。
- [[Fluent 求解模式 GUI]]：ribbon、Outline View、task pages、对话框体系与界面定制（PDF pp. 917–962，Ch.1）。
- [[Fluent 求解模式文件读写]]：case/data 读写与自动保存、profile/表格/settings 文件、journal、解插值与 FMU（PDF pp. 963–1054，Ch.2–3）。
- [[Fluent 单位制]]：任意单位制与 SI 内部存储、内置与自定义单位制（PDF pp. 1055–1058，Ch.4）。
- [[Fluent 表达式语言]]：基于 Python 的声明式表达式，驱动边界条件/源项/求解器设置与报告（PDF pp. 1059–1154，Ch.5）。
- [[Fluent 模型拓扑（Model Topology）]]：labels 驱动的物理/几何解耦设置、树结构、限制与启用（PDF pp. 1155–1168，Ch.6）。
- [[Fluent 网格读取与操作]]：网格拓扑与选型、质量定义与阈值、网格来源与拼接、参考帧、曲线坐标系、非一致网格接口、Overset、Gap Model、网格检查修复/统计/多面体转换/22 项修改操作（PDF pp. 1169–1346，Ch.7 全章完成）。
- [[Fluent Cell Zone 与边界条件设置]]：zone 类型清单、设置与复制规则、TUI 批量语法、参数体系、Fluid/Solid/多孔介质条件、全部 22 类边界条件、瞬态 BC、声学波模型、Profiles 与 1D 耦合（PDF pp. 1347–1649，Ch.8 全章完成）。
- [[Fluent 物理属性]]：材料类型与数据库、温度函数、密度与黏度全选项、导热/UDS 扩散/电导/热容/辐射属性/质量扩散、操作压力与真实气体模型（PDF pp. 1651–1797，Ch.9 全章完成）。
- [[Fluent 基本流动建模]]：UDS 输运方程、流向周期流、旋流（旋流数选湍流模型）、可压流（浮动操作压力）、无黏流（PDF pp. 1799–1829，Ch.10 全章完成）。
- [[Fluent 运动参考系]]：SRF/MRF（frozen rotor）、速度公式选择、限制与设置、后处理（PDF pp. 1831–1849，Ch.11 全章完成）。
- [[Fluent 运动定义与辅助几何]]：运动定义（表达式支持）与辅助几何四类型（PDF pp. 1851–1860，Ch.12–13 全章完成）。
- [[Fluent 高超声速流动]]：HSN、有限速率化学与预定义混合物、Gupta 拟合、双温度模型、稀薄滑移与温度跳变、部分催化壁、烧蚀、最佳实践（PDF pp. 2393–2426，Ch.18 全章完成）。
- [[Fluent 虚拟叶片模型（VBM）]]：致动盘降阶模型、EDM/FDM 两模式、BET 动量源与 NR 自动配平、尖部损失、翼型 .dat 格式、28 步配置、场变量与载荷报告（PDF pp. 2427–2450，Ch.19 全章完成）。
- [[Fluent 组分输运与有限速率化学]]：组分上限与混合物材料、TCI 与化学求解器、Thickened Flame、CHEMKIN 导入与内置机理、反应/机理定义、Coal Calculator、表面反应与 CVD、颗粒/电化学反应、Reacting Channel、Reactor Network、Composition PDF Transport、化学加速六方法（PDF pp. 2451–2570，Ch.20 全章完成）。
- [[Fluent 缩阶湍流燃烧模型]]：非预混平衡化学与火焰let、柴油机非稳态火焰let、煤/液体燃料流股组成、PDF 查表与全制表、Inert 模型、预混 C/G 方程模型、部分预混与 FGM（PDF pp. 2571–2670，Ch.21 全章完成）。
- [[Fluent 发动机点火模型]]：火花模型、Knock/Ignition Delay 自燃模型、缝隙模型 ring pack（PDF pp. 2671–2684，Ch.22 全章完成）。
- [[Fluent 污染物生成模型]]：NOx 四路径与 SNCR/Reburn、Soot 四模型（一步/两步/MB-Hall/MoM）、Decoupled Detailed Chemistry（PDF pp. 2685–2724，Ch.23 全章完成）。
- [[Fluent 气动噪声模型]]：FW-H 声学模型全流程、声学波动方程与 Kirchhoff、宽带噪声源、密度基海绵层（PDF pp. 2725–2770，Ch.24 全章完成）。
- [[Fluent 离散相模型（DPM）]]：Lagrangian 颗粒追踪、injection 全类型、高分辨率追踪、物理与破碎模型、侵蚀与液膜、求解策略、后处理与 SCR 风险、并行（PDF pp. 2771–3004，Ch.25 全章完成）。
- [[Fluent 宏观颗粒模型（MPM）]]：大颗粒 add-on 模块——拖曳/碰撞/沉积/吸引力/注入与初始化（PDF pp. 3005–3026，Ch.26 全章完成）。
- [[Fluent 多相流模型]]：VOF/Mixture/Eulerian、体积分数格式与界面建模、明渠流与波 BC、传质七机制、拖曳/升力/润滑/湍流扩散交互全参数、Wet Steam 与 UDWSPF、求解策略与 mphase-summary 检查（PDF pp. 3027–3334，Ch.27 全章完成）。
- [[Fluent 熔化与凝固]]：焓-多孔介质法、Mushy Zone 参数、Lever/Scheil 规则、连续铸造 pull velocity 三法、热溶质浮力、液相分数 URF 与后处理变量（PDF pp. 3335–3342，Ch.28 全章完成）。
- [[Fluent 流固耦合（FSI）]]：intrinsic FSI 单向/双向、结构模型限制、Wall Structure 位移边界、动网格耦合设置、Newmark/BCGSTAB 等求解控制与非一致界面（PDF pp. 3343–3354，Ch.29 全章完成）。
- [[Fluent Eulerian 壁面液膜]]：EWF 模型选项与动量五项、DPM/相耦合、求解控制、Wall Film 六子页边界条件、EWF-VOF 耦合与后处理变量（PDF pp. 3355–3380，Ch.30 全章完成）。
- [[Fluent 电势场与电化学]]：电势场与 Joule 热、精细锂离子电池（Butler-Volmer/老化/肿胀 FSI）、电化学器件（电解/燃料电池七类、MEA 三法）、后处理变量（PDF pp. 3381–3426，Ch.31 全章完成）。
- [[Fluent 电池模型]]：MSMD 电池模型——解法四选、NTGK/DCIR/ECM/P2D 参数估计与 HPPC/BPX、载荷 profile 与查找表、独立 Echem 与老化、Pack Builder、ROM Tool Kit、肿胀/Venting/热滥用/短路/熵热与后处理（PDF pp. 3427–3536，Ch.32 全章完成）。
- [[Fluent 燃料电池]]：PEMFC/Fuel Cell and Electrolysis/SOFC+UE 三 add-on 模块——设置选项卡全参数、电堆与退化、边界条件、求解指南与后处理 UDS/UDM（PDF pp. 3537–3634，Ch.33 全章完成）。
- [[Fluent 磁流体动力学（MHD）]]：DC/AC 磁场下导电流体——感应/电位两法、外磁场 Patch/Import、边界条件、求解控制与数据文件格式（PDF pp. 3635–3658，Ch.34 全章完成）。
- [[Fluent 连续纤维模型]]：熔纺/干纺纤维拉丝 add-on——模型选项、材料属性、注入类型与纤维网格、UDF 定制、求解控制与后处理（PDF pp. 3659–3698，Ch.35 全章完成）。
- [[Fluent 降阶模型（ROM）]]：DesignXplorer 用 ROM——参数定义、变量/区选择、Fluent 内求值与后处理、Profile 导出与限制清单（PDF pp. 3699–3708，Ch.36 全章完成）。
- [[Fluent 求解器使用]]：压力基/密度基求解器全设置——离散、P-V 耦合、NITA、CFL/CASM、AMG/FAS、初始化、瞬态与自适应步进、伪时间、云计算、收敛监视/条件与稳定性、Solution Steering（PDF pp. 3709–3904，Ch.37 全章完成）。
- [[Fluent GPU 求解器]]：原生 GPU 求解器——启动与重映射、异步输出、支持特性与限制全清单、监视器与 EnSight 导出、疑难与性能排查（PDF pp. 3905–3974，Ch.38 全章完成）。
- [[Fluent 网格自适应]]：PUMA/悬挂节点自适应——Manual/Automatic 设置、Prismatic 拆分、五组预定义判据与几何重建（PDF pp. 3975–4014，Ch.39 全章完成）。
- [[Fluent 表面与单元寄存器]]：表面创建（等值/裁剪/变换/表达式体积）与管理、Facet/Vertex 赋值、七类单元寄存器与操作（PDF pp. 4015–4078，Ch.40 全章完成）。
- [[Fluent 图形显示]]：网格/等值线/矢量/迹线/LIC/体渲染/场景显示、视图动画、直方图 XY/FFT/累积绘图/瞬态后处理（PDF pp. 4079–4324，Ch.41 全章完成）。
- [[Fluent 数据报告]]：报告定义九类型、通量/力/积分/效率报告、参考值、输出参数与系统资源报告（PDF pp. 4325–4394，Ch.42 全章完成）。
- [[Fluent 场函数定义]]：节点/单元/面值语义、速度报告选项、分类场变量表与限制代码、自定义场函数（PDF pp. 4395–4524，Ch.43 全章完成）。
- [[Fluent 并行处理]]：并行架构、Launcher/命令行启动、调度器、网格分区方法与负载均衡、性能检查与优化、Arm 计算节点（PDF pp. 4525–4588，Ch.44–45 全章完成）。
- [[Fluent 仿真报告]]：HTML/PDF/PowerPoint 报告生成、限制与定制、模板与服务器工作流（PDF pp. 4589–4616，Ch.46 全章完成）。
- [[Fluent 参数化研究]]：设计点表、Sequential/Concurrent 更新、optiSLang DOE 与优化、DP/参数化报告、项目文件管理（PDF pp. 4617–4684，Ch.47 全章完成）。
- [[Fluent 设计分析与优化]]：伴随求解器、Design Tool、Gradient-Based Optimizer、湍流模型优化、几何参数化与网格变形器/优化器（PDF pp. 4685–4848，Ch.48 全章完成）。
- [[Fluent System Coupling]]：系统耦合变量与设置、FSI 建议、重启与排障（PDF pp. 4849–4886，Ch.49 全章完成）。
- [[Fluent 任务页参考]]：任务页控件参考（General 等，PDF pp. 4889 起，Ch.51 章内进行中）。
- [[Fluent 热能模拟]]：导热对流与 CHT 策略、shell conduction、辐射模型全套（含 Solar Load）、周期传热、换热器模型（dual cell/macro）、PCB 热分析（PDF pp. 2221–2392，Ch.17 全章完成）。
- [[Fluent 湍流模型设置]]：模型清单与 RANS/SRS 选型指南、各模型设置（SA/k-ε/k-ω/GEKO/转捩/RSM/SAS/DES/LES/ELES）、通用选项、湍流边界条件、初值、求解策略与后处理（PDF pp. 2125–2220，Ch.16 全章完成）。
- [[Fluent 叶轮机械流动]]：Turbo Setup 引导工作流、Frozen Gust、GTI 三类 pitch-change 界面与混合面、叶片颤振气动阻尼（TWM/ICM）、相位滞后法、湿蒸汽、叶片气膜冷却、TSN、叶轮后处理与性能计算（PDF pp. 1993–2124，Ch.15 全章完成）。
- [[Fluent 滑移与动网格]]：滑移网格技术/设置/时间周期解、动网格更新方法三族（光顺/层化/重划）、In-Cylinder/Six DOF/接触检测/动网格事件/解稳定化/稳态动网格（PDF pp. 1861–1992，Ch.14 全章完成）。

### 5. Part IV — Web Interface

- [[Part IV - Web Interface]]：通过 Web 界面与网格、仿真设置、求解和结果交互。

## 教程案例（Ansys Fluent Tutorial Guide 2026 R1）

- [[Ansys Fluent Tutorial Guide 2026 R1]]：1454 页教程指南来源记录；2026-10-27 起按章摄取（摄取对象为 Downloads 副本，SHA-256 `8347db…`，与 vault 上一级同名文件版本不同，页码不混用）。
- [[Fluent 教程12 Frozen Rotor 方法]]：离心泵+蜗壳稳态 frozen rotor——NPS turbo 界面、Moving Wall 相对/绝对运动、head 表达式与瞬态 rotor-stator 转换三步（PDF pp. 517–534）。
- [[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]]：1.5 级压气机 Turbo Setup Workflow 十三步——zone 名映射 Preferences、GTM 导入、mixing-plane 默认界面、twf_ 表达式与效率/压比结果（PDF pp. 535–572）。
- [[Fluent 教程14 叶排交互稳态与瞬态仿真]]：同一压气机稳态 mixing-plane → 瞬态 pitch-scale——等熵效率表达式、local scaling 残差、Period-Based 推进与叶片通过周期、熵云图与 Periodic Instancing（PDF pp. 573–618）。
- [[Fluent 教程15 滑移网格]]：单级压气机滑移网格瞬态——22.5° 周期部分几何、无粘 Euler、Periodic Repeats 界面与 one-to-one-pairing TUI、时间步推导、Data Sampling 与 FFT 叶片通过频率（PDF pp. 619–664）。

## 其他资料

## 综合分析（analyses）

- [[NUMECA 网格导入 Fluent 警告解读]]：实测 transcript 诊断——Reversing faces 警告无害；outflow 与压力边界不共存，须将 zone-type 改为 pressure-outlet（8.4.11）；细碎分区按 7.12.1 合并 cell zone 与同 BC 墙区、先合并后建界面的简化流程。

## 后续处理

各 Part 页列有待摄取章节。每批正文内容需回链到对应来源页，标注 PDF 页码、版本和适用边界。
