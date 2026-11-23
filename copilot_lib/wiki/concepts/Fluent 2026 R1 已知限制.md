---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - limitations
  - workarounds
  - 2026R1
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 2026 R1 已知限制

## 摘要

User's Guide 2026 R1 第 1.3 节（PDF pp. 155–174）按类别列出 Ansys Fluent 的已知限制，多数条目附 Ansys 缺陷编号和变通方法。本页按手册原有类别整理为中文摘要，保留缺陷编号、关键命令与适用平台；引用时以手册原文和具体版本为准。这是版本敏感清单：仅对应 2026 R1，其他版本须重新核对。

## GUI（p. 155）

- 4K 显示器（分辨率高于 1920x1080）下，Fluent Meshing 工作流中调用字段级 "?" 帮助时窗口不能自动调整大小，文本被截断并出现滚动条。(1006416)
- （仅 Linux）不支持 AMD Radeon Pro 显卡，Fluent 会话可能意外关闭。(348500)
- 在 4K 与非 4K 显示器之间拖动应用可能缩放异常；变通：移动到新屏幕后重启 Fluent。(345352)
- 非默认布局（如 console 与 graphics 窗口选项卡化）且强制 MSW 图形驱动（`HOOPS_PICTURE=msw/win` 或 `-driver msw`）时可能意外挂起。(269471)
- （Windows 4K）可能需要调整显示缩放与布局设置以适配窗口。
- （仅 Linux 4K）应用窗口自动缩放与 graphics 窗口交互不兼容；设 `QT_AUTO_SCREEN_SCALE_FACTOR=1` 可正确缩放，但交互可能异常。(143229)

## 文件导入/导出（pp. 155–156）

- （仅 Red Hat 8.8）CGNS 不受支持，导入/导出会导致会话意外关闭。(882695)
- Fluent→Mechanical 单向传输（legacy `.dat`/`.dat.gz`）：多相算例的压力值可能不出现在 Mechanical 中；变通：右键 Fluent Solution 单元 → Clear Generated Data → 更新 Solution 单元（确保生成 legacy `.dat.gz`）→ 更新 Mechanical Setup 单元。
- wall/wall-shadow 对：导出到 CFF-Post 的变量可能被错误填零（如耦合 wall shadow 上的壁面剪应力），导致与 EnSight/CFD-Post 对比出现差异；应以 Fluent 内显示的后处理值为准。(419385)
- 创建 adjoint bounded-by-surfaces 设计条件或 imprinted surface 时无法读取默认 CFF 算例文件（`.cas.h5`）；变通：在 Fluent 会话中用 `file/cff-files? no` 关闭 CFF 写出后另存为 `.cas`。(199821)
- （仅 Windows）无法导出大于 2GB 的 CGNS 文件；变通：改用 Linux 机器导出。(259220)
- EnSight 格式导出的表面可能带 ID 0：导入 EnSight 没问题，但导入 ParaView 等第三方后处理软件会报错；变通：为该表面创建 zone surface 并导出新表面。(254966)
- TurboGrid 2019 R3 导出的 CGNS：须在 TurboGrid 中关闭 Split Blade Faces By Geometry（右键 3D Mesh → Edit in Command Editor → 设为 false），否则 Fluent 无法读取。(121053)
- 在 Autosave 对话框中更改 File Storage Options 会丢失 solution history。
- 瞬态模拟导出 EnSight Case Gold 时，不能在运行中切换 serial/parallel 或更改并行节点数，否则各时间步文件互不兼容；不支持带拓扑变化的 EnSight 导出。
- Fieldview（`.fvuns`）：网格文件须用 `fieldview-unstruct-grid` 文本命令导出；并行会话导出网格与数据文件时节点数必须一致。
- Tecplot 导入不支持 Tecplot360 文件格式。
- 单个 Fluent 会话最多读取 50 个 profile。
- CFF 文件 I/O 的 PARALLEL INDEPENDENT 模式写性能慢：并行文件系统上建议 PARALLEL COLLECTIVE，其他网络文件系统上建议 HOST 或 NODE0 模式。
- UNC 路径：必须对路径中所有文件夹有访问权限，否则无法打开文件。
- （仅 Windows）Select File 对话框的文件过滤器可能失效，需手动选择文件。(174291)
- Ansys 产品写出的文件不支持与 Microsoft OneDrive 同步。(187717/74067)

## 网格（p. 157）

- 切割（slit）耦合壁面时，若该壁面包含同时被两对以上周期边界共享的节点，Fluent 会异常终止；注意启用时间平均显式热耦合（`define/models/cht/explicit-time-averaged-coupling/conformal-coupled-walls`）也会触发 slitting。变通：先用 `define/boundary-conditions/modify-zones/slit-periodic` 解耦相关周期对。(528636)
- gap 模型带流动阻塞区域、或动网格接触检测用 contact marks 方法做流动控制时：被标记为阻塞的单元不得与周期边界相邻，否则初始化或计算时报错。(498569)
- 许可证偏好设为 "Share a single license between applications when possible" 且已开 Fluent Meshing 会话时，再打开 Fluent Solution workspace 会导致 Meshing 挂起来不及保存；变通：改为 "Use a separate license for each application"。(147834)
- Meshing Mode 中没有悬停高亮和 Boundary Markers。(241447)
- 带 hanging nodes 的面无法做边界区拉伸（extrusion）。
- 多区域+接触问题：Fluent 中一个 zone 只能存在于单个接触区域，与 Mechanical/Meshing 对接触区域的处理方式不同。
- 不支持边缘（edge）的 FSI 数据映射，因此 2D 不支持 FSI。
- 非一致界面：Matching 选项不再允许与 Mapped 选项共用；打开旧版本两者皆启用的算例时会提示重建界面。
- 壁面附近阶梯式（step-wise）棱柱网格：不要将 node-based gradients 与 MUSCL 联用。

## 模型（pp. 157–159）

- 降阶模型（ROM）不支持 Mass-Weighted Average 报告定义（ROM 只有面心和单元心数据）；改用 Area-Weighted Average、Facet Average/Minimum/Maximum。(281540)
- 物理速度（physical velocity）多孔介质公式：当多孔阻力（惯性或粘性）小于或与跨多孔界面的动压变化相当时，可能产生非物理流场和差收敛；将多孔界面区改为 porous jump 边界可有效解决。(61773)
- Oppdif flamelet 导入仅支持 Chemkin II 格式。
- S2S（surface-to-surface）辐射模型不能用于运动/变形网格。
- DPM work pile 算法与 wall film 边界条件不兼容。
- 瞬态 Lagrangian 多相 + DPM 非定常颗粒追踪：当 Particle Time Step Size 小于 Run Calculation 的 Time Step Size，或用 `define/models/dpm/numerics/re-randomize-every-iteration? no` 关闭了初始位置再随机化时，atomizer/cone 注入会从同一位置而非随机位置释放颗粒。变通（console 中 Scheme 命令）：`(rpsetvar 'dpm/random/seed-timestep-corrected? #t)` 与 `(dpm-parameters-changed)`；注意这也会影响随机追踪、破碎等涉及随机数的机制的颗粒轨迹。(176638)
- shell conduction 模型不适用于运动壁面。
- 换热器模型与网格自适应不兼容。
- Fluent/Ansys Reaction Design KINetics 耦合在 win64 平台不可用。
- DO-Energy 耦合仅建议用于大光学厚度（> 10）算例。
- FMG 初始化：不能与 shell conduction 模型联用；与非定常求解器不兼容。
- MHD 模块与 Eulerian 多相模型不兼容。
- Bounded 2nd order 时间离散与运动/变形网格不兼容。
- 多孔介质 + 非平衡热模型：Porosity 不能为 0 或 1（必须严格在两者之间）；非平衡热模型不支持与辐射和/或多相模型联用。
- 多孔介质相对速度阻力公式：存在非零 swirl 阻力时不支持 axisymmetric-swirl。
- 启用 shell conduction 的壁面与非一致耦合壁面的交接处不受支持：两者之间不会有热连接。
- 启用 Eulerian Wall Film 模型后不允许保存网格修改（分离单元、拉伸面区、更改单元区类型）；须先完成全部网格操作再启用该模型。
- Transition SST（γ-Reθ）模型不满足伽利略不变性，不应用于相对计算坐标系运动的表面；此类情况应改用 Intermittency Transition（γ）模型。
- 用户定义壁面函数与 Eulerian 多相公式不兼容。
- v16.0/16.1 生成的 S2S view factor 文件：若 mapped interface 启用了 Matching 选项，可能与新版本不兼容；须在新版本中重算 view factors。

## 参数化研究（p. 159）

- Parametric ribbon 的 Save Journal 保存的 journal 是为新会话设计的，在已初始化参数化研究的会话中运行可能出错；变通方法需联系技术支持。(932695)

## 并行处理（pp. 159–160）

- DTRM（离散 transfer 辐射模型）在并行求解器中不可用。
- 使用大页（large pages）内存分配的系统上，Fluent 报告的虚拟内存可能远高于实际用量；以 resident memory 为准。
- Eulerian Wall-film 模型与混合并行 DPM 追踪的 DPM Domain 选项不兼容；须在 Discrete Phase Model 对话框 Parallel 选项卡关闭 Use DPM Domain。
- 自 v18.0 起，每个节点进程比 v17.0–17.2 约多用 60 MB 内存。
- Windows-Linux 混合模拟：若 `C:\windows\system32` 内有 OpenSSH，Fluent 可能找不到 ssh（报 "'ssh' is not recognized..."）；须用 `-rsh=c:\cygwin64\bin\ssh.exe` 指定实际 ssh 路径（或 Fluent Launcher Remote 选项卡 → Remote Spawn Control 选 Other 填路径），并把 ssh 可执行文件位置加到 PATH 开头。(184255/176971)
- InfiniBand 互连的并行模拟内存占用可能比之前版本高，密集 I/O（频繁写 `.dat.h5`）时尤其明显，集群大算例可能耗尽内存；变通：改用 ethernet 互连，或降低求解期间 I/O 频率，或在内存开始增长时停止计算再重启。(597320/610518)
- 动态进程 spawn：须手动指定互连——共享内存或无 InfiniBand 的分布式内存用 `-pethernet`，InfiniBand 分布式内存用 `-pib.ofed`。

## 消息传递接口 MPI（p. 160）

- 某些 Mellanox 驱动/库配置的 InfiniBand 集群：Intel MPI 可能需要 `-pib.ofed` 或 `-pib.psm3` 而非 `-pib`（等价于 Launcher Interconnects 列表中的 infiniband.ofed / infiniband.psm3）；多数用户不需要。
- IBM MPI 已被厂商停止维护，不再随 Fluent 标准安装提供。
- Intel MPI 是 Windows（少于 64 逻辑核）和 Linux 的默认 MPI，已知限制：
  - Windows 上经 Ansys Installation Launcher 安装 Intel MPI 时 hydra 服务安装失败；变通：管理员手动运行 `"c:\Program Files (x86)\Intel\oneAPI\mpi\2021.8.0\bin\hydra_service.exe" -install`。(812613/791313)
  - Windows 或混合 Windows/Linux 下，从 meshing mode 切换到 solution mode 时无法动态 spawn 额外进程（无论用 Launcher 中 Meshing Processes < Solver Processes 还是 `/parallel/spawn-solver-process`）。CFD Pro 级别下若以 Solver Processes > 1 启动，这些核也会进入 Meshing workspace，但网格划分仍是串行（CFD Pro 不支持并行网格）。(236195/257722)

## 平台支持与驱动（pp. 160–161）

- Windows Server OS：并行运行仅支持 MS MPI；安装 Intel MPI 库会冲突。
- Windows 7 及以后：安装到 C: 以外的驱动器可能因路径空格未转换为短文件名出问题（`NtfsDisable8dot3NameCreation` 默认值变化）；安装前须运行 `fsutil 8dot3name set <driveletter> 0`（如 `D:`）。
- Linux 最低 OS 要求：SLES 11 SP2 或 RHEL 6；SLES 12.5 不受支持。
- Linux：当前工作目录路径不支持空格字符。
- 在已装旧版 Fluent 的 Windows 机器上安装 2026 R1：装完 Intel MPI 先决组件后须删除环境变量 `I_MPI_ROOT`，否则旧版本并行运行会冲突。
- Remote Solver Facility（RSF）不再受支持；Itanium 平台（lnia64）不再受支持。
- Fluent 使用多个 TCP/IP 端口通信和错误处理；端口冲突警告（如 `mpt_accept: warning: incorrect exercise message "GET /" ...`）通常可安全忽略，长时间大算例更易出现。
- CentOS/RHEL 7.3 且 DISPLAY 指向 VNC 会话时，启动期间可能异常终止；变通：确认使用受支持显卡并更新厂商驱动；或把 DISPLAY 设为本地；或设 `LD_PRELOAD=/usr/lib64/libstdc++.so.6`；或改用 x11/null 驱动（`HOOPS_PICTURE` 环境变量或 `-driver` 选项）。

## 远程显示（pp. 161–162）

- 加速远程显示（DCV、EOD 等）+ OpenGL2 图形驱动可能导致 Fluent 意外关闭；变通：切换 OpenGL1（`display/set/rendering-options/driver/opengl`）。(283643)
- 模拟运行中连接/断开 VPN 会因网络接口变化导致失败。
- 远程显示下异常终止：检查是否为较新的专业显卡并装最新驱动；不满足时改用纯软件驱动 MSW（Windows）或 X11（Linux）。
- （Exceed onDemand、VNC Viewer）Num Lock 数字键和方向键可能在 GUI/console 中失效；设 `XKB_DEFAULT_RULES=base` 可恢复方向键，数字须用主键盘区数字键输入。(172528)
- （仅 Linux）VNC/Nice DCV/EoD 下可能因第三方问题出现意外报错；须安装 xcb-util-wm-0.4.1-5.el6、xcb-util-keysyms-0.4.0-1.el6、xcb-util-0.4.0-2.2.el6、compat-xcb-util-0.4.0-2.2.el6、xcb-util-image-0.4.0-3.el6 包。(185796)
- （仅 Linux）无加速显卡的集群上可能不接受键盘输入；设 `QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb`。

## 单元区与边界条件（p. 162）

- 3D fan zone 的流体区不能有非一致界面。
- Mesh Motion 与 6DOF 不兼容；需要相对 6DOF 区运动时应创建 Rigid body dynamic zone。

## 参考系（p. 162）

- Reference Frame 对话框中点 OK 会用当前可编辑设置重新定义参考系（Current State 会被置为 Initial State 选项卡的值）；无意更改时应点 Cancel 退出。(184248)

## 求解器（pp. 162–165）

- 标准 CPU 求解器：同时含可压与不可压流动区的算例可能得到错误结果（影响温度和速度）；变通：改用 Fluent native GPU solver。(892103，手册在 p. 162 与 p. 165 重复列出)
- 启用基于单元梯度质量的 poor mesh numerics 时：单精度下应用到的单元数会随进程数不同而变化；变通：用双精度求解器。(362753)
- 压力出口边界存在强回流时，绝对速度与相对速度公式可能给出不同结果。
- NITA（非迭代时间推进）只适用于有限模型集合；NITA 分数时间步方法与多孔介质不兼容。
- 密度基求解器不可用的模型：VOF、Multiphase mixture、Eulerian 多相、非预混/预混/部分预混燃烧、Composition PDF 输运、Soot、Rosseland 辐射、熔化/凝固、Enhanced Coherent Flamelet、惰性组分输运（内燃机 EGR）、Dense discrete phase、shell conduction、浮动操作压力、火花点火与自燃模型、多孔介质物理速度公式、SAMG。
- 压力基耦合求解器不可与 Fixed velocity 联用。
- 某些 Linux 平台上 Ctrl+C 无法中断求解；变通：使用 Fluent 检查点机制保存/退出（手册 “Checkpointing an Ansys Fluent Simulation”，印刷页码 p. 216，属 Part I 尚未摄取页段）。
- 四面体/混合网格中 Least-Squares Cell Based 梯度 + cell-to-cell limiter 可能导致发散；建议改 Green-Gauss Node Based 梯度或改 cell-to-face limiter。
- 自 v17.0：若用 `define/models/shell-conduction/multi-layer-shell` 禁用了多层 shell，则 WFGC（warped-face gradient correction）不支持 shell conduction。
- 瞬态/时间相关算例：推进到下一时间步取决于时间步长与收敛准则等输入，不直接依赖监控用的 flow time interval（报告定义、自动保存、瞬态导出等）；这些操作在 flow time 达到或超过指定间隔时才触发。
- 残差相关问题：启用 High Order Term Relaxation 的算例重启后可能出现小残差跳跃 (178223)；壁面函数边界处理 + No Slip 剪切条件的湍流算例重启后残差历史可能与连续运行略不同 (165935)；两者偶尔影响长时间瞬态模拟（LES、SRS、SBES，各时间步未深度收敛时）的残差历史。
- R19.2 或更早创建的定常、单相、压力基算例：当物理设置含反应流和/或组分输运 + 伪时间方法时（点 Default 按钮或新启用两者），Solution Controls 中 Density 显式松弛因子会被置为 1，而应为 0.25（与 2019 R1 行为一致）；变通：手动输入 0.25。(182453)
- `solve/set/set-controls-to-default` 只对 limits 生效，对 solution controls 和 AMG controls 无效；变通：分别点 Solution Controls 任务页和 Advanced Solution Controls 对话框 Multigrid 选项卡的 Default 按钮（旧的定常单相反应流+伪时间算例还须手动设 Density 松弛 0.25）。(183926)
- Fractional Step 压力-速度耦合与动网格 layering 联用不受支持；如需运行，计算前输入 `(rpsetvar 'dynamesh/layering/layering-before-move? #t)`。(125886)
- profile 更新间隔若高于瞬态算例每时间步最大迭代数，定义边界条件的 profile（UDF 或命名表达式）不会每时间步更新；须保持默认值 1。(882920)

## 用户自定义与 UDF（p. 165）

- zone motion（MRF 或动网格）用的表达式中 "Time" 取上一时间步的 flow time，而 DEFINE_TRANSIENT_PROFILE 的 "Time" 参数取当前时间步的 flow time。(147162)
- 用花括号 `{}` 指定已定义对象名（报告定义、cell register 等）时自动建议被禁用，必须键入完整显示名。(118322)
- Fluid/Solid 单元区对话框 Fixed Values 选项卡中字段用的表达式不能带单位。(146295)
- 向 Fluent 下拉菜单添加菜单项的脚本/journal 已失效（菜单被 ribbon 取代）；须创建独立的用户自定义菜单（见 Fluent Customization Manual “Adding Menus to the Right of the Ribbon”）。
- 解释型（interpreted）UDF 不能与 InfiniBand 互连联用，必须改用编译型 UDF。
- Windows 10 上 Visual Studio Express 2015 for Windows 安装器把库装到非标准位置；为确保用 Visual Studio 编译 UDF，应使用 "Express 2015 for Desktop" 安装器，或手动设置 LIB 路径（如 `LIB="C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\lib\onecore\amd64";%LIB%`）。

## 图形、报告与后处理（pp. 165–168）

- （后处理应用，仅 Linux）用户自定义表面（如 line）位置更新后仅重新显示 scene 可能不生效；须重新显示表面本身。(450062)
- 数据文件不存储导出量（如压力梯度）：读入数据文件后立即显示压力梯度会错误地显示为零；运行一次迭代再重新显示。(774389)
- （仅并行）鼠标探针选取的位置与代码选定的表面顶点可能偏差较大；变通：在 Preferences（File > Preferences...）Graphics 分支关闭 Remove Partition Lines。(458754)
- （仅 Linux）关闭 Node Values 显示的后处理对象可能不显示全部所选表面（第三方问题）；变通：用 OpenGL 图形驱动。(347474)
- bounded plane 或平面 iso-clip 上的结果可能错误地显示部分六面体单元为三角形；不影响这些表面上的结果数值；关闭 Bounded 选项创建的平面无此问题。(380979)
- 平面表面后处理出现孔洞/暗斑时，可改用 iso-surface 显示目标量（Iso-surfaces，印刷页码 p. 4046）。
- （仅 Linux）启用 dynamic shadows 时不显示等值线；在 graphics 工具栏或 Preferences 中关闭 dynamic shadows。(343770)
- pathlines 的 Keyframe Scene 动画只支持非持久/"global" 版 Pathlines 对话框（无 Name 字段）；打开方式：Outline View 中右键 Pathlines → Edit...，或 Results ribbon 的 Graphics 下 Pathlines → Edit...；须先在 Preferences Graphics 分支启用 "Expose legacy non-persistent graphics"。(269934)
- 对 dp/dt 定义的自定义场函数，非定常统计的 mean/rms 可能显示为零；变通需联系支持。(199006)
- （仅 2D）框选表面只支持从右向左拖动；在 Mesh Display 对话框启用 Edges 或 Faces、或在 Preferences Appearance 分支启用 "Show model edges" 可恢复从左向右框选。(259419)
- 带等值线的填充云图导出为 AVZ 格式后，等值线在 Ansys Viewer 中不可见；变通：scene 中放两个重复的云图对象（一个填充、一个只有等值线），可关掉其中一个的 colormap。(137138)
- 监视器所在 zone 被停用后，监视器可能仍继续打印/绘图。
- Windows 上自动保存多个 scene 时，Headlight 灯光状态（开/关）可能不一致；变通：每个 scene 在单独的 graphics 窗口渲染。
- 自定义场函数的 Mean/RMSE 统计只对 mixture 可用；对 phase 指定是 R16.0 之前的错误行为，2026 R1 运行此类旧算例可能段错误（segmentation error）；须重新定义相关监视器。
- mouse-annotate 功能已移除；标注仍可用 Annotate 对话框（印刷页码 p. 5503）。
- 自 v15.0：运动固体壁面上的热流率 flux 报告包含固体运动导致的对流热流，报告值可能与边界条件定义不同（如绝热壁报告非零热流）。
- 导入 18.0 之前创建、多个监视器共用同一窗口的算例：运行前须检查并把各报告图分配到不同窗口，否则同窗口的图会丢失。
- 用文本命令（如 `display/objects/create`）创建名称含空格的图形对象（contour、vector、mesh、pathline、particle track、XY plot、scene）后，无法用 `display/objects/display` 显示（只报错）；变通：创建时不用空格，或用 GUI 显示。
- XY plot 的 Curve Length X Axis Function 偶发不能正确绘图（即使曲线面是分片线性的单一闭合曲线）；变通：用 Direction Vector X Axis Function。
- 非线性函数的瞬态统计：Mean Velocity Magnitude 是由平均速度分量构造的向量的模，Mean Pressure Coefficient 用平均压力计算；要得到此类量的真实 Mean/RMS，应定义自定义场函数再收集其统计（如 `vmag_cff = sqrt(Vx^2 + Vy^2 + Vz^2)`，报告 vmag_cff 的 Mean 和 RMS）。
- Key Frames（Animate 对话框）创建的 scene 动画与等值面上的图形显示（云图、矢量、pathline、颗粒轨迹）不兼容；pathlines 与 scene 动画完全不兼容（无论选什么表面）。
- 网格单元数很大（约 1.5 亿及以上）时，meshing mode 可能因 IOS（inverse or thoskew）值错误而报告不正确的 skewed 单元数；变通：`(tgapi-util-set-number-of-parallel-compute-threads 1)`。(168453)
- rake 表面上用可保存 XY plot 图形对象（New... 创建）时结果可能不立即显示；变通：XY Plot 对话框 Curves... → Marker Style 选 Symbol → Apply → 重新显示；若关闭 Node Values 显示单元值时点被连成线，把 Curves - Solution XY Plot 对话框 Line Style 的 Pattern 改为 "empty"。(180547)
- Transform Surface 对话框不支持用户创建的表面（line、point、iso-surface 等）；须手动平移输入点并新建对应表面。
- 显示范围含固体区的密度云图：range 计算会包含固体区，显示的固体密度不反映实际设置（流体区正确）；在 Contours of 下拉中选 Density... 与 Density All 可正确显示固/流密度。(155346)
- 对象名不应使用特殊字符（`/^*%@,<>{}()?&~!=`）：可能影响图形显示甚至完全不显示 (157473)；还可能导致报告文件名不一致，启动计算时出现 validation 问题 (531947)。
- annotation 文本的前景/背景色与 Preferences 不同步，由 `display/set/colors/foreground` 和 `display/set/colors/background` 文本命令控制。
- 图形渲染/图片保存速度显著变慢时，手册给出的最佳实践：cortex 运行在带合适显卡和最新驱动的机器上（`-gui_machine=<hostname>` 或 Launcher Scheduler 选项卡 Graphics Display Machine 选 Specify Machine）；cortex/host 进程与 compute node 0 分开机器（`-gui_machine` 指定的机器不要作为 `-cnf=x` hosts 文件/机器列表的第一台）；图形驱动不要设为 null、x11（Linux）、msw（Windows）；保存图片时启用 Preferences（Graphics）中的 Fast hardcopy。

## Fluent in Workbench（pp. 169–170）

- Fluent Meshing 配合 RSM 与并发设计点更新时，个别 Design Point 在网格更新期间偶发失败；重新提交通常可成功。(694742)
- Workbench 项目中 CFF 格式的 case/data 若同时导出 `.cdat` 文件，用 CFD-Post 后处理可能报错（导出 `.cdat` 时会同时写出 legacy `.cas` 作为最新 case，与 CFF 数据文件 `.dat.h5` 配对，而 CFD-Post 不能混用 legacy 与 CFF 文件）；变通：导出 `.cdat` 后手动写出新的 `.cas.h5` 和 `.dat.h5`。(310992)
- 导入 Fluent Case 和 Data 到 Fluent 系统、且 Update Option 选 "Submit to Design Point Service" 时，项目更新会失败；变通：更新前右键 Solution 单元选 Refresh，或在 Project Schematic Properties 中把 Update Option 改为 RSM。只导入 Case（无 Data）或从 Geometry/Mesh 开始的项目不受影响。(277667)
- colormap 的 Automatic Skip 选项未按预期工作；变通：手动指定 skip 值。(273989)
- 含下列内容的算例在 Workbench 中更新可能失败（报 "Value cannot be null. Parameter name: fileName"）：转换为报告定义的 legacy（18.0 之前）监视器；未指定文件名的报告文件对象（任何版本）。变通：先在 Fluent 中读入 case，删除报告文件或为其指定有效文件名。(146221)
- 不支持 Fluent 与 HFSS 或 Q3D Extractor 的耦合。
- Maxwell-Fluent 双向耦合默认 zone：体积损耗映射用 Maxwell Mapping Volumetric 对话框中选定的 zone 列表；表面损耗映射用所有 cell zone。更改反馈映射 zone 用 Scheme 命令，如 `(em-set-feedback-map-cell-zone '(1 2))`（只指定 cell zone ID）。
- Fluent 分析系统中 Solution 单元的 Clear Generated Data 不会清除动画相关文件；须在打开 Workbench 前将 `FLUENT_WB_REMOVE ALL_GENERATE_FILES`〔原文如此，含空格，疑为手册排版错误，未核实确切变量名〕定义为本地系统环境变量。
- RSM 设计点研究可能因错误未完全更新；重跑受影响的设计点即可（可能需多次）。(350696, 385734, 553033)

## 帮助（p. 170）

- （仅 Ubuntu）Fluent Launcher 与 Fluent Solution workspace 中的部分帮助链接失效（Fluent Migration Manual、Ansys News Center、Ansys Blog、Fluent Documentation、Tutorials、Videos、Ansys Learning Hub、Ansys Training Center、Online Technical Resources）；变通：启动 Fluent 前将 `LD_PRELOAD` 设为 `/usr/lib/x86-64-linux-gnu/lib-stdc++.so.6`〔路径为手册原文印刷形式，与 Ubuntu 惯用写法 `/usr/lib/x86_64-linux-gnu/libstdc++.so.6` 字符不同；已视觉核对 p. 170 确认原文如此，实际使用哪个写法待验证〕。(736116)

## 其他（pp. 170–172）

- `/define/custom-field-functions/create` 对电离组分失败：组分名中的 "+"（如 `NO+`）被解释为运算符；变通：在 GUI 的 Custom Field Function Calculator 中建好方程并存为 scheme 文件，journal 中用 `/define/custom-field-functions/load` 加载。(1375077)
- 不要用 `inf` 命名任何边界、cell zone 或对象（报告定义、图形对象等）：与 Python 语言中表示 "infinity" 的 `inf` 冲突。
- 启动时加载 ACT 后访问 Preferences 可能出现警告；变通：关闭 Fluent，在 Fluent Launcher 中禁用 Load ACT 再启动，运行中修改 Preferences 并点 OK 保存。(462205)
- Windows HPC 集群上 Microsoft HPC Pack 的 affinity 处理不佳可能拖累性能；变通：Job Scheduler Configuration 的 Affinity 选项卡中 Affinity Type 选 "No jobs"。(395881/400841)
- Save Picture 对话框截取的嵌入式 graphics 窗口图片不带边框，与 Preferences 设置无关。(336851)
- CFD Pro 许可证：user-defined specification method 对部分字段（如材料属性）可用，但不能加载 UDF（该级别不支持）。(321331)
- Fluent 导出的 CFF-Post 文件可能把压力梯度错误指定为零；变通需联系支持。(239127, 243318)
- 串行或并行计算期间网络连接丢失，Fluent 会话可能异常终止。（手册在 p. 171 与 p. 172 重复列出）
- IRIS Image 和 HPGL hard copy 格式不再受支持。
- 配合 RSM 使用 Fluent：处于 pending 状态的已保存项目只有一份能成功重连；不支持 Maxwell 耦合；UDF 支持有限制（见 Workbench User's Guide “Submitting Fluent Jobs to Remote Solve Manager”）。
- 叶轮机械后处理的 turbo-averaged 云图在选定拓扑中可能出现意外的云图区域。
- Linux 上从 Fluent 打开 Ansys Help 可能报错：其他用户创建安装并运行过 Fluent 生成 registry 文件后，再运行同一安装会有权限冲突；变通：删除 `path/ansys_inc/v261/Tools/mono/Linux64/etc/mono/registry`，并移除 `.../etc/mono` 目录的写权限。
- Windows 上串行 Fluent 会话读网格时，每核超过 2000 万单元可能失败。
- 文件名、zone 名和边界名不支持非 ASCII 字符。
- Linux 上以 Load ACT 选项启动的会话退出时可能无响应，须手动终止进程（报错提到 corrupted double-linked list）；发生在项目保存之后，无数据丢失。
- Linux + Load ACT 运行时，求解迭代期间可能反复出现 "Unexpected error checking licensing server" 警告；无害，不影响 Fluent 或 ACT 使用。
- 混合 Windows/Linux 配置或远程 Windows 安装下运行 standalone Fluent 时 ACT 无法打开；须设置 `AWP_ROOT261` 环境变量指向 Ansys 安装目录。
- 自 Release 19.2 起 Linux 上禁用 Fluent 的 ACT；要用 ACT：Windows 上用 19.2 或更高，Linux 上用 19.1。(177173)

## Fluent Meshing（pp. 172–173）

- （2026 R1 或更早）workflow 树/outline view 与 graphics 窗口显示重叠时，删除 home 目录下的 `.cxlayout.ini` 文件。
- 引导式网格工作流的限制单独成文：手册 “Limitations of the Fluent Guided Workflows”（印刷页码 p. 287，属 Part II，尚未摄取）。
- rapid octree 网格：新建 mesh object 在 GUI 可用，TUI 中须依次用 `/parallel/auto-partition? no`、`/parallel/agglomerate yes`、`/objects/create`。
- Fault-tolerant 工作流在大型机器配置（如 256 核及以上）读网格文件时可能出问题。
- polyhexcore 网格存在孤立单元时 mesh check 结果可能不满意；用 `(%tg-delete-isolated-cells (get-cell-zones-of-filter '*))` 删除孤立单元。
- 向 Fluent Meshing 导入 Discovery 文件（`.dsco`）前，须先在 Discovery 中把备选许可证偏好设为 ANSYS CFD PrepPost。
- 使用旧版本的 journal（`.jou`）或 workflow（`.wft`）文件可能拖慢甚至停滞体网格生成；变通：journal 开头加版本信息（如 `/file/set-tui-version "19.5"`）；workflow 文件把 Create Volume Mesh 任务的 Quality Warning Limit 设为接近 0 的值（如 0.05）而非接近 1。(163320)
- 混合 Windows/Linux 环境下写 CFF（`.cas.h5`）文件时，Fluent Meshing 只在 Linux 节点上写文件；变通：Windows 侧用映射驱动器作为工作目录，并把远程工作目录指到该映射驱动器的源路径。
- （仅 Linux）从 Ansys Mechanical、DesignModeler、Meshing 导入几何依赖 xmessage 命令：SLES 装 xmessage 包，RHEL 装 xorg-x11-apps 包。
- 从 Ansys Meshing 导入的网格可能缺 interior face；变通：在 Ansys Meshing 中生成网格前，把所有内表面放进名称含 "internal" 的 Named Selection。
- 19.2 之后单个 cell zone 内不允许多个 interior zone；旧算例中此类 zone 不会显示。变通：把网格读入 19.2，将 interior zone 类型设为 'wall' 以恢复缺失 zone；读旧版网格时用 `Meshing>file read-options`，依次回答 `Enforce mesh topology [no]`、`Check read deata [no]`〔菜单文字为手册原文转录，"deata" 拼写如此〕、`Correct Interiors? [yes] no`；读入后把问题边界类型改为 'internal' 并保存网格文件。(143347)

## gRPC（pp. 173–174）

- 多远程 IP 地址的机器：证书必须为 Fluent gRPC 服务器实际选用的同一 IP 地址生成；可查看 gRPC 服务器写出的 server-info 文件确认服务器 IP。(1342741)
- 遗留行为：gRPC 服务器选 IP 不确定（有的机器选 localhost/127.0.0.1，有的选集群数值 IP）；workspaces 中有多种文档化变通方法，例如用 workspace preference 选项把 127.0.0.1 固定为 gRPC IP，或用 `REMOTING_SERVER_ADDRESS` 环境变量固定任意地址；证书须按将被选用的同一 IP 生成。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）第 1.3 节 “Known Limitations in Ansys Fluent 2026 R1”，PDF pp. 155–174。类别划分与缺陷编号照录手册；条目为中文转述，命令、环境变量、路径和报错文字保留原文。
- **版本敏感**：全部条目仅对应手册声明的 2026 R1（个别条目标注了引入版本，如 15.0、17.0、18.0、19.2）。在其他版本使用本页前须重新核对。
- 两处字符串经 400/600 dpi 视觉核对确认为手册原文印刷形式，但疑似排版错误，已用〔〕标注待核实：`FLUENT_WB_REMOVE ALL_GENERATE_FILES`（p. 170，含空格）；`/usr/lib/x86-64-linux-gnu/lib-stdc++.so.6`（p. 170，与 Ubuntu 惯用路径写法不同）。`Check read deata`（p. 173）为手册转录的菜单原文。
- 本页为便于检索的完整转述，但个别长条目做了压缩；引用具体限制解决实际问题时，应回到手册对应页码核对原文与前置条件。
- 手册中 "Known Limitations" 与 "Third-party software" 的交叉引用（支持文件类型表）在 1.4 节，见 [[Fluent 程序架构与能力]]。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part I - Getting Started]]
- [[Fluent 程序架构与能力]]（同章 1.1/1.2/1.4 节）
- [[CFD 仿真工作流与验证]]
- [[Fluent 启动与批处理自动化]]（启动参数、平台差异相关条目可互相印证）
- [[Fluent 网格质量诊断]]（skewness 报告在大网格下可能不准确的条目与之相关）
- [[index]]
