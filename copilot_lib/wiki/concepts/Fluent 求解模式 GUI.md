---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - GUI
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 求解模式 GUI

## 摘要

User's Guide 2026 R1 Part III / Chapter 1（PDF pp. 917–962）描述 Solution Mode 的图形界面：七大组件（ribbon、Outline View 树、工具栏、task pages、console、对话框、graphics windows）、拖放/复制/TSV 导入导出、对话框与输入控件体系、快捷属性编辑器、界面定制、Preferences 文件位置、界面语言本地化、空闲超时与帮助系统。多数组件与 Meshing 模式同构（见 [[Fluent 网格模式入门]]），本页记录 Solution Mode 特有或新增的内容。

## 1.1 组件（PDF pp. 917–953）

### Ribbon（pp. 918–920）

主设置入口，标签大体按典型仿真工作流从左到右排列。各标签入口：**Domain**（网格操作与度量、几何修改、turbo）；**Physics**（General、物理模型、材料、边界条件）；**User-Defined**（UDF/标量、named expressions）；**Solution**（求解方法与控制、监视、初始化、运行设置）；**Results**（图形、报告、动画）；**View**（显示外观、工具栏显隐）；**Parallel**（并行状态）；**Design**（adjoint）；**Parametric**（设计点研究、仿真报告）；**Learning and Support**（教程/文档/**Ansys Engineering Copilot——仅在许可证含 `gpt_ai_plus` 键时可用，否则打开 Information Space**）；**Transient Postprocessing**（瞬态数据后处理，印刷页码 p. 4317）。

### Outline View（pp. 920–926）

- 左侧交互树；条目顺序配合 ribbon 的典型设置流程；Shift/Ctrl 多选、右键命令；树顶过滤框支持通配符/正则（见 Filter Text Entry Boxes）。
- **拖放（同会话）**：文件拖入会话直接打开（支持 `.cas.h5/.cas/.cas.gz/.dat.h5/.dat/.dat.gz/.msh.h5/.msh/.msh.gz/.jou/.log/.csv/.pdf`）；cell zone/边界条件拖到另一边界 = 复制条件、拖到图形窗口 = 显示（累加）；report definitions/surfaces/graphics/plots/scene 拖到父分支 = 建副本、拖到同类对象 = 属性复制；graphics 对象拖入图形窗口类似 Add to，多个对象后可右键 Save as Scene 随 case 保存；**plot 对象拖入图形窗口会清除先前显示、只显示最新拖入者**。
- **拖放（跨会话）**：仅支持**同 release 版本**；Workbench 下需关闭共享许可；**拖单个对象只在新会话创建一个对象**——依赖（如 mesh 显示所用的 plane surface）不会被一并创建，依赖缺失则对象无效。跨会话还支持 Solution Methods/Controls/Initialization/Run Calculation 设置复制、Animation Definitions 整分支或单个拖放（同名对象被标记并更新设置）、report definitions/surfaces 同名时确认后更新。
- **Copy & Paste** 对象：边界条件、named expressions、report definitions/files/plots、后处理对象。**多相 mixture 级边界条件可拖放/复制，phase 级不可**。
- **Export To File / Import From File**（右键）：边界条件（phase 级除外）、named expressions、report definitions、后处理对象——保存为 **`.tsv`**（另见印刷页码 p. 982）。

### Graphics Windows（pp. 926–930）

- 内嵌或独立窗口；右键窗口顶部切换 tab/子窗口（SubWindow View）。
- **Hover-Over Highlight**（Preferences > Appearance > Selections）：悬停高亮面边并 tooltip 显示面名；Edge Thickness / Front Edge Transparency 控制外观。Surfaces 列表悬停时同步高亮（需 mesh outline 显示 + 该选项启用）。
- 右键上下文菜单可直接改设置（示例：右键 inlet 设为 velocity-inlet）。**右键不开菜单的三种情形**：RMB 设为 Probe 且无选择时右键模型；RMB 设为 Zoom/Fit to Window；"reserved" 窗口（求解中自动生成的灰色图标窗口：残差、report plots、animation definitions）。
- **取消显示操作**：数据处理阶段 Ctrl+C，开始绘制后不可取消。显示项变更后窗口可标记 [Out of Date]——右键 Refresh Display；mesh display 刷新按全局 Mesh Display 对话框当前选择显示（可能与原显示不同）。右键不出菜单时查 Preferences > Navigation 的鼠标映射。
- Copy to Clipboard：窗口标签右键或 **Ctrl+Shift+C**；窗口尺寸影响图片字体大小。

### Quick Search（p. 930）

右上搜索栏或 **Ctrl+F**；点击结果等同 ribbon 点击；**文本命令结果自动填入 console 但不执行，须按 Enter**。

### Toolbars（pp. 930–937）

- **Pointer Tools**：Box Select、Rotate View、Pan、Zoom In/Out、Zoom to Area（右拖放大/左拖缩小）、Probe。**Important：求解迭代中滚轮缩放不工作——需在计算开始前把 Zoom In/Out 赋给左键**。Probe 依赖 Preferences > Appearance > Selections 的 Hover-Over Probe Values；限制：全局 graphics 对象不支持（mesh 除外）、Pathline/Vector 启用后需重新显示、镜像/周期重复中的 vector 不高亮、场景中的 pathline 无探针值；并行时探针位置偏差可关 Remove Partition Lines 改善；Ctrl+Shift+C 截图可包含探针值。
- **View Tools**：透视/正交（仅 3D；正交比例尺准确；Preferences 设 Orthographic 时额外出现 Ruler 选项）、Fit to Window、Last/Next View、预设视角、**Synchronize Views**（所有已开窗口同步到活动窗口；其后新开窗口默认不同步，需右键 Synchronize > Add this window）。
- **Visibility Tools**：Axes/Ruler/Titles、Boundary Markers（solution mode 可用；Meshing 模式不可用）。
- **Copy Tools**：Copy to Clipboard（Ctrl+Shift+C）、Save Picture（印刷页码 p. 1040）。
- **Object Selection/Display**：Show All、Hide Selected、**Make Selected Transparent（临时效果——Save as Scene 不捕获、case 不保存；无选择时清除本工具施加的全部透明；重复点击可移除单面透明）**、Clear Selection（同时清除测量显示）。
- **Graphics Effects**：Reflections、Static/Dynamic Shadows（动态阴影随旋转更新、可能降低性能）、Grid Plane。
- **Additional Display Options**：Filter Selected Surfaces——预定义 box select 选中范围或过滤已选面（配合 mouse-multi-select/-add/-toggle）。

### Task Pages（pp. 937–938）

双击树分支在右侧打开；比右键菜单提供更多高级设置；每页 Help 按钮指向 Task Page Reference Guide（印刷页码 p. 4889）。General task page（p. 4890）的全局设置保存进 case。

### Console（pp. 938–941）

- 可移动/选项卡化，或经 "arrange the workspace" 的 **Console>In Message Window** 停靠进 Messages 对话框（与 Warnings/Errors 并列标签；停靠时新警告/错误图标在窗口状态栏右下）。
- 文本着色区分用户输入/标准输出/警告；auto-scroll 复选框；顶部搜索栏可检索 transcript（导航/清除按钮）。
- 行为类似 xterm/MS-DOS；Ctrl+C break；Windows 复制用 Ctrl+Insert / 粘贴 Ctrl+v，Linux 划选 + 中键粘贴。
- Warning/Error 对话框（console 右上图标）：**消息是到 console 位置的 hyperlink；在对话框中清除消息不会从 console 或 transcript 移除**。
- **Note：console 有 30,000 行保留上限，超过后 auto-scroll 失效。**

### Dialog Boxes（pp. 941–953）

- 两类按钮行为：**OK/Cancel**（应用即关）与 **Apply/Close**（保持打开便于反复修改；按钮常改名 Display/Adapt——后处理与网格自适应多用后者）；全部对话框有 Help 按钮；含列表的对话框可扩展。
- 输入控件：Tabs；Buttons；Check Boxes；Radio Buttons（Linux 显示为菱形）；Text/Integer/Real Number Entry（整数支持科学计数如 5E4；**步进箭头配合 Shift=×10、Ctrl=×100**；实数标签显示单位）；**Filter Text Entry**（通配符/正则过滤，如 `*let*`、`example-wall-?-23`；输入即过滤，Enter 展开匹配子分支）；单选/多选列表（点击切换、Shift 范围选、拖选；多选列表右上按钮：显示已选、树视图按名称/类型分组并可按组全选、全选/全不选）；Drop-Down List；Scales（滑杆 + 箭头键）。
- 对话框类型：Information、**Warning（确认前暂停控制）**、Error、**Working（任务完成自动关闭，可 Cancel 中止任务）**、Question、**Select File**：UNC 路径需对路径中所有文件夹有权限；Files of type 过滤——非标准扩展名需换过滤或选 All Files (*)；**Display Mesh After Reading**（读后自动显示全部边界 zone（3D 内部 zone 除外）；默认值由 Launcher 同名选项决定）；**Lightweight**（大网格只读 case 设置不读网格数据，便于低内存机器检查/修改设置；详见 Reading the Lightweight Data，印刷页码 p. 980）；多文件选择累积列表（Remove 可移除）；Write Binary Files 复选框。

### Quick Property Editor（p. 953）

Preferences > Appearance 启用 **Show quick property view** 后，选中边界即在图形窗口出现快捷属性编辑器；离开字段即保存；More... 打开完整对话框；多相模型可下拉切换 phase（编辑 mixture 或各相）。**quick-edit 的每次改动打印到 console 并写入 transcript（含旧值与新值）。**

## 1.2–1.6 定制、偏好、语言、超时与帮助（pp. 954–962）

- **定制**：Color Theme 选 Dark 可用暗色主题；**Application Font Size**（Appearance 分支）影响 ribbon/对话框/console/树/task page 字体（**不影响 Simulation Reports**）；图例/colormap 字体在 Graphics > Colormap Settings（Text Behavior 固定/自动 + 比例或固定字号）；GUI 基于 Qt Toolkit，可用 home 目录 `cxdisplay.qss` 样式表定制；拖拽布局、折叠组件（折叠图标）；**组件停靠坞（component dock，窗口左侧）恢复折叠/隐藏项**；预定义布局与右键 Outline View/Console 顶部恢复。
- **Preferences**（pp. 955–957）：File → Preferences...；悬停 tooltip；顶部搜索栏过滤设置；局部覆盖仅本会话生效、Apply 行为的细节与 [[Fluent 网格模式入门]] 1.4.3 相同；**配置文件位置：Windows `%HOMEDRIVE%%HOMEPATH%\.fluentconf\26.1.0\preferences`（若定义了 `%HOME%` 环境变量则为 `%HOME%\.fluentconf\26.1.0\preferences`）；Linux `%HOMEPATH%/.fluentconf/26.1.0/preferences`**；找不到时先尝试从旧版本迁移，否则按默认新建；Default 按钮或删除文件复位。
- **界面语言**（pp. 957–959）：启动前定义环境变量 `lang=ja`/`lang=ko`/`lang=zh`（可在 Launcher Environment 页设置）。**未完全翻译**：下拉菜单/列表项、quick search 结果、弹出消息、图形窗口标题与标签、对象名（边界条件、图形对象等）、无等价词的标签（X/Y/Z/Cp/OK 等）、**Console 整体**。Important：**workspaces（Aero、Icing、Material Processing、Post-Analysis）的本地化为 Beta 级暴露**（Post-Analysis 本身也是 Beta）。
- **空闲超时**（pp. 960–961）：File → Idle Timeout... 启用 Automatically exit after timeout 并设分钟数——**剩 5 分钟时弹出 Application About to Exit 倒计时；关闭前自动把 case 与 data 保存到工作目录**；"Remember this choice for future sessions" 仅保存当前设置供未来会话（复选框本身不保持勾选）。或用环境变量 **`FLUENT_MAX_IDLE_TIMEOUT`**（分钟）设置管理员级最大空闲时间，用户不能超过——适合集群/HPC 批处理资源管理，应定义在运行批作业的机器上。限制：**对 Fluent Meshing 不可用（Workbench 内运行除外）；Windows 下与 `-g`/`-gu` 启动模式不兼容。**
- **帮助系统**（pp. 961–962）：task page/对话框 Help 按钮、User's Guide 目录、其他文档（Theory Guide、Customization Manual）；最后两章（Task Page Reference Guide p. 4889、Ribbon Reference Guide p. 5565）合称 Reference Guide；Learning and Support ribbon 页；许可证信息由 ANSLIC_ADMIN 管理并打印到 console；Help 菜单 Version... 查看版本。**推荐浏览器：最新 Chrome/Firefox；不支持 IE/Edge。**

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part III / Chapter 1，PDF pp. 917–962；目录范围至此完成（Ch.2 自 p. 963 起）。Figure 1.1–1.33 及对话框示意为图形元素，仅文字机制被摄取。
- 印刷页码引用（p. 215、980、1040、4241、4889、4890、4894、5478 等）指向尚未摄取章节，仅作定位；p. 215 属 Part I Chapter 4（已摄取 [[Fluent 启动与批处理自动化]]）。
- 快捷键（Ctrl+F、Ctrl+Shift+C）、环境变量（`lang=*`、`FLUENT_MAX_IDLE_TIMEOUT`）、console 行上限（30,000）与浏览器要求均为手册明确陈述，对应 2026 R1。
- 与 [[Fluent 2026 R1 已知限制]] 交叉：4K 帮助窗口、Linux AMD 显卡、远程显示等 GUI 限制条目在本章未重复。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 手册排版与数学约定]]（本章路径写法所依据的约定）
- [[Fluent 网格模式入门]]（Meshing 模式同构组件）
- [[Fluent 2026 R1 已知限制]]（GUI 相关限制条目）
- [[index]]
