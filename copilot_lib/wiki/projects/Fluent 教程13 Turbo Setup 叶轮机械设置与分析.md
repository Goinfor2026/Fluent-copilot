---
type: project
created: 2026-10-27
updated: 2026-10-27
tags:
  - Ansys Fluent
  - CFD
  - tutorial
  - turbo-setup-workflow
  - 压气机
  - 叶轮机械
sources:
  - "[[Ansys Fluent Tutorial Guide 2026 R1]]"
---

# Fluent 教程13 Turbo Setup 叶轮机械设置与分析

## 摘要

Tutorial Guide 2026 R1 第 13 章（PDF pp. 535–572）：用 **Turbo Setup Workflow** 对 1.5 级轴流压气机（入口导叶 IGV + 转子 + 静子，TFD Hannover 压气机前三排）完成从几何描述、网格导入、区域映射到求解与后处理的端到端设置。该工作流自动生成湍流模型、边界条件、**mixing-plane 网格界面**、`twf_` 前缀命名表达式、报告定义与监视器。同一几何的叶排交互（frozen rotor / 瞬态）分析在第 14 章。教程注明此流程在**所有许可级别**均完整支持。

## 问题描述（13.3，p. 536）

- 1.5 级轴流压气机前三排：IGV **26** 叶、转子 **23** 叶（**17100 RPM**）、静子 **30** 通道。
- 入口总压 **60000 Pa**；出口静压沿**径向平衡分布**（radial equilibrium），轮毂处 **60500 Pa**。

## Turbo Setup Workflow 十三步（13.4.2，pp. 537–553）

1. **启用**：Domain → Turbomachinery → Turbo Setup → Enable Workflow；任务带完成状态图标，可随时用 Edit / Revert and Edit 回退修改。
2. **Turbo Preferences**（File → Preferences → Turbo Setup，影响 zone 名自动映射的搜索规则）：
   - Face Zone Mapping：Inlet Region = `*inflow*, *in`；Outlet Region = `*outflow*, *out`；Periodic 1 Region = `*per*1*, *per`——保证带后缀 inflow/outflow/per1 的名字先于泛化通配被匹配。
   - Search Order 全序列：`*int*, *def*, *bld*, *blade*, *tip*2*, *tip*b*, *tip*out*, *tip*, *sym*, *per*1*, *per*2*, *per*b*, *high*per*, *per*, *hub*, *shr*, *cas*, *inflow*, *outflow*, *in*, *out*`；要点：叶片名（bld/blade）先于 tip 组件、per1 与 per2 都要搜、inflow/outflow 先于 in/out。粘贴时必须保持单行。设置持久生效。
3. **Describe Component**：Type = Axial Compressor；Name = hannover；3 排；表定义 igv/stationary/26/无端壁间隙，r1/rotating/23/**有叶尖间隙（End Wall Gap = yes）**，s1/stationary/30/no；可 Ctrl 多行右键在图形窗口高亮验证。
4. **Define Blade Row Scope**：可整机描述但只正式纳入部分排；**纳入的排必须连续**（不能单排除中间排）。
5. **Import Mesh**：三个 TurboGrid GTM 文件（IGV/R1/S1.gtm），也支持全组件单文件；**工作流仅支持 `*.msh*`、`.def`、`.cgns`、`*.gtm`** 四种格式；Mesh Display 支持通配符（`*bld*`、`*hub*`）选面。
6. **Associate Mesh**：cell zone ↔ 排关联——igv 排选 igv-inlet + igv-passage-main（Ctrl 多选），r1/s1 排各选对应 passage-main；建议勾 Use Wireframe for Highlighting。
7. **Map Regions**：逐 cell zone 审查 face zone → hub/shroud/blade 等区域映射；第 2 步的 Preferences 规则在此生效。
8. **Create CFD Model**：可复制通道（自动复制、旋转、合并 region）；本例每排单通道（# Blades Per Sector = # Sectors to Model = 1）。
9. **Define Turbo Physics**：Rotation Speed = **1790.708 rad/s**（即 17100 RPM）；Operating Pressure = 0；工质 **air (ideal gas)**。
10. **Define Turbo Regions and Zones**：Pressure Inlet / Pressure Outlet；入口总压 60000 Pa、总温 288.15 K、方向 Normal to Boundary；出口静压 60500 Pa 并启用 **Radial Equilibrium Pressure Distribution**；另有可选 Merge Zones（每通道多叶片合并），本例不用。
11. **Define Turbo Topology**：审查 hub/shroud/casing 区域定义并创建 topology 对象。
12. **Define Turbo Surfaces**：默认沿 3 个等 span 位置创建 iso-surface，重命名为 twf_span_25 / twf_span_50 / twf_span_75。
13. **Create Report Definitions & Monitors**：批量创建 span 云图对象与 turbo 专用报告定义/监视器；**此步结束时自动完成初始化**。

## 工作流自动生成物与求解（13.4.3–13.4.4，pp. 553–567）

- 模型/材料：自动设 **SST k-omega** 与基本材料属性；cell zone、边界条件、Outline View 全部就位。
- **网格界面默认全部为 mixing planes**（混合面）——改用 frozen rotor 需手动改（见第 14 章）。
- Named Expressions（`twf_` 前缀）：如 `twf_p_ratio` 定义为出口/入口压力比；可在 Expression Manager 查看/修改。
- 自动创建 8 个报告定义：isentropic-eff-compressor、p-ratio、tot-mflow-outlet、To-inlet、To-outlet、Po-inlet、Po-outlet、mflow-outlet，并配套 report files/plots。
- 求解控制：动量方程欠松弛因子改 **0.1**，以便采用更大时间步长；残差监视器已针对叶轮机械优化（非默认值，无需再改）。
- 初始化：Hybrid + Reference Frame **Absolute** + Use Specified Initial Pressure on Inlets（Initialize 已由工作流自动执行）。
- 运算：Time Scale Factor = 10、200 迭代；同时监控残差、等熵效率、压比、出口总质量流量。

## 结果（13.5，pp. 567–572）

- 后处理直接使用工作流生成的 span 云图（速度幅值/总压/Mach，twf_velmag / twf_totpress / twf_macnum × span 25/50/75）。
- Named Expressions 批量 Compute 结果：`twf_isentropic_eff_compressor` = 0.86127817；`twf_p_ratio` = 1.2339942；`twf_tot_mflow_outlet` = -8.0308548 kg/s；`twf_omega` = 1790.708 rad/s；`twf_vol_avg_gamma` = 1.3990095；其余边界值与设置一致（Pt 60000、Ps 60500、Tt 288.15 K）。
- Report Definitions 批量 Compute 结果：p-ratio = 1.2379454；isentropic-eff-compressor = 0.85721193；tot-mflow-outlet = -7.9825762 kg/s；Po-outlet = 74276.727 Pa；To-outlet = 309.24999 K。
- 注意：表达式表与报告定义表的效率/压比数值略有差异（0.8613 vs 0.8572；1.2340 vs 1.2379），教程未解释，照录两组——推断与求值时刻/口径有关，未经原文证实。

## 证据与适用条件

- 依据：[[Ansys Fluent Tutorial Guide 2026 R1]] Ch.13 全章（PDF pp. 535–572，2026 R1 Downloads 副本，SHA-256 `8347db…`）。
- 版本敏感：工作流任务名、Preferences 键名与默认搜索序均按 2026 R1；数值结果仅代表该教程算例。
- 教程正文大量使用截图；云图/收敛曲线内未读取数值，结论只取文字与控制台表格。
- 提取文本两处可疑拼写：`equalibrium`（应为 equilibrium）、`Preferences Dialog Dox`（应为 Box）——照录，未能核对原印刷是否如此。
- 工作流机理与界面理论见 [[Fluent 叶轮机械流动]]（User's Guide Ch.15）；模型拓扑映射另见 [[Fluent 模型拓扑（Model Topology）]]；表达式语法见 [[Fluent 表达式语言]]。

## 关联页面

- [[Ansys Fluent Tutorial Guide 2026 R1]]（来源记录）
- [[Fluent 教程12 Frozen Rotor 方法]]（前置教程）、[[Fluent 教程14 叶排交互稳态与瞬态仿真]]（同一几何的后续分析）、[[Fluent 教程15 滑移网格]]
- [[Fluent 叶轮机械流动]]、[[Fluent 表达式语言]]、[[Fluent 数据报告]]
