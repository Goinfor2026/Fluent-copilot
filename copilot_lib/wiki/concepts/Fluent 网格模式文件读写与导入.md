---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - file-io
  - journal
  - cad-import
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 网格模式文件读写与导入

## 摘要

User's Guide 2026 R1 Part II / Chapter 1 的 1.6 节（PDF pp. 258–284）规定 Meshing Mode 下各类文件的读写：mesh/case/size-field/journal/transcript/domain 文件与外部格式导入（含 CAD）。对自动化最重要的规则集中在 Journal 的"记录/回放无状态"语义、`/file/set-tui-version` 版本固定、CFF 与 legacy 格式开关，以及 CAD 导入的命名/单位规则。

## 1.6.1 读写快捷特性（PDF pp. 258–260）

- **二进制文件**：mesh、case、size-field 默认写为二进制（比文本更省内存、读写更快）；要存文本需在 Select File 对话框关闭 Write Binary Files。
- **压缩文件**：读 `.z` 自动调 zcat、读 `.gz` 自动调 gunzip（经操作系统管道导入）；TUI 读压缩文件只需输入文件名（先按原名查找）。写压缩文件在文件名后加 `.z`/`.gz`（`.msh` 等扩展名自动补齐）。**Windows 只支持 gzip**：`.z` 文件既不能读、加 `.z` 写出也不压缩。Case 文件的默认 CFF 格式**不适用**这种压缩，`.z/.gz` 只是并入文件名（如 `.gz.cas.h5`）；真正的压缩只用于 legacy 格式（`file/cff-files? no` 后）。
- **波浪号展开（仅 Linux）**：`~/` 展开为主目录，`~username/` 展开为对应用户主目录。
- **关闭覆盖确认**：`file/confirm-overwrite?` 答 `no`。默认写重名文件会询问 "OK to overwrite"。

## 1.6.2 Mesh 文件（PDF pp. 260–265）

- **定义**：网格文件由 Ansys Meshing、Fluent meshing mode、GAMBIT、GeoMesh、PreBFC 或第三方 CAD 包生成；是 case 文件的子集——含节点坐标、连接性、面 zone 的类型与编号，**不含边界条件和流动参数**。case 读入命令也可读网格文件；反之把 case 当 mesh 读会丢失边界条件数据。
- **扩展名与查找顺序**：默认保存为 `.msh.h5`（自动追加）。`file/read-mesh` 按"原名 → 加 `.msh.h5` → 加 `.msh`"顺序查找。
- **读入**：File → Read → Mesh...；也支持把文件直接拖入 Fluent 会话；读入时一并读取 boundary layer flags（供之后 append 时识别 prism 单元）。默认格式为基于 HDF5 的 Common Fluids Format（CFF）；CFF/HDF 恒为二进制且自带压缩，不能用文本编辑器查看（可用第三方 HDF 工具探索）。当前会话读 legacy `.msh`：`file/cff-files? no`；后续会话：Preferences（General）→ Default Format for I/O 选 Legacy。含多面体单元的 case 可在 meshing mode 读取（显示、部分操作、质量检查）。
- **限制**：经 hanging-node 自适应求解器输出的网格**不能读入**；须先在求解器中粗化回原始未自适应网格。
- **`/file/read-options` 两个选项**：
  - Enforce mesh topology（默认关）：读取时一致定向 face zone；必要时分离 zone，使每个边界 face zone 至多邻接两个 cell zone；相邻 cell zone 间插入 internal face zone。
  - Check read data（默认关）：读时校验网格拓扑，遇错误发警告并删除错误实体；**不做自动修复**，可能留下非保形/空洞/错误部分；其用途是允许读取损坏文件，默认关闭以缩短读取时间。（[[Fluent 2026 R1 已知限制]]中"旧版 interior zone 修复"条目引用同一菜单，且菜单原文转录为 `Check read deata`。）
- **多文件**：两个以上文件构成的网格可一次多选读入拼成完整网格（如三角边界网格 + 六面体网格的 hybrid），也可逐个 Append（见下）；在 3D 版本中读 2D 网格用 File → Import → Fluent 2D Mesh...。
- **Append（追加）**：先正常读第一个文件，之后在 Select File 勾选 Append File(s) 逐个追加（首读时 Append 选项不可用）。无 GUI 对应的文本命令：`/file/append-meshes-by-tmerge`（用 tmerge 工具）。追加规则：重名的 zone/domain/refinement region 的名称与 ID 会被修改并在 console 报告；edge-face zone 关联、zone 级 prism 参数、boundary layer flag、节点曲率数据均保留；boundary layer 单元/面计数在 append 时报告（poly-prism 计数进入网格统计摘要）。
- **写出**：File → Write → Mesh...（默认 CFF `.msh.h5`；legacy 开关同上；Files of type 默认扩展名由偏好决定，可只输基名）。`/file/write-options` 的 enforce mesh topology 对写出同样生效。手册建议**写出前先删除 dead zones**。
- **边界网格**：读：File → Read → Boundary Mesh...（适合从大体网格文件中复用边界网格；同样支持多文件拼装）。`.tgf` 面离散几何（Workbench 导出）可用 Read Mesh 或 Read Boundary Mesh 读入；face zone 命名可由 Workbench Named Selection 控制。写：File → Write → Boundaries... 只输出选定边界 zone——用于把大算例分块在独立会话中做体网格再 Append 合并，避免频繁切换 domain。

## 1.6.3 Case 文件（PDF pp. 265–268）

- Case 文件含网格、边界/单元区条件、求解参数以及界面与图形环境信息；可读文本/二进制、压缩/未压缩格式，读取时自动判别。
- **重要规则**：在 meshing mode 修改 thread（zone）ID 可能影响 case 设置，操作时会有确认提示；**在 meshing mode 读过并重写的 case 与旧存的数据文件不兼容**——转入 solution mode 时不得同时读旧 data 文件；meshing mode 操作改变了 zone 拓扑时，转入 solution 后必须核对 case 设置。
- 在 solution mode 自适应过的 case 读入 meshing mode 会**丢失 cell hierarchy**；非一致界面 case 读入 meshing 再切回 solution 的限制（手册 Note）：zone ID 可对上但名称可能不一致；相交 thread 上的边界条件不保留；未关联（dangling）NCI 表面仍存在。
- 读/写：File → Read/Write → Case...；默认 CFF（`.cas.h5`）；legacy 用当前会话开关 `file/cff-files? no` 或 Preferences 的 Default Format for I/O；写 hexcore 网格时可勾选 **Write As Polyhedra**（把 hanging-node 细分内及 hex-tet 交界处的 hex 转为多面体单元输出，避免非一致网格导出；转换后仅能做显示、部分操作与质量检查，不能再深入编辑）。写出前同样建议删除 dead zones。

## 1.6.4–1.6.5 Size-Field 与 Scheme 源文件（PDF p. 268）

- Size-field 文件保存按参数定义的 size function；File → Read/Write → Size Field...。缩放模型后读 size-field 时，须确保 size-field 顶点与缩放后的模型一致。
- Scheme 源文件三种加载法：File → Read → Scheme... 或 `(load "file.scm")`（大文件适用）；File → Read → Journal... 或 `file/read-journal`；短文件也可用别名 `.` 或 `source`——按字符逐条回显，如同键入。

## 1.6.6 Journal 文件（PDF pp. 268–270）

Journal 是 Fluent 命令序列的记录/回放文件：界面命令记录为 Scheme 代码行；可用文本编辑器手写，注释行以 `;` 开头。读取时每行回显到标准输出，读完控制权交回键盘。

手册强调的核心语义（Important）：

- **journal 不含状态信息**——不记录录制时或回放时的程序状态。录制时不要切换工作目录；回放前应尽量重建录制时的前置状态。典型失败案例：journal 里的写文件指令遇到磁盘上已有同名文件时触发覆盖确认，而 journal 中无应答 → **Fluent 无法继续执行**。前置依赖同理：如 journal 显示表面，必须先读入相应网格。
- **版本固定**：每次开始录制，文件顶部自动加 `/file/set-tui-version "XX.X"`；它使旧版 journal 在新版中正常工作（隐藏新增 TUI 提示、恢复被删提示）。手写在编辑器中的 journal 也建议加此行。限制：**指定版本必须在运行版本前后两个完整 release 之内**；2026 R1 对应 `"26.1"`。
- **录制规则**：命令即使以部分字符串键入也记录完整形式；只记录成功完成的命令（Ctrl+C 中断的不记录）；文本命令执行期间发生的界面事件会被**先**记录；所有默认值都被记录。
- **并发与嵌套**：同一时刻只能有一个 journal 在录制；任何时候都可读取 journal；journal 与 transcript 可同时写；一次可按选择顺序读多个 journal；journal 可嵌套调用其他 journal（`/file/read-journal "路径" ""`）。
- 操作：File → Write → Start Journal...（菜单项变为 Stop Journal，停止或退出程序时结束）；File → Read → Journal...。**journal 总是在主（顶层）文本菜单加载**，无论发出命令时处于菜单层级何处。

## 1.6.7 Transcript 文件（PDF pp. 270–271）

Transcript 记录会话的全部标准输入/输出（键盘与界面输入、屏幕输出）及会话开始/结束/总时长；界面命令同样记录为 Scheme 行。**不能读回程序**（含消息与输出文本）。

- 自动记录：Preferences → General → Automatic Transcript，每次启动新会话自动生成，命名格式 `fluent-YYYYMMDD-HHMMSS-<processID>.trn`；保存到可写的工作目录，否则临时目录（绝对路径打印在 Console）。
- 同一时刻只能开一个 transcript 录制（启用 Automatic Transcript 时仍可另建一个）；可与 journal 同时写；录制 transcript 期间可读 journal。手动：File → Write → Start/Stop Transcript...。

## 1.6.8 Domain 文件（PDF p. 271）

完整网格可有多个 domain（各含节点、面、cell zone ID 列表）；mesh 文件内已含 domain 信息一节，domain 文件则单独写出全部 domain 信息。命名约定后缀 `.dom`（读写自动补加，读取时先找原名再找 `.dom`）。File → Read/Write → Domains...；读入已存在的 domain 会警告；Fluent 会校验定义 domain 的 zone 是否存在于网格。

## 1.6.9 导入外部文件（PDF pp. 271–272）

File → Import 子菜单（或对应文本命令）支持：ANSYS Prep7/cdb、CGNS、GAMBIT neutral、HYPERMESH ASCII、NASTRAN 文件（格式与无导入命令时的转换见 Appendix A，印刷页码 p. 869）。**许可证注意**：与 solution mode 相同，导入 Prep7/cdb 和 CGNS 使用 VKI 库、需 VKI 许可证；过旧的 cdb 版本（如 5.5）不被 VKI 支持，须用最新版重新生成。支持多选导入与 Append 外部文件（先读/导一个，再勾选 Append File(s) 导入其余，需选格式与 surface/volume 类型）。

### 1.6.9.1 导入 CAD 文件（PDF pp. 272–279）

经 CAD reader 或关联几何接口（plug-in）导入；File → Import → CAD... 打开 Import CAD Geometry 对话框。

- **基本选项**：默认单文件导入；关闭 Import Single File 后按 Directory + Pattern 多选。路径分隔符须平台正确；文件名支持的特殊字符：Windows `– + $ ^ ( ) [ ] { } @ # % _ - = , . ; ' ~ ` !`，Linux 另含 `: > “`。勾选 Append 可把 CAD 数据追加到既有模型/网格（仅在已读入模型后可用）。
- **单位**：导入时按选定长度单位缩放（默认 mm）。**重要**：缩放只作用于 meshing mode 会话；转入 solution mode 后模型单位**还原为原始 CAD 单位**；solution mode 缩放另见 Scaling the Mesh（印刷页码 p. 1332）。
- **Tessellation 两种模式**：
  - **CAD Faceting** → 导入产生 Geometry Objects。可勾选 Refine Faceting 并设 Tolerance（默认 0 = 不精化）与 Max Size（限制过大面片）；手册建议：首用 Tolerance=0 做诊断性导入，再以预期最小尺寸的 1/10 重导。Merge Nodes（选 CAD Faceting 时默认开）合并几何对象节点——若因此导致面片节点上的尺寸计算不合预期，关闭后重导。
  - **CFD Surface Mesh** → 导入产生（保形的）Mesh Objects。须指定 Min Size、Max Size（上限为包围盒对角线的 1/10）、Growth Rate；Size Functions 默认 Curvature（按 Curvature Normal Angle 细化），可加 Proximity（按每间隙单元数，可为 ≥0.1 的实数，可作用于边/面/边+面）；Auto-Create Scoped Sizing 默认开（对导入期间新建对象自动建 scoped sizing）；可按参数保存 size-field 文件并在下次导入复用（Use Size Field File，注意单位匹配）。mesh 对象节点在此模式下**总是合并**；表面网格失败的面会被分入带 "failed" 标识的独立 face zone；ICEM CFD（`.tin`）不支持 CFD Surface Mesh 选项。
- **CAD Options 对话框要点**：
  - 可递归读取子目录；仅线体/导线（edge zone）的 CAD 文件不能导入。
  - 可保存中间 PMDB 文件（每个 CAD 文件一份 `.pmdb`），换选项重导同一 CAD 时更快。
  - Named Selections 处理：支持 Ansys Discovery、DesignModeler、CATIA 出版物等；可用 `/file/import/cad-options/named-selections` 按模式/通配符忽略导入；**Ansys Meshing 定义的 Named Selection 不能导入**。
  - **命名规则**：CAD 名默认保留；对象/zone 名合法字符 = 字母数字 + `_ + - : .`，其余（含空格和斜杠 `/`）导入时替换为连字符 `-`；body/部分/文件/NS 名以数字或（除 `_ :` 外的）特殊字符开头时加 `zone` 前缀（例：`.test.agdb` → `zone.test`）；表面体对象名加 `-sheet` 后缀（用 One Object per part 导入时除外）。
  - 节点曲率数据默认导入（可关）；特征提取默认开（Feature Angle 默认 40）。
  - **对象创建粒度**：勾选 Create CAD Assemblies 生成 CAD Assemblies 树（保留原 CAD 子装配层级，详见 CAD Assemblies，印刷页码 p. 605）。对象粒度：每 body / 每 part / 每 CAD 文件 / 每选择 / program-controlled（默认；按共享拓扑 off→per body、on→per part 自动选择）；zone 粒度：每 body（默认）/ 每面 / 每对象。ICEM `.tin` 须设每选择一个对象。导入多体 part 时建议每 part 或每 file 一个对象且 Tessellation 用 CFD Surface Mesh 以保留拓扑；对象定义上不共享 face/edge zone——选每 body / 每选择粒度时公共面/边 zone 会被**复制**使对象相互独立。
  - 其他文本命令级选项：出错仍继续导入；导入 part/body 名；从 DesignModeler（`.agdb`）导入 enclosure 与 symmetry 命名选择；按角度/连接性/命名选择分离特征边（边 zone 名加相应后缀）；组件名默认加入对象/zone 名；part 名添加默认 auto（粒度=body 时加入对象与 zone 名，粒度=part/file 时不加入 zone 名/面区标签/区域名，可显式 yes/no）；无 Named Selection 的 zone 默认不继承对象名；NS 默认按粒度用作对象/zone 名，跨多 part/body 的 NS 默认以 part/body 名作后缀；每 file 一对象时 NS 默认不参与（`use-collection-names?` 可改）；CFD Surface Mesh 下 NS 可导入为 face zone 标签；可为单边连接面/多边连接面/共享面加标签；默认保留扩展名与路径前缀于名字（路径前缀 auto=每 file 粒度时移除）；重名对象/zone 默认不加递增整数后缀（可开）。
  - 注意：压缩的 CAD 文件（`.stl.zip/.stl.gz/.stl.bz2`）不能导入；DOS 8.3 短路径名不能导入（用完整路径）；Ansys Mechanical/Meshing 中定义的 virtual topology、被抑制/改名的 part/body 在 CAD 导入时被忽略；导入 BladeBuilder 创建的 DesignModeler 几何前须把 Geometry 许可证偏好列为 BladeBuilder（Workbench Tools > License Preferences > Geometry 移到首位）；Linux 的 CATIA V5 Reader 不提供体层级（树中只出现最底层 child 标签）；平台支持的 CAD 包列表见 Ansys Help 的 CAD Integration。
- **问题 CAD 几何（如绕中心点密绕的线圈）**：此类几何表面面积与包围盒对角线平方之比远大于 1，且两点投影有歧义（参数空间无关方法对多数模型最稳健，此处失效），不易在 Fluent Meshing 中划分。手册变通：用一平面把体表面切成上下两半再导入——体积保持单一，投影歧义消失，可获得正确网格（Figure 1.21/1.22 为图形示意）。

## 1.6.10 保存图片文件（PDF pp. 279–283）

- 支持格式：EPS、JPEG、PPM、PostScript、TIFF、PNG、HSF、GLB、VRML，及 Window Dump（仅 Linux）。保存图与窗口显示可能有细微差异（内部软件渲染器 vs 硬件加速）；消除差异并最快保存的四项 best practice 与 [[Fluent 2026 R1 已知限制]]图形条目一致：cortex 放合适机器/显卡/驱动（`-gui_machine=<hostname>` 或 Launcher Scheduler 页 Specify Machine）、cortex/host 与 compute node 0 分机（勿让 `-gui_machine` 机器占 `-cnf=x` 首位）、图形驱动勿设 null/x11/msw、保存图启用 Preferences（Graphics）Fast hardcopy。Window dump 最快且与窗口完全一致。
- Save Picture 对话框流程：选格式 → 设着色 → 文件类型（PostScript/EPS 可选 Raster/Vector）→ 分辨率（raster 按 Width/Height 像素，0/0=活动窗口分辨率；PostScript/EPS 按 DPI）→ 选项（Landscape 默认开、White Background 默认开）→（Window Dump 时）填 dump 命令 → Preview（可选）→ Save。点 Apply 只保存设置作为后续默认。
- 细节：EPS = PostScript + Adobe DSC v2 声明，当前不含预览位图；单色打印设备会把彩色渲染成灰度，选 Gray Scale 可保证线性灰度渐变；VRML 导出三维几何实体（文本、标题、色标、方位轴及光照/着色/透明/可见性等显示特性不导出，由查看软件控制）。快速打印 PostScript 的选项在 `display/set/picture/driver/post-format`。
- **Window Dump（Linux）**：命令如 `xwd -id %w > 文件`，`%w` 自动替换为活动窗口 ID；动画用 `%n` 递增编号（如 `myfile%n.xwd`，无需手动编号）；ImageMagick 用 `import -window %w` 输出 `.miff`（动画更高效）；功能与系统/图形驱动相关；Window Dump 格式下对话框中控制分辨率/颜色/透明的输入被禁用（所见即所得）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Chapter 1 之 1.6 节，PDF pp. 258–284（p. 258 上半为 1.5 与章头，已归 [[Fluent 网格模式入门]]；p. 284 仅版权页脚，无正文）。Figure 1.21/1.22 为图形元素，仅文字机制被摄取。
- 印刷页码引用（p. 869 附录 A、p. 1332 Scaling the Mesh、p. 615 Proximity、p. 605 CAD Assemblies 等）指向尚未摄取章节，仅作定位，其内容未经本库核实。
- p. 281 的格式列表在文本提取中夹带脚注标记导致轻微错乱；格式名单以 p. 279 正文列表为准（两处内容一致），未据 p. 281 的乱序文本推断。
- 命令、默认值与平台支持随版本变化；本页对应 2026 R1。Journal 版本窗口（两个完整 release）与 `"26.1"` 为手册明确陈述。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 网格模式入门]]（同章 1.1–1.5）
- [[Fluent 启动与批处理自动化]]（solution mode 侧的 journal/批处理与检查点触发文件）
- [[Fluent 2026 R1 已知限制]]（journal/workflow 旧文件、CFF 写出、图形驱动等条目）
- [[Fluent 网格质量诊断]]
- [[index]]
