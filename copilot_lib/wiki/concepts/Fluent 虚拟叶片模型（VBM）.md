---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags:
  - Ansys Fluent
  - VBM
  - actuator-disk
  - blade-element-theory
  - rotorcraft
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 虚拟叶片模型（VBM）

## 摘要

User's Guide 2026 R1 Part III / Chapter 19 "Fluent's Virtual Blade Model"（PDF pp. 2427–2450，共 9 节）讲旋翼/螺旋桨/风轮的**时间平均致动盘降阶模型**。**本页全章完成（批次 66，pp. 2427–2450，覆盖 19.1–19.9）**：模型定位与两类致动盘方法、BET 动量源与自动配平（Newton-Raphson）、Embedded/Floating Disk 两模式、网格指南、翼型数据文件格式、GUI 配置 28 步、15 个场变量与 Rotor_xx_Loads.csv 报告。

## 19.1 引言与两类致动盘方法（pp. 2427–2428）

- **定位**：分析多旋翼与机身气动干扰；把 3D 旋翼替换为致动盘（actuator disk），经**隐式动量源项**作用于控制方程；叶片不实体建模故称"虚拟叶片"。支持混合非结构网格（多旋翼近距布局 + 局部加密方便）；旋翼尾迹与机体等的非线性干扰由 VBM 与 Fluent N-S 求解器耦合获得；配平（trimming）用迭代法自动完成。
- **适用场景**：时间平均累计效应足够时——机身阻力与尾梁力预测（多工况）、发动机尾焰分布及其对蒙皮加热与 IR 特征的影响等；需要叶片细节（失速行为、噪声、FSI）时应用高保真方法。历史做法即"等直径转子盘替代物 + 3D N-S/Euler 求解器"，网格更小更简单、计算量大幅降低。
- **两类致动盘方法**：①**pressure-disk rotor model**（Chaffin）——盘由两面组成、一侧出流一侧入流；盘可无厚度、两面网格节点无需配对重合；跨盘施加随半径与方位角变化的压力跳升，**质量须显式守恒**。②**Zori et al. 动量源法**——动量源作用于与网格一体的**单单元厚**致动盘，无进出流边界；**质量自动守恒**。两者都按**叶素理论（BET）**用翼型堆叠的升阻力系数查表计算旋翼力。**Fluent VBM 基于 Zori 与 Yang 模型并增强**。
- **配平沿革**：传统假设推力系数-集体角、力矩-周期角线性 → 配平例程易实现但数值不稳定 → 历史上只能单旋翼（忽略尾桨）；Yang et al. 提出 **Newton-Raphson 迭代自动配平**处理非线性关系。
- 叶片用**2D 翼型截面堆叠**表示（twist、chord、翼型沿展向可变）；升阻力查表可含 **Mach 与 Reynolds 数**依赖（覆盖低/高速）。支持**任意数量旋翼**：主/尾桨直升机、多倾转旋翼、四旋翼、多机近距编队、单/多发螺旋桨飞机、大型风电场。
- 致动盘单元的两种指定：**Embedded Disk**（网格中标记为独立 cell zone）或 **Floating Disk**（按盘面几何切割搜索单元）。

## 19.2 VBM 理论（pp. 2428–2430）

- 同时解决两任务：①时间平均流场解（Fluent 完成；无粘/层流/湍流、可压/不可压均可）；②叶片气动降阶解计算动量源。动量源初始未知，经致动盘与流解耦合、随迭代演化。
- **BET 计算**：叶片 → 展向翼型截面堆叠，每截面按 2D 翼型处理（chord、翼型、twist 沿展向可变）。绝对系速度场 → 变换到局部叶片截面参考系（切向速度矢量 + 盘法向定义）得相对速度 → 定出局部迎角 α、Mach、Re → 查该截面翼型表得 cl、cd → 单位展向瞬时旋翼力（**Eq 19.1**，公式体未提取；含弦长 c(r/R)、桨尖半径 R、截面相对流速）。
- **时间平均**：设转速恒定，一个周期的时间平均 = **2π/N 角度上的几何平均**（**Eq 19.2**，公式体未提取）；N = 叶数，r = 单元中心径向坐标；盘上面面积 A 的单元得平均力向量 → 变换回绝对系 → 除以单元体积 V = 单位体积时间平均源项，加入致动盘每单元动量方程。迭代至收敛。**支持结构化与混合非结构网格（六面体与棱柱）**。
- **推力/力矩系数惯例**（19.2 收尾）：北美惯例 k = 1（½ 吸收进系数）、欧洲惯例 k = ½（公式显含 ½）；**Fluent VBM 取 C_NA-EU = 1**（p. 2430 符号经渲染视觉核对）。
- **湍流建模注记**：建议用标准两方程模型 **k−ε 或 k−ω**（p. 2430 经渲染视觉核对）；VBM 不直接增大建模转子区内的湍动能生成，但转子动量会间接影响下游湍流混合。

## 19.2.1–19.2.7 模型构成（pp. 2430–2437）

- **19.2.1 VBM Mode**：**EDM（Embedded Disk method）**——网格中建单单元厚致动盘；**FDM（Floating Disk method）**——按盘面几何切割搜索单元。EDM 网格要求见 19.3.1；更准更稳，但多旋翼时建网困难；**瞬态模拟中盘的任何移动都需网格位移/替换，不实用**。FDM 无需盘网格与棱柱层（机身周围任意单元类型）；浮动盘可自动生成，或用 Fluent 后处理工具建平面再 iso-clip 手动创建（GUI 设中心/取向/tip 与 root 半径后按键创建）；**省略创建则求解前自动生成**。
- **19.2.2 Rotor Disks**：几何由中心 {X,Y,Z}、tip/root 半径、pitch 与 bank 角（或盘法向量）表征。**盘法向自然取向为 +Z**；取向不同时**先 pitch（绕 Y 轴）后 bank（绕旋转后的 x′ 轴）**。Note：**旋转不可加、不可交换、必须按此顺序、遵循右手法则**；CAD 建模倾斜旋翼也须同序。示例：螺旋桨法向沿 −X → pitch = −90°、bank = 0°；旋翼轴沿 +Y → pitch = 0°、bank = −90°。也可直接给法向分量，VBM 按自然取向反算 pitch/bank。
- **19.2.3 Blade Geometry**：翼型堆叠沿归一化展向 r/R 变化 chord/twist/翼型；**每截面两端之间 chord、twist 等按线性分布**（两端之间插值的具体符号在提取文本中缺失，按上下文为截面几何量线性插值）。查表覆盖全部可能工况的 Re/Mach 范围越全，精度越高（VBM 在叶片上定出局部 Re/Mach 后插值取 cl/cd）。
- **19.2.4 Blade Pitch**：桨距角（勿与旋翼 pitch 角混淆）= 相对盘平面的角度；一阶近似（忽略扭转弹性与高阶谐波）= 基线集体角 θ0 + 周期角分量 θ1c·cos ψ + θ1s·sin ψ（ψ 方位角；公式体未提取）。θ0/θ1c/θ1s 可手动指定或由自动配平算出。集体角 = 全部叶片同步相对盘面的均匀角；θ1c/θ1s（cos/sin 幅值）对应多数直升机旋翼的**自动倾斜器（swash plate）角**，控制俯仰/滚转姿态。叶片**扭转（twist）叠加到集体角**，集体角与扭转的参考点可沿叶片任选（只要两者之和给出正确桨距）；直升机传统参考点在 **3/4 展长**，主旋翼常向桨尖**负扭转**——逐渐减小桨尖迎角、增大失速与抖振裕度、卸载外段、增大挥舞稳定性。VBM 把**有效桨距角 = 集体角 + twist(r/R)** 作为 VBM 场存入解文件。
- **19.2.5 Blade Flapping**：铰接式旋翼叶片在离心与气动力下挥舞；**挥舞运动不由模型计算**，但若挥舞特性已知，模型可经"速度从旋翼盘面变换到实际桨尖轨迹平面"计及**锥角 β0 与一阶挥舞谐波 β1c、β1s**；合成挥舞角 β = β0 + β1c·cos ψ + β1s·sin ψ（公式体未提取）。Note：**旋翼盘保持平面，模拟的是叶片挥舞**。挥舞引起的迎角变化被计算；较小的挥舞速度分量（本应加到垂直于叶片路径的速度上）被忽略；摆振（lead-lag）因影响小而忽略。
- **19.2.6 Rotor Trimming**：前飞旋翼载荷相对"前飞速度矢量与旋翼法向所定义平面"不对称；除集体角维持平飞高度外还需周期角平衡盘上载荷、控制俯仰/滚转力矩。精确仿真须旋翼在目标推力 T、滚转力矩、俯仰力矩下运行；自动配平例程免去经验试凑。**Important：参考面积与速度在不同应用（旋翼机/螺旋桨等）可能不同——推力与力矩系数必须用同一公式；VBM 把系数定义为桨尖速度与含根部切除（root cutout）的盘面积的函数**。**Note：力矩计算中忽略挥舞铰偏置（flapping hinge offset）的影响**。配平例程算出达到目标推力/俯仰/滚转力矩的集体与周期角；系数表达为集体/周期角的函数（公式体未提取）。**Newton-Raphson 迭代**（Yang et al.）自动配平任意数量旋翼：用户给初始角；每 N 次流动迭代（**update frequency**）求解器暂停，VBM 计算旋翼参数并用 Newton-Raphson 求新角度组；**无解析 Jacobian → 在冻结流场（时间层 n）对每个角度独立 ±a 扰动数值求导**（算法实为 **Secant Method**）；角度更新带**欠松弛因子（Damping Factor）η**，0 < η ≤ 1，**推荐 0.7**；每 N 迭代重复至性能参数达目标且流场收敛；配平收敛用系数误差的 **L2 范数**打印到 Console 展示；例程稳健、多旋翼算例可收敛。
- **19.2.7 Tip Losses**：大展弦比叶片按展向各站位 2D 流动近似计算升阻力；**桨尖附近环流 90° 转折脱落形成尖涡**，引入 VBM 无法直接模拟的升阻力损失 → 用**尖部损失因子 F** 修正桨尖附近的 cl/cd；**cd 修正值强制不低于该翼型最小阻力系数**。两选项：①**Quadratic Tip Loss Function**——与到桨尖距离平方成反比的阻尼函数，从用户指定的 **tip loss limit** 起（默认 **96% 旋翼展长**）；②**Modified Prandtl's Tip Loss Function**——Prandtl 尖部损失函数一般用于 BEMT（叶素动量理论：盘上环形流管动量平衡 = 对应展向截面叶素力平衡）；VBM 中 RANS + BET 组合下 RANS 本身可捕捉盘尖附近的损失，但那不代表真实旋翼桨尖的损失，故用**修正版**允许按应用调谐：F 由调谐系数（**应 > 1**，UI 设置）与 f 给出（f 由叶数 N、叶素径向位置 r、旋翼半径 R、**诱导入流角 φ**——叶素处相对入流速度法向与切向分量夹角——定义；公式体未提取）。

## 19.3 网格指南与创建 VBM 盘（pp. 2437–2439）

- **19.3.1 Embedded Disk**：流域中旋翼位置建**平盘形内部表面**；CAD 中标记为 internal wall / internal surface，按**单层节点**离散（网格跨界连续、无重复节点）；根部切除（cutout，毂附近死区）可忽略。从盘面单元沿盘法向**挤出单层均匀棱柱或六面体单元**；厚度无定则，**建议保持为盘直径的 1/40–1/100**；**盘下游的单层棱柱单元标记为独立 zone（rotor zone，每旋翼一个）**。VBM 逐 zone 循环读单元算源项。Note：**与盘单元搭接以过渡到其余网格的 pyramid/tetra 单元属于流动域、不属于 rotor zone**。
- **19.3.2 Floating Disk**：无需建盘网格；浮动盘由旋翼几何定义创建（Blade Tip Radius、Blade Root Radius、Rotor Disk Origin、Rotor Disk Normal Vector）；若取向按角度给出，Fluent 自动算出法向分量。GUI/TUI 按 **Apply** 后自动创建；也可 Apply 前 **Create Floating Disk** 手动创建，流程：①创建 custom field function **radius-fdisk-RotorName**（从 Rotor Disk Origin 算半径）②按 Origin + Normal 建 plane surface **plane-fdisk-RotorName** ③用 iso-clip 切出半径介于 root 与 tip 之间的 **srf-fdisk-RotorName** ④在 GUI Rotor Surface 下选中。Note：**iso-clip 仅在有解时可用——按 Apply 或 Create Floating Disk 前须先加载或初始化解，否则警告**。
- **19.3.3 General Considerations**：支持结构化与非结构混合网格。**盘附近及盘内外圆周加密**（干扰效应与损失模型作用区）——默认 quadratic 尖部损失模型在 **0.96 ≤ r/R ≤ 1.0** 网格很粗时解不平滑。注意进出口边界尺寸：**大重量直升机悬停工况须保证穿过计算域的空气质量流远大于穿过全部旋翼的质量流**，否则整体仿真发散、收敛很差或旋翼产生不了目标推力；原因：VBM（以及 MRF 等高保真法）是**超定**的——真实飞行速度由力平衡决定，而 CFD 中速度由用户指定，可能与旋翼设置不兼容；例如**悬停直升机远场边界应指定合适的非零质量流**。下游网格要足够加密以捕捉 VBM 附加动量与旋翼尾迹同其他旋翼/机体部件的干扰；旋翼载荷一般非均匀 → 可能出现二次涡，应尽量捕捉。

## 19.4 翼型文件格式（pp. 2439–2441）

- VBM 结果精度取决于各叶素升阻力数据；多翼型文件可用；桨尖速度高 → 数据文件应含覆盖全部气动工况的 Re/Mach 范围；前飞**后退边可能倒流 → 数据须覆盖 −180° ≤ AoA ≤ +180° 全迎角谱**。文件须位于工作目录、后缀 **.dat**（如 naca0012.dat）。
- **Table 19.1 格式**（两列空格分隔）：`Airfoil` 名（与文件同名，**≤30 字符**）；`Itot` = 文件中 cl 与 cd 表总数（**最多 30 张（cl 加 cd）**）；`cl` 标签（**≤10 字符**）开始升力表；`Re` 表的雷诺数；`Ma` 表的马赫数；`Jtot` 随后表的行数；每行 `AoA 值`（**最多 250 个数据点**）；`cd` 标签开始阻力表（同结构）；更多表则重复。
- 示例 naca0015：2 张表；cl 表 Re 100000.0、Ma 0.1、41 行（−180°→+180°）；cd 表同 Re/Ma、71 行。

## 19.5–19.6 启用与配置（pp. 2441–2446）

- **启用**：Physics ribbon 的 Models 组 → Virtual Blade Model 对话框；或树 Setup → Models；或 Models task page。TUI：`define/models/virtual-blade-model/enable?`。**Note：仅 3D + Parallel 可用（Serial 选项已弃用）；必须已设置或读入有效 case/mesh 才能启用；不兼容多相流——若激活 Fluent 将阻止启用并在 Console/弹窗警告**。
- **配置入口**：Virtual Blade Model Rotor Inputs 对话框（GUI）或 TUI（命令清单见 Fluent Text Command List）。每个活动旋翼最多三个配置面板：**General、Geometry、Trimming**；EDM 与 FDM 输入相同（另注处除外）；General 随模式略异，**Geometry 与 Trimming 两页完全相同**。
- **28 步配置要点**：①Enable VBM ②选 VBM Mode（EDM/FDM）——**全部 rotor zone 必须同一模式，只能为第一个 Rotor Zone 选择** ③Rotor Names 下 Add 新旋翼或选已有（支持任意数量）④Active Rotor Name ⑤Number of Blades ⑥Rotor Speed [rad/s]——**转向按相对旋翼法向的右手法则** ⑦Blade Tip Radius [m] ⑧Blade Root Radius [m]（**仅 FDM 模式下可输入**）⑨Tip Loss Function——Quadratic：Tip Loss Limit（桨尖半径百分比，**默认 96%，100% = 不引入尖部损失**）；Prandtl：Tuning Coefficient（**≥ 1，默认 1**）⑩Rotor Disk Origin XYZ——**EDM 输入盘 cell zone 的中心（不是盘几何中心）；FDM 输入盘中心** ⑪取向——Rotor Disk Angles（pitch/bank [deg]）或 Rotor Disk Normal（XYZ 分量）⑫盘面——**EDM 从 Interior Surfaces 列表选 Rotor Face Zone；FDM 无需选择** ⑬FDM 手动建盘（可选）：先设半径/root cutout/原点/取向，**先加载或初始化解**（否则警告），按 Create Floating Disk → 自动创建并选中 srf-fdisk-RotorName ⑭初始 Collective [deg] 集体角 ⑮Blade Pitch 的 Cyclic Sin/Cos [deg] 系数（幅值）⑯Cone [deg] 挥舞角 β0 ⑰Blade Flapping 的 Cyclic Sin/Cos [deg] 系数 ⑱Geometry 页 ⑲Number of Sections（**默认最多支持 50 截面**）⑳自最内（cutout）逐段输入 Radius（r/R）、Chord [m]、twist [deg]、该截面含 CL/CD 数据的 Airfoil Data File 名（可带可不带 .dat 后缀，自动补全；**但项目目录中必须存在对应的 .dat 文件**）㉑Trimming 页（需配平的旋翼）㉒启用 Collective pitch 和/或 Cyclic pitch（按所选配平操作激活附加输入框）㉓**Damping Factor（欠松弛因子）：默认 0.1，最大 1，推荐 0.7（增大可加快收敛）** ㉔Desired Thrust Coefficient ㉕Desired Pitch-/Roll-moment 系数通常留 0（需要俯仰/滚转力矩时可给非零）㉖**Change/Create 保存当前旋翼数据——不点就切到其他旋翼会丢失当前活动旋翼设置** ㉗对其他 rotor zone 重复 3–26 ㉘**Apply：保存当前旋翼 + 预处理全部旋翼输入 + 关闭对话框**。Note：初始配置后每当改动活动旋翼参数，切换旋翼前必须 Change/Create；忘记 Apply 就开始迭代 → VBM 会自动预处理输入并执行初始计算与内存分配；**.cas 文件保存全部旋翼信息**。
- 数值口径：19.2.6 给 Damping Factor 推荐 0.7；配置步骤给默认 0.1/最大 1/推荐 0.7——两处一致（默认 0.1，推荐调至 0.7）。

## 19.7–19.8 场变量、监视与报告（pp. 2446–2448）

- **19.7 场变量**：VBM 为全域每个计算单元提供 **15 个 VBM 数据场**；**cell-based——按 node 变量显示会不正确**；实际只在致动盘附着单元上有意义。Table 19.2：VBM Radius（半径）、VBM Incident Velocity（气流相对入流速度）、VBM Pitch Angle（有效桨距角）、VBM Chord（弦长）、VBM Reynolds Number、VBM Mach Number、VBM AoA（迎角）、VBM cl、VBM cd、VBM Normal Force / Tangential Force / Radial Force（瞬时旋翼力三分量）、VBM X-Force / Y-Force / Z-Force（时间平均力分量）。
- **19.8 监视与报告**：默认为每个旋翼 xx 写 **Rotor_xx_Loads.csv**，报告 VBM 全局输出——按 BET 计算的旋翼盘力、力矩与功率（Table 19.3；局部坐标按 Figure 19.1）。**Table 19.3 输出类型**：Xp-force (N)、Yp-force (N)、Thrust (N)、Roll-moment (N·m)、Pitch-moment (N·m)、Torque (N·m)、Power (W)——每类给出 Quantity（物理量）与 Coefficient（系数，Ouput Type 可选）两种定义。**VBM Report Definition** 建立路径：Solution → Reports → Definitions → New... → VBM Report → Rotor...；选择报告类型；需要时把 Output Type 设为 Coefficient。要多个报告定义分别打印到 Console/写文件/绘图，须**逐个单独定义**——用于监视收敛与记录时间历程。Note：**读入 data 文件时，配平期间算出的新集体/周期角会打印到 Console，但不会替换 VBM 输入设置中的现值；想用新值继续仿真须手动更新 VBM 设置**。

## 19.9 References（p. 2448–2449）

16 条文献。关键的：Chaffin NASA CR-4692（1995，pressure-disk rotor model）；Zori & Rajagopalan（J. American Helicopter Society Vol.40, 1995，动量源法原型）；Yang, Sankar, Smith, Bauchau（AIAA Reno 2000，NR 自动配平）；Leishman《Principles of Helicopter Aerodynamics》（2000）；Capitao Patrao（2017，OpenFOAM rotorDiskSource 验证）；Liou/Brand/Komerath 等旋翼-机身干扰实验系列（1989–1990）。

## 证据与适用条件

- 页码：pp. 2427–2449 为正文（19.9 References 止于 p. 2449）；**p. 2450 为空白版权页**。目录范围 pp. 2427–2450 全部覆盖，**Ch.19 全章完成**。
- **公式**：Eq 19.1 起全部编号公式（BET 单位展向力、时间平均、推力/力矩系数定义、配平方程组与角度更新、两种尖部损失函数）公式体未提取，知识页按周边文字记录结构、变量与语义，未凭空补写。
- **符号核验**：p. 2430 湍流建议模型（k−ε / k−ω）与系数名 C_NA-EU 经 fitz 500 dpi 渲染视觉核对确认；19.2.3 "每截面两端之间线性分布"句中的具体符号在文本层缺失，已按上下文定性记录。
- Figures 19.1–19.6（旋翼盘示意、翼型堆叠、有效桨距、挥舞、VBM 网格剖面、GUI 面板）为图形元素未摄取；Table 19.1–19.3 已完整提取照录。
- 硬约束：**VBM 仅 3D + Parallel（Serial 弃用）；不支持多相流**；须先有有效 case/mesh。
- 手册建议值（两方程湍流模型、棱柱层厚 1/40–1/100、tip loss limit 96%、Damping Factor 0.7、悬停远场非零质量流）受具体问题条件影响，不应视为通用保证。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]
- [[Part III - Solution Mode]]
- [[Fluent 运动参考系]]（MRF 高保真对照；VBM 亦被手册归为超定模型一类）
- [[Fluent 叶轮机械流动]]（turbo 方法对照）
- [[Fluent 滑移与动网格]]（EDM 瞬态盘移动需动网格的对照）
- [[index]]
