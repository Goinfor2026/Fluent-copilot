---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - meshing
  - mesh-import
  - fe2ram
  - third-party
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 第三方网格导入与 fe2ram 过滤器

## 摘要

User's Guide 2026 R1 Part II 附录 A（PDF pp. 869–876）说明边界/体网格的外部来源：GAMBIT、ICEM CFD TetraMesher（RAMPANT 文件）以及第三方 CAD/CAE 包（经 File → Import 或独立 `fe2ram` 转换器）。核心事实：体网格生成要求以三角形/四边形单元集合定义计算域边界；**经这些途径导入的所有边界 zone 一律按 wall 处理**，须在 meshing 或 solution mode 中重新指定类型。

## 前提与内部来源（PDF p. 869）

- 体网格生成方案要求一组定义计算域边界的三角形和/或四边形单元。
- **A.1 GAMBIT**：可创建表面与体网格（细节见 GAMBIT Modeling Guide，不在本手册内）。
- **A.2 TetraMesher（ICEM CFD Engineering）**：TetraMesher 用递归细分八叉树方案生成四面体体网格，ICEM CFD 从其写出 **RAMPANT 文件**；读取途径：File → Read → Mesh 或 `file/read-mesh`。

## A.3 第三方 CAD/CAE 包（PDF pp. 869–871）

两条途径：File → Import 菜单项，或先用独立 **`fe2ram` 过滤器**把有限元包文件转成 Fluent 网格格式——支持 ANSYS、I-deas、NASTRAN、PATRAN 的表面/体网格与 **VRML 1.0** 文件；ARIES 只能先另存为 ANSYS Prep7 再转。

手工转换命令：

```
utility fe2ram [dimension] read-format [merge] [zoning] [write-format] input-file output-file
```

- `dimension`：3D 为默认（省略）；2D 网格 `-d2`；表面网格 `-surface`。
- `read-format`：`-tANSYS` / `-tIDEAS` / `-tNASTRAN` / `-tPATRAN`；其他包的转换能力列表用 `utility fe2ram -cl -help`。
- `merge`：网格合并容差，默认 1e-6；`-mTOLERANCE` 自定义、`-m` 恢复默认。
- `zoning`：zone 识别方式——按 group（默认，省略）、按 property ID 用 `-zID`、忽略全部分组用 `-zNONE`。
- `write-format`：默认写 Fluent 网格；`-oFIDAP7` 写 FIDAP 格式。
- **输出文件不能是 CFF（`.msh.h5`）**。
- 手册示例（2D I-deas 体网格文件转 Fluent 网格）：`utility fe2ram -d2 -tIDEAS sample.unv sample.msh`
- 产物在 meshing mode 经 File → Import 读入；体网格产物也可直接在 solution mode 读入。
- **重要**：所有边界类型都被视为 wall zone；appropriate 类型须在 meshing/solution mode 中设置。

## A.3.1 I-deas Universal 文件（PDF pp. 871–872）

- 表面网格：读已被 I-deas 分组为 zone 的三角/四边形边界单元；体网格：读边界节点或 2D 边界单元已适当分组的 2D/3D 网格。**节点与边界单元不得混在同一 group**。
- 识别的 Universal dataset：节点坐标 15、781、2411；单元 780 或 2412；Permanent Groups 752、2417、2429、2430、2432、2435。
- **单元须用线性单元**（Fluent 使用线性单元）：数据集中的抛物线单元其中间边节点被忽略——该假设仅在单元边近似直线时成立，高曲率区域抛物线单元与线性差异大时可能产生错误拓扑。
- 体网格注意：**mesh area/mesh volume dataset 不被识别**——把多个 mesh area/mesh volume 写入同一 Universal 文件可能使 fe2ram 或 Fluent 混乱。
- 分组方式：表面网格用 Group 命令把面分组（同组面输出为单一 zone；可按 mesh area 自动生成组——zone 多但事后可合并——或手工把多个 mesh area 归一组）；体网格按节点分组（同组节点成一 zone；**内部面的节点不得与边界面的节点同组**）。
- 周期边界：在 I-deas 中一般难以生成有效周期网格；手册指引改用 Fluent meshing mode 的专用功能（Creating Periodic Boundaries，印刷页码 p. 728，属已摄取的 Chapter 7 范围，见 [[Fluent 高级网格主题]]）。
- 重复节点：I-deas 创建三角形时常产生重复节点，必须移除——用 I-deas 的 remove coincident node 命令，或 Fluent 的 Merge Boundary Nodes 对话框 Merge 按钮 / `/boundary/merge-duplicates` 文本命令；合并过程在 meshing mode 通常更快，在 I-deas 更直观。

## A.3.2 PATRAN Neutral 文件（PDF pp. 872–873）

- 表面网格：读按 named component 分组或以 property ID 标识的线性三角/四边形边界单元；体网格：读边界节点按 named component 分组的 2D/3D 网格；全部边界 zone 视为 wall。
- 识别的 Neutral 数据集（Packet Type）：节点数据 01、单元数据 02、分布载荷 06、节点温度 10、Name Components 21、文件头 25。
- 分组：named component 应用于节点形成面组（=zone）；**2D 体网格额外要求所有单元位于 Z=0 平面**。
- 周期边界：同 I-deas 的处理指引（p. 728）。

## A.3.3 ANSYS 文件（PDF pp. 873–874）

- 表面/体网格：读在 ANSYS 中用节点+单元选择分组的线性三角/四边形边界单元、边界节点分组体网格；全部边界 zone 视为 wall。
- 识别的数据块：NBLOCK（节点块）、EBLOCK（单元块）、CMBLOCK（单元/节点分组）。
- **单元必须是 STIF63 线性壳单元**；单元数据若无显式单元 ID，过滤器按顺序编号创建 zone。
- 周期边界：同一指引（p. 728）。

## A.3.4 ARIES 文件（PDF p. 874）

ARIES 自带过滤器，或在 ARIES 中写出 Prep7 文件后按 ANSYS 文件用 fe2ram（`-tANSYS`）处理；Prep7 可经 ARIES 或 Fluent 任一过滤器转换。写出 Prep7 须满足：

1. 在 Geom 模块为 part 命名；
2. 在 Material 模块创建或从 mat_lib 读取材料（创建须提供密度、泊松比、弹性模量）；
3. 在 Environment 模块为表面生成面压力（写 Prep7 时传递给各单元）；
4. 在 Environment 模块生成至少一个约束（restraint）；
5. 单元类型设为 STIF63（三角形壳单元）并给定非零厚度；
6. 写 Prep7 时让其自动把压力赋给单元。

## A.3.5 NASTRAN 文件（PDF pp. 874–875）

- 表面网格：读定义域边界的线性三角/四边形单元；体网格：读 2D/3D 网格；全部边界 zone 视为 wall。
- 识别的 Bulk Data 条目：GRID（单精度节点坐标）、GRID*（双精度）、CBAR（线单元）、CTETRA/CTRIA3（四面体/三角形）、CHEXA/CQUAD4/CPENTA（六面体/四边形/楔形）。
- 线性单元要求与抛物线中间节点忽略的告诫同 I-deas。
- 周期边界：同一指引（p. 728）。
- 重复节点：NASTRAN 创建三角形时也常产生重复节点，须用 Merge Boundary Nodes 对话框或 `/boundary/merge-duplicates` 合并。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Appendix A，PDF pp. 869–876；p. 876 为版权页脚，无正文；本附录条目（A.1–A.3.5.3）至此全部完成。
- 本批文本提取无表格错位或乱序（数据集/条目均为无歧义的成对列举），未做额外视觉核对；命令与选项照录原文。
- 内容偏 legacy：GAMBIT/TetraMesher/ARIES/PATRAN/I-deas 等工具本身已过时，fe2ram 相关说明是手册明确陈述的现行为；第三方包支持版本另见 [[Fluent 程序架构与能力]] 的 Table 1.2（2026 R1）。
- 印刷页码 p. 728（Creating Periodic Boundaries）已核对落在 Chapter 7 范围（pp. 605–868）内，内容归 [[Fluent 高级网格主题]]。
- "所有边界视为 wall""输出不能为 CFF""STIF63 限制"等为跨格式共性，实际使用时须在目标环境验证。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 网格模式文件读写与导入]]（正文侧的 Import/Read 操作，1.6.9 曾指向本附录）
- [[Fluent 程序架构与能力]]（第三方软件支持版本表）
- [[Fluent 高级网格主题]]（周期边界创建功能所在章）
- [[index]]
