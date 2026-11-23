---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - workflow
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 引导式网格工作流

## 摘要

User's Guide 2026 R1 Part II / Chapter 2（PDF pp. 285–300）介绍 Fluent 引导式网格工作流（Guided Workflows）的通用框架：两种预置工作流的适用条件、几何前提与命名约定、已知限制、任务定制与 Python journal 接口、任务状态/编辑/分组机制、通配符过滤、工作流的保存加载及相关首选项。对自动化最有价值的是 journal 中的 `%py-exec workflow...` 记录格式、`(%py-console)` Python 接口和通配符 journal 的动态解析语义。

## 总览（PDF p. 285）

引导式工作流位于 GUI 的 Workflow 选项卡，用预定义步骤（可增删、分组）从导入的 CAD 几何快速生成**保形连接的体网格**供 solution mode 使用。两个预置工作流：

- **Watertight Geometry**：适用于基本不需要清洗修改的水密 CAD 几何（详见手册印刷页码 p. 301 = PDF p. 301 起的 Chapter 3，尚未摄取）。
- **Fault-tolerant Meshing**：适用于更复杂的非水密几何（重叠、相交、孔洞、重复等缺陷），内/外流均可用（Chapter 4，PDF pp. 409–524，尚未摄取）。

## 2.1 前提与命名约定（PDF pp. 286–287）

- 几何要求：定义良好的 CAD 几何；支持共享公共面的多 body，或单一完全封闭的 body。用 SCDM 的 **Force Share** 验证装配连接性并共享可找到的面；Force Share 不成功时，工作流会尝试连接剩余未连接的面。Discovery 的 named selections 被支持，显示为工作流中的 labels。
- 手册建议（Important）：对（实体模型的）开口周围面与需要局部尺寸的区域使用 named selections（DM）/groups（SCDM），便于在工作流中识别、提高设计变更时的持久性并改善大模型性能。
- **名称模式 → 边界类型自动映射**（由一个默认启用的高级选项控制，作用于所有 zones）：

| 名称模式 | 映射类型 |
| --- | --- |
| `*inlet*` | velocity-inlet |
| `*outlet*` | pressure-outlet |
| `*symmetry*` | symmetry |
| `*far*field*` | pressure-far-field |
| `*mass*inlet*` | mass-flow-inlet |
| `*press*inlet*` | pressure-inlet |
| `*mass*outlet*` | mass-flow-outlet |
| `*outflow*` | outflow |
| `*inlet*vent*` | inlet-vent |
| `*outlet*vent*` | outlet-vent |
| `*intake*fan*` | intake-fan |
| `*exh*fan*` | exhaust-fan |
| `*fan*` | fan |
| `*porous*jump*` | porous-jump |
| `*radiator*` | radiator |
| `*overset*` | overset |

  内部 zone（多区域共享）另有：`*internal*`/`*interior*` → internal；`wall` → wall；`fluid` 或 `enclosure`/`air` 前缀 → fluid region。含冲突边界类型的 label 自动赋 "multiple-types"。**注意**：只有 SCDM/Discovery 的 shrink-wrap body 名字应含 "wrap"；由于这些约定会自动触发类型映射，**不建议**在文件名、body 或 part 名中使用这些模式，也不建议在边界名中用 "fluid"/"enclosure"，并应避免 "unknown"。
- 版本变化注记：几何 zone 前缀由 "geom-" 改为 **"origin-"**；几何 labels 不再使用 "object" 前缀。

## 2.2 限制（PDF pp. 287–288）

- zone 名称与各任务中的列表可能与其他 release 不同：引用具体 zone 名的 **2020 R1 之前创建的 journal 与 .wft 模板文件将不可用**，须替换为新 zone 名。
- 字段级用户协助（悬停字段旁点击帮助图标）：多数工作流字段可用，但**Linux 不可用、使用 ACT 时不可用**；需 OpenGL ≥ 2.1 及加速图形；建议避免经 VMware Horizon 远程桌面使用。
- 工作流特定限制分文：Watertight（印刷页码 p. 302）、Fault-tolerant（p. 410），属 Chapter 3/4。

## 2.3 定制工作流（PDF pp. 288–289）

- 可添加/移除任务（取决于工作流位置与任务输入输出依赖，仅部分任务可插入）；可**多次添加**的任务：Update Regions、Add Boundary Type、Update Boundaries、Run Custom Journal。定制工作流可保存复用（2.11）。
- **journal 与工作流的集成**：标准 journal 在工作流中同样受支持，但工作流使用时**只记录你改动过的值**（journal 更干净）。工作流相关命令带 `workflow` 前缀，经 `%py-exec` 包裹记录，手册示例：

```
(%py-exec "workflow.InitializeWorkflow(WorkflowType=r'Watertight Geometry')")
(%py-exec "workflow.TaskObject['Import Geometry'].Arguments.set_state({r'FileName': r'D:/sample/elbow.dsco',})")
(%py-exec "workflow.TaskObject['Import Geometry'].Execute()")
(%py-exec "workflow.TaskObject['Create Regions'].Arguments.set_state({r'NumberOfFlowVolumes': 6,})")
```

- 自定义 journal 文件可加入两种工作流（Run Custom Journal 任务，另见印刷页码 p. 406），**必须从零创建**（在全新的 Fluent Meshing 会话中）。手册给出按范围设置边界层的 prism 控制自定义 journal 示例（元组列表：名称、last-ratio、首高、层数等字段，面区用通配符如 `"*fuselage*"` 指定）。
- 自定义 journal 脚本（或上游任务）偶尔会改变 zone 名，影响后续基于 zone 的任务；Fluent 的缓解方式：**用 zone 的包围盒位置而非名称来识别 zone**。

## 2.3.1 用 Python 定制 Journal 文件（PDF pp. 289–292）

- 在 Meshing console 输入 `(%py-console)` 进入 Python 接口，可交互调用全部工作流命令及其取值。
- `workflow.TaskObject['<task-name>'].help()` 输出任务对象信息：TaskType（允许值 Simple/Composite/Compound/Conditional/Compound Child）、State（允许值 Out-of-date / Attention-required / Up-to-date / Forced-up-to-date）、Errors/Warnings 列表、Arguments 字典（含由对应命令派生的状态模板与逐参数元数据）。以 Import Geometry 为例：参数含 FileFormat（默认 CAD；允许 CAD/Mesh）、LengthUnit（默认 mm；允许 m/cm/mm/in/ft/um/nm）、ImportType（Single File/Directory Pattern）、AppendMesh、CadImportOptions（OneObjectPer 默认 Program-controlled；允许 Body/Part/File/Selection/Program-controlled；OneZonePer 默认 Body；ExtractFeatures=True、FeatureAngle=40、ImportCurvatureDataFromCAD=True、ImportNamedSelections=True 等）、ImportCadPreferences（CISeparation 默认 none；SeparationAngle=40、Tolerance=0、MaxFacetLength=0、Refaceting=False）。
- `dir(meshing)` 打印全部可用命令；命令名与工作流任务名对应（如 CreateRegions、ModifyMeshRefinement）。`meshing.<Command>.help()` 列出命令关键字参数的 Display text、默认值、允许值与 active 状态；每个对象自带可复制进 journal 的用法示例。

## 2.4–2.9 任务机制（PDF pp. 293–295）

- **2.4 任务状态**（图标语义）：绿色对勾 = 完成；绿色对勾带星号 = 完成但有警告（可继续，console 有细节，右键 Show Errors and Warnings 查看）；闪电 = 未完成；感叹号 = 需处理（有必须先解决才能继续的问题属性）。
- **2.5 任务操作**（树中右键）：Insert Next Task（可插入任务按推荐排序）、Create Group、Update（执行）、Delete、Rename。Fault-tolerant 大模型下任务对象的自动显示依 Task based display 偏好可能禁用；悬停任务上出现的图标可快速显示该任务对象而无需进入任务详情。
- **2.6 分组**：Create Group 把标准任务组成自定义组任务；更新组时按顺序更新组内任务；标准任务更新后不编辑就不能再次更新，而**组任务任何时候都可更新**。
- **2.7 编辑**：完成且 up-to-date 的任务控件被禁用；点 Edit 启用，改完点 Update——当前任务重算、后续 up-to-date 任务变 out-of-date（下游须手动逐个更新），Cancel 则丢弃更改且保持 up-to-date。含 zone/label 选择列表的任务用 **Revert and Edit**：回退到该任务之前状态（后续任务变 out-of-date）再编辑；Cancel 会丢弃更改且状态不回恢复（当前与下游保持 out-of-date）。带单位标签的字段支持改单位后自动换算数值。启用 Dockable Workflow Editor 偏好（并新开会话）后任务属性可拆入可浮动/调整大小的 Workflow Editor；用 Meshing Default 视图复位。
- **2.8 监控更新**：任务执行进度显示在 Fluent 窗口底部的消息与进度条区（Figure 2.2 为图形元素）。
- **2.9 高级选项**：多数任务把高级用户/特性设置放在 Advanced Options 下（平时隐藏，+/- 图标切换）；这些属性由任务使用，只是常规应用不需要改。

## 2.10 列表过滤与通配符（PDF pp. 295–296）

工作流任务的列表（选 zone/label）默认支持 Filter Text 下拉内的文本/表达式过滤（`* ? []`）；选 **Use Wildcard** 提供通配符过滤，用 `?` 或 `*` 时匹配项被自动选中。

- **对 journal 回放的影响（重要）**：Use Wildcard 模式下 journal **捕获通配符本身**，回放时动态解析所有当时匹配的名称（更灵活，适合设计变更后的复用）；Filter Text 模式 journal 只记显式选中的条目名（更静态）。
- 通配符语义（手册原文含义）：`*` = 前面元素出现零或多次（`in*`、`*in*`）；`?` = 单个未知字符（`gr?y` → grey/gray）；`[]` = 字符串开头的字符/数字范围（`[ot]`、`[a-z]`、`[0-9]`）；`^` = 布尔 NOT（`^*in*`）；`|` = OR（`*part*|*solid*`）；`&` = AND（`*part*&*solid*`）。

## 2.11 工作流的保存与加载（PDF pp. 296–297）

- Save Workflow 按钮保存任务/子任务及其设置为自定义模板；Load Workflow 载入；Reset Workflow 重置整个工作流；任务删除走右键 Delete。
- **写网格文件（File > Write > Mesh...）时**：当前工作流连同网格信息存入网格文件；并把会话临时目录中的任务编辑数据复制到工作流专属文件夹（如 `my_mesh_file_workflow_files`），便于在其他会话回退/编辑任务——由 2.12 的 Save task editing data with mesh file 偏好控制。
- 工作流另存为 **`.wft` 模板文件，内部含版本号**（2026 R1 为 `"version": "26.1"`）。
- 工作流文件/journal 中的默认设置是**模型相关**的：套用到新模型时会变；只有你显式改过的值才作为用户设置跨模型保留。

## 2.12 工作流首选项（PDF pp. 297–299）

File → Preferences... 的 General 与 Meshing Workflow 类别：

- **Dockable Workflow Editor**（General）：拆分任务步骤与属性到可移动编辑器；改动后需重启会话生效。
- **Save task editing data with mesh file**：启用时 Saving data for editing tasks 自动设为 Write mesh files。
- **Saving data for editing tasks**（编辑任务时网格数据的管理方式）：
  - *Write mesh files*（默认）：编辑期在临时文件夹写网格文件；关闭该项则编辑已完成任务时自动逐个更新先前任务重新生成网格（不需要事后编辑时建议关闭）。
  - *Write into memory*：信息存内存；**Fault-tolerant 工作流不完全支持，选定后自动改用 Write mesh files**。
  - *Do not save data*：编辑任务不存网格；此时回退更改后再更新该任务会连带更新所有先前任务。
  - 前两种下，任务完成即保存其网格信息，编辑时按任务取回并恢复设置。
- **Save workflow template (.wft) with mesh file**（默认开）：每次写网格自动把当前工作流以同名 `.wft` 存入对应 workflow_files 文件夹；回退/编辑任务的中间自动写文件不创建模板。
- **Temporary files folder**：临时网格文件位置，默认当前工作目录；可写 `.`（自动展开）、环境变量语法（Linux `$env-var`、Windows `%env-var%`）、Linux `~`。
- **Workflow templates folder**：启动时从该目录加载自定义 `.wft` 进 Workflow 下拉；**同基名的 `.scm` 文件在选择该工作流时自动一并加载**。
- **Verbosity**（默认 off）：控制 console 中任务相关消息量。
- **Write CAD logs to**（CAD Logs）：console / temporary files folder（+日志前缀名）/ user folder（+前缀与目录）/ none。
- **Task based display**（Graphics Settings）：auto（按 Automatic display face zone limit 与 facet limit 阈值自动显示）、yes（总是按任务要求切换显示）、no（整个工作流不自动改变显示）。

## 2.13 工作流任务帮助（PDF p. 300）

Workflow Help 按钮访问总体与任务级文档；多数字段可悬停后点帮助图标获得字段级协助（平台限制见 2.2）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Chapter 2 全章，PDF pp. 285–300。本章目录范围至此完成（Chapter 3 自 PDF p. 301 起）。Figure 2.1/2.2 为图形元素，仅文字机制被摄取。
- 名称模式→类型映射表为手册明确陈述（默认启用、作用于所有 zone）；"对本项目的含义"性质的推断未写入正文，如需引用请回查原文。
- 印刷页码引用（p. 301、406、409、410 等）中 p. 301/409 已复核等于 PDF 页码（见 [[Ansys Fluent Users Guide 2026 R1 - 目录地图]]），其余属未摄取章节，仅作定位。
- 通配符语义、`.wft` 版本字段、2020 R1 前 journal/.wft 不兼容、Fault-tolerant 对 Write into memory 的回退均为版本敏感信息，对应 2026 R1。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 网格模式入门]]（Workflow 选项卡简介；pp. 225–258）
- [[Fluent 网格模式文件读写与导入]]（journal/transcript 通用语义；旧版 journal/wft 问题条目）
- [[Fluent 2026 R1 已知限制]]（4K 帮助窗口、旧 wft/journal 拖慢体网格、guided workflow 限制引用等条目）
- [[index]]
