---
type: concept
created: 2026-10-17
updated: 2026-10-17
tags:
  - Ansys Fluent
  - mrf
  - srf
  - rotating-flow
  - solution-mode
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 运动参考系

## 摘要

User's Guide 2026 R1 Part III / Chapter 11 "Modeling Flows with Moving Reference Frames"（PDF pp. 1831–1849，共 3 节）讲运动参考系（MRF）建模。**本页已覆盖全章（批次 51）**：SRF 单参考系（壁面/周期边界要求、速度公式选择、求解策略）、MRF 多参考系（"冻结转子"近似、限制清单、网格两法、设置八步、后处理）。滑移网格见 [[Fluent 滑移与动网格]]（Ch.14）。

## 11.1 引言（p. 1831）

- 默认在静止（惯性）系解方程；运动件（叶片/叶轮）在静止系下使问题非定常——**运动参考系可在特定限制下把问题变成运动系下的稳态问题**。激活 MRF 后运动方程加入参考系变换的附加加速度项。帧速恒定时可稳态求解；**帧速非恒定会有附加项**（见 Theory Guide Relative Velocity Formulation）；**恒速运动系中也可跑非定常**（如旋转叶片自身的涡脱落——非定常来自流体失稳而非静止件干涉）。路线：全域单一运动系 → **SRF**；复杂几何 → 分区 + 界面 → **MRF**；静止/运动件非定常干涉重要 → **滑移网格**（Ch.14）。

## 11.2 单运动参考系 SRF（pp. 1833–1841）

- **壁面要求**（稳态 SRF 可行性的关键）：①随参考系运动的墙可任意形状（no-slip 定义在相对系——相对速度为零，如叶轮叶片面）；②旋转问题中**相对静止系不动的墙必须是绕旋转轴的旋转面**（no-slip 定义为绝对速度为零，如环绕螺旋桨的风洞壁）。**旋转周期边界**可用但表面须绕轴周期（单叶片叶排模型，图 11.3）。入口/出口多数可任选静止系或运动系给定（速度入口给相对或绝对速度）。
- **网格坐标约束**（11.2.1）：2D 旋转轴平行 z 轴；2D 轴对称旋转轴 = x 轴；3D 建网格时预定旋转区原点与转轴（常取 (0,0,0) 与 x/y/z 轴；也支持任意）。**静止系零速墙若非旋转面 → 必须用界面把旋转件包起来分多区**——稳态用 MRF、非定常干涉用滑移网格。
- **设置**（11.2.2）：① General 页选 **Velocity Formulation：Relative 或 Absolute**（密度基恒为绝对，此步无关）。② 逐 cell zone 给平移速度和/或角速度与转轴：Fluid/Solid 对话框 Reference Frame 页给 Rotation-Axis Origin/Direction；开 **Frame Motion**；给 Rotational Velocity 的 Speed 与/或 Translational Velocity 分量（常数或瞬态 profile/DEFINE_TRANSIENT_PROFILE；整体运动可用 DEFINE_ZONE_MOTION——**挂 UDF 后旋转轴原点/方向与速度不可再访问**）；**固体区不能与相邻固体区速度不同——那种情形用 Solid Motion**；**Note（CHT）**：固液一起运动的共轭传热无须给固体区开 Frame Motion；开它的场景是**内禀 FSI 要结构模型计入旋转力**（p. 3343）。③ MRF↔滑移网格切换用 Copy To Mesh Motion / Copy to Frame Motion（拷轴/原点/速度分量/DEFINE_ZONE_MOTION）——稳态 MRF 解作瞬态滑移初场（叶轮机械）。③ 墙速度给绝对或相对（相对邻区）：随系运动的墙给相对角速度 0、静止系静止的墙给绝对零——**改区速度时无需改墙条件**。④ 入口边界同 8.4（速度/总压/方向均可绝对或相对）。⑤ 压力基瞬态可开 `solve/set/advanced/transient-frame-motion-numerics`（时间步长无关的连续性离散，见求解策略）。⑥ 瞬态可用 **Moving Mesh Courant Number**（Velocity... 类）指导解。
- **速度公式选择**（11.2.2.1）：**选使大部分流域速度最小的参考系——减小数值扩散**。绝对公式适合域内大部分流体不动的场景（大房间里的风扇）；相对公式适合大部分流体随叶轮转动的场景（搅拌槽大叶轮）；两者之间任选。**Important：求解中途切换公式不会转换当前解——残差会大幅跳变；要换先重新初始化**；密度基恒绝对。入口/墙的速度/总压/方向给绝对或相对与公式选择无关（入口湍流量按换算到所选公式的速度处理）。压力出口静压与参考系无关；**回流时静压按总压用**——绝对公式按绝对系总压、相对公式按相对系总压；回流方向假定垂直出口（绝对/相对对应）。
- **求解策略**（11.2.3）：难点同轴对称旋流（10.3.4.2）——动量方程强耦合。手段：（压力基）切换速度公式；（压力基 segregated）**PRESTO!**；网格加密；（压力基 segregated）**速度欠松弛降到 0.3–0.5 或更低**；（压力基瞬态）`solve/set/advanced/transient-frame-motion-numerics`——**时间步长无关的连续性离散**；Note：**case 含动网格区或滑移网格区时该离散不生效**；强烈推荐用于钝体单相非定常尾流场景（如车轮用 frame motion 的汽车仿真）。低转速起步渐进升速（同 10.3.4.2.2：10% → 求解 → 存 → 倍增 → 重启循环）。
- **后处理**（11.2.4）：绝对与相对速度均可绘制/报告——所有速度参数有对应 Relative 版本（Relative Velocity Magnitude/Relative Mach Number）；总压/总温等含动压贡献的量也有 Relative 版本（Relative Total Pressure/Relative Total Temperature/**Rothalpy**）。矢量图默认绝对系；Vectors of 选 **Relative Velocity** 画相对矢量（建议 Color by 选 Relative Velocity Magnitude）。

## 11.3 多运动参考系 MRF（pp. 1842–1849）

- **两个方案**：**MRF（稳态近似）** 与 **SMM 滑移网格（本质非定常，Ch.14）**。多运动件或静止面非旋转面时必须分区+界面。
- **MRF 概念**（11.3.1.1）：各 cell zone 可赋不同旋转/平移速度；运动区用运动系方程、静止区退化为静止方程；**界面处做局部参考系变换**以计算相邻区边界的通量（Theory Guide MRF Interface Formulation）。**MRF 不考虑运动区相对相邻区的相对运动——网格固定**，相当于把运动件"冻结"在某位置看瞬时流场——故称 **"frozen rotor approach"**。适用：转子-静子干涉较弱、界面流动简单（搅拌槽叶轮-挡板干涉弱、无大尺度瞬态效应）；**另一用途：为瞬态滑移网格计算提供初场**（免去起动计算）；**强转子-静子干涉的瞬态必须用滑移网格**。
- **限制**（11.3.1.2）：
  - **界面取向**：界面法向的参考系速度分量必须为零——平移运动区的边界须平行于平移速度向量；旋转问题的界面必须是绕该流体区旋转轴的**旋转面**（示例中的虚线边界必须是圆形而非方形）。
  - **严格只对稳态有意义**——但 Fluent 允许 MRF 下解非定常（所有输运方程加瞬态项）；**须慎重评估是否有意义：非定常干涉用滑移网格通常更有意义**。瞬态压力基可开 `solve/set/advanced/transient-frame-motion-numerics`。
  - **DPM**：迹线/颗粒轨迹默认用相对 cell zone 参考系运动的速度；颗粒轨迹可在 DPM 对话框 Numerics 页勾 **Track in Absolute Frame**（或 `define/models/dpm/options/track-in-absolute-frame`）改绝对系。**Note：轨迹跨过不同参考系运动的界面时，坐标变换会造成颗粒速度突变**。入射速度的解释与跟踪一致（相对局部系或绝对坐标）。
  - **多参考系 + 相对速度公式不能准确模拟轴对称旋流**（当前实现未把 Theory Guide 式 2.16 的变换用于旋周速度导数）——**该情形用绝对速度公式**。
  - **平移与旋转速度视为常数（不允许时变 ω⃗、v⃗）**。
  - **相对速度公式不能与 MRF + mixture 多相模型联用**——用绝对公式。
  - **单一界面不得一部分是耦合双面墙、另一部分是普通耦合**——拆成两个界面（耦合界面 + 标准流-流界面，见 p. 1227）。
  - **Important：MRF → 滑移网格切换用 `mesh/modify-zones/mrf-to-sliding-mesh`** 或手动断开再融合 cell zones（p. 1868）。
- **网格**（11.3.2）两法：界面**保形**（节点重合）→ 常规建网格、所有 cell zone 放同一 mesh 文件、每个参考系一个 cell zone、界面用 interior 区；界面**非保形** → 按 8.4 的非一致网格流程（p. 1227）。
- **设置八步**（11.3.3）：① 选 Velocity Formulation（密度基无关）；② 逐区给平移/角速度与轴（同 SRF：Reference Frame 页 + Frame Motion + 速度/profile/UDF；**固体区不同速 → Solid Motion**；Copy To Mesh Motion 切换）；③ 墙速度绝对或相对（**例：impeller=wall-3、内部流体=fluid-5 → fluid-5 给角速度与轴，wall-3 给相对速度 0——以后改转速只改 fluid-5**）；④ 入口边界（绝对或相对）；⑤ **定义网格界面**：Setup → Mesh Interfaces → New...（用法同非一致网格，p. 1227）；⑥ 压力基瞬态开 transient-frame-motion-numerics；⑦ **初始化必须用绝对参考系**（Solution Initialization 的 Reference Frame 选 **Absolute**——选 Relative to Cell Zone 会造成初始流场间断、前几步收敛问题）；⑧ 瞬态可用 Moving Mesh Courant Number。
- **求解策略**（11.3.4）：按 SRF 指南；**多区时运动/静止件干涉表现为收敛差或振荡——强烈建议改用滑移网格解析非定常干涉**。
- **后处理**（11.3.5）：绝对/相对速度与相对总压/总温同 SRF。**Important：相对速度相对"参考区"（Reference Values 任务页指定的 zone）的平移/旋转速度——参考区速度取其 Fluid 对话框定义值**。矢量图默认绝对；Relative Velocity 画相对（颜色建议 Relative Velocity Magnitude）。**周向平均 XY 图**（circumferential averages）——量在指定周向面积上平均后对径向/轴向坐标作图（p. 4290）；叶轮机械专用后处理见 p. 2094。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.11；本页覆盖批次 51（2026-10-17）实际读取的 pp. 1831–1849，**Ch.11 全章完成**（p. 1850 为空白版权页）。
- **公式体未提取**：Ch.11 无编号公式（10.14 切向动量式在 Ch.10 已记录；Theory Guide 引用式 2.16 未提取）；坐标轴符号按 7.2.1 约定补全。Figures 11.1–11.8 为图形元素未摄取。
- 关联章节（滑移/动网格 p. 1861、混合面 p. 2030、叶轮机械后处理 p. 2094、DPM p. 2771、FSI p. 3343）仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 基本流动建模]]（10.3 旋流五分类与求解策略为 MRF 的前置）
- [[Fluent Cell Zone 与边界条件设置]]（zone 运动输入 8.2.1.1.7/8.2.2.1.5）
- [[Fluent 滑移与动网格]]（Ch.14；批次 55 后生效）
- [[index]]
