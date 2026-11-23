---
type: concept
created: 2026-10-16
updated: 2026-10-17
tags:
  - Ansys Fluent
  - model-topology
  - UTL
  - automation
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 模型拓扑（Model Topology）

## 摘要

User's Guide 2026 R1 Part III / Chapter 6（PDF pp. 1155–1168）介绍 Model Topology 方法：物理定义与几何/网格解耦，设置完全基于 labels——脚本化只需知道 label 无需 zone ID，可先定义物理再网格化、换网格不必重设。**启用条件：以 CFD Pro 许可级别启动并勾选 Model Topology；一旦使用不能转回 legacy 设置格式**。当前限制较多（仅 conformal 界面、不支持周期性/NETM/shell conduction 等）。

## 6.1 概念与收益（PDF pp. 1155–1158）

传统方式把边界条件等定义在载入的网格上；Model Topology 把物理定义挂到"模型拓扑"（位置）上，物理与几何分离，命名得当时换网格无需重定义设置。

**收益**：

- 设置完全基于 **labels**（等价于名字与命名选择）——**脚本化只需知道 label，不需要 ID**。
- 平台与核数无关的设置。
- labels 可分组，少量组代替大量 zone——树更小：case 读写更快、含边界/zone 列表的对话框（含 physics volumes 与边界条件编辑）打开更快。
- 设置与特定拓扑表示解耦：**可先设置物理再网格化**；几何/网格可变只要 labels 不变；相似问题间易于迁移（模板）。
- 拓扑信息经 **CFF** 持久共享——Fluids Business Unit 各产品一致的基于 label 的设置交换；EnSight 与 CFD-Post 可一致地比较与后处理结果。
- 模型专属 zone 在后台自动创建（如某些多孔模型）。

**树结构三分支**：Model Topology（模型几何的 bodies/parts/faces/groups，可分组）；Physics（physics volumes/boundaries/interfaces；Physics 分支右键 **Group By** 可选 Physics Type（默认）或 Adjacency；右键 physics 定义 → Location... 打开 Edit Physics Location 指定应用的几何 body/bodies/group）；**Interfaces**（统一泛化网格界面——处理区域间保形与非保形连接，设置独立于网格连接性；含周期界面）。多数情况下**拆分默认体积或创建新体积时界面自动定义**（p. 1157–1158）；未自动定义时右键 Interfaces → Auto Create，或 New Interface... 手动创建（此概括与 6.5 的操作口径存在手册内部张力，见 6.5 节标注）。树中图标区分固-流/固-固/流-流界面。

## 6.1.3 限制（2026 R1，PDF p. 1158）

- **不支持图形驱动工作流**：直接在图形窗口对项目做选择/改设置可能不符合预期。
- **仅支持 conformal 界面**：原父边界列在 Interface 节点下；这些"普通 wall"的物理设置只适用于 Leftover（非重叠）部分——纯保形网格下该面积为零；计算中或从非一致网格替换网格时该面积可能变为非零，此时会使用这些 wall 设置。
- **周期性尚不支持**；**非平衡热模型（NETM）尚不支持**；**shell conduction 尚不支持**。
- 把拓扑 body 从一个 physics volume 改到另一个时，关联的 physics boundary 可能难以重新指派（该边界仍是旧 volume 的子项、选不到新位置）——此时须删除该 physics boundary 定义、在新 volume 位置下重建（手册 body.1/outlet.1/volume1/volume2 示例）。
- （仅 Fluent WebUI）连接运行会话时软件错误地允许创建同名多个表面，case 保存重读后出问题——表面命名须避免重名。

## 6.2 启用（PDF pp. 1159–1160）

- **以 CFD Pro 许可级别启动**（Capability Level 下拉），并在 General Options 页启用 Model Topology。
- 偏好 **Unified Topology Layer** 使该功能在 **Meshing 与 Solution 两个 workspace** 都可用（与 [[Fluent 水密几何网格工作流]] 3.2 的 UTL 同源）。
- 其他 Model Topology 偏好：Initial Physics Volume Definitions（基于几何创建最少 physics 定义）、Create default UTL object as per need、Skip creation of groups pointing to single entity（后两项手册未附说明文字）。
- **Important：一旦开始以 Model Topology 方式处理 case，不能转回 legacy 设置格式。**

## 6.3–6.4 网格化与算例设置（PDF pp. 1160–1168）

- **网格化**：Model Topology 仅支持 Watertight Geometry 工作流；与非 UTL 版的唯一区别是涉及 CAD 选择的任务多了 topology 选项——用 topology 选项可保证 meshing 中的选择带入 solver。
- **从几何开始**：走 watertight 工作流，输入与步骤与 non-UTL 一致；区别是 Add Local Sizing、Update Boundaries 等任务可按拓扑或 label 选择几何 body。从 meshing 起步时，可用 **Create Physics on Meshing to Solver Switch** 偏好控制在切到 solution workspace 时是否自动为所有几何边界创建物理条件。
- **新 physics volumes**（两种方法）：首选从默认体积 **Split**（右键 fluid/solid → Split in to New Volume... → 命名并选拓扑位置；Fluent 把 body 从默认区移到新区，避免对所选拓扑 body 过指定）；或右键 Volumes/fluid/solid → New Volume → <类型>（命名、选位置、定义设置——**此法不自动创建界面**）。
- **新 physics boundaries**：meshing 中定义的边界在 solver 中被尊重并正确分类；右键 Boundaries 分支 → New Boundary → 类型 → 选位置；也可从现有边界 Split（机制同体积拆分）。
- **Important：物理应用位置任何时候都可改；但运行仿真后改位置会使"变更过的 physics volumes/boundaries"上评估的结果失效——改位置后须重跑求解器才能保证后处理结果有效。**
- **默认 volumes/boundaries 两类**：新会话默认创建的（通用名 fluid/Solid/wall；CAD 与 Fluent Meshing 的 named selections/labels/groups 也会默认建边界）；以及删除指向拓扑位置的 physics 定义后出现的默认项——带 **[Default] 标签、是"active"的**：再删除其他 physics boundary 时其原位置会并入该 default boundary（通用名如 default_wall）。
- **检查与视觉提示**：除 console/对话框消息外，Model Topology 额外检查设置完整性——问题分支显示感叹号图标；**先右键最嵌套（最小子）分支选 Error details/Warning details 打印消息，通常先解决最小元素即可连带解决上层问题**；位置对话框中绿色对勾 = 已有物理的拓扑位置（避免过指定）。
- **显示/着色**：可按 model topology 或 defined physics 显示；**着色 By Association 取代按 surface ID**——By Topological Body（单 body 单色）/By Topological Face（每面一色，似随机）/By Physics Volume（同 volume 同色）/By Physics Boundary；树右键显示时 Model Topology 用 By Topological Face、Physics 用 By Type；无选择右键图形窗口可设 Color By Association（仅非持久 mesh 显示）。
- **报告与后处理**：定义 report definitions/后处理对象时默认只列出已定义的 physics 位置；需要更细粒度位置时，**右键带箭头（>）的 physics volume/boundary → Show Location 展开其拓扑位置**。

## 6.5 重要事项（PDF p. 1168）

- 检查界面是否正确定义：**Split in to New Volume 会自动创建所需界面；New Volume 方式不自动创建任何界面**——用后者时须手动补（Interfaces → Auto Create 或 New Interface...）。（注意：6.1.2 概述句称"拆分或创建新体积时界面自动定义"（p. 1157–1158），与本条存在手册内部表述张力；6.5 是章节末尾的操作性告诫，实践中按"New Volume 不自动建界面"对待，创建后核对 Interfaces 分支。）

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part III / Chapter 6，PDF pp. 1155–1168；目录范围至此完成（Ch.7 自 p. 1169 起）。Figures 6.1–6.8 与界面图标为图形元素，仅文字机制被摄取。本页全部主张已于批次 33（2026-10-17）以 pypdf layout 模式提取全章逐节比对核验，未发现与原文不符处。
- 该功能为 2026 R1 的较新/演进中特性：限制清单（仅 conformal、无周期性、无 NETM/shell conduction、WebUI 重名问题）为手册明确陈述，升级版本后须重新核对。
- 与 [[Fluent 水密几何网格工作流]] 3.2 节的 UTL 任务清单互补（那里列的是 meshing 侧可按拓扑选择的任务）。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 水密几何网格工作流]]（3.2 UTL；6.3 所依赖的 Watertight 工作流）
- [[Fluent 求解模式 GUI]]（Outline View/树基础）
- [[Fluent 表达式语言]]（基于 label 的设置与表达式位置引用互补）
- [[index]]
