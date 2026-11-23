---
type: concept
created: 2026-10-17
updated: 2026-10-17
tags:
  - Ansys Fluent
  - motion-definitions
  - auxiliary-geometry
  - dynamic-mesh
  - adaption
  - solution-mode
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 运动定义与辅助几何

## 摘要

本页覆盖 User's Guide 2026 R1 Part III 的两个短章（批次 52–53）：**Ch.12 "Managing Motion Definitions"（pp. 1851–1853；p. 1854 空白）**——运动定义的创建与管理（用于刚体动网格区与局部参考帧，支持表达式/输入参数）；**Ch.13 "Managing Auxiliary Geometry Definitions"（pp. 1855–1860）**——辅助几何定义的创建与管理（用于 PUMA 几何自适应、变形动网格、滑移网格边界投影；四种定义类型）。

## Ch.12 运动定义管理（pp. 1851–1853）

- **用途**：运动定义（motion definition）= 名称 + 参考帧 + 平移定义 + 旋转定义，用于**刚体动网格区**（Rigid Body Motion，p. 1970）与**局部参考帧**（p. 1202）。优点：给动网格区定义刚体运动比 profile/UDF 更简单；**支持表达式和/或输入参数**定义运动。
- **创建**：Setup → Motion Definitions → Manage... → New... → Motion Definition 对话框：
  1. **Name**；
  2. **Reference Frame** 下拉——默认全局参考帧或已建的局部参考帧（[[Fluent 网格读取与操作]] 7.4）；
  3. **Type**：**Rigid Body Motion**（自定义平移/旋转分量）或 **System Coupling Motion**（外部刚体求解器经 System Coupling 给定运动；仍须把运动指派给 cell/boundary zone，见 p. 1970；System Coupling 能力与限制见 p. 4849）；
  4. **Translation 组**：Velocity_X/Y/Z（3D 含 Z）——各可为**常数/表达式/输入参数/命名表达式**；
  5. **Rotation 组**：Axis_X/Y/Z（3D；2D 轴向恒为正 Z）+ **Speed**（相对定义轴按右手定则）——同样四类输入；
  6. OK 保存；可重复建多个。
- **管理**（p. 1853）：Manage 对话框选中定义显示 Properties；**Edit...** 修改、**Delete** 删除。

## Ch.13 辅助几何定义管理（pp. 1855–1860）

- **三个用途**：
  1. **PUMA 边界自适应**（默认多面体非结构自适应，p. 3979）——自适应新生成节点投影到几何定义上，使网格更贴合几何（概念见 Theory Guide Geometry-Based Adaption）。
  2. **变形动网格区**（Deforming Motion，p. 1974）——变形网格节点投影到辅助几何上；**提供除 UDF 外本不可用的变形区形状**。
  3. **滑移网格仿真**（p. 1868）——把一个/多个边界区的节点投影到与辅助几何重合（见 [[Fluent 网格读取与操作]] 7.12.10）——保证非一致界面的边界对面节点在同一平面/曲面上，减小仿真误差。
- **创建**：Setup → Auxiliary Geometry Definitions → Manage... → New... → Auxiliary Geometry Definition 对话框：
  1. **Name**；
  2. **Type** 四种：
     - **Primitive**：**Cone / Plane / Sphere / Frustum（锥台）/ Cylinder** + Definition 组内其余设置。**Note**：① Frustum 的 Lower Radius 在 Frustum Origin 端、Upper Radius 在另一端；② **Frustum 与 Cylinder 的几何只含曲面——不含两端圆平面**（端面需另建 Plane primitive）；③ Plane 的简便定义：**Compute from a Face Zone...** 按钮 → 选一个平面 face zone → Compute 自动填充（可先 Display 核对该区）。
     - **User-Defined**：已编译的 UDF（须用 **DEFINE_GEOMETRY** 宏）。
     - **Surface Mesh**：用**单独网格文件中的表面区**定义几何——Surfaces Meshes... → Read... → 选 case/mesh/**STL** 文件（注意选择建网格时的单位）→ 关闭对话框 → Background Mesh 下拉选表面区（读表面网格见 p. 1201）。
     - **Reconstruction**：由 Face zones 列表选中的一个/多个边界区**重建**——基于当前节点坐标建光滑背景模型。**若要保持在两边界区交界处的尖锐特征边，应把两个区放在分开的几何定义里**（否则交界边在重建中会被磨圆）。
  3. **Display 验证**：Display 按钮在图形窗口显示；Display Options... 可调——**Draw Mesh**（同时画网格，打开 Mesh Display 对话框）、**Faces**（着色面 + Face Color）、**Edges**（边 + Edge Color/Edge Thickness）、**X/Y Resolution**（primitive 曲面离散面数——X 沿长度方向或 Sphere 的 z 向、Y 沿周向或经度；值越高分辨率越高）。
  4. OK 保存；可重复建多个。
- **管理**（p. 1860）：Manage 对话框选中定义显示 Properties；**Edit...** 修改、**Display** 显示、**Delete** 删除。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III Ch.12 与 Ch.13；本页覆盖批次 52–53（2026-10-17）实际读取的 pp. 1851–1860，**两章全部完成**（p. 1854 为空白版权页；p. 1860 为 Ch.13 正文收尾）。
- 无公式与提取缺口；Figures 12.1–12.2、13.1–13.5 为图形元素未摄取。
- 关联章节引用（Rigid Body Motion p. 1970、Deforming Motion p. 1974、Refining and Coarsening p. 3979、Using Sliding Meshes p. 1868、局部参考帧 p. 1202、System Coupling p. 4849）仅作定位；滑移/动网格细节见 [[Fluent 滑移与动网格]]（Ch.14，批次 54–55 后生效）。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 运动参考系]]（局部参考帧与 MRF）
- [[Fluent 滑移与动网格]]（Ch.14 动网格区与变形区定义的落点）
- [[index]]
