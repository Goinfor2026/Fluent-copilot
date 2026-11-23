# 维护日志

本文件按时间追加，不回写或重排旧记录。

## [2026-10-15] setup | 初始化 Fluent Copilot 知识仓库

- 建立 raw、wiki、templates 三层目录和维护规则。
- 登记 Ansys Fluent Tutorial Guide 2026 R1。仅检查了 PDF 元数据和目录（1454 页）；没有提炼章节结论。
- 待处理：摄取教程优先章节；整理 Fluent Copilot 项目已有代码与文档。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 1

- 在 `raw/inbox/Ansys_Fluent_Users_Guide.pdf` 登记原始资料（6056 页，版本 2026 R1）；原 PDF 未修改。
- 从 PDF 书签生成完整目录地图（4783 条书签项）。目录仅用于导航，不等于正文摄取。
- 阅读并提炼 PDF pp. 177–184，建立 `CFD 仿真工作流与验证` 页面，涵盖工作流程、建模规划、网格检查、监控和结果验证。
- 边界：p. 183 抽取文本缺失残差公式数字，未推断阈值；其余 User's Guide 正文仍待分批摄取。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 2

- 阅读并提炼 PDF p. 185 及 pp. 198–215 中的部分 Linux/Windows 启动、命令行参数、PyFluent 服务启动选项和批处理/错误退出行为。
- 建立 `Fluent 启动与批处理自动化`，并更新来源页和索引。
- 边界：尚未摄取 Journal/TUI 语法参考、调度器全部参数或 Part II–IV 正文；平台细节需在实际安装环境核验。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 3

- 阅读并提炼 PDF pp. 582–602 的网格诊断与质量指标章节，建立 `Fluent 网格质量诊断`，包含检查流程、报告范围、直方图、skewness 与 orthogonal quality 等。
- 更新来源页和索引。保留各指标定义差异，不把经验规则写成普适验收标准。
- 边界：网格生成/修复的完整操作流程及 Part II 其他章节尚未摄取。

## [2026-10-15] setup | 按 User's Guide 目录建立五个顶层主题

- 将手册知识按“全手册总览 + Part I–IV”组织为五个入口页。
- 把已摄取的 CFD 流程/启动主题归入 Part I，把网格质量主题归入 Part II；Part III、IV 标为尚未摄取。
- 更新 `index.md` 和来源页的导航，保留原有主题页面及证据页码。

## [2026-10-15] setup | 建立跨会话摄取续接规范

- 新增 `ingest-state.md`，记录 User's Guide 的来源 SHA-256、已完成离散页段、最近批次、下一续接位置和未处理页段。
- 更新 `AGENTS.md`：所有智能体每次摄取开始前先读检查点，完成/中断时准确更新页段和状态；同一来源不并行推进。
- 更新来源页与索引，提醒后续工作从 PDF p. 603 续接；p. 602 不是此前所有页都已摄取的意思。

## [2026-10-15] setup | 修正 User's Guide 的默认续接顺序

- 原因：先前自行优先抽取网格质量，导致正文从 pp. 198–215 跳到 pp. 582–602；这是主题跳读，不是连续摄取。
- 更新规则：默认按目录顺序处理最早未摄取正文；只有用户明确指定优先主题时才跳读，并记下待回填范围。
- 将下一续接位置从 p. 603 改为最早未摄取正文 p. 143（Part I Chapter 1）；保留已完成页段的真实记录。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 4

- 核验来源身份（路径、6056 页、SHA-256 一致）后，按检查点从最早未摄取正文 PDF p. 143 开始，完整阅读 pp. 143–176：Part I 扉页与 Chapter 1（架构、1.1 APIP、1.2 程序能力与 Table 1.1 许可证矩阵、1.3 已知限制、1.4 Table 1.2 第三方软件）。
- 新建 `Fluent 程序架构与能力` 和 `Fluent 2026 R1 已知限制` 两个知识页；更新 Part I 项目页、来源页和索引。
- Table 1.1 勾选列在普通文本提取中丢失位置，用版面模式 + 字形坐标逐行核对级别归属；p. 170 两处可疑字符串经 600 dpi 视觉核对确认为手册原文印刷形式（疑排版错误），已在知识页标注待核实，未做猜测性修正。
- 边界：p. 143 扉页仅登记各章起始页；pp. 144、176 空白/版权页无正文；1.3 节条目为转述摘要，实际排障时须回查手册原文页码。Part I 剩余 pp. 186–197、pp. 216–219 及 Part II–IV 大部分正文尚未摄取。

## [2026-10-15] setup | 改为每轮按目录只摄取一个章节

- 更新 `AGENTS.md`、`INGEST_PROMPT.md` 和 `ingest-state.md`：每轮限一个目录章节；章节页码以书签目录起止页为准；章节过长时只在章内续接。
- 检查点现指向 Part I / Chapter 1（PDF pp. 145–176）。将 Chapter 2–3 标为已完成、Chapter 4 和 Part II / Chapter 6 标为部分摄取，记录章内未处理范围。
- 更新来源页、索引和 README 导航。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 5

- 依据来源 SHA-256、版本和 PDF 页数核对身份；按续接检查点完成 Part I / Chapter 4 “Starting and Executing Ansys Fluent”（目录范围 PDF pp. 185–218）。
- 本轮补充阅读并整理 pp. 186–197、pp. 206–209、pp. 216–218；与先前已整理的 p. 185、pp. 198–205、pp. 210–215 合并，覆盖本章完整目录范围。
- 更新 `Fluent 启动与批处理自动化`，补充 Launcher/工作区和精度、Windows/Linux 启动差异、并行与调度器选项、启动命令、运行检查点、清理及退出说明；同步更新来源页、Part I 项目页、索引和续接检查点。
- 限定：平台、许可证、调度器和安全设置均受具体安装/集群配置约束；本页是手册摘要，不替代目标环境验证。p. 219 Glossary 不属于本章，尚未处理。
- 下一续接位置：Part II / Chapter 1 “Introduction to Meshing Mode in Fluent”，PDF pp. 225–284，从 p. 225 开始；本次未进入下一章。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 6（Part II / Chapter 1 章内进行中）

- 核对来源身份（路径、6056 页、SHA-256 一致）后按检查点续接 Part II / Chapter 1 "Introduction to Meshing Mode in Fluent"（目录范围 PDF pp. 225–284）。
- 本轮按小节顺序阅读并整理 1.1–1.5（PDF pp. 225–258）：网格化两种途径、Meshing Mode 能力、-meshing 启动与 .tgrid/.fluent、双进程构建、动态 spawn 的平台限制、GUI 各组件（Ribbon 模式切换规则、Workflow 页、Outline View 对象树、Console、工具栏、Preferences 文件位置、帮助）与 TUI 总览。
- 新建知识页 `Fluent 网格模式入门`；更新 Part II 项目页、来源页和索引。
- 边界：1.4 节的界面截图图形元素未摄取，仅整理文字描述；印刷页码引用（p. 558、605、893、904 等）指向尚未摄取的后续章节，仅作定位。Chapter 1 的 1.6 "Reading and Writing Files"（pp. 258–284）未开始。
- 检查点保持该章 `in-progress`，下一续接位置：PDF p. 258（1.6 节起）；不提前进入 Chapter 2。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 7（Part II / Chapter 1 完成）

- 核对来源身份（路径、6056 页、SHA-256 一致）后按检查点续接 Part II / Chapter 1 的 1.6 "Reading and Writing Files"（PDF pp. 258–284），全章目录范围至此完成。
- 新建知识页 `Fluent 网格模式文件读写与导入`：二进制/压缩/tilde/覆盖确认快捷；mesh 文件读写、append 规则、read/write-options、边界网格分块；case 文件与 meshing/solution 互转的兼容性警告；size-field、Scheme 源文件；journal 的无状态回放语义、set-tui-version 版本窗口（26.1，两个完整 release 之内）、录制规则与嵌套；transcript 与自动命名；domain 文件；Prep7/cdb 等导入（VKI 许可证）；CAD 导入的 Tessellation/粒度/命名/单位规则与问题几何变通；Save Picture 格式与最佳实践。
- 更新 `Fluent 网格模式入门` 边界说明、Part II 项目页、来源页和索引。
- 边界：p. 258 上半的 1.5/章头归入门页，p. 284 为版权页脚无正文；Figure 1.21/1.22 仅文字机制被摄取；印刷页码引用（附录 A p. 869、Scaling the Mesh p. 1332 等）指向未摄取章节仅作定位；p. 281 格式列表提取乱序，以 p. 279 正文为准。
- 下一续接位置：Part II / Chapter 2 “Getting Started with the Fluent Guided Workflows”，PDF pp. 285–300，从 p. 285 开始（Chapter 3 从 p. 301 起，已按目录地图复核）。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 8（Part II / Chapter 2 完成）

- 核对来源身份（路径、6056 页、SHA-256 一致）并复核检查点无漂移后，按目录续接 Part II / Chapter 2 "Getting Started with the Fluent Guided Workflows"（PDF pp. 285–300），一次读完并整理全章。
- 新建知识页 `Fluent 引导式网格工作流`：Watertight/Fault-tolerant 两种预置工作流的适用条件；几何前提与 Force Share；16 项名称模式→边界类型映射表及命名禁忌；2020 R1 前 journal/.wft 不兼容；字段级协助的平台限制；`%py-exec workflow...` journal 记录格式、`(%py-console)`、TaskObject/命令 help() 与 dir(meshing)；任务状态图标、Edit/Revert and Edit、组任务；通配符过滤及 journal 动态解析语义；.wft 版本字段（26.1）、工作流随网格文件保存、task editing data 与 Workflow templates folder（同名 .scm 自动加载）等首选项。
- 更新 Part II 项目页、来源页和索引。
- 边界：Figure 2.1/2.2 为图形元素未摄取；印刷页码引用 p. 301/409 已复核等于 PDF 页码，其余（p. 302、406、410）属未摄取章节仅作定位；映射表与默认值对应 2026 R1。
- 下一续接位置：Part II / Chapter 3 "Using the Watertight Geometry Meshing Guided Workflows"，PDF pp. 301–408（Chapter 4 自 p. 409 起，已按目录地图复核），从 p. 301 开始；章长 108 页，须分多轮在同章内按小节顺序续接。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 9（Part II / Chapter 3 章内进行中）

- 核对来源身份（SHA-256 一致）并复核检查点无漂移后，按"当前唯一续接章节"续接 Part II / Chapter 3 "Using the Watertight Geometry Meshing Guided Workflows"（目录范围 PDF pp. 301–408，108 页，分多轮）。
- 本轮按小节顺序阅读并整理 3.1–3.6（PDF pp. 301–326）：Watertight 工作流总限制与逐任务限制清单、UTL（以 CFD Pro 级别启动启用，各任务按拓扑选择）、Import Geometry（单位、body labels、Separate Zone By 四模式与 face 选项代价、PMDB/.dsco/Linux 流程）、Import BoI（须在 Import Geometry 后、禁带连接体）、Add Local Sizing（Edge/Face/Body/BOI/FOI/Curvature/Proximity 七类控制与 BOI 规则）、Generate Surface Mesh（size field/control 文件、重划范围、Auto Assign Zone Types 表、质量改进、Remove Steps、Auto Remesh 三种 auto 行为与 re-faceting）。
- 新建知识页 `Fluent 水密几何网格工作流`；更新 Part II 项目页、来源页和索引。
- 边界：p. 321 边界类型表提取有单元格错位，已用 2.1 节同源表交叉核对（差异如实记录，逐字用于脚本前建议回查原页）；Figures 3.1–3.5 仅文字说明被摄取；印刷页码引用（p. 332、361、372、612、615、623）指向未摄取页段仅作定位。
- 检查点保持该章 `in-progress`，下一续接位置：PDF p. 326（3.7 "Setting Up Periodic Boundaries" 起）至 3.28（p. 408）。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 10（Part II / Chapter 3 完成）

- 依用户本次指定的五章范围，续接并完成 Part II / Chapter 3 “Using the Watertight Geometry Meshing Guided Workflows”（目录范围 PDF pp. 301–408）。
- 阅读并整理 3.7–3.28（PDF pp. 326–408）：周期边界、几何描述/共享拓扑、封口与区域、薄体与边界层、多区与体网格、边界/网格改进、变换/拉伸、线性 pattern、zone 管理、局部细化和自定义 journal。
- 更新 `Fluent 水密几何网格工作流`、Part II 项目页、来源页、索引和检查点；Chapter 3 为用户五章任务第 1/5 章。
- 下一章为 Chapter 4（PDF pp. 409–524）。本五章任务后续依次为 Chapter 5 pp. 525–538、Chapter 6 pp. 539–604、Chapter 7 pp. 605–916。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 11（Part II / Chapter 4 完成）

- 核对 PDF 路径、版本、6056 页和 SHA-256 与检查点相符；按序读取 Part II / Chapter 4 “Using the Fault-tolerant Meshing Workflow”，完整目录范围 PDF pp. 409–524。
- 新建 `Fluent 容错网格工作流`：整理 CAD/meshing object 管理、几何和流动类型、封口/泄漏/region 设置、wrap-target 尺寸、contact patch/gap cover、surface/volume mesh、boundary layers、overset、zone 后处理和部件替换。
- 更新 Part II 项目页、来源页、索引和 `ingest-state.md`。记录平台/格式限制与特定默认值受 2026 R1 和几何条件约束。
- 用户五章任务进度为 2/5。下一章 Chapter 5 “Using the 2D Meshing Guided Workflow”，PDF pp. 525–538，从 p. 525 开始。

## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 12（Part II / Chapter 5 完成）

- 按目录处理 Part II / Chapter 5 “Using the 2D Meshing Guided Workflow”（完整范围 PDF pp. 525–538）。
- 新建 `Fluent 2D 网格工作流`，归纳 CAD/PMDB 导入、区域和边界、全局/局部 sizing、MultiZone、2D shell boundary layers、初始表面网格、专用 2D mesh 导出及轴对称 sweep/网格 extrusion。
- 同步更新来源页、Part II 页面、索引和 `ingest-state.md`。二维专用 mesh 不能直接读回 2D workflow；平台和文件格式约束按 2026 R1 记录。
- 用户五章任务进度为 3/5。下一章 Chapter 6 “Improving and Examining the Mesh and its Quality”，PDF pp. 539–604；历史 pp. 582–602 待复核。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 13（Part II / Chapter 6 完成）

- 依目录整理 Chapter 6 全章 PDF pp. 539–604；合并早期已摄取的 pp. 582–602，并补充 p. 539–581、603–604。
- 扩充 [[Fluent 网格质量诊断]]：网格平滑/交换/Improve、sliver 与 cavity 修复、zone/domain 操作、mesh check、显示/鼠标探测、统计和 print-info；指标和诊断范围仍以手册条件为准。
- 同步更新来源页、Part II 项目页、索引及检查点。五章任务进度 4/5。
- 下一章 Chapter 7 “Advanced Meshing Topics”，PDF pp. 605–916，从 p. 605 开始。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 14（Part II / Chapter 7 进行中）

- 开始 Part II / Chapter 7 “Advanced Meshing Topics”（目录范围 PDF pp. 605–916），本批次按序完成 7.1 CAD Assemblies 和 7.2 Size Functions and Scoped Sizing（pp. 605–627）。
- 新建 [[Fluent 高级网格主题]]，整理 CAD 装配树与对象关联、FMDB、曲率/邻近/硬软/BOI sizing、size field 计算及复核。
- 更新索引、Part II 项目页、来源页和检查点；本章仍为 in-progress。下一未读小节 7.3 “Objects and Material Points”，从 PDF p. 628 开始。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 15（Chapter 7 续接）

- 按序完成 Chapter 7 7.3 “Objects and Material Points”（PDF pp. 628–643）：对象类型/优先级与 Subtract、zone labels、对象管理操作、material points 对体区提取和拆分的作用。
- 扩充 [[Fluent 高级网格主题]] 并同步更新来源页、索引与检查点。Chapter 7 仍进行中；下一节 7.4 Object-Based Surface Meshing，从 p. 644 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 16（Chapter 7 续接）

- 按序完成 Chapter 7 7.4 “Object-Based Surface Meshing”（PDF pp. 644–669）：wrapper 与 join/intersect 两种流程、几何准备和 patch、groups、诊断、表面连接与间隙/厚度修复、Sew。
- 扩充 [[Fluent 高级网格主题]] 并同步更新索引、来源页和检查点。Chapter 7 仍进行中；下一节 7.5 Object-Based Volume Meshing，从 p. 670 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 17（Chapter 7 续接）

- 按序完成 Chapter 7 7.5 “Object-Based Volume Meshing”（PDF pp. 670–679）：region compute/validate/update、Auto Mesh 与 Auto Fill Volume、Prepare for Solve 及流程限制。
- 扩充 [[Fluent 高级网格主题]]，同步更新索引、来源页、Part II 与检查点。Chapter 7 仍进行中；下一节 7.6 Manipulating the Boundary Mesh，从 p. 680 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 18（Chapter 7 续接）

- 按序完成 Chapter 7 7.6 “Manipulating the Boundary Mesh”（PDF pp. 680–731）：节点/表面编辑、intersect/join/stitch、改进/细化、edge features、重三角化、zone 拆分与操作、表面构造及 periodic/gap 操作。
- 扩充 [[Fluent 高级网格主题]]，同步更新来源页、索引及检查点。Chapter 7 仍进行中；下一节 7.7 Wrapping Objects，从 p. 732 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 19（Chapter 7 续接）

- 按序完成 Chapter 7 7.7 “Wrapping Objects”（PDF pp. 732–748）：Cartesian wrapping 流程、几何/尺寸准备、material point、孔洞/泄漏修复、分对象/整体包覆、网格对象质量改善。
- 扩充 [[Fluent 高级网格主题]]，同步更新来源页、索引及检查点。Chapter 7 仍进行中；下一节 7.8 Creating a Mesh，从 p. 748 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 20（Chapter 7 续接）

- 按序完成 Chapter 7 7.8 “Creating a Mesh”（PDF pp. 748–777）：网格策略选择、Auto Mesh、thin volume、pyramids/non-conformal/heat exchanger、并行分区和线程控制。
- 扩充 [[Fluent 高级网格主题]]，更新索引、来源页和检查点。Chapter 7 仍进行中；下一节 7.9 Generating Prisms，从 p. 778 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 21（Chapter 7 续接）

- 按序完成 Chapter 7 7.9 “Generating Prisms”（PDF pp. 778–807）：增长流程/首层与层数设置、多区与方向/碰撞控制、邻接区投影、质量改善及常见问题。
- 扩充 [[Fluent 高级网格主题]]，同步更新来源页、索引和检查点。Chapter 7 仍进行中；下一节 7.10 Generating Tetrahedral Meshes，从 p. 808 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 22（Chapter 7 续接）

- 按序完成 Chapter 7 7.10 “Generating Tetrahedral Meshes”（PDF pp. 808–822）：自动/手动生成、初始化、全局/局部细化、混合网格和常见失败诊断。
- 扩充 [[Fluent 高级网格主题]]，同步来源页、索引、Part II 和检查点。Chapter 7 仍进行中；下一节 7.11 Generating the Hexcore Mesh，从 p. 823 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 23（Chapter 7 续接）

- 按序完成 Chapter 7 7.11–7.13（PDF pp. 823–837）：Hexcore Cartesian/Octree 控制、Poly dual 网格质量与限制、Poly-Hexcore 混合控制。
- 扩充 [[Fluent 高级网格主题]]，更新来源页、索引和检查点。Chapter 7 仍进行中；下一节 7.14 Rapid Octree Meshes，从 p. 838 继续。


## [2026-10-15] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 24（Part II / Chapter 7 完成）

- 按目录完成 Chapter 7 7.14 “Generating Rapid Octree Meshes”（PDF pp. 838–868）：体域与边界定义、Boundary Projection/Cartesian Snapping、Improve Geometry Resolution、全局/局部尺寸、coarsening、curvature/proximity、anisotropic prism layers 和限制。
- 核对目录地图发现本章实际止于 p. 868；p. 869 起为 Appendix A。修正此前错误记成 pp. 605–916 的范围；未将附录并入 Chapter 7。
- 更新 [[Fluent 高级网格主题]]、Part II、来源页、索引和检查点。本次用户指定 Chapters 3–7 五章任务已全部完成 5/5；后续按目录可从 Appendix A p. 869 续接。

## [2026-10-16] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 25（Part II / Appendix A 完成）

- 核对来源身份（SHA-256 一致、6056 页）并按检查点续接：批次 10–24 由其他会话完成 Part II Chapters 3–7；本来源下一目录项为 Appendix A（p. 869）。开始前已在检查点登记 `in-progress`。
- 按目录逐条推进原则，本批仅处理一个目录条目 **Appendix A. Importing Boundary and Volume Meshes（PDF pp. 869–876）**：A.1 GAMBIT、A.2 ICEM CFD TetraMesher/RAMPANT、A.3 fe2ram 转换器与 I-deas/PATRAN/ANSYS/ARIES/NASTRAN 各格式要求。
- 新建知识页 `Fluent 第三方网格导入与 fe2ram 过滤器`：fe2ram 命令行全参数、输出不得为 CFF、VRML 1.0、各格式识别数据集（dataset/packet/bulk entries）、线性单元与抛物线中间节点告诫、分组规则（内部面节点不与边界面节点同组、2D PATRAN 体网格 Z=0 约束、ANSYS STIF63 限制）、周期边界统一指引（印刷 p. 728，属已摄取 Chapter 7）、重复节点合并命令、ARIES Prep7 六条件；所有导入边界 zone 视为 wall。
- p. 876 为版权页脚无正文；本批文本提取无表格错位，未触发额外视觉核对。更新 Part II 项目页、来源页（含补挂容错/2D/高级网格三个此前未挂的关联链接）、索引。
- 一处操作失误如实记录：清理来源页过时备注时误插了一个"### 批次 14"标题行，随即已删除并复核该区内容正确。
- 下一续接位置：Part II / Appendix B “Mesh File Format”，PDF pp. 877–892，从 p. 877 开始；其后 Appendix C（pp. 893–906）、Bibliography（pp. 907–908），Part III 自 p. 909。

## [2026-10-16] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 26（Part II / Appendix B 完成）

- 核对来源身份（SHA-256 一致）与检查点（无漂移）后，开始前登记批次 26 `in-progress`，按目录摄取 Appendix B "Mesh File Format"（PDF pp. 877–892），一次完成全条目。
- 新建知识页 `Fluent 网格文件格式（legacy .msh）`：节结构总则与二进制前缀约定；11 类网格节的格式（含声明节、右手法则、bc-type/element-type/face-type 全表、非一致相交面 bc-type+1000）；hanging-node 树节可读性差异（Face Tree 59 可在 meshing mode 读、Cell Tree 58 不可）；Interface Face Parents 61 跳过行为与 1.6.3 互转限制互证；Zone 节 39/45 的使用条件与十进制 zone-id；zone-type 枚举与 Scheme 符号命名规则；三个完整 2D 示例文件的节排布。
- 更新 Part II 项目页、来源页和索引。
- 边界：本格式为 legacy 文本/二进制 .msh，CFF（HDF5）内部结构不在附录范围；Part III 引用（印刷 p. 5920、5932）未摄取仅作定位；图 1–3 为图形元素；示例代码照录原文。
- 下一续接位置：Part II / Appendix C "Shortcut Keys"，PDF pp. 893–906，从 p. 893 开始；其后 Bibliography（pp. 907–908），Part III 自 p. 909。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 33（Part III / Ch.6 Model Topology 完成）

- 核对来源身份（SHA-256 一致、6056 页）与检查点（10 条目任务 8/10，下一未读 ⑨ Ch.6 p. 1155）。发现该章知识页已由先前会话建好（2026-10-16）但簿记缺失（日志与来源页批次记录止于批次 26、索引未挂 Part III 知识页）；开始前已在检查点登记批次 33 in-progress。
- 本批次以 pypdf layout 模式提取 PDF pp. 1155–1168 全章 14 页，与既有知识页逐节比对：6.1 收益与三分支树、6.1.3 六项限制（含 WebUI 重名问题）、6.2 CFD Pro 启用与不可回退 legacy、6.3 仅 Watertight 工作流、6.4.2 两种建体积方法与位置变更 Important、6.4.3 两类默认项与 [Default] 活动标签、6.4.4 感叹号/绿勾检查提示、6.4.5 By Association 着色与 Show Location、6.5 界面自动创建差异——全部主张与原文相符；Figures 6.1–6.8 为图形元素未摄取。
- 据原文两处小幅修订知识页：标注 6.1.2（p. 1157–1158）与 6.5（p. 1168）关于 New Volume 是否自动创建界面的手册内部表述张力（操作口径以 6.5 为准）；把 6.4.2 Important 的失效结果限定为"变更过的 physics volumes/boundaries 上评估的结果"。
- 簿记补录：来源页补批次 27–32 概录（①②=批次 27、③=批次 28 有项目页记录；④–⑧ 批次号无簿记可考，按顺序推定 29–32）与批次 33 条目，同步其续接检查点/摄取边界/尚未处理/关联页面；Part III 页已摄取清单补 Ch.1–6；index 补 Part II 快捷键页与 Part III 五个知识页。
- 状态：10 条目任务 9/10；下一未读 ⑩ Part III / Ch.7 Reading and Manipulating Meshes，PDF pp. 1169–1346，从 p. 1169 开始。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 34（Part III / Ch.7 章内第 1 段：7.1–7.3）

- 核对来源身份（SHA-256 一致）与检查点（10 条目任务 9/10，下一未读 ⑩ Ch.7 p. 1169），无漂移。Ch.7 全章 178 页，按小节分段：本批登记并完成 7.1–7.3（PDF pp. 1169–1201）。
- 新建知识页 `Fluent 网格读取与操作`：7.1 接受单元类型/悬挂节点默认读入时转多面体及关闭命令与 interior wall 报错三情形、可接受拓扑清单、七种单元 face-node 连接表（3D poly 无显式编号）、选型三考量与四档推荐组合、数值扩散六要点；7.2 轴对称 x 轴要求与周期边界两式、正交性双点积定义、正交质量按单元类型与增强定义开关、长宽比定义、Report Quality 与 check-verbosity 检查入口、手册阈值（正交质量 > 0.01、tri/tet 偏斜度 < 0.95 且超限时改欠松弛/耦合求解器、通道 ≥ 5 单元）、Eq 7.3 层流壁面间距式、单元分布/光顺度/流动场依赖性；7.3 网格来源清单、NASTRAN 三路径与识别 Bulk Data、CFX 分区两法与五类保留边界、TurboGrid、fe2ram 概要（细节交叉引用 Part II Appendix A 页不重复）、多文件读取三法（solution append / meshing 合并 / tmerge，tmerge 不支持 CFF）、悬挂节点转换产物在自适应与动网格下的限制、表面网格读入（PUMA 与 hanging node 两入口）。
- 提取缺口核验：Eq 7.3 公式体与 p. 1193 "constant z plane" 的坐标符号在 layout 提取中缺失，经 fitz 500 dpi 渲染视觉核对补全；Figures 7.1–7.25 为图形元素未摄取。质量阈值标注为手册通用指引而非验收标准。
- 更新来源页（批次 34 条目、续接检查点、摄取边界、关联页面）、Part III 项目页和索引。
- 下一续接位置：同章 7.4 Reference Frames，PDF p. 1202；其后 7.5（1206）、7.6（1212）、7.7（1250）、7.8（1279）、7.9（1290）、7.10（1296）、7.11–7.12 至章尾 p. 1346。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 35（Part III / Ch.7 章内第 2 段：7.4–7.6）

- 核对来源身份（SHA-256 一致）与检查点（下一未读 7.4，p. 1202），无漂移；按 30–60 页/批的章内分段口径登记并完成 7.4–7.6（PDF pp. 1202–1249，约 48 页）。
- 扩充知识页 `Fluent 网格读取与操作`：7.4 参考帧（User Defined 与 Track by Zone 两类、Constant Velocity/Motion Definition、点 OK 会把帧重定义为对话框当前设置的 Important、可用于 point surface/profile/injection/motion definition）；7.5 曲线坐标系（Direction 0/1 必填、Direction 2 叉积、Diffusion/Base Vector/Vector Projection 三法定向与线圈示例、多孔区禁变形/网格运动、Jump boundary 仅限闭环且每闭环至多一个、同 thread ID 注意事项）；7.6 非一致网格（交线生面的通量计算与 non-overlapping zone；六选项逐一整理含限制——one-to-one 接口仅支持 Coupled Wall、Mapped 不支持密度基求解器/Lagrangian DPM/动网格/shell conduction 且至少一侧全 solid、Static 误用于会动的界面结果错误；interface boundary metrics/projection/virtual polygon 三算法沿革与左手面处置命令；自动命名规则全集；要求与限制清单含容差不得大于相邻单元尺寸、many-to-many NCI 面不参与后处理、3D fan zone 禁用；7.6.4 使用流程十四步与 auto-options 全套 TUI、over-intersected 指标（面交叠 > 面积×1.25）、Interface Overlap Fraction 云图复查、delete-interfaces-with-small-overlap；运动传递 transfer-displacements/project-nodes 两法与 (recreate-sliding-interfaces) 迁移命令；多对多/一对一手动创建流程与差异）。
- p. 1202 顶部为 7.3.14 收尾步骤（PUMA 与 hanging node 两法的自适应设置入口），已并入知识页 7.3 节。本批提取无表格/公式缺口，未触发渲染核对；Figures 7.26–7.54 为图形元素未摄取。
- 更新来源页（批次 35 条目、续接检查点、摄取边界）、Part III 项目页和索引。
- 下一续接位置：同章 7.7 Overset Meshes，PDF p. 1250；其后 7.8（1279）、7.9（1290）、7.10（1296）、7.11–7.12 至章尾 p. 1346。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 36（Part III / Ch.7 章内第 3 段：7.7 Overset）

- 用户指定连续执行 5 批（批次 36–40）。核对 SHA-256 一致、检查点无漂移后登记批次 36，完成 Ch.7 之 7.7 Overset Meshes（PDF pp. 1250–1278，全十个小节）；p. 1250 顶部 7.6.4.3 收尾注记并入知识页 7.6 节。
- 扩充知识页 `Fluent 网格读取与操作`：Overset 概念（dead/solve/receptor/donor 分类、background/component 规则、一 zone 一接口、物理边界可重叠不可相交、collar mesh、cut control）；域连接三步（hole cutting、overlap minimization 与 donor-priority/grid-priority、donor search ≥4 单元）；诊断（seed 误置、重叠边界泄漏容差 ≤ 一壁面法向单元、orphan 处置原则——细化 donor 侧）；自适应（orphan/size/gap 标记、≤5 cycle×默认 2 sweep、自动模式每时间步单 cycle、控制项与默认值）；最佳实践（Coupled 推荐、双精度推荐、闭域不可压不支持、时间步准则、least squares/inverse distance 插值选择）；限制与兼容性清单（SRS 不兼容、DPM 高分辨追踪必须、边界条件排除清单、源项限制、多孔仅 superficial velocity）；设置（overset 边界须在建接口前定型）与后处理（Overset Cell Type 值表、积分重复计数误差随重叠增大）。
- 提取缺口核验：V_d/V_r > R_l³（3D）/R_l²（2D）判据与 k-ε/k-ω/Transition k-kl-ω 模型名经 fitz 500 dpi 渲染核对。手册 p. 1269 verbosity 命令印作 overset-interface（单数）与他处不一致，照录待核。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 7.8 Controlling Flow in Narrow Gaps，PDF p. 1279（批次 37 = 7.8–7.9，pp. 1279–1295）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 37（Part III / Ch.7 章内第 4 段：7.8–7.9）

- 五批连续任务第 2 批。SHA-256 一致、无漂移；完成 Ch.7 之 7.8 Controlling Flow in Narrow Gaps（Gap Model）与 7.9 Checking the Mesh（PDF pp. 1279–1295）；p. 1279 顶部 7.7.10 Overset 文件读写收尾（CFF 保存域连接）并入知识页 7.7 节。
- 扩充知识页：Gap Model（两型机制与适用、长限制清单、BC/材料/收敛建议、对话框全流程、Gap Reynolds Number 与 Eq 7.4、Sponge Layer 两种阻力类型、UDF 源项、Stabilization Level、专家命令组、场变量与稳态重初始化告诫、gap 重叠告诫）；网格检查（检查项全集、四类退化、负体积/零面积定位、check-verbosity 分级）与修复（劣质单元统计、solver 变量 1–6 及"默认 3/4/5、推荐 2"、Repair 能力、边界节点开关、多面体转换开关）。
- 提取缺口核验：Eq 7.4（Re_gap = ρ_avg·u_avg·L/μ_avg）经 500 dpi 渲染核对；p. 1290/1292 轴对称坐标轴符号按 7.2.1 陈述与报告样例互证。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 7.10 Reporting Mesh Statistics，PDF p. 1296（批次 38 = 7.10–7.12，pp. 1296–1346，Ch.7 收官）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 38（Part III / Ch.7 章内第 5 段：7.10–7.12，Ch.7 全章完成）

- 五批连续任务第 3 批。SHA-256 一致、无漂移；完成 Ch.7 最后一段（PDF pp. 1296–1346）：7.10 统计报告、7.11 多面体转换、7.12 网格修改。p. 1296 顶部 7.9.2 修复收尾并入知识页 7.9 节。**Ch.7 全章（pp. 1169–1346）完成，10 条目连续任务 10/10 收官**。
- 扩充知识页：统计报告四命令（含 Linux/Windows 内存定义与进程名）；多面体转换三路径与公共限制（全域 dual 聚合、边界层保留询问、hex 仅在与非 hex 相邻时转换、preserve-interior-zones、并行分区不自动迁移）；网格修改 22 项全览（合并/分离/断开/融合/周期区创建与解耦/slit（与 disconnect、separate 的语义区别、散热器出口改 mass-flow-inlet 用例）/定向/挤出/投影/替换与删除与停用与激活 zone（overset 须关插值、含界面 zone 须先初始化）/复制/替换整网（跨区插值不保守恒）/邻接改名/RCM 重排/缩放平移旋转（先于视角因子与初始化；保形连接区不可单独动）/光顺与换面（仅 quality-based 受推荐且并行可用）/边界层重分布/删除与提取单元）。
- 提取缺口：7.12 坐标轴符号按上下文与 7.2.1 约定互证补全（未逐处渲染）；Figures 7.84–7.111 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.8 Cell Zone and Boundary Conditions，PDF p. 1347（批次 39 = 8.1 Overview，pp. 1347–1369）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 39（Part III / Ch.8 第 1 段：8.1 Overview）

- 五批连续任务第 4 批。SHA-256 一致、无漂移；完成 Ch.8 之 8.1.1–8.1.11（PDF pp. 1347–1369）；8.1.12 自 p. 1370 起，留批次 40。
- 新建知识页 `Fluent Cell Zone 与边界条件设置`：zone 类型四大类清单（Table 8.1）；改类型规则（同类别互换、默认名自动改名、wall/shadow 一次性转换、periodic 需专流程）；设置与复制（zone 关联而非面、TUI 括号列表/通配符批量、q 退出生效、外部/内部 wall 求能量方程不可互拷条件）；Turbo CSV 导出与 System Coupling 共享节点；改名保留规则；参数体系全览（输入参数须带单位常数且不可引用其他表达式、单位变更影响参数值、默认名不复用、Scheme 过程 args->string 规则与单行限制、UDF RP_Get_Input_Parameter 宏、TUI advance/use-in/delete/list）。
- 本批无表格/公式提取缺口，未触发渲染核对；Figures 8.1–8.10 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.1.12 与 8.2 Cell Zone Conditions，PDF p. 1370（批次 40 = 8.1.12 + 8.2 起始段）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 40（Part III / Ch.8 第 2 段：8.1.12 + 8.2.1–8.2.3）

- 五批连续任务第 5 批（收官）。SHA-256 一致、无漂移；完成 PDF pp. 1370–1422（53 页，本来源单批最大）：8.1.12 保存/复用 BC、8.2.1 Fluid、8.2.2 Solid、8.2.3 Porous Media 全节。
- 扩充知识页 `Fluent Cell Zone 与边界条件设置`：Fluid（Laminar Zone 默认行为与保留 μt 的 TUI 开关、旋转轴同轴告诫、MRF/滑移运动与相对参考、Copy To Mesh Motion/Frame Motion）；Solid（纯固体域去激活流动方程、三种运动选项、速度须无散与唯一例外、Boundary Advection）；多孔介质全节（动量汇假设清单、表观/物理速度公式、初始化推荐、NETM dual cell 与不兼容清单、Darcy/惯性/幂律、14 步用户输入、阻力系数方向向量与正交化告诫及圆锥/曲线坐标系、Alternative Formulation、系数推导四法与 Δp–v 拟合法、NETM 设置流程与低 porosity 瞬态时间步建议、相对黏度"最后输入值作用全部多孔区"陷阱、Corey 相对渗透率与残余饱和 fix 命令、毛细压力五模型与限幅及作扩散替代、能量源不按 porosity 折算、各向异性限 2–3 数量级、2022R1+ presto-dissipation Scheme 变通）。
- 提取边界：Eq 8.1–8.55 公式体多为图形对象未提取，按公式周边文字记录结构与式号、未凭空补写（v_sup=γv、k_eff 体积平均等文字明确处除外，K'=8→C2=8000 m⁻¹ 按示例正文程序导出）；坐标轴符号按 7.2.1 约定补全；Figures 8.11–8.28 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.2.4 3D Fan Zones，PDF p. 1423。五批连续任务（批次 36–40）至此全部完成。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 41（Part III / Ch.8 第 3 段：8.2.4–8.3）

- 新一轮五批任务（41–45）第 1 批。SHA-256 一致、无漂移；完成 PDF pp. 1423–1442：8.2.3.9 尾注/8.2.3.10 多孔后处理（收尾）、8.2.4 3D Fan Zones、8.2.5 固定变量值、8.2.6 锁定温度、8.2.7 源项、8.3 操作条件（浮力驱动流）。
- 扩充知识页：3D Fan（环形分布动量源、拐点比、风机曲线缩放、轴向源两法、限制）；固定值（不解方程不计残差、压力基限制、全速度固定则表压置零）；温度锁定（与固定值区别、BCGSTAB 不兼容）；源项（单独成区、质量源配套要求、末组分差值法、P-1 源配反号能量源、单位体积折算）；操作条件（封闭域两法、Boussinesq 适用与限制、操作密度建议、PRESTO!、高 Rayleigh 数无稳态解警示）。
- 提取边界：Eq 8.56–8.69 公式体未提取按周边文字记录；湍流源单位部分残缺可辨；Figures 8.29–8.33 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.4 Boundary Conditions，p. 1443（批次 42 = 8.4.1–8.4.9，pp. 1443–1494）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 42（Part III / Ch.8 第 4 段：8.4 开头与 8.4.1–8.4.9）

- 五批任务（41–45）第 2 批。SHA-256 一致、无漂移；完成 PDF pp. 1443–1494：8.3.1.6.1 高 Rayleigh 数策略（8.3 收尾）、8.4 引导、8.4.1–8.4.2 十二类进出口总览与入口湍流参数、8.4.3 压力入口、8.4.4 速度入口、8.4.5 质量流入口、8.4.6 质量流出口（含 ECMF）、8.4.7 进口通风口、8.4.8 吸气风扇、8.4.9 压力出口。
- 扩充知识页：湍流入口参数通用参考（各模型 method、I/ℓ/μt/μ 定义与默认值、8.74–8.82 换算、SRS 脉动速度）；多类入口共享要点（Supersonic/Initial Gauge Pressure、静水压、圆柱坐标正方向、Local Cylindrical Swirl 禁忌、温度按相语义、Prevent Reverse Flow）；七类边界逐节整理（choked 告诫、轴对称 2π/1 弧度惯例、Average Mass Flux、混合面联动、ECMF、径向平衡 bins、Strong/Weak Averaging、压力 profile 乘子、目标质量流设置与限制）。
- 提取边界：Eq 8.70–8.107 公式体未提取按周边文字记录（文字明确处除外）；个别数值缺失按上下文定性记录；Figures 8.34–8.44 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.4.10 Pressure Far-Field，p. 1495（批次 43 = 8.4.10–8.4.15，pp. 1495–1534）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 43（Part III / Ch.8 第 5 段：8.4.10–8.4.15）

- 五批任务（41–45）第 3 批。SHA-256 一致、无漂移；完成 PDF pp. 1495–1534：8.4.9 目标质量流策略收尾、8.4.10 压力远场、8.4.11 Outflow、8.4.12 出口通风口、8.4.13 排气风扇、8.4.14 Degassing、8.4.15 Wall 边界条件全节。
- 扩充知识页：far-field（理想气体限制、20 倍弦长、Riemann 不变量、flux-based 与切向修正）；outflow（不可用清单、回流告诫、权重归一陷阱）；degassing（质量汇机制、主相须液、必须开重力）；Wall 全节（粗糙壁不兼容模型清单、结冰模型限制、壁面运动法向分量被忽略、四种剪切条件、热条件七型、薄壁/双面墙/壳导热/System Coupling/Mapped Interface 的关键约束、二次梯度限制、边界对流自动检测、washcoat 因子、剪切与换热计算语义）。
- 提取边界：Eq 8.108–8.130 公式体未提取按周边文字记录（文字明确处除外）；结冰关联式与换热公式定性记录；Figures 8.45–8.59 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.4.16 Perforated Wall，p. 1535（批次 44 = 8.4.16–8.4.22，pp. 1535–1572，8.4 收官）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 44（Part III / Ch.8 第 6 段：8.4.16–8.4.22，8.4 大节完成）

- 五批任务（41–45）第 4 批。SHA-256 一致、无漂移；完成 PDF pp. 1535–1572：8.4.15.15.6（Wall 收尾）、8.4.16 多孔壁、8.4.17 Symmetry、8.4.18 Periodic、8.4.19 Axis、8.4.20 Fan、8.4.21 Radiator、8.4.22 Porous Jump。**8.4 大节 22 小节全部完成。**
- 扩充知识页：多孔壁（Uniform/Discrete、动态/静态注入、CHT 耦合三前提、输入文件关键字表、后处理变量）；symmetry/periodic/axis 的语义与告诫（axis 在 y=0、periodic 默认 Translational 与网格周期性核查）；fan（Zone Average Direction、限速只限压跃升、profile 升序、后处理关节点值）；radiator（K 线性递减示例、h 二阶拟合示例、绝对零度给实际热流技巧）；porous jump（公式语义、耦合求解器收敛告诫、默认值为无阻力模型）。
- 提取边界：Eq 8.131–8.152 公式体未提取按周边文字记录（文字明确处除外）；fan Hub Radius 默认数值未提取；Tables 8.2–8.3 提取完整；Figures 8.60–8.81 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.5 Editing Multiple Boundary Conditions at Once，p. 1573（批次 45 = 8.5–8.8，pp. 1573–1615）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 45（Part III / Ch.8 第 7 段：8.5–8.8）

- 五批任务（41–45）第 5 批（收官）。SHA-256 一致、无漂移；完成 PDF pp. 1573–1615：8.4.22 补遗、8.5 Multi Edit、8.6 瞬态边界条件、8.7 边界声学波模型（四类）、8.8 用户自定义风机模型。
- 扩充知识页：Multi Edit（图标语义、单面/耦合墙不可混选、绿勾字段必应用）；瞬态 BC 三格式（标准/表格 profile 的 SI/全小写/周期闭合规则、运动网格变量名 v_x/omega_x）；声学波模型四件套对照（turbo NRBC 的密度基/稳态/理想气体/结构网格/禁回流限制与混合面、并行单分区；general NRBC 的 LRM、sigma 0.15 / sigma2 5.0、目标质量流互斥、切向流回流方向告诫、CFL 2.0/4.0 最佳实践；IBC 的反射系数极点-留数近似与无源性 |R0|<1、cell acoustic CFL<1、连续性 1e-4、impedance 工具全参数与省略 R C 建议；TFF 的入射波强 profile 与 CFL≤1）；用户自定义风机（三参数、fantest.f 流程、(update-user-fans) 初始化、profile 名自动出现在 Fan 对话框）。
- 提取边界：Eq 8.153–8.214 公式体未提取按周边文字记录（文字明确处除外）；turbo NRBC 欠松弛默认值与 TFF 波强式未提取；瞬态 profile/阻抗数据/fantest.f 示例照录；Figures 8.82–8.95 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 8.9 Profiles，p. 1616；8.9–8.11 至章尾 p. 1650。五批连续任务（批次 41–45）至此全部完成。

## [2026-10-17] query | NUMECA 网格导入 Fluent 警告解读与 outflow 修复

- 用户将 NUMECA（AutoGrid）导出的 turbomesh.msh（叶轮机械 rotor+stator 单通道，约 100 万节点 / 95 万 hex）读入 Fluent 2026 R1，附 transcript（`../test/meshtest`，非网格文件）请求解读。
- 诊断：`Reversing N faces` 为读取时对边界面区的自动法向翻转，无害（实测判断，手册未见明文）；`Both outflow and pressure boundaries are present` 为阻断性警告——zone 65 `rotor_outflow_1` 为 outflow，与 pressure-outlet/velocity-inlet/pressure-inlet 共存。依据 8.4.11（outflow 不可用于含压力入口的问题），修复为把该区 zone-type 改成 pressure-outlet（GUI 或 `define/boundary-conditions/modify-zones/zone-type`）。
- 新建 [[NUMECA 网格导入 Fluent 警告解读]]（首个 analyses 页），链接 [[Fluent Cell Zone 与边界条件设置]]、[[Fluent 网格读取与操作]]、[[Fluent 求解模式文件读写]]；索引新增"综合分析"小节。
- 待核实：`rotor_stator_10_left/right` 与周期对的接口设置属后续步骤，尚未实测验证；如用户继续设置界面再归档。

## [2026-10-17] query | NUMECA 细碎分区的 Fluent 内合并简化

- 用户追问：NUMECA 导出网格分区过碎（15 个 cell zone、百余个面区），在 Fluent turbo 工作流中不便，如何合并简化。
- 综合回答（更新 [[NUMECA 网格导入 Fluent 警告解读]]）：依据 7.12.1 用 Domain → Zones → Combine → Merge（TUI `mesh/modify-zones/merge-zones`）按"同类型 + 将共享同一 BC"分组合并——15 个 cell zone 各并为 rotor/stator 两个流体区、rotor_hub_1..4 等墙面按物理组各并一个；合并后经 7.12.14 改名。红线：rotor/stator 之间、periodic 对与 shadow、不同运动/热条件的壁面均不可互并；先合并后建 mesh interface；合并后存新 case。7.12.4 fuse 不需要（interior-* 为块间连接面）。源头治理（NUMECA 导出时合并 patch）与 Turbo Setup 衔接标注为产品经验，对应手册章节尚未摄取。
- 索引条目同步扩充；待验证项：AutoGrid 导出 patch 合并选项的实际效果、`merge-cell-zones` 命令在 2026 R1 的实存性。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 46（Part III / Ch.8 第 8 段：8.9–8.11，Ch.8 全章完成）

- 十批连续任务（46–55）第 1 批。SHA-256 一致、无漂移；完成 PDF pp. 1616–1649：8.9 Profiles、8.10 GT-POWER 耦合、8.11 WAVE 耦合；p. 1650 为空白版权页。**Ch.8 全章（pp. 1347–1649）完成。**
- 扩充知识页 `Fluent Cell Zone 与边界条件设置`：六种 profile 类型与插值（point 零阶默认/line/mesh 零阶、radial/axial/transient 线性升序、radial 轴确定规则）；标准格式（≤64 字符全小写、SI、必含坐标字段）与 CSV 格式（[Name]/[Parameters]/[Spatial Fields]/[Data]/[Faces] 节标识、类型字段标签、逗号分隔、SI/单位规则、保留 X 轴标签）；三种点插值（Constant/Inverse Distance/Least Squares）与 cell zone 不适用、容差回退 TUI；profile 挂参考系、体积源项的线性化限制；删除/替换顺序告诫；重定向（Orient：坐标字段必须小写 x,y,z、Euler 角旋转矩阵+平移向量）与复制（Full 360 deg.、扇区计数、Autofill、复数模态 harmonic index/Complex Pair 单对限制）；GT-POWER/WAVE 耦合（边界类型、20 区上限、面积 5% 校核、Mass Flux 强制、k-ε 自定义建议、组分 Chemical Formula 对应、50 组分上限、GTI 不向后兼容、WAVE 五组分与同步保存间隔）与转矩-转速耦合（v2017.2+、墙名=叶轮机名）。
- 提取边界：Eq 8.215–8.224 公式体未提取按周边文字记录（8.224 转速式按变量定义导出为 rpm=60V/(πD)）；Figures 8.96–8.111 为图形元素。
- 更新来源页、Part III 项目页和索引（索引由其他会话新增了综合分析条目，已在其最新状态上编辑）。
- 下一续接位置：Part III / Ch.9 Physical Properties，p. 1651（批次 47 = 9.1–9.4，pp. 1651–1699）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 47（Part III / Ch.9 第 1 段：9.1–9.4）

- 十批任务（46–55）第 2 批。SHA-256 一致、无漂移；完成 PDF pp. 1651–1699：9.1 材料定义、9.2 温度函数属性、9.3 密度、9.4 黏度。
- 新建知识页 `Fluent 物理属性`：材料六类与三大库（Fluent 675 种/GRANTA MDS 需单独许可/用户 .scm）、纯流体与 mixture species 独立对象告诫、Name 29 字符上限；温度函数四型（NASA-9 仅 Cp；分段线性 50 点/3 区间/8 区间上限；外推规则；系数按 K/R 输入；解限值保证物理有效）；密度七法（流态选型、可压理想气体多区不混用、compressible-liquid Tait 六输入与默认值 7.15/1.1/0.9、组分依赖五法与混合公式）；黏度（Sutherland 两/三系数空气值、幂律、动能理论、Gupta 30,000 K、mass-weighted/ideal-gas-mixing-law、四种非牛顿模型与 Arrhenius 因子、湍流不可用、挂主相建议）。
- 提取边界：Eq 9.1–9.44 公式体未提取、按周边文字与变量定义记录（非牛顿模型标准形式按文字与空气系数对应给出；Tait/动能理论混合式仅记语义）；空气物性为原文数值；.scm 示例照录；Figures 9.1–9.21 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 9.5 Thermal Conductivity，p. 1700（批次 48 = 9.5–9.10，pp. 1700–1734）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 48（Part III / Ch.9 第 2 段：9.5–9.10）

- 十批任务（46–55）第 3 批。SHA-256 一致、无漂移；完成 PDF pp. 1700–1734：9.4.6.5.1 Herschel-Bulkley 输入（9.4 收尾）、9.5 导热系数（含固体各向异性六法）、9.6 UDS 扩散率、9.7 电导率、9.8 热容、9.9 辐射属性、9.10 质量扩散系数。
- 扩充知识页：导热各向异性仅压力基、后处理零值与 XX…ZZ 分量、biaxial 仅壳、cyl-orthotropic 近壁用旁单元；UDS 扩散双求解器可用但后处理仅各向同性单元；辐射按模型的属性矩阵、WSGGM 三选项与颗粒/烟灰交互开关（DPM 仅 P-1/DO）、相函数四选；质量扩散七法（三种不适用于完整多组分）、湍流 Schmidt 0.7 一般不改、完整多组分不推荐湍流、多孔各向异性组分扩散默认单位阵。
- 提取边界：Eq 9.45–9.71 公式体未提取按周边文字记录；各向同性 UDS 默认扩散系数值未提取；Figures 9.22–9.37 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 9.11，p. 1735（批次 49 = 9.11–9.17，pp. 1735–1798，Ch.9 收官；先补记热扩散系数延续步骤）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 49（Part III / Ch.9 第 3 段：9.11–9.17，Ch.9 全章完成）

- 十批任务（46–55）第 4 批。SHA-256 一致、无漂移；完成 PDF pp. 1735–1797：9.10.4 收尾、9.11–9.14（标准态焓熵/未燃热扩散率/动能理论参数）、9.15 操作压力、9.16 参考压力、9.17 真实气体模型全节。**Ch.9 全章（pp. 1651–1797）完成**；p. 1798 空白。
- 扩充知识页：标准态焓熵（可逆反应才需熵）；操作压力三意义（不可压理想气体决定密度/低 Mach 防舍入/高 Mach 设 0）与 Table 9.1 建议；参考压力分组机制与 method 2 迁移命令；真实气体三方案对照（区域覆盖、两相限制、边界限制、NRBC/多相/反应兼容性）；立方 EOS 四模型参数需求与伪临界混合两法、Vapor/Liquid 状态选择与 spinodal 警告、DPM 液滴温度限 Table 9.2（水 582.3 K）与蒸发-沸腾切换；NIST 152 流体（带 * 仅无黏）、单仿真一种 NIST 材料、查找表 20 species 上限与 10% 表外指标、不随 case 保存；UDRGM C 函数集与 RealGasFunctionList 固定顺序、参考温度 298.15 K 一致性、体积反应后开；RGP 表预处理查表、rgp-table 自动带 Cp/k/μ、饱和属性 rgp-table-sat、连续性线性化 TUI。
- 提取边界：Eq 9.72–9.114 公式体未提取按周边文字记录（文字明确处除外）；Tables 9.1–9.3 照录；UDRGM 代码清单照录；Figures 9.38–9.52 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.10 Modeling Basic Fluid Flow，p. 1799（批次 50 = Ch.10 整章，pp. 1799–1830）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 50（Part III / Ch.10 Modeling Basic Fluid Flow，Ch.10 全章完成）

- 十批任务（46–55）第 5 批。SHA-256 一致、无漂移；完成 PDF pp. 1799–1829（p. 1830 空白）：10.1 UDS 输运方程、10.2 流向周期流动、10.3 旋流与旋转流、10.4 可压流动、10.5 无黏流动。
- 新建知识页 `Fluent 基本流动建模`：UDS（50 条上限从 0 编号、Flux/Unsteady Function 三选、固体区忽略 MRF 对流、湍流扩散不自动叠加、Specified Flux/Value 与 Coupled Boundary、收敛手段 F-Cycle/BCGSTAB/ILU）；流向周期（不可压限制、单周期对、压力基质量流/压力梯度 + β 子迭代、密度基压降、云图周期/shadow 差异）；旋流（五分类、旋流数 S 阈值选 RNG/realizable k-ε 或 RSM、轴对称旋流设置、五步分步求解、渐进升速、PRESTO!、欠松弛建议）；可压（Mach 分区、良定边界组合、压力出口超音忽略静压、浮动操作压力原理与限制、滞止初始化 + URF 0.4/0.3 策略）；无黏（滑移壁、初场用途）。
- 提取边界：Eq 10.1–10.22 公式体未提取按周边文字记录（Mach/声速/0.5283 等明确处除外）；Figures 10.1–10.12 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.11 Moving Reference Frames，p. 1831（批次 51 = Ch.11 整章，pp. 1831–1850）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 51（Part III / Ch.11 Moving Reference Frames，Ch.11 全章完成）

- 十批任务（46–55）第 6 批。SHA-256 一致、无漂移；完成 PDF pp. 1831–1849（p. 1850 空白）：11.1 引言（SRF/MRF/SMM 三路线）、11.2 SRF、11.3 MRF。
- 新建知识页 `Fluent 运动参考系`：SRF 壁面要求（旋转面静止墙/旋转周期边界/非旋转面须分区的告诫）；速度公式选择（最小速度参考系减小数值扩散；切换须重初始化；密度基恒绝对）；设置（Frame Motion、Solid Motion 分界、CHT 无须固体 Frame Motion、Copy To Mesh Motion）；MRF frozen rotor 近似与适用（弱转子-静子干涉、滑移初场）；七项限制（界面须旋转面/平移平行、MRF 非定常慎用、DPM 轨迹参考系与速度突变、多 MRF+相对公式禁轴对称旋流、时变速度禁止、mixture 模型用绝对公式、耦合界面拆分）；mrf-to-sliding-mesh 命令；网格保形/非保形两法；设置八步（初始化必须 Absolute）；后处理（相对量、参考区周向平均、Rothalpy）。
- 提取边界：Ch.11 无编号公式；Theory Guide 式 2.16 未提取；坐标轴符号按约定补全；Figures 11.1–11.8 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.12 Managing Motion Definitions，p. 1851（批次 52 = Ch.12 整章，pp. 1851–1854）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 52–53（Part III / Ch.12 + Ch.13，两章完成）

- 十批任务（46–55）第 7、8 批。两章极短（4+6 页）且相邻，**一次提取读完并在日志中合并记录**；登记与完成仍按两批分别记录。SHA-256 一致、无漂移。批次 52 = Ch.12 Managing Motion Definitions 全章（pp. 1851–1853；p. 1854 空白）；批次 53 = Ch.13 Managing Auxiliary Geometry Definitions 全章（pp. 1855–1860）。
- 新建知识页 `Fluent 运动定义与辅助几何`（两章合页）：运动定义四元组（名称/参考帧/平移/旋转）与 Rigid Body Motion、System Coupling Motion 两型，字段支持常数/表达式/输入参数/命名表达式；辅助几何三用途（PUMA 自适应、变形动网格、滑移网格投影）与四类型（Primitive 五种基元——Frustum/Cylinder 只含曲面、User-Defined DEFINE_GEOMETRY、Surface Mesh STL、Reconstruction 重建——尖锐特征边须分区定义）、Display Options 分辨率。
- 提取边界：无公式；Figures 12.1–12.2、13.1–13.5 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.14 Modeling Flows Using Sliding and Dynamic Meshes，p. 1861（批次 54 = 14.1–14.6.2.1，pp. 1861–1900；批次 55 = 14.6.2.2 起，pp. 1901–1931）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 54（Part III / Ch.14 第 1 段：14.1–14.6.2.1）

- 十批任务（46–55）第 9 批。SHA-256 一致、无漂移；完成 PDF pp. 1861–1900：14.1 引言（滑移 vs 动网格选择、同区不兼容）、14.2–14.4 滑移示例/技术/界面形状、14.5 使用滑移网格全节、14.6 动网格设置与 14.6.2.1 光顺方法族。
- 新建知识页 `Fluent 滑移与动网格`：滑移 vs 动网格选择准则与同区不兼容告诫；滑移网格要求（界面无法向运动、独立 face zone、周期角一致、periodic repeats 五限制、耦合界面拆分、压力振荡与 Matching、gap model）；设置七步（Mesh Motion、interface 类型、墙默认相对零速、Mesh Interfaces 三选项、辅助几何投影、预览、Moving Mesh Courant Number）；mrf-to-sliding-mesh 两 Important（固体邻接不适用/包围不适用，手动 disconnect-fuse 备选）；时间周期解（周期公式、5% 判据、起动大时间步、变更 ≤20% 与末几周期不改）；后处理（periodic repeats、相对速度、相交区不能建 zone surface 与图形不连续、时间平均须周期后开）；动网格 13 步设置（PISO、动区自动墙条件例外）；光顺七法全览（扩散双扩散率与 α 0–2/旋转 1.5、弹簧因子 0–1、线弹性 Poisson −1.0–0.5 与可不指定几何、RBF 四优点与 Local Smoothing、参考位置自动启用与 legacy 告诫、Laplacian 仅偏斜改进才动、边界层 Deform Adjacent Boundary Layer）与兼容性矩阵（与 adaption 不兼容、RBF 唯一支持周期/动墙、扩散/线弹性不兼容边界层光顺等）。
- 提取边界：Eq 14.1–14.14 公式体未提取按周边文字记录（扩散方程/Hook 定律/Laplacian 语义明确处除外；14.3/14.4 幂律形式未提取）；数值为原文正文数值；Figures 14.1–14.29 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 14.6.2.2 Dynamic Layering，p. 1901（批次 55 = 14.6.2.2–14.6.2 末，pp. 1901–1931）。

## [2026-10-17] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 55（Part III / Ch.14 第 2 段：14.6.2.2–14.6.2.5）

- 十批任务（46–55）第 10 批（收官）。SHA-256 一致、无漂移；完成 PDF pp. 1901–1931：14.6.2.2 动态层化、14.6.2.3 重划、14.6.2.4 体积网格更新程序、14.6.2.5 瞬态考量；补记 14.6.2.1 边界层光顺。
- 扩充知识页 `Fluent 滑移与动网格`：动态层化（Height/Ratio Based 分裂与 collapse 合并、因子 α_s/α_c、适用条件与滑移界面过渡）；重划 Unified 默认与 Methods-Based 五法（local cell——3D 偏斜默认 0.9/2D 0.7、zone remeshing 回退 0.98；local face；cell zone；face region 与棱柱层体积分解建议；2.5D surface 仅兼容 Laplacian）；尺寸函数（Variation α_s∈[−1,1]、Rate β>−1、Resolution 2D 3/3D 1）与 sizing controls/prism controls 全参数；体积网格更新自动选法、并行微差与 shell conduction 耗时；瞬态考量（重划事件使二阶时间格式回退一阶、verbosity 监控、网格交换触发）。
- 提取边界：Eq 14.15–14.24 公式体未提取按周边文字记录；Figures 14.30–14.50 为图形元素。
- 更新来源页、Part III 项目页和索引；同步补全检查点逐章进度表（Ch.8–Ch.14 行，此前批次 46–54 未回写该表）。
- **用户指定的十批连续任务（批次 46–55）全部完成**：合计约 312 页（34+49+35+63+31+19+4+6+40+31），Ch.8 收官 + Ch.9/10/11/12/13 全章 + Ch.14 之 14.1–14.6.2。
- 下一续接位置：同章 14.6.3 Feature Detection，p. 1932（14.6.3–14.6.11 至章尾 p. 1992）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 56（Part III / Ch.14 第 3 段：14.6.3–14.6.11，Ch.14 全章完成）

- 十批任务（56–65）第 1 批。SHA-256 复验一致、无漂移；完成 PDF pp. 1932–1992（61 页）：14.6.3 特征检测、14.6.4 In-Cylinder（含 14.6.4.1 缸内设置示例全节）、14.6.5 Six DOF、14.6.6 隐式更新、14.6.7 接触检测、14.6.8 动网格事件、14.6.9 动区运动指定（含解稳定化与刚体运动学）、14.6.10 运动预览、14.6.11 稳态动网格。**Ch.14 全章完成。**
- 扩充知识页 `Fluent 滑移与动网格`：特征检测 Feature Angle 语义与三条适用性；In-Cylinder 曲轴角设置（步长默认 0.5°）、piston-full/piston-limit（曲柄半径/连杆/活塞销偏移）、Eq 14.25–14.27 语义、缸内输出 8 列与轴默认值、三区网格拓扑（层化区保形/重划区/静止气道，阀层化区与燃烧室间必须滑移界面）、阀 profile angle(度)/lift(米) 字段、最小阀升程 0.1 mm 示例、关阀=删滑移界面转墙；Six DOF 属性组（Mass+惯量张量必填、One DOF、Hooke 弹簧、Constrained）；隐式更新三参数与三类禁用；接触检测两法（Contact Zones 多孔区完全兼容 vs Contact Marks 零质量流完全堵流、仅压力基/无 GG-Node Based/QUICK/NITA）；20 种事件类型；动区六型流程与各型边界条件默认行为差异（Rigid Body/User-Defined 默认计入、Deforming 默认不计入）；解稳定化（volume/coefficient-based、只影响收敛速率）；刚体运动学（profile 六字段、欧拉角约定 ψ-θ-φ）；预览两法差异（Mesh Motion 实改网格必须先存 case）；稳态动网格（dtime=1、三不可用）。
- 提取边界：Eq 14.25–14.39 公式体未提取按周边文字记录；Figures 14.51–14.96 为图形元素。**笔误自纠**：向知识页插入 14.6.3–14.6.11 大块时再次覆盖了"证据与适用条件"标题，当即发现恢复。
- 簿记：更新来源页（检查点块/尚未处理/关联页面——补记此前缺漏的四个知识页链接/批次 56 条目）、Part III 项目页（Ch.14 行转完成、待摄取行改 Ch.15）、索引、检查点（最近完成/活动任务/活动批次/逐章进度表 Ch.14 行转 completed/开始结束段）。
- 下一续接位置：Part III / Ch.15 Modeling Turbomachinery Flows 段 1（15.1–15.3，pp. 1993–2035）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 57（Part III / Ch.15 第 1 段：15.1–15.3）

- 十批任务（56–65）第 2 批。SHA-256 一致、无漂移；完成 PDF pp. 1993–2035（43 页）：15.1 Turbo Setup 引导工作流、15.2 Frozen Gust/入口扰动、15.3 叶排干涉建模。
- 新建知识页 `Fluent 叶轮机械流动`：工作流入口与 _workflow_files 依赖；11 任务要点（部件四类型与 End Wall Gap 默认 rotor Yes/stator No、连续行集、五类网格格式与多叶片区支持、区名改写规则、扇区数估计与区名加扇区号、物理三流体选项、进出口三组合与合并默认、拓扑跳过选项、iso 面 0.25/0.5/0.75、报告监视器、Edit/Revert and Edit 语义与单位自动换算、.wft 版本内嵌、Write case files/Do not save data 偏好）；Frozen Gust 两构型五步流程（profile 链接旋转参考系 vs Mesh Motion）；GTI 三类 pitch-change（PS 拉伸压缩通量 profile 且节距比 < 2、NPS 虚拟副本任意节距比与 nps-minimize-po-loss、MP 周向平均默认 40 带且仅 Frame Motion）与 FR/TRS 由 zone motion 隐式判定；求解器/模型兼容清单（多相除 Wet Steam、辐射、DPM、声学不可用；不支持 repartition/migration）；ensemble 整数节距比才可 TRS；Interface Check（相交率 ~100%、周期贴合、ghost link、面排序）；legacy 混合面限制（无 LES/组分/VOF、DPM 非耦合）与设置（出口必须 pressure outlet、质量守恒须 mass-flow inlet、Radial/Axial 几何、Area/Mass/Mixed-Out、Eq 15.1 欠松弛）及定压/旋流/总焓三守恒选项。
- 提取边界：Eq 15.1 公式体未提取按周边文字记录；Figures 15.1–15.8 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 15.4 Aerodynamic Damping（Blade Flutter Analysis），p. 2036（批次 58 = 15.4–15.5，pp. 2036–2076）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 58（Part III / Ch.15 第 2 段：15.4–15.5）

- 十批任务（56–65）第 3 批。SHA-256 一致、无漂移；完成 PDF pp. 2036–2076（41 页）：15.3.4.3 混合面求解策略（补齐批次 57 未含的章内尾段）、15.4 气动阻尼（叶片颤振分析）、15.5 相位滞后法。
- 扩充知识页 `Fluent 叶轮机械流动`：混合面倒流处置与平均方法切换；颤振六步共同设置（报告定义须在流场初始化后建）；振型 .csv 格式（EXPROFILE/EXOPTION、Harmonic Index、Passage number 右手定则编号、Mesh Motion 须局部参考系、System Coupling 对齐粗 FEM 网格）；频率基准时间推进；Periodic Displacement 组与 Fast Mesh Smoothing（实/虚分解预解存储省时）；Amplitude/Scaling 推荐初值（弦长 0.05%/0.5）；动网格区配置（叶片 User-Defined、shroud 回转面 Deforming、带界面 tip gap 不支持）；TWM（IBPA=节距×节径、能量法 Eq 15.2 正功阻尼/负功激发、每节径 FTW+BTW、全轮/周期扇区/单通道+phase-lag 三构型、谐波压力 .csv 导出供 FEM 强迫响应）；ICM（一次运行全覆盖节径、中间叶片振动叠加、仅实振型、叶数须奇数、Aerodamping/Generalized Force 报告）；Phase-lag（时间 Fourier 分解原理、k-ε/k-ω/SST/Wet Steam 限定、界面两创建法、NumberSectors360 自动谱描述、每周期 ≥40 步、双精度建议）。
- 提取边界：Eq 15.2–15.13 公式体未提取按周边文字记录；Figures 15.9–15.16 为图形元素。手册原文瑕疵记录：p. 2070 小节标题残留跨章编号"21.2.3.6"；/define/turbo-mode/... 命令路径疑为 turbo-model 之误。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 15.6 Non-equilibrium Wet Steam Model，p. 2077（批次 59 = 15.6–15.10 至章尾，pp. 2077–2124，Ch.15 收官）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 59（Part III / Ch.15 第 3 段：15.6–15.10，Ch.15 全章完成）

- 十批任务（56–65）第 4 批。SHA-256 一致、无漂移；完成 PDF pp. 2077–2124（48 页）：15.6 湿蒸汽模型、15.7 叶片气膜冷却、15.8 叶轮机械描述、15.9 叶轮专属数值（TSN）、15.10 叶轮机械后处理；补记 15.5.3.4 尾段。**Ch.15 全章完成。**
- 扩充知识页 `Fluent 叶轮机械流动`：phase-lag 第三初始化流程与后开定常 .dat 报错告警；湿蒸汽模型求解器与 phase-lag 兼容；BFC 虚拟孔全流程（孔心 .csv 与参考帧语义——shroud 冷却用 global、冷转子用跟随参考系；radial-distribution 二次温度分布自动保焓通量；overlap/non-overlap 生成与 vbr 内部 profile；周期对孔位自动旋转；限制五条含瞬态转子 Mass Flow 陷阱与多界面孔位更新陷阱）；TSN 条件与参数（HOTR 0.1、Limiter Filter、备选欠松弛 0.5→0.1）；后处理全节（拓扑封闭域与 Theta Min/Max 定义叶片、零角线、专属变量七项、Fourier 系数移动平均/公共周期/图形谱欠松弛 1.0 与 phase-lag 0.7 的差异、多行频率选择三算法、Turbo Report 各量 Eq 15.19–15.44 语义、Turbo Performance 命名表达式与仅可压流限制、MassFlowAveAbs 比值方向随 Process 反转）。
- 提取边界：Eq 15.14–15.44 公式体未提取按周边文字记录；Figures 15.17–15.39 为图形元素。手册命令路径不一致第三处记录（turbo-models vs turbo-model）。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.16 Modeling Turbulence 段 1（16.1–16.9，pp. 2125–2166；批次 60）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 60（Part III / Ch.16 第 1 段：16.1–16.9）

- 十批任务（56–65）第 5 批。SHA-256 一致、无漂移；完成 PDF pp. 2125–2166（42 页）：16.1 引言与模型清单、16.2 湍流模型选型全节、16.3 使用步骤、16.4 SA、16.5 k-ε、16.6 k-ω（含 GEKO/WJ-BSL-EARSM）、16.7–16.9 转捩模型设置。
- 新建知识页 `Fluent 湍流模型设置`：默认 k-ω SST 与 Preferences 改默认；RANS 各模型定位（SA 航空壁面流勿作通用、k-ε 分离不敏感与 Realizable+EWT/ML 推荐、standard k-ω 来流敏感不推荐、BSL/SST 推荐、SST 低涡黏特性、low-Re 项不建议）；GEKO 四系数（Csep 分离 1.75 吻合扩压器、Cnw 后台阶、Cmix 掺混、Cjet 射流 1.0）与 2024 默认版；RSM 强旋转曲率与 EARSM 折中；转捩四模型（γ-Reθ 非伽利略不变/不适合管槽流、γ 唯一计横流失稳、Alg-γ 零附加方程、k-kl-ω 不再开发；低 Re 网格膨胀因子 < 1.15、tet/prism 不推荐、进口湍流衰减先估）；增强项取舍（Sarkar 默认关、浮力开 k 源项）；壁面处理（y⁺ 不敏感推荐、壁面函数 y⁺ ~30 下限、Scalable 解网格限制）；网格（SA/SST ≥10 层结构化在层内、棱柱全覆盖）；SRS 全景（LES 仅限无壁边界层场景/WALE、WMLES 与增强版、SAS von Karman 尺度不依赖网格间距、DES GIS 与 DDES 重标定默认、SDES/SBES 取代、SBES+WALE 最优、ELES 分区与 Vortex Method/Spectral Synthesizer）；SRS 网格与数值（CFL~1 主 SRS 区、BCD 复杂应用首选、CD 声学、PRESTO! 不推荐、LeastSquares/GG-Node 梯度、NITA→SIMPLEC/PISO→耦合、压力校正 0.7、连续性每步 2 量级、Extrapolate 省 40%）；使用步骤与各模型设置选项清单（含 GEKO TUI 全菜单与 DEFINE_TRANS 关联 UDF）。
- 提取边界：Eq 16.1–16.3 公式体未提取按语义记录；Figures 16.1–16.17 为图形元素。提取文本希腊字母系统性丢失——模型/系数名按标准名与 TUI 命令核实补全（记录于证据节）。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 16.10 Setting Up the Reynolds Stress Model，p. 2167（批次 61 = 16.10–16.20 至章尾，pp. 2167–2220，Ch.16 收官）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 61（Part III / Ch.16 第 2 段：16.10–16.20，Ch.16 全章完成）

- 十批任务（56–65）第 6 批。SHA-256 一致、无漂移；完成 PDF pp. 2167–2220（54 页）：16.9 尾段、16.10 RSM、16.11 SAS、16.12 DES、16.13 LES、16.14 模型常数、16.15 ELES、16.16 通用选项 27 小节、16.17 湍流边界条件、16.18 初值、16.19 求解策略、16.20 后处理。**Ch.16 全章完成。**
- 扩充知识页 `Fluent 湍流模型设置`：RSM 两组子模型与墙反射标定范围告警；DES 五底层（Cdes 0.65/0.61、F1/F2/DDES/IDDES、SA 仅破坏项长度尺度替换选项）；LES 五亚格子模型（WALE 默认、动态选项、Near Wall RANS Layer、近壁三处理含 TUI）；ELES 全流程（SA 不兼容、RANS 冻结 vs 混合模型被动模式、rans-les-interface、Vortex Method 涡数 ≥ 面数 1/4、无倒流界面）；通用选项 27 项（浮力 Off/Only Production/Full 三档、曲率 CCURV 与角隅 CCORNER、生成限制器两式默认面、RNG 微分黏度与旋流常数 0.07、湍流阻尼因子 10 仅 sharp 界面、Stress-Omega/BSL 可用项差异、SBES 三混合模型与亚格子选择 WALE 推荐、Update Interval k-omega 最优 5 及四条限制、Prandtl/Schmidt UDF 范围）；湍流 BC（粗糙壁不可用五组合、层流区置零含 SA/RSM、RSM 进口两法）；初值 I 1–10%/TVR 1–100；求解策略（RSM 先 k-ε、EWT-ε 残差为零现象、LES 五步含 init-turb-vel-fluctuations/init-flow-statistics、至少数个驻留时间）；后处理各模型专属变量清单、ELES 双涡黏区分、壁面无统计告警、排错三查（k、黏度比两量级、Re_y）。
- 提取边界：Eq 16.4–16.8 公式体未提取按语义记录；Figures 16.18–16.36 为图形元素。核实补全 WMLES S-Omega 变体名。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.17 Modeling Thermal Energy 段 1（17.1–17.3.5，pp. 2221–2276；批次 62）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 62（Part III / Ch.17 第 1 段：17.1–17.3.6）

- 十批任务（56–65）第 7 批。SHA-256 一致、无漂移；完成 PDF pp. 2221–2276（56 页）：17.2 导热对流全节（含 CHT 专节与 shell conduction、CCS）、17.3 辐射总流程与 17.3.2–17.3.6（非灰 P-1/DTRM/S2S/DO/MC 设置）。
- 新建知识页 `Fluent 热能模拟`：设置五步与温度限；双隔离流体区不用 outflow；能量欠松弛 0.8–1.0 与焓参考温度；CHT——固体时间步须流体整倍数、松耦合两方法（Instantaneous Implicit / Time-Averaged Explicit）与频率基、七条限制、耦合频率匹配热场主频建议、时间平均显式热耦合 Moving Average、各向异性三热流法与 local-neighbors 梯度 2–3 倍提速；custom-heat-flux 导出格式；shell conduction——BC 施加在最远层表面/仅内发射率在 wall surface、13 条限制（仅压力基、端部通量不入热平衡报告、尖折角 GG-Node Based 非物理温度等）、Conduction Manager CSV、shell surface 命名 <wall>-<c0>:<c1> 与 Static/Wall Temperature 读法、勿开 Node Values、CFD-Post 不支持；CCS 三步；辐射六模型与流程（Rosseland 仅压力基、启用辐射自动开能量）；非灰带数最小化与真空波长；DTRM 光线默认 1×4、ray file 改网格必重建且勿压缩；S2S——环境辐射（仅 Convection 热边界计入能量）、FPSC Manual/Automatic 与 Critical Zone、分裂角 20°、Cluster 基限制、Hemicube 三假设（Aliasing/Visibility/Proximity）、Blocking/Nonblocking、参与区自动剔除流程与 300 K 默认、CRF 格式、MPI/OpenMP 线程、GPU Cromwell（无文件 I/O、不支持网格运动、MIS Level 1 聚类）；DO——divisions 默认 2 建议 3–5、像素化 1×1/2×2、非灰带 n·λ 换算（Eq 17.3）、DO/Energy 耦合光学厚度 > 10；MC 目标历程 100,000 与 Target Cells Per Volume Cluster 粗化。
- 提取边界：Eq 17.1–17.3 公式体未提取按语义记录；Figures 17.1–17.28 为图形元素。**笔误自纠**：新页文件名误写"Fulent"，当即 mv 改正。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 17.3.7 Defining Material Properties for Radiation，p. 2277（批次 63 = 17.3.7–17.4，pp. 2277–2340）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 63（Part III / Ch.17 第 2 段：17.3.7–17.4）

- 十批任务（56–65）第 8 批。SHA-256 一致、无漂移；完成 PDF pp. 2277–2340（64 页）：17.3.7 辐射材料、17.3.8 辐射边界条件、17.3.9 辐射求解策略、17.3.10 辐射后处理、17.3.11 Solar Load 太阳辐射模型、17.4 周期传热；触及 17.5 节引言（p. 2340）。
- 扩充知识页 `Fluent 热能模拟`：材料属性（DTRM 只需吸收系数、非灰逐带常数限制、散射系数默认 0 与颗粒告诫）；边界条件（黑体温度与 cooler-outside 告诫、DO/MC transparent BC、半透明墙"向 0 K 辐射"告戒与内部发射率忽略、MC Polar Distribution Expression/Table、多孔跳板吸收/透射 = 面积比估算法、Participates In Radiation）；求解策略（P-1 光学厚度 0.01–10 与小腔增大吸收系数不改变物理、MC Poisson 统计 30% 阈值与温度探针建议、S2S 先解流动须降 Iteration Interval、暂停辐射两法）；后处理（Incident Radiation vs Surface Incident Radiation 区分、辐射热流正号离壁、DTRM 光线数与热平衡、S2S .sif 报告）；Solar Load 全节（Ray Tracing 非参与型、只算贴流体边界、热源指派顺序 shell→solid→fluid、两带光谱、quad-tree 默认 7、scattering fraction 默认 1.0 仅 TUI、ground reflectivity 0.2、Solar Irradiation beam 方向符号相反、Solar Calculator ASHRAE/NREL 与三项全球位置必填、不透明屋顶外部通量被忽略须手动施加、多孔跳板太阳设置、动画三命令）；周期传热（约束六条、缩放温度/σ 理论、顺序法与初始化取体温度壁温均值、periodic-bulk-temperature-ratio、显示温度场不周期）。
- 提取边界：Eq 17.4–17.21 公式体未提取按语义记录；Figures 17.29–17.62 为图形元素。三个数值（DO Beam Width 默认、镀膜玻璃角度阈值、beam width 自动值）符号未提取、已在证据节标注待核。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 17.5 Modeling Heat Exchangers，p. 2341（批次 64 = 17.5–17.6 至章尾，pp. 2341–2392，Ch.17 收官）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 64（Part III / Ch.17 第 3 段：17.5–17.6，Ch.17 全章完成）

- 十批任务（56–65）第 9 批。SHA-256 一致、无漂移；完成 PDF pp. 2341–2392（52 页，p. 2392 为章尾空白页）：17.5 换热器模型、17.6 PCB 热分析。**Ch.17 全章完成。**
- 扩充知识页 `Fluent 热能模拟`：选型决策树与表 17.1（NTU 仅单相/可倒流/可变密度 vs 简效率可两相/不可倒流/不可变密度/须主热容小）；dual cell（重叠网格、网格不一致传热不守恒告诫、五页设置、Raw vs NTU 数据选择依据、多行程质量加权平均串联与顺序要求）；macro（NTU 分段线性主流量-NTU 曲线、简效率两相相变能力、13 条限制含 Hex/Wedge 建议与宏整除要求、平面工具三节点精确贴合 x0→x1 辅助流/x1→x2 行程间、DEFINE_SOURCE 焓 UDF 索引约定、Core Porosity Model 三法与样例文件、Apply 最后点与控制台报错排查、View Passes）；grouped（Primary Flow Direction 三选、Upstream 只能建组时连且改连须删组重建、补充辅助流负流量幅值限制、温度初始化自动传播与覆写、组内 Fixed 选项须一致）；后处理（重叠区绝不同时选主辅区/不选 = 全选告戒、Heat Exchanger Report 四报告、macro 无辅助 cell zone 字段差异、Volume Report 的 Temperature+Heat Exchanger Source）；TUI (report-connectivity)；PCB 模型（SIWave DC IR 功率图、ECAD 材料支持清单、Multizone 只生六面体与非保形界面要求、subst 密度 UDF/比热 1/正交导热 UDF、By Count/By Size、.prof 须列于 board_config.dat 末尾、Thermal Conductivity XYZ 后处理与 User Source、四条限制含 Win/Linux 混合平台不支持）。
- 提取边界：批次 64 段无编号公式（Theory Guide Eqs 6.x 仅定位）；Figures 17.63–17.98 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.18 Modeling Hypersonic Flow 全章，p. 2393（批次 65 = 十批收官）。

## [2026-10-18] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 65（Part III / Ch.18 Modeling Hypersonic Flow 全章，十批收官）

- 十批任务（56–65）第 10 批（收官）。SHA-256 一致、无漂移；完成 PDF pp. 2393–2426（34 页，p. 2426 为章尾空白页）：18.1 引言、18.2 High Speed Numerics、18.3 有限速率化学离解、18.4 Gupta 曲线拟合、18.5 双温度模型、18.6 部分滑移、18.7 温度跳变、18.8 部分催化壁、18.9 壁面烧蚀、18.10 最佳实践。**Ch.18 全章完成；用户指定的十批连续任务（批次 56–65）全部完成。**
- 新建知识页 `Fluent 高超声速流动`：HSN adaptive/expert 0–5 档（0.7/1.4/2.5/4.5 Mach 分档）与 Pressure Discontinuity Sensor；Damkohler 数语义与空气离解温度（2000/4000/9000 K）；11 种预定义混合物（地球 2/5/11 组元、火星金星 5/8/16、土卫六 13/21；含电离组元的选择规则）与默认属性方法矩阵；Gupta 拟合 ≤30,000 K 且仅 air 混合物；双温度模型 13 步设置（需许可；Cp nasa-9/Boltzmann、Blottner、特征振动温度常数/多模态、gupta-mixing-law 碰撞截面、非平衡进口边界、耦合墙定域平衡、vib-ele-energy 残差、11 个后处理变量与 Total Temperature 定义调整）；稀薄气体（Maxwell 滑移、Kn < 0.01/0.01–0.2/> 0.2 三区、Knudsen 计算器、温度跳变自动联动、仅密度基层流、不支持壁厚热生成与 CHT）；部分催化壁（γ 0/1 语义、一般材料常数 vs TPS Kolodziej/Zoby/Scott）；烧蚀（需许可、仅瞬态、Vielle/Surface Reaction、自动动网格设置与 RBF 固体区告诫、先定常后瞬态）；最佳实践（Tmax < 1000/1000–10000/> 10000 K 三档物理选择、求解器七条、FMG 参数与目视检查、监视清单与后处理五查）。
- 提取边界：Eq 18.1–18.13 公式体未提取按语义记录；Figures 18.1–18.25 为图形元素。手册瑕疵：图 18.25 标题误印为 "The Perforated Walls Dialog Box"。
- 更新来源页、Part III 项目页和索引。
- **十批总结**：批次 56–65 合计摄取 495 页（61+43+41+48+42+54+56+64+52+34），Ch.14–Ch.18 五章全部完成；Part III 进度至 p. 2426；新建知识页 4 页（叶轮机械流动、湍流模型设置、热能模拟、高超声速流动）、扩充 2 页（滑移与动网格、物理属性相关页索引）。
- 下一续接位置：Part III / Ch.19 Fluent's Virtual Blade Model，p. 2427（2427–2450）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 66（Part III / Ch.19 Fluent's Virtual Blade Model 全章）

- 十批任务（66–75）第 1 批。SHA-256 一致（c68e1762…372a4）、无漂移；完成 PDF pp. 2427–2450（24 页，p. 2450 为空白版权页）：19.1–19.9 全部。**Ch.19 全章完成。**
- 新建知识页 `Fluent 虚拟叶片模型（VBM）`：两类致动盘方法（pressure-disk 双面边界质量显式守恒 vs Zori 动量源单层盘质量自动守恒）、BET 翼型堆叠与 2π/N 几何平均、推力/力矩系数 C_NA-EU=1 与湍流建议 k−ε/k−ω（p. 2430 渲染核对）、EDM/FDM 两模式与网格指南（EDM 单层棱柱 1/40–1/100 盘径、FDM 四步创建 srf-fdisk-RotorName、悬停远场非零质量流超定告诫）、pitch/bank 旋转顺序（先绕 Y 后绕 x′，不可交换）、桨距/挥舞分解、NR 配平（±a 扰动 Secant 法数值 Jacobian、Damping Factor 默认 0.1 推荐 0.7、update frequency）、Quadratic（96% 默认）/Modified Prandtl 尖部损失、翼型 .dat 格式（≤30 表/250 点/±180° 全迎角）、28 步 GUI 配置、15 场变量（cell-based）与 Rotor_xx_Loads.csv 七类输出；启用限制（仅 3D 并行、不支持多相）。
- 提取边界：Eq 19.1 起公式体未提取按周边文字记录；Figures 19.1–19.6 为图形元素；Table 19.1–19.3 完整提取。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.20 Modelling with Finite-Rate Chemistry 第 1 段（20.1 前半），p. 2451。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 67（Part III / Ch.20 第 1 段：20.1 引言至 20.1.1.9 前半）

- 十批任务（66–75）第 2 批。完成 PDF pp. 2451–2495（45 页）：章引言、20.1.1.1–20.1.1.9 前半。
- 新建知识页 `Fluent 组分输运与有限速率化学`：组分上限（700 全模型 / 50 密度基·Eulerian PDF·熔凝·Crevice·热扩散·表面/位点组分）与 CFD-Post 多相质量分数 Note；混合物材料五要素与副本语义 Warning（改组分属性不传播到已建混合物）；TCI 四选项（No TCI 的 Flow Iterations/Aggressiveness 0.5/Temperature Threshold 200 K、EDC 标准/PSR 与 Constant/Dynamic Cmix）；Chemistry Solver 三选（Relax to Chemical Equilibrium 需热力学库 therm_NASA9.dat、Stiff/CHEMKIN-CFD 的 GPU 与并行分区注记、None-Direct Source 仅密度基推荐）；加速方法 DMR/CA/ISAT/DCC 适用矩阵；Thickened Flame（效率函数 none/Colin/Charlette、8 网格点、Integral Length Scale 1/4–1/2、火焰速度 metghalchi-keck-law、仅非稳态层流或 LES/DES/SAS/SBES/SDES）；CHEMKIN 导入（加密机理六限制、末位 bulk 组分规则、END 关键字、输运数据导入属性方法表、内置四机理）；Species 对话框顺序规则（末位 = bulk 不解方程、增删重置全部组分设置、化学式不可改）；Reactions 对话框（全局正向 vs 可逆、Arrhenius 英制仍输 SI、第三体、压力依赖 lindemann/troe/sri 与 CAB 反应、覆盖度依赖、Include Backward Reaction 锁产物指数、Mixing Rate A=4.0/B=0.5）；等效燃料 C4.17H6O2.75 与生成热符号约定；Zone 级机理与 Site Density 1e-8–1e-6、瞬态覆盖度和须为 1；Table 20.1 修正 Cp 系数（CO₂/H₂O/O₂，渲染核对）；Coal Calculator 三煤流（ proximate/ultimate、一/两步机理、CO/CO2 Split、HTVY、char N、OK 后自动建材料启用 DPM 但不启用 Fuel NOx）；组分 BC（末位组分 = 1−和、NRBC 不兼容、进口扩散默认关）；求解流程（两步冷流、密度欠松弛 0.5–1/真实气体 0.1、点火 patch 无影响于终态、刚性化学 Δt=1/10 最小对流/扩散时间尺度、密度基 Temp Positivity 0.2/Time Step Reduction 0.25、EDC 先平衡后切换）；后处理变量（Enthalpy 仅压力基、Source Term 仅密度基、TFM Thickening Factor）。
- 提取边界：Eq 20.1–20.8 公式体未提取按周边文字记录；Table 20.1 列标题（CO₂/H₂O/O₂）经 fitz 渲染视觉核对；等效燃料分子式按分子量式反推小数点；Figures 20.1–20.16 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 p. 2496（20.1.1.9 收尾），批次 68 = pp. 2496–2541。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 68（Part III / Ch.20 第 2 段：20.1.1.9 收尾至 20.1.7）

- 十批任务（66–75）第 3 批。完成 PDF pp. 2496–2541（46 页）：20.1.1.9 收尾、20.1.2–20.1.7 全部。
- 扩充知识页 `Fluent 组分输运与有限速率化学`：后处理变量补全（TFM Omega/火焰速度厚度、Cell Time Scale 与 Fine Scale 系列限 EDC+刚性层流、Kinetic/Turbulent Rate of Reaction-n、净速率须至少一迭代）；壁面表面反应与 CVD（表面物种与气相异体、表面 CHEMKIN 须伴气相文件、粘附系数 Stiff 下转 Arrhenius 而 CHEMKIN-CFD 全兼容、None-Explicit/F-R-E-D 五类气相+五类表面反应白名单、Heat of Surface Reactions/Mass Deposition Source（密度基恒开）/Diffusion Energy Source（密度基不可关）、Low-Pressure Boundary Slip 下 Shear 显示重置、表面位点初值助收敛）；颗粒反应（仅配 species transport、禁 breakup/collision/coalescence、Diffusion-Limited/Catalyst Species、multiple-surface-reactions 须先在 Combustion Model 选、颗粒表面物种分数和为 1、禁与 custom laws 同用；多组分颗粒 mixture+particle-mixture 两材料、两预定义对、Solid/Condensed 清单固态处理无黏度表面张力（urea 三液体 TUI 例外）、五反应模型 kinetics/diffusion·surface·volume·phase-change·thermolysis（thermolysis 不适用 wall-film）、DEFINE_PR_RATE、蒸发完才开始反应）；电化学反应（多孔双电位 vs 壁面单电位不混用、密度基不可用、Charge Number 必设/e- 可忽略、电导率设混合物、Butler-Volmer/Tafel 参数全可函数化、参考摩尔浓度默认 1 kmol/m³、DEFINE_EC_KINETICS_PARAMETER/DEFINE_EC_RATE、多孔 zone 触发双电位与 Electrolyte Conductivity、双面墙单侧设置自动复制、Faradaic Interface Current 欠松弛、后处理变量全集、双电位 zone 自动检测三依据与燃料电池分区示例、Water Corrosion Pre Tool 全流程与 Tafel 参数数值）；无反应组分输运（Mean Molecular Weight 等后处理）；Reacting Channel（稳态 3D 专属、禁 shell conduction、中心线一维与扫掠结构化网格建议、边界组/Flow Iterations Per Coupling/欠松弛 Eq 7.150、进口流向判定通道进出口、U 形管 reacting-channel-model-options TUI、通道壁零热通量禁改、8 类通道变量 Plot/Report）；Reactor Network（快化学 CFD→聚合反应器解详细机理、仅稳态或统计定常 LES、默认 50 反应器、Solve Temperature、Use Current Reactor Network、LES 用 Data Sampling+Use Time Averaged Fields、Expert Options（ODE 容差 1e-05/1e-12、收敛容差 1e-08、segregated 快但停滞改 coupled、组成变量默认混合分数或 N2/H2O+温度、可换至多四个自定义场函数））。
- 提取边界：Eq 20.9–20.12 公式体未提取按周边文字与数值照录；CO2 环境四个均相反应方程体未提取；Figures 20.17–20.35 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 20.2 Composition PDF Transport，p. 2542（批次 69 = 20.2 + 20.3 至章尾 p. 2570，Ch.20 收官）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 69（Part III / Ch.20 第 3 段：20.2–20.3，Ch.20 全章完成）

- 十批任务（66–75）第 4 批。完成 PDF pp. 2542–2570（29 页，p. 2570 空白）：20.1.7.3 收尾、20.2、20.3。**Ch.20 全章（pp. 2451–2570）完成。**
- 扩充知识页 `Fluent 组分输运与有限速率化学`：Composition PDF Transport（仅压力基；Lagrangian 更准更慢/Eulerian；九步流程与"从 Laminar FR/EDC/非预混/部分预混既有解出发"Important；Lagrangian 默认刚性+ISAT、Modified Curl/IEM/EMST、Liquid Micro-Mixing 锁 Mixing Constant、Particles Per Cell、Local Time Stepping 三数；Eulerian 仅 IEM、气相常数 2、Include Temperature Fluctuations 多模态能量、Stiff 默认关；进口/回流混合分数、壁面零通量、Equilibrate Inlet Stream 禁纯燃料/氧化剂、初始化变量混合分数+温度；稳态 Run Calculation 迭代平均 50/Increment 0.2、残差判据须调低、Flux Reports 热平衡核对；非稳态分数步长增粒子数；可压缩压力做功式；CHT 固体有限体积；后处理瞬时值非物理用 Mean/RMSE、粒子轨迹 Skip；Eulerian 逐模态变量）；化学加速六方法（ISAT——除 None-Direct Source 外全求解器、禁表面反应、容差 0.001 渐进减小准则、Max Storage 100 MB、Verbosity 1/2 文件族、清表三法含 clear-isat-table TUI、预混火焰表现好/长驻留退化、表读写不建议+并行节点 ID 规则；DMR——DRG 算法每单元每步约减、平均提速 ≥2 倍、容差 0.01、目标物种 h 起步 3 个、Expert TUI 全流程、DRG Reduced 零值=ISAT 查表且不落盘、渐进容差重启策略、大面积低活性区才有效、负载平衡 ISAT vs Stiff Chemistry 选法；CA 0.02/10 K 不必更低；DR——超 700 物种机理专用、代表物种 >10 且 <700−未代表元素数默认 12、reduced-dimension-mixture 禁改名、全机理物种后处理类别、仅配 ISAT；DCC——CHEMKIN-CFD 专属五参数默认；DAC——CHEMKIN-CFD 专属、与 ISAT 不兼容、容差 0.001、目标物种默认 co+ho2 须补燃料物种）。
- 提取边界：Eq 20.13 与可压缩粒子内能式公式体未提取按周边文字记录；Figures 20.36–20.44 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.21 Modelling of Turbulent Combustion With Reduced Order，p. 2571（批次 70 = 21.1 前半，pp. 2571–2625）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 70（Part III / Ch.21 第 1 段：21.1 引言至 21.1.9）

- 十批任务（66–75）第 5 批。完成 PDF pp. 2571–2625（55 页）：21.1.1–21.1.9。
- 新建知识页 `Fluent 缩阶湍流燃烧模型`：非预混模型使用步骤与四化学描述；平衡化学（绝热二维/非绝热三维查表差异、Compressibility Effects、二次流七情形与运行时 PDF 积分开销、经验燃料两 Important、RFL≈2× 化学计量分数与富燃非平衡依据）；火焰let三模式（机理 ≤700 组分、非稳态火焰let五输入 + Initialize Unsteady Flamelet Probability 两告诫、Max Scalar Dissipation 30/s、柴油机非稳态三前提、多 flamelet 起始时间、Burnt Initial Flamelet、Flamelet Fluid Zones 选缸内、IC 发动机 ≥2 flamelet/split ≥3/多循环重置、Reset 概率加权重建 vs Inert EGR Reset）；流股组成（边界组分默认清单、温度与蒸发/脱挥约定、凝聚相密度规则、经验原子分数、液体燃料蒸发物种、煤三方案与单/双混合分数两法、Burnout Ratio 2.67/Latent Heat 规则、Coal Calculator 非预混版）；控制参数（NOx 排除与 TUI 强制纳入、火焰let Fourier 数控制、慢化学默认置零 17 物种+H2(l)+C(s)）；火焰let计算与后处理（标量耗散乘子/步进、AGR、Flamelet 2D/3D 对话框）；PDF 查表（表参数全集、Max Species 200、单/双混合分数运行时差异 Important、全制表 4D/5D、经验燃料富燃失败热值补偿、PDF Table 对话框与缩放方差 0–0.25）；标准 flamelet 文件关键字表与缺失物种规则；Inert 模型（H/C 比、Inert Stream 边界、patch 重算焓、Heywood 反应式族、Inert EGR Reset 化学计量惰性化、G-Equation 负值）。
- 提取边界：Eq 21.1–21.10 公式体未提取按周边文字记录；AGR 网格点默认值缺失；Figures 21.1–21.29 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 21.1.10，p. 2626（批次 71 = 21.1.10–21.2，pp. 2626–2642）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 71（Part III / Ch.21 第 2 段：21.1.10–21.1.14 + 21.2）

- 十批任务（66–75）第 6 批。完成 PDF pp. 2626–2642（17 页）：21.1.9.3 尾注、21.1.10–21.1.14、21.2 全节。
- 扩充知识页 `Fluent 缩阶湍流燃烧模型`：非预混边界条件（混合分数进口 0/1 约定与方差取 0、烟气再循环例外、Inlet Diffusion 默认关、进口温度须与 Chemistry 页一致否则表外插值）；pdf-mixture 材料（组分不可改、只设输运性质且不可组分函数、WSGGM 可用、真实气体配 Compressibility Effects）；求解策略（prePDF 2 不支持/PrePDF 3+ 兼容、PDF 文件名存 case 自动找回但全路径才保险、初始化混合分数 0 值、fmean/fvar/psec/pvar、PDF 方程欠松弛 1 与 0.9、密度欠松弛 0.5–1/真实气体 0.1、双混合分数 Compressibility Effects 仅非绝热）；Robust Numerics（pdf_stability_marker 标记焓低于表最小值的单元、pmn 每 5 迭代/2 时间步、默认停用需 TUI 激活、Preferences 永久化）；后处理（Pdf/Species/Temperature/Unsteady Flamelet 四类变量、非稳态火焰let仅前 50 物种、绝热模拟温度焓也来自查表、Inert 八变量）；预混燃烧（五限制、湍流模型先选且非 Spalart-Allmaras、绝热 Adiabatic Burnt Temperature/非绝热 Heat of Combustion + Unburnt Fuel Mass Fraction、Zimont 五常数/Peters 仅 TUI + Ewald Corrector、G 方程方差 RANS 输运 LES 代数、曲率源项默认排除、Turbulent Schmidt 兼作 Energy Prandtl、premixed-combustion 密度与 Adiabatic Unburnt Density/Temperature、Critical Rate of Strain 默认极高贫预混典型 3000–8000、c=0/1 边界与 patch 初始化、后处理变量分类与 G 方程附加量、组分浓度自定义场函数）。
- 提取边界：批次段无新编号公式；21.2.4.1 场函数公式体未提取按语义记录；Figures 21.30–21.35 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 21.3 Modeling Partially Premixed Combustion，p. 2643（批次 72 = 21.3 至章尾 p. 2670，Ch.21 收官）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 72（Part III / Ch.21 第 3 段：21.3，Ch.21 全章完成）

- 十批任务（66–75）第 7 批。完成 PDF pp. 2643–2670（28 页，p. 2670 空白）：21.3 全节。**Ch.21 全章（pp. 2571–2670）完成。**
- 扩充知识页 `Fluent 缩阶湍流燃烧模型`：部分预混限制（FGM 仅 c-Equation）；设置 11 步（C/G 方程 State Relation 选择矩阵、预混进口两设法——预混物种组成+c=1/f=0 优于纯燃料+当量比、prepdf-polynomial 超范围告诫、Recalculate Properties）；FGM 全节（进度变量自定义对话框、预混火焰let参数与标量耗散 1000/s 默认、AGR 两套默认 64/0.5/0.5 与 12/250/0.5/0.1、网格分布编辑、扩散 FGM 无 Maximum Flamelets/步长≈熄灭应变率 1/20/熄灭火焰let建模流形、Include Equilibrium Flamelet、非绝热热损失焓级数与 Fully Premixed FGM）；查表（表参数、Use Flamelet Distribution、FGM Scalar Transport 表前选标量与稳态后处理模式、4D/5D 表后处理与 Enthalpy Slice 绝热级语义）；FGM 标准文件（PREMIX_CHI/REACTION_PROGRESS/PREMIX_YCDOT；样例另现 PREMIX_STOICH_SCADIS 照录）；Premix 页（SBES RANS 两常数、TCI 两法、方差 transport/algebraic/hybrid 推荐矩阵、Algebraic Variance Constant）；未燃属性多项式（prepdf 拟合范围六燃料/贫限–1/298–800 K/1–40 bar、Piecewise Linear 20 点限外恒值、二次混合分数列、Non-Adiabatic Laminar Flame Speed）；拉伸层流火焰速度（需输运数据、热损失点 0.05 增量）；内燃机多循环（G-Equation 唯 Inert+EGR Reset 一途）；GPU 求解器边界量报 0 三限制。
- 提取边界：批次段无新编号公式；SBES hybrid 方差分区符号未提取；Figures 21.36–21.51 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.22 Modeling Engine Ignition 全章，p. 2671（2671–2684，批次 73）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 73（Part III / Ch.22 Modeling Engine Ignition 全章）

- 十批任务（66–75）第 8 批。完成 PDF pp. 2671–2684（14 页，p. 2684 空白）：22.1–22.3 全部。**Ch.22 全章完成。**
- 新建知识页 `Fluent 发动机点火模型`：火花模型（载体模型、16 火花上限、kernel 参数、In-Cylinder 起始角按曲轴角/时长仍秒且 Eq 14.30 循环联动、Energy 默认 0 非点燃所需、R14.5 回退与 spark-model TUI）；自燃模型（Knock=SI/Ignition Delay=柴油机、Species Transport/Premixed/Partially Premixed 兼容矩阵、Hardenburg+十六烷值四参数、Generalized 八参数、Douaud 五参数）；缝隙模型（纯 TUI：crevice-model?/crevice-model-controls 全参数（默认值照录）、泄漏壁+共享边界线程、逐环七几何参数与 n+2 初始压力、单环复制多环法、crevice-summary、Crevice Model Sources 0.8、质量流失∝压差/峰值压力比例下降、crev.out 每时间步格式、Gnuplot/Excel 读回与 Fluent 拆列三行头法）。
- 提取边界：本章无编号公式（Theory Guide Eq 10.8/10.9 与 Eq 14.30 引用未展开）；Figures 22.1–22.10 为图形元素；TUI 交互样例照录。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.23 Modeling Pollutant Formation 全章，p. 2685（2685–2724，批次 74）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 74（Part III / Ch.23 Modeling Pollutant Formation 全章）

- 十批任务（66–75）第 9 批。完成 PDF pp. 2685–2724（40 页）：23.1–23.3 全部。**Ch.23 全章完成。**
- 新建知识页 `Fluent 污染物生成模型`：NOx（解耦后处理八步与预混不兼容、SNCR 需 NH3/尿素先行、四路径、非预混 Fuel NOx 需 DPM、三燃料流与 N 源、Conversion Fraction 默认 1 语义与 Partition Fractions、Char N Conversion 四选 + BET 面积、N2O quasi-steady 残差恒零、Reburn 两法与等效燃料 C/H 比选法、SNCR 气/液喷射与尿素升华/两分解模型、Reagent Fraction 与 nox-chemistry TUI、PDF Mode 三选与跨污染物一致性、PDF Points 10→20–25 渐进、Tmax 四选项、求解 DPM Interval 0/欠松弛 1.0/残差 1e-6、后处理变量全集）；Soot（大分数或辐射须随主解、四模型不兼容预混、一步/两步仅湍流、Soot-Radiation Interaction 下不可后处理、一步丙烷默认、两步 Tesner 仅配 eddy-dissipation、MB-Hall 前提 C2H2/C6H6/C6H5/H2、user-correlation 分段多项式默认仅甲烷 290 K 有效/三段八系数/低到高排序、Fenimore-Jones vs Lee extended、氧化缩放参数恒 1 与 soot-parameters TUI、UDF 两钩子、MoM 矩数 3–6/粘附系数/聚集模型临界直径+分形维 1.7–2.0+高估告诫/HACA 位点密度 cm² 单位/归一化矩、后处理变量全集）；DDC（稳态流场+详细机理后处理、Original vs Pollutant Species 互斥、pollutant-mixture+Stiff Solver、非污染物平衡计算、ISAT 1e-5+大内存）。
- 提取边界：Eq 23.1–23.9 公式体未提取按周边文字记录；两步模型 3.5e8 参数名缺失；Figures 23.1–23.14 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.24 Predicting Aerodynamically Generated Noise 全章，p. 2725（2725–2770，批次 75 收官）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 75（Part III / Ch.24 Predicting Aerodynamically Generated Noise 全章，十批收官）

- 十批任务（66–75）第 10 批（收官）。完成 PDF pp. 2725–2770（46 页，p. 2770 空白）：24.1–24.5 全部。**Ch.24 全章完成；用户指定的十批连续任务（批次 66–75）全部完成。**
- 新建知识页 `Fluent 气动噪声模型`：三方法概览（直接法远场不可行/近场伪声、FW-H 中远场自由空间限制、波动方程低 Mach 常密度、宽带源仅诊断不预测接收点）；FW-H（稳态单 MRF 用法、forward-time projection、模型常数与 2D Source Correlation Length、on-the-fly、ASD/CGNS 导出——SYSNOISE 体积源与柱坐标 TUI、Simcenter 3D 文件族与旋转壁一致性限制、源面规则——多面禁包围/内部面 cell zone 指定/渗透面禁与内壁同选、保存参数与磁盘预估、移动接收器发射时刻语义、显式求解器自适应采样、信号读写流程与 on-the-fly 缓冲冲掉告诫、auto-pruning、Surface dpdt RMS、Acoustic Sources FFT 四页——Clip Time/Hanning/存储区 Overwrite 两模式/点探针 .dat 导出/倍频程与 1/3 倍频程与 20 恒定带宽与 20 单频变量/SPL=Surface Pressure Level/面平均 .xy 与柱状图/CGNS 频谱导出 links 与 Mechanical FLUREAD/相对路径与 Windows 网络盘告诫、GPU .asdg 与四限制——无 on-the-fly/分区冻结/不支持稳态旋转转子/FFT 须同分区）；波动方程模型（低 Mach scale-resolving、常密度声速限制、仅瞬态二阶隐式、非轴对称、源掩模 UDF 与 Region 基本形状（register 用后改删不影响）、子迭代控制与 AMG 0.1、声学独立初始化与 Sound Potential 0/ramping 步数/DEFINE_ON_DEMAND、七个后处理场与 retain-temporary-solver-mem 高级源场、Kirchhoff——单积分面/共享接收器/.ark/恒自动修剪/仅 on-the-fly/与 FW-H 同仿真五步流程）；宽带噪声源（Proudman/射流/边界层/LEE/Lilley、Realizations 200/Fourier Modes 50、后处理变量全集含轴对称 Jet 系列与 3D Z 系列限定）；密度基海绵层（压力基单相可压瞬态、不支持多相、远场密度二次混合、ramping 80–100% 厚度、厚度 ≥2 波长、重叠层归最远内边界、Sponge Layer Distance/Blending Function 两场）。
- 提取边界：Eqs 24.1–24.4 公式体未提取按语义记录；Reference Acoustic Pressure/Power 默认数值与 Table 24.1 表体缺失（参考压 2e-5 Pa 经 24.2.6 节交叉确认）；Figures 24.1–24.24 为图形元素。
- 更新来源页、Part III 项目页和索引。
- **十批总结**：批次 66–75 合计摄取 346 页（24+45+46+29+55+17+28+14+40+46），Ch.19–Ch.24 六章全部完成；Part III 进度至 p. 2770；新建知识页 6 页（虚拟叶片模型 VBM、组分输运与有限速率化学、缩阶湍流燃烧模型、发动机点火模型、污染物生成模型、气动噪声模型）。
- 下一续接位置：Part III / Ch.25 Modeling Discrete Phase，p. 2771（2771–3004）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 76（Part III / Ch.25 第 1 段：25.1–25.2）

- 新十批任务（76–85）第 1 批。SHA-256 一致（c68e1762…372a4）、无漂移；完成 PDF pp. 2771–2818（48 页）：25.1–25.2。
- 新建知识页 `Fluent 离散相模型（DPM）`：三概念（Coupled/Uncoupled、Steady/Unsteady Tracking、parcel——DEM 中 parcel 体积由代表质量定而轨迹用 particle 直径）与六类限制（体积分数 <10–12% 质量载荷不限、Knudsen 连续区 + 10 nm 最小粒径、连续悬浮需非稳态、颗粒旋转五限、与其他模型联用清单、Hybrid 并行静默回退与 Use DPM Domain 失效）；12 步流程；DPM Iteration Interval 与 Update DPM Sources Every Flow Iteration（非稳态默认）；稳/瞬态颗粒处理（曲轴角注入、Clear Particles、四种 parcel 释放方法——雾化器/file/UDF 初始化强制 standard、constant-number 推荐于喷雾、2D/3D parcel 几何 APF 2/3）；追踪时机（瞬态每步首必追踪、间隔 0 = 步末推进、碰撞模型禁设间隔）；Max Steps 50000/500、Length Scale/Step Length Factor（默认 5）与稳态经验法则；高分辨率追踪（subtet + 重心插值、多相属性插值自动开、梯度插值与瞬态插值不兼容）及高分辨率/重心插值/颗粒重定位三组 TUI 全录；物理模型 14 项（Particle Radiation 限 P-1/DO、热泳、Saffman、虚拟质量+压力梯度、侵蚀与 Accumulate、蒸发绝对压力默认、Pressure Dependent Boiling 切换条件 p_sat≥P 与超临界处理、温度相关潜热、Two-Way Turbulence Coupling 六模型适用清单、随机碰撞/Coalescence、DEM 设置全流程（四种法向力律 + 两种摩擦律、碰撞伙伴、限制六条、数值推荐三项）、体积位移 0.95 限制单相均质多相与密度基禁用）；UDF 七钩子；数值（implicit/trapezoidal/analytic/RK + Automated 高低阶（须 Accuracy Control）、耦合热质限因子 0.3/0.1、参考系、节点平均四核、源项线性化与三 UDF 不兼容、动态交互范围八叉树 30 层三限制、空间/时间错列与随机数重置、Packing Limit Enhanced Numerics 开头）。
- 提取边界：Eq 25.1–25.5 与 2D/3D parcel 几何公式体未提取按语义记录；Max Steps 上限截断按 1e5 记录待核；Figures 25.1–25.12 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 p. 2819（25.2.7.8 收尾），批次 77 = 25.3（2819–2881）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 77（Part III / Ch.25 第 2 段：25.3）

- 十批任务（76–85）第 2 批。完成 PDF pp. 2819–2881（63 页）：25.3 全节。
- 扩充知识页 `Fluent 离散相模型（DPM）`：25.2.7.8/25.2.7.9 收尾（Enhanced Numerics、film height 欠松弛 0.5–0.9 与重心插值互斥）；12 种注入类型与选择指引；5 种颗粒类型激活 Law 表（massless/inert/droplet/combusting/multicomponent 及密度方法前置）；单/组/锥/面/体注入点属性全参数（group 线性插值与单属性区间告诫；锥注入四类几何、hollow 弥散角与旋流分数、扇区方位角参考向量、瞬态每步重算 vs 稳态一次初始化；面注入比例流量/随机起点互斥/法向注入/壁膜颗粒注入限制；体注入三种投放口径与 DDPM 自动起点数及 Packing Limit 0.63）；五种雾化器全参数；file 注入三格式与一致性检查列/flow-time 升序/Start Flow-time/Repeat Interval；condensate；RR/对数 RR/随机 RR/表格分布（样条插值选项）；injection 管理；22 步属性定义（蒸发/氧化/产物物种、GPU+非绝热 FGM 限前 15 组分、多组分 Components 页与近零蒸气压非挥发液体技巧、Wet Combustion、Multiple Reactions）；injection 级物理模型（八种拖曳律、六种换热系数、旋转两 law 组、粗糙壁三参数、布朗运动前置、六种破碎模型全参数与 Rayleigh 生长开关）；DRW 湍流扩散（Tries 非稳态锁 1、C0 0.15/RSM 0.3）；自定义 Laws 与 Switching；批量修改 Modify 勾选语义；瞬态 .ttab profile。
- 提取边界：Eq 25.7–25.12 公式体未提取按语义记录；TAB y0 默认值缺失；Figures 25.13–25.38 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 25.4，p. 2882（批次 78 = 25.4–25.6，2882–2914）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 78（Part III / Ch.25 第 3 段：25.4–25.6）

- 十批任务（76–85）第 3 批。完成 PDF pp. 2882–2914（33 页）：25.4–25.6。
- 扩充知识页 `Fluent 离散相模型（DPM）`：八种 DPM 边界条件（reflect 旋转 Tsuji/trap 蒸发全释放/escape/wall-jet 适用域/wall-film/interior 限内部 zone/reinject 全流程与时间延迟/user-defined）；默认 BC 矩阵（壁/对称/轴 reflect、流边界 escape、内部 interior）与恢复系数仅壁面可改、按撞击角函数化；摩擦系数 0.2 与分段默认点；颗粒-壁撞击换热（wall-film 下直接颗粒-壁、飞溅不适用、燃烧须 Wet Combustion）；侵蚀/沉积六模型全参数（Generic 三函数/Finnie/McLaury/Oka/DNV/Shear Stress + Granular Phase Shielding、默认全启用、Oka 实验调校告诫）；25.5 侵蚀耦合动网格（准稳态 Eq 25.13、前置八步、三限制、Reference Erosion Model 五选 + UDF、壁材密度 2719 默认、Automatic Dynamic Mesh Setup 与 erosion UDF 动区、变步长 10% 节点移动、Total Time of Erosion、Solve DPM during Flow Simulation、自动存盘图形、Accumulated Deformation）；25.6 LWF（九条限制、撞击/飞溅三模型与 Regime Parameters、飞溅数 0 关闭、剥离单材料限制、分离三模型、膜-壁换热导热默认/对流模型/偏移/旧 case 告诫、caloric 温度、壁温限幅与 Leidenfrost、膜冷凝触发与五步设置、气侧边界层默认与热解覆盖、原位数据约简 N³×M³×K 与跨 injection 合并、液膜初始化参数）。
- 提取边界：Eq 25.13 公式体未提取按语义记录；Figures 25.39–25.55 为图形元素。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 25.7，p. 2915（批次 79 = 25.7–25.8，2915–2937）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 79（Part III / Ch.25 第 4 段：25.7–25.8）

- 十批任务（76–85）第 4 批。完成 PDF pp. 2915–2937（23 页）：25.7–25.8（另含 25.6.6 尾注）。
- 扩充知识页 `Fluent 离散相模型（DPM）`：材料属性汇总表（五张表逐类型×属性×方程）；离散相材料四类与"先建注入才有材料类型"规则、particle-mixture 组分；属性逐项（Binary Diffusivity film-averaged/unity-Lewis 与压力依赖、多组分沸点=分压和达总压、Combustion Model 三选、Cp/Density 的 char 组分相关选项与非预混语义、脱挥发四模型与最低挥发分 0.01、热解热符号约定、潜热常数取沸点值、反应热固相分配默认 0、饱和蒸气压限幅与 RGP、膨胀系数 1、温度平均系数 1/3 与蒸发物种属性前置、Thermolysis 四模型与 SCR 尿素建议、talbot 热泳默认、蒸发温度建模决策语义、汽-粒平衡三选、蒸发/沸腾两模型与变 Lewis/传热平均 TUI、挥发分不互溶假定、发射率 1.0/0.5 散射 0.9 与连续相散射忽略）；液膜初始化尾注（Reset/Initialize LWF）；求解策略（非耦合两步/耦合五步、全部 injections 强制、interval 0 语义、solve/dpm-update、随机追踪系综收敛、源欠松弛 0.5/0.9 与 200 迭代示例、线性爬升 TUI、Reset DPM Sources、随机轨迹 12 场景与按颗粒种子分区无关、re-randomize 两开关组合矩阵）。
- 提取边界：Eq 25.14 公式体未提取按语义记录；Figures 25.56–25.59 为图形元素。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 25.9，p. 2938（批次 80 = 25.9 前半，2938–2972）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 80（Part III / Ch.25 第 5 段：25.9 前半）

- 十批任务（76–85）第 5 批。完成 PDF pp. 2938–2972（35 页）：25.9.1–25.9.7。
- 扩充知识页 `Fluent 离散相模型（DPM）`：轨迹显示全流程（单流追踪/非稳态语义/Pulse 动画与视频保存/同种子同轨迹/显示性能告诫）；轨迹十种风格与矢量三风格全参数（sphere Detail 4–50、ribbon Twist By、refined-sphere 性能语义）；Coarsen/Skip 粗化；追踪统计 parcel 计数语义与 tracking-statistics TUI；汇总报告（稳态不存 .dat、Fates 表、Mass/Energy Summary、耦合稳态热平衡校核 Important、命运全集含非稳态五追加、incomplete_parallel 分区交换限、再注入 Reinject/Inserted 配平语义与 BC-UDF 命运、蒸发质量 Film/Freestream 分解两 TUI）；逐步报告（仅稳态、Reporting Variables 与 Add Color by）；非稳态当前位置（Sample File Format 跨仿真迁移）；相间交换项 13 变量清单（仅耦合更新）；颗粒变量六表全录（Law Index 1–7、Tracking Scheme 0–3、Number in Parcel 稳/非稳态双语义、Spalding Bt/Bm 数、DEM 力不存 .dat、Breakup Type 0–7 与各破碎模型专属变量）。
- 提取边界：Eqs 25.15–25.22 公式体未提取按语义记录；Figures 25.60–25.66 为图形元素；Tables 25.7–25.12 提取照录。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 p. 2973（批次 81 = 25.9 后半 + 25.10，2973–3004，Ch.25 收官）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 81（Part III / Ch.25 第 6 段：25.9 后半 + 25.10，Ch.25 全章完成）

- 十批任务（76–85）第 6 批。完成 PDF pp. 2973–3004（32 页）：25.9.8–25.9.15、25.10。**Ch.25 全章（pp. 2771–3004）完成。**
- 扩充知识页 `Fluent 离散相模型（DPM）`：DPM 变量三档清单（自动侵蚀六种/均值/RMS、Eq 25.23–25.24 驻留时间加权、节点平均失效告诫）；非稳态统计（Data Sampling + DPM Variables、变量清单、与瞬时均值差异）；轨迹采样（Sort Sample Files、网格界面三文件、Append、DEFINE_DPM_OUTPUT）；直方图（权重选择、Correlation 与 (Variable)^3 质量曲线技巧、Cumulative Curve）；数据约简（全变量分箱、No. of Bins=1 忽略、Create Steady from Unsteady）；面采样云图（Plotting Grid Interval Size 大于网格原则、九命名表达式、与 DPM 变量类加权差异、限本面）；颗粒汇总（D10–D43 应用表、RR 拟合误差）；侵蚀后处理（Accumulate 平均、换 injection 丢弃、面量限制、25R2 前 data 丢弃）；SCR 沉积风险两法（Level-based 四风险等级与参数 TUI 全套及免重跑调参；Weighting-based 0–1 归一与四权重因子、自动报告定义与场函数、后处理变量清单）；并行三模式（Shared Memory 仅 Linux/Windows 串行/host 内存、多相联用禁 Shared Memory、Workpile 与 wall film 互斥、文件系统同路径要求与 transcript 变通、dpm-load-balancing 与 hybrid-2domain TUI、颗粒步数加权）。
- 提取边界：Eqs 25.23–25.35 公式体未提取按语义记录；Figures 25.67–25.78 为图形元素；Tables 25.13–25.14 提取照录。
- 更新来源页、Part III 项目页和索引。
- **十批进度**：批次 76–81 完成 6/10（Ch.25 全章收官，234 页）；余批次 82（Ch.26）、83–85（Ch.27 前三段）。
- 下一续接位置：Part III / Ch.26 Modeling Macroscopic Particles 全章，p. 3005（3005–3026）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 82（Part III / Ch.26 Modeling Macroscopic Particles 全章）

- 十批任务（76–85）第 7 批。完成 PDF pp. 3005–3026（22 页，p. 3026 空白）：26.1–26.4 全部。**Ch.26 全章完成。**
- 新建知识页 `Fluent 宏观颗粒模型（MPM）`：add-on UDF 套件定位与适用域（20–30 单元解析、Re<<1、密度比≈1、非通用模型）；七条限制（无传质辐射、禁动网格、单碰撞事件、无 DPM 碰撞、多相源项手动、无子迭代、禁网格界面）；加载两法（ribbon 或 addon-module 号 10、仅 3D、默认启用）；设置 11 步（除 cemented 外瞬态）；七页设置（Tracking——颗粒不跨单元；Drag 四律 MDR/MA/Cd/Size-Based 与 drag factor/弛豫时间 1/4 子步、多相 Drag Based On；Collision 恢复系数/摩擦/滚动摩擦/Substeps；Deposition detachment 力与速度阈、颗粒间团聚；Injections 四类型与 Cemented/连续注入/移动旋转注入点；Attraction n1–n5/G；Initialize MPM——PRESTO! 自动切换、mpm1/mpm3 命令、Display Particles 着色）。
- 提取边界：MDR/MA/弛豫时间与 Eqs 13.6–13.10 公式体未提取按语义记录；Figures 26.1–26.7 为图形元素。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：Part III / Ch.27 Modeling Multiphase Flows，p. 3027（批次 83 = 27.1–27.2，3027–3089）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 83（Part III / Ch.27 第 1 段：27.1–27.2）

- 十批任务（76–85）第 8 批。完成 PDF pp. 3027–3089（63 页）：27.1–27.2 全节。
- 新建知识页 `Fluent 多相流模型`：九步流程与双精度/granular 材料告诫；三模型启用输入（Eulerian 的 DDPM/Boiling/Multi-Fluid VOF）；体积分数 Explicit/Implicit 与稳态选择准则；界面建模三类型 + Interfacial Anti-Diffusion（强度 0–1、动态强度指数 1.5/上限 0.75）与 Zonal/Phase Localized 离散；格式三表（Geo-Reconstruct 最准首选劣质网格、Donor-Acceptor 过时、保形网格禁零厚壁）；cutoff 1e-6 仅 Explicit（上限 1e-4 局部再分配）；flotsam/节点过滤（0.001）；操作密度四法与 Boussinesq 归零；可压流组合规则与 Enhanced/Alternative Numerics；Implicit Body Force 与 VOF 轻相操作密度；多相组分输运（逐相 Full MCD、Stiff 限一相）；异相反应（Heterogeneous Stiff Chemistry 分数步、population-balance 多反应告诫、arrhenius 仅脱挥发）；传质七机制全录（空化两模型+蒸气压五法+专家选项全套+裁剪压力语义、蒸发冷凝 Lee 0.1 调参与 Thermal Phase Change 单机制限制、组分传质五条件与系数模型推荐组合、替代能量源与 RGP 排除）；多相 BC 三表体系（接触角 90° 语义、Backflow vs From Neighboring Cell、滑移速度比/体积分数、湍流参数归属、逐相复制不联动）；初始体积分数 patch 与 Patch Reconstructed Interface（良序、最后 register）。
- 提取边界：Eq 27.1–27.11 公式体未提取按语义记录；Figures 27.1–27.26 为图形元素；Tables 27.1–27.9 提取照录。
- 更新来源页、Part III 项目页和索引。
- 下一续接位置：同章 27.3，p. 3090（批次 84 = 27.3 VOF，3090–3150）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 84（Part III / Ch.27 第 2 段：27.3 VOF）

- 十批任务（76–85）第 9 批。完成 PDF pp. 3090–3150（61 页）：27.3 全节（另含 27.2.12.2 局部湍流初始化补遗）。
- 扩充知识页 `Fluent 多相流模型`：Localized Turbulence Init（TI 5%/黏度比 10）；稳态 VOF 自动 Global Time Step + Coupled；伪时间法指南；Coupled Level Set + VOF（伪流修正 density/heaviside correction、geo-reconstruct 推荐）；明渠流全套（进/出口组规则与三相限制、自由面/底部液位带符号定义与 UDF profile、压力指定三法、密度插值三法与振荡告诫、Froude 更新/无关出口/倒流静压 TUI、平移 MRF 船壳方案五条）；明渠波 BC（Averaged/Segregated、Power Law 0.16、缓冲层 0.02、Shallow/Short Gravity/Shallow Waves/None 四型与参数、Wave Theories 五种与 Spectrum 尾段、波况检查限值表、瞬态 profile UDF、Stokes Fenton 变体）；明渠初始化 Flat/Wavy 与 auto-init；数值海滩全参数与八条策略；相定义选择建议；表面张力（CSF/CSS、粘附/跳跃粘附三限制、TUI 四参数、Smoothed VOF Gradient、网格与光顺告诫）；Phase Localized Compressive（三应用、limiter 0–2 语义）；Explicit 子步四法与每迭代求解；熔凝置零；VOF-to-DPM（九步、转换参数全套、diffuse lumps 三机制策略、体积守恒气体平衡、Lump Detection 变量）；DPM-to-VOF（双向 LWF、材料匹配与主相限制、三阈值语义、Auto Adaption/Coarsening、半球引入与守恒）。
- 提取边界：Eqs 27.12–27.17 公式体未提取按语义记录；Figures 27.27–27.45 为图形元素；Tables 27.10–27.11 提取照录。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 27.4，p. 3151（批次 85 = 27.4 + 27.5 前半，3151–3205，十批收官）。

## [2026-10-19] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 85（Part III / Ch.27 第 3 段：27.4 + 27.5 前半，十批收官）

- 十批任务（76–85）第 10 批（收官）。完成 PDF pp. 3151–3205（55 页）：27.4 全节 + 27.5.1–27.5.3。**用户指定的十批连续任务（批次 76–85）全部完成。**
- 扩充知识页 `Fluent 多相流模型`：Mixture 相定义（颗粒相七参数——摩擦堆积限 0.61/颗粒温度/固相压力三法/径向分布四法/弹性模量/堆积限 0.63）；IAC 输运方程法（sauter-mean 直径、聚并/破碎核三模型与参数表、wu-ishii-kim 耗散、稳态 URF 1.0）；代数 IAC 五法；流型建模（仅代数滑移低 Stokes、六种相对组合的拖曳/滑移/面积默认表、drag-hybrid 与 ia-hybrid 分区、AIAD 四参数 TUI、Relaxation Time 核验）；Singhal 空化（蒸气压默认 3540 Pa、先机制后启用）；半机理沸腾（适用五限制、Chen 法、参数全套——叠加常数 2/热流乘子/chen-steiner 抑制/forster-zuber/hsu 最小过热/润湿分数 0.2 与 20、Cell Zone 沸腾、求解策略 y+>5 与 URF 系列与热流欠松弛 0.8→0.3、非沸腾验证先行）；Eulerian 相间作用全录（拖曳 20 余种含 EMMS/filtered/syamlal-para 的输入与适用告诫、grace swarm 指数语义、拖曳修正四法、恢复系数 0.9、升力七法与 tomiyama 交叉点、Shaver-Podowski、壁面润滑三法前置条件、湍流扩散五法与 Limiting Function、虚拟质量）；湍流三模型（Mixture/Dispersed/Per Phase）与交互源项三法（troshko-hassan/sato/simonin 限 Dispersed/Per Phase）与先无源后有源策略。
- 提取边界：Eqs 27.20–27.21 与 Theory Guide 14.x 引用式公式体未提取按语义记录；Figures 27.46–27.69 为图形元素；Table 27.12 提取照录。
- 更新来源页、Part III 项目页和索引。
- **十批总结**：批次 76–85 合计摄取 574 页（48+63+33+23+35+32+22+63+61+55），Ch.25–Ch.26 两章全部完成（DPM 234 页 + MPM 22 页）；Ch.27 摄取至 p. 3205（27.1–27.4 + 27.5.1–27.5.3 完成，27.5.4 起待续）；新建知识页 3 页（离散相模型 DPM、宏观颗粒模型 MPM、多相流模型）。
- 下一续接位置：Part III / Ch.27 27.5.4 Including Heat Transfer Effects，p. 3205；其后 27.5.5–27.5.11（至 3242）、27.6 Population Balance（3243–3287）、27.7 Wet Steam（3288–3299）、27.8–27.10（3300–3334）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 86（Part III / Ch.27 第 4 段：27.5.4–27.5.11）

- 新十批任务（86–95）第 1 批。SHA-256 一致、无漂移；完成 PDF pp. 3205–3242（38 页）：27.5.4–27.5.11。
- 扩充知识页 `Fluent 多相流模型`：27.5.4 换热十相关式（two-resistance 及 time-scale/zero-resistance 子模型、fixed-to-sat-temp 仅 Boiling 禁用时、多沸腾机制告诫）；27.5.6 AIAD（两相即可/夹带需第三相同材料、自动 MF-VOF+Sharp/Dispersed+Phase Localized、drag-aiad 四组参数、aiad-entrained-absorption 机制、自动 k-ω SST+SWT、Transient 与保守 URF 自动、夹带 URF 0.2）；27.5.7 GENTOP（非均相 Eulerian、gentop-complete-coalescence、PBM 自动不可改、校准系数 1.0、主-GENTOP 拖曳三法）；27.5.8 DDPM（Transition Factor 0.75→0.5625、Discrete Phase Domain、能量耦合三 TUI、颗粒相 VF Packing Limit 0.4725 与 Enhanced Numerics）；27.5.9 沸腾模型 13 步（三模型 RPI/Non-equilibrium/CHF、自动默认表、Standard State Enthalpy 必须、气泡直径/脱离频率/成核密度/面积影响各法、混合函数 lavieville/tentner/ioilev、NLBF 与淬冷修正互斥、two-resistance-boiling-framework、Coupled、URF 系列、后处理八变量）；27.5.10 多分散沸腾（三相同汽材料、pb-boiling 自动）；27.5.11 Multi-Fluid VOF（拖曳按界面建模联动、各向异性拖曳参数）。
- 提取边界：Eqs 27.25–27.28 公式体未提取按语义记录；Figures 27.70–27.88 为图形元素。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 27.6，p. 3243（批次 87 = 27.6 Population Balance，3243–3287）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 87（Part III / Ch.27 第 5 段：27.6 Population Balance）

- 新十批任务（86–95）第 2 批。完成 PDF pp. 3243–3287（45 页）：27.6 全节。
- 扩充知识页 `Fluent 多相流模型`：PBM 五方法（Discrete bins≤50/Inhomogeneous Discrete 多二次相/SMM/QMOM 4·6·8 矩/QBMM 2·4·6·8/DQMOM 三相限四相无成核）；Phenomena（成核/生长 Inhomogeneous 不可用、VF cutoff 0.8）；Include Expansion（可压二次相、深水钻井）；聚合核六种与破碎核频率七种 + PDF 五种全参数；QBMM 专家 TUI 全套（CFL 五法、SSP-RK 容差体系、zero-moment 调参）；DQMOM 值生成三文件格式（PDF/CDF/Overall Moments、乘真实 VF）；边界条件 Specified Value/Flux + 对数正态自动初始化；成核生长传质（Eqs 27.30–27.34、C_PB_DISCI_PS 守恒、population-balance 机制/反应速率函数免 UDF、结晶须主相 Species Transport）；Size Calculator（气泡四判据/液滴三判据）；QMOM 低 VF 源保留 TUI；后处理变量全集与 Moments/NDF 对话框（.pb）；PBM UDF 宏族（KCl 结晶示例）。
- 提取边界：Eqs 27.30–27.34 公式体未提取按语义记录；Figures 27.89–27.109 为图形元素；Table 27.12 提取照录。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 27.7，p. 3288（批次 88 = 27.7–27.10，3288–3334，Ch.27 收官）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 88（Part III / Ch.27 第 6 段：27.7–27.10，Ch.27 收官）

- 新十批任务（86–95）第 3 批。完成 PDF pp. 3288–3334（47 页）：27.7 Wet Steam、27.8 求解策略、27.9 mphase-summary、27.10 后处理。**Ch.27 全章（pp. 3027–3334）完成。**
- 扩充知识页 `Fluent 多相流模型`：27.7 Wet Steam（droplet-growth-rate young/hill、virial-equation vukalovich/young、rgp-tables、stagnation-conditions、zonal-phase-change、enhanced-source-linearization 全套 TUI；UDWSPF 16 个必需 C 函数 wetst_init/satP/satT/eosP/eosRHO/cpv/cvv/hv/sv/muv/ktv/rhol/cpl/mul/ktl/surft 与 WS_Functions WetSteamFunctionList 结构体、编译加载流程）；27.8 求解策略（双精度建议；压力速度耦合五法 Coupled/PC-SIMPLE/PISO/SIMPLE/SIMPLEC 与 Coupled with Volume Fractions 告诫；2020R1 默认控制变更 TUI；VOF 稳定性——参考压力置于最疏相、PRESTO! 非结构变体、差网格 Geo-Reconstruct、好网格 Compressive、BGM 收敛告诫、Rhie-Chow 选项、瞬态 PISO URF=1、稳态 URF 0.2–0.5；Mixture 滑移 URF ≤0.2 与初场技巧；Eulerian 四种初场方法；Wet Steam 策略）；27.9 define/report/mphase-summary 十五类检查（相数/主相/BC/材料/操作条件等逐项核对照录）；27.10 后处理（各模型专属变量、逐相速度矢量与相索引、Fluxes/Forces/Flow Rate、逐相体积积分）。
- 提取边界：Eqs 27.36–27.43（耦合求解器矩阵/修正）公式体未提取按语义记录；Figures 27.110–27.115 为图形元素；UDWSPF 函数清单照录。
- 更新来源页、Part III 项目页、index.md；来源页"尚未处理"推进至 Ch.28（p. 3335）。
- 下一续接位置：Part III / Ch.28 Modeling Solidification and Melting，p. 3335（批次 89 = Ch.28 全章，3335–3342）。

## [2026-10-20] ingest | 十批任务（批次 86–95）阶段小结（3/10）

- 已完成：批次 86（Ch.27 27.5.4–27.5.11，3205–3242）、批次 87（Ch.27 27.6 PBM，3243–3287）、批次 88（Ch.27 27.7–27.10 收官，3288–3334）。**Ch.27 Modeling Multiphase Flows 全章完成。**
- 待做：批次 89（Ch.28 Solidification/Melting，3335–3342 全章）→ 新页 [[Fluent 熔化与凝固]]；批次 90（Ch.29 FSI，3343–3354）→ 新页 [[Fluent 流固耦合（FSI）]]；批次 91（Ch.30 Eulerian Wall Films，3355–3380）→ 新页 [[Fluent Eulerian 壁面液膜]]；批次 92（Ch.31 Electric Potential/Electrochemistry，3381–3426）→ 新页 [[Fluent 电势场与电化学]]；批次 93–95（Ch.32 Batteries，3427–3536，110 页分三段 3427–3470/3471–3510/3511–3536）→ 新页 [[Fluent 电池模型]]（分段前先从目录地图核对 Ch.32 小节结构）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 89（Part III / Ch.28 全章：Modeling Solidification and Melting）

- 新十批任务（86–95）第 4 批。完成 PDF pp. 3335–3342（8 页）：**Ch.28 全章（28.1–28.5）完成。**
- 新建知识页 `Fluent 熔化与凝固`：28.1 设置（A_mush 推荐 10⁴–10⁷ 与振荡告诫、Lever/Scheil 仅 Species Transport、Back Diffusion γ∈[0,1]、Pure Solvent Melting Heat 必须>0、多组分 mixing-law/DEFINE_PROPERTY 且固液相线同法、壁面 Contact Resistance 与 Marangoni Stress）；28.2 连续铸造 pull velocity 三法（patch/全程 Eq 15.22/只算一步）；28.3 热溶质浮力（限凝固+Species Transport、Solutal Expansion Coefficient、TUI 自定义参考质量分数）；28.4 求解（导热初场、推荐瞬态、α_β 与 Eq 28.1、四类易困难工况）；28.5 后处理五变量。
- 提取边界：Theory Guide Eq 15.3–15.23 未提取按引用记录；Figures 28.1–28.4 图形元素；p. 3336 A_mush 范围与 p. 3341 Eq 28.1 经 fitz 300 dpi 渲染核实；α_β 数值默认本章未印出。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.29 Modeling Fluid-Structure Interaction，p. 3343（批次 90 = Ch.29 全章，3343–3354）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 90（Part III / Ch.29 全章：Intrinsic FSI）

- 新十批任务（86–95）第 5 批。完成 PDF pp. 3343–3354（12 页）：**Ch.29 全章（29.1–29.2.1）完成。**
- 新建知识页 `Fluent 流固耦合（FSI）`：29.1 限制清单（单元类型禁多面体/hexcore、启动后禁换网格、禁三种动网格选项、壁面 UDF 三宏、不兼容自适应/英制 CGS/FMG/自适应步长、Workbench 不可用、线性弹性限屈服强度内、周期边界按无应力）；29.2 十六步设置（Linear/Nonlinear Elasticity、Thermal Effects、电池肿胀自动启用、非常数起始温度场重初始化 TUI、Wall Structure 选项卡五类位移边界与表达式支持、刚体运动病态告警、双向动网格 Smoothing/Implicit Update/Intrinsic FSI 区域、Newmark/Backward Euler、BCGSTAB 默认+GMRES 回退/CG、expert 三开关、enhanced-strain 抗剪切自锁、Rayleigh 阻尼、Structural Point 面、仅 CFF 写文件、单向先流后构提速）；29.2.1 非一致界面（仅流体-固体）。
- 提取边界：Theory Guide Eq 16.16 未提取按引用记录；Figures 29.1–29.3 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.30 Modeling Eulerian Wall Films，p. 3355（批次 91 = Ch.30 全章，3355–3380）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 91（Part III / Ch.30 全章：Eulerian Wall Films）

- 新十批任务（86–95）第 6 批。完成 PDF pp. 3355–3380（26 页，p. 3380 空页）：**Ch.30 全章（30.1–30.7）完成。**
- 新建知识页 `Fluent Eulerian 壁面液膜`：限制（仅 3D/单组分/禁非一致界面-Overset-网格操作-运动变形网格-LWF）；工作流七步与 Make Polyhedra/区域分合影响；模型选项（Solve Momentum/Energy/Scalar、动量解析或方程五项、DPM 耦合 Source Smoothing 默认 2/0.5、Edge Separation/Particle Stripping、DPM injection 同名规则、Phase Coupling 三用途、Treat Sharp Edge）；求解控制（时间离散四法、High Order Explicit 阶 2–4、Maximum Thickness、稳态/瞬态/隐式/DPM 各自参数、自适应升降因子>1）；Wall Film 六子页（边界/初始条件与 Flow Momentum Coupling、源项能量源配质量源告诫、相变三模型、部分润湿三参、撞击三模型与 UDF 覆盖、VOF 交互判据与松弛 0.5）；EWF-VOF 耦合六步；后处理变量全集与 Film 通量报告及 TUI。
- 提取边界：Theory Guide Eq 17.x 与 12.245–12.273 未提取按引用记录；Figures 30.1–30.10 图形元素；p. 3380 空页。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.31 Electric Potential Field and Electrochemistry，p. 3381（批次 92 = Ch.31 全章，3381–3426）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 92（Part III / Ch.31 全章：Electric Potential Field and Electrochemistry）

- 新十批任务（86–95）第 7 批。完成 PDF pp. 3381–3426（46 页，p. 3426 空页）：**Ch.31 全章（31.1–31.4）完成。**
- 新建知识页 `Fluent 电势场与电化学`：31.1 电势场（Potential Equation、Joule 热、电位边界三选与 Contact Resistance、禁 shell conduction）；31.2 精细锂离子电池（定位与 MSMD 区分、全电池限制、Echem Rate 七参、浓度/迁移数参数、老化三模型参数全集与少循环告诫、肿胀 FSI 与更严单元限制、专家三开关、16 步流程含阳极 0 电位/阴极电流符号约定/收敛收紧 1e-10·1e-12/Faradaic URF 0.01→0.001/自动 soc·capacity 报告与电流平衡检查）；31.3 电化学器件（七区几何、Mixture 强制禁 VOF/Eulerian、七类 Device、MEA 三法、九 Options、Electrical System 三法、参数页按器件可用性、Customized 反应/机理流程、四 Zone Type 与默认电导率表、Leverett 三系数 1.417/2.12/1.263、Electrolyte Resolved/Unresolved、Contact Resistivity 单侧、膜扩散默认 1e-15、前 10–20 迭代关源）；31.4 后处理三类别与矢量图。
- 提取边界：Theory Guide 公式未提取按引用记录；符号占位缺失按名称语义记录；p. 3411 电导率表照录；Figures 31.1–31.19 图形元素；原文两疑误照录标注。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.32 Modeling Batteries，p. 3427（批次 93 = Ch.32 段 1，3427–3470）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 93（Part III / Ch.32 第 1 段：32.1–32.2.3.4.4）

- 新十批任务（86–95）第 8 批。完成 PDF pp. 3427–3470（44 页）：Ch.32 段 1/3。
- 新建知识页 `Fluent 电池模型`：MSMD 方法与四电化学子模型总览；限制（nPmS、tab 连续面）；Model Options（解法四选、ROM 前 3 步参考场、内部短路仅 MSMD、NTGK/DCIR/ECM/P2D/User-defined 特性、URF 0.8/1.0、Static/Dynamic 聚类、六种电载荷与停止判据）；Life Model 与老化表（各 20 层）；Time/Event-Scheduled profile（三列/五列、类型码 0–4 与 FC 码 1–8、照录示例）与快充 2D 表四插值法；查找表 plain text/compact 两格式（3D 末位 0=bilinear）；Conductive Zones 与 Electric Contacts（虚拟连接 tab/zone 两格式、zone 式仅限无 Joule 热 Circuit Network）；Model Parameters——CHT（.ttab 瞬态 profile）、FMU-CHT（Tcell 映射）、NTGK/DCIR（U/Y 五数据类型、Raw Data、DCIR 内阻 3D 表、限流表、参数估计 DOD 10–20 层与双 C-rate 要求）、ECM（4P/6P、JH/LM、HPPC 文件与库、充放双跑、6P 先行建议）。
- 提取边界：Theory Guide Eq 19.x 未提取按引用记录；Figures 32.1–32.20 图形元素；示例文件格式照录。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 32.2.3.4.5 Inputs for the Newman's P2D Model 正文，p. 3471（批次 94 = 段 2，3471–3510）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 94（Part III / Ch.32 第 2 段：32.2.3.4.5–32.2.3.6.7）

- 新十批任务（86–95）第 9 批。完成 PDF pp. 3471–3510（40 页）：Ch.32 段 2/3。
- 扩充知识页 `Fluent 电池模型`：32.2.3.4.5 P2D 输入全节（正/负极/隔膜三十余参数、BPX json 导入与三公式差异、echem 数据库文件位置、Use Analytical Cs 降阶、老化稳态 profile、肿胀参数与电极层取向四式、独立模式机械载荷三型）；32.2.3.4.6 User-defined 三参；32.2.3.5 UDF 选项卡；32.2.3.6 Advanced Options——独立 Echem（三模型 profile 输出变量清单）、独立老化（寿命模型参数、Aging Speed Multiplier、aging profile 两类复用与最低字段、自动映射）、Pack Builder（定位文件 12 数/行、先旋后移、前缀重命名、Create NCI、冻结流场+Init、产物不可复用限制）、ROM Tool Kit（LTI/SVD 原理与成立条件、训练数据创建、状态空间矩阵生成 Thermal_ROM_Matlab.m、SVD 场重建）、正交各向异性导热工具（Pack Builder 联动、两告诫）、经验肿胀（限 NTGK/ECM）、Venting 模型（释放面、Species/Phase 选项、Abuse Rate/File Input、无阀门模型）。
- 提取边界：Theory Guide Eq 19.x/16.41 未提取按引用记录；Figures 32.21–32.37 图形元素；BPX URL 原文疑误照录标注。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 32.2.3.6.8，p. 3511（批次 95 = 段 3 收官，3511–3536）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 95（Part III / Ch.32 第 3 段收官：32.2.3.6.8–32.2.9）

- 新十批任务（86–95）第 10 批。完成 PDF pp. 3511–3536（26 页，p. 3536 空页）：**Ch.32 全章（32.1–32.2）完成。**
- 扩充知识页 `Fluent 电池模型`：熵热（Data Table 充放双表或 DEFINE_BATTERY_ENTROPIC_HEAT、P2D 个体/合并 dU/dT 勿双计）；热滥用模型（One/Four/N-Equation 动力学与内短五常数、滥用动力学数据库、N 方程 8 参数文件格式、Fitting Tool/Standalone 全参数与四种图、Run Abuse Only、TUI 拟合 A/E/HW/m/n 回填）；内外短路（UDM Short Circuit Resistance、Patching 或 C_BATTERY_SHORT_R、仅 MSMD）；肿胀算例五步（Young's modulus 自动均值、Smoothing+Linearly Elastic Solid+Intrinsic FSI）；参数估计 TUI 三会话（NTGK DOD 默认 30 与示例 [20] 并照录、ECM 4P/6P+JH/LM、热滥用 Eq 32.1 与多组数据建议）；初始化两法、材料 defined-per-uds、Phi±开关、预定义报告三件、后处理按解法变量全集（Active/Passive Zone Connection 编码、9 位 Connection Index、P2D 平均量、热滥用变量、矢量图）。
- 提取边界：Theory Guide Eq 19.x/32.1 未提取按引用记录；Figures 32.38–32.44 与 Connection Index 数位图图形元素；p. 3536 空页。
- 更新来源页、Part III 项目页、index.md。

## [2026-10-20] ingest | 十批任务（批次 86–95）完成总结

- **全部完成（10/10，合计 309 页，pp. 3205–3536）**。章节收官情况：Ch.27 Modeling Multiphase Flows 全章完成（批次 86–88，3205–3334）；Ch.28 Solidification and Melting 全章（批次 89）；Ch.29 Intrinsic FSI 全章（批次 90）；Ch.30 Eulerian Wall Films 全章（批次 91）；Ch.31 Electric Potential and Electrochemistry 全章（批次 92）；Ch.32 Modeling Batteries 全章（批次 93–95，3427–3536）。
- 知识页变动：`Fluent 多相流模型` 扩充至全章完成；新建 `Fluent 熔化与凝固`、`Fluent 流固耦合（FSI）`、`Fluent Eulerian 壁面液膜`、`Fluent 电势场与电化学`、`Fluent 电池模型`（全章）。
- 下一续接位置：Part III / Ch.33 Modeling Fuel Cells，p. 3537。空页记录：p. 3380、3426、3536。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 96（Part III / Ch.33 第 1 段：33.1 PEMFC）

- 新十批任务（96–105）第 1 批。完成 PDF pp. 3537–3584（48 页）：33.1 PEMFC 全节。
- 新建知识页 `Fluent 燃料电池`：三 add-on 模块总览（PEMFC 推荐/Resolved Electrolyte/SOFC+UE）；PEMFC 概览与限制、几何九区、加载（模块号 9、3D 双精度）；Model 选项卡十七选项（Butler-Volmer/Tafel、Anisotropic E-cond defined-per-uds、Electrical System 三法、F-cycle 最佳实践）；Parameters 电化学八参与液相组；Anode/Electrolyte/Cathode 五 Zone Type 与膜仅固体区、阴极颗粒模型；Advanced（接触电阻、冷却流道、电堆管理、退化模型 UDS-5）；Customized UDFs 与 Reports（监控文件、入口计算器）；自动挂接 UDF 表；边界条件与求解指南；UDS 0–4/UDM 0–18 后处理表与 pemfc_user.c 函数清单。
- 提取边界：Theory Guide Chapter 20 式与 Eq 33.1–33.5 未提取按引用记录；Figures 33.1–33.18 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 33.2，p. 3585（批次 97 = 33.2 Fuel Cell and Electrolysis，3585–3617）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 97（Part III / Ch.33 第 2 段：33.2 Fuel Cell and Electrolysis）

- 新十批任务（96–105）第 2 批。完成 PDF pp. 3585–3617（33 页；p. 3585 顶部 4 个 pemfc_user.c 尾函数已并入 33.1.10）：33.2 Fuel Cell and Electrolysis 全节。
- 扩充知识页 `Fluent 燃料电池`：模型三选（PEMFC/SOFC/SOEC）；选项几乎全默认开（High Temperature PEM、Membrane Water Transport/Multiphase 仅低温、Tafel 回退、Anisotropic E-cond、Knudsen）；URF Saturation Source/Water Content；Enable Smooth Partition 与 F-cycle；Parameters（Open-Circuit Voltage、Leakage Current 总量、Pore Blockage 两项、负电压接阳极的符号约定告诫）；Anode/Cathode 四 Zone Type（Viscous Resistance、Contact Angle、Pore Size）；电解液膜可流体或固体区；Advanced（冷却四物性、Suggest Stack Setup 自动电堆识别与核验告诫）；Reports（Electrolyte Projected Area、External Contact Interface(s)）；33.2.7 集流体建模（固体区 UDS-0 激活、UDS Diffusivity 必须 cond::fuelcells 式 user-defined 勿用 defined-per-uds）；边界/求解指南；UDS 0–3 与 UDM 0–14 后处理表；pem_user.c 十五函数清单。
- 提取边界：Theory Guide Eq 20.69–20.107 未提取按引用记录；Figures 33.19–33.36 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 33.3，p. 3618（批次 98 = 33.3 SOFC with Unresolved Electrolyte，3618–3634，Ch.33 收官）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 98（Part III / Ch.33 第 3 段收官：33.3 SOFC with Unresolved Electrolyte）

- 新十批任务（96–105）第 3 批。完成 PDF pp. 3618–3634（17 页，p. 3634 空页；p. 3618 顶部 33.2.11 尾函数已并入）：**Ch.33 全章（33.1–33.3）完成。**
- 扩充知识页 `Fluent 燃料电池`：33.3 SOFC+UE——限制与加载（模块号 4）；启用自动配置（求解器/组分输运四设置/F-cycle/Metis、diffusivity::sofc 与 E_Conductivity::sofc 材料、支持 shell conduction 不支持横向导电）；UDM 0–13 与 UDS-0（守恒性辨析、线性化量无物理意义）；五选项卡全参数（七 Model 选项含 Electrolysis Mode 符号规则、URF 0.3/0.2、电化学默认值 1e10/100 A/0.5、迂曲度 2–4、Electric Field 双 Tap）；constit.c 八函数。
- 提取边界：Theory Guide Eq 20.108–20.141 与 Eq 33.6/33.7 未提取按引用记录；Figures 33.37–33.42 图形元素；p. 3634 空页。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.34 Modeling Magnetohydrodynamics，p. 3635（批次 99 = Ch.34 全章，3635–3658）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 99（Part III / Ch.34 全章：Magnetohydrodynamics）

- 新十批任务（96–105）第 4 批。完成 PDF pp. 3635–3658（24 页）：**Ch.34 全章（34.1–34.6）完成。**
- 新建知识页 `Fluent 磁流体动力学（MHD）`：实现（感应/电位方程 UDS 2+1 标量、五个核心 UDF、固体区可解、多相混合物域、薄壁/耦合边界、DPM 力与源）；使用（addons/mhd 模块号 1、自动基础设置、case 绝对路径告诫、Magnetic Induction/Electrical Potential 两法、外磁场 Patch（DC/AC/移动场）或 Import（双段叠加）、BC 必须在 MHD 对话框设且不支持自定义、壁面四类、Initialize MHD、Lorentz/Joule 开关、B0 Scale Factor 渐进重启策略）；求解指南（从收敛流场起步、URF 0.8–0.9、电位方程勿设 1）；后处理五矢量；限制四条（低磁 Re、常数各向同性、禁电流指定、AC 低频无时间平均）；磁场正弦/方波定义与外磁场数据文件七段格式。
- 提取边界：Theory Guide Eq 21.x 与 Eq 34.1–34.4 未提取按引用记录；Figures 34.1–34.11 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.35 Modeling Continuous Fibers，p. 3659（批次 100 = Ch.35 全章，3659–3698）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 100（Part III / Ch.35 全章：Continuous Fibers）

- 新十批任务（96–105）第 5 批。完成 PDF pp. 3659–3698（40 页，p. 3698 空页）：**Ch.35 全章（35.1–35.9）完成。**
- 新建知识页 `Fluent 连续纤维模型`：加载（模块号 2、两问语义、UDM=8 与 fm_adjust、绝对路径告诫）；模型与选项（Melt/Dry Spun、双向耦合、侧向拖曳、辐射交互、粘性加热、三组交换相关式）；材料属性（单材料限制、熔纺/干纺差异全清单）；注入定义（四类型、file 七列格式、Injections 对话框操作、组内纤维数、四种纤维网格）；UDF 模板定制与编译（不可改名清单、双平台命令）；求解控制九参数；后处理（fiber-location、交换项七变量、print-xy 23 变量、并行 host 瓶颈）。
- 提取边界：Theory Guide Eq 22.x 未提取按引用记录；Figures 35.1–35.17 图形元素；p. 3698 空页。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.36 Creating Reduced Order Models，p. 3699（批次 101 = Ch.36 全章，3699–3708）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 101（Part III / Ch.36 全章：ROMs）

- 新十批任务（96–105）第 6 批。完成 PDF pp. 3699–3708（10 页）：**Ch.36 全章（36.1–36.4）完成。**
- 新建知识页 `Fluent 降阶模型（ROM）`：Production/Consumption 两段（FMU 2.0/ROMZ）；2026 R1 适用范围（稳态/牛顿/Ma<1/无辐射）；模块 11；输入参数 1–2/3–6/>7/>15 指引；输出参数派生做法；Variables+Zones 选择对应 I/O 参数告诫；Workbench 求值流程（Export ROM→Import ROM→Evaluate→ROM Cell Functions 后处理、Node Values 关）；导出 Profile；限制清单（报告定义可用性、Facet/Area-Weighted 替代建议、四类不支持输出参数）。
- 提取边界：DesignXplorer 侧未摄取；Figures 36.1–36.2 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.37 Using the Solver，p. 3709（批次 102 = 段 1：37.1–37.5，3709–3758）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 102（Part III / Ch.37 第 1 段：37.1–37.5）

- 新十批任务（96–105）第 7 批。完成 PDF pp. 3709–3758（50 页）：Ch.37 段 1/4。
- 新建知识页 `Fluent 求解器使用`：37.1 两求解器/两算法与模型可用性清单、11 步流程；37.2 梯度三选、默认离散规则、一阶-高阶混合因子、QUICK/MUSCL/BCD 适用、压力插值六格式选型（PRESTO! 边界限定 TUI）、密度插值、HOTR 全参数与限制；37.3 P-V 耦合五法选型全则（SIMPLEC/PISO URF 策略、Coupled CFL 200、porous jump 告诫、增强斜率修正）、Flux Type Rhie-Chow 与 Auto Select、URF 失稳组合、NITA 全套（设置、Accelerated Time Marching、显式松弛分层、Expert 三参数、Hybrid NITA 与 Instability Detector、高级 TUI、兼容三清单）、方程顺序、动量修正形式；37.4 密度基 CFL（显式 1/隐式 5、AMG 自降五次）、通量三格式与 Roe-FDS+BCD 组合、CASM/增强 CASM、防发散、FAS 多重网格、残差光顺、轴稳定化；37.5 AMG 循环分配、稳定化方法选型、Fixed Cycle/Coarsening 参数与 smoother 组合表、三粗化选项、verbosity、FAS industrial-strength。
- 提取边界：Theory Guide Eq 23.x/37.1 未提取按引用记录；"MDM"原文照录；Figures 37.1–37.12 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 37.6，p. 3759（批次 103 = 段 2：37.6–37.13，3759–3811）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 103（Part III / Ch.37 第 2 段：37.6–37.13）

- 新十批任务（96–105）第 8 批。完成 PDF pp. 3759–3811（53 页）：Ch.37 段 2/4。
- 扩充知识页 `Fluent 求解器使用`：解限值（适用差异、Positivity Rate 0.2/0.05）；多级时间步进（3/4 级系数、逐级 Dissipation/Viscous）；梯度限制器（三型、三方向、Limiter Filter）；初始化（标准/Patch 全则/shell 区/Workbench 注意/profile 冲洗；FMG 参数与粘性 FMG；Hybrid 三选项卡与多孔介质告诫）；稳态计算（Reporting Interval 兼收敛检查、稳态统计采样两法差异）；瞬态计算（隐式 Fixed/Adaptive 全套、CFL-Based 四 type、Error-Based 预测-校正、Multiphase-Specific 八时间尺度与 Global CFL 建议表、Duration 四法、Extrapolate Variables、显式瞬态与 rk2、时间统计与运行时 DFT beta）。
- 提取边界：Theory Guide Eq 37.2–37.23 未提取按引用记录；Figures 37.13–37.29 图形元素；DFT 限制清单跨段至 p. 3812。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 37.14，p. 3812（批次 104 = 段 3：37.14–37.19，3812–3854）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 104（Part III / Ch.37 第 3 段：37.14–37.19）

- 新十批任务（96–105）第 9 批。完成 PDF pp. 3812–3854（43 页）：Ch.37 段 3/4（并补 37.13.6 运行时 DFT 输入参数与后处理变量尾段）。
- 扩充知识页 `Fluent 求解器使用`：伪时间方法（Local/Global 两法适用与禁用清单、Expert 逐方程 Time Scale Factor/开关、燃烧与 UDS 默认语义、Automatic 步长与 Time Scale Factor 3–10、Length Scale 三法、Solid Time Scale）；远程资源管理提交；Ansys Cloud Burst Compute（前提、认证两法、Job/Case/Journal/Output Details 全字段、View Jobs 九动作与刷新）；收敛监视（单/双精度残差极限、压力基三式与连续方程增强式、密度基 RMS、缩放/归一化/判据四型与默认值、存储与绘图参数、残差场后处理）；统计五量与解量监视运行平均；收敛条件（Check For/All-Any、Stop Criterion 残差公式）；计算中执行命令。
- 提取边界：Theory Guide Eq 37.25–37.37 未提取按引用记录；Figures 37.30–37.52 图形元素。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 37.20，p. 3855（批次 105 = 段 4 收官：37.20–37.24，3855–3904）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 105（Part III / Ch.37 第 4 段收官：37.20–37.24）

- 新十批任务（96–105）第 10 批。完成 PDF pp. 3855–3904（50 页，p. 3904 空页）：**Ch.37 全章（37.1–37.24）完成。**
- 扩充知识页 `Fluent 求解器使用`：自动初始化与 case 修改（三初始化法、命令应答规则、.tsv）；解算动画全流程（六存储类型、回放操作、三种保存与视频参数、读取免 case）；Case Check 五选项卡规则全集（Mesh 4/Models 7/Boundaries 13/Materials 4/Solver 4 条）；收敛与稳定性（判断收敛的准则局限与替代、分步求解与能量开关/反应开关、Poor Mesh Numerics 三档阶与五判据 TUI 族、WFGC 两模式、能量噪声滤波）；Solution Steering（FMG+两阶段、五 Flow Type 马赫区间、Steering/FMG Settings 参数）。
- 提取边界：Theory Guide 引用式未提取按引用记录；Figures 37.53–37.78 图形元素；37.23.1 两处判据符号占位按 37.17 默认值补全；p. 3904 空页。
- 更新来源页、Part III 项目页、index.md。

## [2026-10-20] ingest | 十批任务（批次 96–105）完成总结

- **全部完成（10/10，合计 367 页，pp. 3537–3904）**。章节收官情况：Ch.33 Fuel Cells 全章完成（批次 96–98，3537–3634）；Ch.34 Magnetohydrodynamics 全章（批次 99，3635–3658）；Ch.35 Continuous Fibers 全章（批次 100，3659–3698）；Ch.36 ROMs 全章（批次 101，3699–3708）；Ch.37 Using the Solver 全章（批次 102–105，3709–3904）。
- 知识页变动：新建 `Fluent 燃料电池`（全章）、`Fluent 磁流体动力学（MHD）`（全章）、`Fluent 连续纤维模型`（全章）、`Fluent 降阶模型（ROM）`（全章）、`Fluent 求解器使用`（全章）。
- 空页记录：p. 3634、3698、3904。
- 下一续接位置：Part III / Ch.38 Using the Fluent Native GPU Solver，p. 3905。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 106（Part III / Ch.38 第 1 段：38.1–38.9 前半）

- 新十批任务（106–115）第 1 批。完成 PDF pp. 3905–3940（36 页）：Ch.38 段 1/2。
- 新建知识页 `Fluent GPU 求解器`：平台要求（CUDA 12.8/驱动 570/ROCm 6.0）、启动（许可级、命令行 <n> 三语义、多节点调度）、CPU/GPU 重映射与异步输出（Intel MPI 限定）、CPU 进程分工、case 读入自动转换、支持特性全清单（模型/材料/求解器设置/Optimized LES Numerics/DPM 数值/参数化/边界条件）、Profiles 与 Expressions 三型及 Table 38.1–38.4 摘要。
- 提取边界：Eq 38.1 未提取按语义记录；Table 38.4 跨段；Figures 38.1–38.2 图形元素；"combusion"原文拼写照录。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 Table 38.4 续，p. 3941（批次 107 = 段 2 收官，3941–3974）。
- **协议偏差自报**：批次 102 时来源页"关联页面"清单漏登 [[Fluent 求解器使用]]，本次补登并记录。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 107（Part III / Ch.38 第 2 段收官：Table 38.4 续–38.14）

- 新十批任务（106–115）第 2 批。完成 PDF pp. 3941–3974（34 页）：**Ch.38 全章（38.1–38.14）完成。**
- 扩充知识页 `Fluent GPU 求解器`：Table 38.4–38.15 摘要（边界字段、表达式运算/函数/常数）；DPM 边界与后处理；监视器与报告定义（五类、场变量十一类、表达式支持域）；EnSight DVS 导出差异与流程；Arm 部署；限制清单全集（含 DPM 限制与 TUI 崩溃告诫）；稳态转瞬态；疑难排除五步；性能排查（每 GPU 200 万单元、metis 负载均衡、带宽延迟基准）。
- 提取边界：Table 38.5–38.15 摘要照录；Figures 38.3–38.8 图形元素；p. 3974 章尾。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.39 Adapting the Mesh，p. 3975（批次 108 = Ch.39 全章，3975–4014）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 108（Part III / Ch.39 全章：Adapting the Mesh）

- 新十批任务（106–115）第 3 批。完成 PDF pp. 3975–4014（40 页）：**Ch.39 全章（39.1–39.4）完成。**
- 新建知识页 `Fluent 网格自适应`：指南七条（多面体仅 PUMA、悬挂节点两情形、先收敛后自适应等）；Manual/Automatic 十四步设置（三方法、Prismatic、General Controls 全参数、skip-until）；预定义判据五组（边界层、空气动力学五判据与默认频率、燃烧 Flame+Spark、VOF 三选、Overset 四选项）；四类示例（含 Scaling Option 与 Global Maximum 阈值首选值、表达式布尔照录）；悬挂节点几何重建。
- 提取边界：Eq 39.1 未提取按语义记录；Figures 39.1–39.38 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.40 Surfaces and Cell Registers，p. 4015（批次 109 = Ch.40 段 1，4015–4046）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 109（Part III / Ch.40 第 1 段：40.1–40.2.10 前半）

- 新十批任务（106–115）第 4 批。完成 PDF pp. 4015–4046（32 页）：Ch.40 段 1/2。
- 新建知识页 `Fluent 表面与单元寄存器`：Facet/Vertex 赋值规则（三类表面、主/因变量）；十类表面设置（Zone/Partition/Imprint 弃用/External 不存 case/Split/Point overset 不兼容/Structural Point/Line-Rake 与 Line Tool/Plane 三法多面命名/Quadric 前半）；命名规则与显示注意两条。
- 提取边界：二次曲面方程符号占位按数学语义补记；Figures 40.1–40.22 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 40.2.10 续，p. 4047（批次 110 = 段 2 收官，4047–4078）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 110（Part III / Ch.40 第 2 段收官：40.2.10 续–40.3）

- 新十批任务（106–115）第 5 批。完成 PDF pp. 4047–4078（32 页，p. 4078 空页）：**Ch.40 全章（40.1–40.3）完成。**
- 扩充知识页 `Fluent 表面与单元寄存器`：等值面（前提与临时面告诫、多值一面）；Iso-Clip；Transform（旋转/平移/等距、用户面除外）；Expression Volumes（面/体双态、2D 语义、插值超范围告诫）；表面管理（分组/重命名/渲染优先级治 z-fighting/删除/统计）；单元寄存器全集（七类——Region 形状与鼠标规则、Boundary 两距离法、Variable Limiter、Field Variable 四求导途径与缩放与十种 Type、Residuals 仅压力基、Volume、Yplus/Ystar；上限 16 个；操作报告；复制重命名；后处理显示 1/0）。
- 提取边界：Theory Guide Eq 40.1–40.7 未提取按语义记录；Figures 40.23–40.42 图形元素；p. 4078 空页。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.41 Displaying Graphics，p. 4079（批次 111 = Ch.41 段 1，4079–4130）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 111（Part III / Ch.41 第 1 段：41.1 前半）

- 新十批任务（106–115）第 6 批。完成 PDF pp. 4079–4130（52 页）：Ch.41 段 1/5。
- 新建知识页 `Fluent 图形显示`：persistent/弃用对象、性能五设置；网格显示（四视图、配色三法与随机化、材质、透明层数、Feature/Shrink）；等值线与剖面（快速着色、生成与 Profile Options、Filled/范围三开关、Node-Boundary Values 四组合与 bnv、Setup 存储、定义管理）。
- 提取边界：界面流程为主；Figures 41.1–41.36 图形元素；"XREF" 占位照录。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 41.1.4 正文，p. 4131（批次 112 = 段 2，4131–4182）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 112（Part III / Ch.41 第 2 段：41.1.4 续–41.2.1）

- 新十批任务（106–115）第 7 批。完成 PDF pp. 4131–4182（52 页）：Ch.41 段 2/5。
- 扩充知识页 `Fluent 图形显示`：自定义矢量管理与定义；迹线全集（生成与步长法则、Style 十种、Twist、配色、Path Skip/Coarsen、Reverse/Oil Flow/Pulse 动画、Accuracy Control、Relative、XY along trajectories、三格式数据保存照录、Node Values 告诫、定义与场景限制）；LIC；体渲染（四选项卡、裁剪整窗、高质量图设置）；场景；扫掠面（Create 存等值面、动画 legacy 限）；隐藏图形窗口（null 驱动与恢复）；41.2 起始与嵌入式仪表板。
- 提取边界：界面流程为主；迹线数据文件格式照录；Figures 41.37–41.55 图形元素。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 41.2.1 续，p. 4183（批次 113 = 段 3，4183–4234）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 113（Part III / Ch.41 第 3 段：41.2.7.2 续–41.3.2）

- 新十批任务（106–115）第 8 批。完成 PDF pp. 4183–4234（52 页）：Ch.41 段 3/5。
- 扩充知识页 `Fluent 图形显示`：标注管理（编辑/隐藏/对象关联）；色标全套（Quick-Edit、术语十条、预定义清单照录、选择尺寸对数格式标签、自定义 Editor 与存 case、文献）；灯光（方法三插值、默认灯、定义/移除/重置）；渲染选项（线宽/标记/动画/双缓冲/前面透明/隐藏面四法与设备信息）；增强视觉效果（优先级四选、抗锯齿/反射/静动阴影与 Plane 字段）。
- 提取边界：界面流程为主；色标清单与文献照录；Figures 41.56–41.82 图形元素。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 41.3.2 续，p. 4235（批次 114 = 段 4，4235–4286）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 114（Part III / Ch.41 第 4 段：41.3.2 续–41.10.2.5）

- 新十批任务（106–115）第 9 批。完成 PDF pp. 4235–4286（52 页）：Ch.41 段 4/5。
- 扩充知识页 `Fluent 图形显示`：效果尾（地面网格/交互刷新）；光线追踪全流程与限制；鼠标按键功能全集；测量工具；显示状态（字段清单与全窗作用）与视图（triad 交互、auto-spin、相机参数、视图文件、镜像与周期重复及限制）；高级场景合成（可见性/色透/变换/等值改值/迹线属性/边界框）；关键帧动画（两法、创建播放保存读取）。
- 提取边界：式 41.1 未提取按语义记录；Figures 41.83–41.115 图形元素；"Number of Reppeats"原文拼写照录。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 41.10.2.5 续，p. 4287（批次 115 = 段 5 收官，4287–4324）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 115（Part III / Ch.41 第 5 段收官：41.10.2.5 续–41.14）

- 新十批任务（106–115）第 10 批。完成 PDF pp. 4287–4324（38 页）：**Ch.41 全章（41.1–41.14）完成。**
- 扩充知识页 `Fluent 图形显示`：Order Points 与并行绘图；多数据源 XY（恒 SI 单位）；profile 双绘图；周向平均 TUI 与 band 面；XY 文件格式照录；残差绘图；直方图（Divisions 10、范围、报告）；轴/曲线属性全集（Log 指数语义、blank 线型/标记）；FFT 后处理（五输入格式、频率上下界、四窗函数、prime-factor FFT 点数表、分段平滑 Overlap 0.5、单边谱 Y 轴七函数与 X 轴五函数、倍频程计权表照录）；累积力/力矩/系数绘图；瞬态后处理（Timestep Selector 语义、四功能、动画五步与色标统一 TUI）。
- 提取边界：Theory Guide Eq 41.2–41.18 未提取按语义记录；Table 41.1–41.3 照录或摘要；Figures 41.116–41.136 图形元素。
- 更新来源页、Part III 项目页、index.md。

## [2026-10-20] ingest | 十批任务（批次 106–115）完成总结

- **全部完成（10/10，合计 420 页，pp. 3905–4324）**。章节收官情况：Ch.38 GPU Solver 全章完成（批次 106–107，3905–3974）；Ch.39 Adapting the Mesh 全章（批次 108，3975–4014）；Ch.40 Surfaces and Cell Registers 全章（批次 109–110，4015–4078）；Ch.41 Displaying Graphics 全章（批次 111–115，4079–4324）。
- 知识页变动：新建 `Fluent GPU 求解器`（全章）、`Fluent 网格自适应`（全章）、`Fluent 表面与单元寄存器`（全章）、`Fluent 图形显示`（全章）。
- 协议偏差自报：批次 106 补登批次 102 遗漏的来源页 [[Fluent 求解器使用]] 关联链接。
- 空页记录：本轮无新增空页；p. 3974 为 Ch.38 章尾内容页。
- 下一续接位置：Part III / Ch.42 Reporting Alphanumeric Data，p. 4325。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 116（Part III / Ch.42 第 1 段：42.1–42.2）

- 新十批任务（116–125）第 1 批。完成 PDF pp. 4325–4360（36 页）：Ch.42 段 1/2。
- 新建知识页 `Fluent 数据报告`：报告约定（2D 单位深度/轴对称 2π）；报告定义九类型全参数（Surface 十七/Volume 十含 Sum*2Pi/Force-Moment 四对话框/Flux 十一类型内部区告诫/Mesh/Aerodamping/DPM 七类型与 per-injection TUI/User Defined 宏/Expression 花括号规则）；报告文件与绘图（格式照录、Linux 隐藏文件告诫、Average Over 与瞬态频率约束、滑动平均、清史）。
- 提取边界：42.1 数值符号占位按惯例补记；Figures 42.1–42.22 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 42.3，p. 4361（批次 117 = 段 2 收官，4361–4394）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 117（Part III / Ch.42 第 2 段收官：42.3–42.15）

- 新十批任务（116–125）第 2 批。完成 PDF pp. 4361–4394（34 页）：**Ch.42 全章（42.1–42.15）完成。**
- 扩充知识页 `Fluent 数据报告`：输出参数（14 来源、More 五命令、Average Over=1 约束）；通量报告全语义（九 Options、内部区重定向量、反应流 Total/Sensible 守恒性、DPM 三源与颗粒反应热归属、多相 mixture 查总平衡、DDPM In-domain 字段与限制、电位、其他体积源）；力/压力中心报告（Center 不可存输出参数）；投影面积迭代精度；面积分/体积分注意事项（均匀性指数语义、cell registers 不可用）；效率计算三法与限制；直方图/DPM/S2S 指引；参考值用途清单与 Reference Zone；case 摘要两式；系统资源三报告（CPU/GPU/内存/计时示例照录）。
- 提取边界：界面流程为主；Figures 42.23–42.38 图形元素；DDPM 示例报告照录。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.43 Field Function Definitions，p. 4395（批次 118 = Ch.43 段 1，4395–4434）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 118（Part III / Ch.43 第 1 段：43.1–43.3 前半）

- 新十批任务（116–125）第 3 批。完成 PDF pp. 4395–4434（40 页）：Ch.43 段 1/3。
- 新建知识页 `Fluent 场函数定义`：43.1 三种值语义（单元值/节点值两步算法与 bnv/面值 zone vs 后处理表面、主/因变量边界差异）；43.2 速度三选项与柱坐标四工况约定；43.3 分类表结构（24 表）与限制代码体系照录（bnv/fv/e/kw 等约 80 个）。
- 提取边界：证据边界原则——24 张参考表记结构与代码体系不逐行复制（原表 pp. 4403–4435）；Figures 43.1–43.2 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章表续，p. 4435（批次 119 = 段 2，4435–4480）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 119（Part III / Ch.43 第 2 段：43.3 表尾 + 43.4 前半）

- 新十批任务（116–125）第 4 批。完成 PDF pp. 4435–4480（46 页）：Ch.43 段 2/3。
- 扩充知识页 `Fluent 场函数定义`：Table 43.23/43.24 收尾；43.4 字母序清单前半（A–M）——条目结构（类别+语义+单位量）、通用条目（cell register 与 Runtime DFT 三变量）、代表性定义摘录（叶轮机坐标族、Absolute Pressure、辐射吸收系数、侵蚀累计变形、DPM 两个 Accum 统计的稳/瞬语义、Pressure Discontinuity Sensor、Pressure Hessian Indicator）。
- 提取边界：清单为参考内容按证据边界原则摘录不逐条复制。
- 更新来源页、Part III 项目页。
- 下一续接位置：同章 43.4 续，p. 4481（批次 120 = 段 3 收官，4481–4524）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 120（Part III / Ch.43 第 3 段收官：43.4 续 + 43.5）

- 新十批任务（116–125）第 5 批。完成 PDF pp. 4481–4524（44 页）：**Ch.43 全章（43.1–43.5）完成。**
- 扩充知识页 `Fluent 场函数定义`：43.4 清单后半 M–Z 代表条目（Progress Variable、PSD of dp/dt 族、Q Criterion 两式、NOx/Soot 速率族、Rate of Reaction-n 三模型语义与颗粒换算、Reactor 族、Reduced 温压）；43.5 自定义场函数全节（三条重要语义、创建与数值范围、按钮注意、管理与 Scheme 保存/加载、三示例函数）。
- 提取边界：Eqs 43.30–43.33/43.78–43.81 未提取按语义记录；清单按证据边界原则摘录。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：Part III / Ch.44 Parallel Processing，p. 4525（批次 121 = Ch.44 段 1，4525–4555）。

## [2026-10-20] ingest | Ansys Fluent User's Guide 2026 R1 — 批次 121（Part III / Ch.44 第 1 段：44.1–44.5.4 前半）

- 新十批任务（116–125）第 6 批。完成 PDF pp. 4525–4555（31 页）：Ch.44 段 1/2。
- 新建知识页 `Fluent 并行处理`：并行架构（host/cortex/compute-node-0/MPI）；Launcher 全设置（互连与 MPI 兼容性、hosts 块分配、四调度器、远程 Linux、图形机器）；Windows/Linux 命令行（-ccp 与 Microsoft Job Scheduler 四式含 XML 模板）；分区与负载均衡前半（自动分区 Metis+Laplace 与架构感知重分区、手动指南、对话框各选项卡、Weighting 前半）。
- 提取边界：XML 模板与示例命令照录；Tables 44.1–44.3 照录；Figures 44.1–44.8 图形元素。
- 更新来源页、Part III 项目页、index.md。
- 下一续接位置：同章 44.5.4 Weighting 续，p. 4556（批次 122 = 段 2 收官，4556–4584）。

## [2026-10-22] ingest | 批次 122：Ch.44 Parallel Processing 段 2 收官（pp. 4556–4584）

- 完成新十批任务（116–125）第 7 批：Ch.44 段 2/2，pp. 4556–4584，[[Fluent 并行处理]] 全章完成（批次 121–122）。
- 内容：Weighting 续（DPM Hybrid Optimization/ISAT/Stiff Chemistry flame sensor/model-weighted partitioning、动网格 Auto Repartition）、分区 ID 示例与区内分区（Metis 不支持）、负载均衡动态均衡、分区方法 17 法（Principal Axes 默认、Metis 固体 0.1、虚拟多边形面跨非一致界面）、Smooth/Merge/Pre-Testing、分区过滤器、active vs stored 与 overset 统计、load-distribution、#AMG# 疑难四对策、线程控制、Connectivity、Parallel Check 五项、performance meter 字段全解、Reporting Interval 告诫、加速 DO（do-acceleration? 与不兼容清单）、清 Linux 文件缓存（-cflush / (drop-cache)）。
- 记录原文印刷特征：`do-acceleration?` 等 Scheme 命令照录。
- 下一步：Ch.45 Running Fluent on Arm Compute Nodes 全章（pp. 4585–4588）。

## [2026-10-22] ingest | 批次 123：Ch.45 Running Fluent on Arm Compute Nodes 全章（pp. 4585–4588）

- 完成新十批任务（116–125）第 8 批：Ch.45 全章 4 页，并入 [[Fluent 并行处理]]（Ch.44–45 同页）。
- 内容：aarch64/Armv8.2-A 仅批模式（无 UI/图形、不支持 Windows）；安装包 tar/sh 与推荐 OS（Rocky 8.9/RHEL 8.8/9.3 + 前置库）；Open MPI 4.1.8 唯一 MPI；`fluent 3ddp -i ...` 默认 -g；`-scheduler=slurm`；45.5 已知限制全清单（GUI/图形/Launcher/Meshing/CAD 导入/FMU/EnSight DVS/MC 辐射/RBF 动网格/.gtm→.def/解释型 UDF/CFF S2S view factor/参数化研究/fe2ram/Enhanced Design Tool/几何参数化/Intel MKL/linx64 beta/各向异性自适应 beta/5 Integrations/2 Add-ons/4 Workspaces）。
- 记录原文印刷特征：`linx64 beta features`（疑为 aarch64 语境下原文如此，照录）。
- 关联提示：Arm 不支持参数化研究——与 Ch.47 Parametric Studies 章相关，已在该章批次核对此点。
- 下一步：Ch.46 Using Simulation Reports 全章（pp. 4589–4616）。

## [2026-10-22] ingest | 批次 124：Ch.46 Using Simulation Reports 全章（pp. 4589–4616）

- 完成新十批任务（116–125）第 9 批：Ch.46 全章 28 页，新建知识页 [[Fluent 仿真报告]]。
- 内容：HTML/PDF/PowerPoint 导出与 Report Outline；本地服务器 vs serverless Ansys Dynamic Reporting（远程/参数化并发作业强制本地）；限制 13 条（OpenGL 2.1+、2025 R1 报告需 2025 R2 重生成、Linux QtWebEngine、VMware Horizon、多会话服务器、H264、图形加速、AVZ、字号、BC 组分分数、PPT 长表）；报告节结构与 Header；全局属性（Visibility/Layout/Image/Theme）；拖放重排两约束；生成与查看（FluentReportServer 免重生成、Show Only Modified Settings、超链接互跳、绘图工具栏、invert-normals-for-avz）；保存（Linux PDF 需 X11）；Options 四项；定制（Object State View、分辨率、tabs/columns、*.fsrt 模板、User Data 加图、隐藏节）；TUI 菜单。
- 记录原文印刷特征：`Qt WebEnging locales directory not found.`（应为 WebEngine，原文拼写照录）。
- 下一步：Ch.47 Performing Parametric Studies 段 1（pp. 4617–4650）。

## [2026-10-22] ingest | 批次 125：Ch.47 Performing Parametric Studies 段 1（pp. 4617–4650）

- 完成新十批任务（116–125）第 10 批：Ch.47 段 1/2，pp. 4617–4650，新建知识页 [[Fluent 参数化研究]]。
- 内容：前提与限制 11 条；Ribbon 七分组；Automatic DP Report Settings 两法与 HTML/PDF/PPTX 存储规则；Outline 双视图；设计点表（列定制、Write Data/Capture 默认、Sequential/Concurrent、180 秒远程延迟、分布式内存基准会话与许可、Concurrent Settings Remote/Local、License Details、HPC Platform、本地并发 GPU 一 DP 一 GPU）；optiSLang Create DOE（六默认+八 Pro 采样型、±10% 边界、环境变量查找序）与 Create DOE and Optimize（Criteria 表、AMOP/OCO 全设置、结果表）；DP 右键操作 14 项；Generate DP Reports 跳过规则；CSV 导入导出全规则；Update Mesh Morphs；47.7.8 Base DP 流程与 case 改动处理至 47.7.8.1 开头。
- 记录原文印刷特征：`Parameteric Report`（应为 Parametric，两处）、`Tn the local approach`（应为 In）、`dependant`，均照录并标注。
- 下一步：Ch.47 段 2（47.7.8.1 续，p. 4651 起）。

## [2026-10-22] ingest | 十批任务（批次 116–125）完成小结

- 用户指定十批连续任务（批次 116–125）全部完成：Part III pp. 4325–4650，共约 326 页，Ch.42–Ch.46 五章全章收官 + Ch.47 段 1。
- 章完成情况：Ch.42 Reporting Alphanumeric Data（4325–4394，批次 116–117，[[Fluent 数据报告]]）；Ch.43 Field Function Definitions（4395–4524，批次 118–120，[[Fluent 场函数定义]]）；Ch.44 Parallel Processing（4525–4584，批次 121–122，[[Fluent 并行处理]]）；Ch.45 Arm Compute Nodes（4585–4588，批次 123，并入 [[Fluent 并行处理]]）；Ch.46 Using Simulation Reports（4589–4616，批次 124，[[Fluent 仿真报告]]）；Ch.47 Parametric Studies 段 1（4617–4650，批次 125，[[Fluent 参数化研究]]，章内进行中）。
- 知识页变化：新建 4 页（数据报告、场函数定义、仿真报告、参数化研究）；新建 1 页后扩 1 页（并行处理，Ch.44–45 同页）。本十批无空页记录（Ch.42 起各章末未见空页占位）。
- 累计进度：Part III Ch.1–46 全部完成（pp. 909–4616），Ch.47 章内进行中（4651 起续）。Part IV 尚未开始。
- 原文拼写记录：批次 122 `do-acceleration?` Scheme 命令照录；批次 124 `Qt WebEnging`；批次 125 `Parameteric`/`Tn`/`dependant`。

## [2026-10-23] ingest | 批次 126：Ch.47 Performing Parametric Studies 段 2 收官（pp. 4651–4684）

- 完成新十批任务（126–135）第 1 批：Ch.47 段 2/2，pp. 4651–4684，[[Fluent 参数化研究]] 全章完成（批次 125–126）。
- 内容：初始化三选项与更新方式差异；复用 case 行为表；case 改动管理两节；监视十状态与禁用项、Show 标签、残差图告诫；图形定制；optiSLang 导出五式与 Data Visualization；Parametric Plots；DP 报告与参数化报告全套（条件格式、滑块视图、Pan/Grid/Probe/Pin、XY 过滤比较、PPT 增强、过时管理、输入参数表达式差异）；偏好七项；当前 case 参数表；*.flprj 项目、Project View、DP 工作目录与动画存储、轻量项目。
- p. 4684 为空白页（仅页脚），已记录。
- 下一步：Ch.48 Design Analysis and Optimization 段 1（48.1 Adjoint Solver，pp. 4685–4702）。

## [2026-10-23] ingest | 批次 127：Ch.48 Design Analysis and Optimization 段 1（pp. 4685–4702）

- 完成新十批任务（126–135）第 2 批：Ch.48 段 1/6，pp. 4685–4702，新建知识页 [[Fluent 设计分析与优化]]。
- 内容：伴随 vs 变形器/优化器选择判据（物理支持性、设计空间维度 10–20 分界）；48.1 全节——观测量全类型（Force/Moment/Swirl/压降/表面体积分各十式、adjoint energy/turbulence 前提、目标场 UDM 要求）、通用运算、离散 vs 连续伴随及离散法胜出原因、离散伴随方程构造（Jacobian 转置、伪时间预条件迭代、人工压缩性）、稳定化两方案（Dissipation/Residual minimization）、基于解的自适应（伴随加权选单元）、梯度算法与稳健性、三变形技术（polynomials/direct interpolation/RBF）与两约束法（standard 三建议/enhanced 四限制）。
- 记录：式 48.1–48.54 与一元运算清单符号在抽取文本缺失，知识页已注明须对照原文。
- 下一步：Ch.48 段 2（48.2.1–48.2.3.2，pp. 4703–4730）。

## [2026-10-23] ingest | 批次 128：Ch.48 Design Analysis and Optimization 段 2（pp. 4703–4730）

- 完成新十批任务（126–135）第 3 批：Ch.48 段 2/6，pp. 4703–4730，[[Fluent 设计分析与优化]] 扩充。
- 内容：七步典型工作流；模型假设与一致性检查（k-ε/k-ω、冻结湍流 vs GEKO、UDS/组分伴随 ≤50、SRF/MRF、材料属性清单、边界类型限定、警告/错误机制）；DEFINE_SOURCE_AE；观测量定义全套（类型输入、表达式规则——禁 Flux/Report Definition/gradient/normalize/不连续函数、角度 1[rad]、可用变量清单、Sensitivity Orientation、湍流优化目标三步法）；Methods 对话框（Adjoint Energy/Ideal Gas/Turbulence、AMG Full/Partial、Default/Best Match/Balanced、Rhie-Chow、劣质网格数值）；Controls 对话框（Auto-Adjust、Courant、人工压缩性、各 Scaling/欠松弛、AMG 控制）；稳定化策略前半（None/Blended/Residual Minimization 4、Auto Detection?、Initialize Strategy）。
- 下一步：Ch.48 段 3（48.2.3.2.1 续–48.2.4.3，pp. 4731–4746）。

## [2026-10-23] ingest | 批次 129：Ch.48 Design Analysis and Optimization 段 3（pp. 4731–4746）

- 完成新十批任务（126–135）第 4 批：Ch.48 段 3/6，pp. 4731–4746，[[Fluent 设计分析与优化]] 扩充。
- 内容：残差最小化使用提示与 Blended 策略；Adjoint Residual Monitors（八方程收敛判据）；收敛诊断三 TUI 命令（按区/按单元/按分布）；Run Adjoint Calculation 三初始化按钮与 Calculation Activities（Autosave 默认 0/保留 5、Execute Commands 两时机）；48.2.4 后处理——Postprocess Options（RBF vs Spring、Smoothness）、Sensitivities 场全集（体敏感度/形状敏感度/最优位移/边界敏感度/Flow Blockage/GEKO 与神经网络族/诊断残差场）、矢量场六种、Adjoint Reporting 入口。
- 记录原文印刷特征：`Sesnitivity to Shape`（应为 Sensitivity，照录）。
- 下一步：Ch.48 段 4（48.2.4.3 续 + 48.2.5 Design Tool，pp. 4747–4779）。

## [2026-10-23] ingest | 批次 130：Ch.48 Design Analysis and Optimization 段 4（pp. 4747–4779）

- 完成新十批任务（126–135）第 5 批：Ch.48 段 4/6，pp. 4747–4779，[[Fluent 设计分析与优化]] 扩充。
- 内容：Adjoint Reporting 收尾；Design Tool 全节——11 步流程与 Basic/Advanced；区域定义（圆柱四注意）；区域条件（控制点 20–40、Shape Preserving、Periodic 三区分、连续性阶数）；观测量目标（Objective 三选、参考权重归一化）；九类设计条件全解（bounding surfaces 导入/Orientation/Fit、prescribed profile 表达式 vs UDF、compound superposed/sequenced）；数值设置（RBF Inverse MultiQuadric/Bi-Harmonic、Constraint Relaxation 取舍、Enhanced 三 Improve 选项）；形状修改 14 步（Fix Surfaces adjacency/distance、Check Fatal/Possible、Mesh History 限制、Remesh 仅四面体+棱柱、Export STL/CAD 与 Feature Tolerance 1/10 法则）。
- 记录原文排版特征：p. 4779 CAD Feature Tolerance 条目重复排版两次；`descibed` 拼写照录。
- 下一步：Ch.48 段 5（48.2.6 Gradient-Based Optimizer，pp. 4780–4814）。

## [2026-10-23] ingest | 批次 131：Ch.48 Design Analysis and Optimization 段 5（pp. 4780–4814）

- 完成新十批任务（126–135）第 6 批：Ch.48 段 5/6，pp. 4780–4814，[[Fluent 设计分析与优化]] 扩充。
- 内容：Gradient-Based Optimizer 全节——准备豁免、14 步流程（Goal 四选与二次惩罚/约束可行性机制、三 Method 与接受判定规则、迭代数与收敛判据、Mesh Quality 下限、Monitor 虚实线诊断、Autosave 命名、;@ 命令关键字十个、Optimize 终止条件、最佳实践）；Turbulence Model Design Tool——online/offline 策略对比与组合、设计区域、设计变量（TKE Source Coefficient 推荐）、Model（None/Neural Network + Hook）、NN 设置（激活函数、默认拓扑 24/16/8、八 Input Features 及范围、六表达式上限）、离线训练（Mini Batch 10–1000、.tdat 管理）、验证三步、.scm 管理与训练/部署相似性要求。
- 下一步：Ch.48 段 6 收官（48.3–48.5，pp. 4815–4848）。

## [2026-10-23] ingest | 批次 132：Ch.48 Design Analysis and Optimization 段 6 收官（pp. 4815–4848）

- 完成新十批任务（126–135）第 7 批：Ch.48 段 6/6，pp. 4815–4848，[[Fluent 设计分析与优化]] 全章完成（批次 127–132）。
- 内容：48.3 几何参数化与探索（无需伴随、七类设计条件、Symmetric/External Periodic 与 Design Tool 行为差异）；48.4 网格变形器/优化器（三限制、盒式变形区、六非梯度优化器全解——Compass/NEWUOA/Simplex/Torczon/Powell/Rosenbrock）；48.5 使用流程 17 步（目标函数三式与命名规则、Regular vs Unstructured 控制点分布、BSP、约束三选默认、参数单位规则、Motion Settings 两式与 Indexed Grouping、disable-mesh-check、Custom Calculator、Optimizer Settings 与 Run 号区分、Initialization 三选、%i 文件名陷阱、workbench 路线）。
- p. 4848 空白页（仅页脚），已记录。
- 下一步：Ch.49 Performing System Coupling Simulations Using Fluent 全章（pp. 4849–4886）。

## [2026-10-23] ingest | 批次 133：Ch.49 Performing System Coupling Simulations 全章（pp. 4849–4886）

- 完成新十批任务（126–135）第 8 批：Ch.49 全章 38 页，新建知识页 [[Fluent System Coupling]]。
- 内容：能力与限制（力/位移/热传递、刚体 FSI、Maxwell 电弧、时均 HTC 子步、禁 RSM/NITA/shell conduction 等 13 条）；.scp 生成与 2020 R1 元素数据映射；Fluent Input 三 Option 与 GenerateInputFile()；Workbench 流程；变量七表全录；壁面传力与参考压力语义（海底管道示例最佳 −10 bar）；多孔跳跃两情形；增量位移语义；Fluent 设置（双精度、HTC 参考温度法、UDM 变量、SC 接管时间步）；FSI 建议全节（接触检测、动网格 0.4/1.4 起点、四病理与 dummy UDF 拆区八步、overset 工作流与 donor-priority 0/1）；重启与 Recover Missing Solution；补丁数据 *.ip 变通；排障三文件；许可。
- 记录：式 49.1 与时均公式符号缺失；`k-epsiloin` 抽取伪影注明；p. 4886 空白页。
- 下一步：Ch.50 Customizing Fluent 全章（pp. 4887–4888）+ Ch.51 段 1（4889–4902）。

## [2026-10-23] ingest | 批次 134：Ch.50 Customizing Fluent 全章（pp. 4887–4888）

- 完成新十批任务（126–135）第 9 批：Ch.50 全章仅 2 页（正文一段，p. 4888 空白页）。
- 内容：Ansys ACT 仿真向导（独立 Fluent / Workbench 中的 Fluent 均可运行）；详见 ACT Developer's Guide 与 ACT Customization Guide for Fluent——本手册不展开。
- 簿记决定：内容过小不单独建页，并入 [[Fluent 程序架构与能力]] 的"定制（ACT）补充"节并补关联链接。
- 下一步：Ch.51 Task Page Reference Guide 段 1（51.1–51.3，pp. 4889–4902）。

## [2026-10-23] ingest | 批次 135：Ch.51 Task Page Reference Guide 段 1（pp. 4889–4902）

- 完成新十批任务（126–135）第 10 批：Ch.51 段 1/多段，pp. 4889–4902，新建知识页 [[Fluent 任务页参考]]。
- 内容：章引言 21 任务页清单；51.1/51.2 一句导引；51.3 General 全解——Mesh 组（Scale/Check/Report Quality/Display）、Solver 组（压力基/密度基、Absolute/Relative、Steady/Transient、2D Space 三式与轴对称改 axis 告诫）、Gravity；51.3.1 Scale Mesh；51.3.2 Mesh Display（全局/持久两版、Options 六项、Coloring 四式与 Ctrl+Shift+O）；51.3.3 Set Units（四标准制）；51.3.4 Define Unit；51.3.5 Mesh Colors。CFD Pro 功能受限 Important 已记录。

## [2026-10-23] ingest | 十批任务（批次 126–135）完成小结

- 用户指定十批连续任务（批次 126–135）全部完成：Part III pp. 4651–4902，共约 252 页，Ch.47–Ch.50 四章全章收官 + Ch.51 段 1。
- 章完成情况：Ch.47 Parametric Studies（4651–4684，批次 126，[[Fluent 参数化研究]] 收官）；Ch.48 Design Analysis and Optimization（4685–4848，批次 127–132 六段，[[Fluent 设计分析与优化]]）；Ch.49 System Coupling（4849–4886，批次 133，[[Fluent System Coupling]]）；Ch.50 Customizing Fluent（4887–4888，批次 134，并入 [[Fluent 程序架构与能力]]）；Ch.51 Task Page Reference 段 1（4889–4902，批次 135，[[Fluent 任务页参考]]，章内进行中）。
- 知识页变化：新建 4 页（设计分析与优化、System Coupling、任务页参考、以及上一轮已建的参数化研究在本轮收官）；并入 1 处（Ch.50 → 程序架构与能力）。
- 空白页记录：p. 4684、p. 4848、p. 4886、p. 4888（均章末空页）。
- 累计进度：Part III Ch.1–50 全部完成（pp. 909–4888），Ch.51 章内进行中（4903 起 51.4 Models Task Page 续）。Part IV 尚未开始。
- 原文记录：批次 129 `Sesnitivity to Shape`、批次 130 CAD Feature Tolerance 条目重复排版与 `descibed`，均照录并标注。
- 簿记偏差自报：批次 131 与 132 的 ingest-state 更新因锚点与实际登记文本不符首次断言失败（131 为漏写"Based"、132 为预设了尚不存在的 Ch.49 表行），同会话内核对实际文本后重跑成功，无内容遗漏。

## [2026-10-27] ingest | 批次 TG-1：Tutorial Guide Ch.12 Using the Frozen Rotor Method（pp. 517–534）

- 新来源《Ansys Fluent Tutorial Guide 2026 R1》（1454 页，36 章）首次正文摄取。**来源身份核验发现两份同名 PDF**：用户指定 Downloads 副本（SHA-256 8347db…）与 vault 上一级副本（d889ce…）自 Ch.14 后段起书签错位约 2 页、抽样正文不同，属不同文件版本；按规则以 Downloads 副本为摄取对象并单独登记，两副本进度不合并。检查点新增"来源二"区块与教程批次序列 TG-N。
- 完成批次 TG-1（四批任务第 1 批）：Ch.12 全章，新建知识页 [[Fluent 教程12 Frozen Rotor 方法]]。
- 内容：离心泵（5 叶片、1450 RPM、出口 90 kg/s、入口总压 0 Pa）frozen rotor 稳态仿真；NPS（No Pitch-Scale）turbo 界面连接两个 360° 界面；k-omega SST 选型理由（预测叶轮机械分离）；impeller 用 Frame Motion 1450 rpm 而 volute 静止；Moving Wall 的 Relative（hub 随域转）与 Absolute（inblock-shroud 静止）差别；出口被自动识别为 mass-flow-inlet 须先改类型；Mesh Check 必须在创建 turbo interface 之后否则失败；Green-Gauss Node Based + High Order Term Relaxation；head 表达式 ({p-out}-{p-in})/(998.2·9.81) 配三个表面报告定义；Hybrid Init 用 Absolute 参考帧与入口指定初压；Time Scale Factor 10、200 迭代；结果 head ≈ 20.7 m、叶片压力积分 ≈ 5650 Pa·m²；稳态转瞬态 rotor-stator 三步（transient、Copy to Mesh Motion、Time Step）。
- 记录：教程配套视频 URL 在提取文本中为空（PDF 内为链接图形）；"k-omega"在部分行因字体抽取丢失，依上下文完整行确认。
- 下一步：批次 TG-2，Ch.13 Turbo Setup Workflow 全章（pp. 535–572）。

## [2026-10-27] ingest | 批次 TG-2：Tutorial Guide Ch.13 Turbo Setup Workflow（pp. 535–572）

- 完成四批任务第 2 批：Ch.13 全章，新建知识页 [[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]]。
- 内容：1.5 级轴流压气机（IGV 26 叶/转子 23 叶 17100 RPM/静子 30 通道，入口总压 60 kPa、出口径向平衡静压轮毂 60.5 kPa）经 Turbo Setup Workflow 十三步完成设置——Turbo Preferences 的 zone 名映射规则（inflow/outflow/per1 优先 + 20 项 Search Order 全序列）、GTM 导入（仅支持 *.msh*/.def/.cgns/*.gtm）、Associate/Map Regions、单通道 CFD model、1790.708 rad/s、径向平衡出口、三 span iso-surface、报告定义批量生成；自动产物为 SST k-omega、mixing-plane 默认界面、twf_ 表达式族；求解要点动量 URF 0.1、Time Scale Factor 10；结果等熵效率 ≈0.861（表达式表）/0.857（报告表）、压比 1.234/1.238（两组数教程未解释差异，照录）。
- 记录：提取文本 `equalibrium`、`Dialog Dox` 可疑拼写照录未核对原印刷；纳入排必须连续的 blade row scope 规则已录。
- 下一步：批次 TG-3，Ch.14 Blade Row Interaction 全章（pp. 573–618）。

## [2026-10-27] ingest | 批次 TG-3：Tutorial Guide Ch.14 Blade Row Interaction（pp. 573–618）

- 完成四批任务第 3 批：Ch.14 全章（p. 618 空白页仅页脚），新建知识页 [[Fluent 教程14 叶排交互稳态与瞬态仿真]]。
- 内容：与 Ch.13 同一 1.5 级 Hannover 压气机的两段式分析——稳态 mixing plane（Energy On + ideal-gas、rotor1-shroud 绝对系静止 Moving Wall、三排旋转周期 Conformal 创建、tipgap 独立界面 + mpm1/mpm2 Mixing Plane、Turbo Topology 六边界、 Ave 报告 ×5 与三个表达式 p-ratio/mfr_out_360/iso_efficency（γ=1.4 硬编码）、残差 local scaling + Absolute 判据、100 迭代）与瞬态 pitch-scale（界面改 ps1/ps2 Pitch-Scale、Copy to Mesh Motion、**禁用 Average Pressure Specification——非定常中可致非物理压力反馈**、Second Order Implicit、Period-Based 推进、周期=60/17100/23=0.000152555 s、每周期 40 步×5 周期×每步 10 迭代、效率/流量/压比周期波动属叶片通过交互、熵云图 -7~80 展示尾迹穿越与 pitch-scale 不连续、Periodic Instancing 2/23/2 全环重现）。
- 记录原文照录：报告定义名 `iso_efficency`（缺 i）与其 report plot 名 `iso_effiiciency-rplot`（双 i）不一致；周期面名含 `sdie`（side 误拼）；14.4.12 Reference Values 仅文字一句、截图未提取。
- 下一步：批次 TG-4，Ch.15 Using Sliding Meshes 全章（pp. 619–664）。

## [2026-10-27] ingest | 批次 TG-4：Tutorial Guide Ch.15 Using Sliding Meshes（pp. 619–664）

- 完成四批任务第 4 批：Ch.15 全章（无空白页），新建知识页 [[Fluent 教程15 滑移网格]]。
- 内容：单级轴流压气机（转子 16 叶 37500 rpm/静子 32 叶、周期角 22.5° 只建 1+2 叶、无粘 Euler、air ideal-gas 自动开能量方程）滑移网格瞬态——4 对 wall 改 Rotational 周期（选择顺序决定 periodic/shadow 属），fluid-rotor 用 Mesh Motion 37500 rpm，atm 压力单位 + 0 操作压力，Periodic Repeats 界面前须 TUI `define/mesh-interfaces/one-to-one-pairing? no`，小 zone 作 Side 1 经验规则；Coupled + 显式松弛 0.5/亚松弛 0.9/相对判据 0.01；时间步推导 360/16/15=1.5° → 6.6667e-6 s、一转 240 步；分 1+3+1 转推进并逐段改 report file 输出名防覆盖；滑移网格存 data 必须同存 case、%t 文件名；末转 Data Sampling for Time Statistics（均值+RMS）；FFT 去均值后峰值 = 叶片通过频率 10/20 kHz 及高次谐波；Mean Static Pressure 云图外机匣见激波。
- 知识点对照：Mesh Check 的 unassigned interface 警告在界面创建前属预期（与批次 TG-1"先建界面再检查"互补）；无粘壁面仅需法向零速度。

## [2026-10-27] ingest | 四批任务（批次 TG-1–TG-4）完成小结

- 用户指定连续摄取 Tutorial Guide Ch.12–15（批次 TG-1–TG-4）全部完成，共约 148 页（pp. 517–664），四个叶轮机械教程收官。
- 新来源登记：《Ansys Fluent Tutorial Guide 2026 R1》以用户指定 Downloads 副本（SHA-256 8347db…）为摄取对象；vault 上一级同名文件（d889ce…）经书签与正文比对确认自 Ch.14 后段起内容不同，属不同文件版本，两副本进度不合并（检查点"来源二"区块）。此前该来源仅有目录登记，无旧结论作废。
- 知识页新建 4 页（wiki/projects/）：教程12 Frozen Rotor 方法、教程13 Turbo Setup 叶轮机械设置与分析、教程14 叶排交互稳态与瞬态仿真、教程15 滑移网格；与 User's Guide 既有知识页（运动参考系、叶轮机械流动、滑移与动网格、表达式语言、数据报告、图形显示）建立双向关联。
- 空白页记录：p. 618（Ch.14 章末）。原文照录：iso_efficency / iso_effiiciency-rplot 名称不一致、sdie 误拼、equalibrium 与 Dialog Dox 可疑拼写（未核对原印刷）。
- 教程协议自报：会话前段曾在检查点与来源页预写未完成批次的"已完成"状态，发现后当即改回实际进度（两次），最终回写均以实际完成批次为准。
- 剩余待摄取：Ch.1–11（pp. 33–516）、Ch.16–36（pp. 665–1454）。
