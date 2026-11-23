---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - meshing
  - file-format
  - legacy-msh
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 网格文件格式（legacy .msh）

## 摘要

User's Guide 2026 R1 Part II 附录 B（PDF pp. 877–892）定义 Fluent 网格文件的节（section）结构——即 legacy `.msh`/`.cas` 文本与二进制格式。核心规则：文件由带类型索引的括号节组成；网格节索引为十进制类型码（节点 10、边 11、单元 12、面 13 等），二进制时加前缀 20（单精度）/30（双精度）；网格节内索引与计数用**十六进制**，而非网格 Zone 节（39/45）的 zone-id 用**十进制**。本附录是解析或生成 legacy 网格文件（含自动化脚本）的权威依据。

## 总则（B.1–B.2，PDF pp. 877–878）

- 网格文件是 case 文件的子集（只含网格相关节）；case 节全集见手册 Part III 引用（Grid Sections 印刷页码 p. 5920；Non-Grid Legacy Case Sections p. 5932）。
- 文件由若干**节**组成：每节括号包裹，以一个十进制整数开头标明节类型（formatted 与 binary 的索引含义不同）；所有条目组用括号包裹，便于跳转解析与向前兼容；条目列表的头部信息在独立的括号组里、位于条目之前。
- **二进制约定**：节头索引前加 20（单精度二进制）或 30（双精度二进制），如 2010/3010；二进制数据以字面文本 `End of Binary Section 2010`（或 3010）结尾、位于节收尾参数之前。手册示例：`(3010 (2 1 2aad 2 3)(…binary…) End of Binary Section 3010)`。
- 各节的符号名可作为 Scheme 符号（`xfile.scm`，向 Ansys 索取）或 C 头文件宏（安装目录内 `xfile.h`）使用。

## 网格节（B.3，PDF pp. 878–887）

格式均写作 `(索引 (zone-id first-index last-index type [element-type])(体))`；`zone-id=0` 的节是**声明节**（计数、无体或特殊），非零为常规节。

- **Comment（0，XF_COMMENT，可选）**：`(0 "comment text")`，可出现在文件任何位置（其他节内部除外）；建议在每个长节或相关节组前加注释说明。
- **Header（1，XF_HEADER，可选）**：`(1 "程序名与版本")`，标识写出程序；可多次出现，构成文件的处理历史。
- **Dimensions（2，XF_DIMENSION，可选）**：`(2 ND)`，ND 为 2 或 3，用于校验网格维度。
- **Nodes（10，XF_NODE，必需）**：`(10 (zone-id first-index last-index type ND)(x y [z] …))`。声明节（zone-id=0）：给出节点总数，无坐标体。常规节：索引为十六进制，各节 last-index ≤ 声明总数；节点类型 type：0 = virtual（忽略不读写）、1 = 无类型、2 = 边界节点；ND 可选（2D 时每行只有 x y）。索引用十六进制以节省空间并加快 I/O。
- **Periodic Shadow Faces（18，XF_PERIODIC_FACE，仅周期网格需要）**：`(18 (first-index last-index periodic-zone shadow-zone)(f00 f01 …))`；f\* 为周期面对的面索引（十六进制，指向全局面列表的偏移）；**注意 first/last-index 是"周期对列表"的序号，不是面索引**。
- **Cells（12，XF_CELL，必需）**：`(12 (zone-id first-index last-index type element-type))`。声明节给出总单元数；**last-index=0 表示网格无单元**（纯表面网格文件，用于提醒求解器不可用）。声明节必须位于所有常规单元节之前。常规节无体，type 标识单元区类型：1 = fluid、17 = solid、0 = dead zone（solution mode 读取时跳过）。element-type：0 mixed、1 triangular、2 tetrahedral、3 quadrilateral、4 hexahedral、5 pyramid、6 wedge、7 polyhedral（面/点数 NF/NN 随具体多面体变化）；mixed 型需要体逐单元列出 element-type。Note：纯表面网格文件在 meshing mode 不需要 Cells 节。
- **Faces（13，XF_FACE，必需）**：`(13 (zone-id first-index last-index bc-type face-type))`。声明节给出总面数。常规节每行一个面：`n0 n1 n2 c0 c1`（n = 顶点，c = 相邻单元；节点数随 face-type）。**单元索引顺序按右手法则**：按节点顺序弯曲右手，拇指指向 c0。mixed（0）或 polygonal（5）面区每行以节点数开头：`x n0 n1 … nf c0 c1`。单侧有单元时 c0/c1 之一为 0；纯边界网格文件两者皆为 0。
  - **bc-type 表**：interior 2；wall 3；pressure-inlet/inlet-vent/intake-fan 4；pressure-outlet/exhaust-fan/outlet-vent 5；symmetry 7；periodic-shadow 8；pressure-far-field 9；velocity-inlet 10；periodic 12；fan/porous-jump/radiator 14；mass-flow-inlet 20；interface 24；parent（hanging-node 悬挂节点父面）31；outflow 36；axis 37。**非一致网格相交面放入单独 face zone，bc-type 加 1000**（如 1003 = wall）。
  - **face-type 表**：0 mixed；2 linear（2 节点）；3 triangular（3）；4 quadrilateral（4）；5 polygonal（NN 不定）。
- **Edges（11，XF_EDGE，可选）**：`(11 (zone-id first-index last-index type element-type))`；element-type 完全忽略。体每行 `v0 v1`。type：5 = boundary edge、6 = interior edge。Note：**case 文件中会省略 Edges 节**。
- **Face Tree（59，XF_FACE_TREE，仅 hanging-node 自适应网格）**：`(59 (face-id0 face-id1 parent-zone-id child-zone-id)((number-of-kids kid-id-0 …)))`，记录父面到子面的层级；十六进制；**可在 meshing mode 读取**。
- **Cell Tree（58，XF_CELL_TREE，仅 hanging-node 自适应网格）**：结构与 Face Tree 同；**不能在 meshing mode 读取**（与 1.6.2.1 的"hanging-node 自适应网格拒读"一致）。
- **Interface Face Parents（61，XF_FACE_PARENTS，仅非一致界面网格）**：`(61 (face-id0 face-id1)((parent-id-0 parent-id-1 …)))`，记录相交面（child）与原面（parent）的关系，每个 child 至少引用一个 parent。**在 solution mode 保存的非一致网格读入 meshing mode 时该节被跳过，非一致界面信息不被保留；切回 solution mode 需重建界面**——与 1.6.3.1 的 case 互转限制互相印证。

## 非网格节（B.4，PDF pp. 887–889）

包含边界条件、材料属性与求解控制设置。网格相关的是 **Zone 节（39 或 45，XF_RP_TV，必需）**：

- 通常网格引用的每个 zone 一个节；网格 zone 可以没有对应节，但每个 zone **至多一个** zone 节。
- 格式：`(39 (zone-id zone-type zone-name domain-id)((condition . value)…))`。网格生成器/前处理器只需给出头部与空条件表：`(39 (zone-id zone-type zone-name domain-id)())`——**收尾空括号必须写**，求解器按 zone-type 自行补充条件。
- **索引 45 只能用于不含边界条件的节**（仅有 zone-id/type/name/domain-id 四字段；45 节四字段之后的内容一律被忽略）；含边界条件必须用 39。meshing mode 可从 39 或 45 读取 zone 名与类型，但**只能写出 39**。
- **zone-id 为十进制**——与网格节的十六进制相反。
- zone-type 枚举：degassing、exhaust-fan、fan、fluid、geometry、inlet-vent、intake-fan、interface、interior、internal、mass-flow-inlet、outflow、outlet-vent、parent-face、porous-jump、pressure-far-field、pressure-inlet、pressure-outlet、radiator、solid、symmetry、velocity-inlet、wall、wrapper。
  - interior、fan、porous-jump、radiator 只能赋给域内面 zone（interior 用于 cell zone 内部的面，其余用于域内无限薄面上的 interior face）；wall 既可用于域内也可用于边界上的面 zone。
  - cell zone 只能是 fluid 或 solid；其余类型仅用于边界（face）zone。
- **zone-name 必须是合法 Scheme 符号**（写出时不带引号）：首字符须为小写字母或 special-initial，后续字符为小写字母、special-initial、数字或 special-subsequent；special-initial 为 `! $ % & * / : < = > ? ~ _ ^`，special-subsequent 为 `. + -`。（这与 1.6.9.1 CAD 导入的"非法字符替换为连字符"规则同源。）
- 手册给出的 meshing mode 产出示例：`(39 (1 fluid fuel 1)())`、`(39 (8 pressure-inlet pressure-inlet-8 2)())`、`(39 (2 wall wing-skin 3)())`、`(39 (3 symmetry mid-plane 1)())`。

## B.5 示例文件（PDF pp. 889–892）

三个 2D 四边形网格完整示例（概念同样适用于 3D；图 1–3 为图形元素）：

- **示例 1**：无周期边界、无悬挂节点的四边形网格——展示 Comment/Dimensions/声明节/常规 12、13、10 节的完整排布（含 interior=2、wall=3、interface=24 的用法）。
- **示例 2**：带周期边界——增加 18 节（周期面对配对）与 bc-type=8（periodic-shadow）面节。
- **示例 3**：带悬挂节点——含 58（Cell Tree）、59（Face Tree）节与 bc-type=31（parent）面节，演示自适应层级与父面记录。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Appendix B，PDF pp. 877–892；本附录条目（B.1–B.5）至此全部完成。示例代码块照录原文（十六进制索引、节排布），图 1–3 为图形元素未摄取。
- 本格式为 **legacy `.msh`/文本与二进制格式**；默认 CFF（`.msh.h5`，HDF5）的内部结构不在本附录范围（1.6.2 说明 CFF 为二进制 HDF5，需第三方工具探索）。
- Part III 引用（印刷页码 p. 5920、5932 的 case 节全集）未摄取，仅作定位。
- 索引编号、bc-type/element-type/face-type 表、zone-type 枚举与 Scheme 符号规则均为手册明确陈述，对应 2026 R1；解析器实现仍应以 `xfile.h`/`xfile.scm` 与实际文件为准。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 网格模式文件读写与导入]]（读/写操作、CFF 与 legacy 开关、`Check read data`）
- [[Fluent 第三方网格导入与 fe2ram 过滤器]]（fe2ram 产物即本格式，输出不得为 CFF）
- [[Fluent 引导式网格工作流]]（zone 命名规则同源的自动化上下文）
- [[index]]
