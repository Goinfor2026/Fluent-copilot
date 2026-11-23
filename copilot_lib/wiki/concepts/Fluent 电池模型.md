---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - battery-model
  - msmd
  - ntgk
  - ecm
  - p2d
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 电池模型

## 摘要

User's Guide 2026 R1 Part III / Chapter 32 "Modeling Batteries"（PDF pp. 3427–3536，两节）。Fluent 电池模型用 MSMD（多尺度多域）方法把整电池视为正交各向异性连续体，网格不受电池微观结构约束，在电池域解两个电位方程；电化学子模型四选——NTGK/DCIR（经验）、Equivalent Circuit Model（半经验）、Newman's P2D（最全面物理）、User-defined。另提供均匀热源法（CHT 耦合、FMU-CHT 耦合、Circuit Network）。**本页全章完成（批次 93–95，pp. 3427–3536）：32.1–32.2 全节，含熵热项、热滥用模型（一/四/N 方程+拟合与独立工具）、内外短路、肿胀算例、参数估计 TUI、初始化/材料/求解控制/预定义报告/后处理全变量清单。**精细电极尺度模型见 [[Fluent 电势场与电化学]]（Ch.31）。

## 32.1 引言（pp. 3427–3428）

- **MSMD 方法**：整电池为正交各向异性连续体；解两个电位方程；三种复杂度层次的电化学子模型——**NTGK/DCIR**（Newman-Tiedemann-Gu-Kim 与 Direct Current Internal Resistance）、**ECM**（等效电路）、**Newman's P2D**（伪二维）。此外提供均匀热源处理：**CHT coupling、FMU-CHT coupling、Circuit Network**（Theory Guide "Battery Solution Methods"）。
- **通用流程十步**：启动 → 读网格 → 缩放 → 加载模块并在 Battery Model 对话框定义参数 → 材料属性 → 操作条件 → 边界条件 → 计算 → 存 case/data → 后处理。手册以 GUI 为主，TUI 亦可完成多数任务。

## 32.2 MSMD 电池模型使用（pp. 3428–）

### 32.2.1 限制（p. 3429）

- 电池包仿真：**所有电池初始必须相同**（同类型同初值）。
- 电池包只支持 **nPmS 连接模式**（n 并联 × m 组串联）。
- 系统**正负极 tab 必须是连续面**，不相连的面不能并为一个实体。
- 正负 tab 之间必须经**真实 tab/busbar 导电体**或**文件定义的虚拟连接**连通。

### 32.2.2 几何定义（p. 3429）

MSMD/Cell Network 框架不解析集流体/正负极——电池是均质体，网格无需拟合电池内各层。须标认：**Active cell zones**（发生电化学反应；Battery Model 对话框 Conductive Zones 选项卡 Active Components 列表）与 **Passive zones**（tab 与 busbar，仅导电；Passive Components 列表）。电位场在活跃与被动区都求解。

### 32.2.3 设置（pp. 3429–3470）

启用：Setup → Models → Battery Model → Edit，勾 **Enable Battery Model**。对话框七选项卡——**Model Options**（通用设置）、**Conductive Zones**（活跃/被动区）、**Electric Contacts**（接触面与外部连接器）、**Model Parameters**（子模型参数）、**UDF**、**Advanced Options**（独立模式快速检查子模型行为与高级功能，详见 p. 3480，批次 94）。Apply 保存输入，Reset 恢复所有选项卡上次保存设置。

#### 32.2.3.1 Model Options 选项卡（pp. 3431–3439）

1. **Solution Method 四选**：
   - **CHT coupling**：每活跃区内均布热源（直接指定）；是否解电位方程取决于是否含被动区 Joule 热（无或一个）。
   - **FMU-CHT coupling**：热源由 FMU（functional mockup unit）计算；同样无或一个电位方程。
   - **Circuit Network**：热源由 Fluent 内电路网络计算；同样无或一个电位方程。
   - **MSMD**：未开 Reduced Order Method 时**每次迭代解两个电位方程**。
2. **Reduced Order Method（ROM）**：更快；使用前**必须先不开 ROM 跑至少 3 个时间步**，结果作为 ROM 参考电位场（条件见 Theory Guide ROM 节）。选 Circuit Network 或 ROM 时设 **Number of Sub-Steps/Time Step**——热与电化学计算的时间步比（如 10 = 电化学用 CFD 时间步的 1/10）。**重要**：内部短路处理需要两个电位方程——**只能配 MSMD，不能配 ROM**。
3. **E-Chemistry Models 四选**：**NTGK/DCIR**——经验模型，最简单最便宜、输入最少；与 Single-Potential Empirical 模型同用 NTGK 法，但连续解两个电位方程（而非带隔膜跳变条件的单方程）；**不能准确捕捉电池动态（惯性）响应**。**Equivalent Circuit Model**——半经验，动态行为预测能力有限。**Newman P2D**——最全面物理模型，计算昂贵、需大量电池基础信息输入。**User-defined E-Model**——须在可定制 `cae_user.c` 源码中提供 `user_defined_echem_model()` 空函数。
4. **Energy Source Options** 三开关（均默认开）：Enable Joule Heat in Passive Zones（tab 与 busbar 等被动导电区，Eq 19.3）、Enable Joule Heat in Active Zones、Enable E-Chem Heat Source。
5. **Solution Controls**：**Current Under-Relaxation Factor**——两电位方程的体积电流密度欠松弛，默认 **0.8**（多数够用），推荐 0.8–1.0；**Voltage Correction Under-Relaxation Factor**——默认 **1.0**，仅电位方程收敛困难时调小。（仅 ECM 与 P2D）**Cluster Cells** 电池聚类——**Static**：按 Nx/Ny/Nz（默认 1/1/1，首次运行推荐默认）把每电池活跃区划成 Nx×Ny×Nz 簇、以簇平均信息解子模型；纯几何、仿真前形成后固定。**Dynamic**：设 Number of Clusters 与 Target Variable（voltage 或 temperature，或 `DEFINE_BATTERY_CLUSTER` UDF 自定义）；每个时间步开始前动态成簇——按目标变量在活跃区的取值范围等分分簇、按值归簇。
6. **Electrical Parameters**：
   - **Nominal Cell Capacity**（单电池标称容量）。
   - **Life Model**：模拟容量随时间与充放循环衰减（见下节 Life Model）。
   - **Solution Options 六选**：**Specified C-Rate**（正=放电倍率/负=充电倍率；阴极 tab 总电流固定为 C-Rate×Nominal Capacity、阳极 tab 电位锚 0；**电流只按单电池标称容量算、不计连接信息**——如 2P2S 模块想一小时放空需设 C-rate 2）；**Specified System Current**（作用于阴极 tab，正=放电/负=充电）；**Specified System Voltage**（阴极 tab 电压，阳极 0 V）；**Specified System Power**（求解器保证系统电流×电压=功率，正=放电输出/负=充电输入）；**Specified Resistance**（外部短路仿真的 External Resistance，Ω；保证系统电压/电流=外阻）；**Set in Boundary Conditions**（直接在边界条件页设 UDS 边界）；**Using Profile/Data Table**（见下）。
   - **Echem Stop Criterion**：**Voltage 法**（Min/Max Stop Voltage）或 **SOC 法**（Min/Max Stop SOC）；每个时间步后检查，满足即自动停止仿真。

##### 32.2.3.1.1 Life Model（pp. 3436–3438）

- 参数：**Calender Time**（存储时间，Eq 19.50）、**Cycle Number**（已历循环数，Eq 19.51）、**Operation Temperature**（电池历史平均温度，Eq 19.50/19.51——**不是** CFD 仿真中的电池温度）。
- **Calendar Life Parameters**（按钮打开对话框）：Ref.Temperature（动力学参数的参考温度）、Pre-exponential Factor、Activation Energy、Exponent Value（时间指数因子）（Eq 19.50）。
- **Battery Aging Table**（循环寿命，NTGK）：容量衰减因子 2D 查找表（温度×循环数；各至多 **20** 层；Write/Read 文本表）；格式见 32.2.3.1.3。

##### 32.2.3.1.2 Profile/Data Table 电载荷（pp. 3439–3443）

- **Time-Scheduled**：三列 ASCII（.dat/.txt）——时间、载荷值、载荷类型（0 C-rate / 1 Current / 2 Voltage / 3 Power / 4 External electric resistance）。照录示例：0/500 s 15 A 放电（类型 1）→ 500.1/1000 s 60 W（类型 3）→ 1000.1/1500 s −1 C-rate 充电（类型 0）。**正=放电、负=充电；单位永远 SI**；线性插值——要捕捉突变更用小时间间隔。
- **Event-Scheduled**：五列——类型、值、转发条件 FC（1 Time>val、2 I<val 放电电流下限、3 I>val 充电电流上限、4 V<val 电压下限、5 V>val 电压上限、6 P<val 放电功率下限、7 P>val 充电功率上限、8 时间持续>val）、FC 值、停止旗标（0 继续/1 结束）。照录示例：1 C 放电至 3.5 V → 静置 300 s → 15 A 恒流充至 4.1 V → 4.1 V 恒压充至电流 > −1 A 停止。时间表皆可改写为事件表，反之不可。
- **Table Data**（快充）：充电电流 = f(平均 DOD, 温度) 的 2D 查找表；温度法选一个或多个温度 report definition——**对所选定义都查表取最小充电电流**。Fast Charging Table 对话框：插值法四选——**bilinear**、**staircase-floor**（DOD 取低值、温度线性插值）、**staircase-ceiling**（DOD 取高值）、**corner minimum**（取表最低角值）；照录 2×2 示例（T=300/310 K，DOD=0.2/0.3 → 10/5/20/10 A）：T=305 K、DOD=0.25 时四法分别得 11.25/7.5/15/5 A。表参数：Temperature Levels、DOD Levels、各值与电流幅值。

##### 32.2.3.1.3 电池模型中的查找表（pp. 3443–3445）

- 表为 tab/空格分隔 ASCII。**Plain text（.txt）2D 表六行结构**：`x-values` 头 + x 点行 + `y-values` 头 + y 点行 + `table-values` 头 + 数据行（照录容量衰减示例）。**3D 表**（仅内阻数据）：每电流层一段——`z-value <电流值>` + 该层 2D 表，依此重复（照录 z=-10/0/10 三段示例）。
- **Compact scheme（非 .txt，如 .tab）**：数据组括号包裹——2D `((300 310) (0 100 200) ((0 0) (0.1 0.15) (0.2 0.25)))`；3D `((-10 0 10) (三个2D表) 0)`——**末位数字为插值法，0=bilinear，此表必须用 bilinear**。跨仿真传输用 compact，手写数据用 plain text 更可读。

#### 32.2.3.2 Conductive Zones 选项卡（pp. 3445–3446）

选 Active Components（电池单元）与 Passive Components（tab 与 busbar）；Display Active/Passive Components 按钮自动勾选相关组件打开 Mesh Display。**不同电池的活跃区或被动区可分组合并以减区数、提升性能**。

#### 32.2.3.3 Electric Contacts 选项卡（pp. 3446–3449）

- **Contact Surfaces**：选接触面区并设 **Specific Contact Resistance**（接触电阻）。
- **External Connectors**：真实连接时定义系统负/正 tab；虚拟连接勾 **Use Virtual Battery Connection** 并给连接定义文件。两种格式：
  - **tab surface-based**：`mP 2` / `nS 2` / 逐行 `tab_N_xPyS tab_P_xPyS` 对（1P1S…mP1S 到 1PnS…mPnS 顺序；照录 2P2S 示例）。定义后 Fluent 自动检测电池网络连接。
  - **active zone volume-based**：`mP 1` / `nS 4` / 逐行活跃区名（每电池一行；多 cell 体积同行空格分隔，照录 cell_1_a cell_1_b cell_1_c 示例）。**此格式只能用于无 Joule 热的 Circuit Network 法**（包内电流通道未定、电位场与 Joule 热解不了）；导入时自动启用 Circuit Network 并禁 Joule 热、Conductive Zones 按文件自动更新。
- 定义/修改后点 **Print Battery System Connection Information** 核对控制台连接信息有无错误。

#### 32.2.3.4 Model Parameters 选项卡（pp. 3449–3470+）

只显示所选解法/子模型相关参数入口。

##### 32.2.3.4.1 CHT Coupling 输入（p. 3450）

每活跃区 **total Energy Source** +（考虑被动区 Joule 热时）**Tab Electric Current**；均为 constant 或已导入瞬态 profile。瞬态 profile 按内置格式读入（.ttab 表格瞬态；照录 energy-source 示例——首行名称/字段数/行数/周期旗标，次行字段名必含 time，其余为数据）；profile 存入 case 文件。包仿真同热源时勾 **Use Same Settings for All Zones** 只填一套。

##### 32.2.3.4.2 FMU-CHT Coupling 输入（p. 3451–3452）

①**Define Output Parameter-Tcell**——为每活跃区创建平均温度输出参数；②**Open FMU Dialog Box** 用这些温度定义 FMU 输入参数（FMU 导入详见 p. 1050）；③Energy Source Mapping 为每活跃区选 FMU 输出参数作能源项；（含 Joule 热时）Tab Electric Current 同 CHT。

##### 32.2.3.4.3 NTGK/DCIR 输入（pp. 3452–3462）

- **Initial DoD**（DOD=0 时的初始 DOD；默认 0 = 满电）；**Reference Capacity**（实验取参数用的容量，Eq 19.5；可与标称容量不同）。
- **U/Y 参数**（Eq 19.7）数据类型五选：**Polynomial**（U Coefficients/Y Coefficients 组直接填多项式系数与温度修正）；**Table**（每参数 2D 表——**DOD 至多 50 层、温度至多 20 层**；U Table.../Y Table... 对话框；Write/Read；格式见 32.2.3.1.3）。**默认值取自 Kim 论文 315，模型电池不同必须另给参数**（极化参数基于电池极化测试曲线）。
- **Raw Data**：Import Testing Data 导入不同温度与 C-rate 的放电曲线（Load Discharging Files）；可选 **Capacity Fade Effect**——导入后自动生成容量衰减表（可查不可改；**开关状态改变须重新载入数据重处理**）。导入后无需其他输入——求解器存 U~I 关系直接使用。
- **Internal Resistance**（DCIR 法）：Internal Resistance Table... 开 3D 表——Electric Current Levels 数、Selected Current Level、Current 值、温度层/DOD 层/各对电流幅值（**正=放电、负=充电——充放电可用不同内阻**）；逐电流层重复；可写/读文件。可选开 **U Table** 提供开路电位（每 DOD-温度对）。**告诫：无 U 表时只能用 current 或 C-rate 载荷，且只能单电池或纯串联连接**。
- （非快充）**Limiting Current**：启用后 Temperature Method 选 report definition(s)，Current Limiting Table... 设限流 3D 表（输入同快充表）。
- **Parameter Estimation**（拟合 U/Y）：输入——Testing Battery's Capacity（自动取自 Reference Capacity，须核对）、**Number of DOD Levels（10–20，默认 20 推荐所有工况）**、Minimum/Maximum DOD（默认 0.01/0.95）、至少**两个不同 C-rate** 的放电数据文件（不同温度可多文件；每 C-rate 一个文本文件；格式照录：首行 `Crate 1.0`、次行 `Temperature 300.0`、其余时空格分隔时间-电压对）。可选 Capacity Fade Effect（**拟合结果依赖该开关，改变须重拟合**）。Load Discharging Files → **Fit Parameters**——多温度时逐温度拟合、结果以 Table 类型自动传入（Table 类型自动选中）；单温度时 Polynomial 与 Table 都填、Polynomial 为默认。Visualize Fitting Results 组按温度×C-rate 对比拟合与实验曲线。U Function/Y Function 选参 Plot 随 DOD 作图（Polynomial/Table 类型）。NTGK 参数估计工具另有 TUI 入口（p. 3525）。

##### 32.2.3.4.4 ECM 输入（pp. 3462–3470）

- **Initial State of Charge**（默认 1 = 满电）；**Reference Capacity**（Eq 19.9）。
- 电阻 Rs/R1/R2、电容 C1/C2、开路电压 Voc 数据类型四选：**Chen's original**（Eq 19.11 全系数）、**Polynomial**（Eq 19.10 系数）、**Table**（每参数 2D 表，同 NTGK 表法）、**Parameter Estimation**。**默认值取自 Chen 文献，电池不同须另给**。可选 **Use Different Coefficient for Charging and Discharging** 并另给充电参数。
- **Parameter Estimation**：输入——Testing Battery's Capacity（核对）、**Circuit Model**（4P Parameter Model 单 RC 环 / 6P Parameter Model 双 RC 环）、**Fitting Method**（**JH** Jiang-Hu 法仅用弛豫段数据；**LM** Levenberg-Marquardt 法用脉冲+弛豫段；LM 先自动跑 JH 作初值，失败打警告不画线）、HPPC 测试数据。Capacity Fade Effect 开时须载放电曲线（格式同 NTGK 工具），衰减表自动生成不可改。
- **HPPC 文件**：不同 SOC 与温度各一文件；每温度至少一个有效 SOC；SOC 范围应覆盖 CFD 仿真范围。格式照录：首行 `SOC 1.0`、次行 `I 14.6`（脉冲电流）、三行 `Temperature 300.0`、其余时间-电压对；**须含静置段、脉冲段、弛豫段**。加载两法：Load User's HPPC Test Files（多选 Ctrl/Shift，Remove 可剔除）或 **Import Files from HPPC Library**（对话框选库、Summary 显示信息）。
- **Fit Parameters**：多温度→逐温度拟合、Table 类型自动选中；单温度→Polynomial 默认；含充放两组曲线→**工具跑两次**并自动选 Use Different Coefficient、结果分别进 Discharging/Charging Parameters 组。**选型建议**：每条 SOC 曲线数据要足够多；6 参数电路物理更多、4 参数更稳健；JH 比 LM 稳健——先试 6P，不满意换 4P。Visualize 按 Temperature×SOC 对比（充放数据分别可视化）。Chen/Polynomial/Table 类型可 Plot Rs/R1/R2/C1/C2 与时间常数 R1*C1/R2*C2 随 DOD 曲线。ECM 工具另有 TUI 入口（p. 3526）。
- **HPPC Library**：自带库仅 **Generic-Cell** 一个电池（示范目录结构用）；位于 `path/fluent26.1.0/addons/msmdbatt/hppc_database/`（如 `C:\Program Files\ANSYS Inc\v261\fluent\fluent26.1.0`）。标准 HPPC 测试=特定温度与 SOC 下脉冲电流测电压响应（依赖脉冲性质/幅值/温度/SOC）。命名约定：电池名任意但**容量必须在括号内带 "A h" 单位**；一级文件夹名必须是 **discharge 与 charge**；二三级文件夹数与名任意。可自建库放同目录共享。**告诫：参数估计工具目前只能取 discharge 支路、且只处理单一 C-rate 层**（不同 C-rate 当不同库；charge 支路暂未用、未来版本支持）。

##### 32.2.3.4.5 Newman's P2D 输入（pp. 3470–3478）

- **Theoretical Capacity** 由所输 Newman 参数自动算出并显示。**Initial SOC** 默认 1 = 满电。
- Positive/Negative Electrode 与 Separator 三列各设：**Thickness**（Eq 19.32）、**Number of Grids**（离散该区网格点数）、**Grid Size Ratio**（偏置网格；默认 1 = 均匀）、**Particle Diameter**、**Specific Area**（电极多孔材料比表面积；**仅 BPX 导入时出现**）、**Number of Grids in Solid** 与 **Grid Size Ratio in Solid**（颗粒球离散）、**Cs,max**（固相最大锂浓度，Eq 19.20）、**Stoi. at 0%/100% SOC**（算理论容量与初始锂浓度用）、**Init. Cs**（电极初始锂浓度）、**Init. Ce**（电解液初始锂浓度）、**VOF of Electrolyte**（Eq 19.21）、**Filler Fraction**（Eq 19.30）、**Ds**（25°C 参考温度固相扩散系数）、**Activation Energy E_d**、**Brugg**（Bruggeman 迂曲度指数，Eq 19.21；**仅非 BPX 导入时可用**）、**Tran. Efficiency**（多孔介质输运效率；**仅 BPX 导入时可用**——否则按 Bruggeman Eq 19.21/19.22 算）、**Conductivity**、**Ref. Rate Constant**（25°C）、**Activation Energy E_r**、**Trans. Coef. a/c**（Eq 19.20）、**OCP**（开路电位，Eq 19.19；通常是锂化状态 sol 比的函数，piecewise-linear 或 UDF）、**dU/dT**（熵变系数）、**De**（电解液 Li+ 扩散系数）、**E_de**（Eq 19.29）、**t+ Factor**（迁移数）、**Ionic Cond**（Eq 19.22）、**E_k**（Eq 19.28）、**Activity Term**（Eq 19.23）。
- OCP、扩散系数、电导率、迁移数、活度项可用 constant / piecewise-linear / polynomial / UDF（`DEFINE_BATTERY_PROPERTY`）。
- **echem 材料数据库**：Material Database 按钮——Material Type 选 anode/electrolyte/cathode，Name 列表选材（Properties 只读展示），**Copy** 复制到 Newman Model Parameters 各字段。**Import BPX File**——BPX（Battery Parameter eXchange）为共享物理锂电模型参数的开放标准（json）；载入后自动创建 Import-BPX<ID> 命名材料供 Copy。**BPX 与 Fluent 公式三处差异**：①比表面积——Fluent 由孔隙率与颗粒直径算出（GUI 不直接输），BPX 显式给出；②迂曲度——Fluent 用 Bruggeman 关联（指数），BPX 用 transport efficiency 参数；③Butler-Volmer 反应速率常数——导入时按公式从 BPX 速率值换算（含 BPX 速率常数、固相最大锂浓度、参考电解液浓度）。数据库文件位于 `<安装目录>/fluent/fluent26.1.0/addons/msmd-batt/lib/echem_database.scm`，可自行扩充。
- **Use Analytical Cs**：固相锂扩散方程的降阶解析解（文献 [90]），需给 **Cs Function Order**；默认数值离散求解。
- **Include Aging Effects**：把老化效应作为**稳态输入 profile** 进 P2D——可选导入自定义 profile 文件（随 case 存储；若 profile 由 32.2.3.6.2 独立模式寿命模型生成则已在 case 中无需导入），再从 Select Aging Effects Profiles 选一个；profile 含 SEI 浓度、表面膜电阻、孔隙率等老化信息。
- **Include Swelling Effects**（P2D 肿胀）：展开后 Positive/Negative Electrode（及 Separator）列设 **Swell Coefficient**（活性颗粒体积增长率 vs 归一化锂浓度，Eq 19.74）、**Young's Modulus**（Eq 19.77/19.84/19.85）、**Neutral Swell SOC**（肿胀中性 SOC——**Thickness/Particle Diameter/VOF of Electrolyte/Filler Fraction 都按中性 SOC 给值**，肿胀计算中真实值在其附近波动）；再设 **Electrode Layer Orientation**（Eq 16.41；Figure 32.22）——**Pouch Cell**（Layer Normal Vector XYZ）、**Cylindrical Cell**（Cylinder Axis Vector XYZ）、**Rounded Prismatic Cell**（Cylinder Axis Vector + Vector Connecting Two Origins 两矢量）、**UDF**（`DEFINE_BATTERY_SWELL_LAYER_N`，复杂几何）；肿胀算例设置见 p. 3523（批次 95）。**P2D 默认参数取自 Cai & White 文献 [90]，电池不同须另给**。（独立模式 P2D 肿胀另可选 **Mechanical Load Type**：External Pressure——电极层端部外法向力，正值=压缩，Eq 19.83；Total Deformation——电极层总厚度变化百分比，Eq 19.84 右端；External Stiffness——外部约束有效刚度，Eq 19.85。）

##### 32.2.3.4.6 User-Defined E-Model 输入（p. 3478）

User-Defined E-Chem Model Parameters 三项：**Number of Memories per Cell**（每计算单元需保存的子模型参数个数）、**Initial SOC**、**Reference Capacity**（Ah）。

#### 32.2.3.5 Hooking UDF（p. 3479）

UDF 选项卡为各电池模型参数挂 UDF；可用宏清单见 Customization Manual "Battery Model DEFINE Macros"。

#### 32.2.3.6 Advanced Options 选项卡（pp. 3480–3510）

九大功能：①独立模式快速检查电化学模型；②独立模式跑物理寿命模型模拟老化；③Battery Pack Builder 从已有模块与冷板算例组装电池包；④LTI-ROM/SVD-ROM 训练数据创建与 SVD-ROM 结果后处理；⑤为全部活跃区定义正交各向异性导热；⑥（仅 NTGK 与 ECM）经验肿胀模型配 FSI；⑦电池 venting 模型；⑧熵热项；⑨热滥用分析。

##### 32.2.3.6.1 独立模式 Echem（pp. 3481–3485）

Run Echem Model Standalone... → 对话框设 **Report Time Step**（结果保存/报告间隔）、**Total Run Time**、**Reference Temperature**（P2D+肿胀专属 **Mechanical Load Type**，见上）；点 **Draw Profile** 启动；完成后 Plot Profile Data 对话框看结果——**NTGK**：`ntgk-time-history-profile`（soc/voltage/current/power 随时间）；**ECM**：`ecm-time-history-profile`（同上 + v1/v2，Eq 19.9）；**P2D**：`p2d-time-history-profile`（current/voltage/power + ce_x/cs_x/phis_x/phie_x 于 x=lnsp/lns/ln/0 四位置——正极外表面/正极-隔膜界面/隔膜-负极界面/负极外表面的电解液锂浓度、活性材料表面锂浓度、固相电位、液相电位）与 `p2d-field-profile`（仿真末空间分布：phi_e/phi_s/ce/cs_center/cs_average/cs_surf）。**X-Y 图变量一律 SI 单位**。

##### 32.2.3.6.2 独立模式老化（pp. 3485–3490）

前提：Model Options 选 **Newman P2D**、Solution Options 选 **Using Profile**、Time/Event-Scheduled 给单个载荷循环 profile。Advanced Options → Run Echem Model Standalone → 勾 **Enable Physics-Based Battery Life Model**；除 Report Time Step/Reference Temperature 外设 **Total Run No. of Cycle**（载荷 profile 自动循环次数；**大量循环前先用少循环（如 <20）做 sanity check 并估时**）。参数：**SEI Growth Parameters**——EC Conc.、EC Diff.（Eq 19.63）、SEI Dens./MW（Eq 19.65–19.67）、SEI Cond.、Ref. Rate Const.、Trans. Coef. c、Eq. Potential（Eq 19.61）；**Include Lithium Plating**——Li Dens./MW（Eq 19.65–19.67）、Ref. Curr. Dens.、Trans. Coef. c、Eq. Potential（Eq 19.62）、**Frac. of Li forming SEI**（Eq 19.59–19.60）。**Solution Controls**：**Aging Speed Multiplier**（每循环后 SEI 与析锂浓度循环增量的放大因子）、**Save Aging Effects Profile per N Cycles**（保存间隔）、**Start from Aged Battery**（从老化电池起算——profile 导入一次存 case，删除或同名覆盖前一直有效）、Import Aging Effects Profile 文件、Aging Effects Profiles 下拉选初条件。Draw Profile 启动。**输出**：`p2d-time-history-profile` + `aging-cycle-history-profile`（每循环末记录：cs_sei_x=lps、cs_li_x=lps（mol/m³）、r_film_x=lps（Ohm·m²）、theoretical_capacity（Ah/m²）；x=lps 为隔膜-负极界面）；老化效应 profile 存 `aging-field-profile.prof`——名为 `aging-cycle-<number>`，每 profile 含循环末一维空间场：x（负极网格中心坐标 m）、cs_sei、cs_li、eta_sei、eta_li（两反应过电位 V）、j_sei、j_li（孔壁电流通量 A/m²）、delta_film（负极颗粒表面膜厚 m）、r_film（表面膜电阻 Ohm·m²）、por_e（电解液孔隙率）。**两类复用**：Scenario A——Start from Aged Battery 作独立仿真初条件（自定义 profile 至少含 x、cs_sei，可选 cs_li 缺省为 0）；Scenario B——CFD 中 Model Parameters 勾 Include Aging Effects 作**时间冻结快照**输入（自定义 profile 至少含 x、c_sei、r_film、por_e）。profile 的 x 坐标（网格点数/负极厚度）与 P2D 网格不同时自动映射。

##### 32.2.3.6.3 Battery Pack Builder（pp. 3490–3494）

从已有"电池模块 case"+"冷板 case"在 Fluent 内组装电池包（两 case 均须设置完备；冷板几何须朝向正确；有 data 文件自动加载）。Advanced Options → Battery Pack Builder...：
- **模块定位两法**：①手动——Total Number of Modules + 逐模块 Translation/Rotation Info（Tran_x/y/z 平移；Orgin/Axis/Angle 旋转——**先旋转后平移**；通用连接另设连接模式 NS/NP，Series Connection 选项勾上则全串联无需连接数据）；②**Import Module Location File...** 文本文件——每行 12 个数：平移 xyz、旋转原点 xyz、旋转轴 xyz、旋转角、连接信息 NS NP（外层再包一对括号；照录三模块串联示例与并联时末两列的 1 1/1 2/1 3 写法）；导入后字段自动填充可编辑；Export Module Location File... 可导出。
- **Build Battery Pack**：逐个装载模块再装冷板；**覆盖既有几何**为组合包几何；为便于识别，模块内实体加前缀 `module#`（串联用序号；通用连接用 1s1p/1s2p…），冷板实体前缀 `coldplate`；控制台打印包连接信息（例：2S3P 模块连接、每模块 8s1p）。
- **注意**：模块与冷板的对齐（接触面共面）由用户负责；逐模块 append 耗时（控制台打印计时）。
- 第 4 步 **Create NCI**：在 Non-Conformal Pairing Faces 多选列表选配对面（**强烈建议手选**——不选则全列表搜索、大列表很慢）后点 Create NCI——自动检测接触面、一对一法生成非一致界面并列于 Mesh Interfaces；Display Selected Faces / Display NCI Pairs 可视化。
- 第 6–7 步：核查求解器（稳/瞬态）与模型（能量方程等）与包级电载荷；**液冷等流量场不变时可冻结流场**，仅点 Battery Model 对话框 **Init** 按钮初始化电池模型开始仿真。
- **限制**：Pack Builder 产出的 case **不能**再作为模块 case 输入。

##### 32.2.3.6.4 Battery ROM Tool Kit（pp. 3494–3504）

背景：CFD 对系统级瞬态热分析太大太慢——**LTI-ROM**（线性时不变：输入=功率/热源，输出=指定点或区域平均温升；完全由脉冲响应刻画，任意输入的输出=卷积；实际加单位阶跃监测响应，脉冲响应=阶跃响应的时间导数）与 **SVD-ROM**（SVD 分离温度场时空贡献、保留前几个主导奇异值与左奇异矢量构成降维空间、在其中套 LTI）。**LTI 成立条件**：恒流量、恒物性、线性边界条件（辐射边界非线性不满足）；水冷系统假设相当准，空冷在温变范围内亦可。LTI-ROM 只能给单元平均或点温度，场温度需 SVD-ROM。**Fluent 生成的 SVD-ROM 文件可用于 Ansys Twin Builder 跑系统仿真**（详见技术支持）。Advanced Options → Battery ROM Tool Kit... 三选项卡：
- **ROM Data Creator**：ROM Type 选 LTI 或 SVD。ROM Input Parameters——**Volume Heat...**（Select Volumes：Value 填热源值、选区后 Add as a Group（组参数——热源在组内均分）或 Add Individually（逐区参数）；Remove 移除；组内分配可 Edit Group Value... 逐区指定）、**Face Heat Flux...**（可 **With Profile** 给面通量分布——纯文本四列 `x y z flux_value`，仿真中归一化使总通量匹配设定值）、**Face Temperature...**；（Model Options 勾了 Enable Joule Heat in Passive Zones 时）**Input Tab Current for Joule Heat** 可解电位方程并给电流边界。**LTI-ROM Output Parameters**——Cell Zone Average.../Face Zone Average.../User Surface Average.../User Point.../Report Definition...（区域平均温度/点温度/报告定义的温度响应；组参数可 Show Group Entities 查看成员）。**SVD-ROM Output Parameters**——Exported Temperature Zone... 选导出温度的区。**Transient Setup**：Time Stepping **parametric**（默认）——Parameters：Initial/Max Time Step Size、Time Step Increment Factor、Number of Time Steps（同一步长的步数）、Max Iterations per Time-Step；Stop Condition：**Max Time** 与 **Max dT_duration/T_range to Stop**（所有监测温度的"温变/时长÷温度范围"低于阈值即提前停）；Reset to Default Settings 可复位；**file** 法——时间步进文件三列（时间步/步数/每步最大迭代；照录示例）。**File Saving Frequency**（默认不存）：Volume Heat Run/Face Heat Run/Face Temperature Run/Joule Heat Run 各设保存频率（设 1 全存、2 存一半……）。**Run Training**：按输入参数逐个顺序跑瞬态训练（训练次数=输入参数个数）；每个从初始时间步开始、按因子增大步长直至 Max Time 或满足停止条件；结果存工作目录 **LTI/** 或 **SVD/** 文件夹，供 Twin Builder 使用（LTI-ROM 也可直接用 LTI-ROM Generation 工具生成的文件）。
- **LTI-ROM Generation**：Response/Input File Location 指定响应文件目录；Control Parameters——**State Space Model Min/Max Order**（阶高更准更慢；输 0 时依 Tolerance for 0th Order 可能仍忽略交叉加热贡献）、**Target Relative Error**（越小阶越高）、**Tolerance for 0-th Order**（贡献 < 容差×最大贡献的输入（如某些交叉加热）被忽略，显著缩小模型）、**NonZero StepRes Slop**（No/Calculate/Provided——全绝热边界时阶跃响应永不稳态、曲线带斜率，可让求解器算或手动给）。**Generate LTI-ROM**：使用目录内 Input_PortNames.txt、Input_StepInputValues.txt 与全部响应文件拟合，生成状态空间方程系数矩阵存 **Thermal_ROM_Matlab.m**（任何能解状态空间模型的系统仿真软件可用）；GUI 设置自动存 **Input_ROMconfig.txt**（Load Config... 可回读）。
- **SVD-ROM Post-Processing**：输入 One of Basis File 与 Transient Coefficient File——重建并显示各快照时刻的 3D 温度场、可做动画（详见技术支持）。

##### 32.2.3.6.5 正交各向异性导热（pp. 3505–3506）

电池是卷绕/叠层三明治结构，面内导热远大于跨面方向。两法定义：①Create/Edit Materials 逐电池建材料设（圆柱）正交导热（每电池独立原点与轴，繁琐易错）；②内置工具——Advanced Options → **Orthotropic Material...** → 勾 **Use Orthotropic Thermal Conductivity for Each Battery** → 选 Pouch/Cylindrical/Rounded Prismatic + 方位矢量（同 P2D 电极层取向）→ 设 **Layer Normal 与 Layer In-Plane 导热分量** → OK——工具自动定各活跃区原点并施加到全部活跃区。**Pack Builder 联动**：由此设置的属性会带到各模块，其他模块中电池的圆柱原点与轴按模块位置与朝向自动更新。**两条告诫**：方位检测要求**每电池单个固体活跃区**（否则检测可能错）；多电池时**所有电池方位必须一致**。

##### 32.2.3.6.6 经验肿胀模型（pp. 3506–3507）

**仅 NTGK/DCIR 与 ECM** 可配 FSI 耦合（Theory Guide "Empirical-Based Swelling Model"）。步骤：E-Chemistry 选 NTGK/DCIR 或 ECM → Advanced Options → **Battery Swelling Model...** → 勾 Include Swelling Effects → 设 **Swell Coefficient、Neutral Swell SOC、Electrode Layer Orientation**（控件同 P2D）；自定义肿胀应变用 **Customize Swelling Strain** + 编译好的 `DEFINE_BATTERY_SWELL_STRAIN` UDF（Swelling Strain UDF 下拉选）。同样适用两条方位告诫（单活跃区、方位一致）。

##### 32.2.3.6.7 电池 Venting 模型（pp. 3507–3510）

Advanced Options → **Battery Venting Model...** → 勾 Venting Model → **Gas Release Faces** 选排气面（**只列出电池活跃区与流体区之间的面**）→ Options：无多相时 **Species Model** 三选——`species-transport-w/o-reaction`（不考虑排气后燃）、`eddy-dissipation-model` 或 `eddy-dissipation/finite-rate`（排气气体燃烧重要时；两者差异见 Theory Guide Volumetric Reactions）；多相时用 **Phase of Venting Gas** 下拉选排气进入的相。**Venting Gas Composition...** 调排气混合物各组分质量分数（改混合物本身见 Material Types and Databases p. 1652）。**Venting Gas Release Method** 两法：**Using Abuse Rate**——按热滥用模型给每电池产气参数（One-Equation：Released Gas Mass，Eq 19.46；Four-Equation：SEI Decomposition / Positive-Solvent / Negative-Solvent / Electrolyte Decomposition 四反应，Eq 19.47；N-Equation：每滥用反应的产气量，Eq 19.48）；**Using File Input**——**Activation Temperature**（激活排气温度）+ 排气速率文件（空格/Tab 分隔三列：时间 s、排气温度 K、排气速率 kg/s；照录示例）。后处理：Battery Variables... 类别新增 **Venting Gas Mass Source**（显示排气加入位置；体积积分=总排气速率 kg/s）。**注意：当前版本未实现 venting 阀门模型**（需要时联系支持）。

##### 32.2.3.6.8 熵热项（pp. 3511–3512）

任一电化学子模型都可在热源计算中计入熵热（Eq 19.8/19.13/19.32）：勾 **Include Entropic Heat** → Data Type 二选——**Data Table**（dUdT Table... 查找表：Temperature Levels/Soc Levels/各值/每 SOC-温度对的 dUdT；操作同 Battery Aging Table；**Different Table for Charge/Discharge** 可分别设放电表 dUdT Table for Discharge... 与充电表 dUdT Table for Charge...）或 **UDF**（编译 `DEFINE_BATTERY_ENTROPIC_HEAT` 挂 Entropic Heat UDF 下拉）。**注意**：Newman P2D 算例的熵热可直接在 Model Parameter 选项卡给正/负极各自的 dU/dT（见 32.2.3.4.5），也可给单一合并值——**切勿同时给个体值与合并值导致熵热重复计算**。

##### 32.2.3.6.9 热滥用模型（pp. 3512–3522）

勾 Thermal Abuse Model 后展开参数；热失控反应动力学模型三选——**One-Equation / Four-Equation / N-Equation**（理论见 Theory Guide "Thermal Abuse Model"）。

- **One-Equation（32.2.3.6.9.1）**：Abuse Reaction Rate Type 三选——**Arrhenius**（Parameters for Kinetics Model 组给电池常数 A、E、HW、m、n 等，Eq 19.35–19.36，及初始反应进度）；**Table Data**（Initial Reaction Progress Variable、Specific Heat Release HW（Eq 19.36）、Abuse Reaction Rate Table...——温升速率 dT/dt 随温度的表（Temperature Levels/Temperature/Rate dT/dt），控件同 Battery Aging Table）；**UDF**（同前两项 + 编译 `DEFINE_BATTERY_ABUSE_RATE` 算 Eq 19.35/19.36 速率）。**Enable Internal Short Heat**（内部短路反应 Eq 19.44——滥用反应的引发与传播）：Internal Short Heat Reaction 组给 A_ec（指前因子）、E_ec（活化能）、H_ec（短路电化学反应热，Eq 19.41）、T_trigger（触发温度，Eq 19.45）、Soc（反应进度变量，Eq 19.44）。
- **Four-Equation（32.2.3.6.9.2）**：电池常数（Eq 19.37–19.41）+ 四个反应进度变量初值；内部短路同上。可从 Fluent 数据库导入滥用反应动力学——Material Database 按钮 → Material Database for Abuse Kinetics → Available Material List 选正极材料（Properties 展示反应属性）→ **Copy**（名字进 Material Name、动力学自动填入各反应组）。
- **N-Equation（32.2.3.6.9.3）**：Total Number of Abuse Reactions + 每反应动力学参数（Eq 19.42–19.43）与初值；直接输入或 **Import Abuse Reaction Rate File**——每行 8 个速率参数、空格/Tab 分隔、外层再包一对括号（照录 7 反应示例）；**Export Abuse Reaction Rate** 可存他案复用；内部短路同上。
- **Fitting Tool/Standalone（32.2.3.6.9.4）**：Fitting Tool/Standalone Model... 按钮 → 选 **Fitting Tool**（参数估计）或 **Standalone Model**（CFD 前预演滥用反应并可视化）。Common Inputs——**rho*Cp**（体积热容）、**T0**（初温）、**Adiabatic?**（非绝热另给 Volume、Area、T_conv、T_rad、h、epsilon）。Standalone 专属：Time Step、Total Time；**Compare with Experimental Data**（ARC 实验文件——两列时间-温度纯文本）；Plot Of 四选（Temperature Profile / Heating Rate vs Time Profile / Heating Rate vs Temperature Profile / Reaction Progress Variable Profile）→ Plot Graph。Fitting 专属：Initial alpha（Eq 32.1 反应进度初值，对应第一个实验点）、Data Include Peak Temperature（数据未含反应全程时必须给 Total Temperature Increase）、Fix Exponent of alpha/(1-alpha) Term（固定则给 Exponent Value）、File Name（两列时间-温度）→ **Fit Data**。**注意**：拟合工具仅限一方程模型；GUI 拟合只能一组数据——多组用 TUI（32.2.4.2.3）。
- **仅跑热滥用模型（32.2.3.6.9.5）**：勾 **Run Thermal Abuse Model Only (Battery Model is Turned off)** 只解能量方程（Eq 19.3）；否则两个电位方程（Eq 19.4）也解。**注意**：热滥用动力学参数是电池材料专属的，默认设置可能不适用——必须自备参数；一方程模型可用 TUI 参数估计工具从烤箱测试数据求动力学参数——拟合完成后以 Arrhenius 与 Table Data 两种格式同时传入（对应字段自动填充），实验条件传给 Fitting/Standalone 对话框，可跑独立模型评估拟合质量并微调。

##### 32.2.3.7 外部与内部短路电阻（pp. 3522–3523）

- **外部短路**：Model Options → Specified Resistance + External Resistance（见 32.2.3.1）。
- **内部短路**：强度由体积接触电阻决定，存于预定义 UDM **Short Circuit Resistance**；默认极大值（无内短）。两种设法：①**Patching**——把接触电阻 patch 到短路区（Region Register 对话框建区域 cell register）；②**UDF**——`DEFINE_ADJUST`/`DEFINE_ON_DEMAND` 用 UDM 宏 `C_BATTERY_SHORT_R(c,t)` 设接触电阻（可为位置与时间的函数）。**内部短路模型仅限 MSMD 解法**。

##### 32.2.3.8 电池肿胀算例设置（pp. 3523–3524）

①Model Options：Solution Method 选 **MSMD 或 Circuit Network**，E-Chemistry 选 **P2D / NTGK-DCIR / ECM** 任一。②肿胀参数：NTGK/ECM 走经验肿胀（32.2.3.6.6）；P2D 走其肿胀输入（32.2.3.4.5）。**肿胀启用后电池活跃区材料的 Young's modulus 自动设为正极/负极/隔膜三组肿胀输入的平均值**。③按 intrinsic FSI 流程设结构模型（Ch.29，p. 3345）——Structural Model 对话框 **Battery Effects 自动选中**。④给全部电池壁面区设边界条件。⑤要模拟肿胀变形后的绕流则设动网格：Mesh Methods 选 **Smoothing**，Mesh Method Settings 选 **Linearly Elastic Solid**；Dynamic Mesh Zones 对话框中为每个预期显著变形的区选 Type = **Intrinsic FSI**（其余默认即可；**建议为电池表面相邻的所有流体区都建**）→ Create。

### 32.2.4 参数估计工具（pp. 3524–3529）

NTGK、ECM、一方程热滥用模型的参数是电池专属的，理论上可从标准测试数据拟合；GUI 与 TUI 双入口。GUI 入口分别在各自输入节（NTGK p. 3452、ECM p. 3462、热滥用 p. 3512）。

- **TUI 总入口**：`define/models/battery-model/parameter-estimation-tool` → Model option 1 NTGK / 2 ECM / 3 Thermal Abuse。
- **NTGK TUI（32.2.4.2.1）**：逐温度层输入文件名（顺序无关；可用 `*`/`?` 通配；输 quit/q 或回车结束文件循环）；提示——Battery capacity（自动传入 Reference Capacity）、**Number of DOD-levels（正文称默认 30 通常够用；示例会话显示 [20]——两处照录）**、Include Capacity Fade Effect。单温度数据时 Polynomial 与 Table 都回填、Polynomial 自动选中。完整会话示例照录（ntgk-*.dat 通配 15 条曲线、容量 [14.6]）。
- **ECM TUI（32.2.4.2.2）**：HPPC 数据逐 SOC 一文件；每温度至少一个有效 SOC、SOC 范围须覆盖仿真范围；提示——Battery capacity（工具并不需要但必须给）、Circuit Model 1=4P（单 RC）/2=6P（双 RC）、Fitting Method 1=JH（只用弛豫段）/2=LM（脉冲+弛豫段）、Include Capacity Fade Effect（yes 还需另给不同放电倍率的放电曲线文件组）。多温度→逐温度拟合、Table 自动。完整会话示例照录（soc??-???k.dat 30 条曲线、默认 [2]/[2]）。
- **热滥用 TUI（32.2.4.2.3）**：动力学参数电池专属，用烤箱/ARC 温度-时间数据拟合；热平衡方程 **Eq 32.1**（变量 V 体积、A 外表面积、ρ、cp、h、Stefan-Boltzmann 常数、ε、反应热、A 指前因子、E 活化能、α 反应进度、T、T_amb、T_rad 辐射环境温度、m/n 反应级数）会打印到控制台；输入两列时间-温度纯文本；**建议用不同加热条件（不同烤箱温度或不同初始温度）的多组数据**。拟合输出 **A、E、HW、m、n** 传入 Battery Model 对话框（Advanced Options）并打印。

### 32.2.5 初始化（p. 3530）

两法：①Solution Initialization 初始化流场（电池模型一并初始化）；②Battery Model 对话框 **Init** 按钮**只初始化电池模型**、其他流场变量不动。冻结流场换电池模型时用后者；**切换电池子模型必须重新初始化**。

### 32.2.6 材料属性修改（p. 3530）

MSMD 电池模型必须定义 cell、tab、busbar 材料的电导率。活跃区材料通常用 **defined-per-uds** 法（正/负极分别给不同电导率 σ+ 与 σ−）；被动区材料通常用 constant 法。

### 32.2.7 求解控制（p. 3530)

两个电位方程 **Potential Phi+ 与 Potential Phi-** 出现在 Equations 对话框（Solution → Controls → Equations...），求解过程中可开/关；必要时在 Advanced Solution Controls（Setup → Controls → Advanced...）设高级参数。

### 32.2.8 预定义报告定义（pp. 3530–3531）

自动创建三个：**battery-max-temperature**；**battery-terminal-voltage**（仅 Circuit Network 与 MSMD）；**battery-terminal-current**（同前）。可用于报告文件与报告图；**不可导出或复制**。

### 32.2.9 后处理（pp. 3531–3535）

Battery Variables... 类别。**注意**：电位场由 UDS 解出——要在 CFD-Post 中查看，先在 Fluent 把解导出为 CFD-Post 兼容的 .cdat 文件再载入（保证变量全集可用）。

- **CHT/FMU-CHT 解法**：Potential Field、Current Magnitude、Electrical Conductivity、Total Heat Source、X/Y/Z Current Density in Battery。Total Heat Source 恒可用；其余需勾 Enable Joule Heat in Passive Zones。
- **Circuit Network 解法**：上述 + **Network Current / Network Voltage / Network State of Charge**，另有三个连接整型变量——**Active Zone Connection**（末两位=级内并联序号、高位=串联级号；16S26P 例：第一级第一并 = 101，最后级最后并 = 1626）、**Passive Zone Connection**（1–N 标识被动区位置）、**Battery Connection Index**（9 位数存控制体积连接信息；数位含义图为图形元素未摄取）。Network Current/Voltage/SoC 与 Total Heat Source 恒可用，其余需 Joule 热选项。
- **MSMD 解法**：Cathode Potential、Cell Cluster ID、Cell Voltage、Current Magnitude、Cathode/Anode Electrical Conductivity、Passive Zone Electrical Conductivity、Passive Zone Potential、State of Charge、Joule/Echem/Entropic/Short-Circuit Heat Source、Total Heat Source、Short/Echem/Total Current Source、Short-Circuit Resistance、phi+/phi- 各 X/Y/Z Current Density、X/Y/Z Current Density in Battery、Newman P2D 专属平均量（ce in Cathode/Separator/Anode、cs in Cathode/Anode、phis in Cathode/Anode/Electrolyte、phi_s−phi_e at anode-separator interface）、Li-Insertion-Induced Electrode Layer Thickness Change Ratio（Eq 19.82）、X/Y/Z Component of Battery Layer Normal Vector、Total Electrode Layer Thickness Change Ratio（Eq 19.84/19.85 左端）、Projected Stress in Electrode Layer Normal Direction、Active/Passive Zone Connection 与 Battery Connection Index（定义同 Circuit Network）。
- **热滥用模型**（任何解法）：一方程——Thermal-Abuse Heat Source、Abuse: alpha；四方程——再加 Abuse: Csei/Cpe/Cne/Ce 与分反应热源（SEI Decomposition / Negative-Solvent / Positive-Solvent / Electrolyte Decomposition、Internal Short 仅勾 Enable Internal Short 时）；N 方程——Thermal-Abuse Heat Source、Reaction i 热源、Progress Variable i。
- **矢量图**：MSMD——`current-density-jp`（正极电位场电流矢量）与 `current-density-jn`（负极）；解至少一个电位方程的工况——`current-density-j`（电池导电区电流矢量）；肿胀或正交各向异性导热工况——`layer-nornal-direction`（原文拼写如此，电池层法向矢量）。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3427–3536（批次 93–95，2026-10-20，pypdf layout 模式提取；p. 3536 为仅含页脚的空页）。
- Theory Guide Eq 19.x（19.3–19.85 引用到的各式）与 Eq 32.1 公式体未提取，按引用记录变量与语义；部分符号占位（如 NTGK U/Y 记号、Time-Scheduled 例子中的公式位）在文本层缺失。
- Figures 32.1–32.44（对话框截图）为图形元素未摄取（含 Battery Connection Index 数位含义图）；文中示例表/文件格式（2D/3D 表、time/event-scheduled profile、.ttab、NTGK 放电文件、HPPC 文件、HPPC 库目录约定）已照录。
- 版本敏感默认值：Current URF 0.8、Voltage Correction URF 1.0、ROM 前 3 步、DOD 拟合 10–20 层默认 20/0.01/0.95、老化表各 20 层、NTGK 表 50 DOD×20 温度、HPPC 库仅 Generic-Cell——以 2026 R1 为准。
- 相关页面：[[Fluent 电势场与电化学]]（Ch.31 精细电极尺度 P2D 与肿胀 FSI）。
