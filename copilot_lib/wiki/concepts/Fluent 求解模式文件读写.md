---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - file-io
  - export
  - journal
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 求解模式文件读写

## 摘要

User's Guide 2026 R1 Part III / Chapter 3（PDF pp. 965–1054）规定 Solution Mode 的文件读写：读写快捷特性（含文件名自动编号）、case/data 与自动保存、轻量读、TSV/HTML 设置导出、profile/表格文件、边界条件 settings 文件、journal/transcript、各格式导入与解数据导出、瞬态自动导出、网格间解插值、FSI 数据映射、图片保存、`.fluent` 启动文件与 FMU 联合仿真。Ch.2 "Text User Interface"（pp. 963–964）与 Meshing 模式 1.5 节同文（Scheme 方言、分层菜单、输入可存文件编辑后回读），另见 [[Fluent 网格模式入门]]。

## 3.1 读写快捷特性（PDF pp. 966–971）

- 默认后缀自动追加/检测（`myfile` → `.cas.h5`）；Files of type 可选只 CFF 或全部格式；格式优先顺序由 Preferences 的 Default Format for I/O 或 `file/cff-files?` 控制。
- case/data/ray 文件默认二进制（更省更快；二进制不能像文本一样读编辑）；要文本必须先切 legacy 格式；读 case/data/mesh/PDF/ray 自动检测文本/二进制。
- **Recent file list**（File/Read 子菜单底部，默认 4 个）：从列表读 case 时只有"同基名且上次随 case 一起读/写"的 data 才跟随读入；**Launcher 的 recent list 只加载 case 不加载 data**；列表可能含不适合当前会话的文件（3D case 列在 2D 会话）。
- 压缩：`.Z`→zcat、`.gz`→gunzip、**`.bz2` 也支持**；Windows 只能读/写 gzip（`.Z` 写出不压缩）；**压缩 ray 文件不能读/写**（光线追踪信息无法正确访问）；CFF case/data 不做文件级压缩（后缀并入名字如 `.gz.cas.h5`），压缩仅 legacy（`file/cff-files? no`）。
- Tilde expansion（Linux：`~/`、`~user/`）。
- **文件名自动编号**（对自动化关键）：`%t` 时间步、`%f` 流时间（默认场宽 10、6 位小数；`%x.yf` 定制；`%-x.yf` 去前导零）、`%i` 迭代号、`%n` 图片文件序号（仅图片）；`%i/%t/%n` 默认场宽 4，可用 `%xi` 等定制；**稳态不要用 `%t`/`%f`（恒为 0）**。
- 覆盖确认关闭：Batch Options（印刷页码 p. 214）或 `file/confirm-overwrite?` no。

## 3.2 读网格（PDF pp. 971–972）

网格文件是 case 文件的子集；File/Read/Mesh... 或 Read/Case...。**已读入网格/算例后再读网格会弹 Read Mesh Options 对话框**：丢弃 case 读新网格、或替换现有网格；可启用 Show Scale Mesh Panel After Replacing Mesh（手册推荐）。CFF 查找顺序 `.msh.h5 → .msh.gz → .msh`（Select File 中只要所选文件存在就按所选执行）。legacy 读法（Files of type 选 All Mesh Files、`file/cff-files? no`、Preferences Legacy——**同时影响 case/data 的读写**）。并行分区 filter 见印刷页码 p. 4570。

## 3.3 Case/Data 与自动保存（PDF pp. 972–979）

- **CFF 选项**：压缩级别 `file/cff-options/compression-level`（0–9，默认 1；提级不一定减小文件）；I/O 模式 `file/cffio-options/io-mode`——HOST（host 进程串行；文件路径对 compute node 0 不可访问时的默认）、NODE0（node 0 串行；路径可访问时默认）、PARALLEL INDEPENDENT（MPI 独立）、PARALLEL COLLECTIVE（MPI 集体）；**并行 I/O 模式不支持压缩——切换时压缩自动置 0**；双精度求解器可用 `file→cffio-options→single-precision-data?` 减小 data 文件。
- **Important**：网格自适应后必须同时保存新 case 与 data（否则不对应；未存最新文件退出时会有警告）；**瞬态设定时间步长后读入含不同值的 data 文件会用 data 的值覆盖时间步长**。
- case 预览：Launcher 的 Case File Info 或 File>Read>Case/Mesh Info...（版本、精度、维度、单元/面/节点总数）。
- GUI 写 case 会把工作目录更新为写出位置（`file/write-case` 文本命令不更新；`pwd` 查看）。单精度版本写 case 时节点坐标默认双精度（保证读回 meshing mode 不丢精度），`file→single-precision-coordinates?` 可降。
- **legacy 格式**（2020 R1 前默认）：`file/cff-files? no`（当前会话）或 Preferences=Legacy（当前+未来）；**Important：wall/symmetry 等从单元中心插值到表面的计算值在 legacy 格式不保留**——无求解器的后处理（如 EnSight）无法正确插回；HDF 格式解决此问题。legacy 格式全集见印刷页码 p. 5919。
- **自动保存**（Autosave 对话框，经 Calculation Activities 的 Autosave Every → Edit...；印刷页码 p. 5404）：Save Data File Every 默认 0（不保存）；in-cylinder 可按 Time Steps 或 Crank Angles；Save Associated Case Files：Only if Modified / Each Time；**只存 data 用 TUI `file→auto-save→case-frequency→if-mesh-is-modified`**（强制仅网格修改时存 case——data 必须有匹配网格的 case 才能读）；Flow Time + Adaptive 时间推进可能因浮点比较产生重复文件；稳态按迭代、瞬态按时间步（显式格式按迭代）；**Retain Only the Most Recent Files** + Maximum Number of Data Files 限制数量（case 与 data 分别计数、到上限覆盖最早；启用时**内存中的 solution history 被丢弃并重置**）；文件名 = 根名 + 编号（迭代/时间步/流时间/曲轴角）+ 自动扩展名；**同时写一个 `.flprj` 项目文件**（含瞬态导出的时间值元数据，CFD-Post/EnSight 建议读它；自动导出与 autosave 同根名且 CFF 时元数据写入同一项目文件）；**默认路径 `./<filename>` = 当前会话工作目录；硬编码目录则固定存那里**；autosave 设置保存在内存并随 case 保存。

## 3.4 轻量读（PDF pp. 980–982）

大单元数算例可只读 case 设置不读网格数据（File/Read/Case/Mesh Lightweight...、Read Case 勾 Lightweight、`file→read-case-lightweight`）：推荐 Launcher 的 Pre/Post Only 或 `-post` + `-t1`（单进程省内存）；**2021 R1 之前生成的 CFF 文件可能异常，建议用新版本重建 case**。限制：不能操作网格、建非一致界面、跑计算、设除 adjoint/population balance 外的附加模块（GUI 置灰、`define/models/addon-module` 不可用）；可显示表面网格（首次按需加载较慢）与初始化（不生成数据）。写回**同名** case 快且省空间；新名则需复制网格数据（要内存/空间）。

## 3.5–3.6 设置导出与旧版文件（PDF pp. 982–983）

- **TSV/Text/HTML 设置导出**：右键 Outline View 分支——边界条件（phase 级除外）、named expressions、report definitions、后处理对象导出 **TSV**；Results 分支可导 HTML/TXT 以比较算例设置；Copy Settings 可粘贴到另一会话。
- Fluent/UNS 3/4 与 RAMPANT 2/3/4 case 可直接读：UNS→Pressure-Based；RAMPANT→Density-Based + Explicit；UNS 4/RAMPANT 4 data 可读。

## 3.7–3.8 Profile 与表格文件（PDF pp. 984–991）

- **Profile**：`.prof` / 瞬态 `.ttab` / CSV；同名 profile 覆盖旧的；**每会话最多 50 个 profile**。写出（Write Profile 对话框）：Define New Profiles（选面+变量；**Write Merge Profiles（≥2 面）把所选面合并为一组数据点写成 .csv**；选参考系）；Write Currently Defined Profiles + Select Profiles...。**限制：点 profile 的坐标变换仅支持笛卡尔参考系；矢量点场 profile 不支持变换到局部参考系**。周向平均 profile（启用 Turbo Models）：Mass/Area 平均、按 Mesh Density 或 Equal Distance 分布、Max Sample Points；X/Y/Z Velocity 自动转圆柱分量；输出 `.csv`（头部信息更多）或 legacy `.prof`；命令 `file/write-circumferential-averaged-profile`。
- **表格文件**（Table File Manager：User-Defined ribbon 或 File→Table File Manager...）：Matrix 表（tab/空格分隔；第 1 行表名 ≤128 字符无空格、第 2 行列名、第 3 行起数据——**预期几百点以内，因为读入后随 case 一起写出**；行尾不得有空格/tab；首/末行的插值量作为下/上界）；插值用二分 + 局部线性插值。**RGP 表**（真实气体属性，温度/压力函数）格式见 CFX-Solver Modeling Guide，使用见印刷页码 p. 1794。

## 3.9–3.11 边界条件 settings、边界网格、Scheme（PDF p. 992）

- **`file/write-settings` / `file/read-settings`**：把边界与 cell zone 条件、求解器与模型设置写成"case 的 zone 节格式"文件；读入按 **zone 名匹配**，无匹配则忽略该组条件；拓扑变化后检查变化区域的边界（wall 尤其）；未检查且未初始化则算例无法运行；不用 read-settings 时导入网格取全默认设置。**zone 名可加通配符**（编辑 settings 文件把 `wall-12` 改成 `wall-*` 可命中 wall-12/15/17）。**Note：settings 文件只含用户改过的设置，不含默认参数——跨版本复用同一 settings 文件不保证相同设置（默认参数随版本变），可能造成解差异。**
- File/Write/Boundary Mesh...：把表面网格写出供 meshing mode 生成体网格。
- Scheme 源文件三种加载法（Read Scheme/`(load "file.scm")`；Read Journal/`.`/`source`）同 [[Fluent 网格模式文件读写与导入]]。

## 3.12–3.13 Journal 与 Transcript（PDF pp. 992–996）

与 Meshing 模式 journal/transcript 语义一致（见 [[Fluent 网格模式文件读写与导入]]），Solution Mode 补充：

- **录制精度影响回放**：单精度录制的 journal 读入双精度会话（或反之）可能受影响。
- 记录示例：`mesh/smooth-mesh , 5 ,`（逗号/Enter = 默认值）记录为 `/mesh/smooth-mesh "quality based" 5 0.1`；`so set ur mom 0.2 pres 0.4` 记录为两条 `/solve/set/under-relaxation/...` 命令；只记录成功完成的命令；GUI 事件先于进行中的文本命令记录；默认值全部记录。
- Transcript 额外记录**每迭代墙钟时间**与所用图形驱动；自动命名 `fluent-YYYYMMDD-HHMMSS-<processID>.trn`。

## 3.14 导入（PDF pp. 996–1004）

支持：ABAQUS（.inp/.fil/.odb）、CFX（.def/.res）、CGNS、EnSight（.encas/.case）、GAMBIT、HYPERMESH ASCII（.hm/.hma/.hmascii）、Mechanical APDL（.inp/.cdb/.rst/.rmg）、NASTRAN Bulkdata（.nas*/.dat*/.bdf*）与 Op2、PLOT3D（.p3d/.bin/.x/.xyz/.grd）、Tecplot（.plt，7.1–11.2，**11.0 不支持**；只读网格）、TurboGrid（.gtm）、METIS 分区、CHEMKIN mechanism。**带 \* 的需 VKI 许可证**（ABAQUS、CGNS、EnSight、HYPERMESH、APDL、NASTRAN、PLOT3D、Tecplot）。**导入任何第三方文件后应确认边界/单元 zone 设置符合预期**。要点：

- **ABAQUS ODB：2026 R1 因安全问题未含导入库，需联系支持**；.inp 只产生 FE 模型 dataset（无结果）。
- CFX：仅 3D；Create Zones from CCL Physics Data 选项。
- CGNS：Mesh / Mesh & Data / Data 三种；**不能导入 2D 多面体表面数据；不能导入 CGNS Structured Zones 上的数据**；变量映射表（pressure↔Pressure、u/v/w-velocity↔VelocityX/Y/Z、uu-stress↔ReynoldsStressXX、k↔TurbulentEnergyKinetic、epsilon↔TurbulentDissipation、omega↔TurbulentDissipationRate、temperature↔Temperature）；**正确流程：先只导网格并改好边界类型（如 outlet→pressure-outlet）与模型（读 CGNS 网格后默认 Laminar），再导数据（选择性导入）**；新旧网格 zone 须相同且同序；（Linux）`LC_NUMERIC`/`LC_ALL` 须未设或 en_US。
- EnSight：只读网格、数据丢弃。

## 3.15–3.16 导出解数据（PDF pp. 1004–1021）

格式：ABAQUS、Mechanical APDL Input（.cdb，ASCII）、ASCII、AVS、CDAT、CGNS、CFF-Post、EnSight Case Gold、EnSight DVS、Data Explorer、FAST、FIELDVIEW、I-deas、NASTRAN、PATRAN、TAITherm、Tecplot（第三方版本见 Table 1.2）。共性限制：

- **并行导出**仅限 ABAQUS、CDAT、ASCII、CGNS、CFF-Post、EnSight Case Gold、EnSight DVS、Fieldview Unstructured、APDL Input、NASTRAN、TAITherm（仅表面）、Tecplot；由 host 进程写——**写文件所需内存可能超过 host 可用内存**；串行 TAITherm 仅表面。
- solution mode 不能导入表面（meshing mode 可以）；VKI 许可证：ABAQUS、CGNS、I-deas、NASTRAN、PATRAN、Tecplot；多瞬态算例的导出文件成组使用须**同平台同进程数**；**用户自定义表面不可导出 EnSight Case Gold**；（Windows）CGNS >2GB 不可导出（用 Linux）。
- NASTRAN/ABAQUS/APDL/I-deas/PATRAN 导出量：节点/单元、节点集（边界条件）、温度、压力、热流、换热系数、力（面力 = 压力+粘性+表面张力，按共享节点数分摊到节点）。
- **EnSight DVS 自动导出开始后不能创建/删除 report definitions**（EnSight 需要完整残差与报告历史）。

各格式要点：ABAQUS/APDL 载荷分 Structural（Force/Pressure/Temperature）与 Thermal（Temperature/Heat Flux/HTC），能量方程关闭时只有前两者，整域导出时载荷只写边界 wall；**ABAQUS 导出仅对固体 zone 或固-固交界有效，温度全域导出**。ASCII：Location Node/Cell Center、逗号/空格分隔。**CDAT**：`.dat.h5` 是原始数据，CFD-Post/EnSight 显示可能与 Fluent 内不一致；`.cdat` 在导出前处理数据以减少不一致；**只含节点值（即使面 zone）**；必须同时选中创建 isosurface/clipped surface 所用的变量否则表面无法重建；同时写 legacy `.cas` 与 `.cst` 状态文件（CFD-Post 加载 .cst 前须先加载 .cas 与 .cdat）；结构模型算例不可用。**CGNS**：HDF5/ADF；`file/export/settings/` 微调（cgns-mesh-type 1 Mixed/2 Native/3 Polyhedral——**native 通常最小**；cgns-familyname；cgns-merge-ngons-to-single-ngon；cgns-separate-cellzones——仅保形 zone；**周期边界须先 `mesh/modify-zones/slit-periodic`**）；**zone 名 >30 字符截断并加 zone ID（CGNS 标准）**。**CFF-Post**：不同表面/zone 可导**不同**量（壁面剪应力 + 出口压力）；写 `<name>.cas.post` + `<name>.dat.post`；只含节点值（cve 标记的单元量除外）；**混合 Windows/Linux 须在启动时指定远程工作目录**（Launcher Remote Working Directory、`-nodehomedir=`、`NODEHOMEDIR=`）。**EnSight Case Gold**：瞬态多文件用 `file→transient-export→ensight-gold-from-existing-files`（base name 或文件列表、Skip、Cell-Centered、每时间步单独文件、二进制、频率、静态网格 case 命名规则、读 case、zone/标量列表）；产物 `.geo/.vel/.sclN/.encas`；**非静止参考系的速度按所选参考系相对导出**；导入 ParaView 等第三方需无 ID 0 表面。FAST 仅三角形/四面体。**FieldView Unstructured**：`.fvuns` + `.fvreg`（体数据按绝对参考系写）；同网格多稳态解只导数据用 `file/export/fieldview-unstruct-data`/`-surfaces 2`。**TAITherm**：仅能量方程启用时；多面体只导边界；HTC 选 Flux Based 或 Wall Function based（无湍流模型时 wall-function HTC = k/h，k 导热率、h 贴壁单元高度）；输出 PATRAN neutral `.neu`；wall/shadow 对只写原 wall。Tecplot：无面选择→全域单元中心；**fe2ram 只能导入 FEPOINT 格式 Tecplot**。

## 3.17–3.20 颗粒历史与瞬态自动导出（PDF pp. 1021–1030）

- **稳态颗粒历史**（File/Export/Particle History Data...）：类型 CFD-Post/FieldView/EnSight/Geometry（.ibl——**非定常颗粒追踪启用时不可用**）；导 EnSight 前须已用 Solution Data 导出生成 `.encas`；Particle Residence Time 不在变量列表但**总是导出**；Skip 减轨迹数、Coarsen 减点数（仅稳态）；EnSight 的 .encas 被改写重命名为 `root.new.encas`（读新文件）；输出 `.mpg` + `.mscl`。
- **瞬态自动导出**（Calculation Activities task page → Create → Solution Data Export... / Particle History Data Export...）：Export Data Every 按 Time Steps 或 Flow Time（颗粒另可按 DPM Iteration）；EnSight Case Gold 的 Separate Files for Each Time Step 默认启用且推荐（中断不丢全部数据；**EnSight 不支持 Append File Name with——启用时总附加时间步号**）；CDAT 可选 Only if Case/Mesh Changes 省空间；颗粒文本命令 `file/transient-export/particle-history-data` 另有 geometry（.ibl）与 history（`.dpmhist` ASCII 表）类型；**颗粒导 EnSight 须同时设置 solution data 的 EnSight 自动导出且 Separate Files 设置一致**；FieldView 每时间步单独文件用 `%t`；**EnSight 不支持瞬态计算中新增 cell zone/surface（如 in-cylinder）的导出**。
- **Export to CFD-Post**：默认 Open CFD-Post（自动打开并加载显示）；**仅当 mesh/case 变化时才保存新 case（省空间）；CFD-Post 读取拓扑变化/增删 zone 的瞬态算例可能困难**。
- **并行 EnSight 导出**：仅并行 Fluent；Export 对话框勾 EnSight Parallel；**Cell Zones 与 Surfaces 二选一**。

## 3.21–3.23 解文件管理、插值与 FSI 映射（PDF pp. 1030–1040）

- **Solution Files 对话框**（File → Solution Files...）：列出自动保存文件，Read 设为 current（多选禁用；**设较早解为 current 后继续计算会移除更晚文件**）；Delete（当前加载的不可删）；File Names... 看路径；Workbench 下 Recover Missing Solution... 从 `dp0\FFF|FLU\Fluent` 恢复。
- **网格间解插值**（File → Interpolate...；**零阶插值**）：Write Data（Cell Zones——**流体与固体 zone 数据分文件写**；Binary 更快更省内存）→ 新 case（读新网格、**启用原 case 全部模型**——漏开能量方程则温度不插值；可用原模型 `write-settings` + 新网格 `read-settings` 复用边界）→ Read and Interpolate（未初始化时默认全选 zones；流/固需执行两次）→ **先调低欠松弛算几步避免插值后通量失衡，再恢复正常**。插值文件格式：行 1 版本（2/3/4/5，对应 12.0–14.0 文本、14.5 文本、14.5 单精度二进制、14.5 双精度二进制）、行 2 维度、行 3 点数、行 4 场数、场名、坐标、场值；v3 用 `( )` 定界、v4/5 用 `( \nEnd of Binary Section 0)`——**定界符用于跳过未启用模型的节；v2 无定界符可能跳节失败导致后续场错插**；**14.5+ 写的文件不能被更早版本读取**。
- **FSI 数据映射**（File/FSI Mapping/Volume 或 Surface；**零阶插值**）：把 Fluent 单元/面数据映射到 FEA 网格（ABAQUS .inp / NASTRAN .bdf，输入输出类型可不同）；输入网格须与 Fluent 对应区域空间重合（Length Units 缩放）；**仅 3D；输入可以是部分模型但节点/单元编号须与最终 FEA 文件一致**；输入文件仅保留在内存直到写出或关对话框；**体数据只能映射 Temperature；表面可映射 Force/Pressure/Temperature（结构）或 Temperature/Heat Flux/HTC（热）；映射温度或热分析变量须启用能量方程**；Surface 对话框**默认全选所有 wall（含 shadow）——wall/shadow 对须只选正确一侧；inlet zone 无 HTC 数据**；Include FEA Mesh 默认关；Temperature Units（K/C/F）；HTC Type：ref-temp / cell-temp / wall-func-htc。

## 3.24–3.27 图片、附加量、.fluent、FMU（PDF pp. 1040–1054）

- **保存图片**：与 Meshing 模式同基础（cortex 最佳实践四条相同）；格式更多：EPS/JPEG/PPM/PostScript/TIFF/PNG/HSF/**AVZ**/**GLB**/**USD**/VRML/Window Dump；Raytracer Image 可选。**AVZ 限制**：反射/地面网格不导出、可能变暗（`display/set/picture/invert-normals-for-avz` 纠正）、仅面与边、Node Values 禁用时等值线值可能错、等值线线不导出、**2D 图（report plots/残差/XY）不能存 AVZ**、多 colormap 场景可能重叠（先拖动重排）、按材料着色的 mesh 渲染不正确等。**GLB**：VR/AR 二进制 glTF；不能存动画；只能 faces 或 faces+edges。**USD**（NVIDIA Omniverse）：**保存路径不能含空格**；不能存动画；线以 3D 圆柱表示（粗细由 Preferences 的 Line width 控制：正数按比例、负数固定）。**Gray Scale 在 Windows DX11 驱动不支持**（切 `display/set/rendering-options/driver opengl2`）；Monochrome 预览的灰色保存后为黑色；White Background 在 Dark theme/自定义背景下保持图像一致；HSF 动画高压缩（iOS/Android HOOPS Viewer）；PPM 序列 + ImageMagick `convert -adjoin` 可拼 GIF；PostScript 快打印选项在 `display/set/picture/driver/post-format`（fast-raster/raster/rle-raster 默认/vector）。
- **Data File Quantities**（legacy data 附加量）：标准量不可取消；**EnSight 建议改用 EnSight Case Gold/CFF-Post 导出**；**CFD-Post：附加量列表中与标准量同名的应选附加量（要求特定推导形式）；并非所有标准量在 CFD-Post 可用（如 Mach number）**；附加量选择随 legacy case 保存。
- **`.fluent` 文件**：启动时从 home 目录 Scheme load；可含 Scheme 函数与 TUI 命令（`(ti-menu-load-string "file read-case test.cas.h5")`）；**与 `.tgrid` 并存时 solution mode 先加载 `.tgrid` 再加载 `.fluent`（故 solution mode 中 `.fluent` 优先）；从 meshing 切到 solution 不会自动重新加载 `.fluent`**——与 meshing mode 的加载顺序（`.fluent` 先、`.tgrid` 后）互补。
- **FMU 联合仿真**（FMI 2.0）：**仅 co-simulation 型 FMU、仅压力基求解器、只能导入一个 FMU**；重启仅当 FMU 支持（case 须存默认 .h5）；导入（File/Import/FMU...）后自动识别 FMU 输出变量并建同名 Fluent 输入参数；**FMU 输入变量须钩到 Fluent 输出参数**（可事后补建）；可选修改 FMU 参数值（参数研究须每次重访对话框）；可选监视 FMU 局部变量（自动建同名输入参数供 report definitions）；**输入参数与用途的单位须一致**（不一致可建缩放参数或表达式）；初始化时创建 FMU 实例；**非定常首次迭代调用 FMU、定常每迭代调用**；重跑已有 case：FMU 文件须在同目录或原绝对路径。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part III / Chapter 2（pp. 963–964）与 Chapter 3（pp. 965–1054）；两章目录范围至此完成。Figures 3.1–3.23 为图形元素，仅文字机制被摄取。
- **TAITherm wall-function HTC 的公式在文本提取中缺失**（正文与 Note 分别描述"k 为导热率、h 为贴壁单元高度"的构成），公式本体未摄取、未推断。
- 命令、默认值（压缩级别 1、profile 上限 50、`%f` 场宽 10/6 位等）对应 2026 R1；跨版本行为（settings 文件、插值文件版本、2021 R1 前轻量读）为手册明确陈述的版本敏感信息。
- 印刷页码引用（p. 5919 legacy 格式全集、p. 4361 输出参数、p. 4570 分区、p. 5402 Calculation Activities 等）指向未摄取章节，仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 求解模式 GUI]]（Select File 对话框、Lightweight 入口）
- [[Fluent 网格模式文件读写与导入]]（journal/transcript 通用语义、CFF 开关）
- [[Fluent 启动与批处理自动化]]（批处理、检查点触发、远程工作目录选项）
- [[Fluent 网格文件格式（legacy .msh）]]（legacy mesh 格式；case 格式另见 Part III 附录 B）
- [[Fluent 第三方网格导入与 fe2ram 过滤器]]（fe2ram 与 Tecplot FEPOINT）
- [[index]]
