---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - fault-tolerant
  - workflow
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 容错网格工作流

## 摘要

Fluent User's Guide 2026 R1 Part II / Chapter 4 介绍 Fault-tolerant Meshing 工作流（PDF pp. 409–524）。它围绕 CAD 装配导入、区域识别与泄漏封闭、几何包装/表面网格、局部尺寸和体网格，再提供 overset、网格替换等任务。工作流根据用户声明的内部/外部流动目标生成子任务；应先核实区域、尺寸场和中间产物，再继续生成网格。

## 适用边界和总体步骤

- 已知限制包括：过薄的 wrapped region 可能与 construction surface 错误连接；局部较小 growth rate 可能扩展到全域；用已有 size-control 文件后若中间 checkpoint 文件缺失，Revert and Edit 可能触发非预期任务更新。多 CAD 文件单位需一致；不支持 2D 模型、Poly/Poly-Hexcore 网格导入，Windows 远程 Linux 节点不支持 CAD 导入；固体区不支持该工作流的 boundary layer；并行 Poly-Hexcore 可能有少量无效单元或尺寸跳变（pp. 410–412）。
- 一般顺序是导入 CAD 与建立 meshing objects → Describe Geometry and Flow 选内部/外部/混合流动或仅 skin wrapper → 封口、识别区域、设置泄漏阈值、网格控制和局部尺寸 → gap/contact/表面网格 → 边界层、overset（如需）与体网格 → zone 清理、变换或替换部件。具体任务序列会随所选目标和子选项变化。

## CAD 导入、对象树和几何准备（PDF pp. 412–481）

- **Import CAD and Part Management（4.2）**：支持多种 CAD、faceted mesh 和 Ansys 格式，具体 Import Route 随格式和平台改变。树中可只把所需零件从 CAD Model tree 移到 Meshing Model tree，或自动按 part 建对象；大模型可按对象更新以节省时间。CAD 文件树状态（update-required/up-to-date）有助于识别需要重算的输入（pp. 412–425）。
- 每 part 自动对象可设边提取、Create One Zone Per（object/part/body/face）及 refaceting；Auto 提取边在对象数超过 10,000 时不提取。自定义对象还可设 zone 命名前缀、合并子对象或继承父级设置。Meshing Operations 可组合平移/旋转/轴旋转/缩放/镜像、refaceting 和对象属性操作；refaceting 不适用于共享拓扑几何，缩放对象会跳过 refaceting（pp. 425–445）。
- **Describe Geometry and Flow（4.3）**：prime wrapper 通常更快，但对大量固体零件不具备 decoupled parallel processing；按 internal flow、external flow、两者或仅 skin surface 确定后续任务。标准选项决定是否建 cap、识别 region、处理 leakage、加厚零厚度几何、提取 edge feature、定义 porous region 或添加 overset 任务（pp. 445–447）。
- **Cap、external boundary 与 refinement（4.4–4.6）**：封口支持多种边界类型和单面/环形开口；annular cap 的内外面必须同一 label，倾斜环形开口不支持直接封口。外流边界可用相对几何比例或直接坐标建 box，也可复用已有边界，并在 surface-mesh 或 wrap extraction 间选择。局部细化可由已有体、box、cylinder、offset surface 或 offset box 定义；offset 几何按 flow direction 构建尾迹层。避免细化区互相重叠，以免造成意外局部粗化（pp. 447–460）。
- **Construction surfaces、edge features、thickness 与 porous regions（4.7–4.10）**：construction surface 可用 CAD 中已有面、box 或 offset surface 定义，以分割主流体区（例如旋转区域）；不能可靠连接到过薄的 wrapper。Edge features 有 Feature Angle、Intersection Loops、Sharp Angle 三种提取方式；需要网格节点贴合尖角时需确保对应 face zone 分开。Add Thickness 给零厚度面按 facet 法向加厚，正负偏移可控制方向。Porous region 支持文本文件、直接坐标和非矩形方式；矩形宏观多孔区网格需粗且结构化，buffer 有助于避免入口/出口接口问题（pp. 461–475）。
- **Identify Regions / Leakage / Region Settings（4.11–4.13）**：Material point 可用坐标、图形拾取、对象质心或相对偏移定位，分类为 fluid/solid/void；若 region 由 construction surface 分割，必要时显式关联该面。Leakage Threshold 允许预览并迭代最大泄漏尺寸，使用剖切面检查内部通道。Region Settings 选择主流体区、extract method（wrap、surface mesh、CFD surface mesh 或 overset existing mesh）、区域类型、fill 类型和 leakage size；surface/CFD surface extraction 的同一对象内区域不得互相相交。CFD surface mesh 直接使用原 CAD，能避免先 refacet，但 Discovery `.dsco` 需走 Workbench import route（pp. 475–481）。

## 尺寸控制、接触修复与表面网格（PDF pp. 481–497）

- **Choose Mesh Control Options / Add Local Sizing（4.14–4.15）**：尺寸控制可新建默认/自定义集合或读 `.szcontrol` / size-field 文件。Fault-tolerant 工作流区分更细的 initial wrap size（捕捉几何、识别区域）与较粗的 target size（最终解算网格），默认 wrap/target ratio 为 2/3；降低比例可更精细捕捉但提高成本。Curvature、Proximity、Soft、BOI 控制可配置 min/max size、growth rate、Cells Per Gap、曲率角等（pp. 481–486）。
- **Contact Patch 与 Gap Cover（4.16–4.17）**：contact patch 用于难以直接网格化的接触（如轮胎/地面），指定 source、ground、偏移距离和 defeaturing。Gap Cover 在表面网格前封闭间隙；可用统一 wrapper 最大 gap，或按尺寸场计算 gap 上限。分辨率、是否仅封闭不同边界区间、节点投影到 edge feature 等选项影响精度与耗时；投影更准确但大模型成本较高（pp. 486–490）。
- **Skin Surface / Generate Surface Mesh（4.18–4.19）**：skin assembly 模式会闭合 leakages/voids 并生成包覆表面，可导出到新会话。常规 surface mesh 目标 skewness 手册建议约 0.7–0.85；可保存中间文件、分离 fluid/solid contact、移除小岛面、合并固体接触 wrapper、控制最小 spike/dihedral angle、投影节点回 CAD、自动边界类型以及内部 pocket 处理。自动类型依赖 zone 名称模式，生成后默认边界 zones 分离（pp. 491–496）。
- **Update Boundaries（4.20）**：检查并重命名/重分类边界；默认仅显示外部 wall，可切换显示全部边界，并按 inlet/outlet/wall 预览（pp. 496–497）。

## Overset、边界层和体网格（PDF pp. 497–518）

- **Overset（4.21、4.25–4.26）**：Describe Overset Features 决定创建 collar mesh、component mesh；两者可由相交对象/zone/edge、offset surface、background box 或已有对象构造，指定 cell size 和填充类型。创建 overset interface 后用 Identify Orphans 检查孤立单元；可按 cell volume 或 boundary distance 选择 donor priority，配置 grid priorities 和 interface-intersection 检查。孤立单元通常提示重叠不足或网格尺度不匹配（pp. 497–502、511–513）。
- **Boundary Layers（4.22）**：为流体 wetted walls 配置 prism/inflation，可按 region 多次定义。Offset method 包括 aspect-ratio、last-ratio、uniform；设置首层高度/增长率/层数、连续或 stair-step 后处理、only-walls/all-zones/选定 zone/label 生长范围及 split prisms。Continuous 不支持 baffles，stair-step 可处理 baffle 但不能拆分；split prism 时各 stair-step controls 的层数需满足指南约束（pp. 502–506）。
- **Identify Deviated Faces（4.23）**：surface mesh 和 boundary layer 后，可自动或手动设 deviation 范围，叠加 mesh/geometry 显示偏差，并选择是否把 gap cover 纳入检查（pp. 506–507）。
- **Generate Volume Mesh（4.24）**：支持 tet、hexcore、poly、poly-hexcore；可配置区域级 fill/max cell length、并行、质量改善触发值和保存。size field 可提高局部尺寸控制能力，但并行时每个核都要复制 size field，增加内存压力；关闭 size field 时可通过 octree/boundary ratio、buffer layers、tet/poly growth rate 管理尺寸过渡。Stair-step、conformal prism split 等设置受 fill 类型和相邻区域层数约束。工作流生成网格后质量度量默认为 Orthogonal Quality（pp. 507–511）。

## 网格后处理与部件替换（PDF pp. 513–524）

- **Transform / Extrude（4.27–4.28）**：体网格可平移或旋转复制。Extrude 可从边界面向外延伸，多个面须满足共面等条件；周期/shadow 面不能直接作为普通 extrusion 面。可设 Total Height 或 First Height、层数、增长率和增长 pattern；圆柱面拉伸过高会形成无效网格，应降低高度重试（pp. 513–518）。
- **Manage Zones（4.29）**：网格生成后可按类型/面积/体积筛选 cell/face zones，再合并、重命名或改前缀/后缀；cell zone 合并可连带处理相邻 face zone，但带 face labels 的面不支持该面合并（pp. 518–520）。
- **Separate Contacts（4.30）**：分离流体 cell zones 间接触后会生成 `out_solver_f2f_set_nci.scm`；在 solver 中缩放网格后读取该 Scheme 文件以设置 mesh interfaces（p. 520）。
- **Part Replacement（4.31）**：可对已有 CAD 部件做 replacement/addition/removal。Surface Mesh Based 不要求 construction surface，但会重新网格化所有体区域；Volume Mesh Based 只重网格局部区域，速度更快，但需预先创建包围替换区域的 construction surfaces。可为替换件单独加局部尺寸和边界层，并局部更新 volume mesh；并行替换网格最终会聚合至单一 active node（pp. 520–524）。

## 证据与适用条件

来源：[[Ansys Fluent Users Guide 2026 R1]]，Part II / Chapter 4，PDF pp. 409–524。工作流默认值、支持格式与许可证/平台行为均针对 2026 R1；实际 CAD 路由、调度并行、几何质量和区域分类应按目标文件与安装配置验证。图形截图仅按正文说明归纳。

## 关联页面

- [[Part II - Meshing Mode]]
- [[Fluent 水密几何网格工作流]]
- [[Fluent 引导式网格工作流]]
- [[Fluent 网格质量诊断]]
- [[Ansys Fluent Users Guide 2026 R1]]
- [[index]]
