---
type: concept
created: 2026-10-17
updated: 2026-10-17
tags:
  - Ansys Fluent
  - mesh
  - topology
  - mesh-quality
  - solution-mode
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 网格读取与操作

## 摘要

User's Guide 2026 R1 Part III / Chapter 7 "Reading and Manipulating Meshes"（PDF pp. 1169–1346，共 12 节）讲 solution 模式的网格读入、检查与操作。**本页已覆盖全章（批次 34–38，pp. 1169–1346）**：非结构求解器不强加拓扑、悬挂节点默认读入时转多面体、face-node 连接约定、按几何复杂度选型、质量定义与手册阈值、网格来源与拼接、参考帧、曲线坐标系、非一致网格接口、Overset 网格、Gap Model、网格检查/修复、网格统计报告、多面体转换与全部 22 种网格修改操作。章首概览：3D 网格可转多面体（纯 hex 网格除外，转换时 hex 单元保持不变）；可查内存、simplex/拓扑/域信息、节点/面/单元数、最小最大单元体积等诊断。

## 章节地图（12 节 → PDF 起始页）

- 7.1 Mesh Topologies（1169）；7.2 Mesh Requirements and Considerations（1186）；7.3 Mesh Sources（1191）；7.4 Reference Frames（1202）；7.5 Curvilinear Coordinate Systems（1206）；7.6 Non-Conformal Meshes（1212）；7.7 Overset Meshes（1250）；7.8 Controlling Flow in Narrow Gaps（1279）；7.9 Checking the Mesh（1290）；7.10 Reporting Mesh Statistics（1296）；7.11 Converting the Mesh to a Polyhedral Mesh；7.12 Modifying the Mesh。
- 自适应与并行分区在别的章：Adapting the Mesh（p. 3975）、Mesh Partitioning and Load Balancing（p. 4546），未摄取。

## 7.1 网格拓扑（pp. 1169–1185）

- **非结构求解器**：用内部数据结构给单元/面/节点排序并维护相邻单元连接，不需要 i,j,k 索引——求解器不强加整体结构，可自由选最优拓扑。
- **接受单元**：2D quad/tri/poly；3D hex/tet/pyramid/wedge/poly。单块与多块结构网格、含上述单元的混合网格均可；非一致边界网格（子域交界处节点不重合）也可。
- **悬挂节点/悬挂边**：可接受，但 2D 与 3D 默认在读取时把相邻单元自动转成多面体以消除（转换后单元总尺寸不变、面数可能增加）。读取前用 `file/convert-hanging-nodes-during-read? no` 可关闭；关闭后若 interior wall 上有悬挂节点/边会报错——三种触发情形：读入带 interior（two-sided）wall 边界但 shadow wall 尚未创建；把 interior 面转成 wall；slit interior 面（改为非一致界面）。hexcore/CutCell 网格常见此问题。读入后补救（3D）：`mesh/polyhedra/convert-hanging-nodes`（详见 7.3.10 限制）。
- **7.1.1 可接受拓扑示例**（pp. 1171–1176，Figures 7.2–7.13）：O 型（不要求 cyclic branch cut，但接受带 cut 的）、零厚度壁面、C 型、保形块结构、多块结构、非一致、非结构 tri/tet/quad/hex/poly。
- **7.1.2 face-node 连接**（pp. 1176–1184；与 Fluent 接口对接时使用）：

| 单元 | 面 → 关联节点（Face 1, 2, …） |
|---|---|
| 三角形 | 1-2；2-3；3-1 |
| 四边形 | 1-2；2-3；3-4；4-1 |
| 四面体 | 4-3-2；3-4-1；2-1-4；3-1-2 |
| 楔形 | 1-2-3；1-4-5-2；2-5-6-3；3-6-4-1；4-6-5 |
| 金字塔 | 1-2-3-4；1-5-2；2-5-3；3-5-4；4-5-1 |
| 六面体 | 1-2-3-4；1-5-6-2；2-6-7-3；4-3-7-8；1-4-8-5；5-8-7-6 |
| 2D 多面体（五边形例） | 1-2；2-3；3-4；4-5；5-1 |

  **3D 多面体单元没有显式 face/node 编号**（p. 1184）。
- **7.1.3 选型**（pp. 1184–1186）三考量与推荐实践：
  - *setup time*：复杂几何建结构/块结构网格极耗时甚至不可行——是非结构 tri/tet 的主要动机；几何简单时两者无节省。结构网格用于复杂几何的风险：几何过度简化、质量问题、分布低效（不重要区过密）→ 单元数偏高。已有结构网格（含 FLUENT 4，经过滤器）直接复用可省时。
  - *computational expense*：tri/tet 可在选定区域聚类 → 复杂几何或流动尺度范围大时单元远少于等效 quad/hex；quad/hex 允许大得多的长宽比（tri/tet 大长宽比必然恶化 skewness，妨碍精度与收敛）——细长管道等流动贴合几何的情形用高长宽比 quad/hex 单元更省。tet 全域转多面体：单元数更低、网格更粗，但收敛通常更快。
  - *推荐组合*：简单几何 → quad/hex；中等复杂 → 非结构 quad/hex；较复杂 → tri/tet + 边界层楔形单元；极复杂 → 纯 tri/tet。
  - *numerical diffusion（false diffusion）*：真实扩散小（对流主导）时最显著；一切实用格式都含有限数值扩散（源于离散化截断误差）；二阶与 MUSCL 格式可减轻；数值扩散与网格分辨率成反比（细化可缓解）；**流动与网格对齐时最小**——tri/tet 永远无法对齐，quad/hex 仅在简单流动（细长管道）可对齐，此时用更少单元获得更好解；需要垂直壁面方向更高分辨率 → 壁面附近建高长宽比 prism 层。

## 7.2 网格要求与质量（pp. 1186–1191）

- **几何要求**（7.2.1）：轴对称几何的旋转轴必须是定义几何所用笛卡尔坐标系的 x 轴。周期边界可用保形或非保形周期区：保形周期区两区网格必须相同（meshing 模式或 GAMBIT 建网格时生成）；solution 模式可从两个保形区创建周期区对，也可从非保形区创建周期界面（CAD 无法产生真周期边界时必需）→ Creating Periodic Zones and Interfaces（p. 1315）。
- **正交性定义**（7.2.2，p. 1187–1188）：对每个面计算两个归一化点积——面面积向量与（单元质心→面质心）向量（Eq 7.1）；面面积向量与（单元质心→相邻单元质心）向量（Eq 7.2）；全部面取最小值 = 单元 orthogonality。最差单元接近 0、最好接近 1。
- **正交质量（orthogonal quality）默认按单元类型**：tet/prism/pyramid 取 min(orthogonality, 1−skewness)；hex/poly 即 orthogonality。可用 `mesh/enhanced-orthogonal-quality?` 启用增强定义：综合面正交性、局部边缘劣形（扭曲/凹性）检测与面法向变化——**最适合薄 prism 单元评估**。
- **长宽比（aspect ratio）**：单元质心→各面质心的法向距离（距离向量与面法向的点积）与质心→各节点距离中的最大值/最小值之比；单位立方体为 1.732；适用于任何网格类型含多面体。
- **检查入口**：Setup → General → Report Quality（控制台输出最小正交质量与最大长宽比）；需更多信息（附加指标 + 最差单元所在 zone）先设 `mesh/check-verbosity` 为 3（有效值 0–3）再点 Report Quality；按 cell zone 诊断：Setup → Cell Zone Conditions → <zone type> → Info。改善劣质单元见 Repairing Meshes（p. 1293）；耦合双面 wall 附近面正交性差时的防发散见 Orthogonality-Based Secondary Gradient Limiting（p. 1525）。
- **手册明确给出的阈值/经验值**：
  - 最小正交质量：所有单元类型 **> 0.01**，平均值应显著更高。
  - 偏斜度（skewness，与等体积正则单元形状之差）：最优 quad 顶角近 90°；tri 近 60° 且所有角 < 90°；**tri/tet 网格最大偏斜度多数流动应 < 0.95**（平均显著更低）——超过 0.95 可能收敛困难，需减小欠松弛因子和/或改用 pressure-based coupled solver。
  - 长宽比：强各向异性流动中大长宽比可用更少单元得准确结果；但在流动变化/梯度大的区域避免长宽比突变。
  - 任何流动通道**不少于 5 个单元**（多数情形需远多于 5）。
  - 单元尺寸变化与面 warp 是影响稳定性/精度的额外指标（详见 Fluent Meshing 部分）。
- **单元分布**（7.2.2.1）：剪切层、分离区、激波、边界层、混合区等流动特征的分辨率决定精度；逆压梯度分离预测强依赖分离点上游边界层分辨率；壁面间距直接影响壁面剪应力与换热系数——层流要求 **Eq 7.3：y_p·√(u_∞/(ν·x)) ≤ 1**（y_p = 相邻单元质心到壁面距离，u_∞ = 自由来流速度，ν = 运动黏度，x = 沿壁面距边界层起点距离；基于零攻角平板层流 Blasius 解，文献 [139]；公式体经 500 dpi 渲染核对）。湍流按所用近壁模型查 Model Hierarchy（p. 2144）。精度随网格数上升但 CPU/内存同步上升；解自适应细化可按演化流场增减密度 → Adapting the Mesh（p. 3975）。
- **光顺度**（7.2.2.3）：相邻单元体积剧变 → 截断误差增大；可按单元体积或体积梯度标记后细化。**流动场依赖性**（7.2.2.4）：歪斜单元在流动平缓区可容忍、强梯度区危害大；强梯度位置无法先验确定 → 应追求全域高质量网格。

## 7.3 网格来源（pp. 1191–1201）

- **来源清单**（p. 1191）：Ansys Meshing、Fluent meshing 模式、（v14.5 前独立的）Fluent Meshing、GAMBIT、GeoMesh、ICEM CFD、NASTRAN、ARIES、CFX、TurboGrid 及其他前处理器；也可用 Fluent/UNS 或 RAMPANT 网格、拼接多个网格文件。GAMBIT 导出 Fluent 5/6 格式；GeoMesh 的 3D tet 需把表面网格读入 meshing 模式补生成体网格；多数来源经 File/Read/Mesh... 读入。
- **NASTRAN 三条导入路径**（7.3.6）：① meshing 模式导入（遵循 Part II Appendix B 限制）；② solution 模式 File/Import/NASTRAN 直接导入（限线性 tri/quad/tet/wedge/hex 单元）；③ fe2ram 转换后读入。用后两法读入 tri/tet 体网格后建议做 Quality-Based Smoothing（p. 1339）。识别的 Bulk Data 条目：GRID（单精度节点）、GRID*（双精度）、CBAR（线单元）、CTETRA/CTRIA3（tet/tri）、CHEXA/CQUAD4/CPENTA（hex/quad/wedge）；**2D 体网格单元须位于同一 z = 常数平面**（p. 1193；缺失符号经 500 dpi 渲染核对为 z）；重复/重合节点须在 NASTRAN 端删除后再导出。
- **CFX 文件**（7.3.7，.def/.result）：**只导入网格，不带任何结果/数据**。分区方式二选一：默认 Create Zones from CCL Physics Data（"Zoning by CCL"——按物理数据对象建 zone，**不导入 CFX subdomain 区**）；关闭该选项则按 primitive mesh region 分组（"Zoning by Group"——可导入 subdomain 区；primitive 拓扑可能含物理定义之外的多余区）。单元集 → cell zone（tet/pyramid/wedge/hex）；边界区保留边界条件名/类型：inlet、outlet、symmetry、interface、wall。interface 可保形或非保形：非保形保留；保形 interface 的重合节点被合并并转为 Interior（必要时调 merge 容差，或改用 Fusing Face Zones，p. 1313）。
- **TurboGrid**（7.3.8）：.gtm 与 .defTurboGrid 可读入多个但一次一个；File/Import/TurboGrid...，或 Domain → Zones → Append → Append Case File...（可多次追加）。
- **fe2ram**（7.3.9）：`utility fe2ram [dimension] format [zoning] input_file output_file`；2D 加 `-d2`（3D 缺省不填）；format 如 `-tANSYS`/`-tIDEAS`/`-tNASTRAN`/`-tFIDAP7`（`utility fe2ram -cl -help` 列出全部）；zoning：`-zID`（按属性 ID）/`-zNONE`（忽略分组）/缺省按 group；**输出不得为 CFF（.msh.h5）；不支持 VRML 2.0 及以后**。示例：`utility fe2ram -d2 -tIDEAS sample.unv sample.msh`。命令行全参数与各格式要求详见 [[Fluent 第三方网格导入与 fe2ram 过滤器]]。
- **多文件读取三法**（7.3.13）：① solution 模式——先 File/Read/Mesh... 读第一个，再 Domain → Zones → Append → Append Case File... 追加（Append Case & Data Files... 连数据一起追加）；**append 后、计算前复查 case 设置**。② meshing 模式——依次读入自动合并成单一网格后保存。③ tmerge——启动前合并 legacy .msh（**不支持 CFF 文件**），合并前可对各文件做旋转/缩放/平移，内存占用很低；`utility tmerge -3d` 或 `-2d`，交互输入文件名与变换参数（`utility tmerge -h` 看全部选项）。多个网格交界处节点无需重合（非一致接口可处理）。保形网格若不想要相邻区之间的边界 → Fusing Face Zones（p. 1313；匹配面移入新 interior 区，原区丢弃）；**计划用滑动网格或存在非一致边界时不要合并重叠区**，改边界类型后按非一致流程设置。
- **悬挂节点转换产物（多面体）的限制**（7.3.10.1）：不可用 modify-zone 下的 extrude-face-zone、skewness smoothing、swapping（对 poly 单元无效）；不可用 hanging-node 法自适应（但默认的 PUMA 法可以）；动网格：所有 remeshing 方法都不会修改 poly 单元，光顺允许且推荐径向基函数（RBF）光顺，线弹性固体光顺不兼容 poly。
- **表面网格文件**（7.3.14）：作几何自适应的背景网格。PUMA 法（2D/3D 默认）：Auxiliary Geometry Definition 对话框 → Type 选 Surface Mesh → Surfaces Meshes...；hanging node 法：Geometry Based Adaption 对话框启用 Reconstruct Geometry → Surfaces Meshes...；Read... 选文件并指定单位（默认米）；同对话框可显示/删除面。读入后的自适应设置（p. 1202）：PUMA 3D 在 General Adaption Controls 启用 Reconstruct Geometry 并经 Manage Geometry-Based Adaption 设置，2D 用 `mesh/adapt/geometry/reconstruct-geometry` 与 `mesh/adapt/geometry/manage`；hanging node 法在 Geometry Based Adaption 对话框 Wall Zones 列表选区 → Set...；之后按 Refining and Coarsening（p. 3979）执行。

## 7.4 参考帧（Reference Frames，pp. 1202–1206）

- 用途：创建多个局部坐标系（含位置与朝向，可带运动可不带）；没有它，点表面、profile、喷射等只能按全局坐标系指定。
- **创建**：Outline View 右键 Reference Frames → New...（Setup → Reference Frames → New...）。命名后二选一定义方式：**User Defined**（完全指定位置/朝向/运动；需选 Parent reference frame）或 **Track by Zone**（"附着"到某个 cell zone，可指定位置与朝向但**不能指定运动**，随所跟踪 zone 移动；需选被跟踪的 Cell Zone/Dynamic Zone）。
- **运动设置**（仅 User Defined，Motion 选项卡）：Motion Type 二选一——**Constant Velocity**（Linear Velocity 与 Rotational Velocity，均相对 parent reference frame 朝向）或 **Motion Definition**（选已定义的运动定义，可用表达式/输入参数定义 → Managing Motion Definitions，p. 1851）。
- **Initial State 选项卡**：Origin；Axis-1 Orientation（选 X/Y/Z 轴，用点或方向指定）；可选 Axis-2 Orientation（默认 Automatic 自动给出，可关闭手动指定）。
- **图形显示与状态**：创建后图形窗口显示 triad（三脚架），默认显示 Current 状态（瞬态计算中随动参考帧移动）；对话框底部 Display State 可切 Initial；Initial State / Current State 选项卡查看相对全局系的值。
- **Important**：在 Reference Frame 对话框点 OK 会**把参考帧重定义为对话框当前可编辑设置**（Current State 被设为 Initial State 选项卡的值）；不打算改动时用 Cancel 退出。
- **使用位置**：定义 point surfaces、profiles、profile 文件、injections、motion definitions 时可在相应对话框的 Reference Frame 下拉中选局部参考帧。

## 7.5 曲线坐标系（CCS，pp. 1206–1212）

- 用途：创建跟随模型几何的局部坐标系（如沿电机绕组弯曲方向），**最典型用于各向异性导热**（→ p. 2248）。Setup → Curvilinear Coordinate System → New...。
- 定义：命名；选择适用的 cell zones；**Direction 0 与 1 必须指定，Direction 2 = 0 与 1 的叉积自动得出**。方向定义三种 Method：
  - **Diffusion**：用 Start 与 End face zones 指定矢量场方向；闭环几何可用 **Jump boundary**——指定一个耦合 wall 作为环的横截面，拆成 start/end 两面。
  - **Base Vector**：已知某方向在全几何上与全局坐标轴对齐时，直接给用户矢量。
  - **Vector Projection**（**仅 Direction 1 可用**）：给 Alignment Vector 的 X/Y/Z 分量，方向 = 该矢量在主矢量场（Direction 0）上的投影。Important：精度取决于 Alignment Vector 与 Direction 0，**务必可视化核验**。
- 可视化选项：Direction 0/1/2 显示开关、Auto Scale、Draw Mesh、Scale、Skip（抽稀）；Note：方向矢量不会在所有内部边界上显示。
- **7.5.2 线圈示例**：Direction 0 用 Diffusion（两端圆面作 Start/End）；Direction 1 无法用 Diffusion（只有圆柱面、无端面），Base Vector (0,0,1) 也不贴合弯曲——应用 **Vector Projection (0,0,1)**，使 Direction 1 垂直于 Direction 0。
- **限制**（7.5.3）：含多孔区时 CCS 不支持变形/网格运动（多孔存在时无法重算 CCS）；周期边界 face zone 不会出现在 Jump 条件 Start/End 面的可选列表中。
- **Jump boundary 限制**（7.5.4）：仅对闭环几何有效（开口几何会得到错误结果）；每个闭环**最多一个** jump boundary；同一闭环内多个耦合 wall 若 thread ID 相同，在其中一个上指定 jump 会使全部变成 jump（无效）——同一 thread ID 的多个闭环也只能选一个耦合 wall 作 jump；各闭环 thread ID 不同时则可每环各选一个。

## 7.6 非一致网格（Non-Conformal Meshes，pp. 1212–1249）

### 计算方式与六种接口选项（7.6.1）

- 非一致界面 = 相邻 cell zone 交界处节点不重合的边界，-zone 间仍可传递通量。Fluent 先求两 interface zone 的**交线**：同材料 solid-solid 或 fluid-fluid 界面 → 重叠区生成 **interior zone**；异材料 solid-solid 或 fluid-solid → 默认按 **coupled wall** 处理。部分重叠时默认为不重叠部分创建 **non-overlapping zones**（类型与设置可改）。通量用**交线产生的面**计算，不用原界面网格面（2D 示例 pp. 1213）。
- 六选项：**Periodic Boundary Condition / Periodic Repeats / Coupled Wall / Matching / Mapped / Static**。Note：**默认 one-to-one 方式创建的接口只有 Coupled Wall 选项可用**。
- **Periodic BC**（7.6.1.1）：实现非一致周期边界——两区节点不必一一对应；两区不空间重叠，把第一区节点平移/旋转"periodic offset"到第二区上，在合并节点集间生成新面再应用于原区。启用 Periodic BC 时 **Matching 默认同时启用**。
- **Periodic Repeats**（7.6.1.2）：当各 interface zone 与一对保形周期区或非一致周期界面相邻时适用；重叠部分正常耦合，非重叠部分按 periodic offset 平移/旋转通量后相互耦合；典型与滑移网格联用（转子-静子界面）。**interface zone 与 solid zone 相邻时不支持**。
- **Coupled Wall**（7.6.1.3）：界面作 wall（不过流）但传热耦合；异材料 solid-solid / fluid-solid 默认即此，fluid-fluid 需手动启用（模拟薄壁/挡板）。可与 Periodic Repeats 同时启用。
- **Matching**（7.6.1.4）：只要内部区（interior 或 wall/shadow 对）、不生成多余 wall 区；两侧完全重叠时推荐。Fluent 会检查 zone 穿透，matching 与 non-matching 的可容忍度不同，过严重时报消息。
- **Mapped**（7.6.1.5）：耦合 wall 的替代法，专治界面穿透/间隙（标准公式会因此产生左手面而失败）；启用 Mapped 自动启用 Coupled Wall。质量不达标时用 `define/mesh-interface/improve-quality` 调大容差。v19.2 及更早建立的 CHT mapped 接口建议切 `/define/models/cht/implicit-coupling?`（隐式现为默认、收敛更好）。**限制**：至少一侧全为 solid zone；不兼容 shell conduction；Eulerian 多相不在 mapped 界面做热耦合；除 Coupled Wall 外不能组合其他选项；S2S 的 Face-to-Face 视角因子不兼容多面体 mapped 界面；**不支持基于密度求解器、Lagrangian DPM、运动/变形网格**。
- **Static**（7.6.1.6）：默认会为界面可能发生的运动/变形预建额外 zone；确定界面两侧**永无相对运动/变形**时启用 Static 可省内存与时间（区很多时节省显著）。Warning：用在实际会相对运动/变形的界面上**结果错误**。不限稳态。

### 自动命名规则（7.6.1.7）

- 占位符：`<mesh interface name>`（用户指定或前缀）、`<connection number side 1/2>`（两侧 zone 序号）、`<side number>`（1 或 2）。
- 默认：non-overlapping = `<interface zone name>-non-overlapping`；interface wall 侧 1 = `<name>-wall1-<c1>-<c2>`、侧 2 加 `-shadow`；interior（one-to-one）= `<mesh interface name>`；interior（many-to-many）= `<name>-interior-<c1>-<c2>`。
- Periodic BC：interior = `<name>`；Periodic Repeats：interior = `<name>-periodic`（且可能创建**用户不可改名/修改的未命名 zone**）；Matching 同默认 interior 规则；Coupled Wall one-to-one = `<name>` 与 `<name>-shadow`、many-to-many 同默认 wall 规则；Mapped wall = `<name>-wall<side>-<c1>-<c2>`；**Static 不影响命名**。

### 算法（7.6.2）

- 三种实现：Coupled Wall 用 **interface boundary metrics**；Mapped 用 **projection approach**——两者都稳健、避免产生左手面。其余类型用 **virtual polygon approach**（存储多边形面的面积向量与质心；无节点移动、单元不必然水密，梯度对缺失面面积作修正；瞬态中静止 NCI 在网格更新时自动保留）。
- 沿革：≤16.0 全用 virtual polygon；6.1 及更早用三角面法（有节点移动、需水密、欠稳定）。16.0 前的 case 现版本可正常运行，**重建接口时**才换算法：coupled wall → interface boundary metrics，其余 → virtual polygon。
- 滑移网格界面匹配差会产生左手面：Fluent 自动尝试扶正，残留用 `define/mesh-interfaces/remove-left-handed-interface-faces?` 删除；尖锐边角几何也会产生左手 cell——应先分离 zone 再分别建界面。重建 face-periodic 界面可能需在控制台补输入 angle/translation vector；现行并行算法无需 encapsulation。

### 要求与限制（7.6.3）

- 界面形状任意（3D 可非平面），但两侧须基于同一几何；有尖锐特征/曲率时两侧网格都必须贴紧该特征。**两界面间最大容差不得大于该处相邻单元尺寸——不允许有单元被完全封闭在两界面之间**。
- 后处理：one-to-one 的 NCI 面可参与后处理（non-overlapping 面仅当相对父面足够大时才显示/计入积分，否则用父面）；**many-to-many 的 NCI 面不参与后处理（显示为零，父 wall 非零）**。
- 单一网格内多个 cell zone 以非一致边界分隔时，每个 cell zone 在该边界上必须有**独立 face zone**（位置形状相同、归属不同）——可 Disconnecting Cell Zones（p. 1313）或分文件后合并（p. 1197）。
- 周期区必须先正确定向（旋转/平移）再建界面。Periodic BC/Repeats 有效的前提：第二区边界相对第一区**均匀**偏移（等距平移或等角旋转）；Periodic BC 另要求旋转周期角能整除 360。Periodic Repeats 要求两区有部分重叠、且非重叠部分形状尺寸全同（滑移网格须在全程保持）。3D 中每个 interface zone 相邻的保形周期区对**最多一对**。
- 不允许单个界面一部分是耦合双面 wall、另一部分是普通耦合——必须拆成两个界面。Fluent/Mechanical/Meshing 联用时一个 Fluent zone 只能属于一个 contact region。**3D fan zone 不能有非一致界面**。把含 NCI 的 case 读入 meshing 模式再切回 solution：zone ID 可能对应但名字不一致、intersected thread 上的边界条件不保留、悬空 NCI 面仍存在。

### 使用流程（7.6.4）

1. 读入网格（多文件先合并）；2. 改组成非一致边界的 zone 类型：one-to-one + 对话框 → interface 或 wall，右键/`define/mesh-interfaces/create` → 任意外部边界类型，many-to-many → 全部 interface；3. 默认 one-to-one 配对法，优点：单一边界 zone 可进入多个界面（无需在 meshing 拆大 zone——拆分会损质量且多面体网格不可拆）、可选 wall 等外部边界类型、可配对完全无重叠的两区（滑移网格起始无重叠）、可直接选 cell zone（等价选其全部 wall/interface 面）；局限：创建时几乎不能带选项（仅单对时可手动启用 Matching；固-固异材/固-流自动启用 Coupled Wall）、创建后只能改名和加耦合 wall。切换法：`define/mesh-interfaces/one-to-one-pairing?`——同一 case 所有接口应用同一方法，切换时提示删除（转 many-to-many）或转换（转 one-to-one，不兼容设置被禁用；适合升级旧 case）。
4. one-to-one 可选设置（均在 `define/mesh-interfaces/auto-options/` 下）：`set-exclusion-pairs`（排除指定配对，须偶数个 zone）、`naming-option`（后缀用 zone 名/ID/相邻 cell zone 名/省略）、`set-default-name-prefix`、`coupled-interfaces-inherit-bcs?`（固-固异材/固-流建耦合 wall 时继承原 BC）、`pairing-between-different-cell-zones-only?`、`set-one-to-one-pairing-tolerance`（绝对容差或相对长度因子×界面最大网格尺度；面积过大/误配对→调小，缺界面/面积偏小→调大）、`set-minimum-area` / `set-minimum-area-percentage`（自动创建后删除小于阈值的配对；面积百分比两侧都低于阈值才删；默认 0 不删——滑移网格起始重叠小时注意别误删）、`order-interface-lists-by-area?`（默认按面积百分比排序）。
5–7. 创建入口：Setup → Mesh Interfaces → New... 打开 Mesh Interfaces 对话框。**周期/周期重复接口必须先禁 one-to-one 再 Manual Create...**（→ 多对多手动法）；其余接口用 one-to-one 手动法或**自动法**——自动法在对话框中选区（可含 cell zone；区名旁方括号数字 = 已属界面数，多界面归属仅 one-to-one 支持）→ 输 Interface Name Prefix → Create；可选 Interface Creation Options 对话框批量套 Mapped（仅一侧全 solid 的界面，不看质量、容差取全局）与 Static（确知无相对运动才启用，创建前启用才省内存）。控制台输出各界面面积百分比及 **over-intersected 边界区指标**（单面交叠总面积 > 面面积 × 1.25 即 over-intersected；需排查）。
8–12. 管理：Outline View 的 Setup / Mesh Interfaces 节点（右键 Delete All / List / Group By 按列表视图、名字、相邻 cell zone、两侧材料、zone 类型分组；Show non-overlapping boundaries 开关，或 Preferences → Appearance 的同名选项）或对话框 Toggle Tree View。one-to-one 编辑仅限改名（Edit...）与把 interface interior zone 右键 Type → wall（做成流-流热耦合墙；固-固异材/固-流默认已耦合无需操作）。many-to-many（禁 one-to-one 时）经 Edit Mesh Interfaces 对话框可改 Coupled Wall / Matching / Mapped（+Enable Local Tolerance 覆盖全局容差）/ Static（仅兼容 Coupled Wall 与/或 Matching）；名称与 zone 仅单选界面且 zone 未指派时可改；**Periodic BC 与 Periodic Repeats 不能在编辑中切换——须删除重建**；Periodic BC 的 Type/Offset 可改（Offset 须先关 Auto Compute Offset）。界面生成/删除会连带创建/删除附加 wall/interior zone：部分重叠时检查 non-overlapping zone 的类型与设置（删 one-to-one 界面时其类型与设置回写到父边界 zone）；耦合 wall 界面在 Boundary Conditions 任务页定义边界条件。
13. 初始化并复查：显示 **Interface Overlap Fraction**（Contours 的 Mesh... 类）云图核查；one-to-one 可右键显示 intersected zone（创建时生成的 interior 或耦合 wall，代表重叠面积；non-overlapping 显示在交界处是近似的）；List 按钮或 `define/mesh-interfaces/list` 输出各 zone 面积与面积百分比（界面面积/各侧边界面积；最后一行给两侧百分比）。one-to-one 可用 `define/mesh-interfaces/delete-interfaces-with-small-overlap` 批删小重叠界面（面积和/或百分比阈值；两侧百分比均低于阈值才删）。
14. 动网格运动传递：仅一侧用 User-Defined Motion 或 System Coupling Motion 指定运动时，默认自动把运动插值传到被动侧以维持耦合；`define/mesh-interfaces/transfer-motion-across-interfaces?` 可改法或关闭（关闭后两侧可能分离/穿透 → 收敛困难或网格失效）。两法：**transfer-displacements**（默认；逆距离加权插值节点位移；界面有需保持的间隙/穿透时推荐；切向运动也会被传递，可能造成意外的网格拖曳）与 **project-nodes**（被动侧节点投影到主动侧面；主动侧大切向运动时推荐，仅法向位移有效传递；间隙/穿透显著时可能使网格失效）。v17.2 及更早创建的滑移界面建议在 18.0+ 用 Scheme 命令 `(recreate-sliding-interfaces)` 重建以减少左手面与收敛问题。

### 多对多 / 一对一手动创建（7.6.4.1–7.6.4.3）

- **多对多手动**（Create/Edit Mesh Interfaces 对话框，先禁 one-to-one）：只有要用 **Periodic Repeats** 时才必须手动（Periodic BC 也可用 Create Periodic 对话框，p. 1315；其余类型用自动法更方便）。选 Side 1 / Side 2 各一或多个 zone（**用 Periodic BC/Repeats 时每侧只能选一个 zone**）；Periodic BC 选 Translational/Rotational，Auto Compute Offset 默认开启（创建后显示偏移且不可编辑；关闭则手动给偏移坐标/角度）——**Important：自动计算依赖 cell zone condition 对话框里填的 Rotational Axis Origin/Direction，需事先正确设置，软件不会自动探测更新**；3D 自动计算且周期面非平面、又未被至少两个交于一条棱（棱指向从一个周期区到另一个）的面 zone 连接时，应保证两侧网格尺度相近（一侧平均尺寸 ≤ 另一侧 2 倍）。Periodic BC 启用时 Matching 默认启用且不兼容其他选项；Periodic Repeats 仅兼容 Coupled Wall。删除界面会连带删除创建时生成的附加 zone。
- **一对一手动**（Create Mesh Interfaces 对话框，one-to-one 启用）：适用于批量配对当前不重叠的边界 zone（滑移网格）或单对创建时启用 Matching。Boundary Zone List 1 / 2 各选一个或多个——**两列表间所有组合都会建界面，不论当前是否重叠**；两侧都单选时可启用 Matching（只生成内部区；超阈值报 warning；**Matching 用的边界 zone 不能再用于其他任何界面**）。
- **运动跨界面传递**细节见上文第 14 步。（p. 1250：若预期运动产生大位移，应考虑在被动侧 cell zone 上启用网格更新方法（光顺/重划，见 Dynamic Mesh Update Methods，p. 1880）。）



## 7.7 Overset 网格（pp. 1250–1278）

### 概念与拓扑（7.7.1–7.7.2）

- Overset（Chimera）= 用**相互重叠**的网格拼装计算域；与 NCI 沿匹配面连接不同，overset 在重叠区**插值单元数据**。各部件可独立生成、约束少，换部件无需重划全局。初始化时自动建立连接并分类单元：**dead**（域外）、**solve**（解方程）、**receptor**（接收插值）、**donor**（receptor 取数的来源，solve 的子集）。
- 接口内 cell zone 数量不限；zone 分 **background**（构成背景域，**不能有 overset 边界**）与 **component**（覆盖在背景上、在连接处有 overset 边界；多个 component 相连时至少一个要有 overset 边界）。支持全部单元类型（含 2D/3D 多面体）、混合单元、网格自适应、稳态与瞬态；并行稳态默认 Metis 会在初始化/读数据时按 model-weighted 自动重分区。
- 一个 case 可有多个 overset 接口，但**一个 cell zone 只能属于一个接口**；按拓扑拆多接口更高效，只装必要 zone。允许无 background、仅两个以上 component 的接口；多个 background 共存要求彼此不相交。
- **物理边界 zone（wall/inlet/outlet/symmetry 等）不得相互相交**（wall 不能穿过另一 wall），但允许**重叠**（贴合不交叉）——可用重叠部件拼装/修改外形，Fluent 在判定 solve/dead 时自动识别重叠边界。Overset 边界可与 overset 或物理边界相交。部件边界相交无法避免时用 **collar mesh**（额外 component 桥接相交物理边界，把"相交"问题化为允许的"重叠"问题；起圆角作用，把真实边界交点移入体内部）。扩展流体域（管道+腔体）需 **cut control** 指定某边界不切割某 cell zone。耦合 wall（baffle）在 background/component 中均允许。
- NCI 与 overset 非完全兼容：overset zone 内部可有 NCI，但网格界面边界不得与 overset 界面空间重叠；初始化与更新时检查接近度，间距不足发警告且 mesh check 失败。

### 域连接三步（7.7.3）

1. **Hole cutting**：标记物理边界切到的单元 + 体内外 seed 单元，flood fill 出 dead 区，得到最大重叠的有效网格。默认所有非 overset 边界切割所有 cell zone；`define/overset-interfaces/cut-control/add` 可禁止特定切割。纯 overset 边界的 component 在他区中心切出单个 cut seed（导向孔，后续放大）；`.../cut-control/cut-seeds/cut-seeds-for-all-component-zones?` 强制所有 component 生成 cut seed（加 cut control 时自动启用）。collar mesh 一般无需额外操作（重叠边界自动保护）；漏判时用 `define/overset-interfaces/collar-meshes/add` 手工指认（默认受保护不被切割；仅 hole cutting 阶段特殊对待 collar；`.../options/protect-collar-meshes?` 可关默认保护）。
2. **Overlap minimization**：把能找到更高 donor 优先级 donor 的 solve 单元转为 receptor、多余 receptor 转为 dead，使界面移到单元尺度相当的区域（默认**单元越小优先级越高** → 局部最细网格上求解）。并非字面"最小化重叠"；插值不一定发生在 overset 边界处——overset 边界只声明"要耦合"，不指定位置。donor 优先级法：`.../options/donor-priority-method` → **cell size**（默认；component 近壁细、远壁粗时最佳）或 **boundary distance**（到最近边界的反距离；重叠网格分辨率均匀且几乎相同时用；距离评估含所有边界）。**grid priorities**（`define/overset-interfaces/grid-priorities`，整数、只看相对值）：优先级高的网格在最小化中占先，覆盖 donor 优先级——可强行让解落在粗网格上。`.../options/minimize-overlap?` 整体关闭（仅全局，作用于所有接口）。
3. **Donor search**：为每个 receptor 在其他网格中找 donor 候选（包含 receptor 质心的 solve 单元及其连通单元）；每个 receptor 至少一个有效 donor。**两网格重叠区至少 4 个单元**才能成功。

### 诊断（7.7.4）

- 初始化失败通常**不改网格就无法恢复**。专家工具 `define/overset-interfaces/options/expert?` 启用后可用 `intersect` / `clear` 不初始化即执行/清除 hole cutting；`debug-hole-cut` 可对单接口执行并标记 dead/seed（flood fill 关闭 → mark0 register = seed 候选；开启 → mark1 register = 实际 flood fill 起点——定位问题最高效）。verbosity 1 + list 命令诊断。
- **Flood fill 失败**两类：① seed 单元误入流体区（拓扑/几何复杂或网格分辨率问题）→ 整个流体区被标 dead；seed 必须全在体内/域外，无法绕过。② **重叠边界泄漏**：重叠边界匹配不足，dead 泄漏到体外 → 整区消失。重叠边界容差**最多一个壁面法向单元尺寸**（高长宽比棱柱层很受限）——需改进重叠边界匹配。
- **Orphan cells**：receptor 找不到有效 donor（重叠不足或分辨率不匹配；receptor 叠在 receptor 上即成 orphan）。两壁间距**至少 4 个单元**。用 mark-cells 标记 orphan 定位需增大重叠的位置；**应细化 orphan 应该找 donor 的那侧网格，而非 orphan 所在网格**。无法消除时求解器有数值处理（部分案例防发散），但无先验质量/鲁棒性保证——强烈建议改网消除。

### Overset 自适应（7.7.5）

- 目的：除 orphan、减小 donor/receptor 尺寸失配、加密间隙。标记+自适应一步完成；迭代至多 **5 个 cycle**、每 cycle 默认 **2 次 sweep**，每 cycle 后需重建连接（代价高）。手动按需（稳态/无运动）；自动用于动网格——**每个时间步网格更新后执行、每步只做 1 个 cycle**（欠彻底但每步持续）。
- 标记类型：**orphan**（标记包围 orphan 质心的重叠网格单元 + 默认 1 层 buffer；orphan 所在 zone 不标）；**size**（donor 体积 V_d 与其最小 receptor 体积 V_r 之比超限即标——V_d/V_r > R_l³（3D）/ R_l²（2D），最大长度比 **R_l 默认 3**；可后处理 Overset Donor Size Ratio 场变量；符号经 500 dpi 渲染核对）；**gap**（间隙分辨率低于目标值即标，默认目标 4 单元；默认关闭）。
- 手动：`define/overset-interfaces/adapt/adapt-mesh`（一步）；`mark-adaption` 仅标记（mark0 = orphan+size+gap，mark1 = coarsening；需专家工具）；verbosity 2 打印标记数。自动：Automatic Mesh Adaption 对话框或 `.../adapt/set/automatic?`；与传统自动自适应（如 VOF）完全兼容、可同开互不干扰。
- 控制项（`define/overset-interfaces/adapt/set/`）：`automatic?`（默认关）、`maximum-refinement-level`（默认 4，与 mesh/adapt 同名命令取大者）、`mark-size?`、`length-ratio-max`（默认 3）、`mark-orphans?`、`buffer-layers`（默认 1）、`mark-fixed-orphans?`（需 mark-orphans）、`mark-gaps?`（默认关）、`gap-resolution`（默认 4）、`prismatic?`（合适的 3D 棱柱单元各向异性细化、不切特定棱 → 省单元；orphan 目标降长宽比、gap 目标适配边界层）、`mark-coarsening?`（默认开）、`adaption-sweeps`（默认 2）。

### 最佳实践（7.7.6）

- donor/receptor 尺寸应相当；间隙至少 4 单元（更多更稳）。压力基默认 Coupled 压速耦合（推荐）；瞬态时间步接近 CFL 极限时 segregated（SIMPLE/SIMPLEC/PISO）更省总时长，大时间步则 Coupled 更优。湍流从静止流场起步：standard initialization（全 zone 求默认值）有用。瞬态宜从收敛稳态解启动；稳态启动困难→边界条件渐升（低流速、高黏度起步）。伪时间法自动时间步（global time step 法）→ 改用 user-specified length scale 法。**替换 overset 接口中的 zone 后须重新初始化或对其 patch 再继续**。**推荐双精度求解器**。闭域不可压流动不支持；不可避免时在远离兴趣区加小压力出口。动/滑移网格：每步相对运动 ≤ 界面处最小单元长（时间一阶）或其半（二阶），长度取重叠区单元；VOF 时间二阶+大 CFL（>1）→ 先用时间一阶；单元状态翻转（dead↔solve/receptor）不可避免，verbosity 1 监控并尽量减少；运动路径上避免网格尺度剧变（grid priorities 可缓解）；时开时闭窄缝（阀/旋泵）→ gap model（p. 1279）。
- 插值法：`solve/set/overset/interpolation-method` → **least squares（默认）** 或 inverse distance。多孔区启用时推荐 least squares（多孔叠多孔尤其）；必须用 inverse distance 时可能还需非二阶压力插值 + 界面高阶压力外推 `solve/set/overset/high-order-pressure? yes`（对多孔压降/流量预测关键）。

### 限制与兼容性（7.7.7）

- **限制**：接口不能含 solid cell zone；zone 内 NCI 不得与 overset 界面空间重叠；component zone 不能有周期边界；background zone 不能有 overset 边界；component 网格边界不能与耦合 wall 重叠；无 FMG 初始化、不用 FAS 多重网格、不能开隐式残差光顺；闭域不可压不支持；后处理节点权重的 node-based gradient 不可用；不兼容 Coupled Level Set + VOF；支持的湍流模型不能与 SRS 模型/选项组合；DPM 须开 High-Res Tracking、wall film 粒子不能跨 overset 网格移动；WFGC 不支持。
- **兼容**（未列出一律视为不支持）：稳态+瞬态；层流/湍流+传热；单相；VOF 与 Mixture 多相。压力基（2D 平面/轴对称与 3D 绝对速度公式、可压、全部梯度格式、全部压力插值、一二阶空间格式、SIMPLE/SIMPLEC/PISO/Fractional Step/Coupled、全部 Rhie-Chow 质量流类型、伪时间法、一二阶及有界二阶瞬态、NITA 与 hybrid NITA（VOF））；密度基（绝对速度公式、可压、全部梯度与对流格式 Roe-FDS/AUSM/Low Diffusion Roe-FDS、一二阶空间、伪时间、瞬态格式）；湍流 **k-ε**（Standard/RNG/Realizable）、**k-ω**（Standard/BSL/SST）、Spalart-Allmaras、转捩 **Transition SST / Intermittency Transition / Transition k-kl-ω**（模型符号均经 500 dpi 渲染核对）；DO 辐射；组分输运（仅单相、须关闭反应）；VOF（明渠流与表面重力波；空化与蒸发/冷凝）；Mixture（非颗粒流；空化与蒸发/冷凝）；动/滑移网格限时间一阶；gap model；UDS；UDF（overset 循环宏）；AMG 除 Laplace Coarsening；边界条件除 exhaust fan/inlet vent/intake fan/outflow/outlet vent（非内部面）与 fan/porous-jump/radiator（内部面）；源项与 fixed values 只能加在不参与 overset 接口的 cell zone；支持 MRF；多孔仅 superficial velocity 公式；hybrid/standard 初始化；任意网格类型含自适应网格。

### 设置与后处理（7.7.8–7.7.9）

- **设置**：① 先把 component 网格的边界 zone 改为 overset 类型——**Important：创建 overset 接口前必须把所有 overset 边界指定完毕，之后不能再在 overset 与其他类型间切换**；② Domain → Interfaces → Overset 创建接口（命名；选 Background Zones 与 Component Zones；component-only 接口可不选背景）。③④⑤ 可选：无重叠边界可关 `.../options/overlap-boundaries?` 提性能；cut control / collar meshes；donor-priority / grid-priorities / minimize-overlap。以上只**定义**接口——**hole cutting 发生在解初始化时**。有 overset 面区但未定义接口时，初始化会自动生成含全部 cell zone 的 `default-overset-interface`（手动只装必要 zone 更高效）。
- **后处理**（初始化后才可用）：Mesh Display 勾 Overset 只显示 solve 单元（取消显示全部表面；`.../options/render-receptor-cells?` 可连 receptor 一起显示；orphan 显示也需此项）。Overset Cell Type 场函数（Cell Info... 类）：donor=2、solve=1、receptor=0、orphan=−1、dead=−2；云图从不显示 dead 值；overset 网格显示可能有 z-fighting（两网格重合所致，按 ID 着色尤甚）。专家选项下还有 Overset Donor Count（每 receptor 的可用 donor 数上限，实际用量可能更少）与 Overset Receptor Count。`mark-cells`（按类型全局或单区标记入 register）+ `display-cells`；`list` 列接口信息（verbosity 1 附每 zone 各类型计数）。
- **后处理限制**：体积分遍历全部 solve 单元 → 重叠区**重复计数**；面积分（含力/力矩报告）在创建面（plane/rake 等）上且跨重叠区时也有误差——在边界 zone 上或无重叠区取面积分则精确。**Important：积分误差随重叠面积增大**。
- **Overset 文件读写**（7.7.10，p. 1279）：写 case 推荐默认 CFF——overset 域连接保存在 .cas.h5，新会话读取**无需重建连接**（legacy .cas 需要），且跨不同核数读取连接完全一致。未初始化就写 CFF case 时默认先建立域连接再写；专家工具启用后可用 `define/overset-interfaces/options/update-before-case-write?` 关闭。

## 7.8 窄缝流动控制 Gap Model（pp. 1279–1290）

- **用途与机制**（7.8.1）：动网格/overset/滑移网格模拟随时间开合的窄缝（阀、旋泵）时，gap model 在缝隙闭合时**封堵或减速**流动。gap region 由一对 face zone 构成；一个面区进入另一面的 proximity threshold 内即标记其间的流体单元——标记区边界面上加零质量通量边界、单元退出求解（**Flow-Blocking** 型），或在标记区内减速流动（**Flow-Modeling** 型）。优点：blocking 型零泄漏（符合全闭阀真实工况）；modeling 型在 blocking 不稳时减速流动、把泄漏降到最低；减少窄缝高梯度区对高单元数的需求；避免窄通道划网/重划困难；可定义多个 gap region、各自独立阈值。
- **限制**（7.8.2，均不支持）：密度基求解器、轴对称旋转、ablation、Eulerian/Lagrangian wall film、凝固/熔化、电位、锂电池、声学、结构、DPM、辐射、组分模型（仅允许"混合但不反应"的 species transport）、污染物生成、反应器网络、解耦详细化学污染物、Eulerian 多相、多相+组分、带传质的多相；湍流 RSM/SAS/DES/LES 及全部 SRS 选项（SAS/DES/SBES/SDES）；Green-Gauss Node Based 梯度（仅 blocking 型禁）；QUICK/MUSCL 格式（仅 blocking 型禁）；NITA；gap region 不能选耦合 wall；不能与 Options 对话框 Contact Detection 页的 Flow Control 选项同用；gap 所在 cell zone 不能开多孔选项。
- **设置建议**（7.8.3）：单通道域 + flow blocking + 流束脱体的情形避免 velocity-inlet/outflow/mass-flow-inlet，**首选 pressure-inlet/pressure-outlet**；Important：**两种 gap 区附近都不得用 fan/porous-jump/periodic 边界**。材料：blocking gap + 不可压液体 + 收缩/扩张体积会产生非物理压力尖峰——液体选 compressible-liquid、气体用理想气体等可压选项（不可压液体也可用 UDF 加压缩性）。稳定与收敛：时间步要专门关注——域内存在 blocking 区时应比无 blocking 时更小；推荐自适应时间步、CFL=1。收敛差时依次：核查初始化（尤其湍流设置）→ 先低阶后二阶 → 减时间步 → 动量欠松弛降到 0.2 → 开 High Order Term Relaxation；仍不行则从 None 起逐步提高 Advanced Options 的 Stabilization Level、增大每时间步最大迭代、加密 gap 附近网格。
- **使用**（7.8.4）：① 建好含窄缝的动/overset/滑移网格。② Domain → Mesh Models → Gap Model...：Gap Definition 组——Gap Name（不能纯数字）；Face Zones 选 **2 个及以上 wall 或 symmetry 面区**（一个面区可进多个 gap region，但两个及以上面区同用于一区后不能再全体用于另一区；每区面区数越少计算越快）；Proximity Threshold（触发封堵/减速的最大距离）；Gap Type：**Flow-Blocking**（标记区边界面加零质量通量、单元退出求解；适合完全关闭的阀；推荐纯平移运动网格；旋转运动（齿轮/泵）可能发散——可加大阈值使标记区更大、避免未标记单元"孤岛"）或 **Flow-Modeling**（操纵黏度或源项减速；允许一定泄漏但设置得当时更稳健；推荐旋转运动网格）。modeling 型按黏度控制（默认法）时需指定合适 **Gap Reynolds Number**（越低密封越好；试凑或按 Eq 7.4 估算：**Re_gap = ρ_avg·u_avg·L / μ_avg**——L 即 proximity threshold，各量为 gap 区平均密度/速度/层流黏度；公式经 500 dpi 渲染核对）。③ Gap Management 组：Edit... 可加 **Exclude Cell Zones**（指定 zone 的单元不参与标记，控制 gap 形状；**overset 网格自动禁用该选项——组合不支持**）；modeling 型选 Method：**Sponge Layer**（按 Gap Reynolds Number 缩放 gap 内黏度，黏度升、速度降；Resistance Type 默认 **Fictitious Viscosity**——更稳健、对热仿真影响小，在动量方程黏性力离散时缩放层流黏度，显式作用于速度/压力、隐式作用于其他场；或 **Real Viscosity**——改真实层流黏度，全方程受影响）或 **User-Defined Source**（UDF 宏 DEFINE_GAP_MODEL_SOURCE 指定动量+能量源项；仅编译版，不支持解释版）。List 打印属性（标记单元数在初始化/计算后才更新）。**Advanced Options**：Stabilization Level（默认 None；逐级调整数值设置/格式/欠松弛/AMG，**全局作用于所有 gap 区**，非 None 时覆盖 modeling+Sponge 的局部稳定；级别越高越贵，尽量用最低级）；Check CFL Condition（按所选级别给出声学 CFL 建议并在需要更小时间步时告警）；Extend Gap Regions（标记时外扩邻近单元，改善稳定性/收敛）。④ modeling+Sponge 默认启用局部稳定（可用 `define/gap-model/edit` 按区关闭，或被全局级别覆盖）；`define/gap-model/advanced-options/sponge-layer` 统一调：viscosity variation factor（默认 0 = 黏度向中心线性变化最大，适合较大缝隙/高黏度比；趋近 1 = 黏度近似恒定，适合小缝/低黏度——变化越小约束越强但易不稳）、速度下限（gap 内平均速度低于它则禁用黏度缩放）、黏度变化比上限（把区内最大/最小黏度比限制在 0–给定值，防数值不稳）。⑤ `verbosity` 与 `expert?`（专家命令：enhanced-data-interpolation? 更准更贵、fill-data-in-gap-regions? 在 gap 区内插值解数据、precise-gap-marking? 更准的标记搜索（3D/大 gap 代价高）、reduce-gap-regions? 更保守的标记、render-flow-modeling-gaps? 关闭 modeling gap 单元的解渲染）。⑥ Mesh Display 勾 **Gap** 只显示允许流动的单元；云图中被 blocking 的单元不显示（Gap ID/Gap Type 除外）；`render-gap-interface?` 可渲染 gap 区内网格面（blocking 区的解仍不渲染）。⑦ 后处理（Cell Info... 类）：**Gap ID**（区 ID；未标记 = 0）、**Gap Type**（blocking = 1、modeling = 2、未标记 = 0）、**Flow-Blocking Gap Interface**（有零质量通量面的单元 = 1）；**Node Values 不支持**。注意：稳态下改/删 gap region 导致标记变化后**必须重新初始化**；避免两个及以上 gap region 重叠标记同批单元（尤其类型不同时），verbosity 1 会告警——blocking gap 重叠可合并为单一 region（含全部相关面区、阈值取全局合适值）。

## 7.9 网格检查与修复（pp. 1290–1295）

- **检查内容**（Setup → General → Check；**读入网格后应立即检查**）：拓扑（每单元面/节点数——tri 3面3点、tet 4/4、quad 4/4、hex 6面8点、poly 任意）；各 zone 面的 handedness 与节点顺序（应全为右手法则）；四类退化检查（退化距离向量——单元间/单元-面距离无限/未定义/极小；退化边——面顶点尺寸突变/亚机器精度；退化面——面积向量非有限或低于机器精度；退化单元——体积非有限或低于机器精度；verbosity 2–3 可见各 zone 检出数；**未定义/无限实体导致求解失败、极小实体损害鲁棒性，必须修复**）；单元类型一致性（非混合网格不跟踪类型以省工）；轴对称情形列出 x 轴以下的节点（旋转生成体积，x 轴下节点产生负体积，禁止）；旋转周期边界计算最小/最大/平均/指定周期角（常见错误是指错角度）；平移周期边界检查真实性；simplex 计数器核对（实际 node/face/cell 数 vs 文件头声明，差异上报）。
- **检查报告**（7.9.1）：域范围（x/y/z 最小最大，米）；体积统计（最小/最大/总体积及 2D 体积）——**最小体积为负 → 单元连接不当**，可用 iso-value 场变量 cell register 定位查看（Field Variable，p. 4064）、尝试自适应解决，**必须消除后才能继续求解**；面面积统计——**最小面积为 0 → 存在退化单元**，必须消除，很小的非零面积也建议修正。`mesh/check-verbosity` 报告级别：0（默认，只报"正在检查"，警告附在统计后）、1（逐项列出检查名，警告跟在对应检查后）、2（+最多 100 条失败详情：位置/受影响单元）、3（不限量详情）。
- **修复**（7.9.2）：Report Poor Quality Elements 按钮（Solution Methods 任务页底部；仅在 mesh check 检出劣质单元或已标记 poor mesh numerics 时可用——见 Robustness with Meshes of Poor Quality，p. 3891），或 `mesh/repair-improve/report-poor-elements` 打印统计；可用 Field Variable Register 或 Contours 选 Mesh.../Mark Poor Elements 标记显示。solver 变量 1–6：1.0 user_defined_poor_elements、2.0 poor_quality_cells、3.0 modified_centroid_cells、4.0 cell adjacent to small_face_area、5.0 invalid_cells、6.0 solver_identified_poor_cells；默认激活 3.0/4.0/5.0，**推荐 2.0**。检出可修复失败（左手面、节点顺序错误等）后 Domain → Mesh → **Repair** 按钮可用——最简单的修复入口，处理：节点顺序错误、面 handedness 错误/非凸、小面或不存在面、极差质量单元。默认只调内部节点位置——修复前 `mesh/repair-improve/allow-repair-at-boundaries` 可连同边界节点一起改。Repair 可能按偏斜度判据把退化单元转成多面体（→ Converting Skewed Cells to Polyhedra，p. 1304）——若修复后的网格不允许多面体（如要做 hanging node 自适应），修复前用 `mesh/repair-improve/include-local-polyhedra-conversion-in-repair` 关闭该转换。只改善劣质质量单元：`mesh/repair-improve/improve-quality`（可重复执行直到满意；要更细控制用 quality-based smoothing，p. 1338）。Repair 与 improve-quality 在劣质单元很多时 CPU 代价高——不太在意质量时可以只修左手面与节点顺序：先 `mesh/repair-improve/repair-face-node-order`（左手面可能正源于节点顺序错误，一并解决；修后再跑 mesh check），仍有左手面时 `mesh/repair-improve/repair-face-handedness`（改单元质心；对高长宽比单元最有效）。出现"node on face thread N has multiple shadows"警告 = 重复 shadow 节点（仅 periodic-type wall 网格）→ `mesh/repair-improve/repair-periodic`（旋转周期会提示输入角度）。

## 7.10 网格统计报告（pp. 1296–1299）

- **Mesh Size**：Domain → Mesh → Info → Size——节点/面/单元/分区数（partition = 并行用的网格分片）；Outline View 中对某边界或边界类型右键 Info 可看该边界/类型的面数。密度基耦合显式求解器按 FAS 多重网格各级分别输出。
- **Memory Usage**：Domain → Mesh → Info → Memory Usage——节点/面/单元/边/对象指针的已用与已分配量、surface 数组内存、求解进程内存。Linux：static（代码）/dynamic（堆，网格+解变量）/total；Windows：physical（驻留 RAM）/virtual（换页到页面文件）/total；不含静态代码内存；Cortex 独立进程。Windows 进程名例：cx2610.exe（Cortex）、fl2610.exe（solver host）、fl_mpi2610.exe（solver node）。
- **Zone 信息**：Domain → Mesh → Info → Zones——总节点数 + 各 face/cell zone 的数量、单元/面类型、边界条件类型、zone ID。
- **Partition 统计**：Domain → Mesh → Info → Partitions——各分区的单元/面/界面/邻居数（详见 p. 4571）。

## 7.11 转换为多面体网格（pp. 1299–1306）

- 三条路径（求解器基于面，天然支持多面体；非结构网格转 poly 后单元数可降至原来的约 1/3–1/5）：①全域转换（仅含 tet/wedge 的 3D 网格）；②仅转高偏斜 tet 单元；③转含悬挂节点/边的单元。
- **全域转换**（7.11.1）：非 hex 单元按原节点分解为"duals"再围绕原节点聚合成多面体，原节点删除；聚合中分割面会调整合并以减少面数。默认检查边界层单元长宽比、过高时询问是否保留边界层单元（保单元数、留边界特征）——`mesh/polyhedra/options/preserve-boundary-layer?` 可改默认。**hex 单元不转换**，除非与被转换的非 hex 单元相邻：共享面被分解、hex 变为多面体但外形尺寸保持（面数 >6）。楔形边界层只在边界面内分解、不沿法向分解 → 保留楔形单元厚度，转换后边界层单元数通常更低。入口：Domain → Mesh → **Make Polyhedra**。默认丢失 interior 型流形面——转换前 `mesh/polyhedra/options/preserve-interior-zones`（按名称子串匹配）保留。并行：转换后生成新分区但默认不迁移（省内存），随 case 保存、新会话自动使用；建议算前手动 `mesh/reorder/reorder-domain`；当前会话迁移需内存用量 < 半且 `parallel/partition/use-stored-partitions`；预计同会话继续计算可预开 `mesh/polyhedra/options/migrate-and-reorder?`。
- **偏斜单元转换**（7.11.2）：只把超过等体积偏斜度阈值的 tet 转多面体；算法对高偏斜 tet 及其邻域选最优聚合计，共享该边的单元合并为多面体，数据从原单元插值。
- **悬挂节点转换**（7.11.3）：读入时默认自动转换相邻单元（总尺寸不变、面数可能增加）；3D 读入后转换用 `mesh/polyhedra/convert-hanging-nodes`（如 hanging node 自适应后、确认不再细化/粗化时）。
- **共同限制**：已含多面体的网格不能再转；含悬挂节点/边的网格不能转（CutCell/hexcore 若过渡单元已转 poly 则无悬挂节点、可转）；`mesh/modify-zones/extrude-face-zone-delta`/`-para`、skewness smoothing、swapping 不可用（swapping 对 poly 无效）；不能 hanging-node 自适应（PUMA 可以）；动网格不能 remesh（光顺可用，推荐 RBF；线弹性固体光顺不兼容）；poly 网格节点/单元比高得多 → node-based gradient 可能显著增内存。

## 7.12 修改网格（pp. 1306–1346，22 项操作）

**总 Important：任何网格修改后都要存新 case（有数据则连 data）；旧 data 可能与新 case 不对应。** 分区方法另见 p. 4546。

- **合并 zone**（7.12.1）：同类多 zone 合一（Domain → Zones → Combine → Merge...）；zone 过多导致设置/后处理低效时用（大量 zone 设同一 BC 费时易不一致）。合并**不完全可逆**；可能不良影响 dynamic zones 与 mesh interfaces（合并前弹警告框，可先删除）。
- **分离 zone**（7.12.2）：读入时自动分离两种情形（face zone 挂多个 cell zone → 按 cell zone 分开；internal face 定为 wall → 自动生成 shadow wall）。手动：face zone 四法——**Angle**（法向夹角 ≥ 显著角则分；立方体 89° → 六面各自成区）、**Face**（每面一区）、**Mark**（按 cell register，被标单元的面入新区）、**Region**（按连续区域——耦合 wall 需一致朝向时用）；cell zone 两法——**Region**（多个封闭区域共享内部边界时分开；共享边界若为 interior 须先改成其他双面类型如 fan/radiator）、**Mark**。**任一 zone 最多分成 32 个**。对话框 Domain → Zones → Separate → Faces.../Cells...（Report 可预览）；**Important：须在 hanging node 自适应前分离——含悬挂节点的 zone 不能分离**。Mark 分离的角单元面可能进错区 → 再按 Angle 分离 + 合并修正。cell zone 分离常连带分离 face zone（Mark 必然、Region 不必然）。分离后存新 case + 新 data（旧 data 读不上新 case）。
- **断开 cell zone**（7.12.3）：`mesh/modify-zones/disconnect-cell-zones`——从**所有**相邻 zone 断开（滑移/动网格相对运动用）；复制共享面与节点，结果边界为 wall 型。之后可 fuse 重连、translate 移位等。
- **融合面区**（7.12.4）：合并重复节点、删除贴合的保形边界。Fuse Face Zones 对话框（Domain → Zones → Combine → Fuse...）：所选面区必须**整体**与同连接性的另一区融合，**不支持部分融合**；两区融合时可自定义新名；Tolerance 与 matching tolerance 同义，**≤ 0.5** 否则可能融错节点；TUI `define/boundary-conditions/modify-zones/fuse-face-zones`。按 cell zone 融合：`mesh/modify-zones/fuse-cell-zones`——融合所选 cell zone 间全部贴合面区（耦合 wall 与周期边界除外），新 interior 区保留成员名、新 ID。**自适应网格只在串行 + PUMA 法（2D/3D 默认）下可融合**。融合前存 case 副本。
- **创建周期区/界面**（7.12.5）：配对两个面区；保形（节点/面分布一致）→ 两区均变 periodic 型；非保形 → 两区变 interface 型并建周期网格界面（默认 Matching 选项）。Outline View 选两个区（Ctrl 多选；不能是 interior/periodic 型；选择顺序影响命名——第一个为主区被改名，第二个为 shadow）→ 右键 Periodic... → Create Periodic 对话框：Zone Name；Creation Method Conformal/Non-Conformal/**Auto**（不确定就用 Auto，尽量保形）；Type Translational/Rotational；Auto Compute Offset 默认开（关掉才可手输偏移/角度）；旋转配对必须手填 Rotation-Axis Origin/Direction（**自动算偏移不会自动探测这两项**）；3D 自动计算的网格分辨率建议同 7.6.4.1（一侧平均尺寸 ≤ 另一侧 2 倍）。保形配对失败可调 `mesh/modify-zones/matching-tolerance`（面最小边长的分数，**≤ 0.5** 否则可能配错损坏网格）。密度基求解器可为保形周期对指定压力跳跃（p. 1809）。TUI：`define/boundary-conditions/modify-zones/create-periodic-interface`。
- **解耦周期区**（7.12.6）：Outline View（Setup/Boundary Conditions/Periodic）右键 Delete；保形对 → 两区变 symmetry；非保形对 → 面区保持 interface，网格界面与周期区被删除。
- **Slit 面区**（7.12.7）：两个用途——把双面型边界 zone 切成两个耦合 wall；把耦合 wall 对切成两个非耦合 wall（可再改成其他边界类型）。复制除区端（2D）/区棱（3D）外的全部面与节点；端点共享节点只造成显示小误差，但**阻止两侧 zone 相对运动——要相对运动应 disconnect 而非 slit**。slit ≠ separate（slit 创建新面/节点入新区；separate 只重新分配既有面/节点）。slit 后再做自适应会导致边界无法再 fuse。`mesh/modify-zones/slit-face-zone`：internal zone → wall + shadow（再对 wall 或 shadow 执行一次 → 非耦合）。**Important：wall 继承原 zone ID 与面朝向，shadow 拿新 ID**。典型用法：散热器出口（interior 型）→ slit 两次 → mass-flow-inlet（无其他途径）。操作后存 case。
- **面区定向**（7.12.8）：`mesh/modify-zones/orient-face-zone` 把内部面区法向统一方向；某些边界类型必需（如 fan 按法向定流向，混向 → 结果错误）。
- **挤出面区**（7.12.9）：不退出 Fluent 扩展计算域（典型：回流打到出口）。生成棱柱/六面体层（基于面形状与节点平均法向）；两种指定：位移列表（`extrude-face-zone-delta`）或总距离+参数坐标列表（`extrude-face-zone-para`，0.0 起 1.0 终，如 0,0.5,1 = 两等厚层）。限制：悬挂节点面区不可挤出；多边形面区不可；仅 3D；两命令**均不可用于并行版**。
- **投影边界区到辅助几何**（7.12.10）：把边界区节点投影到辅助几何定义上（如保证滑移网格非一致界面对在同一平面/曲面，减小误差）：先建辅助几何（p. 1855）→ `mesh/modify-zones/project-face-zones` → 刷新显示/跑 mesh check 核验。
- **替换/删除/停用/激活 zone**（7.12.11）：**替换**（Replace Zone 对话框）用新网格区域替换局部区域（免全域重划）；替换网格须预备：单 cell zone、同 zone 类型、非一致界面边界须基于同一几何（尖角/曲率两侧紧贴）、zone 名可不同；**BC 按名称自动转移**——重名边界继承 BC，独有名边界取该类型默认 BC；文件限 legacy .msh/.cas，**不能用 CFF**；Interpolate Data 按几何情况开关——**Important：被替换 zone 属于 overset 接口时必须关闭 Interpolate Data**。**删除**（Domain → Zones → Delete...）：连单元/面/节点全删；邻接他区的 interior 面自动变 wall 留在剩余区。**停用**（Deactivate...）：把 fan/interior/porous-jump/radiator 类内部面拆成 wall+shadow 对，从网格与求解循环移除；**含 mesh interface 的 zone 在初始化前不能停用**。**激活**（Activate...）：只列已停用 zone，恢复其最后数据；激活后核查 wall/wall-shadow BC 是否恢复；支持自适应。
- **复制 cell zone**（7.12.12）：`copy-cell-zones-by-offsets`（任意偏移序列）或 `copy-cell-zones-by-delta`（等间距/等角度）；副本 cell 数据初始化为常数，**非一致界面与 dynamic zone 不复制**，外部/内部面区保留原 BC、模型设置相同；首个提示直接回车 = 选全部活动 zone；**有周期边界的 zone 须先 slit 再复制**；副本要与既有区域连通 → fuse 或建非一致界面；NETM 多孔仿真的副本改 solid 型时须把 inlet/outlet 等边界改成绝热 wall。
- **替换整张网格**（7.12.13）：Domain → Zones → Replace Mesh...（细化研究/网格质量不达标时换网续算，已有数据自动插值）。默认按同名 zone 对插值；**Interpolate Data Across Zones** 用于同名区内部边界不一致时——**不保证全局守恒，仅在必要时用**（替换网格边界与原网格重合时插值最佳）。并行时自动按"匹配单元同节点"分区；找不到同节点插值单元会自动开跨区插值——避免该行为用 Scheme `(rpsetvar 'dynamesh/replace-mesh/partition-per-zone? #t)`（代价是额外重分区）。限制：BC 按名映射（无匹配 → 默认）；替换网格须 legacy .msh（或 .cas——只用网格信息、忽略设置；**CFF 不可用**）；用 .cas 替换须先删除已定义的非一致界面；两网**缩放必须一致**否则插值错误。
- **邻接 zone 管理**（7.12.14）：Domain → Zones → Adjacency...——查/显示 cell zone 的相邻面区；可改名：Rename by Adjacency（面区名追加相邻 cell zone 名，如 interior-fluid；仅面区可用）、Rename by Wildcard（From 模式 → To 替换；`*` 只能放首/尾，`?` 匹配单字符）、Fluent 命名约定（类型+ID）、加前缀/后缀；选项 Exclude Custom Names（保护自定义名——关闭则无条件重命名且自定义名永久丢失）与 Abbreviate Types（vi/int/ifc 等缩写）。
- **域重排**（7.12.15）：多进程会话读入时自动按 Reverse Cuthill-McKee 重排单元与面（带宽 = 相邻单元索引差最大值；样例输出含 bandwidth reduction）。
- **缩放**（7.12.16）：Fluent 内部一律以米存储，读入默认按米——非米单位网格必须缩放（Setup → General → Mesh → Scale...：Convert Units 选 m/cm/mm/in/ft 自动给系数如 0.0254 m/inch，或手输 X/Y/Z 因子；也可改物理尺寸，**各向异性缩放会改变长宽比须慎用**）。**Important：必须在算 S2S 视角因子、初始化或计算之前缩放——已有数据在缩放后失效**；建议建 case 前（尤其建 mesh interface/shell conduction 前）先缩放；缩放后图形窗口 [Out of Date] → 右键 Refresh Display。View Length Unit In 可切换显示长度单位（不改数据）；Unscale 按因子除回（选 m 再 Scale ≠ unscale）。单 zone 缩放：`mesh/modify-zones/scale-zone`（与未缩放区保形连接的 zone 不能单独缩放）。
- **平移**（7.12.17）：整体（Domain → Mesh → Transform → Translate...，X/Y/Z 偏移，当前长度单位）——旋转轴不过原点、轴对称轴未对齐 x 轴、或想把原点移到特定点（如平板前缘）时用；单 zone：`mesh/modify-zones/translate-zone`（保形连接的 zone 不能单独平移）。
- **旋转**（7.12.18）：整体（Rotate Mesh 对话框：角度 + 旋转原点 + 轴向量）——结构与 CFD 网格差一个小角度时有用；单 zone：`mesh/modify-zones/rotate-zone`（同样不能单独转保形连接的 zone）。
- **光顺与换面**（7.12.19）：**只有 quality-based smoothing 受推荐**；face swapping 与 skewness/Laplacian 光顺限制多、未来可能移除支持；face swapping 仅限 tri/tet 网格；swapping 与 skewness/Laplacian 仅串行——**并行只能 quality-based**。quality-based：Improve Mesh 对话框（Domain → Mesh → Quality → Improve Mesh Quality...）分 bin 改善正交质量最差的 bin；**Percentage of Cells 上限 10%，先小后多次**；Number of Iterations 默认 4；与 `mesh/repair-improve/improve` 同类但可控比例。Laplacian（不推荐；串行；最适合 quad/hex）：新位置 = 邻节点平均 × 松弛因子（0–1）；改善偏斜但松弛聚类，尖角/粗凸角附近多轮+大因子可致网格线交叉、负体积；多轮后节点偏离边界、失去聚类。skewness-based（不推荐；串行；tri/tet）：内点重定位压低最大偏斜（默认阈值 3D 0.8 / 2D 0.4）；有内检防止增大最大偏斜的移动，但平均偏斜可能上升——权衡是否值得，只对很高偏斜（0.8/0.9）做可减轻副作用。`mesh/smooth-mesh` → laplace/skewness（iterations 默认 4）。face swapping：tri 用 Delaunay 外接圆测试（反复执行 `mesh/swap-mesh-faces` 直到换面数为 0 → 受约束 Delaunay 网格，最大化最小角、趋向等边）；tet 为共边 3 单元 → 共面 2 单元。组合流程：4 次光顺（阈值 0.8/0.4）→ 换面至 0 → 3D 降阈值至 0.6 重复。
- **边界层重分布**（7.12.20）：网格操作后边界层增长率失真时，`mesh/redistribute-boundary-layer`（输入邻接面区 + 目标增长率；hex/wedge 边界层），重分布至域边界 / zone 变化 / 单元类型变化为止。
- **删除单元**（7.12.21）：按 cell register 删标记单元（`mesh/modify-zones/delete-cells-by-mark`；field-variable register 需先初始化）；每个 cell zone 在被删面处生成 symmetry 边界；可 augment 把删除后孤立的邻单元一并删以保证数值有效；**不支持 overset 网格与 shell conduction 壁面；不可撤销——先存 case 副本**。
- **提取单元**（7.12.22）：反向操作——保留标记单元（可加邻层），其余永久删除（`mesh/modify-zones/extract-cells-by-mark`）；每个 cell zone 生成 wall 边界；适合从大网格中切出小区域研究/后处理；同样不支持 overset/shell conduction、不可撤销。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.7；本页覆盖批次 34（pp. 1169–1201，7.1–7.3）、批次 35（pp. 1202–1249，7.4–7.6）、批次 36（pp. 1250–1278，7.7）、批次 37（pp. 1279–1295，7.8–7.9）与批次 38（pp. 1296–1346，7.10–7.12，Ch.7 全章收官），均为 2026-10-17 读取。
- Eq 7.1/7.2 的向量符号、Eq 7.3（y_p√(u_∞/(νx)) ≤ 1）、"constant plane"坐标符号（z）、7.7 节尺寸自适应判据（V_d/V_r 对 R_l³/R_l²）与湍流/转捩模型名（k-ε、k-ω、Transition k-kl-ω）、Eq 7.4（Re_gap = ρ_avg·u_avg·L / μ_avg）均在文本提取中缺失，已逐一按 500 dpi 渲染视觉核对。7.12 节平移/旋转/缩放小节中的坐标轴符号（x/y/z）在提取中丢失，按上下文与 7.2.1 的 x 轴约定、p. 1291 报告样例互证补全，未逐处渲染。另注：手册 p. 1269 将 verbosity 命令印作 `define/overset-interface/options/verbosity`（单数），与其余各处 `overset-interfaces` 不一致，疑为原文排版不一致，按原文照录待核。Figures 7.1–7.111 为图形元素，未摄取。
- 质量阈值（正交质量 > 0.01、tri/tet 偏斜度 < 0.95、通道 ≥ 5 单元）是手册给的通用指引而非验收标准；指标定义的 Meshing 侧详细版见 [[Fluent 网格质量诊断]]（Part II Ch.6）。
- fe2ram/GAMBIT/ARIES 等导入格式细节的完整整理在 [[Fluent 第三方网格导入与 fe2ram 过滤器]]（Part II Appendix A）；本页只记 solution 模式视角的入口与差异点（如 CFX 分区选项、tmerge 不支持 CFF）。
- NCI 界面选项兼容性（Mapped 不支持密度基求解器/DPM/动网格、Static 误用结果错误、one-to-one 仅支持 Coupled Wall 等）与周期选项前提（均匀偏移、整除 360）均为 2026 R1 手册明确陈述，升级版本须复核。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 第三方网格导入与 fe2ram 过滤器]]
- [[Fluent 网格质量诊断]]
- [[Fluent 网格模式入门]]（meshing 模式侧能力对照）
- [[Fluent 求解模式文件读写]]（File/Read/Mesh... 等命令的 Ch.3 详述）
- [[index]]
