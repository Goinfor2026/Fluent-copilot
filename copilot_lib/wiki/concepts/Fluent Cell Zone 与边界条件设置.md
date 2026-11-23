---
type: concept
created: 2026-10-17
updated: 2026-10-17
tags:
  - Ansys Fluent
  - boundary-conditions
  - cell-zone
  - parameters
  - solution-mode
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent Cell Zone 与边界条件设置

## 摘要

User's Guide 2026 R1 Part III / Chapter 8 "Cell Zone and Boundary Conditions"（PDF pp. 1347–1649，共 11 节）讲 cell zone 与边界条件的设置。**本页已覆盖全章（批次 39–46，pp. 1347–1649）**：zone 类型清单、设置/复制/改名规则、TUI 批量语法、参数体系、Fluid/Solid 条件、多孔介质全节、3D Fan、固定值与温度锁定、源项、操作条件、全部 22 类边界条件、Multi Edit、瞬态边界条件、四类声学波模型、用户自定义风机、Profiles（六种类型/两种文件格式/插值/重定向/复制）与 GT-POWER/WAVE 一维耦合。边界条件与 zone 关联而非单个面/单元——合并同类 zone 是简化设置的基本手段（见 [[Fluent 网格读取与操作]] 7.12.1）。

## 章节地图（11 节 → PDF 起始页）

- 8.1 Overview（1347）；8.2 Cell Zone Conditions（1370）；8.3 Operating Conditions；8.4 Boundary Conditions；8.5 Editing Multiple Boundary Conditions at Once；8.6 Transient Cell Zone and Boundary Conditions；8.7 Boundary Acoustic Wave Models；8.8 User-Defined Fan Model；8.9 Profiles；8.10 Coupling BCs with GT-POWER；8.11 Coupling BCs with WAVE。8.3–8.11 的起始页见 [[Part III - Solution Mode]] 章节导航。

## 8.1 Overview（pp. 1347–1369）

### 8.1.1 Zone 类型四大类（Table 8.1）

- **External（外部边界，只连一侧单元）**：axis、degassing、exhaust fan、inlet vent、intake fan、interface、mass-flow inlet、mass-flow outlet、outflow、outlet vent、overset、pressure far-field、pressure inlet、pressure outlet、symmetry、velocity inlet、wall（仅单面）。
- **Internal（内部边界，两侧连单元）**：fan、interior、porous jump、radiator、RANS/LES interface、wall（仅双面）。
- **Periodic**：periodic。**Cells**：fluid、solid（多孔介质与 3D fan 属 fluid cell 的类型）。

### 8.1.2–8.1.4 任务页、改类型、设置

- Cell Zone Conditions 与 Boundary Conditions 任务页（Setup → ...）是 Outline View 树之外的另一套入口；zone 可按名称或类型分组；树中右键单个 zone/边界可直接修改。Boundary Conditions 分支右键 **Group By/Adjacency** 可看出哪些边界属于同一 cell zone。
- **改类型**（8.1.3）：设置条件前先核对全部 zone 类型。External 与 Internal **只能在同一类别内互换**。树中多选（Shift/Ctrl，须同类别）→ 右键 Type 子菜单；TUI `define/boundary-conditions/zone-type` 或 `.../modify-zones/zone-type`，多个 zone 用括号列表如 `(4 9)`。规则：默认名（`<type>-<ID>`/`<type>_<ID>`/`<type>.<ID>`）的 zone 改类型时类型部分自动改名；**大量内部区与 wall/shadow 对互转务必一次性完成**（多选或括号列表）——可大幅缩短处理时间；wall/shadow 对改成其他内部类型（fan/interior/porous jump/radiator/RANS-LES interface）时选 wall 或 shadow 任一即可，结果保留 wall 的 ID 与朝向、shadow 删除；**不能**用此法在 periodic 型与其他类型间转换（须走创建/解耦周期区流程，[[Fluent 网格读取与操作]] 7.12.5–7.12.6）；VOF/Mixture/Eulerian 多相的改类型流程略有不同（p. 3070，未摄取）。
- **设置条件**（8.1.4）：**边界条件与 zone 关联，不与单个面/单元关联**——要共享条件的 zone 先合并（[[Fluent 网格读取与操作]] 7.12.1）。树右键 zone → Edit...，或任务页 Zone 列表选区 → Edit...。TUI `define/boundary-conditions/set/<type>` 一次设一个/多个同型 zone 的一项/多项设置：zone 名用括号列表或通配符（如 `(rotor-blade-*)`）；按 Enter 列出可用设置项；**改完须按 q 退出命令，部分设置在退出后才生效**。多相流程差异见 p. 3070。

### 8.1.5–8.1.8 复制、CSV 导出、改名、非均匀分布

- **复制条件**（8.1.5）：右键 zone → Copy... → Copy Conditions 对话框，From zone → To zones（仅同类型）；**复制的是全部条件，不能只拷一部分（如只拷热条件）**；求解能量方程时**外部 wall 与内部（双面）wall 之间不能互拷**（热条件定义不同）。多相差异见 p. 3087。
- **Turbo CSV 导出**（8.1.6）：启用 Turbo Model 后右键边界 → Export CSV；导出的面网格 CSV 可导入 CFX-Pre/CFD-Post 作 user surface，或导入 System Coupling 做气动阻尼分析；也是 Fluent 读模态振型（p. 2037）的前置步骤。流程：Domain → Turbomachinery → Turbo Models 启用 → Export Mesh Zones 对话框选 zone → 可选 **Add Global Node Number**（帮助识别多表面共享节点，System Coupling 识别共享节点需要它）→ 命名（自动加 .csv）→ Export。TUI：`/define/turbo-model/export-boundary-mesh`。
- **改名**（8.1.7）：默认名 `<type>-<ID>`（如 pressure-inlet-7）；树中慢速双击直接改名，或 Edit... → Zone Name。**注意：非默认名在改类型时保留不动——自动改名只对默认名生效**。
- **非均匀分布**（8.1.8）：多数边界条件可用 profile 函数代替常数——外部 profile 文件（Profiles，p. 1616，未摄取）或 UDF。

### 8.1.9 参数体系（对自动化最相关）

- **用途**：对数值型 cell zone/BC 设置定义参数，形成参数化算例系列；Workbench 参数化研究/优化；或在 Fluent 内把同一值复用到同单位的不同边界；配合 Gradient-Based Optimizer（p. 4780）做多目标多工况几何优化。
- **入口**：任务页 Parameters... 按钮 → Parameters 对话框。**Input Parameters**：可经 Parameter Expression 对话框编辑（即创建对话框；**Workbench 下只能查看不能编辑**）；可删除未指派的参数；More → **Use in Scheme Procedure / Use in UDF**。**Output Parameters**：由既有 report/monitor 生成的单值（surface/volume/lift/drag 等 report definitions，p. 4361）；More 支持 Delete/Rename/Print to Console/Print All/Write.../Write All...。
- **创建**：设置字段旁下拉选 **New Input Parameter...**（real 与 profile 类型的量均可）→ Parameter Expression 对话框填 Name 与 Definition。**Important：输入参数表达式必须直接定义为带单位的常数——不能引用另一个表达式**。**Important：改变某量的单位会改变所有使用该量的输入参数的值**。参数自动命名 parameter_1、2、3…，**删除后默认名不复用**（删 parameter_2 再建新参数得 parameter_4）。
- **Scheme 过程挂接**（8.1.9.2.1）：Parameters 对话框 → More → Use in Scheme Procedure → Select 选参数 → 填 Scheme 过程名或以 lambda 开头的过程体（接收 real 实参）→ Define 注册。例：
  ```scheme
  (define my-funct
    (lambda (value)
      (ti-menu-load-string (format #f "/solve/set/under-relaxation/pressure ~g" value))))
  ```
  **Important：写 Scheme 过程应使用 `args->string` 辅助过程而不是双引号**；`` ` ``（重音符）引导的列表配合 `,value1` 插值、`_` 存当前 TUI 提示的默认值；**在对话框中输入过程体必须合并成单行**。Delete 只删除"用法"不删参数本身。
- **UDF 挂接**（8.1.9.2.2）：More → Use in UDF → Select/Define/Delete/**Print**（打印注册参数的 ID）；UDF C 函数中用 `RP_Get_Input_Parameter("real-4")` 宏按 ID 取值。
- **TUI**（8.1.9.2.3）：`/define/parameters/input-parameters/advance/use-in`（选 scheme-proc 或 udf-side，按提示给参数名、值、apply-function 名/过程体）；`delete`（通配符 `*` 一次删除全部自定义用法）；`list` 列出用法。

### 8.1.10–8.1.11 图形选区与操作条件

- **图形窗口选区**（8.1.10）：树中高亮边界 → 右键 Display / Display in / Add to 可视化确认边界位置；树的边界描述含 zone ID；图形窗口中右键多选面可打印信息（surface ID、zone ID、surface 组）、融合 zone、创建图形对象。
- **操作条件**（8.1.11）：Operating Conditions 对话框（操作压力、参考压力点、重力等）从 Cell Zone Conditions 或 Boundary Conditions 任务页进入（详见 Modeling Basic Fluid Flow，p. 1799，未摄取）；Periodic Conditions 对话框从 Boundary Conditions 任务页进入（详见 Periodic Flows，p. 1809，未摄取）。

- **保存与复用**（8.1.12，p. 1370）：cell zone/边界条件可存成文件供其他 case 复用（→ Reading and Writing Boundary Conditions，p. 991，见 [[Fluent 求解模式文件读写]]）。

## 8.2 Cell Zone Conditions（pp. 1370–1422：8.2.1–8.2.3；8.2.4–8.2.7 待摄取）

Cell zone 分 fluid 与 solid；**多孔区与 3D fan 按 fluid zone 处理**。

### 8.2.1 Fluid 条件

- Fluid zone = 求解全部激活方程的单元组。**唯一必填输入：流体材料**。多相：不在此指定材料，在相定义时选（p. 3122）；组分输运/燃烧：可选 mixture 或 fluid——mixture 材料必须与 Species Model 对话框一致，**不同材料类型的 fluid zone 不得相邻**。可选项：质量/动量/热量（温度）/湍流/组分/其他标量的源项或固定值、zone 运动、旋转轴（邻接旋转周期边界时必填）、Laminar Zone、DO 辐射参与。
- **Participates in Radiation 告诫**：一般不建议关闭（会得错误结果）；少数可关（多 fluid zone 中辐射可忽略的区，省时不影响结果）。
- **材料**（8.2.1.1.1）：Material Name 下拉（库来自 Create/Edit Materials）；Edit... 只显示所选材料属性。组分/多相时 Material Name 列表不出现。
- **Laminar Zone**（8.2.1.1.4）：在特定 fluid zone"关掉"湍流建模——适合已知层流区（如翼型转捩点两侧分区模拟转捩）。默认置零湍流黏度并关闭湍流生成项（湍流量仍被输运，但对混合/动量的影响被忽略）；`define/boundary-conditions/fluid` 回答"Set Turbulent Viscosity to zero within laminar zone?"为 no → 只关生成项、保留非零 μt。**适用于除 LES 外的所有湍流模型**。
- **反应机理**（8.2.1.1.5）：组分+反应时 Reaction 选项 + 机理下拉（p. 2484）。
- **旋转轴**（8.2.1.1.6）：MRF 在 Reference Frame 页、滑移网格在 Mesh Motion 页设 Rotation-Axis Direction/Origin。**同一 zone 同时有 frame motion 与 mesh motion 且邻接旋转周期边界时两轴必须同轴**，否则周期假设无效、告警且 mesh check 失败。cell zone 轴与相邻 wall/其他 zone 的轴相互独立。3D：轴 = 从 Origin 沿 Direction 的向量；2D 非轴对称：只填 Origin（轴为过该点的 z 向向量，z 垂直几何平面）；2D 轴对称：不定义轴——恒绕 x 轴、原点 (0,0)（轴符号按 7.2.1 约定与上下文补全）。
- **Zone 运动**（8.2.1.1.7）：Frame Motion（MRF，p. 1831）/ Mesh Motion（滑移，p. 1869）。**Relative To Cell Zone** 下拉：absolute（默认；无运动区时唯一选项）或相对某个主运动 zone（此时出现 Rotation-Axis Origin (Relative)；列表 = 所有绝对运动的活动 cell zone、不含当前区）。平移速度 X/Y/Z；转速可为常数或瞬态 profile（文件格式 p. 1575 或 DEFINE_TRANSIENT_PROFILE 宏），各分量可单独用 profile/UDF；复杂运动整体用 DEFINE_ZONE_MOTION。**Important：MRF ↔ 滑移网格切换用 Copy To Mesh Motion / Copy to Frame Motion 按钮**（拷贝轴、原点、速度分量与 DEFINE_ZONE_MOTION）——典型用途：稳态 MRF 解作瞬态滑移网格初场（叶轮机械）。流体区相对固体区有法向 zone 运动时，绝对速度公式下总换热率含压力功（只在流体侧，p. 4364）。
- **辐射**（8.2.1.1.8）：DO 模型的 Participates in Radiation（p. 2278）。

### 8.2.2 Solid 条件

- Solid zone = 不解流动方程的单元组：流体仿真中只解导热；内禀 FSI 中算位移与应力。材料实为流体也假定无对流。唯一必填：固体材料。可选项：体积热源、固定温度、zone 运动、旋转轴、DO 辐射参与。**注意：即使全域皆 solid，求解器迭代仍会访问流动/湍流方程——纯固体且流体属性不重要时应手动去激活这些方程以提速**。
- **旋转轴**（8.2.2.1.4）：邻接旋转周期边界且未定义 zone 运动时，在 Reference Frame 页设 Origin/Direction；轴向规则同 8.2.1.1.6。
- **Zone 运动**（8.2.2.1.5）三选项：**Frame Motion**（仅当固体不相对相邻固体运动）；**Solid Motion**（相对相邻固体运动时；Solid Motion 页；须同时在固-流耦合 wall 上定义速度 BC——固-固之间不需要；wall 速度可绝对或相对相邻流体；能量方程开启后对有显著对流换热的边界墙开 **Boundary Advection**，p. 1526）；**Mesh Motion**（滑移，无论是否相对运动）。同轴告诫同上；**唯一允许两轴不同的组合是 solid motion + frame motion**（例：盘式刹车——转子自转为 solid motion、总成绕竖轴转为 frame motion）。**Important：同时平移+旋转仅当旋转轴与平移方向一致（原点固定）**。切换按钮 Copy To Mesh Motion / Copy to Frame Motion；frame → solid motion 用 `mesh/modify-zones/convert-all-solid-mrf-to-solid-motion`（作用于所有开了 frame motion 的 solid zone；升级旧版设置用）。
- **速度须无散**：frame/solid motion 的速度必须与边界相切（法向分量 → 无法能量守恒）；唯一例外：同材料同运动的两固体区之间的耦合 wall 或网格界面。求解器首次在其他边界类型遇到显著法向分量会警告。合法/非法构型见 Figures 8.15–8.21（非法例：边界与运动不相切的旋转体；接触有 squish 的两固体——接触处法向分量致全局能量不守恒，温度场或仍可接受）。
- **限制**：运动效应只作用于能量方程与结构模型（UDS 不含运动）；不允许"固体入口/出口"（运动不能穿过邻接边界区，可给定温度 wall）；开动态光顺和/或 layering 的 zone 不得开 Solid Motion。

### 8.2.3 多孔介质条件（pp. 1383–1422）

- **定位**：填充床、滤纸、多孔板、分布器、管束等单相/多相问题；在 cell zone 上定义，压降由用户输入决定；可含传热（平衡/非平衡两模型）。**Porous jump** 是 1D 简化、加在 face zone 上，用于已知速度/压降特性的薄膜——**更稳健、收敛更好，能用就用**（p. 1571）。
- **8.2.3.1 限制与假设**：模型本质 = 动量方程加动量汇。默认**表观速度公式**（按体积流量计；保证多孔界面两侧速度连续；porosity 不进入对流/扩散项）；可选**物理速度公式**（真实速度；porosity 进入微分项；p. 1390）。多相各相共享同一 porosity；切换公式时 inlet 速度与初始化值须相应改。湍流影响只是近似。porosity 一般设为各向同性，可随空间和时间变化。多孔区内**始终使用专用压力插值格式**（与 Solution Methods 选择无关）。不考虑多孔介质与激波相互作用。MRF 下 Relative Velocity Resistance Formulation 保证源项正确（相对或绝对参考系）。**推荐 Standard Initialization**：默认 Hybrid Initialization 不考虑多孔属性，可能产生不真实初速场——多孔仿真只有勾选 Maintain Constant Velocity Magnitude 才能用 Hybrid。物理速度公式要求 porosity 为**空间常数**（空间变化 porosity 须用表观速度公式）。物理速度公式在阻力值（惯性或黏性）小于等于多孔界面动压变化时可能出非物理流场/收敛差——把多孔界面区改成 porous jump 边界可解。与 NETM 相关：重合固体区不支持 solid motion；NETM 不支持密度基求解器、几何/网格变化区（动网格/自适应/morpher/FSI）、辐射模型、多相模型、非预混燃烧；关闭 NETM 后自动建的固体区不会自动删除——需手动清除。
- **8.2.3.2 动量方程**：动量源 = 黏性损失（Darcy）+ 惯性损失两项（Eq 8.1，S_i = −(ΣD_ij·μ·v_j + ΣC_ij·½ρ|v|v_j)）；简单均匀多孔介质用对角阵 D = 1/α（渗透率）、C = C2（惯性阻力系数，Eq 8.2）。另有**幂律模型**（Eq 8.3，经验系数 C0、C1；**压降各向同性、C0 须 SI 单位**）。Darcy 适用层流（C2≈0，Eq 8.4–8.5，Δn 为模型中各区实际厚度——厚度不符时须调整输入）；高速时 C2 提供惯性损失（单位长度损失系数，按动压头计）；多孔板/管束可只用惯性项（Eq 8.6–8.7）。
- **8.2.3.3 相对黏度**：有效黏度（Eq 8.8）修正动量方程扩散项；三个子模型——Brinkman 修正（8.9）、Einstein 公式（8.10）、Breugem 关联式（8.11）（公式体未提取，见下证据边界）。
- **8.2.3.4 能量方程**：只修改导热通量与非稳态项。**平衡热模型**（默认，8.2.3.4.1）：有效导热系数 + 瞬态项含固体热惯性（8.12）；k_eff = γ·k_f + (1−γ)·k_s 体积平均（8.13；k_f 含湍流贡献）；k_f/k_s 及各向异性有效导热可用 UDF（各向异性时流体各向同性贡献加到固体各向异性矩阵对角）。**非平衡热模型 NETM**（8.2.3.4.2）：**dual cell**——与多孔流体区空间重合的固体区，只通过换热交互；流体/固体区各自独立求解能量方程（8.14/8.15），耦合项为 h_fs（换热系数）× A_fs（界面面积密度 = 界面面积/多孔区体积）× (T_f − T_s)。
- **8.2.3.5 湍流**：默认在多孔区照常解湍流方程（假定固体不影响生成/耗散——渗透率大、介质尺度与涡尺度不相互作用时合理）；要抑制湍流用 **Laminar Zone**（除 LES 外均可）。
- **8.2.3.6 porosity 对瞬态标量**：时间导数项变为 ∂(γφ)/∂t；瞬态自动启用，porosity 默认 1。
- **8.2.3.7 物理速度建模**：v_superficial = γ·v（8.16）；表观速度无法预测多孔区内增速、对速度值/梯度重要时精度不足。Cell Zone Conditions 任务页 Porous Formulation 选 **Physical Velocity**（默认 Superficial）。单相控制方程 8.17–8.19（8.19 末项 = 孔壁黏性+惯性阻力）。**Important：阻力系数输入仍按表观速度的经验关联式给出即可——Fluent 自动换算成物理速度公式兼容值**；进口质量流量按表观速度计——同质量流量+同阻力系数下两种公式压降相同；**porosity 效应不作用于用户自定义源项**（需要的话写进源项定义，对 Fluent 全部 UDF 源成立）。多相（8.2.3.7.2）：全域解物理速度；一般标量方程 8.20（porosity 可随时空变化）；适用于 Eulerian 多相全部输运方程；连续性 8.21、动量 8.22（含润湿相毛细压力项、相剪切应力、质量转移、绝对/相对渗透率、括号内多孔汇项、阻力/湍流扩散/升力/虚拟质量力；未启用毛细压力模型则 F_c=1）、能量 8.23。
- **8.2.3.8 用户输入（14 步）**：① Fluid 对话框勾 **Porous Zone**；②（可选）任务页 Porous Formulation 选速度公式；③ 流经流体材料（组分/多相无此列表）；④（如需）Reaction + 机理——**含壁面表面反应时须给 Surface-to-Volume Ratio**（m²/m³，催化剂负载度量；总反应面积 = 该值 × 单元体积 × porosity；多孔内壁面表面反应仅压力基求解器支持）；⑤ Relative Velocity Resistance Formulation（默认开；动网格/滑移/MRF 下用相对速度算源项，静止+运动多孔混合场景也适用；限制：轴对称带旋且旋向阻力非零时不支持；6.3 起支持动网格与幂律）；⑥ 黏性/惯性阻力系数 + 方向向量（或幂律 C0/C1）；⑦ porosity；⑧（可选）传热设置；⑨（可选）相对黏度模型；⑩（可选，仅 Eulerian）相对渗透率；⑪（可选）源项；⑫（可选）固定值；⑬ 抑制多孔区湍流黏度（Laminar Zone）；⑭ 旋转轴/zone 运动（同常规 fluid zone）。
- **阻力系数定义**（8.2.3.8.6）：Cartesian——2D 给 Direction-1、3D 给 Direction-1+2；D-1 = 主流方向，未给方向自动确定（2D：垂直于 D-1 与 z 所在平面；3D：垂直于 D-1×D-2 平面；**D-2 必须垂直于 D-1**，否则求解器会把 D-2 对 D-1 投影去除后正交化——务必先定准 D-1）。与全局轴不正交时用 plane tool（3D）/line tool（2D）：对齐工具后点 Update From Plane/Line Tool（红箭头 → D-1、绿箭头 → D-2；对应 Surface 对话框须打开）。系数可用 UDF（DEFINE_PROFILE）。轴对称带旋可加第三个切向分量（两种求解器均可）。3D 还可用**圆锥/圆柱坐标系**（Conical 选项 + Cone Half Angle，0 = 圆柱；Cone Axis Vector 单位向量 + 轴上一点；可用 Snap to Zone 自动吸附或 plane tool 对齐）与**曲线坐标系**（Direction Specification → Curvilinear Coordinate System → 选/新建 CCS，阻力方向分量对应 CCS 方向——衔接 7.5）。**Important：系数一般基于表观速度**。惯性阻力系数单位 = 长度倒数（Units 对话框 Quantities 选 resistance 可改）。**Alternative Formulation**（惯性阻力，高各向异性时更稳；压损取决于第 i 分量速度模长，8.24）：与默认式不等价、切换会有解差异；切换后须重跑才能得到一致的力报告与累计图（多孔力按需重算）；**仅压力基求解器兼容**。Conical 指定下 D-1 = 锥面切向、D-2 = 锥面法向（圆柱即径向）、D-3 = 周向。三类系数情形：各向同性（如海绵——各方向须显式设同值）；两同一异（平行流向的带孔圆管束/垂直流向的平板叠层）；三者全异（不规则针列）。
- **系数推导四法**：① **已知压降**（8.2.3.8.7）：多孔单元按 100% 开孔处理——实际开孔率 φ 设备的损失系数 K（基于孔内实速）须换算 K' = K/φ²（例：25% 开孔、K=0.5 → K'=8），再除以模型厚度得单位厚度惯性系数（1 mm 板 → C2 = 8/0.001 m = 8000 m⁻¹）；各向异性逐方向算。② **Ergun 方程**（8.2.3.8.8，填充床湍流，8.29；层流退化为 Blake-Kozeny 8.30；μ、平均粒径 D_p、床深 L、空隙率 γ）→ 对比 8.4/8.6 得各方向 α 与 C2（8.31/8.32）。③ **经验公式**（8.2.3.8.9，Van Winkle 等，方边孔三角排列多孔板湍流；特定 Re 与孔径/板厚比范围内系数 ρ≈0.98）→ 整理得法向 C2（8.36）。④ **表格数据**（8.2.3.8.10，玻璃纤维毡层流：固体体积分数 0.262/0.258/0.221/0.218/0.172 ↔ 无量纲渗透率 0.25/0.26/0.40/0.41/0.80）。另有**实验 Δp–v 数据法**（8.2.3.8.11）：拟合 Δp = a·v + b·v²（示例数据 20/50/80/110 m/s → 197.8/948.1/2102.5/3832.9 Pa），则 1/α = a/(μ·Δn)、C2 = b/(ρ·Δn)；**Important：拟合出现负系数要避免**；同法适用于 porous jump（得渗透率 α 与压降系数 C，对应式 8.152，p. 1571）。
- **幂律/porosity/传热**（8.2.3.8.12–14）：幂律只需 C0、C1（可与 Darcy/惯性模型并用）。**Porosity**：Fluid Porosity 字段，0–1；**NETM 不允许取 0 或 1**；UDF 用 DEFINE_PROFILE；porosity 用于传热预测、瞬态时间导数项，反应源项与体力按流体体积比例——γ=1（默认）= 完全开放。**传热**（不可压无黏流不可用）：平衡模型（默认）选 Equilibrium + 固体材料；非各向同性导热 UDF 用 DEFINE_PROPERTY。**NETM**：适用排气后处理 light-off、燃料电池、催化转化器等；步骤——先完成第 1–7 步并 **Apply 保存（否则启用 NETM 时设置被重置为默认）**→ Thermal Model 选 Non-Equilibrium → 若无重合固体区会弹窗自动创建：流体区不适合固体的边界（进出口等）自动转绝热 wall，其余（symmetry/wall 等）转同类型，流体墙的热 BC 复制到对应固体边界。也可事先手动复制固体区（`mesh/modify-zones/copy-cell-zones-by-offsets`）或读入时即含双区——要求：副本为 solid、边界转绝热 wall、**两区网格细化程度相近（单元质心一一映射）**。随后指定 **Interfacial Area Density 与 Heat Transfer Coefficient**（常数/表达式/参数/UDF DEFINE_PROFILE）；核查新固体区材料；核查两侧 wall BC 匹配。**Important：瞬态 + NETM + 低 porosity（<0.2）建议增大 Solid Time Step Size（约 1 s 或 Automatic，p. 2228）**。后处理：Temperature... 类的 Non-Equilibrium Thermal Model Source 变量；**等值面 From Zones 不可同时选多孔流体区与其重叠固体区（不选 = 全选，小心）**；Contours 中空间重合的两区面不可同选；导热系数报告值：流体区按 γ 缩放、固体区按 (1−γ) 缩放。
- **相对黏度/相对渗透率/毛细压力**（8.2.3.8.15–17）：相对黏度默认常数 1（有效黏度=分子黏度）；**多孔区多个时"最后一次输入的值作用于全部多孔区"**——各区不同有效黏度须在 Create/Edit Materials 里用 DEFINE_PROPERTY 直接定义材料 Viscosity。相对渗透率（仅 Eulerian）：Corey 幂律（8.42–8.44；润湿相曲线凹向上、非润湿相 S 形；水湿油水两相为典型场景）；或表格文本文件（p. 989）。设置：混合相 → Porous Zone 页 → Relative Permeability → Corey Model → 选 Wetting/Non-Wetting Phase → 每相设 Minimum Relative Permeability（默认 1.e-8；防饱和过冲/欠冲，欠冲顽固可再调低）、Reference Relative Permeability 与 Corey Exponent 与 Residual Saturation（后三者仅非表格法）→ Apply。饱和度偶仍低于残余值：`solve/set/multiphase-numerics/porous-media/relative-permeability` → "enable fix option below residual saturation?" yes（表格法不支持）。**毛细压力**（Eulerian 可选子模型）：P_c = P_n − P_w（8.45）；宏观上 P_c = f(S_w)（8.46）；作为润湿相动量方程的附加源项实现。五法：**Brooks-Corey**（8.47–8.48，初级排驱；S_wr 默认、须 >0.001 防无穷大；入口压力与孔隙尺寸指数默认值适配砂中气-水流动）、**Van-Genuchten**（8.49；入口压力 + 孔径分布参数 m=1−1/n；默认同适配砂中气-水）、**Leverett J-Function**（8.50–8.53；平均孔径由 porosity 与渗透率表达；Fluent 公式与 Fuel Cell Module 相同；参数：接触角 + Multiphase Model 对话框 Phase Interaction > Forces 的表面张力系数）、**Skjaeveland**（8.54；对两流体润湿性对称处理、兼顾排驱与吸吮；参数默认 9.e5/9.e5/0.05/0.05）、**Tabular**（文本表：第 1 行表名 ≤128 字符无空格、第 2 行列名如 Sw/Pc、其后数据行）。用法定值：混合相 Porous Zone 页选 Corey Model → Capillary Pressure 下拉选模型 → 设 **Maximum Capillary Pressure**（残余饱和度处曲线渐近 ±∞，必须限幅防数值问题）→ 各模型专有参数（BC/VG 在副相；Skjaeveland 在主副两相；Leverett 在副相给接触角 + 多相对话框给表面张力系数）；UDF 替代用 DEFINE_EXCHANGE_PROPERTY。**Note：润湿相应选为次相**。后处理：次相的 Capillary-Pressure 场变量（仅润湿相数值有意义）。**毛细压力作扩散**（8.2.3.8.17.7）：默认为动量源；两相可改为润湿相连续性方程中的扩散项（某些工况更稳健）；`solve/set/multiphase-numerics/porous-media/capillary-pressure-as-diffusion?` yes；此时次相必须是润湿相；且无论层流/湍流，毛细压力梯度只用黏性阻力计算。
- **源项/固定值等**（8.2.3.8.18–21）：多孔能量源**按输入值原样施加、不按 porosity 折算**（1 m³ 固体区给 100 W/m³ 就输出 100 W，即使固体只占 60%）；其余源项见 p. 1433；固定值见 p. 1429；抑制湍流黏度用 Laminar Zone；旋转轴与 zone 运动同常规 fluid zone。
- **8.2.3.9 求解策略**：流向压降大（α 低或 C2 大）时收敛变慢（动量汇破坏矩阵对角占优）——**最佳对策：给好多孔区两端压降的初场**。推荐 Standard Initialization（Hybrid 仅限 Maintain Constant Velocity Magnitude）。收敛差还可临时关掉 Porous Zone 选项当流体区算出初场再开（高阻力多孔不推荐此法）。**高各向异性收敛困难：把各向异性限制在 2–3 个数量级——阻塞方向阻力无须超过主流方向的 1000 倍**。NETM 案例：默认分区方法可能致收敛问题/解随处理器数变化——选不在导热系数/网格尺寸剧变区切分的分区方法（p. 4564）。**2022R1+ 注意**：多孔流动非一维、或多孔/非多孔区以非一致界面分隔时可能收敛困难——变通：控制台执行 Scheme `(rpsetvar 'pressure/porous-zone-presto-dissipation? #f)`。

- **8.2.3.9 尾注与 8.2.3.10 后处理**（p. 1423）：presto-dissipation Scheme 变通命令可解除压力插值格式的耦合，**但一般不推荐使用**。后处理看速度分量与静压力；热报告按 porosity 加权的导热系数定义（式 8.56）；**Important：体积/质量积分报告不折算 porosity 效应**；表面反应速率可用 Reactions... 类的 Arrhenius Rate of Reaction-n 显示；NETM 后处理须特别小心（p. 1406）。

### 8.2.4 3D Fan Zone（pp. 1423–1428）

- **定位**：以环形（叶片扫掠）流体体积中的**分布动量源**模拟轴流风机；对比 fan 边界（集总参数、无限薄、速度→压跃升）。优点：可算旋周与径向速度（fan 边界主要算轴向、需手给旋周/径向系数）；效果可比 MRF 而无需建三维叶片几何；风机曲线数据测试工况与仿真工况不一致时也能用。**不能有非一致界面**（与 7.6.3 一致）。
- **动量源**（8.2.4.1，式 8.57–8.62 体未提取）：轴向/切向/径向三方向源；切向源基于叶轮机械关系、径向源基于离心力平衡；涉及风机压升、环形区厚度、风机功率、局部半径、运行角速度、轮毂/拐点/叶尖半径、密度、局部切向速度与拐点比（inflection point ratio = 自轮毂起切向速度随半径上升至峰值再回落的叶长分数）。压升按体积流量给定：常数、多项式（8.63，系数由 Fluent 拟合）或分段线性风机曲线。**Important：体积流量可正可负——建模须保证正向流动产生压升**。风机曲线可按测试工况缩放到仿真工况（8.64–8.66，测试温度 vs 风机区体平均温度、角速度缩放）。
- **用户输入**（8.2.4.2）：cell zone 须为**环形**、尺寸匹配叶片扫掠体积（内外半径 = 毂/叶尖半径，轴向长度 = 环形厚度），且为"内部"区——至少两个 interior 型边界与另一流体区相邻、充当风机进出口。Fluid 对话框勾 **3D Fan Zone** → 3D Fan Zone 页。Geometry：① Inlet Fan Zone（须 interior 型、平面、介于 3D fan zone 与另一流体区之间；**风向为垂直该边界吹入 3D fan zone**）；② Hub Radius / Tip Radius / Thickness（自 Inlet Fan Zone 向区内量）；③ Inflection Point Ratio（实验经验取值，或先用 MRF 算真实风机几何再反推）；④ Fan Origin（在 Inlet Fan Zone 平面上、风机直径落在其边界内）。Properties：① Rotational Direction（相对风机方向向量按右手定则为正）；② Operating Angular Velocity（正非零）；③ 可选 Limit Flow Rate Through Fan（最大/最小流量）；④ 可选 Tangential/Radial/Axial Source Term（切向+径向按叶轮理论自动、无需额外输入）；⑤ 轴向源 Method：**constant pressure**（全区恒压跃升）或 **fan curve**（Read Fan Curve... 读制表符分隔 ASCII，p. 5938；拟合选 polynomial〔给阶数〕或 piecewise-linear；给 Initial Flow Rate 估计、Test Angular Velocity、Test Temperature；一个文件可含多个 cell zone 但须在各 Fluid 对话框分别读入）。
- **限制**（8.2.4.3）：不支持预混燃烧模型；不支持 Eulerian 多相模型；**轴向源选 fan curve 时必须开启能量方程**。

### 8.2.5 固定变量值（pp. 1429–1433）

- **机制**：在 fluid/solid zone 内固定一个/多个变量的值 = 给单元内变量设"内部边界条件"；被固定的单元**不解该变量输运方程、不计入残差和**，固定值用于与邻单元的面通量计算 → 与邻值平滑过渡。**Important：温度、组分质量分数、速度分量只能用压力基求解器固定**。
- **用途**（8.2.5.1）：搅拌槽流动——叶轮出口区固定实验测量速度，替代滑移网格/MRF（不必关心叶片附近流场细节时）。
- **可固定变量**（8.2.5.1.1）：速度分量（仅压力基）、湍流量、温度（仅压力基；解能量方程时 fluid 或 solid 区）、焓（非预混燃烧、fluid 区）、组分质量分数（仅压力基；**除最后定义的组分外逐个可固定**）、UDS。Eulerian 多相可按相固定速度与湍流量（p. 3081）。
- **流程**（8.2.5.2）：Fluid/Solid 对话框勾 Fixed Values → Fixed Values 页；常数选 constant、非常数用 profile（p. 1616）或 UDF；**径向型 profile 的局部坐标系由该区的 Rotation-Axis Origin/Direction 定义**（对非旋转区指定轴不会使其旋转）。湍流量按模型给 k/ε/ω/修正黏度/雷诺应力分量（单位 m²/s²、m²/s³、1/s 等；**雷诺应力不能给径向型 profile**）。**Important：全部速度分量都被固定时，该区所有单元的表压被置零**。

### 8.2.6 锁定固体/壳温度（p. 1433）

- 对 solid zone（含用 UDF 加了能量源的单元）与开 shell conduction 的 wall 可"冻结"温度。`solve/set/lock-solid-temperature?`。**与固定值的区别：输运方程仍求解、单元仍计入残差和**。限制：仅能量开启 + 压力基时可用；Advanced Solution Controls 的 BCGSTAB 稳定化不支持此选项；能量收敛监控可能需要改用其他手段。

### 8.2.7 源项（pp. 1433–1438）

- **定位**：在 fluid zone 加体积源（质量/动量/能量/湍流/标量）或在 solid zone 加能量源，用于已知常值（函数依赖用 UDF）。**要给某些单元加源，须把这些单元放入单独的 zone**。典型用途：小于一个单元的"微型进口"（把该单元单独成区，按单元体积折算给定质量源与动量源——正文注明 V 为单元体积）、未显式建模的火源热释放、CHT 的固体能量源、未建模反应的组分源（如烟雾）。
- **Important（质量源守恒）**：输运方程为守恒形式——连续方程加了质量源后，**其他方程（动量/能量/组分）必须有对应源，且不会被自动添加**，须按加入/移除流体的属性（速度、温度、组分等）手动补齐；能量源注意焓值定义。
- **符号与单位**（8.2.7.1）：正 = 源、负 = 汇；一律 SI。
- **流程**（8.2.7.2）：Source Terms 选项 → Source Terms 页 → 各类 Edit... 定义源个数；每源 none/constant/New Input Parameter...；**不建议只给质量源而不给其他配套源**；源为**单位体积**量——先用 Volume Integrals 对话框确定目标区体积再折算。
- **各类源**：质量（单组分给 Mass；多组分给总量 + 除末组分外逐个给，末组分 = 总量 − 其余之和；示例 h2 0.01、o2 0.02、末组分 N2 0.015 → Mass 填 0.045；单位 kg/m³-s；**注意：连续方程加质量源时会自动在能量方程加对应源，参考温度 0 K（无黏）/298.15 K（黏性）**）；动量 N/m³；能量 W/m³；湍流按模型给 k/ε/ω/修正黏度/雷诺应力分量源；平均混合分数及其方差（非预混，含双混合分数的二次对）；P-1 辐射源（W/m³；**若代表内能↔辐射能转移（吸收/发射），须同时给等量反号的 Energy 源**以保能量守恒）；进展变量源（预混）；NOx 的 no/hcn/nh3 源；种群平衡 Bin-i-fraction 源（0 到 N−1 编号）；UDS 源（p. 1801）。

## 8.3 操作条件（pp. 1438–1442）

- **浮力驱动流/自然对流**（8.3.1）：重力作用于密度变化引起；温致即自然对流。
- **封闭域**（8.3.1.1）：解依赖域内质量——两条路：①**瞬态**（初始密度由初始 p、T 算出、质量守恒；**温差大时必须用此法**）；②稳态 + Boussinesq（密度取常数、质量已知；仅小温差适用）。**Important：封闭域的不可压理想气体律只能配固定操作压力（不能浮动）；可压理想/真实气体律两者皆可**（浮动操作压力见 p. 1825）。
- **Boussinesq 模型**（8.3.1.2）：除动量方程浮力项外密度取常数（8.67：ρ = ρ0[1−β(T−T0)]）；β(T−T0) ≪ 1 时近似成立；比显式温度函数密度收敛更快。**限制**（8.3.1.3）：大温差不可用；**不能用于组分计算、燃烧与反应流**。
- **求解步骤**（8.3.1.4）：① 开能量方程（Setup → Models → Energy → On）。② Operating Conditions 对话框：开 Gravity + 各方向重力加速度（默认零）；不可压理想气体律核查 Operating Pressure 非零；非 Boussinesq——按需定义操作密度（单相开 Specified Operating Density；**可压理想/真实气体 + 浮力时 Operating Density 填 0**；多相默认最小相平均法、可改用户输入，p. 3042），再把流体密度定义为温度函数（p. 1670/1678）；Boussinesq——填 Operating Temperature T0、材料 Density 下拉选 boussinesq 给常数值、给热膨胀系数 β（多种流体材料可逐材料决定是否用 Boussinesq，此时上述参数全要设）。③ 边界条件：压力进出口给的是**重定义压力**（8.68）；无外部压差时进出口应给相等压力。④ 求解设置：压力基推荐 **PRESTO!** 压力离散；必要时加密壁面边界层。
- **操作密度**（8.3.1.5）：非 Boussinesq 时体力项含 (ρ−ρ0)g；压力重定义（8.68）与静水压（8.69）。单相默认按全体单元平均求 ρ0；**自然对流 + 压力边界时建议显式指定**（边界给的是重定义压力 p'_s，需 ρ0 才能换算真实压力 p_s），取域特征温度下的近似平均密度即可（有时只为改善收敛）。所有材料都用 Boussinesq 时 ρ0 不出现、无须指定。多相见 p. 3042。
- **求解策略**（8.3.1.6）：高 Rayleigh 数参考 p. 2225 的换热策略；**某些层流高 Rayleigh 数流动不存在稳态解**（本节是否延续到 p. 1443 由批次 42 核对）。

- **高 Rayleigh 数策略**（8.3.1.6.1，p. 1443）：稳态法——把重力加速度调低两个量级（如 9.8→0.098）降低有效 Rayleigh 数、一阶格式收敛后，其 data 作高 Ra 初场、一阶收敛后再升高阶格式。瞬态法（引 [64]）——从同/低 Ra 稳态解起步；时间常数 τ = L/V（8.70），时间步 Δt ≤ τ（8.71，更大可能发散）；振荡频率约 0.05–0.09/τ 的振荡衰减后达稳态；可能需多达 5000 时间步。

## 8.4 边界条件（pp. 1443 起；本页覆盖开头与 8.4.1–8.4.9）

- 边界分 external、internal、periodic 三类，22 个小节；interface 区见 p. 1868、interior 区见 p. 5233、overset 区见 p. 1250、RANS/LES interface 区见 p. 2182。Boundary Conditions 分支默认按类型分组，可改 List View（字母）/Name/Adjacency（按 cell zone）；默认值在 Preferences → Appearance 的 Group boundary conditions by 设置。

### 8.4.1–8.4.2 流动进出口总览与湍流入口参数

- **12 类进出口边界**（8.4.2）：velocity inlet（速度+标量）；pressure inlet（总压+标量；压降未知/浮力驱动/外流自由边界）；mass-flow inlet（**可压流动**用；不可压无需——密度常数时速度入口即固定质量流）；pressure outlet（出口静压+回流标量；**有回流时比 outflow 收敛更好**）；pressure far-field（无穷远自由来流，给定 Mach 与静条件；**仅可压**）；outflow（出口速度/压力事先未知、出口接近充分发展；除压力外所有变量零流向梯度；**不可压不用 outflow？——原文：不适合可压计算**）；inlet vent（损失系数+方向+环境总温总压）；intake fan（压跃升+方向+环境总温总压）；outlet vent（损失系数+环境静温静压）；exhaust fan（压跃升+环境静压）；degassing（分散气泡逸出、液相不逃逸的自由面；**仅 Eulerian 两相液-气**）。
- **入口湍流参数**（8.4.2.1，对所有进出口型边界通用）：
  - **profile 法**（要精确表示入口边界层/充分发展湍流时）：SA 选 Modified Turbulent Viscosity 或 Turbulent Viscosity Ratio；k-ε 选 K and Epsilon；k-ω 选 K and Omega；ε 系 RSM 选 K and Epsilon + Reynolds-Stress Components；ω 系 RSM 选 K and Omega + 分量。
  - **均匀值法**：多数剪切层内生成的湍流远多于入口带入，结果对入口值相对不敏感——但外部流自由流有效黏度过大会"淹没"边界层，须防不物理值。默认 specification method：SA 用 Turbulent Viscosity Ratio；k-ε/k-ω/RSM 用 Intensity and Viscosity Ratio。
  - **湍流强度 I**：u_rms/u_avg；≤1% 低、>10% 高（低湍流风洞可低至 0.05%）；充分发展管流核心按 Blasius 系经验式（8.72；Re 50,000 → I≈4%）；**默认 5%（中等）**。
  - **湍流长度尺度 ℓ**：充分发展管流 ℓ ≈ 0.07L（L 为管道特征尺寸、非圆截面用水力直径；0.07 来自充分发展管流最大混合长度）；湍流源自障碍物（多孔板等）时用障碍物特征尺寸。取法指引：充分发展内流 → Intensity and Hydraulic Diameter（给水力直径）；叶栅/多孔板下游 → Intensity and Length Scale（给开口特征尺寸）；含湍流边界层的壁面约束进口 → Intensity and Length Scale，ℓ 由边界层厚度 δ 计算（换算式未提取）。**注意 0.07L 只是近似，非普适**。
  - **湍流黏度比 μt/μ**：正比于湍流雷诺数；高 Re 边界层/剪切层/充分发展管流中约 100–1000；外部流自由流通常很小；内流可取到 100；**默认 10**。
  - **换算关系**（8.74–8.82，公式体未提取、文字已描述）：ν̃ 由 I 与 ℓ 估算（8.74；假定无黏性阻尼；SA + Intensity and Hydraulic Diameter 时 Fluent 内部即用此式；Cμ=0.09）；k = (3/2)(ūI)²（8.75）；ε 由 ℓ（8.76）；ε 由 μt/μ（8.77）；衰减湍流的 ε 估法（8.78，风洞丝网下游；须用 8.77 复查 μt/μ 不过大）；ω 由 ℓ（8.79）；ω 由 μt/μ（8.80）；RSM 雷诺应力未显式给时由 k 各向同性近似（8.81–8.82；选 K 或 Turbulence Intensity 时启用）。
  - **Important（参考系）**：8.75 中的平均速度取 General 任务页所选 Velocity Formulation；入口速度先换算到所选参考系再算 k；入口不需要速度的边界（如压力入口）用当前局部解速度模长。MRF 下注意入口速度与湍流量换算次序（影响 8.74 的 ν̃）。
  - **SRS 入口湍流**（8.4.2.1.15）：SAS/DES/SDES/SBES/LES 可在速度/压力入口给非定常 Fluctuating Velocity 生成真实湍流内容——须选 Fluctuating Velocity Algorithm 及参数；即使某些 LES 不需要边界湍流参数，选了该算法也必须给。
- **通用要点（多类入口共享）**：Supersonic/Initial Gauge Pressure = 静压，仅超音速进口或按该边界初始化时使用（亚音速被忽略、由滞止量算出；初始化时配合滞止压力按等熵关系/Bernoulli 给初值；亚音速进口应按估计 Mach 数/速度合理设置）；压力值均相对操作压力；开重力后压力输入**不含静水压差**（重定义压力 p'_s，见 8.3），静压/总压报告也不显示静水压影响；常密度流体取 ρ0=流体密度可消去体力项、变密度取平均代表值；方向向量无须单位化（自动归一）；圆柱坐标系（Cartesian/Cylindrical/Local Cylindrical/Local Cylindrical Swirl）正方向：径向离轴为正、轴向沿轴向量为正、切向按右手定则；**Local Cylindrical Swirl 不用于明渠边界与混合面边界**，且建议从小旋周速度起步渐增以稳住解。回流防止选项（Prevent Reverse Flow，压力入口/压力出口均有）：在边界面上竖人工墙阻止出/回流，恢复顺压梯度后自动移除（控制台打印面数与面积占比）；**多相不可用**。温度语义（压力/质量流入口共通）：不可压 → 给的 T 按静温处理；Mixture 多相：可压+不可压混合进入 → 静温、仅可压相进入 → 总温（随 Reference Frame）；VOF：可压相进入 → 总温，否则静温；Eulerian：逐相按可压/不可压取总温/静温。

### 8.4.3 压力入口（pp. 1452–1462）

- **用途**：进口总压已知而流量/速度未知；浮力驱动流；外流"自由"边界。可压/不可压均可。
- **输入**：Reference Frame；Gauge Total Pressure；Total Temperature（Thermal 页）；流动方向；Supersonic/Initial Gauge Pressure；湍流/辐射/组分/混合分数/进展变量/DPM/多相/明渠/声学参数。
- **总压定义**：不可压 p0 = p_s + ½ρv²（8.88，轴对称带旋时 v² 含旋周分量）；可压等熵关系（8.89，γ 为比热比）。总温/总压/方向的参考系按对话框 Reference Frame（压力基随 Absolute velocity formulation 取绝对/相对；**密度基恒绝对**）。Eulerian 多相：总温与速度分量逐相给、各相 Reference Frame 同混合相、**总压只在混合相给**。
- **默认值**（8.4.3.2，SI）：总压 0；Supersonic/Initial Gauge Pressure 0；总温 300 K；方向 Normal to Boundary；I 5%；μt/μ 10。
- **计算程序**（8.4.3.3）：入口 = 从滞止条件无损失过渡——不可压用 Bernoulli（8.92）；可压用理想气体等熵关系（8.93–8.96：p0 与单元静压关系、声速、理想气体密度、由总温求静温）；**流出时总压作静压用、总温=静温**；多组分气体常数 R 由入口组分分数算。

### 8.4.4 速度入口（pp. 1462–1467）

- **用途**：给定进口速度+标量；总压浮动。可压/不可压均可。**Important：可压内流全堵塞无泄流路径时不要用（数值不稳定）——改压力入口或避免堵塞工况（高速超音/跨音）**。特殊用法：出口处也可用速度入口给定流量（标量输入不使用；**必须自行保证全域质量守恒**）。
- **速度定义**（8.4.4.1.2–8.4.4.1.6）：Magnitude and Direction / Components / Magnitude, Normal to Boundary 三法；Reference Frame 选 Relative to Adjacent Cell Zone 或 Absolute（邻区不动则等价）；3D 坐标系 Cartesian/Cylindrical/Local Cylindrical；**方向分量正负号规则：负向进入须给负值**；角速度 ω 可与 Swirl/Tangential Velocity 并给——**两者相加**（每面 v_θ = ω·r，r 为到轴原点距离）。
- **温度**：Thermal 页 Temperature = **静温**。**Outflow Gauge Pressure**：仅密度基——出口面按该压力的压力出口处理。
- **默认值**（8.4.4.2）：温度 300 K；速度 0；方向分量 (1,0,0)；I 5%；μt/μ 10；Outflow Gauge Pressure 0。
- **计算程序**（8.4.4.3）：进口——质量流量 = ρ·v·A·法向分量（8.97），动量/能量/组分通量随之；出口——压力基按边界速度算通量、所有方程对流项迎风取上游单元值；密度基出口面按 Outflow Gauge Pressure 的压力出口处理；密度为常数或按 T/p/组分分数计算。

### 8.4.5 质量流入口（pp. 1468–1476）

- **用途**：给定质量流量/质量通量分布；总压随内场浮动（对比压力入口的总压固定、质量流浮动）。可压/不可压均可；**可压内流全堵塞时同样不要用**。典型：小冷却射流按定质量流入射。也可作出口（方向背离域）。
- **限制**（8.4.5.1）：总压自调可能拖慢收敛——两法都可行时优先压力入口；不可压流直接用速度入口。
- **质量流指定**（8.4.5.2.3）：Mass Flow Rate（默认）/ Mass Flux / Mass Flux with Average Mass Flux（主要为混合面模型）。UDF/瞬态 profile **只能给时间变化**（须瞬态求解器；该挂接不支持空间变化）。**轴对称注意：质量流量按整个 2π 弧域给；质量通量按 1 弧度切片给**。Average Mass Flux 语义：保持 profile 形状、缩放数值使积分流量等于平均值（例：profile 积分 4.7、想要 5 → 平均质量流填 5）。混合面：保留默认 Mass Flow Rate=1 即可，建混合面时 Fluent 自动切换为 Mass Flux with Average Mass Flux 并用上游区积分值。
- **总温**：绝对或相对（随 Reference Frame）；Eulerian 逐相给总温与质量流分量、参考系只在混合相设。温度语义同压力入口。
- **方向**：默认 Normal to Boundary；**轴对称带旋选 Normal to Boundary 时边界无旋周分量**。
- **默认值**（8.4.5.3）：Mass Flow Rate 1 kg/s；总温 300 K；Supersonic/Initial Gauge Pressure 0；方向 (1,0,0)；I 5%；μt/μ 10。
- **计算程序**（8.4.5.4）：每面速度逐迭代调整以维持质量流；ṁ → 均匀通量 ṁ/A（8.98）；理想气体 ρ = p_s/(RT_s)（8.99；超音速用 BC 静压、亚音速由内场外推），静温由总焓（8.100）解出；不可压 T_s=T_0、ρ 由温度/组分定；各变量通量用通量速度与入口值。

### 8.4.6 质量流出口（pp. 1476–1480）

- **用途**：按给定质量流把流体"泵"出域（默认 0）；适合"匹配质量流比匹配出口静压更重要"的场合。**严格只用于纯流出**——禁止混合进出/流向反转工况。
- **限制**：密度基 Wet Steam 模型不支持；Eulerian 多相仅当**只有一个相**在该边界离开时可用，否则结果可能不准。
- **输入**：Mass Flow Rate / Mass Flux / Mass Flux with Average Mass Flux / **Exit Corrected Mass Flow Rate**（仅理想/真实气体材料）+ ECMF Reference Temperature 与 ECMF Reference Gauge Pressure；辐射；DPM。**Reference Frame 仅支持 Relative to Adjacent Cell Zone**。UDF/瞬态 profile 只能给时间变化（瞬态求解器）。轴对称：流量按 2π 全域、通量按 1 弧度切片。默认按"保持出口流量 profile"的方式让边界通量浮动——**要恒定质量通量：`define/boundary-conditions/bc-settings/mass-flow` 对 "preserve profile while flow leaves" 回答 no**。
- **Exit Corrected Mass Flow Rate**（8.4.6.3.1）：把质量流换算到出口总条件、维持恒定修正流量——面向叶轮机械，可从堵塞到失速扫掠整机工作范围；最佳效率点左侧行为似质量流出口、右侧直到堵塞似压力出口。ECMF（8.102）= ṁ·√(T_ref/T0)·(p0/p_ref)；p0、T0 为出口绝对系质量平均总压/总温；参考条件为常数（通常取进口总温总压；其选择不影响数值行为、只给无量纲流量以量纲意义）；**ṁ ∝ p0/√T0**（∝ 1/滞止声速）。初值可由收敛的标准进出口算例换算，再上下调整扫速线。
- **计算程序**（8.4.6.3）：指定流量 → 内部换算为均匀通量（8.101）；profile 保持模式下用"指定/计算质量流"比例缩放边界面法向速度、其余速度分量与压力/温度/组分等从相邻单元中心外推。

### 8.4.7–8.4.8 进口通风口与吸气风扇（pp. 1480–1485）

- **Inlet vent**（8.4.7）：前 12 项与压力入口相同；额外给**损失系数 K**——通风口视为无限薄，Δp = K·½ρv_n²（8.103，v_n 为法向速度）；**Important：压降沿流动方向取——即使回流也表现为阻力**。K 可为常数/多项式/分段线性/分段多项式（法向速度的函数；对话框同温度依赖属性）。
- **Intake fan**（8.4.8）：前 12 项同压力入口；额外给**压力跃升**（法向速度的函数，同类函数选项）。**Note：只考虑动量、不考虑扩散**。回流时按损失系数 = 1 的出口通风口处理。

### 8.4.9 压力出口（pp. 1485–1494）

- **机制**：给出口静（表）压——**仅亚音速时使用**；局部超音速则压力与所有其他量从内场外推；亚/超音速默认按局部法向速度分量判定。**必须同时给一套回流条件**（即便收敛解无回流也应给真实值，以减少万一回流时的收敛困难）。
- **输入**：Gauge Pressure；**Pressure Profile Multiplier**（Gauge Pressure 的常数缩放因子——主要为 profile/UDF 非均匀出口压力设计，如叶轮机械不同流量下性能图谱换算；对常数也生效；与其他选项联动一致，如径向平衡时缩放后的压力作用于参考位置）；回流条件（Backflow Total Temperature；**Backflow Pressure Specification**：Total Pressure——Gauge Pressure 加上基于相邻 cell zone 速度的动压分量 / Static Pressure——Gauge Pressure 直接作为边界面压力；**Backflow Direction Specification Method**：Normal to Boundary（默认）/ Direction Vector（3D 含坐标系下拉）/ From Neighboring Cell；回流湍流/组分/混合分数/进展变量/多相；**Backflow Reference Frame——多相与声学波模型下不可用**；密度基恒绝对）；辐射；DPM；明渠；**Radial Equilibrium Pressure Distribution**；**Average Pressure Specification**（多相不可用）；**Target Mass Flow Rate**（多相不可用）；声学波模型。
- **径向平衡出口**：叶轮机械出口流；参考位置 Reference Position 默认 **Minimum Radius**（相对旋转轴），可选 Maximum/Specified Radius/Specified Span；其余区域按径向速度可忽略假设 dp/dr = ρv_θ²/r（8.104）积分，边界划分为径向周向"bins"，bin 数经 `/define/boundary-conditions/bc-settings/pressure-outlet` 修改；旋转速度为零也可用（含导叶的环腔）；**仅 3D 与轴对称带旋**。
- **平均压力规格**（8.4.9.3.1）：出口压力沿边界可变但均值≈给定值；比均匀规格轻微降低边界反射率。两种实现：**Strong Averaging**（两种求解器都有；压力基的实现即同 strong；面压 = 内场平均压力与指定出口压按混合因子 α 混合，8.105，α=1 全平均、α=0 全指定；profile 指定时按径向/轴向"bins"分别平均；混合因子与 bin 数经同一 TUI 改）与 **Weak Averaging**（仅密度基、主要为遗留算例保留；面压为左右态加权、按出口面法向 Mach 数的五阶多项式混合 [93]；不可压为指定压力与内压的平均，8.106）。**Note：声学波模型激活时不提供该选项；非定常仿真使用可能产生非物理压力反馈——不推荐**。
- **回流发生时**：① 压力按 Backflow Pressure Specification 处理；② 方向按 Backflow Direction Specification；③ 总温/总压/方向按 Backflow Reference Frame 取绝对/相对（压力基随 Absolute velocity formulation；密度基恒绝对）。
- **默认值**（8.4.9.2）：Gauge Pressure 0；Pressure Profile Multiplier 1；Backflow Total Temperature 300 K；Backflow I 5%；Backflow μt/μ 10。
- **Target Mass Flow Rate**（8.4.9.4.2）：每迭代按 Bernoulli 调整出口压力以逼近目标流量（8.107，含当前/所需流量、平均密度、面积）。**限制**：多相与任何 NRBC 不可用；该 zone 用于混合面时不可用；**流动堵塞（边界 Mach=1）时达不到目标**；域内多孔大压降时可能达不到。设置：对话框勾选 + 给目标流量（常数或 UDF）；`define/boundary-conditions/target-mass-flow-rate-settings` 设欠松弛因子（默认 0.05）与 verbosity（默认 no；打印所需/计算流量、平均压力、新施加压力、Δp）；再在对话框给 **Upper/Lower Limit of Absolute Pressure**（多出口且压力差异大时改善收敛；也可经 `define/boundary-conditions/pressure-outlet`）。非反射边界选项见 p. 1590。

- **目标质量流补充**（p. 1495，8.4.9 收尾）：收敛困难时先调低欠松弛因子；或先关掉目标质量流、猜一个使解接近目标的出口压力，稳定后再开该选项迭代收敛（复杂问题常很有效）；FMG 初始化也有帮助（p. 3771）。非定常问题用 DEFINE_PROFILE UDF 挂目标质量流（profile 是时间的函数；同一时刻全区只有一个常值）。

### 8.4.10 压力远场（pp. 1495–1499）

- **用途**：无穷远自由来流（给定 Mach 数与静条件）；即"特征边界条件"——用 Riemann 不变量确定边界流动变量。
- **限制**：**仅限理想气体律密度**；边界须离物体足够远（升力翼型常见远场圆半径 20 倍弦长）；与压力基多相模型（VOF/Mixture/Eulerian）不兼容；不可用于常密度、真实气体、湿蒸汽（密度基）。
- **输入**：静压（表压）、Mach 数（亚/跨/超音速均可）、温度、方向（3D 可 Cartesian/Cylindrical/Local Cylindrical；Cylindrical 的轴参数取相邻 cell zone）、湍流/辐射/组分/DPM。**无多相与声学项**。
- **默认值**（8.4.10.4）：静压 0；Mach 0.6；温度 300 K；方向 (1,0,0)；I 5%；μt/μ 10。
- **计算程序**（8.4.10.5）：基于一维法向流的 Riemann 不变量的**无反射**边界；亚音速有两个不变量（8.108–8.109，v_n 与 c 的进出组合，8.110–8.111 给出边界法向速度与声速）；流出面：切向速度与熵从内场外推；流入面：取自由流值；再算出面密度/速度/温度/压力。
- **Flux-based 压力远场**（密度基替代法）：用 Riemann 求解器算远场边界的数值通量——精度/稳健性与内部面相同；是切向修正的"全局化"，**边界层或尾迹延伸出计算域时更有利**；`/define/boundary-condition/bc-settings/pressure-far-field/type?` 输 1 选 Flux-based。**切向修正**：与自由流方向相切的边界面妨碍稳健性——密度基默认用数值通量求值局部替代标准 Riemann 不变量处理；默认开启，`.../riemann-invariants-tangency-correction?` 可关。

### 8.4.11 Outflow 出口（pp. 1499–1503）

- **机制**：出口速度/压力事先未知；不定义任何条件（辐射/DPM/分流除外），全部由内场外推；处理 = 所有流动变量零扩散通量 + 整体质量平衡修正；出口面外推与充分发展假设一致（出口无面积变化时）；**横向梯度可以存在——只有垂直于出口面的扩散通量假定为零**。
- **Important（不可用情形）**：含压力入口的问题（改用压力出口）；**可压流动**；密度随时间变化的非定常流（即使流体不可压也更宜压力出口）。Eulerian/Mixture 多相的不可压一般可用——但出口可能出现回流或出口流场不充分发展时优先压力出口。
- **位置选择**：放在充分发展区（示例位置 C）严格满足；再附着点附近（位置 B）病态（法向梯度大）；**被吸入通过 outflow（位置 A）病态**——通常不收敛、结果无效（域内质量流"悬空"；流入标量无定义，温度取自相邻流体）。**Important：计算过程中任一时刻经 outflow 的回流都会影响收敛，即使最终解无回流——湍流尤甚**。
- **质量流分流**（8.4.11.3）：多个 outflow 用 Flow Rate Weighting 按权重比例分流（8.112：份额 = 权重/权重总和）；默认全 1 = 平分；要 75/25 就显式给 0.75 与 0.25——**Important：给 0.75 而另一个留默认 1.0，会得到 42.9%/57.1%（按权重归一）**。
- **其他输入**：辐射模型（P-1/DTRM/DO/S2S/MC）给 Internal Emissivity（默认 1）与（可选）External Black Body Temperature Method（默认 300）；DPM 去向。

### 8.4.12–8.4.14 出口通风口、排气风扇、Degassing（pp. 1503–1508）

- **Outlet vent**（8.4.12）：前 4 项（静压、回流条件、辐射、DPM）同压力出口；额外**损失系数 K**——无限薄，Δp = K·½ρv_n²（8.113）；**压降沿流动方向取，回流时也表现为阻力**；K 可为常数/多项式/分段线性/分段多项式（法向速度函数）。
- **Exhaust fan**（8.4.13）：静压 + 回流条件 + 辐射 + DPM + UDS 回流 + **压力跃升**（局部法向速度的函数，同类函数选项）；只考虑动量、不考虑扩散；**Important：建模须保证正向流产生压升；回流时按损失系数 = 1 的进口通风口处理**。
- **Degassing**（8.4.14）：允许分散气泡逸出、连续相（液）不出域的自由面。液相视边界为**自由滑移壁**、气相视为出口；不指定出口压力——Fluent 自动在相邻单元对气相加**质量汇**（按单元中心的边界法向通量计算）。**限制**：仅 Eulerian 液-气两相（**主相必须为液**）；**必须开重力**才能让气体逃逸；只推荐用于不含 freeboard 的鼓泡塔类场景；后处理两相均无法向速度（气体逃逸建模为邻单元质量汇）。**无输入**；但气相体积分数初始条件须设为非零且小于稳态气含率。

### 8.4.15 Wall 边界条件（pp. 1508–1534）

- **总则**：束缚流体/固体区域；黏性流默认 no-slip；可给切向速度（平移/旋转）或以剪切实现在"滑移"壁（零剪切也可用 symmetry 类型，但 symmetry 会作用于所有方程）。剪切应力与换热由局部流场计算。输入：粗糙度（湍流可选）、壁面运动、剪切条件、热、组分/表面反应、辐射、DPM、VOF 接触角、FSI 位移。
- **粗糙度**（8.4.15.3）：经修正的标准壁面律；或**结冰附加粗糙度模型**（仅 SA 与 SST k-ω；Momentum 页 Wall Roughness → Roughness Models → High Roughness (Icing)）。**粗糙壁不兼容**：k-ε 系（standard/RNG/realizable）+ enhanced wall treatment 或 Menter-Lechner 近壁处理；Linear Pressure-Strain 的 RSM；选 Realizable k-ε 的 DES；Stress-Omega / Stress-BSL 的 RSM；transition k-kl-ω；Kader Blending 壁面函数 + Werner-Wengle 壁面处理的 LES。参数：**Roughness Height K_s**（默认 0 = 光滑；须非零才生效；均匀砂粒→砂粒高度、非均匀→平均粒径 d50、其他→等效砂粒高度；非常量可用 profile/UDF）与 **Roughness Constant C_s**（默认值按 k-ε 重现 Nikuradse 紧密堆积均匀砂粒管道阻力数据标定；非均匀砂粒/肋条/丝网粗糙度可能需更高值；任意粗糙度无明确选值指引）。**结冰模型四选项**：Specified Roughness（同标准法）、NASA Correlation（8.114–8.117，经验关联式，涉及自由流速度/温度、液体含量 LC、特征长度 c 等）、Shin-et-al（8.118–8.119，用含液滴平均直径 MVD 的因子修正 NASA 关联）、ICE3D Roughness File（FENSAP-ICE 节点文件，File → Read → Profile 读入后出现在下拉）。**Note（结冰模型）**：仅适用于低 Re 湍流或完全解析边界层的细近壁网格；仅对气动表面/空气验证过；不适用于粗糙度占通道高度显著比例的窄通道；未对液体等非空气工质验证；要求 y+ ≤ 1。
- **壁面运动**（8.4.15.4）：Stationary / Moving。**只能给切向运动——相对相邻 cell zone 有法向分量的壁面运动不能用 moving wall（用滑移/动网格）；给出的法向分量会被忽略**。Relative to Adjacent Cell Zone vs Absolute：相对系零速 = 壁在相对系静止（绝对系随区运动）；绝对系零速 = 壁绝对静止（相对系反向运动）；**Important：用 MRF/滑移/混合面时建议用相对速度（默认）——改区速度无需改壁速度**。Translational（Speed + Direction；默认速度 0 即禁用；变速用瞬态 profile 或 UDF；非线性平移用 Components）；Rotational（Speed + Rotation-Axis Direction/Origin；**轴独立于相邻区与其他墙的轴**；3D 轴 = 过原点沿方向向量；2D 只给原点、轴为 z 向；2D 轴对称恒绕 x 轴原点 (0,0)；瞬态转速用 profile/UDF；**切向旋转运动仅当壁面包围绕该轴的旋转面（圆/圆柱）时才正确**；静止参考系中也可给旋转运动）；Components（X/Y/Z 速度，可用 profile/UDF）。**双面墙**：shadow 自动创建，wall 与 shadow 可各自指定运动（耦合与否均可）；**但与固体区相邻的 wall（或 shadow）不能指定运动**。
- **剪切条件**（8.4.15.4.2–8.4.15.4.7）四种：**no-slip**（默认）；**Specified Shear**（τ 分量常数/profile；滑移壁给零剪切）；**Specularity Coefficient**（多相颗粒流专用；碰撞传给壁动量的份额，0–1，基于 Johnson-Jackson 壁面条件；0 ≈ 零剪切、接近 1 = 显著横向动量传递；**动壁不可用**）；**Marangoni Stress**（表面张力温度梯度引起的剪切，τ = (∂σ/∂T)·∇_s T（8.120）；**须解能量方程**；给 Surface Tension Gradient；**湍流壁面函数不与 Marangoni 选项同用**）。零剪切壁的湍流处理：压力基 + 湍流模型默认移除零剪切壁的湍流壁面函数（湍流量给 Neumann 条件、壁如对称边界），利于收敛；`solve/set/advanced/specified-zero-shear-alternative-treatment? no` 可关（切换会强制重算所有湍流算例的单元壁距离）。稀薄气体部分滑移 → p. 2412。
- **热边界条件**（8.4.15.5）七型：**Heat Flux**（默认；0 = 绝热）、**Temperature**、**Convection**（换热系数 + 自由流温度）、**Radiation**（外部发射率 + 外部辐射温度）、**Mixed**（对流+外部辐射四参数）、**via System Coupling**、**via Mapped Interface**。双面墙可用其中子集并可选用 Coupled（见下）。
  - **增强换热**（8.4.15.5.6）：扰动流/扰动边界层应用（机舱/底板热负载、热透排气系统瞬态换热）可用**对流增强因子**（实测 Nu / 理想流 Nu）——`define/boundary-conditions/wall` 按 profile 或单值给；默认 1 = 不增强。
  - **薄壁热阻**（8.4.15.5.7）：默认零厚度；给材料 + Wall Thickness（常数或表达式/UDF/profile）+ Heat Generation Rate（如 PCB 电功耗）即按一维稳态导热解热阻与壁内产热；**Important：薄壁只能用常数导热系数——非常数导热须用壳导热**。后处理（未开壳导导）：Static Temperature（相邻流/固单元）、Wall Temperature（壁面本身）、Wall Temperature (Thin)（隔厚度对的另一面）。
  - **双面墙热条件**（8.4.15.5.8）：**Coupled**——无需额外热条件（直接按相邻单元解算传热）；仍可给薄壁材料/厚度/产热，且一侧设置的阻力参数自动赋予 shadow；无黏流 Thermal 页灰置、CHT 面热通量报 0；相交边界上的耦合墙在 Node Values 开/关时 wall 与 shadow 结果可能不同。**解耦**：选 Temperature 或 Heat Flux（Convection/Radiation 不适用于双面墙）；**开壳导热时解耦无效**；耦合关系保留可再耦合；两解耦薄墙可不同厚度、彼此绝热。
  - **正交性二次梯度限制**（8.4.15.5.8.1）：耦合双面墙附近面正交性差时，能量与 UDS 扩散通量的切向（二次梯度）分量可能无界 → 发散；压力基可启用限制（8.121，系数按面正交性控制扩散项）。仅压力基、仅能量与/或 UDS、仅耦合双面墙；`solve/set/advanced/secondary-gradient-limiting/energy?` / `uds?`；默认网格质量限 0.7–0.9，`.../mesh-quality-limits` 可调（趋近 1 更稳但损精度）。
  - **固体运动的边界对流**（8.4.15.5.9）：墙仅邻接一个有 solid motion 的固体区且速度明显入/出域时开 Boundary Advection（按法向速度、温度与材料属性计入热能对流）；`define/boundary-conditions/detect-boundary-advection` 可自动审查全部墙——固体速度平均角度 > 2° 的相应墙自动启用。
  - **壳导热**（8.4.15.5.10）：Shell Conduction 选项（能量激活时所有墙可用，mapped interface 除外）+ Edit... 定义单/多层（每层须非零厚度）；不仅法向（总在算）还计算面内导热；详见 p. 2240；串/并行均可读 case；`define/boundary-conditions/modify-zones/create-all-shell-threads` 一键把所有有限厚度墙转为单层 shell（厚度同原薄墙、已有 shell 不动）；`.../delete-all-shells` 一键全部关闭；串并行皆可。
  - **System Coupling**（8.4.15.5.11）：via System Coupling 用于**接收**热数据（向外提供无须勾选）；可传入温度/热流量/换热系数，可传出温度/热流量/换热系数/近壁温度（bulk/ambient）；材料/厚度/产热照常可设。**Note：勾选但 Fluent 实际未在接收耦合数据（未参与或单向只提供）时，边界表现为绝热**。
  - **Mapped Interface**（8.4.15.5.12）：mapped 界面的 wall 区自动选中 via Mapped Interface（处理穿透/间隙的耦合墙）；**Eulerian 多相不在 mapped 界面做热耦合**；可给标准热设置；**Shell Conduction 与 via Mapped Interface 不兼容**。
  - 稀薄气体温度跳跃 → p. 2414。
- **组分/表面反应**（8.4.15.6）：默认所有组分零质量通量（参加表面反应的除外）；Species 页逐组分选 Specified Mass Flux（默认）或 Specified Mass Fraction；壁面表面反应开 Reaction + 机理（p. 2484）；**Surface Area Washcoat Factor** 建模未解析的涂层（增大催化面积）；瞬态沉积后处理：Initial Deposition Thickness 与 Solid Species Density（多固体种给平均密度）——仅用于后处理、不影响结果。部分催化边界（高超声速）→ p. 2415。
- **辐射/DPM/接触角/UDS/液膜/结构**（8.4.15.7–8.4.15.12）：灰模型（P-1/DTRM/DO/S2S/MC）给 Internal Emissivity（Thermal 页）；Rosseland 无需（按 1）；非灰 P-1/DO/MC 在 Radiation 页逐波段给常发射率（默认 1）或参数化；非灰 DO/MC 还须定 opaque/semi-transparent；DO/MC 可开 Boundary Source。DPM 去向见 p. 2882；VOF 壁面黏附接触角（Momentum 页，逐相 pair）见 p. 3070；UDS 见 p. 1801；Eulerian Wall Film 激活后 Wall Film 页可设液膜条件（p. 3364）；FSI 的 Structure 页设位移边界（p. 3345）。
- **默认值与计算**（8.4.15.13–15）：默认热条件 = 零热通量（绝热）、壁不运动。剪切计算：no-slip 层流按壁面速度梯度（8.122）、湍流用近壁处理；specified-shear 反算切向速度；**无黏流所有壁均为滑移（无摩擦）**。换热计算（8.123–8.130）：定温——流体侧 q = h_f(T_f − T_s) + q_rad（h_f 由局部流场算，8.130）、固体侧按导热（8.124）；热通量——反解壁面温度（8.125/8.126）；对流——q = h_ext(T_ext − T_s) + q_rad（8.127）；外部辐射——εσ(T_s⁴−T_rad⁴) 形式（8.128，含 ε_ext、Stefan-Boltzmann 常数、辐射源温度 q_rad）；组合式（8.129）；**各式均假设零厚度壁**。

- **流体侧换热系数计算**（8.4.15.15.6，p. 1535）：层流按壁面 Fourier 定律离散形式（8.130）；湍流用由热/动量传递类比导出的温度壁面律（引 [86]，见 Theory Guide Standard Wall Functions）。

### 8.4.16 多孔壁（Perforated Wall，pp. 1535–1551）

- **用途**： effusion 冷却——低温空气经成千上万小孔注入高温区冷却壁面（燃烧室等）；模型避免逐孔画网格。
- **限制**：模型只影响速度场、温度场（能量开启时）、组分分布（组分输运开启时）、混合分数与进展变量（PDF 模型开启时）；Euler-Euler 多相**只作用于主相**；**对湍流的影响不考虑**。
- **建模概念**：固体壁不画网格（CHT 除外）；在"注入侧"给定流动注入，在"抽出侧"抽取等量质量保证守恒。两种做法：**Uniform**（整个注入侧面给统一质量通量边界；只考虑注入的无黏流向/法向动量通量的一阶效应）与 **Discrete**（逐孔施加注入条件；孔用模型标记而非画网格）。
- **注入流量**：动态法（按局部压力场算）——孔出口质量流 ṁ_h = A·C_d·√(2ρ(P_ext−P_inj))（8.131，不可压；A 有效孔道面积、C_d 排放系数、抽出侧密度与两侧压力）；孔内高速用可压公式（8.132，含气体常数、抽出侧温度、比热比 γ）。可给 C_d 或乘积 A·C_d。静态度：直接指定孔出口质量流。注入量确定后：抽出侧加质量通量、能量/组分从抽出侧算出并等量加到注入侧（守恒）；注入侧动量通量按应用需要选选项。**CHT**：固体壁画网格、孔不画；壁面-注入流换热 q 按 ṁ·c_p·ΔT（8.133），h 用 Cho-Goldstein 短孔关联式（8.134，Nu=f(Re,Pr)），孔出口注入温度（8.135）；孔不画网格 → 壁温假设沿孔取向线性分布、解析总换热（8.136–8.137，孔入口/出口壁温）。
- **设置**（8.4.16.3–8.4.16.4）：任务页 **Perforated Wallis...** 按钮（原文如此）→ 勾 Perforated Wall Model → Model Setup Method：**Import Input Files**（成百上千孔时用输入文件）或 **Manual Inputs**。手动流程：① Number of Injection Walls；② **Injection Explicit Relaxation Factor**（0–1，默认 1；混合当前/上一次迭代算得的注入流量——收敛问题就调低）；③④ 注入壁 ID 与名称；⑤ **Coupled with Extraction Side**（勾选自动选 Dynamic 注入法，否则 Static；**当前实现不能改 Static/Dynamic**）；⑥ 抽出壁名称；⑦ Injection Type：Uniform / Discrete；⑧ Discrete：Number of Holes + Injection Holes Geometry（轴定义 Point-Point 两点+直径 或 Point-Direction 点+方向+直径；逐孔给；Fluent 自动求圆柱与注入/抽出壁交点并标记孔出口/入口面；Z 仅 3D；去掉 Discrete on Extraction Side（默认开）可在抽出侧用均匀条件）；⑨ Static 法（Static Setup 对话框）：Normal to Boundary 或 Direction；逐孔 Mass Flow Rate（kg/s）、Temperature（K）、组分质量分数（末组分差值求得）、方向分量；⑩ Dynamic 法（Dynamic Setup 对话框）：Uniform 型的 Dynamic Method Parameter = Normal to Boundary / Direction / **Injection Angles**（孔轴在局部柱坐标 (e1,e2,e3) 的面角 α_s 与切向角 α_t——e1 为壁面外法向、e2 同全局柱坐标周向、e3 为叉积）；Discrete 型参数 = **Cd 或 ACd** 逐孔给；Injection Formulation 选 Incompressible（8.131）/Compressible（8.132）；可选 **Use Dynamic Cd?**（Discrete + Discrete on Extraction Side 时）挂 DEFINE_PERFORATED_CD UDF（否则常数 C_d）；⑪（含固体区时）**CHT Coupling**——需同时满足 Coupled with Extraction Side + Discrete + Discrete on Extraction Side，且注入/抽出壁须是 wall/wall-shadow 对；⑫ 逐壁重复。
- **输入文件格式**（8.4.16.5）：ASCII；注释行以 / ; ! 开头；行 1 = 墙数（对数）、行 2 = URF；每墙：注入墙名 → 耦合行（coupled [抽出墙名]）→ 注入类型行（uniform|discrete [point-point|point-direction|normal|direction|angle] [ext-discrete]）→ 注入法行（static|dynamic [cd-profile] [incompressible|compressible] [cht-coupling]）→ % 开头的表头行（关键字 x y z vx vy vz x1 y1 z1 x2 y2 z2 diameter nx ny nz alpha-s alpha-t mf tem fmean pv 及组分名，Z 仅 3D，顺序任意但数据行须按其顺序）→ 逐孔数据行。uniform 只用 acd；discrete 用 cd 或 acd；direction 用 nx ny nz；angle 用 alpha-s alpha-t；static 用 mf、tem（能量时）、非零组分名、fmean/pv（PDF 燃烧时）。
- **后处理**（8.4.16.6）：Perforated Walls... 类的 Tagged Face、Injection Hole Mass Flow Rate、Injection Pressure、Conjugate Heat Transfer。

### 8.4.17–8.4.19 Symmetry、Periodic、Axis（pp. 1551–1556）

- **Symmetry**：几何与预期流/热解都镜像对称时用；也可当零剪切滑移壁。无输入，但位置必须定义正确。**Important：轴对称几何的中心线要用 axis 类型而非 symmetry**。反例（图 8.69）：几何对称但流动不对称（浮力；旋周——后者应改用旋转周期边界）。计算处理：对称面上所有量零通量——法向速度为零、所有变量法向梯度为零；剪切为零 → 可视为"滑移壁"。
- **Periodic（无压降型）**：两对面流动完全相同；成对使用。两类周期条件——无压降型（FLUENT 4 称 cyclic）与允许平移周期压降的"充分发展周期流"型（后者见 p. 1809，密度基求解器在 Periodic 对话框多一项周期压降）。输入只有 **Rotational / Translational** 之选（默认全部为 Translational）；旋转周期角度由求解器自动计算，所用轴 = 相邻 cell zone 的旋转轴（**相邻区无需是运动区**——静止系管道扇形切片即可用旋转周期）。**网格核查**：Domain → Mesh → Check 会算周期面旋转角的最小/最大/平均值——三者差异不可忽略 = 网格绕该轴不周期。计算处理：对面周期面被当作直接邻居（取对面相邻单元的流动条件）。
- **Axis**：轴对称几何中心线必须用 axis 类型；也用于柱极坐标四边形/六面体网格中心线。无输入。**Important：2D 轴对称几何中 axis 边界必须位于 y=0 线上**。计算处理：轴上点的变量值取相邻单元的值。

### 8.4.20 Fan 边界（pp. 1556–1563）

- **定位**：集总参数模型——无限薄的 internal face zone 上给经验风机曲线（压跃升 vs 流量/速度）；可另给旋周速度径向/切向分量（仅 3D）。预测过风机流量而非叶片细节流动；作为唯一流动源时系统流量 = 系统损失与风机曲线的平衡点。另有用户自定义风机模型接口（p. 1608）。**限制：Solar Load 模型下 fan 边界总是计入太阳通量计算、无法关闭**。
- **压跃升**：Δp 为法向速度的多项式（8.138）/常数/分段线性/分段多项式/UDF；**速度可正可负——务必保证正向流产生压升**；可选用法向速度的质量平均值给全区单一压跃升值。定义时核查 **Zone Average Direction**（求解器算的面平均方向向量）——指向期望吹风方向就不要勾 Reverse Fan Direction，反之勾选。**Limit Polynomial Velocity Range** 的 Min/Max Velocity Magnitude 只限制压跃升值、**不限制流场速度**（超界取边界值处的压跃升）。Calculate Pressure-Jump from Average Conditions = 用质量平均法向速度算单一值。**profile 法：profile 必须按升序写、最小压跃升在最上**。
- **示例**（8.4.20.3.2.4）：2D 风道 2.0×0.4 m、15 m/s、2000 rpm 风机——Q(m³/s)→Δp(Pa)：25/0、20/175、15/350、10/525、5/700、0/875；按面积 0.4 m² 换算成 v(m/s)：62.5/0、50/175、37.5/350、25/525、12.5/700、0/875；线性式 Δp = 875 − 14v（8.141）。
- **旋周速度**（8.4.20.3.4）：Swirl-Velocity Specification 开 → 给 Fan Origin + Fan Axis + **Fan Hub Radius**（默认值取非零以防多项式除零，具体数值未提取）+ 切向/径向速度为半径的多项式（8.139–8.140，系数按 r 幂次空格分隔）/常数（经 Profile Specification 开关）/UDF 或 profile。**所有旋周速度输入必须 SI 单位**。
- **后处理**：压升 = 用 Transform Surface 把 fan 区向上下游各微移生成两个面，Surface Integrals 分别报平均静压相减；云图/XY 看静压静温——**务必关掉节点值显示**（节点值会把 fan 两侧单元值平均掉、看不到压跃升）。

### 8.4.21 Radiator 边界（pp. 1563–1570）

- **定位**：换热元件（散热器/冷凝器）集总参数模型——无限薄 internal face zone 上给压降与换热系数（均为法向速度的函数）。更详细模型见 p. 2340。
- **方程**：Δp = K·½ρv_n²（8.142）；K = 常数/多项式（8.143）/分段线性/分段多项式。换热 q = h(T_down − T_rad)（8.144；T_down 散热器下游温度、T_rad 散热器温度）；h = 常数/多项式（8.145）/分段函数。**要给实际热流 q：Temperature 填绝对零度（0 K）+ 常数 Heat Flux**。 radiator 温度填 Temperature 字段（**不允许低于绝对零度**）；q 沿散热器面积分。
- **换热系数推导**（8.4.21.1.2.1）：热平衡 q = ṁc_pΔT = hA(T_ext − T_down)（8.146–8.149；变量含质量流量、比热、经验 h、外部参考温度、下游温度、迎风面积；h 可写成速度的多项式）。
- **输入**：identify zone（interior → 改类型为 radiator）；Loss Coefficient；热流或（换热系数 + radiator 温度）；DPM。**示例**：Table 8.2 空气侧数据（v 5/10/15 m/s；T_up 300 K；T_down 330/322.5/320 K；Δp 75/250/450 Pa；水侧 7 kg/min、进水 400 K）→ 简化表 8.3：动压头 ½ρv² = 12.5/50/112.5 Pa，K = 6.0/5.0/4.0（**K 随 |v| 线性递减**，8.150）；取 ρ=1.0、c_p=1000 得 h = 2142.9/2903.2/3750.0 W/m²-K → 二阶多项式拟合（8.151）；**v 取过散热器速度的绝对值**。
- **后处理**：压降/温升 = 平移复制面 + Surface Integrals 平均静压/静温相减；核对 K 用平均法向速度（不与坐标轴对齐时用 Custom Field Function 造法向速度函数）；图示同样**关节点值**。

### 8.4.22 Porous Jump 边界（pp. 1571–1572）

- **定位**：已知速度（压降）特性的薄"膜"；多孔介质 cell zone 模型的一维简化；用于滤网/过滤器压降、不关心换热的散热器。**能用就尽量用它（比完整多孔模型更稳健、收敛更好）**。
- **方程**：Δp = −(μ/α·v·Δn + C2·½ρv²·Δn)（8.152）——Darcy 项 + 惯性损失项，μ 层流黏度、α 渗透率、C2 压降系数、v 面法向速度、Δn 介质厚度；α 与 C2 用 8.2.3.8 的方法算（p. 1393）。System Coupling 可与 porous jump 边界双向传数据（p. 4862）。
- **Note**：只考虑动量阻力、不考虑扩散；**压力基耦合求解器 + porous jump 可能有耦合设置无法解决的收敛问题——改用分离式压速耦合**；porous jump + WFGC 内存节省模式不建议组合。
- **输入**：identify zone（internal face）；**Face Permeability α**；**Porous Medium Thickness Δn**；**Pressure-Jump Coefficient C2**（单位为长度倒数；Units 对话框 Quantities 选 length-inverse 可改）；**Thermal Contact Resistance**（默认 0.1 m²-K/W）；DPM；开 solar load 时给 Solar Boundary Conditions（可定义成半透明边界行为）。厚度/渗透率/压降系数的默认值代表"无动量阻力"模型。

- **porous jump 补遗**（p. 1573）：porous jump 须建模为单元间的 internal face zone（默认识别为其他内面类型时右键改类型）；solar load 下可定义为半透明边界行为（仅对太阳辐射计算，见 p. 2323）；后处理建议同多孔介质（p. 1423）。

## 8.5 批量编辑多个边界条件（pp. 1573–1575）

- **Multi Edit 对话框**：同时编辑同类型多个相关边界。入口：树中 Ctrl 多选边界（或经 Adjacency 对话框的 Adjacent Face Zones 列表选）→ 右键 Multi Edit...。**Note：单面（外部）wall 不可与耦合（内部）wall 一起多选编辑**。
- 适用边界类型：exhaust fans、inlet vents、intake fans、mass flow inlets、mass flow outlets、outflows、outlet vents、pressure far fields、pressure inlets、pressure outlets、velocity inlets、walls。设置方式与非批量版一致。
- **彩色图标语义**：一种图标 = 该设置在各所选边界间取值不同；另一种 = 所显值将在 Apply 时应用。点图标可切换状态（修改多项后发现某项错了就点掉它）。**Note：若某输入会连带改变其他字段，不要指望只还原"主字段"——凡带绿勾的字段 Apply 时都会被应用**。
- **Primary Zone** = 与其他所选区比较的"基准"区（下拉换或按重选顺序定）；多相仿真用 Phase 下拉逐相设置（**切换相之前必须先 Apply**）；Zone List 高亮区才应用绿勾字段（可子选），可按 Adjacency/Name 排序。批量修改会打印到控制台与 transcript。

## 8.6 瞬态 Cell Zone 与边界条件（pp. 1575–1579）

- **三种指定方式**：标准瞬态 profile（Profiles 格式）、表格瞬态 profile、CSV 格式（p. 1619）。**Important：只随时间变化、必须空间均匀**；开启 in-cylinder 模型后可用曲轴转角代替时间（表格与 profile 均可）。
- **标准瞬态 profile**（8.6.1）：`((profile-name transient n periodic?) (field_name …)…)`；profile 名与字段名 < 64 字符；时间字段升序；periodic? 1 = 时间周期。示例：`((sampleprofile transient 3 0) (time 1 2 3) (u 10 20 30))`；曲轴角示例 `((example transient 3 1) (angle 0 180 360) (temperature 300 500 300))`。**Important：一律 SI 单位（读入不做单位换算）；profile 名必须全小写（不接受大写）**。读入：Profiles 对话框（Setup → Boundary Conditions → Profiles...）或 File → Read → Profile...。
- **表格瞬态 profile**（8.6.2）：首行 `profile-name n_field n_data periodic?`，次行字段名，其后数据行；首字段为时间、升序。周期=1 时 **n_data 须恰好闭合一个周期**（示例 periodtabprofile：0/10、1/20、2/30、3/10）。曲轴角示例：angle 0/180/360 ↔ temperature 300/500/300。**Important：SI；profile 名全小写；字段名不含空格/括号；UCS-2 等编码可能读不进——用文本编辑器另存即可**。读入：`file/read-transient-table`，之后同边界 profile 使用（Profiles 对话框可见）。
- **运动/变形网格 profile**（8.6.3）：两种格式皆可（表格或标准）；**变量命名**——位置 x,y,z；速度 v_x,v_y,v_z；角速度 omega_x,omega_y,omega_z。

## 8.7 边界声学波模型（pp. 1579–1608）

- **背景**：人为截断域的标准边界会反射出射压力波 → 域内出现虚假反射。四类模型：**turbo-specific NRBC**（仅密度基）、**general NRBC**（双求解器）、**阻抗 IBC**（仅压力基）、**transparent flow forcing**（仅压力基）。密度基 NRBC 仅限可压理想气体；压力基的 general NRBC/IBC/TFF 用于可压流动瞬态仿真（理想气体、真实气体、组分输运、可压混合物）。替代方案：边界海绵层（密度基、瞬态可压、压力基，p. 2767）。
- **Turbo-specific NRBC**（8.7.1）：叶轮机械专用；对边界解变量做 Fourier 变换消反射（引 [54]，原为轴流、已扩展径流）。**限制**：仅密度基（显式/隐式）；稳态可压 + 理想气体律；进出口只能是压力入口/出口；**压力入口必须用圆柱坐标流动指定法**；3D 进出口面必须是 quad-mapped 结构网格（三角/quad-paved 不行；2D 可非结构；3D 远离进出口处可非结构）；3D 扩展解耦切向/径向变化——叶距相对半径小的时候最好；**进出口不允许回流**（强回流改用 general NRBC）；与组分输运不兼容（主要解理想气体单组分）。理论：线性化 Euler 解的周向 Fourier 分解——0 阶模 = 周向平均（用户输入），高阶谐波按二维无反射处理；亚音速进口 1 出 4 入、出口 4 出 1 入特征波；Fluent 中入口给 P0/T0 即得 s0/h0；超音进口给静压+总压+总温即可、超音出口全外推；欠松弛因子有默认值（数值未提取）。**用法**：密度基隐式**先不用 NRBC 收敛，再开 NRBC 重收敛；发散就降 CFL**（NRBC 激活时压力入口/出口只用近似通量雅可比）。流程：`define/boundary-conditions/non-reflecting-bc/turbo-specific-nrbc/enable?` → `initialize`（成功打印域范围摘要；失败报错）→ `set/` 子菜单（under-relaxation、discretization 默认高阶重构、verbosity 0 静默/1 基本（默认）/2 调试）。**混合面联用**：把混合面界面定义成压力出口/压力入口对；**混合面上有回流时不要用**。**并行**：每个 NRBC 边界区的所有单元必须在同一分区（手动分区，p. 4551）。
- **General NRBC**（8.7.2）：基于 Euler 方程特征波关系；密度基只用于压力出口，压力基用于压力入口/压力出口/速度入口/质量流通量边界；**无几何/网格类型限制**（不同于 turbo），但边界附近网格偏斜度好些利于收敛。**限制**：压力出口启用 target mass flow rate 时不可用；密度基仅可压理想气体（**不得与湿蒸汽、真实气体同用**；不兼容组分输运与混合分数输运——主要理想气体单组分）；压力基不兼容稳态与 Eulerian 多相；VOF/Mixture 含可压气/液时**只有压力入口与压力出口**可开 NRBC（次相体积分数非零时边界仍可能有小反射）。理论：Euler 方程改写到边界正交坐标系（ξ 法向），特征分析修正 ξ 向波项（8.197–8.200，特征值 u_ξ 与 u_ξ±c 等）；出流波幅由内场外推导数算，入流波幅——切向速度波幅取零、压力与熵波幅用 **Poinsot 线性松弛法（LRM）**（正比于边界面局部原始变量与施加值之差）；各边界类型的施加量：压力出口（8.201，σ 因子；回流压力压力基可给静压/总压、密度基只有总压；向无穷远 p∞ 松弛的建议 σ 见 8.202——含声速/域尺寸/域内最大 Mach/欠松弛默认 0.15；要边界平均压力逼近指定值则用 σ2（8.203，默认 5.0；**"指定平均压力"选项仅密度基**））；压力入口（8.204）；质量流通量（8.205）；速度入口（8.206）。**用法**：Pressure Outlet 对话框 Acoustic Wave Model 选 Non Reflecting（压力入口/速度入口/质量流入口同理，压力基可压时）；密度基选 **Exit Pressure Specification**：Pressure at Infinity（非定常/无穷远压力；松弛速度 σ 默认 0.15）或 Average Boundary Pressure（稳态强制平均压力逼近出口压力；σ2 默认 5.0；**5.0 不保证各种工况都凑效——不达标就调 σ2**）；压力基的 Backflow Pressure Specification 静压/总压（密度基只用总压）；压力/质量流/速度入口不允许回流。**Important：流动与边界相切时，Backflow Direction Specification Method 选 Direction Vector 或 From Neighboring Cell——不要选 Normal to Boundary（初始化时面速度按通量算成零 → 收敛失败）**。**最佳实践**：先不开 NRBC 跑出稳定解（不必收敛）再激活；CFL 常需降低——密度基隐式典型 CFL 2.0、压力基 4.0。
- **阻抗边界条件 IBC**（8.7.3）：介于全反射与全无反射之间——指定部分反射（改变入射波幅值与相位）；用于域外物体反射波显著影响流场的场景。**限制：仅压力基；不兼容稳态、多相、可压液体模型**。理论：频域阻抗 = 声压扰动/法向速度扰动（8.207）；时域求解器经卷积积分（8.208）转换；阻抗无界时用导纳；Fluent 统一用**反射系数** R = (Z−ρc)/(Z+ρc)（8.209，Fung [49]）；声压与法向速度扰动关系离散化（8.210）叠加到 NRBC 方程上（NRBC 提供平均流动）。频域反射系数数据通常不满足因果性/实值性 → 基于**系统理论**的近似（Fung [48]）：R 为零阶 + 一阶 + 二阶系统之和（8.211：实项 R0、实极点对、复共轭极点对）。**约束（界面强制）**：实极点 λp 与复极点实/虚部应为正；**无源性要求 |R0| < 1**；另需自行确保按公式算出的 |R| < 1。实验数据可为比阻抗、反射系数或吸收系数（实测或声学求解器）。**用法**：压力出口（或压力/速度/质量流入口；压力基可压）Acoustic Wave Model 选 Impedance → Impedance Parameters 三种给法：Import Parameters（极点/留数文件）、Compute from Data File（Impedance Data Fitting 对话框拟合）、手动输入（零阶项 R0、实极点个数与各极点/幅值、复极点个数与各极点实/虚与幅值实/虚）。**Important：切向流同样不要选 Normal to Boundary 回流方向**。**IBC 叠加在 NRBC 之上：先建立好平均流再开 IBC；IBC 边界相邻单元的 cell acoustic CFL < 1（定义见 p. 4395）；连续性收敛判据收紧到 1e-4**（增加每时间步耦合迭代）。**阻抗参数计算**（8.7.3.4）：读频域实验数据 → 算极点/留数级数（Gustavsen-Semlyen 算法 [60]）；可应用到字段、存 pole/residue 文件、打印、写拟合频率/阻抗数据核对。Note：吸收系数数据的拟合项可能随版本/操作系统不同——不影响结果（只用拟合曲线）。流程：Compute from Data File → Input Data Type（Specific Impedance / Reflection Coefficient / Absorption Coefficient 8.212–8.213）→ Input Data File（monitor 格式：频+实/虚列；示例 nasa-tp-2679.imp、dc-real-complex-rf.rfl、dc-real-complex-ab.abs）→ Perform Fitting；拟合前可经 TUI 调 `define/boundary-conditions/impedance-data-fitting/` 的 iterations（默认 20）、convergence-tolerance（1e-6）、residue-tolerance（1e-6，滤寄生极点）、verbosity 1；Write Fitted Data / Write Impedance Parameters / Apply to Zone → 核查 Apply。**独立工具**：`utility impedance [--help] [-p P] [-f F] [-i I] [-t T] [-r R] [-y Y] [-m M] [-v V] I [R C]`（-p 极点/留数文件、-f 拟合数据、-i 迭代数 20、-t 1e-6、-r 1e-6、-y impedance|reflection|absorption、-m 吸收系数相位（0/random）、-v 0/1、I 输入文件；R C 极点数须满足与数据点数 n 的关系式 8.214 并取 RMS 最小——**建议省略让 Fluent 自动取 RMS 最小的极点数**）。示例：`utility impedance nasa-tp-2679.imp -p par.pr -f fitted.imp`。
- **Transparent Flow Forcing（TFF）**（8.7.4）：把域切小时，边界应像大域的切片——入射瞬态能进来、出射瞬态无反射离开（数值域固有频率与物理波频率耦合时人工反射影响很大）。TFF 在**无反射边界之上**建模入射波、出射波无反射穿过；**压力基、可压流动瞬态**；用于速度/质量流/压力入口与压力出口。**限制：不兼容稳态、多相、可压液体模型**。理论：瞬态流分成入射波 I⁻ 与出射波 I⁺ [79]；声学极限下波强由压力与法向速度扰动表达（公式未提取）；Z0 = 平均流声阻抗（ρ0c0）；出射波强内部计算、**入射波强由用户 profile 给定**。**用法**：① 造入射波强 profile（profile 文件 p. 1616 或 DEFINE_PROFILE；按位置与时间给；可由声压、声速扰动或声质量流量换算）；② 打开边界对话框；③ Momentum 页 Acoustic Wave Model 选 Transparent Flow Forcing；④ Transparent Flow Forcing Parameters → Incoming Wave 下拉选 profile。**Important：切向流回流方向同样别选 Normal to Boundary；TFF 叠加在 NRBC 上——时间步使相邻单元 CFL ≤ 1；先建立好平均流再开 TFF**。

## 8.8 用户自定义风机模型（pp. 1608–1615）

- **定位**：周期性重新生成 profile 文件来更新风机特性（压跃升、径向/旋周速度分量）——普通 profile 文件整个求解过程不变，而此模型允许随流场发展更新。需自建可执行程序（任意语言，如 Fortran/C）：读 Fluent 写出的 profile、写出修改后的 profile；Fluent 按用户设定自动调用。
- **流程**（8.8.1）：① 指定一个/多个 interior 面为 fan zone；② User Defined → Model Specific → Fan Model... 打开 User-Defined Fan Model 对话框填可执行名与读写指令；③ 初始化流场与 profile 文件；④ 用标准 Fan 对话框给风机参数；⑤ 计算。
- **示例**（8.8.2）：圆柱域（长 1.25 m、径 0.2 m）、进口 10 m/s、对称面包围、中心圆风机、下游压力出口。Fluent 周期性写出径向 profile（风机面静压、压跃升、轴向/径向/切向速度按环形段平均；环形段尺寸由风机尺寸与径向点数定）；可执行程序：读 profile → 计算新压跃升/径向/旋周速度 → 写新 profile；Fluent 读取后继续。
- **参数**（8.8.2.1）：Fan Zones 选择（多个不同 profile 的风机区可一起选；zone ID 写入解 profile 文件、可执行每区调用一次、各写各的 profile）；**Iteration Update Interval**（如 10 = 每 10 次迭代执行一次）；**Output Profile Points**（Fluent 写出的 profile 点数，可与可执行写出的点数不同）；**External Command Name**（可执行文件名；不在工作目录须给完整路径）。
- **示例程序 fantest.f**：`rfanprof` 读 profile（npmax=900、zoneid、iptype 0=radial/1=point、半径/压力/压跃升/三向速度数组）；循环更新 `idp = 200 − 10·iva`、`ivt = 20·ir`、`ivr = 0`；`wfanprof` 写新 profile（radial 或 point 格式；字段 r、pressure-jump、radial-velocity、tangential-velocity）。**profile 名任意——初始化后 wfanprof 用的名字会出现在 Fan 对话框下拉中**。
- **初始化与选择**（8.8.2.3–8.8.2.4）：先用 Solution Initialization 初始化流场，再在控制台输入 **`(update-user-fans)`**（含括号）——创建 wfanprof 中的 profile 名。然后在 Fan 对话框给 Fan Axis/Fan Origin/Fan Hub Radius 并从下拉选压跃升/切向/径向 profile（如 fan_8_pressure_jump 等）。
- **运行与结果**（8.8.2.5–8.8.2.6）：控制台每 10 迭代显示写出/读入（`fan-8-out.prof` 由 Fluent 写、可执行读——含压力、压跃升与三向速度；`fan-8-in.prof` 由可执行写、只含更新的压跃升与径向/切向速度——更小；前缀取自 fan zone 名）。验证：横断面速度图（无径向分量、切向随半径增长）；x=0.05 m 处静压 XY 图显示压跃升约 97.8 Pa/m。

## 8.9 Profiles（pp. 1616–1639）

- **定位**：profile 可用作边界条件、cell zone 条件与离散相初始条件——实验数据、外部程序数据或上一解算写出的数据（Write Profile，p. 984）均可作变量边界条件。本节为空间 profile；瞬态 profile 见 8.6（p. 1575）。
- **六种 profile 类型与插值**（8.9.1）：
  - **Point**：无序点集（2D/3D）；默认**零阶插值**（取最近点值）——精度依赖点密度；可选其他插值法。
  - **Line**（2D）：有序点列；零阶插值。
  - **Mesh**（3D）：m×n 网格点；零阶插值。
  - **Radial**（2D/3D）：数据只是半径的函数；**首列必须命名为 r；线性插值；按 r 升序排列**。轴的确定：2D → 过 (0,0) 的 z 向向量；2D 轴对称 → 过 (0,0) 的 x 向向量；3D 有旋风机 → Fan 对话框的风机轴；3D 无风机 → 相邻流体区旋转轴；边界用了局部圆柱坐标 → 该局部坐标系轴。**Important：CSV radial profile 首列须命名 radius 且升序**。
  - **Axial**（3D）：轴向函数；线性插值、升序。
  - **Transient**：时间/曲轴角函数；线性插值、升序；用于瞬态边界条件与颗粒入射的点属性。
- **文件格式**（8.9.2）：
  - **标准格式**：`((profile1-name point|line|radial n) (field1-name a1 a2 …)…)`；mesh 型 `((name mesh m n) …)`。**名字 ≤64 字符（超长截断）；一律 SI 单位（读入不换算）；profile 名全小写**；point/line/mesh 必须含 x,y(,z) 字段、radial 必含 r、axial 必含 z；其余字段名为任意合法 Scheme 符号；缺类型默认按 point。示例 turb-prof：入口边界层 total pressure/k/eps 或速度+tke/eps 点 profile。
  - **CSV 格式**：与电子表格兼容、可读可写；支持 radial/axial/point(X,Y,Z)/transient/transient-periodic；Write Profile 存 .csv 即得；其他 Ansys 产品（Mechanical EXOPTION、CFX Profile Data Format）也能产生。**节标识符**（Table 8.4，按序）：[Name]（下一行 profile 名；空格自动换 '-'）；可选 [Parameters]（名=值，单位放方括号）；可选 [Spatial Fields]（坐标名+单位——决定 1D/2D/3D）；[Data]（数据从下一行开始）；可选 [Faces]（面-节点连接，供曲面预览）。[Data] 后必须按类型给字段标签（Table 8.5）：radial→radius；axial→axis；point→X,Y,Z；transient→time,angle；transient-periodic→time-periodic,angle-periodic——缺标签读取失败。不支持的节标识符被忽略（只找 [Name] 与 [Data]）。单文件可含多个 profile。**Important：只能用逗号分隔（不用空格）；只有 Name+Data 时只支持 SI 值（不能带单位）；含附加字段则必须带单位且不必是 SI**。保留的 X 轴标签：x,y,z,r,time,angle——同名字段被视为 X 轴函数，Y 轴函数须用其他名字。
- **使用流程**（8.9.3）：① 建文件；② Profiles 对话框 Read... 或 File → Read → Profile...（**同名 profile 覆盖旧的**）；③ point profile 可在 Profiles 对话框选插值法：**Constant**（零阶最近点，默认）/ **Inverse Distance**（距离反比加权）/ **Least Squares**（一阶 SVD）；**Note**：后两法不适用于 profile 作用在 cell zone（非面区）的情形；面区离数据点太远（默认容差双精度 ~1e-16/单精度 ~1e-7）时自动退回 Constant——`define/profiles/extrapolation-tolerance-factor` 可乘系数扩大范围；④ 可把 profile 挂到参考系（随系旋转——模拟转子对静子的 clocking 效应）；⑤ BC 对话框中 profile 字段出现在各参数下拉里；⑥ **初始化解以插值 profile**。Note：profile 或 DEFINE_PROFILE 可给体积源项，但 profile 方式拿不到方程中心系数（源线性化需要）——须用 UDF。
- **检查/删除**（8.9.3.1）：Profiles 对话框选中 profile 看 Fields 列表；Delete 删除（字段随之移除）。**Important：删除正在被 BC/cell zone 使用的 profile 后该输入处于未定义状态——须手动改成 constant/udf/expression；替换 profile 的正确顺序：删旧 → 把用它的参数改 Constant → 读新 profile 再应用**。
- **查看**（8.9.3.2）：点云或曲面预览（含 [Faces] 连接的才能曲面预览；不能的 profile 名后括号标注）；Overlay 可叠网格/图形对象；XY 图可画原始数据点或插值后单元面值（p. 4288）；Plot/Contours 选项插值的是相邻单元值（非面实际值）——要核查 BC 参数：读 profile → 用它存一个 BC → 初始化 → 2D 用 Solution XY Plot、3D 用 Contours，**都须开 Node Values**；与指定 profile 不符 = profile 文件有错。
- **重定向**（8.9.3.4，仅 3D）：把已有 profile 旋转/平移到空间任意方位的边界（如把某朝向进口的实验数据用到另一朝向进口）；假定 profile 与边界均为平面。Orient... → Orient Profile 对话框：New Profile 名；New Fields 数 = 向量数 + 标量数 + 1（坐标）；坐标字段名**必须恰好是小写 x,y,z**（Compute From 选原字段；0 表示原 profile 是 2D）；向量字段（3 分量，禁大写）；标量字段（勾 Treat as Scalar Quantity）；**Orient To**：Rotation Matrix RM 由 Euler 角 (φ,θ,ψ) 三次旋转构成（8.215–8.219）+ Direction Vector 平移向量（两 profile 场中心连线；可只转、只移或又转又移）→ Create。
- **复制**（8.9.3.5）：叶轮机械——单通道小模型算出的 profile 周期复制到全 360° 模型。Replicate... → Replicate Profile 对话框：New Profile 名；**Autofill**（profile 含 mesh-disp/meshdisptot 网格位移变量时可用，自动填充）；New Fields 数；坐标/向量/标量字段定义同重定向；**Current Profile Definitions**：Full 360 deg.（自动定复制份数）或手动 Number of copies；Number of sectors in 360 deg.；Number of sectors in profile；Calculated angle（仅显示；份数 = 360/该角）；Rotation-Axis Direction (X,Y,Z)；可选 Include Sector Tag（附加扇区标签列，绕轴右手定则编号）→ Create。**复数模态复制**（8.9.3.5.2）：实/虚向量对不能像实向量那样分开复制——先相位偏移（8.221）再旋转到通道（8.222，旋转矩阵同非复数情形）；profile 须含 **harmonic index** 参数（Ansys Mechanical 周期对称生成的自动带；外部来源须自建并设对）；Replicate 对话框出现 **Complex Pair** 勾选列——实向量行勾选后**虚向量必须紧跟下一行**；**当前限制：只能定义一个复数对**（其余勾选框变灰）。

## 8.10–8.11 GT-POWER / WAVE 一维耦合（pp. 1640–1649）

- **共同模式**：非定常仿真中 Fluent 与 1D 代码逐步互传边界条件；1D 生成 UDF 挂到 Fluent 边界上。流程：读网格、定义模型/材料/区类型（先不设实际 BC）→ User Defined → Model Specific → 1D Coupling... → 1D Simulation Library 对话框选 GTpower/WAVE + 1D 输入文件 → Start（1D 启动并按输入文件为每个边界生成 UDF）→ 在各边界选对应 UDF（**同一边界的所有条件必须选同一个 UDF——它包含该边界全部条件**）；续算需两边都设自动保存。
- **GT-POWER 要求/限制**（8.10.1）：非定常；**可压理想气体律**；边界类型限 velocity inlet / mass-flow inlet / pressure inlet / pressure outlet / wall（转矩-转速耦合）；**最多 20 个边界区**；Fluent 校核 1D 耦合边界面积（两边算的差 >5% 即报错停止并显示两个面积）；质量流/压力入口方向必须 Normal to Boundary、速度入口必须 Magnitude, Normal to Boundary；**质量流入口的指定法必须是 Mass Flux 而非 Mass Flow Rate**；可从 GT-POWER 取速度/温度/压力/密度/组分质量分数/k 与 ε（**k-ε 建议自己在 Fluent 定义——GT-POWER 值基于 1D 模型**）；材料属性须与 GT-POWER 一致；组分名须与 Materials 对话框的 Chemical Formula 对应（**最多 50 组分**）；GT 库非默认位置时设环境变量 Fluent_GTIHOME、Fluent_GTIVERSION；**GTI 不向后兼容**。
- **GT-POWER 转矩-转速耦合**（8.10.3）：Fluent 从 GT-POWER 收轴转速、回传转矩——**须 GT-POWER v2017.2+**；.dat.h5 至少暴露一个叶轮机；在接收轴转速的 cell zone 开 Frame Motion 并给 Rotational Velocity 选对应 UDF；指定一个 **Wall 边界**用于转矩计算与回传——该墙必须附着在旋转 cell zone 上且**墙名必须与耦合的叶轮机同名**；求解中每时间步取轴转速、每步内回传转矩。后处理：转矩用 Force and Moment Summary；转速可自建场函数（8.224：RPM 由速度模长 V 与转子直径 D 表达，公式体未提取、按变量定义即 rpm = 60V/(πD)）。
- **WAVE 要求/限制**（8.11.1）：WAVE 已安装并授权；**必须在 Fluent 中按 WAVE 的定义建模五个组分 F1–F5**（建议给真实物性）；非定常；可压理想气体律；边界类型限四类流动边界（**无 wall——不支持转矩-转速耦合**）；最多 20 区；方向同样必须 Normal to Boundary 系；可从 WAVE 取速度/温度/压力/密度/组分质量分数/k 与 ε（**k-ε 必须自己在 Fluent 定义——WAVE 不算它们**）；材料属性一致；组分名 = Chemical Formula（最多 50 组分）。续算：**Fluent 自动保存间隔必须与 WAVE 重启文件写频率相同**（如都为 100）。
- p. 1650 为空白版权页，无正文。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.8；本页覆盖批次 39–46，**Ch.8 全章（pp. 1347–1649）完成**（批次 46 = pp. 1616–1649 的 8.9–8.11；p. 1650 为空白版权页），均为 2026-10-17 读取。Ch.9 自 p. 1651 起，见后续批次页面。
- **公式体未提取**：本章 Eq 8.1–8.224 的大部分公式体为图形对象、文本提取缺失，已按公式周边文字记录结构与式号、未凭空补写；文字明确的例外已在正文注明（8.224 转速式按变量定义导出为 rpm=60V/(πD)）。需要精确公式时须回看 PDF 对应页。
- profile/CSV/阻抗/fantest.f 等文件格式示例为原文照录；Tables 8.4–8.5（CSV 节标识与字段标签）提取完整。坐标轴符号按 7.2.1 约定补全；Figures 8.1–8.111 为图形元素未摄取。
- 后续章节引用（壳导热 p. 2240、海绵层 p. 2767、XY Plots of Profiles p. 4288、Read/Write Profile Files p. 984 等）仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 网格读取与操作]]（7.12 的合并/分离/周期区创建等 zone 操作是本页设置流程的前置）
- [[Fluent 求解模式 GUI]]（任务页与树的组织）
- [[Fluent 表达式语言]]（表达式与参数体系互补）
- [[index]]
