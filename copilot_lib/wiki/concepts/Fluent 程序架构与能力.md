---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - architecture
  - licensing
  - capabilities
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 程序架构与能力

## 摘要

Ansys Fluent 2026 R1 是用 C 语言编写、面向复杂几何中流体流动/传热/化学反应建模的程序，采用 client/server 架构，分为网格模式（meshing mode）与求解模式（solution mode）。其功能可用性由四个许可证级别（CFD Pro / CFD Premium / CFD Enterprise / CFD HPC Ultimate）分层控制；界面只显示当前许可证支持的选项（User's Guide 2026 R1，PDF pp. 145–154）。

## 架构与运行模式（PDF pp. 145–146）

- **实现与架构**：C 语言编写，动态内存分配、高效数据结构、灵活求解器控制；client/server 架构使其可作为独立并发进程运行在桌面工作站（client）和计算服务器（server）上。
- **网格灵活性**：支持 2D 三角形/四边形/多边形，3D 四面体/六面体/金字塔/楔形/多面体，以及混合（hybrid）网格；可基于流动解加密或粗化网格。
- **双模式**：3D 几何可在 Fluent 的 meshing mode 中直接生成网格（也可读入外部网格）；其余操作（边界条件、流体属性、求解、网格加密、后处理）都在 solution mode 中完成。
- **进程组成**：serial solver 用单进程完成文件 I/O、数据存储和流场计算；utility 进程 **cortex** 管理用户界面和基本图形功能；parallel solver 由 host 进程与一个或多个 compute-node 进程交互，节点可在同一台机器或网络中不同机器上。架构图见手册 Figure 1.1（p. 146，图形元素，本页不复述图内容）。
- 并行处理与 MPI 细节在手册 “Parallel Processing” 章节（印刷页码 p. 4525，属 Part III，尚未摄取）。

## 1.1 Ansys 产品改进计划（APIP，PDF pp. 147–150）

- **默认启用**，通过 Licensing Settings utility 控制；每个会话收集匿名使用数据，会话结束时一次性发送到 Ansys 受限访问的服务器。参与完全自愿、可随时退出（方法见 Ansys Licensing Guide 的 “Enabling the APIP” 文档）。
- **收集的数据类别**（手册明确陈述）：硬件（CPU/内存/显卡品牌类型、处理器数量）、系统（OS 版本、国家码、时区、语言、产品所用环境变量的值）、会话特征（交互/批处理、时长、CPU 时间、许可证与设置、版本与 build、命令行选项、处理器与内存用量、错误与警告）、会话动作计数（保存、重启、网格/求解/后处理动作、帮助与向导使用次数、工具栏选择）、模型统计（实体数量类型、材料/载荷/边界条件/组分数量、坐标系、单位制、维度）、分析特征（物理类型、线性/非线性、时域频域、分析选项）、求解特征（求解器与选项、收敛准则/精度/调优等求解控制、方程数/载荷步/设计点等统计）、特殊功能（用户插件与例程、与其他 Ansys 产品的耦合）。
- **不收集**：个人身份（姓名、地址、用户名）、文件名/部件名/用户标签、几何或设计输入（坐标值、厚度等尺寸）、材料属性/载荷等实际数值。且不记录数据来源位置，无法关联到具体客户/公司/地点。
- **注册范围**：同一台机器上的注册选择适用于所有 Ansys 产品；集群配置下由 host 机器的设置决定。手册声明数据量很小、不影响产品性能。

## 1.2 程序能力（PDF pp. 150–152）

Meshing mode 下 Fluent 是非结构体网格生成器（详见手册 “Meshing Mode Capabilities”，印刷页码 p. 226，属 Part II，尚未摄取）。Solution mode 下手册列出的模拟能力：

- **维度与流态**：2D 平面、2D 轴对称、2D 轴对称带 swirl、3D；定常或瞬态；不可压或可压（低亚音速、跨音速、超音速、高超音速）；无粘、层流、湍流；牛顿或非牛顿流体；理想或真实气体。
- **传热**：强制/自然/混合对流、共轭（固/流）传热、辐射。
- **化学反应**：组分混合与反应，均相/非均相燃烧模型，表面沉积/反应模型。
- **多相与离散相**：自由表面与多相模型（气-液、气-固、液-固）；Lagrangian 轨迹计算（颗粒/液滴/气泡，含与连续相耦合和喷雾建模）；空化；熔化/凝固（相变模型）。
- **其他物理**：多孔介质（非各向同性渗透率、惯性阻力、固体导热、多孔面压跳）；风扇/泵/散热器/换热器集总参数模型；流致噪声声学模型。
- **参考系与运动**：惯性（静止）或非惯性（旋转/加速）参考系；多参考系（MRF）与滑移网格；mixing-plane 模型（转子-定子、变矩器等叶轮机械，可选质量/swirl 守恒）；动网格（运动与变形网格）。
- **源项与材料**：质量/动量/热量/组分的体积源；材料属性数据库。
- **设计优化与定制**：adjoint 求解器、mesh morpher/optimizer；UDF 定制；与 GT-POWER 和 WAVE 的双向动态耦合。
- **附加模块**：Battery、Continuous fiber、Macroscopic particle model (MPM)、Fuel cell、Magnetohydrodynamics (MHD)、Population balance；以及 Fluent Icing。

## 许可证级别与能力矩阵（PDF pp. 152–154，Table 1.1）

四个级别的定位（手册文字描述）：

| 级别 | 定位 |
| --- | --- |
| CFD HPC Ultimate | Enterprise 全部能力 + 在任意数量 CPU 核或 GPU 上求解而无需额外 HPC 许可证 |
| CFD Enterprise | 完整的 Fluent Meshing 与 Fluent 求解器能力；另含 CFX、Chemkin、Reaction Workbench、Energico、Discovery、ICEM CFD、Meshing、EnSight Enterprise、DesignXplorer、Forte、Polyflow Classic、TurboGrid、FENSAP-ICE、Model Fuel Library、Fluent workspaces、Native GPU solver |
| CFD Premium | 完整的 Fluent Meshing 与 Fluent 求解器能力；另含 CFX、Discovery、ICEM CFD、Meshing、EnSight Enterprise、DesignXplorer、Forte、TurboGrid、Polyflow Classic Pro |
| CFD Pro | Fluent Meshing 的 Water-Tight 工作流 + 缩减的求解能力：不可压/可压、定常/瞬态、单相、湍流、无反应流动及传热；另含 Meshing 和 Polyflow Classic Pro（含用于 Polyflow 后处理的 CFD-Post） |

Table 1.1 能力按最低许可证级别归纳（列归属经字形坐标逐行核对，见“证据”）：

- **所有级别（含 CFD Pro）**：GUI；CAD 导入；定常流动与传热（不含辐射）；压力基 Coupled 与 Segregated 求解器（Pro 带脚注 \*）；基础湍流模型（无粘、层流、k-epsilon、k-omega standard/SST、Spalart-Allmaras）；HPC 含 4 核（更多核经 Ansys HPC 许可证）；固体共轭传热（CHT）；多孔介质（各向同性、正交各向异性、锥形）；流体状态模型（不可压、可压理想气体、Boussinesq 近似、非牛顿）；旋转参考系与 MRF（不含周期界面）；惰性与无质量颗粒追踪；2D fan 模型；多流混合（多种非反应组分）；Fluent Meshing Watertight 工作流（Polyhedra、Poly-Hexcore + Mosaic、Tetrahedral、Prism）；Fluent 设置与后处理（含报告）；参数与表达式；一对一非一致网格界面（Pro 带脚注 \*\*）；瞬态流动；shell conduction 传热。
- **CFD Premium 及以上**：TUI（文本用户界面）；参数化研究的并发设计点更新；Workbench 集成；Fluent 批处理求解（batch solving）；Fluent Meshing 并行网格与容错（Fault Tolerant）网格；多对多非一致网格界面；高级湍流模型；密度基求解器、adjoint 求解器、6-DOF 流致固体运动；多相流（自由表面、空化、相变、薄膜、向/从颗粒转变、沸腾、表面张力、反应、颗粒模型、DDPM）；完整颗粒追踪（破碎、聚并、侵蚀、蒸发、壁面薄膜、反应、宏观模型）；燃烧与反应流（污染物/soot、FGM、Finite Rate、effusion cooling）；热辐射模型与换热器模型；真实流体属性（如蒸汽、低温流体）；周期界面与 turbo 界面（mixing plane、pitch change）；叶轮机械叶片颤振分析与叶片膜冷却；动网格、overset 网格、网格自适应（含多面体非结构自适应）；声学；电化学与电池模型。
- **CFD Enterprise 及以上**：Native GPU Solver。
- **仅 CFD HPC Ultimate**：任意数量 CPU 核或 GPU 求解且不需额外 HPC 许可证。

脚注（手册原文含义）：

- (\*) CFD Pro 下压力-速度耦合：定常算例仅支持 Coupled 格式，瞬态算例仅支持 SIMPLE 格式。
- (\*\*) CFD Pro 下一对一网格界面的部分选项不可用：命名选项、配对容差、最小重叠面积百分比。

其他要点：

- CFD Pro 下界面只显示受支持的选项/功能；若需要环境变量（例如 `lang=ja` 切换日文界面），必须在启动 Fluent **之前**在系统级定义（Important 注记，p. 152）。
- **Ansys Student 许可证**支持读取最多 100 万网格单元的算例（Note，p. 153）。
- Ansys 其他 CFD 程序：CFX、Ansys Icepak、Ansys Polyflow Classic，面向不同流态与物理模型（p. 154）。

> 对本项目（Fluent Copilot 自动化）的含义：TUI、批处理求解和 Workbench 集成都要求 CFD Premium 及以上级别；在 CFD Pro 环境下基于 TUI/journal 的自动化不可用（此为从 Table 1.1 得出的直接推论，级别归属本身为手册明确陈述）。

## 1.4 支持的第三方软件（PDF pp. 174–175，Table 1.2）

平台限制（手册明确陈述）：

- Fluent-Platform LSF 集成：Windows 平台不支持。
- Fluent-SGE 集成：仅支持 Linux。
- WAVE 与 GT-POWER 耦合：仅 standalone Ansys Fluent 可用，Workbench 环境不可用。

Table 1.2 支持版本（仅适用于 2026 R1）：

| 第三方软件 | 支持版本 |
| --- | --- |
| Abaqus | version 2024, ODB Library 2024 |
| Altair HYPERMESH | 5.1 |
| Ceetron-SAM | 2.1.0 |
| CGNS | 4.5 |
| EnSight 6（仅 TUI） | EnSight 6 |
| EnSight Case Gold | 10.1.6 |
| FAST | 1.3 |
| Fieldview | 16.0 |
| GT-POWER | 2024.2 |
| HDF5 | 1.12.2 |
| HOOPS | 30.14 |
| Intel MPI | Linux: 2021.14.2；Windows: 2021.8 |
| libpng | 1.6.18 |
| LSTC-DYNA | 970.0 |
| Microsoft MPI | 10.1 |
| MPCCI | 3.0.5 |
| NASTRAN | Bulk data input file — MSC.NASTRAN 2018；OUTPUT2 data file — NX/NASTRAN 12 |
| NIST | 10.0 |
| Open MPI | 4.1.8 |
| Sundials | 2.5.0 |
| TECPLOT | Tecplot 文件格式 version 11.2 |
| WAVE | 2020.2 |
| zlib | 1.2.8 |

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]），PDF pp. 143、145–154、174–175。p. 143 为 Part I 扉页（列出 Part I 各章：Chapter 1 简介 p. 145、Chapter 2 CFD 基本步骤 p. 177、Chapter 3 成功仿真指南 p. 183、Chapter 4 启动与执行 p. 185、术语表 p. 219）；p. 144、176 为空白/版权页，无正文内容。
- Table 1.1 的普通文本提取丢失勾选列位置；本页的级别归属通过版面模式提取 + 字形 x 坐标与表头列坐标（Pro/Premium/Enterprise/Ultimate）逐行比对核实，未凭推测填表。
- 许可证能力由 Ansys 许可政策决定，随版本变化；第三方软件版本表仅适用于 2026 R1。APIP 数据范围以手册陈述为据；实际部署还应查 Ansys Licensing Guide 与隐私政策。
- 本批文本提取存在已知的字符间空格异常，但语义完整；Figure 1.1 为图形元素，仅有题注被提取，图内容未描述。
- “对本项目的含义”一段为综合推论，其余为手册明确陈述。

## 定制（ACT）补充（Ch.50，pp. 4887–4888）

User's Guide Part III Ch.50 "Customizing Fluent" 全章仅一段：可用 **Ansys ACT** 创建仿真向导（simulation wizards），在**独立 Fluent 或 Workbench 中的 Fluent** 运行；一般 ACT 用法见 *ACT Developer's Guide*，Fluent 专属用法见 *ACT Customization Guide for Fluent*（本手册不展开）。UDF/Scheme 定制分别见 Fluent Customization Manual 与本库 TUI 相关页。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part I - Getting Started]]
- [[Fluent 2026 R1 已知限制]]（同章 1.3 节）
- [[CFD 仿真工作流与验证]]（Chapter 2/3）
- [[Fluent 启动与批处理自动化]]（Chapter 4 部分）
- [[index]]
