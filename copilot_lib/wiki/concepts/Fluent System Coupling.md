---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - Ansys Fluent
  - system-coupling
  - fsi
  - multiphysics
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent System Coupling（系统耦合）

## 摘要

User's Guide 2026 R1 Part III / Chapter 49 "Performing System Coupling Simulations Using Fluent"（PDF pp. 4849–4886，十二节）。**摄取状态：全章完成（批次 133，pp. 4849–4886，49.1–49.12 全部十二节）**。System Coupling（SC）编排多物理求解器耦合（如 Mechanical + Fluent 共同分析、或从外部数据源导入静态数据）；运行语境：**SC 的 GUI/CLI** 或 **Workbench 中的 SC**。**最佳实践：Fluent 用双精度求解器参与 SC。**

## 49.1 支持能力与限制（pp. 4849–4854）

**能力**：
- 壁面（含滑移网格区壁面）、porous jump 边界、多孔区界面（经零厚度 porous jump）上的**力与位移传递**：输入增量位移（Dynamic Mesh Zones 对话框的 System Coupling 选项，MDM）；输出总力（黏性+法向）——所有壁面均可输出（无论是否勾 MDM）。
- 壁面与单元区的**热数据传递**：壁面输入温度/热流量/换热系数（Boundary Conditions Thermal 选项卡的 via System Coupling 选项）；经 Maxwell 在毗邻固区的耦合壁输入表面热率；单元区输入热率；壁面输出温度/热流量/HTC；单元区输出温度。
- **双向刚体 FSI**（外部刚体求解器）：建 Motion Definition（Type = System Coupling Motion）→ 建 Dynamic Mesh Zone 并挂该定义 → 导出 `.scp`。SC 接收的运动参数：`delta-x/y/z`、`theta-x/y/z`；初始质心 `initial-x/y/z`；初始姿态 `initial-theta-x/y/z`。
- Fluent ↔ Maxwell **电弧传播**：单元区输入 Lorentz 力/温度/热流量，输出电导率/温度/热流量。
- 耦合与非耦合体的**时间相关运动与激励**（仅 SC CLI/GUI，不支持 Workbench；Fluent 匀速 + Maxwell 一致位移；仅 Maxwell/Fluent 电磁-热分析；固体单元区可按刚体用总位移；运动可用 profile——对应当前耦合步结束时位移）。
- **两个 Fluent 应用间的命令行表面热耦合**（一瞬态一稳态）：瞬态→稳态支持**时均 HTC（或 T*）**传递——耦合步内引入**子步（sub-stepping）**累积非稳热数据后按时均公式计算；HTC 计算扩展支持 **Wall Functions 与 Y plus** 法（默认壁面邻近法）；TUI：`/define/models/system-coupling-settings/htc-calculation-settings>` 下 `htc-calculation-method/` 与 `unsteady-statistics/`；时均仅支持 HTC 与 T* 两量、**显式耦合（每耦合步一次耦合迭代）**；瞬时 HTC（Wall Functions/Y plus）亦可传递。
- 滑移网格区/刚体区壁面的数据传递；三角与四边形面交界单元类型；本地与分布式并行全支持；自定义求解器输入与重启文件（GUI/CLI）；所有方程的**收敛数据**运行时共享给 SC（监视点设迭代频率才共享监视数据——时间步频率不共享）；Workbench 系统耦合图可绘制；监视数据也可在 Fluent Solution Monitoring 绘制。

**限制**：不支持 RSM（Remote Solver Manager）——强制前台运行；动网格重划建议用 **Unified remeshing**（2.5D 不被 unified remeshing 支持；Workbench 中 Fluent-Structural 用 Methods-Based 重划可能报错）；wall + wall-shadow 对作 SC 接口时须在 Mechanical 建复制面（配两套壳单元；见 Mechanical 用户指南 Coupling Thin Surfaces in CFX）；**必须 3D 网格**（传递区域为 3D 网格内的单元面——2D 不行）；传递区域**不得含悬挂节点**（悬挂节点自适应产生；hexcore/CutCell 读入时未启用转换也会有）；**FSI 期间 SC 边界上网格拓扑必须固定**——SC 边界上不能动网格重划（远离 SC 边界的内部节点仍可重划）；wall/wall-shadow 对传力需 Mechanical 两个面（不能用单套壳单元；例：零厚度内部壁两侧不同流体）；**NITA 不可用**；执行 System Coupling case 的设计点时 Fluent Initialization Method 不得用 Program Controlled；Fluent 区域经 SC 接收热数据时**不能用 shell conduction**。

## 49.2 在 GUI/CLI 中执行（pp. 4854–4856）

物理设置在参与者界面完成；耦合分析（启动耦合服务、加载参与者、耦合设置、自动启动参与者）在 SC 界面完成；Workbench 导出的耦合设置可直接在 SC GUI/CLI 打开执行。GUI/CLI 建耦合需要 Fluent 写出的**参与者设置文件（`.scp`）**。

- **49.2.1 生成 .scp**：File → Export → System Coupling... → **Write SCP File...**（任何时候可写，即使未设 SC 信息）；或 **Auto-write SCP File...**（勾 Auto-write SCP File with Case File 后每次存 case 自动写 .scp）。**Important：2020 R1 起可用单元数据映射表面守恒量（表面力、热流量、体积热率）**——`/define/models/system-coupling-settings/use-face-or-element-based-data-transfer?`；缓解边缘效应与剖面涂抹、提升映射精度；**2020 R1 之前创建的 .scp 建议重新生成**。
- **49.2.2 自定义输入文件**：Execution Control | Fluent Input 对象。**Option** 三值（Table 49.1）：**Initial Case File（默认）**——初始运行按 Case File 设置自动生成 journal；重启用上一轮 case/data；journal 可生成后编辑定制——**一般工作流最佳**；**Initial Case and Data File**——按 Case File + Data File 设置自动生成 journal；输入文件可编辑；**Journal File**——初始与重启都用指定 journal；可加命令；**面向专家用户**。注意：SC 不在启动前校验输入文件；多次重启须保持 case/data 值最新。Option 非 JournalFile 时可用 **GenerateInputFile()** 命令按需生成 journal（例：`GenerateInputFile(ParticipantName = 'FLUENT-2', FileName = 'FluentRestart.jou')`）——遵循 Fluent Input 设置、可设为 Journal File 值。

## 49.3 在 Workbench 中执行（pp. 4857–4858）

把 System Coupling 组件系统连到 Mechanical 系统与 Fluent 流体分析系统。支持参与者：Fluent、Static Structural、Transient Structural、Steady-State Thermal、Transient Thermal、External Data。连接 Fluent 分析系统的 Setup 单元到 SC 系统的 Setup 单元即声明 Fluent 为协同仿真参与者；多数耦合设置在 SC 系统的 Setup UI。运行 = 更新 **SC 系统的 Solution 单元**（不是参与者系统的）。可在 Workbench 外运行：右键 SC Setup 单元 → **Export System Coupling Setup** 导出 .cas/.dat/.scp。**注意：Fluent 系统的改动要传到下游 SC 系统，须保存项目/与 Workbench 同步/关闭 Fluent**——否则运行末尾报 Workbench 状态错误 `Update of the Solution component in System Coupling did not mark container as updated (final state is OutOfDate)`。

## 49.4 可用变量（pp. 4858–4864）

流入边界耦合变量（Tables 49.2–49.4，标注传递方向/张量类型/是否广延量/位置）：
- **Mass Flow Inlet**：输入 Mass Flow Rate（Scalar、Extensive）、Components of Flow Direction（Vector）、TKE/湍流耗散率/比耗散率（k-ε 与 k-ω 均可）、总温/静温（Energy 激活时）；输出 Pressure、Back Flow 总温、Back Flow TKE/TDR/SDR。
- **Velocity Inlet**：输入 Velocity（Vector）、TKE/TDR/SDR、总温/静温；输出 Pressure、Back Flow 总温/TKE/TDR/SDR。
- **Pressure Outlet**：输入 Pressure、Back Flow 总温、Back Flow TKE/TDR/SDR；输出 Mass Flow Rate（Extensive）、Components of Flow Direction（Vector）、Velocity、TKE/TDR/SDR、总温/静温。
- **壁面变量**（Table 49.5）：force（输出）；displacement（输入）；temperature（输入+输出）；heat rate（输入）；heat flow（输入+输出）；heat transfer coefficient（输入+输出）；near wall temperature（输出）。
- **单元区变量**（Table 49.6）：heat rate（输入）；temperature（输入+输出）；Lorentz force（输入）；electrical conductivity（输出）。
- **Porous Jump**（Table 49.7）：force（输出）；displacement（输入）。force/位移分别为矢量 F(Fx,Fy,Fz)/D(Dx,Dy,Dz)。

- **49.4.1 壁面传力**（式 49.1）：=（表压 + 浮动操作压力升 − 参考压力）× 面积矢量 + 黏性力矢量 + 颗粒力矢量。**参考压力 = 0 → 传表压力；= 负操作压力 → 传绝对压力**。**浮力激活时非零操作密度引起的水静压力分量不计入——要包含须把操作密度设 0**。
- **49.4.2 多孔跳跃传力**：①分隔两流区/构成流区内域：传**跳跃净力**（厚度+系数 → 压降 → 力矢量；不含黏性力）。②多孔区-流区之间（上下游流-多孔界面改为 porous jump——多孔区界面不能直连 SC）：面压 → 力矢量（正面压指向多孔区内部；不含黏性力）；**最好零厚度**（无压降；多孔区体积力不传递；适合薄多孔区）；非零厚度时用力取**上游侧面压（压降施加前）**——上游侧一致、下游侧与"压降施加后"的下游流体压不一致（Figure 49.2）。
- **49.4.3 位移**：Fluent 收到的是**当前时间步的增量位移**（相对上一时间步末）；仅可用于勾了 System Coupling MDM 选项且为有效耦合区域的壁面；一般耦合分析中 Fluent 先于或同时于位移发送方求解时，**每耦合步第一次耦合迭代收到的位移为 0 m**。
- **49.4.4 滑移网格区位移**：参与者（如 Mechanical）**不得旋转其网格**——Mechanical 中可用 Rotational Velocity 边界条件。
- **49.4.5 绝对压力示例**：加压海底管道（内 110 bar 绝压、外 100 bar 海水、外水不建模）。操作压力 110 bar 时默认只传局部压力变化——不合物理。做法一：参考压力 −110 bar + Mechanical 外表面加 100 bar——但依赖两个大力精确相消、易受离散误差影响。**最佳做法：操作压力 110 bar + 参考压力 −10 bar**——传递力 = 表压 +10 bar = 内外压差，Mechanical 无需加外压、FSI 界面力最小化。

## 49.5 Fluent 中的耦合相关设置（pp. 4864–4866）

- **双精度**：Launcher 勾 Double Precision（MDM 耦合案例尤其建议）。
- **动网格**：要接收位移的移动/变形壁面勾 System Coupling 选项；Solver Options 选项卡为 SC 边界区（及邻近边界区）选**解稳定化选项**——解对耦合数据特别敏感时启用（不可压缩流体 FSI 常有益）。
- **换热**：接收热数据的壁面勾 via System Coupling；HTC 计算法（Wall Functions/Y plus/默认壁面邻近）与子步选项见 49.1 的 TUI。**双向热耦合收敛慢的典型场景**：第一层网格深入边界层内、近壁温度 ≈ 壁温而非自由流温度——可让 Fluent 基于**常数用户指定参考温度**计算 HTC（定义与场变量 Surface Heat Transfer Coef. 相同）：TUI `.../htc-calculation-methods/use-tref-in-htc-calculation?`，参考温度在 Reference Values 任务页 Temperature 字段设（建议接近自由流温度）；**告诫：耦合壁沿线自由流温度变化强烈时此法不适合**。
- **UDM 自定义传递变量**：Zone-Based Memory Allocation 建 UDM 后经 `define/models/system-coupling-settings/user-defined-coupling-variables-via-udm` 启用为耦合变量。
- **Run Calculation**：瞬态耦合分析的时间步长与时长由 SC 控制——**Fluent 的 Time Step Size 与 Number of Time Steps 均被忽略**；Max Iterations/Time Step = 每耦合迭代的最大非线性求解器迭代数。稳态：Fluent 中指定的迭代数 = 每耦合迭代的最大求解器迭代数（14.5 之前是按耦合迭代均分——`(rpsetvar 'sc/steady/default-iteration-method? #f)` 恢复旧行为）；伪时间法见 p. 3812；稳态动网格见 p. 1988。

## 49.6 Fluent-Mechanical FSI 设置建议（pp. 4866–4881）

- **49.6.1 接触检测**：Mechanical 指物理接触、Fluent 指 surface 逼近（流动封堵 flow blockage）。用于需要封堵流动的 FSI（高柔性阀门等）——两侧施加 offset/proximity 阈值：Fluent 侧阈值（Contact Detection Settings，p. 1954）标记阈值内单元施加流动阻力；Mechanical 侧 offset（Adjust Geometric Modification Settings）把运动边界挡在距周围面一定距离处——既形成流动限制腔、又防网格被夹折；两侧镜像、无需改几何/网格。流程：①Fluent——a. 定封堵距离（可先跑单向 FSI 试验）；b. 设接触检测容差；c. 用 contact marks/zones 封堵；d. 选流动控制方法——**推荐 contact numerics**（标记阈值内单元并封锁流动）；②Mechanical——配置匹配设置。调试：`/define/dynamic-mesh/controls/contact-parameters/render-contact-cells? yes` 渲染接触单元（Contours of → Cell Info → Contact Markings、关 Node Values 核对）；`/define/dynamic-mesh/controls/contact-parameters/verbosity 1` 在 transcript 报告接触建立时刻。
- **49.6.2 动网格设置建议**：**平滑**——一般推荐**基于扩散的平滑 + boundary distance 扩散函数**；扩散参数 α = 1.5 起步（利于远场吸收运动）；边界层变形时增大 α；无需重划时（尤其周期运动）选 Smoothing From Reference Position。**例外**：FSI 边界与非 FSI 边界（如出口）相交、且 FSI 运动切向分量大（如热应力位移）时——扩散平滑把非 FSI 边界节点锁在原曲面上，产生网格皱褶（Figures 49.3–49.5）；改用**线性弹性平滑或 RBF 平滑**并把非 FSI 边界的 geometry definition 设为 unspecified 更好。**重划**——Lmin/Lmax 起点：**0.4 Lmin 与 1.4 Lmax**（全局尺度在 Dynamic Mesh > Settings > Remeshing > Parameters 设；网格尺度查 Mesh Scale Info；局部尺度在各 Dynamic Mesh Zone 的 Meshing Options 选项卡）；所有 Deforming 型 Dynamic Mesh Zone **本地启用重划+平滑**（覆盖毗邻 SC 区域的面）；重划方法须同时选 **Region Face 与 Local Cell**（前者按长度尺度、后者按偏斜度——**不选 Local Cell 就不会触发重划**）；重划单元的偏斜度/尺寸判据**无直接控制**——只能收紧判据间接控制。
- **49.6.3 四类病理与对策**：
  - **前几个耦合步网格折叠**：①定位——开折叠网格 case，绘 Cell Volume 云图、量程上限设 0 只显负体积单元（原因指示：时间步过大或动网格区设置错误；棱柱层折叠见下条）；②开平滑/重划 verbosity 重跑找线索：`/define/dynamic-mesh/controls/smoothing-parameters/verbosity 1` 与 `(rpsetvar 'dynamesh/remesh/verbosity 1)`；**注意：重划没触发时核对 Dynamic Mesh Zones 与长度尺度**（开折叠 case 查网格 min/max 尺度对比重划值；收紧长度尺度与偏斜度因子；增大 Size Remeshing Interval）。
  - **棱柱层变形**：Fluent **不支持重划棱柱层**。三条主对策：①增大扩散参数（边界附近网格变刚、远区吸收运动）；②棱柱层均匀（层数恒定）时**把边界层网格拆成独立 cell zone**；③棱柱层不均匀（小间隙阶梯状）和/或需要接触检测时用 **overset 网格**（复杂拓扑亦推荐）。
    - **49.6.3.2.1 边界层平滑 + Region Face 重划**（近距平移致棱柱层剪切时；Boundary Layer Smoothing 见 p. 1898——把耦合面区的位移矢量施加到边界层区各单元节点；**仅 Spring-based Smoothing 支持**；边界层须独立分区）：①建 Boundary Cell Register（右键 Solution > Cell Registers > New > Boundary；用 Cell Distance、高亮棱柱层所在边界区；单元数 = 棱柱层数）；②Zones > Separate > Cells 按寄存器拆区；③核对拆出内边界层/外边界层/内部三区（Figures 49.8–49.10）；④动网格平滑选 Spring based（他法无 Deform Adjacent Boundary Layer with Zone）；⑤开 Region Face 重划；⑥对称/壁面区**关平滑**（防移动壁邻单元过度拉伸；内部仍平滑）；⑦运动棱柱层 cell zone 在 Dynamic Mesh Zones 设为 **Rigid Body**——刚体区默认需 UDF 定义运动，运动来自 SC 时指派**空 UDF**：`#include "udf.h"` + `DEFINE_GRID_MOTION(dummy_motion, domain, dt, time, dtime) { return; }`；⑧开 **Deform Adjacent Boundary Layer with Zone**（Adjacent Zone 的 Cell Height 无需设——棱柱层不重划）；⑨内部 cell zone 设 Deforming（tri/tet 可重划）。效果：大变形下棱柱层质量保持、仅内部重划（Figure 49.11）。
    - **49.6.3.2.2 Overset 网格**：背景与部件各自独立网格、各自控制重划/平滑（例：结构化六面体背景 + 两部件四面体；Figure 49.12）——单网格时棱柱层随间隙闭合吸收变形而折叠；分开后各部件网格在远场吸收变形再映射回 overset、棱柱层质量保持（Figure 49.13）。流程：①拆分并重划几何；②修时间步——三个时间尺度（仿真/网格变形/overset 网格化，最小者主导）；理想步长使每步相对网格运动不超过 overset 交界处最小单元长度（长度取 overset 重叠区单元）；运动路径上避免网格分辨率大幅变化（会致 overset 界面剧变）——**grid priorities** 可抑制；③选 Overlap Minimization：**基于单元体积**（部件网格近壁细、渐粗到不小于背景时推荐）——`define/overset-interfaces/options/donor-priority-method 0`；**基于边界距离**（重叠网格分辨率均匀且几乎相同时；两壁很近时最合适）——`donor-priority-method 1`；④建 overset 接口并初始化（overset 在初始化时创建；Results > Graphics > Mesh 勾 Overset 查看；诊断见 Diagnosing Overset Interface Issues，p. 1261）。**注意：CFD-Post 不支持 overset——后处理须在 Fluent 内做；overset 体积分对所有求解单元积分——重叠区双重计入、体积分有误**。
  - **内部单元高偏斜/过大过小**：①收紧最小/最大长度尺度与偏斜度判据，并把 Size Remeshing Interval 降到 1（每时间步按尺寸触发重划）；②仍不足则启用 **Region Face Remeshing**（棱柱层与重划区同区时不触发——须先按上法把棱柱层拆独立区并作刚体）；Region Face 重划只按长度尺度拆/删移动边界紧邻单元——对重划单元尺寸控制更强；无直接控制告诫同上。
  - **起跑即封堵致发散**（如阀门初始关闭位带接触）：①零速度初始化流场（也防第一步 FSI 大位移折叠网格）；②进口边界条件斜坡（Velocity/Pressure Inlet，pp. 1462/1452）；③气体（如空气）用**理想气体模型**而非不可压助稳（p. 1685）。注意：这三条都影响解与收敛行为本身。

## 49.7–49.10 执行影响、重启、补丁数据、参与者运行（pp. 4881–4884）

- **49.7**：Fluent 执行被小幅修改以让 SC 管理耦合分析的推进（见 Coupled Analysis Management）。
- **49.8 重启**：耦合分析重启需耦合服务与每个参与者都有对应重启点。**49.8.1**：Fluent 按 SC 请求自动生成 case/data 重启文件（Calculation Activities 的 Autosave Every 手动保存之外额外生成）。**49.8.2 指定重启点**：解更新/重启默认用最后生成的 .cas.h5/.dat.h5；更改：Project Schematic **双击 Solution 单元**（**勿双击 Setup 单元——会还原原始网格与设置**）→ File/Solution Files... 打开重启点列表（默认选最新；单选——先点高亮项取消）→ **务必选与 SC 服务及其他参与者一致的重启点** → Read → Close → File/Close Fluent。**49.8.3 重启前改设置**：在 Fluent 内改（重启用当前重启点 case 中的设置；File/Close Fluent 关闭；提示"修改的网格与设置将用于当前运行"选 OK）或用自定义重启文件（Execution Control | Fluent Input，见 49.2.2）。**49.8.4 Workbench 崩溃后恢复**：`ProjectName_files` 目录存有最新结果与重启点（求解器用 live project 而非临时目录）；`.backup` 目录只存上次保存以来被改文件的原版——可恢复最后保存状态、**不能用于重启分析**。步骤：双击 Fluent Solution 单元 → File/Solution Files... → 崩溃前文件不在列表 → **Recover Missing Solution...** 恢复最新 case/data 并填充列表 → 选重启点 → Read → Close → File/Close Fluent。
- **49.9 补丁数据 case**：重跑前 Clear Generated Data 会连带清掉 Fluent patch 的数据（如 VOF 相分数）。变通（**不适用于 Design Point 更新**）：①Workbench Tools > Options > Fluent 勾 **Enable Generation of Interpolation File**——初始化后写出 `*.ip` 文件；②重跑时在 SC Solution 单元 Clear Generated Data 后：双击 Fluent Setup 单元打开 → File/Interpolate... → Read and Interpolate → Read... 选 *.ip → OK → Close；**读 .ip 后无需再初始化**；关 Fluent 继续重跑。
- **49.10 从 SC GUI/CLI 运行 Fluent 参与者**：SC 界面建的耦合按 Preparing/Setting Up/Changing Data Model Settings 与 Solving a Coupled Analysis 执行；Workbench 建的可导出后经 Running an Exported System Coupling Setup 执行；重启见 Restarting a Coupled Analysis（均属 System Coupling User's Guide）。

## 49.11–49.12 排障与许可（pp. 4885）

- **双向耦合排障文件**（Fluent 运行目录，Workbench 下为设计点目录的 FFF/Fluent）：`cortexerror.log`（同目录所有运行的历史错误汇总——注意只看最近运行的条目；示例：`Update-Dynamic-Mesh failed. Negative cell volume detected.`）；`solution 1.log`（Fluent 中使用了 SC 数据的边界条件信息；不追加——仅当前运行）；`solution.trn`（transcript——当前/最近运行完整演革、判断耦合失败原因最有用；要大量调试输出在设置时输入 `(rpsetvar 'sc/verbosity 1)`）。向 ANSYS 提交服务请求时附全部文件。
- **许可**：每个耦合参与者产品各需其许可；**SC 基础设施本身不需额外许可**（详见 System Coupling User's Guide 的 Coupled Analysis Licensing Requirements）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1，Chapter 49（PDF pp. 4849–4886），批次 133（2026-10-23），SHA-256 校验一致；p. 4886 空白页。
- 式 49.1 与时均公式在抽取文本中符号缺失，记其结构与语义，用时对照原文；Tables 49.1–49.7 字段照录（表中 `k-epsiloin` 为抽取连字伪影，原文为 k-epsilon）；SC 侧行为（数据模型、Workbench 状态）以 System Coupling User's Guide 为准，本页仅录 Fluent 视角。
