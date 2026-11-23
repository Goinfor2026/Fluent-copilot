---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - watertight
  - workflow
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 水密几何网格工作流

## 摘要

User's Guide 2026 R1 Part II / Chapter 3 描述 Watertight Geometry 引导工作流的全部任务（3.1–3.28，PDF pp. 301–408）。本页现覆盖全章：批次 9 的 3.1–3.6（pp. 301–326）以及本轮批次 10 的 3.7–3.28（pp. 326–408）。

## 章总览（PDF p. 301）

Watertight Geometry 工作流的任务文档目录：3.1 限制、3.2 UTL、3.3 Import Geometry、3.4 Import BoI Geometry、3.5 Add Local Sizing、3.6 Generate Surface Mesh、3.7 周期性边界、3.8 Describe Geometry、3.9 Share Topology、3.10 Enclosing Fluid Regions、3.11/3.12 Create/Update Regions、3.13 Thin Volume Meshing、3.14 Boundary Layers、3.15/3.16 Multizone、3.17 Volume Mesh、3.18 Update Boundaries、3.19 Improve Surface Mesh、3.20 Add Boundary Types、3.21 Improve Volume Mesh、3.22 Transform、3.23 Extrude、3.24 Linear Mesh Patterns、3.25 Manage Zones、3.26 Modify Mesh Refinement、3.27 Local Refinement Regions、3.28 Run Custom Journal（3.7 起待摄取）。

## 3.1 工作流限制（PDF pp. 302–306）

总体限制（手册明确陈述）：

- 在工作流中抽取流体体积要求所有包络固体网格保形（conformal）。
- 导入 SCDM 文件时，位于另一 body 内部的表面 body 会直接关联到该 body；变通：在 SCDM 中用 named selection，或在 Add Local Sizing 任务中用 zone 选择。
- 命名语法：SCDM 导入时名称中的冒号 `:` 一律转连字符；body/component/named-selection 名不应以数字、特殊字符、大写字母或符号开头。所有 BoI body 必须唯一命名。
- 在另一会话/另一台机器上对 up-to-date 任务执行 revert and edit，需要 CAD 文件（`.pmdb`）、对应的工作流目录（`filename_workflow_files`）与正确的 CAD 配置齐备，且任务从工作流树的最后位置更新。
- 不支持多个周期系统。工作流只支持单一 mesh object，**不支持非一致网格设置**。
- capping、local sizing、update boundaries、modify mesh refinement 任务中：用 **labels 的选择跨设计变更保持持久，用 zones 只在同一设计内持久**。
- 需要改变拓扑/几何/网格时，应通过 Custom Journal 任务纳入工作流以保持持久（见 [[Fluent 引导式网格工作流]] 2.3 节）。
- **导入任务**：Discovery `.dsco` 须先在 Discovery 中把备选许可证偏好设为 ANSYS CFD PrepPost；含面离散几何的 `.dsco` 须对所有"面"用 Named Selections 以保住面离散；**不支持导入 2D 模型**；不支持 `.tgf` 面离散几何；BoI body 追加仅完全支持经 custom journal。选 Mesh 格式导入时：工作流生成的表面网格不得再从此任务导入（应 File > Read > Mesh）；导入网格总是按区域分离；只支持完全连通的网格（`.stl` 可用但须全连通、细分精细）；hanging-node 自适应网格、Cutcell 网格、不连通面离散几何（`.tgf`/`.fmd`）不支持；非 100% 保形的衍生表面网格可能无法重划成保形网格；带非一致细化的体网格不支持；**空洞无法探测**，默认区域分配可能与导入对应 CAD 时不同；外部来源 CAD 在 SCDM 清洗后须以同版本 SCDM 写出 `.pmdb` 供工作流使用，或直接在 Discovery 中清洗。
- **生成表面网格任务**：要读回工作流此前生成的表面网格，须先在 Outline View 删除全部几何/网格对象；使用 Shared Topology 任务时，表面网格的三个高级选项（自动 zone 分离、自动重划去除节点聚集、最终表面网格改进）**实际在 Shared Topology 任务末尾执行**；同一 body 既赋面 label 又赋 body label、或多 body 共用 body label，部分区域可能被误标 dead region；size field 含 BoI/Face of Influence 时不能用 Size Field File 选项（改提供 size control 文件）；用复制实际模型方式创建的 BoI 可能带上 named selections，导致生成表面网格出错，应避免；无局部尺寸且 Auto Remesh 为 Auto/No 时，即使只选 Proximity 也会存在 18° 曲率角——变通：同时选 Curvature 并用更大角度（如 60°）。
- **线性网格图案**：不能对含空洞的 part/对象创建 pattern；已在其他 pattern 中使用的 part 不能再用于 pattern。
- **周期性边界任务**：导入的"body"实际只是面时用手动方法设周期性；**CFD Pro 能力级别下此任务不可用**；Automatic - pick both sides 在无平面面、或平面面法向与圆弧扇形切向不对齐时无法推导参数；旋转周期角过小（约 <10°）时建议 Manual - pick reference side，周期角最好在 SCDM 用弧角+弧半径测量；**任务必须在 Share Topology 之后、Describe Geometry 之后执行**。
- **Share Topology**：两 body 间隙不得超过间隙面处局部网格尺寸的 1/2；跨间隙面平行时共享成功率更高；曲面间共享时曲率角 ≤12° 成功率更高。
- **边界层**：从文件读入 prism control 文件时高级选项（acute angles、invalid normals 等）不支持，且文件读入与任务内新建控制之间的冲突不被系统检查；全局边界层设置位于 Generate Volume Mesh 任务；工作流不再支持用 custom journal 读外部 `.pzmcontrol` 文件。
- **多区域网格**：个别复杂几何中 multizone 会因近区采用 uniform-based 而非 pave-based 而过度细化——微调尺寸分配可解。
- **体网格设置**：invalid normals 过多（>10000）时 Add Boundary Layers 的 Modify Surface Mesh at Invalid Normals? 应设 no，否则体网格生成可能出问题；非流形边连接不支持（内部挡板类非流形连接例外；变通：用面连接或在边连接处断开）；**不同区域不能用不同体网格类型**；持久改名仅在 body 名唯一时保证持久；最差质量低于 Advanced Options 的 Quality Warning Limit 时自动显示最差单元位置（Improve Volume Mesh 同规则）。
- **拉伸体网格**：预览框只对手法向与笛卡尔坐标对齐的选中面可用；圆柱面拉伸过高会产生无效网格——减小总拉伸高度重复操作。
- **Modify Mesh Refinement**：细化基于现有网格（不是几何）作参考几何——几何上未被良好捕捉的特征无法借此改善。
- Named Selection 定义在多个 body 上时，工作流能识别该名字但**不会**把该组当作单一 region 合并；body 分离为独立 cell zone 也分离边界 zone，复杂模型 zone 数会显著增加。

## 3.2 Unified Topology Layer（UTL）（PDF pp. 306–307）

UTL 可用于 Watertight 工作流；**启用方法：以 CFD Pro 许可证级别启动 meshing mode**。UTL 网格下，以下任务可按拓扑（而非网格实体）选择几何 body：Add Local Sizing、Set Up Periodic Boundaries、Create Local Refinement Regions、Add Boundary Type、Describe Geometry、Enclose Fluid Regions (Capping)、Set Up Periodic Boundaries（仅插入于生成表面网格之后）、Add Thin Volume Meshing Controls（仅 Stacked Plates 启用时）、Add Boundary Layers、Add Multizone Controls、Update Boundaries、Manage Zones（仅插入于生成体网格之前）、Extrude Volume Mesh、Axisymmetric Sweep、Transform Volume Mesh。另可在工作流任意点添加 Create Group 任务，把现有 UTL 拓扑中的面（bodies、faces 或两者）合成复合组。

## 3.3 导入几何（PDF pp. 307–311）

Import Geometry 任务指定仿真用几何或表面网格：

1. File Format：CAD（默认）或 Mesh。Note：先前由其他工作流从 CAD 生成的表面网格不要从本任务导入——用 File > Read > Mesh；若必须用于本工作流，先 Read Mesh，再在 Outline View 删除对应几何对象后保存网格、再导入。
2. CAD 格式下 Import Type 可选 Single File（默认）或 Multiple Files（多选须同目录同 CAD 格式）。
3. Mesh 格式须指定 File Unit；图形窗口标尺旁与 Distance 工具计算时显示单位。
4. Units：应选用使网格最小尺寸约为 1 的量纲单位；**网格转入 Fluent solver 时自动缩放为米**。
5. Use Body Labels：CAD 含要用的 body labels 时设 Yes（无 body labels 时自动 No）。Note：NS 只赋予单一 body 时作为 body label 支持；Yes 时另支持多 body 共享 NS 的"复合 body labels"；无标签/单标签 body 与新创建区域同样列出；表面 body 上的 NS 在 Update Boundaries 任务中可能不被识别为 label。
6. Advanced Options：
   - **Model includes shrink-wrapped bodies?**：Discovery 等 CAD 环境中 faceting/wrapping 产生的非 CAD 几何须设 yes 以正确管理；此时所有面离散 body 只应以 "*wrap"（或默认 "shrinkwrap"）结尾命名，其他 body 不得使用该模式。应 shrink wrap 面离散 body 以保证表面网格质量；每个 wrapped body 在 CAD 环境中应有独立 component。
   - **Automatic Object and Label Creation?**（Mesh 导入）：默认 yes；设 no 不创建 labels、只建一个含全部 zone 的 mesh object，可显著加快超大算例导入。含 "boi" 字符串的 zone 不建对象。
   - **Separate Zone By**：region / region & angle（配 Separation Angle，默认 40°，角度越小分离面越多）/ face,edge topology / **none（默认）**。局部尺寸必须依赖 zone 分离：body sizing/BoI 用 region 分离即可，局部面尺寸需按角度分离，multizone 需按 face 分离（自动创建全部 edge labels，保留面/边拓扑；体网格后按 body/region 自动并回）。选 face 的代价与限制：仅小部分用 multizone 时不推荐（边标签创建/共享计算昂贵）；不能再按角度分 zone；面无角度的面内边会使 multizone 失效；CAD 中边上的 named selections 被忽略；生成体网格前不能再插入/使用 Manage Zones 任务。
   - **Use custom faceting**：Tolerance 建议设为最小尺寸的 10%（默认 0 = 最粗面离散）；Max Facet Length 避免过大面片。
7. 支持文件：Discovery `.dsco`、Workbench `.agdb`、`.pmdb`；Mesh 格式支持多文件与 `.stl`（须全连通、质量合理）。**`.dsco` 仅 Windows 支持**；导入 `.dsco` 时 Fluent 同时生成中间 `.pmdb`（须与 `.dsco` 同目录；Discovery 中改动后重导会覆盖它；`.dsco` 未变时优先读 `.pmdb` 更快）。Linux 流程：在 Windows 用 Import CAD Geometry 对话框勾选 Save PMDB (Intermediary File) 生成 `.pmdb` 后拷到 Linux 供工作流使用。
8–9. 手动输入文件名后点 Import Geometry（浏览选择则自动执行）；改动用 Edit→Update / Cancel。

## 3.4 导入 BoI 几何（PDF pp. 311–312）

BoI 常在独立 CAD/网格文件中定义。Import Body of Influence Geometry 任务**须在 Import Geometry 完成后加入**：File Type CAD 或 Mesh；长度单位沿用 Import Geometry 任务；可指定多个 CAD/mesh 文件（多文件、每文件多 body 均可）。**不允许导入含连接 body/区域（如已共享拓扑）的几何**。支持 `.dsco`/`.agdb`/`.pmdb`（PMDB 中间文件规则同 3.3）。完成后 Add Local Sizing 任务自动启用。

## 3.5 添加局部尺寸（PDF pp. 312–316）

Add Local Sizing 定义作用于局部几何/网格部分的尺寸控制；可加任意多条（作为子任务挂在父任务下），但**只能出现在 Generate the Surface Mesh 之前**。Would you like to add local sizing? 默认 no。每条控制：Name（默认随类型变）、Growth Rate，Size Control Type 七种：

- **Edge Size**：按边尺寸细化（仅当导入几何含 named edges 可用）。
- **Face Size** / **Body Size**：按面/体尺寸细化；CAD 含 body labels 且 Use Body Labels=Yes 时任务列出可用 body labels（不可在图形窗口点选）。
- **Body of Influence（BOI）**：对落入 BoI 边界内的所有部分赋最大尺寸。BOI 规则：不得与 CAD 模型本体在 SCDM/DM 中共享拓扑；在 SCDM/DM 中唯一命名；**所有导入的 BOI body 必须各配一条局部尺寸控制**；BoI 初始不封闭时可用 Repair Body of Influence。分配尺寸须小于 BOI 自身且不与其贴合对齐（避免误触发 share topology 的薄区警告）；即使不把 BOI 纳入 share topology，其父 body 在 SCDM 中启用了 Share Topology 属性时仍会影响重叠 BOI。
- **Face of Influence（FOI）**：BoI 的非封闭、非连通面版本（如运动物体后的尾流面）；该面在表面网格阶段被删除，细化在体网格阶段可见。
- **Curvature**：Local Min Size、Max Size、Curvature Normal Angle、Scope to（faces/edges/both/edge labels；选边即选特定面的边）。适合大小尺度混合模型。
- **Proximity**：Local Min Size、Max Size、Cells Per Gap（间隙内单元层数，可为实数、最小 0.01）、Scope to、**Ignore Proximity Across Objects?**（yes 时忽略两物体间人工细小间隙——装配体中重复面/边导致的过度细化与开销——按 body 生成单一 proximity 控制，且同步把 Generate the Surface Mesh 的同名选项设为 Yes）。Scope 为 faces / faces+edges 时可加 **Refine Thin Regions (Ignore Orientation)?**：在板间等薄区周围细化而不整体过密；忽略空洞内的面邻近、不会在薄空洞中细化，适用于基本无薄固体的流体区。
- Target Mesh Size 点击时图形窗口显示红色框预览（Clear Preview 隐藏）；Draw Size Box 显示红立方体。
- 应用对象选择：按 zone 名或 label 名列表（labels 源自 CAD 几何），支持 Filter Text/Use Wildcard 与布尔 `^ | &`（语义见 [[Fluent 引导式网格工作流]] 2.10）。
- 注意：表面网格已生成后再想加一条 local sizing，须 revert and edit 至少一条现有控制（或重导几何并更新该任务）才能正确看到可用对象。

## 3.6 生成表面网格（PDF pp. 316–326）

Create Surface Mesh 任务在导入几何的所有对象上生成保形连通表面网格，或对导入的表面网格整体/局部重划；多数情形默认值即可用于 CFD。

1. **Use Custom Size Field/Control Files?**：No（默认）/ Yes, size field file（含 Preview Size Field；size field 含 BOI/FOI 时不可用，改提供 size control file）/ Yes, size control file / Yes, both files（文件说明见印刷页码 p. 623）。
2. 导入的是表面网格时选择重划范围：未加局部尺寸——All（默认）/Selected（不能全选，全选请用 All）/None（改了导入网格的尺寸必须要 local size control）；已加局部尺寸——All / Assigned in Local Sizing（含预览）/ Assigned and Selected（相邻 zone 总是随已指派 zone 一起包含）。
3–6. Minimum/Maximum Size（面片尺寸上下限，红框预览）、Growth Rate、Size Function：Curvature（按曲率）、Proximity（按每间隙单元数）、默认 Curvature and Proximity；加了局部尺寸时这些控制会**追加**在局部尺寸之后共同决定表面网格尺寸（Size Functions and Scoped Sizing，印刷页码 p. 612）。
7. Ignore Proximity Across Objects?——计划在 Share Topology 用 Interface Connect 方法时**手册强烈建议**启用。
8. Curvature Normal Angle 默认 18°，大约等效圆柱周向 20 个面片。
9. Cells Per Gap 可为 ≥0.01 实数（Proximity，印刷页码 p. 615）。
10. Scope Proximity To：edges/faces/both。
12. **Separate Out Boundary Zones by Angle?**（默认 No）：Yes 时按 Separation Angle 分 face zone——CAD 中未预定义 inlet/outlet/capping/局部边界层等 named selections 时需要；角度越小 zone 越多；只在确需分面（capping/边界条件/特定面边界层设置）时才设 Yes；后续可在 Generate the Volume Mesh 中重新并 zone。
14. **Advanced Options**：
   - **Check Self-Intersection?**：检测自交面（例如漏做 share topology 时）；大模型耗时长，初检通过后可安全关闭。手册给出三分支策略：不确定是否需要 share topology→开检查（默认设置），share topology 会自动启用；确定需要但要控制设置→关检查、手动启用 Apply Share Topology 任务；确定不需要→关检查、不启用该任务（省大型网格的开销）。导入表面网格天然损失部分拓扑信息，判断更难；用 CAD plug-in 时同此策略适用。
   - Smooth Folded Faces/Repair Free Nodes Limit：限制表面网格创建时折面修复的程度。
   - **Auto Assign Zone Types?**：表面网格创建期间按名称模式自动赋边界类型，规则与 2.1 映射表同源但**更细**（fan 还匹配 `*fan.*`、`*fan:*`、`*fan_*`；interface 匹配 `*interface*`；internal 匹配 `*internal*`/`*interior*`），并只对**外边界 zone** 赋值（名为 "inlet" 的内部 zone 不会被设为 velocity-inlet）。
   - **Invoke Quality Improve?**：对 skewness 超过 Quality Improve Skewness Limit 的三角形尝试改进，连续四次采用更大相邻角直到 Quality Improve Max Angle；仍超过 Quality Improve Collapse Skewness Limit 的三角形以固定 120° 上限被激进移除。
   - **Set Volume Mesh Max Size?**（默认 no）：yes 时指定体网格最大尺寸，省去生成体网格时额外的 size function 计算（配合 BOI 使用）。
   - **Remove Steps? + Max Step Width**：清除原始 CAD 遗留的小台阶段差伪影（如 90° 台阶被抹平，消除人工压损）；发生在 auto-remesh 之前可能局部粗化。**台阶移除条件**：台阶与相邻面不属于任何 named selection，或属于同一 NS；同 face zone/label 内一起处理；保护台阶的方法：给台阶或其相邻面加 label、或做 zone 分离（zone 内一个受保护台阶可保护全区台阶）；想要更干净的台阶移除可临时关闭质量改进。也可在 Improve Surface Mesh（3.19）中执行。
   - **Preserve Internal Surface Features?**：保留/提取小边特征（Figure 3.3–3.5 示意），仅 CAD 导入可用；设 yes 后无论 Auto Remesh 选项如何都提取。
   - **Auto Remesh to Remove Clustering?**：去除节点过度聚集。auto 行为分三种：导入网格文件——默认不重划（仅全量重划且显式设 yes 才执行）；导入 size field 文件——默认不重划，应显式设 yes；其余情形——仅当工作流含 Add Local Sizing 时才自动重划。可另选 **"no, use re-faceting"**：远快于自动重划，适合由面面邻近驱动的薄体网格而原始面离散不够细的场景。
   - **Parallel Region Compute?**：大量保形区域时加速区域计算；代价是丢失节点曲率数据（影响表面重划）；仅支持保形区域。
15. 执行时对含多 part 的 CAD 装配体，Fluent 检测几何是否启用了 shared topology；未启用则（在 Describe Geometry 内）向工作流提供 Shared Topology 任务（3.9，印刷页码 p. 332）以识别并闭合问题间隙、选择 join/intersect。任务完成后 console 输出信息与统计（body labels 的倾斜单元数、平均/最大 skewness、面数等）。
16. 进一步表面质量改进可用 Improve Surface Mesh 任务（3.19，p. 372）。

## 3.7–3.12 周期边界、几何描述与区域定义（PDF pp. 326–343）

- **周期边界（3.7）**：可设旋转/平移周期；若同时需要共享拓扑，先执行 Share Topology。自动双侧识别需要两组 zone/label；无平面面或法向无法匹配扇形切向时可能不能推导参数。旋转角很小时（约小于 10°）优先手动指定参考侧；平移周期建议在周期面加 proximity 控制，Cells Per Gap=2。任务不能在 CFD Pro capability level 使用；在表面网格生成前插入时只能按 label 手动选边界。多个周期面不可共享边，且同一 region 不支持多周期与 multizone 组合（pp. 326–330）。
- **Describe Geometry（3.8）**：按纯固体、无空腔纯流体、或流固混合/含空腔选择几何类型，决定是否加入封口、区域创建/更新任务；可选将流体-流体 wall 转 internal（名称含 wall 的 named selection 排除，baffle 保持 wall）。如需重叠非保形接口，使用 non-conformal；其余情形即便无需共享也优先用 Share Topology。非保形方案限制流体区域抽取等能力（pp. 330–332）。
- **Share Topology（3.9）**：最大 gap distance 应不超过表面网格 Minimum Size 的一半，且不能大于实体厚度；过低可能漏标 gap，过高可能使几何坍塌。Join-Intersect 适合常规连接/相交；Interface Connect 可用于重叠面边连接，建议配合 Ignore Proximity Across Objects，并在 CAD 侧 imprint。锐角面应先用圆角处理。若 Discovery Force Share 产生 Connect Topology labels，后续不要删除或改名（pp. 332–338）。
- **Capping 与 Regions（3.10–3.12）**：为开口建立指定边界类型的 cap；环形开口需用单个 named selection 同时标记内外面，倾斜环形开口不支持直接 cap。Create Regions 估算流体区数，仍需检查检测结果；名字匹配 `*fluid*`、`*enclosure*`、`air*`，或连接到 inlet/outlet/internal 的 region 可被识别为流体。Update Regions 可将区设为 fluid/solid/porous/dead；porous 类型仅 UTL 支持，dead/void 不会传到 solver（pp. 338–343）。

## 3.13–3.17 薄体、边界层与体网格（PDF pp. 343–370）

- **Thin Volume Meshing（3.13）**：适用于厚度/底边比小于 5 的薄结构；须置于 Add Boundary Layers 前，不兼容周期边界，加入后全部 regions 串行网格。源/目标面网格尺寸建议为薄区厚度的 1–2 倍；常见 gap 至少保证每 gap 一个单元。可按 source-target、平行面或 stacked plates 自动生成薄区控制；stacked plates 可按层数或尺寸设定，Auto Control Creation 可按 max gap 自动检测，但符合堆叠板场景时专用 Stacked Plates 通常减少阶梯化（pp. 343–352）。
- **Boundary Layers（3.14）**：可选 aspect-ratio、uniform、smooth-transition、last-ratio 等偏置方法，配置首层/增长率/层数并按流体区、固体区、命名 region、zone 或 label 指派。棱角可忽略边界层并设置 buffer layers。无效法向可用球体/局部重划或平滑修复；大规模无效法向修复会增加网格数量。读取 `.pzmcontrol` 后不支持部分 advanced options，且文件控制与界面控制冲突不会自动检查（pp. 352–357）。
- **Multizone（3.15–3.16）**：通过 source-target 面沿扫掠方向生成六面体或主导六面体网格；可选 Standard/Thin technique、Hex-Pave/Hex-Map/Prism/Mixed 填充，以及基于区/边的尺寸控制。需要按角度分区；极薄板可关闭表面质量改进或在 multizone 控制后单独改进表面；圆柱扭曲可尝试拆分圆柱。connected regions 要匹配 sweep 设置；预览和实际网格可能因简化算法不同而略有差异。多区边界层不如非结构网格灵活，建议先无边界层验证，再从 uniform 开始（pp. 357–364）。
- **Generate Volume Mesh（3.17）**：提供 tetrahedral、hexcore、polyhedra、poly-hexcore；可选择流体/固体区域、全局或 region-based sizing、并行及边界层/薄体全局参数。surface local sizing 作用于边界和内部，region maximum cell length 只控制区域内部，不应混为同一尺寸控制。poly-hexcore 可配合尺寸场；填充固体多面体、固体增长率等选项受非保形设置与 region 组合限制。生成后工作流默认报告 Orthogonal Quality（pp. 364–370）。

## 3.18–3.28 网格后处理和高级工作流操作（PDF pp. 371–408）

- **Update Boundaries（3.18）**：按 zone 或 label 查看、改名和重分边界类型；默认列表只显示外部 wall，切换 List All 会丢弃未提交修改。若在 Extrude/Transform 后更新，应手动核对 internal 与 external 类型，避免误赋（pp. 371–372）。
- **Improve Surface Mesh / Add Boundary Type（3.19–3.20）**：表面改进可选 Orthogonal、Enhanced Orthogonal 或 Skewness 质量度量，设置面质量、迭代、角度和去台阶参数；过度提高限制可能导致激进改动。步骤伪影仅在 step 与邻面属于同一 zone/label 时移除；加 label 或分区可保护台阶。Add Boundary Type 可创建新边界并选择 zone，按需合并（pp. 372–375）。
- **Improve Volume Mesh（3.21）**：沿用 Orthogonal/Enhanced Orthogonal/Skewness 等质量度量，可设 cell quality limit、附加质量指标及是否在残余坏单元附近忽略几何特征（pp. 375–376）。
- **Transform / Extrude（3.22–3.23）**：变换支持平移/旋转、复制数量、周期性自动参数和 zone 合并/重命名；自动利用周期参数时不适用于多组周期区。体网格拉伸要求面/区选择满足共面等约束；周期/shadow 面不能直接拉伸，会提示并转为 wall。可设层数、首层/总高度、增长率、增长模式和最大层高；圆柱面拉伸过高可能产生无效网格，应降低高度重试（pp. 376–382）。
- **Linear Mesh Patterns（3.24）**：用于重复 CAD 单元（如电池）。配置轴、pitch、总单元数和自定义命名/脚本规则；一般放在表面网格之后、Describe Geometry 之前，若对象会在表面网格后合并，则需提前插入。pattern 单元要共享拓扑才能连通，已被 pattern 使用的对象不能再次用于另一 pattern。脚本支持单/双命名模式、regular/explicit/flip 规则，按最近一次复制连续派生（pp. 383–393）。
- **Manage Zones（3.25）**：体网格前可按角度拆区、拆圆柱、按全局方向切分非圆柱体、提取边；体网格后可筛选/重命名/拆分/合并 cell 与 face zones、修改前后缀、合并 body labels。body 与 label 不应同名；共享 body label 内可同名，但不同 label 之间需唯一。若导入设置 Separate Zone By=face，前置 zone 管理不可用（pp. 393–398）。
- **Modify Mesh Refinement / Create Local Refinement Regions（3.26–3.27）**：局部重划可 Add 或 Add & Remesh，提供目标尺寸与特征角；不建议用它局部粗化曲面，粗化回到 Add Local Sizing。局部加密区可由 box、cylinder 或 offset surface 建立；offset surface 可沿流向生成尾迹扩展层，控制 defeaturing、总厚度、层数、wake/cross-wake growth；几何对象是构造加密区域的参照，需在工作流图形中核实区域范围（pp. 398–406）。
- **Run Custom Journal（3.28）**：可在工作流中插入已有 Meshing journal 命令，任务可重复添加但不能作为自定义工作流首任务；使用者需理解 Meshing 模式脚本与可用命令（pp. 406–408）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Chapter 3，PDF pp. 301–408。
- p. 321 的 Auto Assign Zone Types 表在文本提取中单元格错位（intake/exhaust fan 两行）；已用 [[Fluent 引导式网格工作流]] 2.1 节（p. 286）的同源映射表交叉核对语义，两表差异（fan 变体模式、interface、仅外边界生效）按原文录入，若逐字用于脚本请回查原页。
- Figures 3.1–3.5 为图形元素，仅其文字说明被摄取。印刷页码引用（p. 332、361、372、612、615、623）指向未摄取页段，仅作定位。
- 各默认值（Separation Angle 40°、Curvature Normal Angle 18°、Cells Per Gap 最小 0.01、Collapse 120° 等）对应 2026 R1，随版本可能变化。
- 限制清单为手册"known issues"转录的中文转述，条目均附任务上下文；实际排障请回查 pp. 302–306 原文。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 引导式网格工作流]]（工作流框架、通配符 journal 语义、任务机制）
- [[Fluent 网格模式入门]]（GUI/树结构基础）
- [[Fluent 网格模式文件读写与导入]]（.pmdb/.dsco/.stl 导入规则的基础）
- [[Fluent 2026 R1 已知限制]]（.dsco 许可证、旧 journal/wft、BoI 相关条目）
- [[Fluent 网格质量诊断]]（skewness 等指标定义）
- [[index]]
