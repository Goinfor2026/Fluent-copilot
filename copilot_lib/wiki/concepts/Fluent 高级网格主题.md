---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - advanced
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 高级网格主题

> 本页按 Part II / Chapter 7 的目录顺序分段摄取；目前覆盖 PDF pp. 605–868（7.1–7.14.2），Chapter 7 已完成；附录按独立目录条目续接。

## CAD 装配树与关联

启用 CAD Options 中的 Create CAD Assemblies 后，Fluent Meshing 保留 CAD 原始装配层级；可按 part/body/file/selection 创建对象，按 body/face/object 建立 zone。按 body 导入通常更有利于保留子装配结构。装配实体含 component（装配/子装配/零件）和 body（基础实体），命名选择也可作为 zone label（PDF pp. 605–606）。

FMDB（`.fmdb`）是供重导 CAD、调整 facet 精度或拓扑表示的中性文件；CAD 实体路径用于命令定位。装配树支持按名称筛选、展开/折叠、抑制同级实体和选取关联对象（PDF pp. 607–608）。

CAD 实体可按新参数更新或重新镶嵌。CAD Faceting 控制 CAD facet 的细化容差和最大尺寸；CFD Surface Mesh 控制最小/最大 facet 尺寸、曲率角及 gap cells，可保存或复用 size field。几何/网格对象可从 CAD 实体新建、添加或替换；标签用于保留面区分组。锁定实体避免同一 CAD 实体被重复建对象；抑制实体可排除不参与分析的部分（PDF pp. 609–612）。对象可更新自 CAD、恢复、附加或解除关联；解除后对象不再跟随 CAD 变更（PDF p. 612）。

## Size Functions 与 Scoped Sizing

尺寸场由尺寸函数和/或 scoped sizing 计算；仅支持三角化 zone，非三角面需先三角化或使用 `triangulate-quad-faces?`。全局/局部控制主要涉及最小/最大尺寸、增长率和来源；曲率、邻近、BOI、soft 通常为软行为，meshed 和 hard 为硬行为（PDF pp. 612–613）。

- **Curvature**：按边/面法向变化限制单元跨越角度，参数为 min/max、增长率和 normal angle；小角度通常捕获更多曲率细节（PDF p. 614）。
- **Proximity**：按窄缝中要求的单元层数控制尺寸，可计算边-边或面-面邻近；面邻近可配置忽略自邻近/朝向。复杂几何可能漏检，需拆分 scoped controls；Quick Edge Proximity 可节省时间和内存但会降低精度（PDF pp. 615–618）。
- **Meshed**：继承已有网格尺寸并按增长率过渡；当前默认软行为，历史版本 15.0 及以前为硬行为，该行为随 mesh 文件保存（PDF p. 618）。
- **Hard / Soft**：Hard 在指定位置强制指定尺寸并覆盖其他 sizing；相邻两个 hard size 会导致突变，重叠时后定义者生效。Soft 指定尺寸上限，可被其他更细 sizing 覆盖（PDF pp. 618–619）。
- **Body of Influence**：封闭面区定义的体内控制尺寸上限；开放区域会按 soft sizing 处理。多个相交闭合 BOI 若作用于同一 sizing，应分别定义控制（PDF pp. 620–621）。

可在 Size Functions / Scoped Sizing 对话框创建、命名、设作用范围并验证控制。默认函数包括全部边/面区上的曲率与邻近函数，normal angle 默认 18°、cells per gap 默认 3（PDF pp. 621–623）。Scoped controls 可写入/读取 `.szcontrol` 文件。计算后的尺寸场可以导入/导出、缩放或周期化；已读入 size field 后，当前会话不能再添加或编辑 sizing 定义（PDF pp. 623–625）。可用等值图、probe 或 preview sizes 检查尺寸分布，再按 size field 重划边/面；关联 feature edge 应先于面区重划（PDF pp. 625–627）。

## Objects 与 Material Points

Object 通常由 face/edge zones 组成，用于界定待网格化区域并保留包覆时的特征；闭合实体/流体、封口面或独立面区均可构成对象。对象之间保持独立，共用的 zone 会复制。对象可先生成连通表面网格，再计算 volumetric regions 并生成体网格（PDF pp. 628–629）。

对象属性包括 geometry/mesh 类型、cell-zone type 和 priority。重叠区域由较高优先级对象占有；同优先级对象可合并为一个 cell zone，包围盒/风洞对象通常需较低优先级。Subtract 构造对象时，优先级顺序决定哪些区域被排除（PDF pp. 629–632）。对象实体包括 face-zone labels、volumetric regions 和 cell zones；labels 帮助保持 CAD/面区来源对应，且 mesh object 必须有 labels（PDF pp. 632–634）。

对象管理方式包括快捷键、屏幕工具、命令和 Manage Objects 对话框，可创建、改属性、自动对齐、重划、删除、合并、移动、变换以及管理标签/边区（PDF pp. 634–641）。

Material Point 用于确定或拆分体区域：当对象边界不足以唯一识别目标流体域、几何中有多个空腔或非连通区域时，用点指示应保留的流体区。双面壁/风扇/多孔跳跃面两侧若都要恢复，需每侧各放 material point；网格生成后可手动合并 cell zones。默认 `auto-delete-dead-zones?` 会自动删除分离出的 dead zones（PDF pp. 641–643）。

## Object-Based Surface Meshing

对象式表面网格先构造连通、共形的表面网格，再据此识别体区并填充体网格。单流体体域常从 CAD faceting 几何对象出发，以 wrapper 连接；复杂拓扑/CHT 通常导入 CFD surface mesh，先诊断和修复连接关系，再 merge 对象、Join/Intersect 连接表面，最后检查质量（PDF pp. 644–647）。

几何准备工具包括创建 wind tunnel/far-field bounding box、封闭环形间隙、patch/cap 填孔、loop selection 生成封口面，以及 user-defined groups 管理大型模型（PDF pp. 647–653）。几何诊断可标记自交/互交、自邻近/交叉邻近和边邻近；连接与质量诊断可逐个定位 free/multi/duplicate faces、skewness 等问题，并用针对性工具修复。Summary 提供面数量、面区数量及质量统计（PDF pp. 653–657）。

Join 与 Intersect 可把重叠或相交面区连接为共形表面，操作后默认自动局部 remesh。操作前应先处理 free/duplicate/sliver faces、自邻近和明显间隙，并尽量让相连面区尺寸相近；容差可用相对局部尺寸或绝对几何单位指定。全局控制适合明确公差的情况，局部逐对处理更适合公差未知情形；完成后应检查是否仍与第三个面区重叠（PDF pp. 657–662）。

Mesh objects 的高级修复包括对象管理、移除面-面/面-边间隙、按法向方向区分 gap 与厚度并投影移除厚度、Sew 多对象形成共形三角表面。厚度移除涉及拆分/合并面区，可能降低质量，操作前建议保存；Sew 适用于多个 mesh objects，不需要用于单对象或仅抽取流体体域的情形。薄区、狭缝等情况可能需要额外处理（PDF pp. 662–669）。

## Object-Based Volume Meshing

对象式体网格要求先有共形连通的表面网格。先 Compute volumetric regions，必要时 Validate/Update，然后对所有区域用 Auto Mesh 或逐区 Auto Fill Volume；生成 cell zones 后检查质量，准备转入 Solution Mode 时可运行 Prepare for Solve 清理 dead zones、几何对象、edge zones 和未用实体。对象式流程合并 cell zones 时要求属于同一 volumetric region（PDF pp. 670–672）。

Volumetric Regions 管理支持按材质点计算区域、校验闭合/水密性、保留名称/类型更新区域、按流体/固体/dead 筛选、管理 baffles，并查看表面统计与区域组成。单个区域可诊断、改类型、合并/删改、设置 scoped prisms/Tet/Hexcore 参数；删除 cell mesh 可保留区域信息（PDF pp. 672–675）。

Auto Mesh 为对象全部计算出的区域统一设置棱柱层（none/scoped/zone-specific）、quad-tet 过渡、Tet/Hexcore/Poly 填充、尺寸和区域内 cell zone 合并策略。Auto Fill Volume 则允许逐区域设定并重复填充未填区域。对象式体网格不支持在同一 region 内只生成棱柱或只初始化 Tet/Hexcore 等部分步骤；这些操作需 domain-based workflow。默认会在体网格前备份表面网格（可配置关闭），但恢复表面后再生成的网格可能因处理顺序不同而略有差异（PDF pp. 675–679）。

## Manipulating the Boundary Mesh

边界网格工具处理 free/isolated nodes、三角边界面交叉、合并和 stitch。Intersect 沿交线连接；Join 合并重叠区域；Stitch 沿自由边并在容差内投影闭合。连接操作会插入交线并局部重三角化，默认再次 remesh；容差不应扭曲几何（PDF pp. 680–688）。Modify Boundary 提供创建/删除/合并节点面区、重分区等原子编辑，操作后立即重显示；并非都可撤销，应先保存（PDF pp. 688–696）。

边界表面可按 skewness、尺寸变化、aspect ratio 或 area 改善，支持平滑、交换和塌缩；局部体网格细化之前，宜同步细化边界以避免尺寸跳变。边界 refinement 只支持三角面，且对远离平面的几何不宜使用可能改变形状的平滑（PDF pp. 696–700）。Feature Modify 可按固定/自适应角度提取 edge zones 以保持锐边；可分离、合并、定向、投影、相交和重划 edge zones。边界 edge 的方向影响新面生成侧，合并只支持同类边区（PDF pp. 700–706）。

Surface Retriangulation 通过 edge zones 与 size field 重划三角或四边形边界面，输出三角面；关联特征边需先重划，多个共享边界面区的共形重划有额外条件（PDF pp. 707–710）。Faceted Stitch 可按容差修复三角面自由边但可能损失特征；四边形 zone 可复制后或原位三角化。Face zones 可按角度、邻接 cell zone、面形状、seed 或已标记区域拆分（PDF pp. 710–715）。

其他边界操作包括将一个面区投影到另一个面区以填隙、建立 zone groups、重命名/合并/删除/改类型和变换面区；法向可翻转或统一定向。可创建 bounding box、平面、圆柱/圆台、扫掠/旋转面并创建 periodic pair；periodic 需要真实建立周期与 shadow 配对和节点对应，单改 zone type 不够，原始边界节点分布必须匹配。还可用 Remove Boundary Gaps 投影修复间隙及 Loop Selection 生成封口边界（PDF pp. 715–731）。

## Wrapping Objects

Wrapper 通过覆盖对象的 Cartesian 网格修复不干净几何，抽取水密、连通的 mesh object，并在可接受的几何细节损失下填补缝隙/重叠。流程是先叠加粗 Cartesian 网格、按 size field 细化、检测与原几何相交单元、围绕 material point 抽取边界、把节点投影回面和特征边，再平滑/交换/重划改进（PDF pp. 732–735）。薄缝需要足够细的分辨率，倾斜/弯曲窄隙可能需比 gap 更细 3–4 倍；大孔洞需先修复，否则可能在 wrap 中被忽略。

Wrapping 前可提取 edge zones、在对象内或对象间创建交线 loops、配置 geometry recovery、检查/修复 wetted holes 和 leak paths。Shrink Wrap 可分别或整体生成 mesh object；material point 决定保留的流体/湿润域，external 点会消除对象内部孔腔。resolution factor 控制采样粗细；复杂大模型需考虑内存和初始 bounding box 对后续多次 wrap 的影响（PDF pp. 735–746）。

Improve 可组合平滑、交换、面改善和可选 imprint，也可按当前尺寸场重划；coarsening 可降面数和计算成本，但 imprint 可能使质量变差。其他命令可辅助薄区恢复、孔洞报告/检测和 feature capture（PDF pp. 746–748）。

## Creating a Mesh

网格策略取决于边界面类型、局部精度需求和计算规模：三角面上可先长棱柱层再填 Tet（viscous hybrid）；混合 tri/quad 与既有 hex 区域可用 pyramid 过渡到 Tet；Hexcore 在近壁用非结构网格、核心区用 Cartesian；Rapid Octree 适合超大规模、近似各向同性网格及可接受一定几何简化的场景，边界投影和 Cartesian snapping 是两种处理方式（PDF pp. 748–755）。非共形 interface 可降低不同网格之间点对点匹配要求；孤立节点可控制局部网格密度，但不可放得过近，否则初始化可能失败（PDF pp. 755–759）。

Auto Mesh 统一选择 face-zone 或 object-based 填充，棱柱层策略、quad-tet transition、Tet/Hexcore/Poly/Poly-Hexcore、尺寸场/增长、区域合并和并行分区。Thin Volume Mesh 以源面和目标面生成薄隙扫掠式网格；Pyramids 用于 quad→tri/Tet 过渡，需注意高面长宽比、快速尺寸跳变和凹角相交问题（PDF pp. 759–767）。非共形界面可分离成成对 face zones；Heat Exchanger Mesh 用四点和间距生成棱柱化的等效换热器区域（PDF pp. 767–769）。

Auto Partition 支持 Poly、Poly-Hexcore、Octree-based Hexcore 等并行路径；Tet 配合 zone/scoped prisms 时棱柱可并行生成而 Tet 后续串行。分区后大量网格修改/几何和对象操作 GUI/TUI 功能会不可用，因此应在分区前完成必要的边界修复并保存网格。Thread Control 可按 node processes 或机器核心数限制线程数（PDF pp. 769–777）。

## Generating Prisms

Prism/wedge layers 可从三角或四边形边界生长，用于边界层、已有域扩展或挤出体网格。生成流程会分析相邻边界、逐层确定方向/offset、检测 proximity 与压缩/分层冲突，最后对相邻三角区投影并重三角化（PDF pp. 778–780）。zone-based 设置需检查无 free nodes、低质量面和法向方向；参数包含首层高度/长宽比、增长规律和层数，生成前保存，生成后核对 cap 面最大 skewness（PDF pp. 781–784）。

可对多壁面同时或分别设置增长参数；相邻区层数可能被统一到较小值，选择顺序会影响生长层数。双面壁可两侧生长；无效法向、相邻面投影和 gap proximity 会影响成功率。growth controls 可压缩层并 stair-step 处理碰撞或尖角，可能将高层棱柱改由 pyramid/tet 填充（PDF pp. 785–806）。方向向量可取法向/指定向量等，normal smoothing 减少向量相交。相邻四边形面可直接作为 prism sides，三角面需满足节点连接与夹角条件后投影、重三角化（PDF pp. 793–800）。

棱柱后处理提供按 ICEM/orthoskew/skewness/squish 平滑改进、剔除低质量层及 warp 优化；也可对邻接 Tet 建 cavity 修复。常见失败检查项包括自由节点导致 retriangulation 失败、法向方向不一致、棱柱生长进入已有单元、尖角层碰撞及质量阈值不适用；应结合预保存网格调整参数重试（PDF pp. 801–807）。

## Generating Tetrahedral Meshes

Tet 生成可由 Auto Mesh 自动执行，也可按初始化、细化、改进分步控制；已有 prism/hex/pyramid 区域时，用 domain 限定待填域或指定需要保留的 cell zones。自动流程先合并自由节点、清理未用节点、改善表面、初始化体网格，再多轮细化、交换/平滑并移除 slivers。混合网格可以自动加入 prisms/pyramids；按 zone type 设置决定哪些 cell zones 参与细化（PDF pp. 808–813）。

手动工作流先验证表面网格，再初始化，然后全局或局部细化。局部 box refinement region 用于调整内部尺寸梯度；可选择 advancing-front 或 skewness-based refinement 和 growth/size-field 参数。全局尺寸及质量统计应在细化后复核，不宜过度细化（PDF pp. 813–821）。

初始网格失败的常见原因包括重复/自由节点、无效或未闭合边界、相交面、额外节点和 sliver 参数不合适；用 free/unmeshed faces 定位，清理重复节点、补洞/合并间隙或调整 boundary closeness 后重新生成。若内部节点过近边界导致高 skewness，可平滑或调高 Min Boundary Closeness（PDF pp. 821–823）。手册示例中的质量范围只作指导，应结合几何与目标用途判断。

## Hexcore、Poly 与 Poly-Hexcore

Hexcore 在核心区生成轴对齐 Cartesian cells，边界附近由 Tet/混合单元过渡，H-refinement 控制尺寸变化。Cartesian 类型逐层标记边界相交/尺寸过大的单元并加 buffer 后细化；Octree 受 size controls/size field 驱动且更快，但不能把 hexcore 延伸到边界。Prisms（若设置）先生成。主要参数含 max/min cell length、buffer layers、peel layers、extents 和局部 box refinement；buffer 太少可能产生较差质量，extents 自动对齐/延伸应检查几何变形风险（PDF pp. 823–831）。
+
+Poly mesh 以 Tet 网格的 dual 构造多面体，通常可显著降低非结构网格 cell 数；前提是高质量三角表面、面尺寸不大于材料厚度且 prism aspect ratio <50。生成过程通过 cell merge/split 和 smoothing 改善凹单元、凹边界面与阶梯面；Squish 和 orthoskew 是较合适的质量指标。生成后要检查 prism 与 poly cell 质量；恢复原始 faces 会删除当前对象面区和 cell zones，之后才能重新生成（PDF pp. 832–836）。
+
+Poly-Hexcore 结合 poly 过渡区和 Hexcore 核心。Auto Mesh 中可设置 scoped prisms、buffer/peel layers 和最小尺寸；控制项可避免 Hexcore 的 1:8 尺寸跳变，并把选定区域设为纯 poly，按区域类型/最大区域进行选择。它继承 Poly 与 Hexcore 的适用条件与限制（PDF pp. 836–837）。
+
+## Rapid Octree Meshes

Rapid Octree 用大规模并行 octree 生成以近似各向同性 cube cells 为主的体网格，目标是稳健、快速处理可接受一定 defeaturing 的模型。输入需有三角化边界；对内部流可按 geometry 或 material points 定义体域，对外流可用 bounding box 定义域，也可用 Generic Region Definition 显式指定各 region 的 material point 与 bounding face zones。多个区域生成的 cell zones 不自动连通，需在 Solution Mode 建非共形接口（PDF pp. 838–845）。

网格尺寸由 bounding box 与 reference size/level 决定，尺寸必须落在 octree 的 2 的幂次网格层级上，改 reference size 后应检查 box 和最终尺寸。Boundary Treatment 可选 Boundary Projection 或 Cartesian Snapping；二者都按网格尺度 defeature 特征，Snapping 更快但不善于表示薄结构，且要求恒定边界尺寸。Projection 可启用 Improve Geometry Resolution 投影边界面以减少边界偏差，但显著增加耗时，并可能损害复杂区域质量；可用 boundary mesh optimization 改善近壁正交性（PDF pp. 846–853）。

Mesh Parameters 设置最大/默认边界尺寸、volume/surface transition layers 和 coarsening；可建立 box、frustum、BOI refinement region。Custom Boundary Sizes 支持 soft、curvature 和 proximity sizing；proximity 要让最窄间隙至少有约 3 个单元解析，并限制过多 refinement levels 以控制计算时间。Boundary Projection 可在网格生成时把默认单层棱柱层细分为指定 anisotropic layers，不必先生成网格再改层（PDF pp. 854–866）。

限制包括：入口/出口等边界面积可能因 defeaturing 与原几何不一致；Cartesian Snapping 只支持恒定边界单元尺寸，且要求封闭、无缝/重叠/自交、法向一致的三角面；Projection 对小几何瑕疵更宽容，但粗网格、尖角和尺寸跳变可能造成边界鼓包。若删除低质量单元会新建 symmetry 面，可能影响后续边界条件/求解，必须谨慎检查（PDF pp. 867–868）。

## 证据与边界

来源：[[Ansys Fluent Users Guide 2026 R1]]，版本 2026 R1，PDF pp. 605–868（7.1–7.14.2）。页码均为 PDF 物理页码。具体支持选项和默认值受工作流、网格状态及版本影响；Chapter 7 已完整摄取至目录边界 p. 868；p. 869 起为 Appendix A，不属于本章。

## 关联页面

- [[Fluent 网格质量诊断]]
- [[Part II - Meshing Mode]]
- [[Ansys Fluent Users Guide 2026 R1]]
- [[index]]
