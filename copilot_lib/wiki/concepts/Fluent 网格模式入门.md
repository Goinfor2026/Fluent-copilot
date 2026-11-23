---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - GUI
  - workflow
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 网格模式入门

## 摘要

User's Guide 2026 R1 Part II / Chapter 1（PDF pp. 225–258 的 1.1–1.5 小节）介绍 Fluent Meshing 模式的两种网格生成途径、能力清单、进入网格模式的方式（含双进程构建与动态进程 spawn）、GUI 各组件与 TUI 总览。网格模式是非结构体网格生成程序，体网格完成后经 "Switch to Solution" 一次性转入求解模式。本章 1.6 “Reading and Writing Files” 已整理至 [[Fluent 网格模式文件读写与导入]]。

## 1.1 网格化方法（PDF p. 225）

手册列出在 Ansys Fluent Meshing 中创建网格的两种主要途径：

1. **从既有边界网格生成**体网格（tet、hexcore 或 hybrid）：边界网格可来自 Ansys Meshing 或第三方网格软件，经 File → Import 子菜单（或对应文本命令）导入，也可用独立 grid filter 转换。
2. **从面离散几何（faceted geometry）生成**：基于 CAD 或 Ansys Meshing 的 `.tgf` 格式产生的 meshing objects 生成 tet/hexcore/hybrid 体网格；此途径需先用 object wrapping 与 sewing 操作构建保形连接的表面网格，再生成体网格。

网格生成完成后，通过 Mode 工具栏或命令 `switch-to-solution-mode` 转入 solution mode；其余操作（边界条件、流体属性、求解、后处理）都在 solution mode 进行。

界面本身用 Scheme（LISP 方言）编写；多数功能可经图形界面或交互菜单使用，高级用户可修改 Scheme 函数定制界面。

## 1.2 网格模式能力（PDF p. 226）

手册明确列出的能力：

- 稳健的非结构体网格生成器；生成的体网格可传输至 solution mode。
- 四面体用 **Delaunay 三角化**；棱柱（prism）用 **advancing layer** 方法；可生成 hexcore 网格；带稳健的表面 wrapper 工具。
- 提供 size functions，可为多数 CFD 计算产生理想的尺寸分布；可导出多面体（polyhedral）单元。
- 具备检查、修复和改进边界网格的工具，以保证体网格生成的起点质量；可操作 face/cell zone。
- 单元类型灵活：**Tet** 适合复杂几何；**Hexcore** 结合 tet/hex/prism 的灵活性，单元数更少、hex-to-tet 比更高；**Rapid Octree mesher** 直接作用于面离散几何，在高核数上快速稳健。
- **Hybrid 网格**：壁面附近 prism 层解析边界层；网格线可顺流向；高拉伸棱柱单元减小体网格规模。
- **非一致网格**：适合选择性替换部件的研究；分别生成的网格可 "glue" 在一起。

## 1.3 进入网格模式与启动文件（PDF pp. 226–229）

- 启动方式：Fluent Launcher 选 Meshing 选项，或命令行加 `-meshing`（启动参数全貌见 [[Fluent 启动与批处理自动化]]）。
- **`.tgrid` 文件**：网格模式启动时 Fluent 在 home 目录寻找可选文件 `.tgrid`，用 Scheme `load` 加载，可定制网格模式行为；例如其中写 `(ti-menu-load-string "file read-case test.msh")` 可在启动时读入 `test.msh`。
- 与 `.fluent` 的关系（Important 注记）：`.fluent`（定制 solution mode）如存在也在启动时加载；两文件同在时**先加载 `.fluent` 再加载 `.tgrid`，网格模式下 `.tgrid` 优先**。从网格模式切到求解模式时 `.fluent` **不会**自动重新加载，需要时须手动用 Scheme `load`。

### 1.3.1 双进程构建（PDF pp. 227–228）

Cortex 跑在本地机器、Fluent 跑在远程机器，用于慢网络下获得快的图形响应（大网格远程操作场景）。步骤：本地 `fluent -serv -meshing`；启动控制台给出的形如 `fluent 3d -r24.2.0 -ic=default -node -t4 -mport <ip1>:<ip2>:p2:0 &` 的节点命令；输入 `listen`（默认超时 300 秒）；远程机器登录并把 DISPLAY 指向本地机器，以 `fluent 3d -cx host:p1:p2` 启动。已知限制（手册 Note/Important）：File 菜单类 GUI 对话框（读/导入文件等）不可用，须改用 TUI（如 `/file/read-mesh`）；host 连接断开即数据丢失、不能 detach 后重连，关机前须保存数据；初始图形信息组装可能很慢（跨洲尤甚），此后操作变快。

### 1.3.2 网格/求解模式间动态 spawn 进程（PDF pp. 228–229）

- 并行会话以 meshing 请求的进程数启动；切换到 solution mode 时自动 spawn 达到求解总进程数所需的其余节点。多进程运行默认启用自动 spawn；切换前也可用 TUI 命令 `/parallel/spawn-solver-process` 调整，依次询问：总进程数（≥ meshing 进程数）、互连类型（infiniband / ethernet / shared memory / 默认）、机器列表或 host 文件、ssh 选项。
- 平台限制（Important）：**Windows 不支持动态 spawn**（可保持同核数，但手册建议另起独立 solver 会话继续迭代）；**仅 Linux 支持，且限 default 与 Intel MPI**。
- 在受支持的负载管理器（SGE/LSF/PBS Pro/Slurm）下：总并行节点数须在会话启动时一次请求，切模式时自动 spawn 其余节点；Slurm 下须加 `-gui_machine=<hostname>`（或在 Launcher Scheduler 选项卡的 Graphics Display Machine 选 Current Machine / Specify Machine）才允许动态 spawn。
- 单一机器 host file 配不同 meshing/solver 核数可能产生非预期的 host 分配；手册建议：host file 只给初始（meshing）模式，切到 solution 前用 `parallel/spawn-solver-processes` 命令追加核数并为追加核指定单独的 machine host file。

## 1.4 图形用户界面（PDF pp. 229–257）

对象式（object-based）网格化是上下文驱动的可视化工作流；菜单栏命令适用于 zone-based 网格化或高级显示/报告选项。界面元素可拖拽/选项卡化组合，属性可定制（1.4.2）。各组件要点：

### Ribbon（pp. 231–238）

- **Solution 组（模式切换规则，对自动化重要）**：`Switch to Solution`（命令 `switch-to-solution-mode`）把全部体网格数据传入 solution mode。手册明确的规则：只有**体网格**能传输，表面网格不能；未连到体网格的 face zone（几何对象或未引用 zone）作为 imported surface 传入；连到体网格但未划分网格的 face zone 会被断开并作为 imported surface 传入；**传输前应检查网格质量**（手册指向 Checking the Mesh，印刷页码 p. 558；Checking the Mesh Quality，p. 562——属本章之后内容）；hanging-node 网格在传输时转换为多面体；对象式工作流中合并 cell zone 要求它们处于同一 volumetric region，非连续的须先删对象再用 Manage Cell Zones 对话框。数据传输后**不能从 solution 退回 meshing mode**；但若 solution mode 尚未读入任何文件，可用 `switch-to-meshing-mode` 返回。两模式的部分用户配置项不同，切换时配置可能被改变。
- **Bounds 组**：按选定实体邻域限制显示区域（选择过滤器、+/- Delta、X/Y/Z-Range、Set Ranges/Reset、Cutplanes 最多 6 个、xyz 各 2）。
- **Clipping Planes**：沿绘制线或坐标轴裁剪显示；Insert Drag Line 在图形窗口拖出任意裁剪面；裁剪面自带可拖动的 triad；法向恒沿局部坐标系 x 轴；`(cx-hide-plane-tool "clipping-plane")` 隐藏、F10 或 `display/show-hide-clipping-plane-triad` 切换 triad 显示；triad 大小在 Preferences>Graphics 设置且需重启生效；Flip 反转方向；Show Cut Edges（默认关）；Draw Cell Layer 在裁剪面上显示一层体网格单元、Freeze Cell Layer 固定该层（可对指定 cell zone 经树菜单使用）。
- **Selection Helper 组**：按 Name Pattern 与 Geometry Recovery 级别选择 face/edge zone、对象、对象 zone；Advanced... 打开 Zone Selection Helper 对话框（可按实体数量、最小/最大面区面积细化标准）；适用于一切含 zone/object 列表的对话框。
- **Mouse Probe Function**：Select（单实体并加入列表）、Box、Polygon、Select Visible Entities（仅选中视线可见实体，默认关；网格不连通时所有实体会被选中；只在本地显示有效，远程系统可能产生警告）。
- **Display 组**：All Faces（按 zone 类型着色）、Free Faces（至少一条边未被邻面共享的面）、Multi Faces（多连通面/节点）、Face Edges（与 All Faces 配合；不显示时先关再开）、Title、Help Text、Highlight、Edge Zones、Marked Faces、Transparency（未选中对象/zone 时整个几何透明化）、Explode、Edge Zone Selection Mode、Edges。
- **Examine 组**：Centroid（打印面/边/节点质心到 console）；Distance（测量两点/边/面/zone 间距离；zone 间距离按各 zone facet 的全局平均质心计算，平面与曲面基准不同）；Entity Information（消息窗口输出所选实体详情，印刷页码 p. 904；被设为 target 的 zone/object 会切换标识色）。
- **Patch Options**：Remesh（自动重新划分补丁区域）与 Separate（新面单独建 face zone/object，粒度与类型选项见印刷页码 p. 648）——两者默认启用。

### Workflow 选项卡（p. 238）

访问引导式工作流（guided workflow）模板，如从 watertight CAD 几何快速生成体网格的 Watertight Geometry 工作流；也可用可用任务（局部尺寸控制、创建表面网格、封闭进出口、创建区域等）自建工作流。详见 Chapter 2（印刷页码 p. 285，尚未摄取）。

### Outline View 选项卡（pp. 238–246）

- 对象聚焦的管理树；右键上下文菜单驱动网格生成流程。树顶过滤框支持通配符 `* ? []`、布尔 NOT(`^`)/AND(`&`)/OR(`|`) 与正则（如 `*let*`、`example-wall-?-23`），另见 Filtering Lists and Using Wildcards（印刷页码 p. 295，待摄取）。
- **Model 级菜单**：新建构造几何/对象、设置网格尺寸参数、material points、periodicity、用户自定义组、准备进入 solution mode。
- **CAD Assemblies 树**：CAD 导入选 Create CAD Assemblies 时创建，保留原 CAD 包结构；实体分为 components（装配/子装配/零件）与 bodies（含 CAD zone）；可为 CAD zone 设置 label。菜单提供绘制/删除全部装配、查看 FMDB 文件位置、树外观控制等（完整描述见 CAD Assemblies，印刷页码 p. 605）。
- **Geometry Objects vs Mesh Objects**：以 CAD Faceting 方式导入生成 geometry objects（可非保形）；以 CFD Surface Mesh 方式导入生成 mesh objects（保形）。由 CAD 实体创建几何/网格对象后，对应 CAD 实体被锁定。从其他格式导入的网格，其 edge zone/边界 face zone/cell zone 进入 Unreferenced 分支（不属于任何对象）。
- **对象层级**：全局对象菜单（draw/select all；关联 CAD 时可 update all/detach all）；单个对象菜单（细化与控制任务，仅在树上选择时可用）；Face Zone Labels（几何对象=构成对象的面区组；网格对象=原始 CAD zone/body 或面区；多对象合并后的 label 保留与原几何的联系；labels 围合 Volumetric Regions——封闭 watertight 体积；Join/Intersect... 可创建保形表面网格）；Cell Zones 为体网格区域；Unreferenced 菜单管理未引用 zone。
- 注意：经 Outline View 右键打开的对话框是模态的——必须先完成操作或关闭对话框，才能改变树的选择。

### Graphics Window / Quick Search / Console（pp. 246–247）

- 图形窗口按 Rendering、Color Scheme、Display 选项显示模型；坐标轴 triad 支持点选轴向、iso-ball、90° 旋转、自由旋转；鼠标按键映射见 Mouse Buttons 对话框（印刷页码 p. 576）。
- Quick Search（右上角搜索栏）：结果等同在 ribbon 点击对应控件；**搜到文本命令时会自动把命令文本输入 console，但不执行，须按 Enter**。
- Console：文本界面；错误（红）、用户输入（蓝）、程序输出（黑）三色区分；行为类似 xterm/MS-DOS；Ctrl+C 可在数据处理中 break（已开始绘制则无法取消）；Linux 复制粘贴用“划选+中键粘贴”；Auto-scroll 复选框控制自动滚动；console 右上角图标可打开独立的 Warning / Error 对话框便于复查，**在其中清除消息不会从 console 或 transcript 移除**。

### 工具栏（pp. 247–254）

- Standard 工具栏：布局整理菜单——最新界面布局保存到 home 目录 `.cxlayout` 文件、下次启动恢复；帮助入口（文档、许可证用量、版本）。手册 Note：**meshing mode 不要使用多个 graphics 窗口**。
- Pointer Tools：改变左键角色（Box Select、Rotate View、Pan、Zoom In/Out、Zoom to Area）。
- View Tools：透视/正交切换（仅 3D；正交保持比例、标尺准确）；Fit to Window；Last/Next View；预设视角下拉（iso + 六正交）。
- Graphics Effects：Reflections；Static/Dynamic Shadows（动态阴影随旋转更新，可能降低图形性能）；Grid Plane 显隐。
- Mesh Display Tools：Mesh Display 对话框；Front Faces Transparent。
- Visibility Tools：Axes、Ruler（开启会切到正交）、Titles、Boundary Markers（**meshing mode 不可用**，与 [[Fluent 2026 R1 已知限制]] 的 241447 条目一致）。
- Copy Tools：Copy to Clipboard；Save Picture（另见印刷页码 p. 279）。
- Object Selection/Display 与 Isolate：取消选择、Show All、Hide Selected Surfaces。
- Filter 工具栏：鼠标探针实体类型 Position/Node/Edge/Zone/Object、Draw Sizes 检查探针点网格尺寸、可见实体选择/取消最后实体/清除全部。
- CAD Tools（仅显示 CAD 实体时可用）、Tools（几何 primitive 构造、loop 选择、按面积/曲率隔离）、Context 工具栏（随所选实体变化的上下文任务；快捷键汇编见 Shortcut Key Actions，印刷页码 p. 893）。

### ACT Start Page（p. 254）

ACT 功能启用后可见；启用方式：Launcher 勾选 Load ACT、Arrange workspace 菜单选 ACT、或命令 `/file/load-act-tool`。

### 1.4.2 界面定制（pp. 254–255）

拖拽/停靠元素；meshing mode 可移动 console 与工具栏；误关的元素可右键顶部工具栏恢复或用预定义布局。GUI 基于 Qt Toolkit，图形属性可通过 home 目录的 Qt 样式表文件 `cxdisplay.qss` 修改。

### 1.4.3 Preferences（pp. 255–257）

全局、与算例无关的设置（File → Preferences...）。规则：局部改动只在当前会话生效且不保留；局部改过的项在 Preferences 里点 Apply 只有当全局值本身有变化时才覆盖局部设置（手册用 Logo 颜色例子说明）；并非所有设置适用于所有 workspace（Flow Model 仅 Solution workspace、Meshing Workflow 仅 Meshing workspace）。偏好文件位置：Windows `%HOMEDRIVE%\%HOMEPATH%\.fluentconf\26.1.0\preferences`；Linux `%HOMEPATH%/.fluentconf/26.1.0/preferences`。找不到时先尝试从旧版本迁移，仍无则按默认新建；Default 按钮或删除文件可复位。（`26.1.0` 对应 2026 R1 内部版本号。）

### 1.4.4 帮助系统（p. 257）

主窗口/对话框的 Help 按钮；Help → User's Guide Contents 进入 Meshing 部分；文本命令帮助在 Fluent Text Command List 的 Meshing 部分或 TUI 内建帮助。Help → License Usage 可列出当前 FluentLM 用户；由 ANSLIC_ADMIN 管理的安装会提示相应信息。

## 1.5 文本用户界面（PDF p. 258）

TUI 用 Scheme（Lisp 方言）编写，是程序底层过程接口之上的分层菜单系统；输入可存为文件、用文本编辑器修改后再读入执行（journal 基础），与 Scheme 扩展语言紧密集成以实现高级控制与定制。完整命令列表见 Fluent Text Command List。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Chapter 1 的 1.1–1.5 节，PDF pp. 225–258。印刷页码引用（如 p. 558、605、893、904）为手册文内链接指向，属尚未摄取章节，仅作定位。
- 1.4 节包含大量图形元素（Figure 1.1–1.20）；文本提取只覆盖文字描述，截图中的界面细节未摄取。
- **1.6 “Reading and Writing Files”（PDF pp. 258–284）已整理至 [[Fluent 网格模式文件读写与导入]]**；p. 258 上半的 1.5 TUI 与 1.6 章头归本页。
- 界面布局、默认值与可用选项随版本变化；本页对应 2026 R1。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 网格模式文件读写与导入]]（同章 1.6）
- [[Fluent 网格质量诊断]]（切模式前建议做的质量检查，与之衔接）
- [[Fluent 启动与批处理自动化]]（`-meshing`、Launcher、并行启动参数）
- [[Fluent 程序架构与能力]]（meshing/solution 双模式的总体介绍）
- [[Fluent 2026 R1 已知限制]]（Boundary Markers、双进程构建等相关条目）
- [[index]]
