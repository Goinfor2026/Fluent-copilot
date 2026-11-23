---
type: concept
created: 2026-10-22
updated: 2026-10-22
tags:
  - Ansys Fluent
  - simulation-reports
  - reporting
  - html-pdf-export
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 仿真报告（Simulation Reports）

## 摘要

User's Guide 2026 R1 Part III / Chapter 46 "Using Simulation Reports"（PDF pp. 4589–4616，八节）。**摄取状态：全章完成（批次 124，pp. 4589–4616，46.1–46.8 全部八节）**。仿真报告把 case/data 的设置与结果汇总为 HTML/PDF/PowerPoint 可分享文档；与 [[Fluent 数据报告]]（Ch.42 报告定义与代数数据报告）互补。

## 46.1 概览（pp. 4589–4592）

- 仿真报告汇总并分享仿真设置与结果——关键信息从项目设置编译，导出 **HTML、PDF 或 PowerPoint**；可定制。需已保存 case 与 data 的完整仿真；从 Outline View 的 Simulation Reports 任务页打开 **Report Outline**。
- 任务页字段：**Current Report**（已有报告下拉）；**Report Name**（生成后仍可重命名）；**Report Address**（生成报告的可分享 URL）；**Report Sections**（各节描述填写）。
- 可在任务页随时改设置再生成新报告（增删描述、树节点勾选、改等值线/绘图视图）。
- **数据管理两式**：本地服务器（默认）或直写（serverless）**Ansys Dynamic Reporting** 数据库——Preferences → Simulation 类别 → Simulation Reports 切换。**注意：单一远程作业提交与参数化远程并发作业提交生成的报告只用本地服务器，无视该偏好设置**。

### 46.1.1 限制清单（p. 4592–4593）

- Fluent 界面内显示报告需 **OpenGL 2.1+**；版本更低则不在 Fluent 内打开（仍可导出 HTML/PDF/PowerPoint 另看）。
- 打开含 2025 R1 或更早版本所建报告的 case 时视图渲染出错——**在 2025 R2 重新生成同一报告即可**。
- Linux 生成报告时控制台可能打印 `locale_file_path.empty()` 与 `Qt WebEnging locales directory not found.`（原文如此）警告——可安全忽略。
- VMware Horizon 远程桌面连接可能导致生成失败。
- 多个 Fluent 会话共用同一工作目录的同一报告服务器：**关闭启动服务器的第一个会话会停掉服务器**；第二会话若恰在用则可能报错/报告数据损坏（服务器下次需要时可自动重启）。
- Linux 上 HTML 报告内动画若浏览器不直接支持 H264 MP4 需插件。
- Linux 上必须**开图形加速**（如 OpenGL2 驱动）生成报告。
- 报告动画与 AVZ 文件不能在 Fluent 界面内可视化。
- Linux 上生成失败疑因旧版遗留中间文件——删除 Linux home 下 `/.local/share/fluent/QtWebEngine` 规避。
- Preferences 的 Application Font Size 不作用于仿真报告。
- 报告不显示边界条件的组分质量分数。
- 导出 PowerPoint 时长 named expression 表不自动跨页拆分。

## 46.2 准备报告（pp. 4593–4596）

- 默认含仿真基本信息，可选补充。Report Sections 树：**Header**（默认 Analyst 姓名 + Date；可加 Company name、Logo 图像、URL、Phone、Fax、Address、Description）；其余各节可写自定义 Description：System Information；Geometry and Mesh（含 Mesh Quality 与 Orthogonal Quality）；Simulation Setup（Solver Settings + Physics——Models、Material Properties、Cell Zone Conditions、Boundary Conditions）；Run Information；Solution Status；Named Expressions；Report Definitions；Plots（Residuals 与 Report Plots；可指定 Line Type(s)/Line Marker(s)）；图形对象（Mesh、Contours、Vectors、Pathlines、LICs、XY Plots、FFT、Scenes、Animations、Histograms、自定义视图；**View 字段选朝向（front/back/left/bottom/isometric 等），Preview View 预览；默认 isometric**）；User Data；Solution Status。各组件可勾掉不入报告；清除图标取消当前节点并清显示。
- **46.2.1 全局属性（Report Settings）**：Visibility（勾选包含/排除）；Layout Settings（结果图排 tabs 或 tabular columns——作用于全部图形结果图）；Image Settings（默认视图朝向与分辨率）；Theme Settings（**Use Dark Theme**——深底白字、图形图像保持原样；Fluent 用深色主题偏好启动时默认启用）。
- **46.2.2 组织**：拖放树节点重排（多选拖到节点加到子节点底部；光标指示可/不可放；两节点间出现线表示可插入）。**约束**：Header 必须在最前（树顶节点）；**专用容器节点**（子节点呈 tab 排列者，如 Contours、Vectors）**内容不可改**——不能加入也不能移出。

## 46.3 生成（p. 4596）

任务页底部 **Generate** 生成。首次生成额外耗时——启动 Fluent report server 需初始化。生成中显示进度条，右侧 **Stop** 可中断。

## 46.4 查看（pp. 4597–4613）

生成后出现在图形窗口旁的独立标签页；或任务页 **View** 按钮。**报告设置随 case 保存**；只要工作目录的 **FluentReportServer** 文件夹未被移动/删除，读入旧 case 可直接 View 无需重新生成。报告内有超链接目录跳转。

- **46.4.1 System Information**：Application（产品名）、Settings（3D、双精度等）、Version、Source Revision、Build Time、CPU、OS。
- **46.4.2 Geometry and Mesh**：默认 **Mesh Quality 表**（region 名、volume fill type、最小 orthogonal quality、最大 aspect ratio）+ 默认 **Orthogonal Quality 图表**。
- **46.4.3 Simulation Setup**：Solver Settings + Physics（Models/Material Properties/Cell Zone Conditions/Boundary Conditions）。**Show Only Modified Settings 默认启用**——只显示偏离默认值的设置。Physics 下还有 **Reference Values** 节（密度/压力/温度等参考值）。边界条件中用到的 named expressions 以超链接显示，跳到报告 Named Expressions 节。
- **46.4.4 Run Information**：机器数与核数、内存占用等；可勾 **Include License Usage** 加许可证信息。
- **46.4.5 Solution Status**：残差与收敛状态。
- **46.4.6 Named Expressions**：表达式表——定义、描述、使用位置；用于边界条件的表达式超链接跳到 Boundary Conditions 节。
- **46.4.7 Report Definitions**：报告定义表。
- **46.4.8 Plots**：Residuals 与 Report Plots。沿图拖动（竖/横）调坐标可视范围；对角拖动缩放。右上工具栏：**Download Plot as PNG**（默认存工作目录）、Zoom、Pan、Zoom in/out、Autoscale、Reset axes、**Show closest data on hover**、**Compare data on hover**。
- **46.4.9 图形对象**：Contours/Vectors/Pathlines/LICs/XY Plots/Scenes/Histograms/Animations 均可入报告；布局可 tabular（46.7.2）。**存为 AVZ/GLB 的图像可能比图形窗口暗——用 `display/set/picture/invert-normals-for-avz` 修正**。AVZ 动画以静态代理图表示——悬停出 play 按钮可在报告内直接播放。

## 46.5 保存（p. 4613）

**Export** 按钮存 **PDF 或 standalone HTML**；也可导出 **PowerPoint**（提供默认 Ansys 模板）。默认存工作目录，可自选位置——同仿真多变体可分别生成报告后查看分析。**注意：Linux 导出 PDF 须在支持 X11 应用的环境**（X11 server + 正确配置与认证的显示环境）。

## 46.6 其他选项（pp. 4613–4614）

**Options** 按钮：**View Report in Web Browser**（默认浏览器看所选报告）；**Delete Report**（删报告及关联图像文件）；**Duplicate Report Settings**（复制报告及自定义设置并载入 Outline，副本名 = 原名尾加 "1"；Current Report 下拉可回看历史报告及其副本）；**Reset to Default Settings**（恢复默认；任务页顶部亦有对应图标）。

## 46.7 定制（pp. 4614–4616）

- **46.7.1 Image Settings**：默认 **Object State View**（对应视图最近保存状态）；**X/Y Resolution** 控制图形采集分辨率（默认值同 Save Picture 对话框）；**Capture Current Resolution** 取当前图形窗口分辨率；勾 **Save Hardcopy** 额外存独立图像文件到工作目录。
- **46.7.2 Layout**：**Layout 字段**——tabs（默认，同类型多图分标签页）或 columns（表格并排同看，**Number of Columns 默认 1**）。可按类别（仅 contours 或仅 vectors 等）或全局（46.2.1）应用。
- **46.7.3 模板**：把报告配置（节点可用性、标题、图形、注释等）存为 **Fluent simulation report template（`*.fsrt`）** 文件复用；任务页上部两图标分别打开/保存模板。**注意：录制 journal 涉及报告时，Fluent 用本地存储的模板跟踪报告设置**。
- **46.7.4 添加额外图形**：默认定义之外的图形放入 **User Data** 节——①外部图像：Image Path + Image Name + Add Image；②仿真内图形：图形窗口布置好视图（网格显示、剖面等）→ 右键 **Add to Report** 捕获窗口内容；③User Data 下见新图像；④重新 Generate。
- **46.7.5 隐藏/显示节**：默认全部节包含（勾选框）；取消勾选后 Generate 即得精简报告。

## 46.8 TUI（p. 4616）

`/report/simulation-reports/` 菜单下若干命令（详见 report/ 命令参考）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1，Chapter 46（PDF pp. 4589–4616），批次 124（2026-10-22），SHA-256 校验一致。
- Figures 46.1–46.34 为图形示例（记录图形元素，未复制图像）；工具栏与字段名按原文照录；`Qt WebEnging` 为手册原文拼写（正确应为 Qt WebEngine），照录并标注。
- 功能细节（默认值、导出格式、限制）为 2026 R1 版本行为，跨版本可能变化；Linux/远程桌面相关限制按原文条件适用。
