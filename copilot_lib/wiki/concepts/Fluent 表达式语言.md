---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - expressions
  - automation
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 表达式语言

## 摘要

User's Guide 2026 R1 Part III / Chapter 5（PDF pp. 1059–1154）定义 Fluent Expression Language——基于 Python 的解释性声明式语言，用于按时间/迭代/位置/解变量定义复杂边界条件、源项和模型/求解器设置，也可用于后处理与报告。对 Copilot 自动化最关键的事实：**表达式值按 Run Calculation 中 Profile Update Interval 的频率更新**、命名规则与维度一致性校验、归约函数与权重语义、自引用归约的会话重启陷阱。

## 5.1 语法与函数（PDF pp. 1059–1067）

- **数据类型**：实数、布尔、实场（如 `2*StaticPressure` 在 zone 上求值为场）、布尔场；**cell register 求值为布尔**。
- **值**：实数（1.0e-3）、整数、布尔（true/false）、**带单位的量** `<number> [<unit>]`（如 `2324.0 [Pa kg^-3 s]`；单位语法基于 CFX-Pre 的 Units Syntax）。
- **Important：表达式值按 Profile Update Interval 频率更新**（Run Calculation 任务页设置）。

### 函数与操作（Table 5.1）

- **运算符**：`+ - * / ** ^`（幂）、`> >= < <= == !=`。
- **条件**：`AND(...)`、`OR(...)`、`NOT(...)`、`XOR(...)`、`IF(cond, true_value, false_value)`——true/false 的**类型与量纲必须一致**；参数可以是场。
- **通量**（可带 `phase=<phase>`，单相不需）：`FilmHeatTransferRate`、`FilmMassFlowRate`、`HeatTransferRate`、`MassFlow`、`RadiationHeatTransferRate`、`SensibleHeatTransferRate`——**只在边界与 face zone 上求值，不在用户自定义后处理表面（平面、iso-surface 等）上**（与 flux report 同要求）。
- **数学**：abs、besselJ/besselY（第一/第二类 Bessel；**n 须为 double 常数**）、ceil、exp、floor、**gradient**（用当前梯度设置求空间梯度——**可能与求解器同变量的梯度不一致**，因求解器使用了稳健性专用技术）、log、log10、max、min、mod、**normalize**（按指定位置最大值归一化，等价 `(expr-Minimum)/(Maximum-Minimum)`）、round、sqrt、**step**（x<0→0、x=0→0.5、x>0→1）、trunc。
- **归约**（`['location',...]` 位置列表）：Area、AreaAve、AreaInt、**Average(Field, [loc], Weight=None|'Area'|'Volume'|'Mass'|'MassFlowRate'|'AbsMassFlowRate')**、Centroid、Count（=Sum(1,loc)）、CountIf（=Sum(IF(...))）、Force（wall，含多孔壁，返回矢量）、MassAve、MassFlowAve、MassFlowAveAbs、MassFlowInt、MassInt、Maximum、Minimum、Moment（对指定点的矩矢量）、PressureForce、Sum（同 Weight）、SumIf、ViscousForce、Volume、VolumeAve、VolumeInt。
  - Weight 语义：MassFlowRate = 质量加权面积分/面平均；AbsMassFlowRate = 绝对值质量加权；Mass = 质量加权体积分；Volume = 体积加权。**report definitions 的 "Mass Weighted Average" 等价于 Average Weight=AbsMassFlowRate；MassFlowAve 类型在 report definitions 中不可用**。
- **矢量**：cross、dot、`<v>.dir`（= v/v.mag）、`vector(x,y,z[,unit])`（分量须同单位；可混合场与单值表达式）、unitVector；分量访问 `.x/.y/.z`、模 `.mag`。
- **Important：单个表达式内不要用多重比较**（`300[K]<StaticTemperature<400[K]` 不成立）——用 `AND(StaticTemperature>300[K], StaticTemperature<400[K])`。
- **Important：自引用归约陷阱**——表达式引用它所应用的同一边界（如 `AreaAve(TotalPressure,'inlet1')+delta` 直接赋给 inlet1）时，**在新 Fluent 会话重启后归约值按 0 解释**。变通：①建 named expression 存初始值；②单独定义循环表达式含实际逻辑；③设 Execute Commands（勾 Execute Repeatedly）反复执行 `(set-cyclic-expr-value-to-expr "cyclic-expr-name" "expr_name")`。

### 5.1.2 单位验证（PDF p. 1067）

- 表达式做单位一致性校验（`1[cm]+TotalPressure` 被拒；不同单位制可混用，如 `1[atm]+200[Pa]`）。
- **弧度虽无量纲仍参与验证**（角度类相加须补 `1[rad]` 因子保持一致；式为图形未摄取）。
- **gallon 按英制帝国定义（4.54609 L），不是美制（3.78541 L）**。
- **温度建议用绝对单位（K 或 R）**：表达式含多个 Celsius/Fahrenheit 温度时各自独立转换，可能产生意外结果。

## 5.2 表达式源（PDF pp. 1067–1072）

- **场变量**：后处理场变量的子集；需上下文的变量用 `Variable(<context>="<value>")`（如 `MassFraction(species="co2")`；多相再加 `phase="air"`）；全清单见 5.5。
- **求解变量**：`Time`、`Timestep`、`DeltaTime`（**稳态下均为 0——除非算例先瞬态运行后切稳态，此时取瞬态运行的最新值**）、`Iteration`（全局迭代计数）。
- **科学常数**：PI、e、R=8314.4626 [kg m² s⁻² K⁻¹ kmol⁻¹]、avogadro、boltzmann、clight、echarge、g、planck、stephan、mupermo、epspermo（=1/(clight²·mupermo)）。
- **别名**：x/y/z（Position）、u/v/w（Velocity 分量）、t（Time）、dt（DeltaTime）、iter、T（StaticTemperature）、P（StaticPressure）、mf（MassFraction）、Amag（FaceAreaMagnitude）、vol（CellVolume）、mass（CellVolume*Density）。
- **Profiles**：`profile('<profile-name>','<field-name>',frame='<ref-frame>')`（frame 仅空间 profile；指定时 profile 坐标按该系变换到全局坐标再插值；`frame='global'` 不变换）；**Important：profile 读入 solver 时值已转为 SI、原单位不保留——表达式中须乘以期望单位**。

## 5.3 创建与使用（PDF pp. 1073–1089）

- **直接应用**：边界/cell zone 条件字段下拉选 expression（可打开大编辑器）；**允许隐式位置**（如质量入口流量 `1 [kg/s]/Area()`；显式给出位置则用显式值）。材料属性可用表达式的有：Density、Viscosity、Thermal conductivity、Absorption coefficient、Scattering coefficient、Lithium diffusivity、Partition coefficient、UDS diffusivities、Mixture mass diffusivity；**多相中编辑某相材料时自动使用该相的变量（无需也不能指定 phase）**；**Density 可为静温或绝对压力的函数，但不能两者兼有——绝对压力版用于轻度可压缩（可压缩液体），此时 Fluent 自动计算声速**。Console 中可用字符串代替实数为设置赋表达式。
- **Named Expressions**（Setup → Named Expressions → New... 或树右键）：
  - 命名规则：唯一（不得与其他表达式、report definitions、表达式常数/变量重名，如 PI、avogadro、T、vol、mass）；**不能含连字符 "-"**（语言自动把连字符转下划线，会与同名 report definition 冲突）；避免与函数名（exp、abs）混淆；**重命名被阻止 = 表达式正在使用中**（如网格自适应）。
  - 定义可用下拉插入函数/变量/cell registers/常数/已有表达式/report definitions/位置/profiles；**用花括号 {} 指定对象名时自动建议禁用、须输显示名；表达式中引用的 report definition 始终取瞬时值**。
  - Use as Input Parameter（**仅常量值表达式可作输入参数**）、Use as Output Parameter；Current Value 刷新仅对单值表达式可用；Used In 列出使用位置。
  - 视觉行为：选表达式赋给字段后，**保存并关闭对话框再重开才显示表达式名**——只是显示方式变化，字段实际已用该表达式。
  - **使用中的表达式不能删除**；可用 `define/named-expressions/` 文本命令创建/修改；**维度必须一致**；含 Per Surface/Per Zone 选项的 report definition 须 Average Over=1；支持 Export To File.../Import From File...。
- **表达式绘图**：Plot 页签——主自变量、Count 点数、Min/Max；**Min/Max 差大而 Count 低时曲线失真，应增大 Count**；可加第二自变量（Curves 数与范围）；复制图像、缩放。
- **表达式后处理**：contours/vectors/pathlines/particle tracks/XY plots 的 Expressions... 字段；可对表达式求导数并可视化；可建表达式体积（Expression Volumes，印刷页码 p. 4053）。**可用于后处理的表达式须：Double 或 Double Vector 类型；求值为场（非单值）；完全指定（species/phase）**；多相中 Phase 下拉不适用（表达式已完全指定；mixture-only 变量如静压不需 phase）；**表达式不能可靠导出到其他后处理器——不导出到 CFD-Post**；colormap 显示单位而对话框 Min/Max 字段不显示。
- **表达式统计**：Zone-Specific Sampling Options 可选场型表达式；**表达式的 RMSE 与等效 custom field functions 的 RMSE 可能不同（表达式计算用 9 位有效数字）**。**后处理求值顺序：表达式先单元值、再由单元值插值节点；custom field functions 先插值节点再计算——陡梯度处两者有可见差异**。
- **Expression Manager**（Setup → Named Expressions → Manage...）：单对话框集中复制/删除/编辑等；多选时部分按钮禁用。

## 5.4 官方示例（PDF pp. 1089–1102）

手册四个逐步示例（定义文本完整可用）：

1. **抛物线入口**（层流管流，管轴沿 Y）：`umax=0.2 [m/s]`；`Radius=sqrt(Area(["in"])/PI)`；`radius=sqrt(x**2+z**2)`；`uprofile=umax*(1-(radius/Radius)**2)`——赋给 velocity inlet 的 Velocity Magnitude（树中右键 Boundary Conditions → Group By > Zone Type 可分组）。
2. **时变抛物线入口**：`omega=2*PI/(10[s])`；`uprofile_transient=uprofile*(sin(omega*Time)*0.1+1)`。
3. **受控出口温度**（稳态、每第 10 次迭代调整入口温度）：`TStart=300[K]`、`TTarget=320[K]`、`TMaxOut=Maximum(StaticTemperature,["out"])`、`TInCurrent=Average(StaticTemperature,["in"],Weight=None)`、`relax=0.9`、`TAdjust=TInCurrent+(TTarget-TMaxOut)*relax`、`TIn=IF(iter<5,TStart,IF(mod(iter+1,10)==0,TAdjust,TInCurrent))`。
4. **参数化攻角算力**：`AOA=5[deg]`（Use as Input Parameter）；`flowDir=vector(cos(AOA),sin(AOA),0.0)`；`totalForce=Force(['wall-top','wall-bottom'])`；`moment=Moment(Centroid(['fluid-16']),['wall-top','wall-bottom']).mag`（输出参数；原文此处括号在提取中错位，语义为对翼型质心的矩的模）；`liftForce=dot(totalForce,vector(-flowDir.y,flowDir.x,0))`（输出参数）；`dragForce=dot(totalForce,flowDir)`（输出参数）——可入表达式 report definitions 监控收敛。

## 5.5 支持的场变量附录（PDF pp. 1103–1153）

以 Type/Section/Variable/Description 四列列出表达式可用的全部场变量，共 40+ 类别：Pressure、Density、Velocity、Perforated、Temperature、EM Losses、Radiation、Solidification/Melting、Icing、Unsteady Statistics、Granular Pressure/Temperature、Turbulence、Acoustics、Species、Reactions、Reactor Network、PDF、PDF Transport、Potential、Lithium、Battery Variables、Structure、NOx、Soot、Phases、Wall Film、Ignition、Properties、Wet Steam、Inert、Sensitivities、Spark、Lump Detection、Wall Fluxes、Cell Info、Mesh、Residuals、Derivatives、Reconstruction、Runtime DFT、Aeromechanics、SystemCoupling、Cell Registers（cell register 以 `<cell_register_name>` 直接按名引用，求值为布尔）。**Note：结构与 Structural Model 相关的变量只在固体 cell zone 上可用——含 Structure... 变量的计算只应包含固体区。**变量条目共数百条，本页不逐条转录，用时回查 pp. 1103–1153。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part III / Chapter 5，PDF pp. 1059–1154；目录范围至此完成（p. 1154 仅版权页脚，Ch.6 自 p. 1155 起）。
- 两处公式为图形未摄取、仅保留正文文字语义：5.1.2 的弧度因子示例式、Ch.4 式 (4.1)（见 [[Fluent 单位制]]）；示例 5.4.3 的式 (5.2)/(5.3) 同为图形，但其步骤文本中的表达式完整转录。Figure 5.1–5.13 为图形元素。
- 函数清单、Weight 语义、科学常数数值、命名规则、RMSE 9 位有效数字等均对应 2026 R1；表达式能力随版本演进，用于脚本前建议在目标版本验证。
- 印刷页码引用（p. 3713 梯度格式、p. 4053 表达式体积、p. 1358/4361 参数、p. 5694/5695 Expression Manager/报告定义）指向未摄取章节，仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 单位制]]（表达式单位验证的背景）
- [[Fluent 求解模式文件读写]]（named expressions 的 TSV 导出/导入；FMU 参数钩连）
- [[Fluent 引导式网格工作流]]（工作流 journal 的 Python 接口，另一条自动化路线）
- [[index]]
