---
type: concept
created: 2026-10-17
updated: 2026-10-17
tags:
  - Ansys Fluent
  - uds
  - periodic-flow
  - swirl
  - compressible-flow
  - inviscid
  - solution-mode
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 基本流动建模

## 摘要

User's Guide 2026 R1 Part III / Chapter 10 "Modeling Basic Fluid Flow"（PDF pp. 1799–1829，共 5 节）讲基本流动物理模型。**本页已覆盖全章（批次 50）**：UDS 输运方程（单相/多相理论、50 条上限、四项自定义、设置与边界条件）、流向周期流动（streamwise-periodic，限制与压力基/密度基输入）、旋流与旋转流（五分类、湍流模型按旋流数选择、轴对称旋流设置与逐步求解策略）、可压流动（Mach 分区、理想气体可压式、浮动操作压力、求解策略）与无黏流动。运动区模型见 Ch.11–14。

## 10.1 UDS 输运方程（pp. 1799–1809）

- **理论**：任意标量 φ 的输运方程（10.1），扩散系数 Γ 与源项 S_φ 由用户给（各向异性时 Γ 为张量）。稳态按对流项处理方式解三种方程之一：**不计算对流**（10.2，纯扩散）/ **按质量流量计算**（10.3）/ **UDF 用户质量通量**（10.4）。**Note：固体区中的 UDS 不考虑带运动参考系的对流项**。
- **多相**：两类标量——**per-phase**（10.5–10.6，标量绑定到相 l，输运方程在该相所占体积内）与 **mixture**（10.7–10.12，标量为各相共享；混合密度/速度/扩散率由相值按体积/质量分数合成；混合扩散率须逐相给各材料扩散率）。UDF 质量通量选项激活时替换相应方程中的质量通量。
- **上限与命名**：最多 **50 条 UDS 输运方程**；编号从 **0** 开始（User Scalar 0/1/…，图形对话框中出现；只能经 UDF 改名）。
- **Important**：UDS 扩散系数是**材料属性**（见 [[Fluent 物理属性]] 9.6）；**湍流扩散率不会自动叠加**——需要时用 UDF 加。
- **固定值**：把某单元的 φ 固定（同 9.4 类似机制）→ 该单元不解 UDS、不计入残差和。可对 wall/入/出口边界逐标量设自定义边界条件。
- **设置要求**：标量输运问题须 Dirichlet/Neumann 边界完备；UDS 收敛判据可能需比默认 0.1 更紧；**残差可能不反映解质量——建 UDS 监控判断收敛**。收敛控制手段：Advanced Solution Controls 用 **F-Cycle** 代替 Flexible cycle、加 BiConjugate gradient stabilizer、用 ILU smoother、增大 pre/post-sweeps、调欠松弛因子。
- **单相设置**（10.1.3.1）：① Parameters & Customization → User Defined Scalars → New... 给条数；可开 **Inlet Diffusion**（入/出口边界含扩散项）；逐标量（UDS Index 递增）：**Solution Zones**（all fluid/all solid/all zones/selected zones）、**Flux Function**（none / mass flow rate / UDF——分别对应 Theory Guide 式 1.9/1.10/1.11）、**Unsteady Function**（none = 稳态 / default / UDF）。② 源项：Fluid/Solid 对话框开 Source Terms → Source Terms 页 → 逐标量 Edit... 给 Number of User Scalar Sources，各源 none/constant/UDF。③ 扩散率：Materials 中 UDS Diffusivity 选 defined-per-uds（默认）或 user-defined。④ 边界条件：BC 对话框 UDS 页逐标量选 **Specified Flux 或 Specified Value**；内部双面墙可选 **Coupled Boundary**（仅当该标量在流体+固体区都定义时出现）；Specified Flux 输入 = 边界通量值（流入域法向 n 的点积负项）；Specified Value = 标量值。⑤ 解参数 + 初始化 + 计算。⑥ 后处理：User Defined Scalars... 类的 **User Scalar-n** 与 **Diffusion Coef. of Scalar-n**。
- **多相设置**（10.1.3.2）：同上，**每标量多一项 Phase 选择（primary/secondary/mixture；默认关联 = mixture）**；边界条件在 mixture 上设。

## 10.2 周期流动（流向周期/streamwise-periodic，pp. 1809–1815）

- 两类周期流：无压降型（见 8.4.18）与**流向周期（"充分发展"/"streamwise-periodic"）**；周期换热见 p. 2335。应用：紧凑换热器通道、管束、充分发展管流——流动图案逐周期重复、每模块压降恒定。
- **限制**（10.2.1.2）：**流动必须不可压**；非稳态 + 平移周期建议用指定压力梯度；密度基只能指定压降（pressure jump）、压力基可指定质量流量或压力梯度；**不允许净质量加入（入/出口）或额外源项**；组分仅在含入/出口（无净加入）时可算，**不允许反应流**；**质量流周期条件仅支持一个周期对**（两对不行）；稳态颗粒轨迹仅当颗粒能离开域（不产生不完整轨迹）；多相可用平移周期但不能用质量流量法（只能恒压力梯度）；压力基：指定非零质量流/压力梯度不能用于变密度流；密度基：密度为压力函数时不能用周期压降；周期边界上温度/压力类变量的节点值 = 相邻单元加权平均（shadow 侧单元不计入）→ 周期区与 shadow 区云图可能不同。
- **压力基输入**（10.2.2）：平移周期边界（平行、等尺寸）→ Setup → Boundary Conditions → **Periodic Conditions...** 对话框：选 **Specify Mass Flow**（多数问题已知流量）或 **Specify Pressure Gradient**（β，式 1.22 的线性压力梯度分量）；质量流输入 Mass Flow Rate（**轴对称按 2π 弧度**）+ 可选 β 初值；压力梯度法直接给 β；**Flow Direction**：给 X,Y,Z 点（从原点指向该点的向量；须平行于周期平移方向或反向）。**β 计算参数**（10.2.2.1）：指定质量流时 Fluent 迭代求 β——**Relaxation Factor** 与 **Number of Iterations**（β 修正在 SIMPLE/SIMPLEC/PISO 压力修正步内的子迭代；默认 2 次子迭代通常够、可增以加速收敛）+ β 初值（Update 按钮刷新当前值）。
- **密度基输入**（10.2.3）：BC 任务页 Periodic → Edit → Translational（默认）+ **Periodic Pressure Jump**。
- **监控**（10.2.4）：指定质量流时建含 periodic pressure gradient 的 report plot 监控 β 收敛。
- **后处理**（10.2.5）：速度场应完全周期；密度基只报告压力的线性分量（非周期）；压力基报告周期压力场 p'。**Note：Pressure Gradient 云图是求解器辅助压力场、非真实值**；β 当前值看 Periodic Conditions 对话框。

## 10.3 旋流与旋转流（pp. 1815–1821）

- **五分类**：①轴对称带旋/旋转；②全三维旋流；③需运动参考系；④需多参考系/混合面；⑤需滑移网格——前三类之外见 Ch.11（后三类为"运动区"）。
- **轴对称 + 旋流**：几何与流条件轴对称但可有旋周速度——2D 求解 + 预测旋周（swirl）速度；轴对称假设 = 无周向梯度，但旋周速度可非零（切向动量方程 10.14）。
- **3D 旋流**：周向有几何变化/流动梯度 → 必须 3D；**3D 旋流无特殊设置输入与求解程序**——建议速度入口用圆柱坐标（p. 1464）、旋转/旋流速度渐进升速有助于稳定。运动边界 → MRF/多 MRF/混合面（p. 1831/2030）。
- **旋流湍流模型选择**（10.3.2）：**旋流数 S = 角动量轴向通量/轴向动量轴向通量**（10.15，R 为水力半径）。**弱-中等旋流（S ≲ 0.5）：RNG k-ε 或 realizable k-ε 明显优于标准 k-ε**；**强旋流（S ≳ 0.5）：强烈推荐 RSM**（只有二阶矩封闭能严格模拟强湍流各向异性）。旋风分离器/旋流燃烧室等近壁湍流多为次要问题——核心区湍流模型精度主导；壁面主动产生旋流（压力梯度驱动二次流）时**非平衡壁面函数**常能改进预测。
- **网格**（10.3.3）：轴对称旋转轴 = x 轴、网格位于 x 线及以上；**旋转边界层很薄 → 旋转壁附近细网格**；自由涡型流动中心线周向速度梯度陡 → 细网格。
- **轴对称旋流设置**（10.3.4.1）：① General 任务页 Space 选 **Axisymmetric Swirl**；② 在入口/墙定义旋周速度 w（入口 p. 1464、运动墙 p. 1514）；**旋转轴用 axis 边界类型**。
- **求解策略**（10.3.4.2）：动量方程高度耦合（强旋转 → 大径向压力梯度 → 驱动轴向/径向流 → 反过来决定旋流分布）→ 可能不稳定。手段：**PRESTO!** 压力格式（仅压力基；适合旋流陡压力梯度）；网格加密；**欠松弛建议：径/轴向 0.3–0.5、旋周 0.8–1.0**（压力基）；**分步求解**（仅压力基；密度基全方程同时解不适用）：① 先按 Axisymmetric（无旋）解流场作初值 → ② 开 Axisymmetric Swirl + 旋流边界 → ③ 只解 **Swirl Velocity** 方程（湍流方程保持激活）让旋转"扩散"全场 → ④ 关 Swirl、固定旋周速度解 **Flow**（动量+连续）建立轴向/径向流动 → ⑤ 全方程联立（配合上述欠松弛）。可先等温后加热、先层流后湍流（两求解器通用）。**渐进升速**（10.3.4.2.2）：从约 10% 转速/旋流起步 → 求解 → 存解 → 倍增转速 → 以上一解重启 → 循环至目标工况。
- **后处理**：Swirl Velocity（Velocity... 类）、Swirl-Wall Shear Stress（Wall Fluxes... 类）。

## 10.4 可压流动（pp. 1821–1828）

- **Mach 分区**（10.4.1）：M = v/c（10.16），c = √(γRT)（10.17）；M ≪ 1（约 0.3 以下）可压性可忽略；M ≈ 1 跨音速（可压性重要）；M > 1 超音速（激波与膨胀扇）。Fluent 覆盖亚/跨/超音速。
- **物理**（10.4.2）：等熵总静关系（10.18–10.19）；空气临界压比 p*/p0 = 0.5283 → 最小面积处壅塞；下游可加速至超音（压降）或回落亚音（压升）；超音遇逆压 → 激波。基本方程 = 常规连续/动量 + **能量方程必须开启**；压力基湍流建议开**黏性耗散**项（高速流重要；密度基恒含）。可压理想气体律 ρ = (p_op + p)/(R T/M)（10.20）；甚高压用真实气体（9.17）。
- **设置输入**（10.4.3）：① Operating Pressure（= 表压零点的绝对静压；指南 9.15；瞬态可压 → 浮动操作压力）；② 能量方程 On；③（压力基湍流）Viscous Model 开 **Viscous Work**（密度基恒含，无需此步）；④ Materials：Density 选 ideal-gas + 相关属性；⑤ cell zone/边界条件选适合流态的良定组合。**所有压力输入为表压；入口温度给总温（滞止）而非静温**。
- **良定边界组合**（10.4.3.1）：入口——压力入口（总温+总压，超音速入口另加静压）/ 质量流入口（质量流+总温）；出口——压力出口（出口静压；**出口超音速时被忽略**——超音区信息全向下游，压力直接从相邻单元外推 [66]）/ 质量流出口（出口质量流）。
- **浮动操作压力**（10.4.4）：处理绝对压力渐变的瞬态可压流——慢速亚音、静压累积场景；**用积分质量平衡单独算压力升降、不经声波传递机制**；典型应用：封闭域内燃烧/加热、向封闭域泵气。**限制：不可用于跨音或不可压流；不能与压力入口/压力出口/exhaust fan/inlet vent/intake fan/outlet vent/pressure far-field 边界同用**。理论：绝对压 = p_op^float + p'（10.21，p' 相对最小压力单元——参考点浮动）；p_op^float = p_op,init + Δp(t)（10.22）；**压升计入浮动操作压力而非 p'，防止 32 位实数的舍入误差**。启用：时间依赖激活后 Operating Conditions 勾 Floating Operating Pressure（Reference Pressure Location 输入项随之消失）；**Initial Operating Pressure 在 Solution Initialization 任务页给**（随 case 保存）；当前值存于 data 文件（Operating Conditions 对话框可见）；**重置数据后自动回到初始操作压力**。监控：Surface Report Definition 的 **Absolute Pressure**（Pressure... 类）。
- **求解策略**（10.4.5）：速度-密度-压力-能量强耦合 + 激波间断 → 不稳定。手段（压力基）：**初场近滞止（速度小非零、压力=入口总压、温度=入口总温）、前 50 迭代关能量方程（能量 URF=1）、压力 URF 0.4、动量 URF 0.3；稳定且能量开启后压力 URF 升 0.7**；Solution Limits 设合理温度/压力限（临近收敛时的限值提示可能是物理值——放宽限值）；边界压比从低渐升；低 Mach 可从不可压解起步（有时初值较差）；有时先算无黏解有帮助。
- **后处理**（10.4.6）：Total Temperature（Temperature...）、Total Pressure（Pressure...）、Mach Number（Velocity...）。

## 10.5 无黏流动（pp. 1828–1829）

- **用途**：忽略黏性——高 Re、惯性主导；高速弹丸气动力快速估算（压力力主导）；**复杂流动/几何的良好初场**：先无黏起步、残差下降后开层流/湍流继续收敛——某些极复杂流动这是唯一能起算的方式。
- **设置**：Viscous Model 选 **Inviscid**；边界与物性照常。**Note：无黏流的壁为滑移面——速度非零，切向速度由控制方程解确定**。
- **求解策略**：高速流 → 压力基降动量欠松弛、密度基降 Courant；残差单调下降后回升至默认；可压流策略通用（p. 1827）。
- **后处理**：升阻力用 Force Reports（Results → Reports → Forces）。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.10；本页覆盖批次 50（2026-10-17）实际读取的 pp. 1799–1829，**Ch.10 全章完成**（p. 1830 为空白版权页）。
- **公式体未提取**：Eq 10.1–10.22 的公式体均为图形对象、文本提取缺失；已按周边文字记录结构与式号（10.16 Mach 定义、10.17 声速、10.19 等熵临界压比 0.5283、10.20 可压理想气体等文字/常识明确处已注明）。需要精确公式时须回看 PDF 对应页。
- 本页 UDS 上限 50、编号从 0、旋流数模型选择阈值、PRESTO!、欠松弛建议值（0.3–0.5/0.8–1.0、压力 0.4/动量 0.3）等均为原文正文数值。Figures 10.1–10.12 为图形元素未摄取。
- 关联章节（运动参考系 p. 1831、湍流 p. 2125、传热 p. 2221、周期换热 p. 2335、组分 p. 2451、DPM p. 2771、多相 p. 3027、凝固 p. 3335、Solver p. 3709）仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent Cell Zone 与边界条件设置]]（8.4.18 无压降周期边界、8.3 操作条件）
- [[Fluent 物理属性]]（9.6 UDS 扩散率、9.15 操作压力、9.17 真实气体）
- [[index]]
