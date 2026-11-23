---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - mesh-adaption
  - puma
  - hanging-node
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 网格自适应

## 摘要

User's Guide 2026 R1 Part III / Chapter 39 "Adapting the Mesh"（PDF pp. 3975–4014，四节）。**本页全章完成（批次 108，pp. 3975–4014）**：解算自适应网格——使用准则与指南、细化/粗化设置（Manual/Automatic 两个对话框、PUMA/悬挂节点/2.5D PUMA 三方法、Prismatic 各向异性拆分、General Adaption Controls 全参数、skip-until）、五组预定义判据（边界层/空气动力学 Hessian 族/燃烧/VOF/Overset）、四类自适应示例（边界/区域/场变量/表达式）、悬挂节点法的几何重建自适应。理论见 Theory Guide "Adaption Process"。

## 39.1 使用自适应（pp. 3975–3979）

- 非结构网格两大优势：建网时间短 + **解算自适应加密**——在需要处加单元、不浪费算力；并行时自适应后**默认自动执行负载均衡**（p. 4548/4562）。
- **39.7.1 示例（叶栅）**五步流程：显示压力等值线定加密阈值 → Field Variable 标记加密 register → 用马赫数梯度重复 → 尾迹区用总压等值线（边界层与尾迹同被标记）→ 细化 register 内单元。
- **39.1.2 指南**：
  - **表面网格必须足够细以表达几何重要特征**——自适应新增节点不会改变初始网格的面片（高曲率翼面不能靠后补节点）。
  - 初始网格应包含足够单元捕捉流场本质特征（钝体激波例：先有合理初解，再用梯度自适应锐化激波、达成网格无关）。
  - **多面体单元只能用默认 PUMA 方法自适应**。
  - **悬挂节点法 + 多面体**：全域转换成多面体（p. 1299）→ 整个网格不可自适应（即使转换后含六面体）；斜四面体转换（p. 1304）或悬挂节点/边邻单元转换（p. 1305）产生的多面体 → 非多面体单元可自适应，多面体单元在启动自适应时自动从 register 剔除、保持不变。
  - **自适应前获得合理收敛的解**（错误解会在错误区域加单元；权衡过早/过晚；自动自适应不适用此条——按迭代/时间步规律执行）。
  - **手动自适应前写 case+data 文件**（网格不满意可回档；自动自适应不适用）。
  - **梯度自适应选对变量**：激波用压力梯度；不可压流动压力梯度无意义——用平均速度梯度；湍流剪切流解析 k 与 ε 梯度；反应流用温度或反应组分浓度（摩尔/质量分数）。
  - **勿过度加密局部**——单元体积梯度巨大会损害解精度。

## 39.2 细化与粗化（pp. 3979–4003）

依据 cell registers、命名表达式或表达式，经 **Manual**（Domain → Adapt → Manual...）或 **Automatic**（Domain → Adapt → Automatic...）网格自适应对话框设置；overset 见 p. 1263。设置十四步：
1. **方法三选**：2D/3D 可选默认 **PUMA**（polyhedral unstructured mesh adaption）或 **hanging node**；仅 3D 另有 **2.5D PUMA**（单单元厚网格）。**2D 且体积分数空间离散选 Geo-Reconstruct 时（VOF 或 Eulerian Multi-Fluid VOF）PUMA 不可用**。换方法：`mesh/adapt/set/method`。
2. 打开 Manual 或 Automatic 对话框。
3. 自动自适应：输入 Name + **Frequency**（两次相邻自适应间隔的迭代/时间步数）。
4. （可选）**Predefined Criteria** 下拉快速设置（可单独或与其他步骤组合）。
5. （可选）经 Cell Registers 下拉建单元 register。
6. 设 **Refinement Criterion**（既有 register/命名表达式/表达式）。
7. 设 **Coarsening Criterion**（同上）。
8. （可选）**Prismatic Adaption**——各向异性拆分（只沿特定方向；典型配边界层网格：boundary layer 预定义判据、边界 register 或 Yplus/Ystar register）。限制：**必须 PUMA**；仅边界相邻层内的棱柱类单元（六面体，或顶底面节点数相同的楔形/多面体）各向异性细化，其余单元各向同性。TUI：手动 `mesh/adapt/set/prismatic-adaption?`、自动 `mesh/adapt/manage-criteria/add` 的 prismatic? 设置。**全局附加设置**：各向异性拆分默认对半（split ratio 0.5，General Adaption Controls 可改）；拆分方向默认垂直于相邻边界区——可用 `mesh/adapt/set/prismatic-boundary-zones` 指定边界区以减少方向数。
9. **General Adaption Controls**（作用于所有判据）：
   - **Maximum Refinement Level**（细化层级数；0 = 不限；**默认 2**，多数问题良好起点；过大迅速爆炸单元数）。
   - **Maximum Cell Count**（总单元数近似上限，Fluent 据此停止标记；0 = 不限；**仅 PUMA**）。
   - **Minimum Edge Length**（3D 体积小于其立方 / 2D 面积小于其平方的单元不细化；默认 0 不限）。
   - **Show Advanced Controls**：瞬态的 **Additional Refinement Layers**（自动自适应可额外细化的层数；受 Max Level 与 Min Edge Length 约束；全局设置，单判据用 `mesh/adapt/manage-criteria/edit` 定制）；**Prismatic Split Ratio**（默认 0.5，控制相对边界区的拆分位置）；**Minimum Cell Orthogonal Quality**（自适应结果单元力求保持的最小正交质量——不保证、保证会拖慢求解；**2D 与悬挂节点法不可用**）；**Zones 列表**（多单元区时可限制自适应区——默认全部）；**几何重建自适应**（PUMA）：先定义辅助几何（p. 1855）→ 勾 Reconstruct Geometry → Manage... 打开 Manage Geometry-Based Adaption 对话框——选 Wall Zone + Auxiliary Geometry Definition → Add（**壁面既有节点须已符合该辅助几何**）；可 Edit/Delete；一区至多配一几何、一几何可配多区；默认只有壁面表面节点随几何移动——让位移向邻近棱柱边界层传播：`mesh/adapt/geometry/manage/edit` 给指数正值（越小传播越远、0 = 关闭；**建议从 0.01 起调**）；悬挂节点法做几何自适应须用 Geometry Based Adaption 对话框（见 39.4）。
   - OK 关闭。
10. （可选）**List Criteria**——控制台打印被标记细化/粗化的单元数。
11. （可选）**Display Options**——定制标记单元的显示。
12. （可选）**Display**——查看标记单元。
13. **手动**：点 **Adapt** 执行；随时可 **Copy to Automatic Adaption** 把设置复制到自动对话框。
14. **自动**：OK 保存判据 → 按需再建多条 → （可选）**skip-until**——`mesh/adapt/manage-criteria/edit` → 输判据名 → `skip-until` + 正整数（默认 1 = 首步即自适应；按控制台打印的迭代计数，重启不重置：skip-until 40 + 频率 20 = 第 1、20 步跳过、第 40 步开始）；三个 Hessian 判据自动设 skip-until=2（首步无有用结果）→ Manage Adaption Criteria 对话框（Domain → Adapt → Manage...）检查/编辑/停用/激活/删除 → 运行计算即按间隔自动执行。

### 39.2.1 预定义判据（pp. 3986–4003）

两个对话框均有 Predefined Criteria 下拉——选中后自动生成所需 register/命名表达式与设置；可能需补强制设置（如 Minimum Cell Length Scale）。

- **39.2.1.1 边界层（按单元距离）**：Adaption Criteria Settings 选 **Boundary Zones + Cell Layers to Split**；PUMA 下默认启用 Prismatic Adaption（沿所选区垂直方向各向异性拆分；split ratio 可调）；生成 register **`boundary_cell_distance`** 自动填入 Refinement Criterion——Boundary Register 对话框可复核并可**切换 Cell Distance → Volume Distance 方法**；Manual 对话框点 Adapt。
- **39.2.1.2 空气动力学**：五选——
  - **Shock Indicator + Density-based**：按密度梯度适配激波；密度基求解器恒可用，压力基仅当材料密度为 real/ideal-gas。
  - **Error-based + Pressure Hessian Indicator**：压力分布 Hessian（二阶导矩阵）误差指示——多尺度多现象（同时捕捉不同强度的激波与尾迹、拉伸棱柱层的各向异性误差）；**不推荐很光滑的解**（目标区过宽、过度加密）。
  - **Error-based + Mach Hessian Indicator**：马赫数 Hessian——马赫数范围更宽、单标量输入；**仅 ideal/real gas 密度可用**。
  - **Error-based + Combined Hessian Indicator**：多场（压力/温度/速度/密度/湍流量各自适用时）Hessian——全马赫范围、多尺度通用。
  - **Error-based + Goal-Based Error Indicator**：伴随 observable——需先定义 observable（p. 4709）、初始化并计算伴随解、显示 **Goal based error indicator (Raw)** 场（Sensitivities... 类别；高值区细化收益大、低值区可粗化）；打开 Adaption Criteria Settings 定制；**建议为 observable 与单元数建监视器**观察变化。
  - 自动自适应默认频率：Density-based **2 步/20 迭代**；Pressure Hessian **20/20**；Mach Hessian **100/100**；Combined Hessian **100/100**；Goal-Based **100 步/20 迭代**（可调——为避免区域振荡式加密/粗化可让步间更收敛；Hessian 类比梯度 register 需更长频率——对小幅波动敏感、否则做无谓自适应）。生成 register（如 `gradient_density_refinement`；Mach/Combined Hessian 用 **Hessian derivative** 选项——改动设置可能使既有指示器失效需重生成）；Pressure Hessian Indicator 场变量（Derivatives... 类别）可后处理（**按全局平均缩放的相对值**）。
- **39.2.1.3 燃烧**：前提——启用燃烧模型 + 能量方程。Predefined Criteria → Combustion... → **Flame Indicator**：沿推进火焰前沿细化（温度/涡量/组分/DPM 浓度，视模型）；Adaption Criteria Settings——**Include Vortex Indicator**（默认开——涡量模计入判据）；**Spark Region Refinement**（仿真开始时细化临时球形火花区、指定时间后粗化回原网格——Time 最长时长、Centroid X/Y/Z、Radius）；自动频率默认 2；其余设置经 General Adaption Controls 复核；生成命名表达式（如 `flame_refinement_1`）与 register（如 `temperature_refinement`）。**告诫**：表达式内最小边长小于体积立方根、或表达式内最大细化层级小于全局设置时，判据与全局限制作用不一致——高梯度区单元分布不均（VOF 类尤其不宜）；**不组合判据时最好把单元体积与细化层级从表达式中移除，只让全局设置限层**。
- **39.2.1.4 VOF**：Multiphase... 三选——**Volume of Fluid**（标准 VOF）、**VOF-to-DPM [Generic]**（VOF-to-DPM 转换机制；较直白的 register 判据）、**VOF-to-DPM [Advanced]**（转换机制；复杂表达式 + 需自定义参数）；基于二次相体积分数生成 register/表达式；自动频率默认 2；同名告诫同上（`vof_refinement_1`、`gradient_vof_refinement`）。
- **39.2.1.5 Overset**：目标——消除 orphan 单元、缩小 donor-receptor 尺寸失配、按需加密间隙（防 orphan 生成）；受益者多为动网格/动态网格算例。**与其他预定义判据不同：不用 cell registers**——overset 专属工具一步完成界面分析与标记自适应；默认合适的 2D/3D 棱柱单元**各向异性**细化以省单元。设置：Automatic 对话框 → Overset → Orphan Adaption（消 orphan）/ **Size Adaption**（Maximum Length Scale Ratio 阈值默认 **3**）/ **Gap Adaption**（目标最小 Gap Resolution 默认 **4**）/ **Coarsening**（不再需要加密时粗化）→ OK；更多自动 overset 自适应设置在 `define/overset-interfaces/adapt/set` 命令菜单（p. 1266）。

## 39.3 自适应示例（pp. 4003–4012）

- **39.3.1 边界 register**：boundary adaption 在所选边界区附近标记/细化——**不能提高曲面的几何分辨率**（曲面形状重要时必须一开始就给足表面节点）。
- **39.3.2 区域 register**：翼型分离——鼠标探针选圆形区域标记翼唇/尾迹区后细化。
- **39.3.3 场变量 register**：CFD 尚无完整严格的误差估计理论——**假设最大误差在高梯度区**，用流场物理特征驱动自适应。**Scaling Option 首选值**：Cells More Than 0.3–0.5、Cells Less Than 0.7–0.9（更小的值 → 更大的自适应区）。**Scale by Global Maximum**：φ、∇φ 或 ∇²φ 按全域最大值缩放（Eq 39.1），恒得与问题无关的 [0, 1] 区间——粗化阈值首选 0.2–0.4、细化阈值 0.5–0.9（更小 → 更大区域）。用导数+缩放选项建细化 register（Cells More Than 型）与粗化 register（Cells Less Than 型），在 Manual/Automatic 对话框组合。
- **39.3.4 表达式自适应**：表达式可配可不配 register 定义细化/粗化判据。组合布尔示例（照录）：`AND(OR(StaticPressure<0.5[Pa], CellRefineLevel<3), CellVolume>1e-06[m^3])`；与 register 组合：`AND(Pressure<p0 [Pa], near_outlet_cells)`（p0 为常实数、near_outlet_cells 为边界 register）。

## 39.4 悬挂节点法的几何重建自适应（pp. 4012–4014）

流程：①TUI `mesh/adapt/set/method` → **hanging-node**；②打开 Domain → Adapt → More → **Geometry...** → Geometry Based Adaption 对话框：勾 **Reconstruct Geometry**；（可选）**Surface Meshes...** 读入细表面网格作几何（Select File 时注意单位）；③Wall Zones 选区 → **Set...** 打开 Geometry Based Adaption Controls 对话框设置（节止于 p. 4014 图示处，全章完）。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3975–4014（批次 108，2026-10-20，pypdf layout 模式提取）。
- Theory Guide Eq 39.1（全局最大缩放）公式体未提取，按语义记录；39.4 的 Geometry Based Adaption Controls 对话框内容止于 p. 4014 图示（章尾）。
- Figures 39.1–39.38（网格图与对话框截图）为图形元素未摄取；预定义判据默认频率表、skip-until 行为、表达式示例照录。
- 版本敏感：PUMA 默认与限制（2D+Geo-Reconstruct 不可用）、预定义判据默认频率、Overset 阈值 3/4、skip-until=2 以 2026 R1 为准。
- 相关页面：[[Fluent 求解器使用]]（瞬态自动自适应联动）、[[Fluent 网格读取与操作]]（多面体转换）、[[Fluent GPU 求解器]]（poor mesh removal 对照）。
