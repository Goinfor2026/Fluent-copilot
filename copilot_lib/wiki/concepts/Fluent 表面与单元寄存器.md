---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - surfaces
  - cell-registers
  - postprocessing
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 表面与单元寄存器

## 摘要

User's Guide 2026 R1 Part III / Chapter 40 "Creating Surfaces and Cell Registers for Displaying and Reporting Data"（PDF pp. 4015–4078，三节）。**本页全章完成（批次 109–110，pp. 4015–4078）：40.1–40.3 全三节——表面数据赋值、十四类表面创建与管理（分组/优先级/统计）、七类单元寄存器与操作/后处理。**表面用于 3D 显示与 XY 绘图、面积分报告；单元寄存器用于显示与操作单元分组（显示/自适应/poor mesh numerics/删除/提取/报告）。

## 40.1 表面创建细节（p. 4016–4017）

求解器建表面即构建"表面网格"——小多边形 **Facets**，角点为 **Vertices**（对应 3D 网格的 Cells 与 Nodes）。
- **Facet 值**（源自单元中心值，赋值方式按表面类型）：**后处理表面**（Plane/Iso-surface/Line 等手工创建）——每个 facet 继承其所在 3D 单元的值（恒定于整个 facet、**不做线性插值**、不考虑与单元形心距离）；point surface 取点所在单元的值。**内部区表面**（Interior 等）——facet 是两体单元（c0/c1）界面，取两邻单元**算术平均**。**边界区表面**（Wall/Inlet/Outlet）——只有一侧流体单元、不可平均，**尽可能按边界物理取值**：**主变量**（如固定壁温、指定进口速度）= 边界条件设定值；**因变量** = 直接取相邻内部单元值。
- **Vertex 值**（源自 3D 网格 Node 值）：**内部与边界区表面**——顶点与网格节点重合，取该节点值（共享该节点的全部 3D 单元的加权平均；边界节点可直接取边界条件值）。**后处理表面**——顶点一般不与网格节点重合，**由周围 3D 网格节点线性插值**；单元内部生成的顶点（point surface、line 端点、external/imprint、transformed surfaces）由所在单元全部网格节点插值。

## 40.2 使用表面（pp. 4017–4046）

表面经 ribbon 或 Outline View 右键创建、Results 分支下查看修改；**全部表面存于 case 文件**；**每个边界区自动生成一个 zone surface**。**命名规则：所有表面与 cell register 名必须以字母或下划线开头、不能含斜杠**（名称须以字母开头，数字/其他字符开头被拒绝）。
- 各类表面总览：**Zone Surfaces**（边界显示）；**Partition Surfaces**（并行分区界面）；**Point Surfaces**（单点监视）；**Structural Point Surfaces**（结构模型固体单元内单点监视——如双向 FSI 位移）；**Line and Rake**（释放 pathline、风洞数据对比）；**Plane**（任意平面显示，可一次多面）；**Quadric**（2D 线/圆、3D 平面/球/一般二次曲面显式定义）；**Iso-surfaces**（等值面）。两条显示注意：新表面（除 zone/line/point/rake）可能含错误线条（多面体单元区更常见）——**光照改 Flat 可减轻**；2D 平面类表面侧视会"消失"（无厚度）——显示前在 Mesh Display 开 Edges 则呈线状。
- **40.2.1 Zone Surfaces**：随边界区自动创建（误删才需重建；`surface/reset-zone-surfaces` 重置恢复缺失的表面区）。Domain → Surface → Create → Zone...：选区（可多选）→ 命名（默认与区同名；重名自动加 `zone-surface-N` 前缀；**多选时不能自命名**）→ Create。Manage... 打开 Surfaces 对话框做分组/删除等（p. 4055）。
- **40.2.2 Partition Surfaces**：并行分区边界表面——Partitions 组给 **Int Part**（内部区 ID）与 **Ext Part**（邻区 ID；ID 从 0 到 进程数−1）；Options 勾 **Cells**（含单元）与 **Interior**（内侧；Cells+Interior = 内侧单元、Cells 无 Interior = 外侧单元、不勾 Cells = 界面面——Interior 勾/不勾决定面值取内/外侧单元数据）；命名（默认 `partition-surface-N`）→ Create。
- **40.2.3 Imprint Surfaces（已弃用）**：**弃用特性，可能于未来版本移除**——已从 GUI 移除，仅 TUI `surface/create-imprint-surface` 可用；推荐改用 External Surfaces。流程：yes 读网格文件（.stl/.msh/.cas）→ 路径 → 单位 → 区 ID（不指定则全域压印——大网格耗时）。**告诫**：单位与缩放须与 case 一致；多个不相连源表面应分别建 imprint 再分组。
- **40.2.4 External Surfaces**：读入 **.stl** 外部表面用于可视化；可勾 **Split Surface at Boundaries** 在外部表面与既有域边界的每个相交处自动生成小表面（示例：多管道 case 测单管流量）。步骤：Outline View Surfaces 右键 → New → External Surface → Browse 选 STL → 指定单位 → 勾 Split Surface at Boundaries（可选）→ From Zones 选要导入的单元区 → Create。**重要：外部表面不存入 case 文件——须保留 .stl 且路径正确，否则未来会话不可见**。TUI：`surface/external-surface`。
- **40.2.5 Split Surfaces**：把任意表面在其与边界相交处拆成多个表面（外部表面导入时未拆的，事后用 Split Surface 对话框拆）。Surfaces 右键 → New → Split Surface → 选表面 → **Split**。TUI：`surface/split-surface`。
- **40.2.6 Point Surfaces**：单点监视。**节点值显示为邻近节点值的线性平均；单元值显示点所在单元值**。**不兼容 overset 网格、可能报错误值**。Domain → Surface → Create → Point...：命名（可选）→ 定位三法——鼠标探针右击（探针自动吸附 Node 或 Cell Center，由 Snap on Probe Click 组决定；`surface/closest-point-search` TUI 可启用"吸附到域内最近有效位置"，避免 TUI/GUI 建点失败；Cell Center 模式偶尔吸附到邻单元中心）、移动 point tool（左键按住轴向平移、中球自由移动；Front Faces Transparent 图标便于观察；2D 吸附需显示带面的单元区——仅 default-interior 不够；triad 尺寸在 Preferences → Graphics 的 triad tool size，重启后生效；手输域外坐标点工具会移动但失去交互）、直接输入坐标 → Create。并行下点表面显示问题联系支持。
- **40.2.7 Structural Point Surfaces**：结构模型固体单元内单点监视（**点必须在固体单元区内、且结构模型已启用**——对话框才可用）；节点值=邻近节点线性平均、单元值=所在单元值。Domain → Surface → Create → Structural Point...：命名 → 定位（同三法；**Center 按钮把点工具与坐标移到当前视图中心**）→ Create。
- **40.2.8 Line and Rake Surfaces**：rake = 两端点间等距指定点数；line = 含端点的线（**数据点位于线与单元面相交处、不一定等距**）。Domain → Surface → Create → Line/Rake...：Type 选 Line/Rake → rake 给 Number of Points → 定位三法（端点坐标 x0..z1；Select Points With Mouse 探针取两点；**Line Tool** 交互定位——End Points 先设初值再开 Line Tool；平移：沿红线拖"line"部分（勿点带箭头的轴——那是旋转）、横向平移 Shift+拖；旋转：点白轴带箭头处（绿环→黄环；**勿点红轴旋转**）；缩放：拖端部白矩形；Reset 复位——默认位置沿域中线方向、横跨域该向全幅）→ 命名 → Create。**Line Tool 前置条件：Preferences → Navigation 把 Shift RMB Drag（或类似组合）设为 Probe**。
- **40.2.9 Plane Surfaces**（仅 3D；可一次多面）三种定义：
  - **坐标面**（YZ/ZX/XY Plane）：面上拖 plane tool 至位置（或直接输坐标；Select with Mouse 探针取点）；**一次多面**——增加 Surfaces 数并给 **Spacing**；命名：多面时 Name 变 **Name Format**（默认 `plane-x={x:+.6f}`，生成如 plane-x=+2.325000 的坐标命名；改 6 控制有效位数、f 改 e 为指数记法）。
  - **Point and Normal**：给 Point（坐标或探针）+ Normal（分量或从 surface/view plane 计算）；多面时命名自动加增量（plane-12=0 / =0.01 / =0.02）。
  - **Three Points**：三点定面；可选 **Bounded**（有界平行四边形，四点中三点由所选点确定）、**Sample Points**（面上均匀分布数据点）+ **Sample Density**（Edge1/Edge2 两方向点密度——Edge1 从 point 0 到 1、Edge2 从 point 1 到 2）；多面命名同上。
  - **Plane Tool 按方法不同**：坐标面——沿垂直轴拖动（triad 尺寸同前 Preferences 设置）；Point and Normal——操纵面中部轴三脚（单轴移/抓中心整体挪）；Three Points——中心三脚 + 三个角部三脚（各自面内移动或自由抓取；中心三脚旋转带动其余三个）；多面时第一个面挪位置、最后一个面调间距。
- **40.2.10 Quadric Surfaces**（至 p. 4046 中）：显式定义 2D 线/圆、3D 平面/球/一般二次曲面。Domain → Surface → Create → Quadric...：Type 三选（3D：Plane/Sphere/Quadric；2D：Line/Circle/Quadric）→ 以 SI 单位给定义方程——Line/Plane：ix/iy/iz（法向系数）+ distance（到原点距离），满足 ix·x+iy·y+iz·z=distance 的点集；Circle/Sphere：圆/球心 x0/y0/z0 + 半径 r；Quadric：直接填一般二次函数十系数（x²/y²/z²/xy/yz/zx/x/y/z/常数项）+ 右侧 value。（式中段跨至下批。）

## 40.2.10（续）Quadric Surfaces 尾（p. 4046）

命名（默认 `sphere-slice-N` / `quadric-slice-N`，重名自动给默认名；首字母规则同前）→ Create；Manage... 管理既有表面。

## 40.2.11 Iso-surfaces（pp. 4046–4048）

等值面显示指定变量恒值的单元面——按 x/y/z 坐标生成即得域的横截面、按压力生成可显示等压面上其他变量。可从既有表面或全域生成、可限定单元区、可一次多面（给定间隔）。**前提**：先初始化、算过、或读过 data；**patch 后的等值面须至少推进一次迭代才能正确显示**（或重开对话框点 Save）。Domain → Surface → Create → Iso-Surface...：①Surface of Constant 选变量类别与量（**不支持 Velocity... > Q Criterion Raw 等值面**）；②可选 From Surface（从既有表面生成子面——不选则全域）与 From Zones（限定单元区——不选则穿全域）；③**Compute** 算所选场的 Min/Max；④设 iso-value 两法——滑块交互预览（**滑块显示的是临时面，确认后须点 Create**）或直接输入（**空格分隔多个值——多等值面并成一个表面、不能选择其子面**）；⑤（可选）多面 + Spacing；⑥命名（默认 `z-coordinate-N` 型；多面时名字附按 Spacing 递增的等值）；⑦Create。

## 40.2.12 Clipping Surfaces（pp. 4048–4051）

Iso-Clip：把已有表面按某标量场的指定范围裁剪出新表面（例如外壁面按 x<0 裁剪只显示后半以看到进气道内阀体）。**前提**：先初始化/计算/读 data；patch 后的 iso-clip 同样须推进一步或重开 Iso-Clip 对话框点 Save 才能正确显示。Domain → Surface → Create → Iso-Clip...：①Clip To Values Of 选标量；②Clip Surface 选要裁剪的面；③Compute 算 Min/Max；④定范围两法——Min/Max 表盘指针拖动交互预览（**显示的是临时面，确认后点 Clip**）或直接输入；⑤命名（默认 `clip-density-N` 型）；⑥**Clip**（原表面保持不变）。

## 40.2.13 Transforming Surfaces（pp. 4051–4053）

从既有表面经旋转/平移/等距偏移生成新表面（如叶轮机叶片面旋转到叶间区域绘图；或离原表面恒法向距离的新面）。Domain → Surface → Create → Transform...：①Transform Surface 选面——**用户创建面（line/point/iso 等）不可 transform**（须手动平移输入点后在相应对话框新建）；②变换参数（三者任意组合）——**Rotate**：About 给旋转原点（坐标或 Mouse Select；轴向同全局系；2D 只能绕 z 轴）+ Angles 给绕 x/y/z 角度；**Translate**：x/y/z 平移距离；**Iso-Distance**：法向偏移距离 d；③命名（默认 `transform-N`）；④Create（原面不变）。

## 40.2.14 Expression Volumes（pp. 4053–4055）

表达式体积——按表达式准则约束的域子集；**视上下文表现为面或体**（等值线图中作为 surface、体积报告定义中作为 volume）。两法创建：①cell register 对话框勾 **Create Volume Surface**（等价于 Expression Volume 对话框选 register 后 Create——可在 Outline View Surfaces 下核对其定义）；②**Expression Volume** 对话框（Results → Surfaces → New → Expression-Volume...；详见 Fluent Expressions Language p. 1059）。**2D 专属语义**：体积 = 满足判据的 2D 单元面积之和 × 参考深度；面积 = 满足与不满足判据的 2D 单元之间边长之和 × 参考深度。流程：读 data 或初始化 →（register 路线）建 register 并勾 Create Volume Surface → Expression Volume 对话框输入表达式（示例照录：`StaticPressure<200[Pa]`）→ Create → Outline View 右键 Display 或在各图形对象 Surfaces 列表选用。**重要**：用与建面相同的变量可视化体积面，显示值可能超出建面范围——表达式体积用单元中心值、其表面供可视化用、面上值由单元中心值插值（示例：305–345 K 温度体面显示 300–350 K 范围）。

## 40.2.15 表面管理（pp. 4055–4059）

入口：Outline View 的 Results → Surfaces 分支，或 **Surfaces 对话框**（Domain → Surface → Manage...；亦为各建面对话框的 Manage... 按钮、双击 Surfaces 分支）。
- **40.2.15.1 分组**：多选表面（≥2 才出现 Group 按钮；选第二个面时 Rename 变 Group）→ Name（默认取第一个所选面名）→ **Group**；UnGroup 还原。用途：一次后处理多面（如全部壁面一张温度云图）。
- **40.2.15.2 编辑与重命名**：Outline View 双击面或右键 Edit... 打开对应建面对话框修改并改名；或 Surfaces 对话框选面 → Name 填新名 → **Rename**（多选时无 Rename、只有 Group）。首字母规则同前。
- **40.2.15.3 渲染优先级**：共面多对象显示的 **z-fighting**（棋盘格/缺像素；mesh 对象优先级低于一切图形对象）——选面 → **Rendering Priority** 下拉选优先级（选择即保存）。**不作用于全局网格显示**（mesh display 工具栏按钮、读 case 后自动显示的网格）。
- **40.2.15.4 删除**：选面 → **Delete**（不可逆——删除后须用相应对话框重建）。
- **40.2.15.5 表面统计**：**Points**（表面节点总数）、**0D Facets**（无连接的孤立节点——point surface、rake 节点）、**1D Facets**（2D 问题中的线性面）、**2D Facets**（3D 问题中的三角/四边形面——3D 内部区表面即由 2D facets 构成、2D 内部区由 1D facets 构成）；多选时显示合计。**从 case 读入的表面须先显示才能查统计**。

## 40.3 使用单元寄存器（pp. 4059–4078）

按判据标记单元（等值/边界邻近等），用于**网格自适应、patch、删除单元、提取单元、（经 Create Volume Surface）建可视化体**。七类：Region / Boundary / Variable Limiter / Field Variable / Residuals / Volume / Yplus/Ystar。**注意三条**：多 register 同窗口叠加显示用 View ribbon → Compose... 打开 Scene Description 的 **Overlays**；（并行）同 case 不同核数下 register 精确单元数可能略有差异（不影响结果）；**最多 16 个 cell registers**。
- **40.3.1 Region**：按区域内外标记（形心判定）。形状——2D：**Quad/Circle/Cylinder**；3D：**Hex/Sphere/Cylinder**。Hex/Quad = 对角两点定义（Min/Max 坐标；与坐标轴对齐）；Sphere/Circle = 圆心 + 半径；**Cylinder** = 轴两端点 + 半径（2D 中为任意取向的矩形——长=轴长、宽=直径；与 Quad 矩形的区别在可任意取向 vs 须对齐坐标轴）。Solution → Cell Registers → New → Region...：Inside/Outside 选边 → 选形状 → 输坐标或 **Select Points with Mouse**（右键取点：对角两点任意序；球先取心再取半径处一点；圆柱先取轴两点再取半径处一点；选后可编辑）→（可选）Create Volume Surface → **Save**。Display Options... 改显示方式（各类通用）。
- **40.3.2 Boundary**：边界邻近标记两法——**Cell Distance**（按单元层数）与 **Volume Distance**（目标边界体积 + 生长因子；单元标记按式 40.1：随形心法向距离增长的目标体积 V_n = V_0·f^n 型关系——V 为单元体积、Boundary Volume 为指定边界体积、Growth Factor 为指数生长因子、n 为形心到所选边界的法向距离）。Solution → Cell Registers → New → Boundary...：选距离法 → 给 Number of Cells 或 Boundary Volume + Growth Factor → 选边界区 →（可选）Create Volume Surface → Save。
- **40.3.3 Variable Limiter**：标记**已达解限值**（Solution Limits 对话框所设，p. 3760）的单元。New → Variable Limiter...：选变量 → Save。
- **40.3.4 Field Variable**：按场变量值标记；派生方式四选（**Derivative Option**：None / **Gradient** / **Curvature** / **Hessian**）+ 缩放四选（**Scaling Option**：None / Scale by Global Average / Zone Average / Global Maximum / Zone Maximum）。**四种求导途径**：①**Isovalue**（Eq 40.2；不基于导数——|φ| 经体积与尺寸比因子加权；适合导数无意义的场景如按反应速率标记反应区；可用 custom field function/UDS 自定义判据）；②**Gradient**（Eq 40.3；∇φ 欧氏范数 × 特征长度；梯度体积权重默认 1=完全体积加权、0=无、0–1 比例；**适合强激波如超音速无粘流**）；③**Curvature**（Eq 40.4；未除拉普拉斯算子 × 特征长度的等分布标记；**适合光滑解**）；④**Hessian**（Eq 40.5；基于解的二阶导与局部插值误差关系（精确解 vs 近似解 + Hessian 矩阵）——外流气动自适应常用（见 39.2.1.2）；可跨尺度多强度探测多种流动特征、以更低计算成本定位精度提升点）。任何可用于等值线显示的场变量都能用于标记（含单元体积场——减小单元体积剧变）。**Type 十种**：Min/Max Value Cells（含最小/最大值的单元）、Cells Less Than / More Than（阈值上下）、Top Value Cells / Low Value Cells（最高/最低 n%）、Cells Inside/Outside Range（区间内外）、Cells Inside/Outside Standard Deviation Range（标准差范围内外——Lower/Upper Limit Factor × 标准差 + 平均值定区间）、Cells Less/More Than Standard Deviation Limit（标准差限上下——Limit Factor 同理）。**Compute** 可算最小/最大/平均/标准差及相应范围。**Hessian 建议**：同时选 **Scale by Global Average**（相对值按局部网格尺寸缩放）。（可选）Create Volume Surface → Save。
- **40.3.5 Residuals**：按残差标记高残差单元定位问题区。**仅压力基可用**。New → Residuals...：选 Equation(s) → 给 **Threshold Percent**（所选方程残差超过该百分比阈值的单元被标记）→ Save。
- **40.3.6 Volume**：按单元体积标记——**Magnitude**（大于阈值的单元——识别大单元）或 **Change**（相邻单元体积比超阈值——识别需平滑区；逐面比较 V1/V2 与 V2/V1，超阈标记）。New → Volume...：选法 → 给 Min Volume 或 Max Volume Change（Compute 可算最小/最大单元体积）→ Save。
- **40.3.7 Yplus/Ystar**：按壁面 y+/y* 标记——**总是限定在所选黏性壁面第一层面连接单元**。New → Yplus/Ystar...：选 Yplus 或 Ystar → 选 Wall Zones → 给 Mark 1st Layer Cells Below / Above 值（Compute 算 min/max）→ Save。
- **40.3.8 管理**：Solution → Cell Registers → Edit...——Manage Cell Registers 对话框查看属性/显示/编辑/删除，New 建新。
- **40.3.9 寄存器操作（报告）**：Solution → Calculation Activities → Cell Register Operations → **New Report...**（须已有 register）——选寄存器、报告 **Frequency**、最大单元数 → Save；Manage Register Operations 对话框（... → Edit...）查看/建/改/删。
- **40.3.10 复制与重命名**：Outline View 右键寄存器 → **Copy...** 改名保存（建相似寄存器）；重命名——选中后单击或 F2 编辑，或在对话框改名 Save。
- **40.3.11 后处理显示**：建 register → 初始化 → Contours 对话框（Results → Graphics → Contours → New...）——Contours of 选 **Cell Registers...** + register 名 → 选 Surfaces → **关闭 Node Values** → Save/Display。register 内单元值为 **1**（field variable register 显示场变量值），其余单元为 0。

**Ch.40 全章完成（pp. 4015–4078）。**

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 4015–4046（批次 109，2026-10-20，pypdf layout 模式提取）。
- 二次曲面方程的符号占位（ix·x+iy·y+iz·z、(x−x0)²+…=r²、一般二次式）在文本层缺失，按数学语义补记；工具操作细节（拖拽/旋转交互）按原文照录摘要。
- Figures 40.1–40.22（界面与示意图）为图形元素未摄取。
- 版本敏感：Imprint Surface 弃用状态、外部表面不存 case、多面命名格式以 2026 R1 为准。
- 相关页面：[[Fluent 网格自适应]]（register 用于自适应）、[[Fluent 求解器使用]]（Structural Point）、[[Fluent GPU 求解器]]（GPU 监视器不支持 Iso-clips/Zone/Quadric 面）。
