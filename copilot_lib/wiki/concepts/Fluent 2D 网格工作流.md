---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - 2D
  - workflow
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 2D 网格工作流

## 摘要

Fluent User's Guide 2026 R1 Part II / Chapter 5（PDF pp. 525–538）介绍在 Fluent Meshing 的常规 3D 环境中为二维几何建网格的引导工作流。核心链路是导入 CAD、检查区域和边界、定义全局/局部尺寸、可选 MultiZone 与 2D shell boundary layers、生成初始表面网格，最后专门导出 2D mesh 文件；如需，也可做轴对称旋转扫掠或网格挤出。

## 工作流与几何导入（PDF pp. 525–530）

- 2D Workflow 适用于常见二维几何网格操作。更新任务期间显示的边颜色表示拓扑连接：单面邻接红色、同面两侧青色、两不同面黑色、三面相连洋红色、四面相连黄色（p. 525）。
- Load CAD Geometry 支持 `.dsco`、Workbench `.agdb`、`.fmd`/`.pmdb`、`.scdoc`/`.scdocx`、SAT 和 Parasolid 等格式。Windows 导入 Discovery 时可保存中间 `.pmdb`，Linux 可直接用该中间文件；源 `.dsco` 更新后旧 `.pmdb` 会被覆盖。工作单位应使最小网格尺寸量级约为 1，导入 solver 时网格会缩放到米（pp. 526–528）。
- 可选择 Native、DSCO、Parasolid 或 Workbench import route；可 refacet 并设置 facet resolution、deviation、normal angle 和最大边长。细 facet 能更好表示曲率和几何细节，但增加计算资源需求。更新 Regions 可设 fluid/solid/dead；Update Boundaries 可按 label/zone 重命名或修改边界类型，二维边界列表额外包括 `axis`（pp. 527–529）。

## 全局尺寸、局部控制与 MultiZone（PDF pp. 530–533）

- Define Global Sizing 设最小/最大尺寸、growth rate 和 curvature/proximity/二者组合。Curvature Normal Angle 默认 18°，约对应圆柱周向 20 个面；Cells Per Gap 可为实数，最低 0.01。若另有局部尺寸控制，全局曲率/邻近控制会附加参与尺寸场计算（p. 530）。
- Add Local Sizing 必须在 Generate Initial Surface Mesh 前加入。支持 edge size（需要 CAD edges）、face size、BOI、curvature 和 proximity 控制；按 zone 或 label 指派。Curvature / proximity 控制可限定作用于 face、edge、两者或 edge label，并配置局部 min/max、曲率角、Cells Per Gap。若表面网格已生成后才追加尺寸控制，需 revert and edit 已有控制或重导几何以刷新对象选择列表（pp. 531–532）。
- 选择 MultiZone mesher 后，可按 Interval、Size 或 Smallest Height 对边进行 sizing，并配置增长 pattern；variable pattern 可按 Growth Rate 或 Bias Factor 指定增长（p. 533）。

## 2D 边界层、表面网格和输出（PDF pp. 533–538）

- Add 2D Boundary Layers 沿所选边生成 shell layers。Offset method 有 aspect-ratio、last-ratio、uniform 和 smooth-transition；可指定层数、增长率、edge label/zone、all adjacent faces 或限定的生长面，并可设置 gap factor、最大/最小长宽比、相邻三角形局部重划、拉伸四边形细化、投影角及目标面 skewness（pp. 533–535）。
- Generate Surface Mesh 控制初始二维表面网格，可启用四边形生成（启用后 Split Quads 不可用）、投影节点回 CAD 或多线程。投影到几何与多线程不能同时使用；可按 label 合并 edge/face zones。此任务输出的是 conformal connected surface mesh（p. 535）。
- 该工作流运行在常规 3D Meshing 环境，因此不能直接切换至 2D solver；应通过 Exporting the Fluent 2D Mesh 写出专用文件供 2D Fluent solver 读取。该专用 2D mesh 不能再读回 2D workflow；若需继续修改，可另写 3D mesh 后回到该 workflow（p. 536）。
- Axisymmetric Sweep 可指定旋转轴原点/方向、角度和层数，把 2D 轴对称网格旋转成 3D 网格。Extrude Mesh 从共面边界延伸表面网格，可设总高度或首层高度、normal/direction-based faceting、层数、增长率和增长 pattern（pp. 536–537）。

## 证据与适用条件

来源：[[Ansys Fluent Users Guide 2026 R1]]，Part II / Chapter 5，PDF pp. 525–538。文件格式、导入平台支持和默认网格设置对应 2026 R1；该章节范围止于 p. 538，Chapter 6 从 p. 539 开始。

## 关联页面

- [[Part II - Meshing Mode]]
- [[Fluent 网格模式入门]]
- [[Fluent 网格质量诊断]]
- [[Ansys Fluent Users Guide 2026 R1]]
- [[index]]
