---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - continuous-fiber
  - fiber-spinning
  - addon-module
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 连续纤维模型

## 摘要

User's Guide 2026 R1 Part III / Chapter 35 "Modeling Continuous Fibers"（PDF pp. 3659–3698，九节）。**本页全章完成（批次 100，pp. 3659–3698）**：连续纤维 add-on 模块模拟熔纺（melt spinning）与干纺（dry spinning）纤维拉丝——分析纤维流动、纤维属性及纤维与周围气体的强耦合；UDF 架构（UDM 8 个、fm_adjust/fm_src_* 函数族）、Fiber Model 对话框（模型/选项/交换相关式）、纤维材料属性、fiber 注入定义（single/line/matrix/file 四类型与四种纤维网格）、UDF 定制编译、求解控制与后处理。理论见 Theory Guide "Modeling Continuous Fibers"（Chapter 22，式号 22.x 由本章引用）。**仅压力基求解器可用。**

## 35.1–35.2 安装与加载（pp. 3659–3662）

`addons/fiber`（UDF 库 + Scheme 库）；**须先有有效 case**。两种加载：ribbon **Fiber Model...** 或 TUI `define/models/addon-module` → 模块号 **2**。加载中的两个提问：
- **Preset all fiber model specific UDF hooks? [no]**——yes：标准纤维源项 UDF 分配到**所有流体区**；no：逐流体区自行设 none/constant/UDF 源项（其余设置自行负责）。**载入已有 case 应答 no**，否则已存源项设置被 UDF 覆盖。
- **Preset mass exchange source terms hooks? [no]**（定义了混合物材料时出现）——**干纺仿真应答 yes**。
未预置挂钩时须自行：分配 UDM、挂 adjust 函数（fm_adjust）、逐区设源项。加载报告 UDF 清单：fm_adjust、fm_src_mass/x_mom/y_mom/z_mom/enthalpy/dom、fm_on_demand，随后 `Addon Module: fiber...loaded!`。
- **重要**：不初始化流场则纤维模型 UDM 分配不正确——**基于已收敛 case 建纤维算例时，初始化求解后必须重新载入 data 文件**。
- 设置随 case 保存且按**绝对路径**保存——模块安装或 case 位置改变后无法自动加载；此时在 UDF Library Manager（User Defined → Functions → Manage...）卸载 fiber 库再重载，已存设置与参数保留。

## 35.3 起步设置（pp. 3662–3663）

- **UDM + Adjust**：①User Defined → Memory 把 **Number of User-Defined Memory Locations 增到 8**（必须初始化求解才能正确分配；收敛 case 同上重载 data）；②Function Hooks 的 Adjust 下拉选 **fm_adjust::fiber**。
- **逐区源项**（TUI 加载且未预置时）：Cell Zone Conditions → 流体区 edit → Source Terms——每个源项（Mass、X/Y/Z Momentum、Energy、DO）none/constant/UDF 三选，UDF 对应 **Table 35.1**：Mass → `fm_src_mass`；X（Axial）/Y（Radial）Momentum → `fm_src_x_mom`/`fm_src_y_mom`；Z Momentum → `fm_src_z_mom`；Energy → `fm_src_enthalpy`；离散坐标（DO）模型 → `fm_src_dom`。
- **辐射交互**：Fiber Model 对话框勾 Fiber Radiation Interaction 时自动挂 `fm_src_dom`；**必须先初始化求解**（为 DO 模型分配内存）后纤维模型才接受辐射交互数据。

## 35.4 纤维模型与选项（pp. 3663–3666）

入口：Setup → Models → Continuous Fiber Spinning → Edit。
- **Model 二选**：**Melt Spun Fibers**（聚合物可熔融不热分解）或 **Dry Spun Fibers**（溶剂溶解液化或生产含溶剂）。
- **Options**：**Interaction with Fluent**（纤维强烈影响流场时必选——迭代中纤维方程与流动方程交替求解、计算耦合源项；源项只在 Fluent 计算过程中算）；**Include Lateral Drag**（横向/交叉流拖曳重要时——交叉流冷却或干燥为主；按绕流圆柱估算 Eq 22.30；**纤维方程不考虑侧向拖曳，故不考虑纤维侧向弯曲**）；**Fiber Radiation Interaction**（P-1 或 DO 辐射模型下考虑辐照对纤维冷却/加热；DO 模型时纤维也影响 DO 场——需给 Properties 组 **Emissivity**）；**Fiber Viscous Heating**（高拉伸速率+大纤维粘度时纤维粘性加热，进纤维能量方程 Eq 22.12）。
- **Exchange 交换相关式**：**Drag Coefficient**——const-drag / kase-matsuo / gampert / user-defined（const-drag 输无量纲常数）；**Heat Transfer Coefficient**——const-htc / kase-matsuo-1 / kase-matsuo-2 / gampert / user-defined（const-htc 输 SI W/(m²K)）；**Mass Transfer Coefficient**——const-mtc / kase-matsuo-1 / kase-matsuo-2 / gampert / user-defined（**const-mtc 输的是传质速率 kg/(m²s) 而非传质系数**）。

## 35.5 纤维材料属性（pp. 3666–3669）

- **单一纤维材料**：一次仿真中所有纤维共用同一材料属性，不能混用不同纤维材料。做法：①Create/Edit Materials 中 **Material Type 设 fluid**（作聚合物或溶剂）；②填全部数据（可用任意温度函数 profile；UDF 属性需改 UDF 模板——**可 UDF 化的属性：粘度、密度、比热、导热、溶剂液-汽平衡压力**）；③Fiber Model 对话框 Materials 组选 Polymer；④干纺另选 Solvent 与代表 **Solvent Vapor** 的气相组分；⑤在 Fiber Model 对话框补其余数据。
- **属性清单**（括注定义处）：**Blending Interval**（Fiber Model；熔纺专用——液/固态纤维粘度平均化的温度区间）；Cp、Density、Thermal Conductivity（材料对话框；干纺按 Polymer 与 Solvent 质量平均）；**Emissivity**（Fiber Model；P-1/DO 辐射 Eq 22.13/22.14/22.24/22.25——须先开 Fiber Radiation Interaction）；**Flory Huggins**（Fiber Model；仅干纺——开则按 Eq 22.3 算纤维表面汽液平衡，需给无量纲 Flory Huggins 参数）；**Latent Heat**（Fiber Model；仅干纺——溶剂汽化潜热 + 参考汽化温度（自动考虑潜热随温度变化，Eq 22.16/22.39））；**Solidification Temperature**（Fiber Model；仅熔纺——低于此温度纤维聚合物固化，用于熔纺粘度计算）；**Solvent Vapor Pressure**（Fiber Model；仅干纺——Antoine 型方程 Eq 22.38 的系数，**系数单位须使结果为 Pa**，并给有效温度范围——范围外按端点值取）；**Zero Shear Viscosity**（零剪切粘度，非拉伸/Trouton 粘度）——熔纺：**固态粘度**填在材料对话框（典型取很高于液态以把固化纤维当固体，可用温度函数），**液态粘度系数**填在 Fiber Model（Eq 22.35；随纤维速度梯度变化时设指数 ≠1；另给 Solidification Temperature 与 Blending Interval，液固混合按 Eq 22.36）；干纺：只在 Fiber Model 给 Eq 22.37 系数（指数 ≠1 可随速度梯度变化），**材料对话框中聚合物/溶剂流体的粘度一概不用**。**注意**：纤维粘度随速度梯度的取值可能使纤维模型方程数值失稳。

## 35.6 定义纤维（pp. 3669–3681）

- **主要输入**：起点坐标；组内纤维数（每根定义纤维可代表一组纤维，仅用于算源项）；喷丝孔直径；**单孔质量流量**（算喷丝出口速度，作纤维动量方程边界条件）；喷丝温度；喷丝溶剂质量分数（干纺，作溶剂连续性方程边界条件）；卷取点坐标；**卷取点速度或力**（动量方程第二边界条件，Eq 22.4）。
- **注入类型四种**：**single**（单纤维）；**line**（起点沿线等距排列——给起终点坐标 + Point Density Edge1）；**matrix**（仅 3D——矩形/平行四边形排布：第一行起终点 + 末行起点；每行 Point Density Edge1 个、Edge2 行；Numbers of Fibers Computed 字段可核对）；**file**（ASCII 表格：注释行以 `;` 开头任意多条；数据行 7 列 `x y z df m Tf Ys` = 坐标/纤维直径/质量流量/温度/溶剂液相质量分数（熔纺忽略）；**z 列 2D 也必须保留以维持解读顺序**）。
- **Fiber Injections 对话框**（Setup → Models → Fiber-Injections → Edit）：Create / Set...（改属性）/ Copy / Delete / **Initialize**（解变量重置为起点边界条件值；不选则全部初始化）/ **Compute**（按 Fiber Solution Controls 的迭代数手动解纤维方程；不选则全部）/ **Print**（每根纤维单独文件、自动命名，供外部后处理）/ **Read Data**（读回数据——与已有注入重名时询问覆盖）/ **Write Data**（ASCII——**数值与模型设置存 case，纤维与注入数据必须另存文件**）/ **Write Binary Data**（二进制）/ **List**（控制台列出：NO/X/Y/Z/U/T/SOLVENT/DIAM/MFLOW/FIBERS/CELLS/IN DOMAIN? 与卷取边界条件 VELOCITY 或 FORCE）。
- **Set Fiber Injection Properties**：命名 → 类型 → Injection Point Properties（single 给 x0/y0/z0；line 给起终点 + Point Density Edge1；matrix 给第一行起终点 + 末行起点 x2/y2/z2）→ **Number of Fibers in Group**（例：400 孔喷丝板按 line 注入 5 组则每组 80——数值上只解 5 根、每根代表 80 根参与源项计算；**该值作用于注入内全部纤维，各组数不同须拆分注入**）→ Diameter（喷丝孔直径）→ **Flow rate per Nozzle**（**单个喷丝孔**的流量，非整注入总量）→ Temperature →（干纺）Solvent Mass Fraction → Takeup Point Properties（**注入内所有纤维收于同一点**，不同则拆分；Boundary Condition 选 **prescribed-velocity**（已知卷取速度）或 **tensile-force**（给 0 = 模拟卷取点自由下落纤维））→ Grid Properties。
- **纤维网格**（每根纤维为注入点→卷取点的直线，划分有限体积单元；每根纤维独立网格）：**equidistant**（等距——Number of Cells）；**one-sided**（注入点侧加密——单元数 + Grid Growth Factor at Injection Point，>1 加密/<1 粗化）；**two-sided**（两端加密——两个生长因子）；**three-sided**（注入点侧 + 内部细化点两侧同比率加密——Number of Cells until Grid Refinement Point、两个生长因子、Location of Local Grid Refinement Point（无量纲 0–1，相对纤维长度）；点 **Compute** 估算细化点后单元数）。

## 35.7 UDF（pp. 3681–3687）

- 模板 **`fiber_fluent_interface.c`**（含拖曳/换热/传质系数与纤维属性的 UDF 源码）。准备：把 `addons/fiber` 目录**真实拷贝**（勿符号链接/快捷方式）到工作目录（Windows 用 VS.NET DOS 提示符；默认路径 `C:\Program Files\ANSYS Inc\v261\fluent\fluent26.1.0\addons\fiber\`）。
- 定制：编辑 `fiber/src/fiber_fluent_interface.c` 文件底部的函数组——摩擦因子（拖曳系数）、换热系数、传质系数、纤维粘度、纤维密度、纤维导热、纤维比热、汽液平衡。**不得另存文件名**；模板函数名 `user_friction_factor`、`user_heat_transfer_coefficient`、`user_mass_transfer_coefficient`、`User_Fiber_Viscosity/Density/Thermal_Conductivity/Specific_Heat/Vle` **不得改**（被模型其他例程调用）。示例照录：换热系数 UDF（Kase/Matsuo 1967——按相对速度算 Reynolds，Nud = 0.42·Red^0.334，α = Nud·k/d 存 fd->alpha[i]）。宏与类型定义在头文件 **fiber.h**（Fiber 类型与 FIB_* 宏）与 **fib-mem.h**（Local_Fiber_Data_Type）——**不得修改头文件**，否则编译库与 Fluent 不兼容报运行时错误。
- 编译：Linux `make -f Make-client FLUENT_ARCH=<arch>`（原文为 Makefile-client，如 lnx86）；Windows——拷贝目录 → VS.NET DOS 提示符 → 设 `FLUENT_INC` 环境变量 → `build_fiber_udf.bat` → 定义 `FLUENT_ADDONS` 指向自定义模块目录（全局设或 Fluent Launcher Environment 标签 Other Environment Variables，**路径不含空格**）。
- 挂接：编译成功后 Exchange 组的拖曳/换热/传质系数下拉出现 **user-defined**；纤维材料属性 UDF 勾 **Enable UDF Properties** 后在 User Defined Properties 组逐属性启用。

## 35.8 求解控制（pp. 3688–3690）

Setup → Models → Fiber-Controls → Edit：**Solve**——动量（Eq 22.4）/能量（Eq 22.11）/组分（Eq 22.1）三方程逐个开关；**Discretization**——每条纤维方程三种离散格式；**Underrelaxation**——全部纤维方程的欠松弛因子；**Convergence Criterion**——逐方程残差收敛判据；**Check Convergence**（关掉则只算固定迭代数）；**Relative Residuals**——按 Eq 22.20 算相邻两次迭代残差相对变化与判据比较；**Iterations**——每次纤维方程更新的纤维迭代数；**Reporting Interval**——残差打印间隔（**设 0 只输出最后一次，耦合求解时推荐**）；**Number of Fluent Iterations per Fiber Computation**——耦合求解中每次纤维更新前的 Fluent 迭代数；**Source Term Underrelaxation**——纤维源项向流体的交换欠松弛（收敛解不受其影响）。

## 35.9 后处理（pp. 3690–3697）

- **纤维位置显示**：Contours 的 Custom Field Functions... 类别选 **fiber-location**（取值 0 到单元内纤维单元数）；3D 可作等值面；或 **Fiber Mesh Display** 对话框（Results/Graphics/Fiber Mesh）——Nodes（纤维单元端点）/Edges（纤维路径线）/Draw Fluent mesh（同屏 CFD 网格）；Line Width 在 Style Attributes 中设；可 Show Single Fiber 按 Fiber ID 显示单根。
- **交换项**（Custom Field Functions 类别；**仅在耦合计算时更新与显示**）：fiber-mass-source（Eq 22.22）、fiber-x/y/z-momentum-source（Eq 22.21）、fiber-energy-source（Eq 22.23）、fiber-dom-absorption/emission（Eq 22.24/22.25）。
- **纤维变量 XY 图**：TUI `continuous-fiber → print-xy` → 输注入名 → 选 x 列与 y 列变量 → 存 xy 文件用 Fluent xy 绘图。可选变量：axial drag、conductivity、curvature、diameter、enthalpy、evaporated mass flux、heat transfer coefficient、lateral drag、length、mass flow、mass fraction、mass transfer coefficient、Nusselt number、Sherwood number、Reynolds number、specific heat、surface mass fraction、temperature、tensile force、user variable、velocity、velocity gradient、viscosity。注入内全部纤维的数据都存入；另可用 Print 存纤维 history 文件。
- **Fiber Display 对话框**（Results/Graphics/Fibers）：显示选项同 Fiber Mesh Display；着色可用上述纤维变量或 Fiber ID / Fiber Density / Fiber Tension；Levels 控制颜色渐变档数。
- **并行**：串并行皆可、无需额外输入；**纤维迭代全部在 host 进程执行**——纤维计算耗时多于并行流场迭代时整体性能受 host 限制；大量纤维时建议把 host 进程放在合适的机器上。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3659–3698（批次 100，2026-10-20，pypdf layout 模式提取；p. 3698 为仅含页脚的空页）。
- Theory Guide Eq 22.x（22.1–22.39 引用到者）公式体未提取，按引用记录变量与语义；两段 UDF 示例代码照录（排版符号有损处按语义记录）。
- Figures 35.1–35.17（对话框/示意图）为图形元素未摄取；Table 35.1 照录。
- 版本敏感：安装路径（v261）、模块号（2）、UDM 数（8）、编译命令以 2026 R1 为准。
- 相关页面：[[Fluent 气动噪声模型]]无关；辐射背景见 [[Fluent 热能模拟]]（P-1/DO 模型）；并行见 [[Fluent 离散相模型（DPM）]] 并行节。
