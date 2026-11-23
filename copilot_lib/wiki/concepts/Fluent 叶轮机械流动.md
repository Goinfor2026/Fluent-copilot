---
type: concept
created: 2026-10-18
updated: 2026-10-18
tags:
  - Ansys Fluent
  - turbomachinery
  - blade-row
  - mixing-plane
  - GTI
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 叶轮机械流动

## 摘要

User's Guide 2026 R1 Part III / Chapter 15 "Modeling Turbomachinery Flows"（PDF pp. 1993–2124，共 10 节）讲叶轮机械仿真能力。**本页全章完成（批次 57–59，pp. 1993–2124，覆盖 15.1–15.10）**：Turbo Setup 引导工作流全 11 个任务、Frozen Gust/入口扰动建模、叶排干涉建模（GTI 三类 pitch-change 界面与 Legacy Mixing Plane）、气动阻尼（叶片颤振 TWM/ICM 两法）、相位滞后法、湿蒸汽模型、叶片气膜冷却（Boundary Interface 虚拟孔）、叶轮机械描述、叶轮专属数值（TSN）与叶轮后处理（拓扑/变量/Fourier 系数/Turbo Report/Turbo Performance）。

## 15.1 Turbo Setup 引导工作流（pp. 1993–2018）

- **入口**：Domain → Turbomachinery → **Turbo Setup → Enable Workflow**（另有 Hide/Show/Disable Workflow；Disable 移除工作流页但保留已做设置、有确认提示）。工作流页与 Outline View 并列；任务机制与网格引导工作流相同（任务状态/分组/编辑见 pp. 293–294）。**Note：完整跑完并存 case/data 后须连 `_workflow_files` 文件夹一起保存——只分享 case 文件时工作流面板初始隐藏（仍可用 Show Workflow 显示）**。
- **任务清单**：Describe Component → Define Blade Row Scope → Import Mesh → Associate Mesh → Map Regions → Create CFD Model → Define Turbo Physics → Define Turbo Regions and Zones → Define Turbo Topology → Define Turbo Surfaces → Create Report Definitions and Monitors（15.1.1–15.1.11）。
- **Describe Component**（15.1.1）：部件类型四选——**Axial Compressor / Axial Turbine / Radial Compressor / Radial Turbine**；行数 1–99、旋转轴 X/Y/Z；每行 stationary（IGV/NGV/stator）或 rotating（rotor）；每行给名称、**# Sectors（叶片数）**、**End Wall Gap?**——Yes 则叶片与 hub/shroud 间留间隙并**自动生成非一致界面**（**默认 rotor 行 Yes、stator 行 No**；stator 行设 Yes 时该间隙按 tip gap 处理）。表格支持多选编辑、上下插行（插行复制当前行属性）。提交后图形窗口出 2D 示意图（图 15.1）。
- **Define Blade Row Scope**（15.1.2）：选择纳入分析的行——**必须是单一连续行集**；逐行 include/exclude；示意图中排除行灰显。
- **Import Mesh**（15.1.3）：可导单个含全部行/通道/叶片的网格文件，或每通道/叶片一个文件；支持 `.msh/.msh.h5/.def/.cgns/.gtm`；**支持同一 cell zone 内多叶片/分流叶片**；每个文件生成子任务（树视图显示 cell zone 与关联 face zone）；Edit 换文件时旧文件卸载、新文件导入显示。
- **Associate Mesh**（15.1.4）：把导入的 cell zone 关联映射到对应行（后续任务据此复制/拼接生成完整 CFD 模型）。默认线框高亮 + 流向箭头。**Modify Zone Names?**：Yes using row names——cell zone 整名改为行名（多区加 `.1` 后缀）、face zone 加行名前缀（`stator_1:s1-inflow-passage`）；Yes using row numbers——加 `row03:` 前缀；No 保留原名。**每行至少指定一个 cell zone**；下拉列表为候选子集，[popup panel] 打开 Select Cell Zones 对话框（可过滤/排序；已关联区可指定为上游或下游）。
- **Map Regions**（15.1.5）：对每个原始 cell zone，把 face zone 映射到正确的叶栅通道区域（供后续边界条件与拓扑定义用）。选 Cell Zone → 表中逐 Region 确认关联 face zone；悬停高亮；**任务更新后周期区不再高亮**（已合并；需高亮须先撤销本任务）。face zone 映射关联默认取自 **Preferences → Turbo Setup** 类别。**Note：完成 Define Turbo Regions and Zones 任务后如需改 Map Regions，须先 Revert and Edit Create CFD Model**。
- **Create CFD Model**（15.1.6）：按前序输入正式生成 3D 模型。给旋转轴；**Apply Sector Number Restriction**（限制建模扇区数为实际叶片数的因子）；**Estimate Number of Sectors** 按钮（按旋转轴与两周期面夹角估算；与 Describe Component 值不一致时应以估算为准并在 Describe Component 中改正——导入网格后才有此估计）；Number Sectors in 360；# Blades Per Sector；**# Sectors to Model + 每行 Angle Offset**（可建小部分、大部分或整机；改值即实时预览）。更新后**区名自动追加扇区号**（passage → passage_01、passage_02…，单扇区也加）。编辑用 Revert and Edit。
- **Define Turbo Physics**（15.1.7）：转速、操作压力、是否解能量方程、工作流体三选——**Air (ideal gas) / Air (incompressible)（可给密度）/ Existing Material**（下拉选现有流体材料或 Create/Edit 新建编辑）。
- **Define Turbo Regions and Zones**（15.1.8）：**Inlet/Outlet Type 三组合**：①Pressure Inlet + Pressure Outlet（进口静压 + 总温 + 流向 Normal to Boundary / 笛卡尔 XYZ / 圆柱径向-切向-轴向；出口表压 + 可选**径向平衡压力分布** Radial Equilibrium Pressure Distribution）；②Pressure Inlet + Mass Flow Outlet（质量流量，按 **Machine/Sector/Passage** 三种口径给）；③Mass Flow Inlet + Pressure Outlet。**Merge Zones**：默认同行的所有单元及进口/出口/hub/shroud 合并成单一区（简化边界条件输入；可取消部分或全不合并）。**Note：本任务只用基本默认值——高级设置（如 profile 支持）直接到 Outline View 改**。
- **Define Turbo Topology**（15.1.9）：把拓扑区（主机通道进出口、hub、shroud、侧边界）关联到区域，供 Fluent 计算叶轮拓扑坐标。**Skip Define Turbo Topology** 可跳过本任务与 Define Turbo Surfaces（不生成叶轮截面/云图，但基于进出口区的面与性能监视器保留）。给拓扑名；**Start Row / End Row**（拓扑定义与 iso 面生成范围）；表中逐区指认；每个拓扑生成子任务、可建多拓扑。
- **Define Turbo Surfaces**（15.1.10）：在展向位置建叶轮 iso 面供后处理——默认 **3 个，Iso-Value 0.25/0.5/0.75**，数量可增减。
- **Create Report Definitions and Monitors**（15.1.11）：自动创建叶轮性能参数报告定义与监视器（流量、压比、效率等）；可选为 iso 面自动建云图。完成后在 Outline View 查看，即可开始计算；还可结合 Simulation Reports（p. 4589）。
- **文本命令**（15.1.12）：`turbo-setup/` 菜单。
- **任务编辑规则**（15.1.13）：完成态任务控件禁用；普通任务 **Edit → 改 → Update**（后续已更新任务全部转为过期，需手动逐个更新；Cancel 丢弃改动、保持完成态）；含区/标签选择列表的任务用 **Revert and Edit**（回退任务先前状态，后续转过期；**Cancel 丢弃且状态不恢复**）。带单位字段的任务：回到工作流开头改单位制后逐任务更新，**数值按新单位自动换算**。
- **工作流保存/加载**（15.1.14）：Save Workflow 存为自定义模板（**.wft 文件含版本号**——2026 R1 内部记 `"version": "26.1"`）；Load Workflow 加载；可删单任务或 Reset Workflow 整体重置。**写网格文件时当前工作流随网格一并保存**，并把任务编辑数据从临时文件夹复制到工作流专用文件夹（如 `my_mesh_file_workflow_files`）——由偏好设置控制。**工作流文件/日志中的默认值是模型相关的**（换模型会变）；显式修改过的值作为用户设置跨模型保留。
- **偏好设置**（15.1.15，File → Preferences）：General 类 **Dockable Workflow Editor**（任务属性可拆到可移动/缩放的工作流编辑器——多任务/多属性时有用）；Turbo Setup 类 **Save task editing data with case file**（存 case 时一并存任务编辑数据；启用后 Saving data for editing tasks 自动设为 Write case files）；**Saving data for editing tasks**：**Write case files**（默认；每个完成的 case 相关任务存一份 case 到临时文件夹，编辑时取回该任务的 case 与设置）/** Do not save data**（不存——**编辑已完成任务时自动逐个重算之前所有任务生成所需 case；不需要再编辑任务时建议禁用**）。

## 15.2 Frozen Gust / 入口扰动建模（pp. 2019–2020）

- **思想**：降低叶排仿真成本——上游排尾迹（通常取自定常解）作为**入口 profile 施加到下游排**；下游排位势场同样可反施加到上游排——把叶排干涉问题化为**带指定进出口 profile 的单排问题**。两种构型（图 15.3）：**A = 转子尾迹施加于静子**；**B = 静子尾迹施加于转子**。
- **流程**：①对目标转子/静子构型做定常叶排干涉仿真（混合面或 frozen rotor，MRF p. 1842 / legacy mixing plane p. 2030）；②提取邻排尾迹/位势 profile（profile 文件 p. 984）；③用 **Replicate Profile 对话框把 profile 扩展到整轮**（p. 1634）；④施加到目标边界（通常是进口）；⑤构型 A：**profile 须链接到随转子旋转的参考系**（p. 1622）；构型 B：转子相对静止尾迹的运动用标准 **Mesh Motion**（cell zone 条件给转速与轴，p. 1373）。

## 15.3 叶排干涉建模（pp. 2020–2035）

- **GTI（General Turbo Interface）**：连接转子-静子的统一界面机制——全轮、周期扇区、**任意节距比 pitch-change 扇区**皆可；也可把**二次流路（腔室、注入、引气）连到主流路**；定常与瞬态皆可。Domain → Turbomachinery → Turbo Models → **Turbo Create...**。
- **界面类型隐式判定**（Important Note）：**GTI + 流体区运动方式共同决定界面是 FR/TRS/MP**——跨接 **Mesh Motion** 流体区的 GTI = **Transient Rotor-Stator**（pitch-change 选 PS 或 NPS）；**Frame Motion** 流体区 = **Mixing-Plane 或 Frozen-Rotor**（PS/NPS）。**无须也不存在显式的"FR/TRS"界面类型选项**——由 zone motion 隐式定义。
- **兼容性/限制**（15.3.1）：仅定常与瞬态；**PS/NPS**：压力基耦合、密度基隐式、SIMPLEC（其他压力基分离式与密度基显式不可）；**MP**：仅压力基耦合与密度基隐式；相对速度公式仅限压力基耦合计数的定常；全部 Species 模型与 UDS 可用；适用 **3D 旋转叶轮机械转子-静子构型**（轴流/径流压气机、涡轮、变矩器）；**2D 与 3D 平移问题（直列叶栅）不可用**；**不可与多相（除 Wet Steam）、辐射、DPM、声学同用**；**不支持 GTI 的 repartition 与 migration**。
- **三类 pitch-change 界面**：
  - **Pitch-Scale（PS）**（15.3.1.1）：在界面两侧**拉伸/压缩解的通量 profile** 保持叶排通道连接。**适用节距比 < 2**；≥ 2 或全轮界面改用 NPS（选 PS 时超限会警告并建议 NPS；**界面建成后可编辑切换 PS↔NPS**）。瞬态下允许叶排间瞬态干涉，但**周期近似使精确频率成分不保真**——**可用于改进气动性能，不能用于预测节距比 ≠ 1 时的精确频率内容**。
  - **No Pitch-Scale（NPS）**（15.3.1.2）：**为小节距通道的流动 profile 创建虚拟副本**保持连接；**任意节距比**，包括扇区对 360°、全轮对全轮；大节距差 + Frame Motion/无运动时界面总压可能有损失——专家选项 `define/turbo-model/general-turbo-interface-settings/expert/nps-minimize-po-loss` 减小。瞬态频率成分同样不保真（周期近似）；**可用于非对称流动或进口畸变建模**。扇区对 360° 时**扇区节距应使 360° 内通道数为整数**。
  - **Mixing-Plane（MP）**（15.3.1.3）：FR（MRF）与 TRS（滑移网格）之外的第三选择——非一致界面 + **周向平均**把叶排间流动变化"混出"；隐式实现 → 混合更稳健、收敛更快；是 legacy profile 交换式混合面（15.3.4）的增强替代。原理：每流体区按定常解，相邻区数据在界面处**空间平均**传递——消除周向不均匀（尾迹、激波、分离）引起的非定常 → 得到时间平均流的合理近似。**按机器类型生成径向带（轴流机）或轴向带（径流机）；默认请求最多 40 个等宽带，生存性检查剔除零面/极少面带后可能远少于 40**。设置 TUI：`define/turbo-model/general-turbo-interfaces-settings/mixing-plane-model-settings`。**Note：MP 用于瞬态仅当跨接区为 Frame Motion——Mesh Motion 区禁止建 MP（会警告）**。legacy→新模型迁移：删 legacy 混合面 → 上下游边界改 interface 类型 → 按前述创建。
- **整排多叶片（ensemble）经 GTI**（15.3.2）：ensemble 节距比 = 360°/ensemble 节距。**两侧皆为整数 → PS/NPS 可用 Frame Motion 或 Mesh Motion；任一侧为分数 → 只能 Frame Motion**（即 TRS ensemble 仅限整数节距比）。**MP 整数分数皆可**（MP 只配 Frame Motion）。**Note：Frame Motion 定常/瞬态皆可用；Mesh Motion 仅瞬态**。示例（表 15.1）：IGV 20 叶取 2（节距 36°，比 10）；转子 16 叶取 3（节距 67.5°，比 5.333）→ 只能 PS/NPS + Frame Motion，不能 TRS。
- **GTI 创建/编辑**（15.3.3）：Create/Edit Turbo Interfaces 对话框——命名；Zone-1/Zone-2 选界面区（**Adjacent Cell Zone 过滤**：列表缩至所选 cell zone 邻接且未被其他界面占用的区；已配对区移入 Paired Zones）；Interface Options：**全不选 = 非叶轮非周期界面（如 tip gap 界面）；勾 General Turbo Interface = 叶排界面（再选 PS/NPS/MP）**。创建后可按名称/类型分组显示；**可多选界面批量编辑/删除/显示/检查（多选批量转换只能转成单一 pitch-change 类型）**。**Note：求解中删除重建界面或初次建界面后，须初始化再求解**。Delete 会连带删除建界面时生成的附加区；Display 预检界面位置；**Interface Check** 控制台输出：界面名、pitch-change 类型、叶排构型（sector-to-sector / 360-to-sector / 360-to-360）、两侧节距与节距比（大/小）、区名/面积、**总相交百分比（应接近 100%）**、**周期边界贴合检查**（周期边界与 GTI 侧须有共享边——失败须改几何）、**ghost link 检查**（ghost 单元与其实际单元的链接；失败则求解器可能跑不起来）、**面排序检查**（ghost 面与实际面创建顺序一致）。**ghost 单元 = 实际单元的平移/旋转副本**——GTI 跨区传变量、phase-lag 法周向传变量都用它。
- **Legacy Mixing Plane 模型**（15.3.4）：基于 profile 边界交换的旧实现；TUI `/define/turbo-model/legacy-models/legacy-mixing-plane`；**仅在 Turbo Model 未 Enable 时可用**；建议改用 GTI 混合面。
  - **限制**（15.3.4.1）：**不能用 LES；不能用组分输运与燃烧；不能用 VOF；DPM 不能用于耦合流**（非耦合可算但粒子会穿出混合面域）。理论参考（Theory Guide）：转子/静子域、混合面概念、平均方法选择、算法、质量/旋流/总焓守恒。
  - **设置**（15.3.4.2）：①速度公式 Absolute/Relative（压力基；**密度基只能 Absolute**）；②每 cell zone 给角速度与旋转轴——旋转区或进口要给圆柱速度分量时须定义轴（Reference Frame 页 Rotation-Axis Origin/Direction；Frame Motion + Speed + 平移速度）；**Important：混合面两侧 cell zone（含静止区）都要定义旋转轴**；③墙速度边界条件同 MRF 设置第 3 步；④进口边界：velocity inlet 可给绝对或相对速度；**pressure/mass-flow inlet 的流向与总压恒为绝对**（混合面计算恒用绝对速度公式）；mass-flow inlet 无须给流量——建混合面时自动改用 **Mass Flux with Average Mass Flux** 方法；**Important：混合面处的出口边界区必须是 pressure outlet；进口边界区须为 velocity inlet（仅不可压）、pressure inlet 或 mass-flow inlet；整机进出口组合不限；若需跨混合面严格质量守恒，下游边界须用 mass-flow inlet——velocity/pressure inlet 不保证严格质量守恒**；⑤Mixing Planes 对话框仅 TUI 打开（`...legacy-mixing-plane/mixing-plane-gui`）：选上游/下游区对（显示网格核对）；3D 选 **Mixing Plane Geometry：Radial（周向平均成沿径向变化的 profile——轴流机）或 Axial（沿轴向变化——径流机）**（径向 ⊥ 转轴、轴向 ∥ 转轴）；3D 设 **Interpolation Points**（径/轴向插值点数 ≈ 面网格分辨率；更多点无益——分辨率受面网格限制）；2D 整界面平均成单点 profile（无须设点数与几何）；**Global Parameters：Averaging Method（Area 默认 / Mass / Mixed-Out）**；**Under-Relaxation**（**Eq 15.1**：新边界 profile = 旧值 + α·(新值 − 旧值) 语义；早期迭代边界值变化剧烈易发散，α < 1 欠松弛、流场建立后可增大）；Create 生成（名字 = 两区名组合）、Delete 删除。
  - **建模选项**（15.3.4.2.1）：**定压选项**（fix-pressure-level）：变矩器等构型用混合面后无定压边界、压力无界漂移——开启后每迭代从表压场中减去 **Reference Pressure Location**（Operating Conditions）处压力；**仅压力基不可压流**。**旋流守恒**（conserve-swirl → enable?；verbosity? 每迭代报告区 ID、上下游单位面积旋流积分与校正前后比值；`report-swirl-integration` 报告每个压力进口/出口、velocity/mass-flow inlet 的旋流积分——按 Theory Guide Eq 2.22 推各部件扭矩）。**总焓守恒**（conserve-total-enthalpy）：调整下游总温 profile 使积分总焓匹配上游——效率类全局参数直接取决于叶排/级总焓变化。

  - **求解策略**（15.3.4.3）：混合面只是合理近似——**混合面附近无显著倒流**为前提；数值上早期常出现瞬态倒流 → **先用固定界面条件（如 frozen rotor）求出过渡解，再切混合面收敛**。用 Mass/Mixed-Out 平均且严重倒流致收敛困难 → **先用默认 Area 平均初始化、倒流消失后切换**；边界值欠松弛（α < 1）也有帮助，流场建立后渐增。总焓守恒 verbosity：每迭代报告区 ID、上下游热流及比值。

## 15.4 气动阻尼——叶片颤振分析（pp. 2036–2067）

- **背景**：强迫响应分析预测叶片结构失效；气动阻尼值是关键量。颤振通常发生在**叶盘组件固有频率**——先用 Ansys Mechanical（或第三方 FEM）做**模态分析**得固有频率与振型（mode shapes）；叶盘组件模态很多，**只有少数模态对颤振有贡献、仅这些进入颤振仿真**。Fluent 提供两法：**Traveling Wave Method（TWM）**与 **Influence Coefficient Method（ICM）**。
- **共同设置**（15.4.1）六步：①先跑定常解备初始化；②读振型 profile 文件；③切瞬态；④配 Run Calculation（Time Advancement：**Type=Fixed、Method=Frequency-Based**、Frequency=振型频率、Time Steps per Period 定时间步、Total Periods、Max Iterations/Time Step）；⑤建动网格区（先开 Dynamic Mesh——**须先启用 Turbo Models 才会出现 Periodic Displacement 选项**；Periodic Displacement 页定义；逐边界指定运动）。**Important：建好动网格区后、定义任何 Report Definitions 之前先初始化流场**——报告定义所需数据只在流场初始化时插值到叶片；⑥建气动阻尼监视器（Solution → Reports → Definitions → New → **Aeromechanics Report**；TWM 与 ICM 各有专用报告）。
- **振型文件**（15.4.1.1）：模态分析导出的 .csv profile。Mechanical APDL 命令：**EXPROFILE**（导出振型）与 **EXOPTION**（含面连接信息）。格式：[Name]；[Parameters]（振型频率——叶片位移定义要用；**复振型还含 Harmonic Index——Nodal Diameter 与 IBPA 计算必需**）；[Spatial Fields]（节点坐标）；[Data]（归一化或非归一化位移，实部或实+虚）；[Faces]（面连接——供 Profiles 对话框 Preview 以曲面预览、核对取向）。**Passage number（sector tag）**为 [Data] 附加列——由单通道模态 profile **Replicate 复制时自动生成**；与机器转向无关、原始通道 = 1、按右手定则绕轮盘递增（图 15.9）。**Mesh Motion 下必须定义与该区转速/方向一致的局部参考系并链接 profile**（Fluent 检查不满足会提示创建；Frame Motion 无此要求）。示例 profile 见 p. 2039–2040（Frequency = 1075.796 Hz、norm meshdisptot x/y/z 列）。**FEM 网格常比 CFD 粗且不对齐 → 可用 System Coupling 自动对齐并把振型映射到 CFD 网格**（须先从 Fluent 导出 .csv 表面网格，p. 1354）。读取：File → Read → Profile。
- **Periodic Displacement**（15.4.1.3.2）：启用时**自动开启网格光顺**；**推荐光顺法按序：线弹性（Poisson 比 0.45）→ 扩散（扩散参数 1.5）**。可建多个 **Periodic Displacement Group**（每组激活一个位移——快速切换不同振型）。**Fast Mesh Smoothing**：把边界运动分解为实/虚部分别在仿真开始时解一次并存储，之后每时间步直接用存储结果更新节点坐标、不再跑光顺——**显著省时**。位移定义：含 meshdisp/meshdisptot 变量的 profile 选入后**自动填充对话框**（含频率、幅值参数）；手动给：Real/Complex 振型、Direction X/Y/Z（复振型加 Imaginary Direction）——取 .csv 位移变量、UDF（**DEFINE_PERDISP_MOTION**）或表达式；**归一化振型给 Amplitude（推荐初值 = 弦长 0.05%），非归一化给 Scaling（推荐初值 0.5）**；**建议用推荐参数预览网格运动至少一个振动周期**；Passage Number 取 sector tag 变量（TWM 用于 IBPA、ICM 用于阻尼计算）。
- **动网格区配置**（15.4.1.3.3，Multi Create 批量）：**叶片** = User-Defined + Mesh Motion UDF/Profile 选 Periodic Displacement Group；**shroud（有叶尖间隙时）** = Deforming + 几何 **surface-of-revolution**——间隙网格节点沿回转面滑动防偏斜、间隙厚度不变（**Cylinder Axis 分量须手动核对**）；**Note：带界面的叶尖间隙不被 Periodic Displacement 支持——无界面 tip gap 可通过 shroud 边界条件正确设置实现**；**hub** 通常静止，复振型时可能与叶片同样处理；**旋转周期边界**通常静止，但与位移面相连（复振型）时须随动——**Deforming + faceted**；其余边界 = Stationary。
- **TWM**（15.4.2）：**所有叶片**都按固有频率振动、叶片间相位差 = **IBPA（Inter-Blade Phase Angle）**——**IBPA = 叶片节距角 × Nodal Diameter**（节距角由叶数定，Turbomachinery Description，p. 2091；分流叶片按主叶片到下一主叶片量节距）。ND = 0 全同相；振动图样成**行波：FTW 顺机器转向、BTW 逆转向**。N 叶盘有有限个节径（公式未提取；偶数叶最大 N/2、奇数 (N−1)/2）。**目标 = 单位振动周期做功（能量法）**：**Eq 15.2** W = 周期内 ∮ p·v⃗·n⃗ dA dt（周期 T、角频率 ω、压力 p、叶片振动速度 v、面积 A、单位法向 n）——**W > 0 振动被阻尼、W < 0 未阻尼/被激发**。**每个节径需两个仿真：FTW 与 BTW 各一**。三种建模构型：①**全轮**（单设置覆盖全部节径、网格大成本高）；②**周期扇区**（须满足周期性、经济但覆盖全节径范围需多套设置、奇数叶可能找不到有效扇区）；③**单通道 + 基于 Fourier 的 phase-lag 边界**（单设置覆盖全节径范围、成本最低——见 15.5）。
  - **TWM 专属设置**（15.4.2.1）：组对话框选 Travelling Wave Method + Aerodynamic Damping；**Wave Direction：Forward/Backward**；**Nodal Diameter**：**复振型（循环对称生成）已含相位偏移——ND = profile 的 Harmonic Index、IBPA 由 ND 算出、两字段不可编辑（要别的节径须换振型）**；纯实振型须自给 IBPA（= 节距 × ND，界面显示在 Nodal Diameter 右侧）。
  - **谐波可视化/导出**（15.4.2.2）：前提是 Turbomachine Description 已定义（工作流自动或 `define/turbo-model/create-turbomachine-description`）。可算：①压力/速度分量/温度的 **Fourier 系数**（Turbomachinery 功能区 Spectral Content 页或 define/turbo-model 菜单；详见 p. 2100）；②表面**实/虚一阶谐波压力载荷**——`define/turbo-model/blade-flutter-harmonics/enable-harmonic-exports?`（默认所有边界、可指定）+ 跑完 `write-harmonic-exports?` 按**每面一个 .csv**（根名提示输入、面名追加；参数区含节径与谐波指标；含面连接可回读 Fluent/CFD-Post 预览与显示实/虚一阶压力）；**该 .csv 供 Ansys Mechanical/FEM 做强迫响应分析**。文件格式示例见 p. 2058–2059（含 Rotation Axis、Frequency、Nodal Diameter、Mode Multiplier、Travelling Wave Flag 参数）。
  - **TWM 后处理**（15.4.2.3）：报告定义 **Aerodamping (Travelling Wave Method)**——多主叶片时选 **Per Zone**（每个动网格区 = 一主叶片 + 分流叶片）；**Integrate Over** = 积分时间步数（建议 = 每周期时间步数；改每周期步数须同步改）。云图（Contours of type **Aeromechanics**）：**Wall Work Density**（**Eq 15.3**：流体对壁做功/面积，相对网格位移 × 面单位矢量）与 **Wall Power Density**（**Eq 15.4**：功率/面积，网格速度 × 面单位矢量）。
- **ICM**（15.4.3）：**对给定实振型，一次运行算出几何支持的全部节径的气动阻尼**；还可算/显示广义（模态）力。核心：建模**足够多片连续排列的叶片、只有中间（参考）叶片振动、其余静止**；依据**线性叠加原理**——叶排中所有振动叶片对参考叶的非定常气动影响 = 参考叶自身振动对自身与所有其他静止叶片影响之和 → TWM 下参考叶一阶压力谐波 = 自身 + 各静止邻叶贡献之和。公式：**Eq 15.5**（给定 IBPA 的叶片压力场 = n 邻叶贡献求和）、**Eq 15.6/15.7**（经 Fourier 展开的气动阻尼一般式）、**Eq 15.8/15.9**（广义/模态力）。**符号约定**：压力虚部 = 累积 B Fourier 系数的相反符号；网格运动（振型）的 B 系数不翻号（正弦运动 t=0 时为 0、只记相位）。
  - **ICM 设置**（15.4.3.1）：组对话框选 Influence Coefficient Method + Aerodynamic Damping；其余同共同设置。**限制**：①**仅实振型**；②振型须读入并扩展覆盖全部参与叶片；③**叶排叶片数必须为奇数**（只有中间叶片振动；Fluent 自动处理——所有叶片只需指派到同一位移组）。
  - **ICM 后处理**（15.4.3.2）：两个报告定义——**Aerodamping (Influence Coefficient Method)**（输出每个节径的阻尼值；只需给 Normalization factor；控制台逐节径输出；`define/turbo-model/blade-flutter-harmonics/write-aerodamping-vs-nodal-diameter?` 把导出文件转成"阻尼 vs 节径"可绘 XY 图）与 **Generalized/Modal Force**（叶片力；Force Component Type 选 Real/Imaginary；Per Zone 逐叶输出）。云图 Aeromechanics 组：Real/Imaginary **Wall Generalized/Modal Force per Area**。
- **共同后处理**（15.4.4）：核心判据 = 气动阻尼**正负号**（Eq 15.2）。云图变量（Contours of type Mesh）：振型显示 **X/Y/Z Periodic Displacement 与 X/Y/Z Imaginary Periodic Displacement**（插值后的实/虚振型分量）；网格运动变量 **X/Y/Z Relative Mesh Displacement**（本步 − 上一步节点位置）与 **X/Y/Z Total Mesh Displacement**（本步 − 参考未变形位置）。

## 15.5 相位滞后法（Phase-lag，pp. 2067–2076）

- **用途**：流动周期性与几何周期性不一致时普通周期界面不可靠——Phase-lag 边界在原周期边界上施加**时间相位偏移的周期条件**，把模型缩到**单个叶栅通道**。三类场景：相邻叶排节距不等（**TRS 瞬态转子-静子**）、信号节距与域节距不等（**边界扰动**）、叶间相位角（**叶片颤振 TWM**）。
- **理论**（15.5.1）：直接在 S1/S2 边界间对原始变量施加相位偏移。Erdos 直接法需在全部 S1/S2 边界存储整周期信号；**Phase-lag 对界面两侧信号做时间 Fourier 级数分解（Eq 15.10）避免逐步存储**（L. He 提出）。各通道按其基频分解谐波——TRS/边界扰动的基频 = **叶片通过周期倒数（Eq 15.11）**。**该边界法收敛到准周期态非常快**。入口扰动构型（图 15.13）：S1/S2 间相位偏移（**Eq 15.12**）与等效时间偏移（**Eq 15.13**）（公式体未提取）；S1 信号 = S2 信号移相、反之亦然。
- **能力与限制**（15.5.2）：支持进口/出口扰动（可多扰动同时）与叶片颤振（TWM）。DBNS：施加于原始变量（静压、静温、速度分量、k、ε、ω）及全部导数/重构梯度；PBNS：另加密度、静焓及导数/梯度。**官方支持模型：k-ε、k-ω、SST 湍流模型与非平衡冷凝（Wet Steam）模型**。限制：**叶尖间隙须保形网格——避免建 tip-gap 界面**；单排多通道时**所有 cell zone 须合并为一个、所有 interior 合并为一个**。
- **使用**（15.5.3）：①仅瞬态；②启用 Turbo Models（`/define/turbo-model/enable-turbo-model? y` 或功能区）；③外周期边界上需有**周向 phase-lag 周期界面**；④**确保无任何扰动信号相对其作用部件速度为零**；⑤需要 Turbomachine Description（工作流自动或手动命令）；⑥**推荐 Frequency-Based 或 Period-Based 时间推进、时间步匹配扰动、Time Steps per Period ≥ 40 左右**；⑦额外谱设置 `/define/turbo-mode/phase-lag-extra-settings`（手册原文如此，疑为 turbo-model 之误）：**Fourier 系数欠松弛（默认 0.7，可调低增稳健）**；**初始化周期数（先用"类周期 BC"跑若干周期再启动 phase-lag——改善 Fourier 系数初值）**；每基频默认谐波数（默认 yes；否则逐频列谐波）；默认谐波数 **10**。⑧**强烈建议双精度**。
  - **建界面**（15.5.3.2）：右键周期边界 → Convert to Phase Lag Periodic Interface；或多选两侧边界右键 → Periodic... → 对话框底部选 Phase Lag Periodic。等价命令：`/define/turbo-model/make-phaselag-from-periodic`（由已有周期界面转换）或 `make-phaselag-from-boundaries`（指定两侧）；成功打印 "Successfully created a phase-lag interface"。
  - **谱描述**（15.5.3.3）：信息齐全后自动生成。**进口/出口扰动**：profile .csv 含参数 **NumberSectors360**（扰动在 360° 的等效叶片数；多扰动加序号 NumberSectors360_2 等）即可自动算等效频率与相移角；无该参数或 UDF 扰动 → `/define/turbo-model/create-phaselag-spectral-content` 手动逐行输入（类型 1 = 叶片通过扰动：给参考帧 + 360° 扇区数；类型 2 = 实频率 Hz：给参考帧 + 基频；类型 3 = 叶片颤振扰动）。**TWM**：动网格边界指定后自动从振型取频率填充谱内容与相移角。辅助命令：`list-phaselag-state`（同时列叶轮描述与图形谱内容）、`append-phaselag-spectral-content`、`delete-phaselag-spectral-content`。
  - **初始化与运行**（15.5.3.4）：推荐①**定常解 → 切瞬态 → 加 phase-lag 设置**（通常收敛最好）；②把定常解插值读入已有瞬态 phase-lag case。
  - 手册小节编号瑕疵：p. 2070 目录把后处理小节印作 "15.5.3.5. **21.2.3.6.** Fourier Coefficient Postprocessing..."（跨章编号残留）；其正文在 p. 2077 起，属批次 59 范围。

  - **初始化与运行**（15.5.3.4）：推荐①**定常解 → 切瞬态 → 加 phase-lag 设置**（通常收敛最好）；②把定常解插值读入已有瞬态 phase-lag case；③进口初始化 → 混合初始化 → 瞬态 phase-lag 设置。**Important：先配好 phase-lag 界面再直接打开等效定常解的 .dat 会报错**（phase-lag 的 ghost 单元在定常解中无对应）——须按上述流程之一。
  - **Fourier 系数后处理入口**（15.5.3.5，标题残留"21.2.3.6"）：见 15.10.3。
  - 手册小节编号瑕疵：p. 2070 目录把后处理小节印作 "15.5.3.5. **21.2.3.6.** Fourier Coefficient Postprocessing..."（跨章编号残留）。

## 15.6 湿蒸汽模型（p. 2077–2078）

- 汽轮机出口湿度增大会**侵蚀低压级叶片**并**降低湿蒸汽区级效率**——湿蒸汽建模重要。选择：Multiphase Model 对话框选 **Wet Steam**（Physics → Models → Multiphase；设置见 p. 3288）。**当前支持：压力基与密度基求解器皆可；支持 Phase-lag 法**（图 15.17–15.18）。

## 15.7 叶片气膜冷却（Blade Film Cooling，pp. 2078–2091）

- **思想**：气膜冷却 = 冷气从叶片表面大量小孔注入边界层；CFD 痛点是逐孔建模/划网格费时。Fluent 用 **Boundary Interface** 特性在**现有边界网格上创建虚拟孔**——孔可当进口/出口处理，**移动、改径改形无须重划网格**。
- **虚拟孔几何**（15.7.1）：①启用 Turbo Models（outline 出现 Boundary Interfaces）；②从 **.csv profile 导入孔心坐标**（每行一孔 x,y,z；附加列给流量数据；Interpolation Method 保持默认 constant）。**profile 的 Reference Frame 控制孔的行为**：定常 → global；瞬态且 cell zone 静止（静子）→ global；瞬态且区在动（转子）：global = 孔在空间不动、转子扫过（适合 **shroud 冷却**）；孔要**冷却运动转子** → Reference Frame 选**跟随转子 cell zone 的局部参考系**（p. 1202）——孔在旋转系中不动、随转子移动。**Note：孔坐标不必精确落在网格面上（有容差）；离面太远的孔不被定位、被忽略**。示例 profile 含参数（InjectionTemperature、Diameter 等）与逐孔数据列（静止系速度分量、质量流量、Sector Tag）；一个 .csv 可含多个 profile。③Create/Edit Boundary Geometry 对话框建虚拟几何：命名；Coordinate Profile 选 .csv；**Geometry BC-type：mass-flow-inlet / mass-flow-outlet / pressure-inlet / wall**（气膜冷却通常 mass-flow inlet；引气 bleed 用 outlet）；**Hole Direction**：normal-to-boundary / cartesian（XYZ）/ cylindrical（RTA，轴向由母区参考系定义）——各可为常数、逐孔 profile 变量或 profile Parameter；**Flow Direction**（可独立于孔向）：hole-direction / from-boundary-panel（取自重叠边界条件）/ normal-to-boundary / cartesian / cylindrical；**Hole Shape**：cylindrical（Diameter）或 rectangle（Length/Width）。**Note：孔形 = 指定孔向在局部面上的投影——非法向"斜钻孔"使圆柱孔在边界上呈椭圆、正方形矩形孔变形**（图 15.20）。**Flow Variables**：开能量且 BC 型为进口/墙 → 须给温度；进口/出口 → 须给质量流量或总压。**Mass Flow 选项**：from-boundary-panel / profile / constant-per-hole / **total-mass-flow**（所有定位孔的总流量均分）/ **total-for-all-sectors**（按整轮 360° 总流量给、按建模扇区比例分配再逐孔均分）。**Temperature 选项**：from-boundary-panel / profile / **radial-distribution**——**Eq 15.14** 孔内温度二次分布（用户常数 A、B + Reference Temperature 常数或逐孔 profile；按孔面心相对孔心的径向位置计算；**k 由 Fluent 自动求值使每孔焓通量 ≈ 均匀温度情形——降低对孔网格分辨率的敏感性**）。pressure-inlet → **Total Pressure**（from-boundary-panel / profile）+ **Loss Coefficient**（钻孔压头损失，p. 1482）：from-boundary-panel / constant / **factor-and-length-ratio**（Darcy 摩擦因子 + 假设长径比内部计算）。可建多几何——按位置分组（压力面/吸力面/hub/shroud）。
- **建 Boundary Interface**（15.7.2）：outline 右键 Boundary Interfaces → New：命名；Boundary Zones Side 1 = 孔所在边界；Geometry Zones Side 2 = 孔几何；**Preview 只显示孔位标记（非真实形状大小**；标记符号/颜色经 `/define/virtual-boundary/hole-geometry/edit/[geometry-name]/preview` 改）；Create/Edit。**Fluent 求交后：每个几何一个 overlap 边界 + 每个底层边界区一个 non-overlap 边界**（图 15.21）；overlap 边界按几何类型自动建为 mass-flow inlet/outlet 或 inlet vent（pressure）。**Note：选了 profile 等（非 constant/from-boundary-panel）选项时，Fluent 生成仅对该重叠边界有效的内部 profile（名以 vbr 开头）并自动挂接**。
  - **旋转周期对上的孔位**（15.7.2.1）：孔位落在边界区与周期边界之外时，**Fluent 自动按周期对节距角逐次旋转孔位直至重叠**（母区有轴矢量且至少一对旋转周期界面时自动触发）；旋转后仍找不到的孔保持未定义。大孔触及/跨越周期边界时，界外部分变换到另一周期边界内侧——孔看似跨周期对。此功能降低周期边界位置对孔位的敏感性。
- **组成**（15.7.3）：outline 展开界面可见 boundary zone、non-overlap zone（后缀 -non-overlapping）、geometry、overlap zone（int-...-overlap-1-1）；Display 时 non-overlap 显示未相交面、overlap 显示相交网格（孔的真实形状尺寸）。
- **重叠边界条件**（15.7.4）：类型由几何定义已定；Fluent 按几何规格自动设置选项（profile/constant-per-hole → 内部 profile 自动挂到 Mass Flux；from-boundary-panel → 须手动给质量流量 = 全部孔总流量按面积加权分配）；逐孔核对流向；其他入流参数（湍流、温度——孔级数据用 profile 选项 + 附加数据列）。**Important：可手动改重叠 BC，但易与几何规格不一致——建议改几何而非直接改边界条件**。
- **限制**（15.7.5）：仅边界（非体积）——流动注入只能挂在引用既有边界的 Boundary Interface 上；**孔之间不得重叠**；孔心须在 cell zone 网格内或附近（否则警告并排除）；**边界条件逐孔为常数、不能在单孔内变化**；报告的边界通量会显示逐孔质量流量与所有几何合计（重复计）——**Net Results 不含重复、收敛后仍应趋零**；**瞬态运动转子上的 BFC：profile 用跟随转子的局部参考系时，几何的 Mass Flow 若非 from-boundary-panel 会施加错误流量；转角超过一个节距可能失稳；即使用 from-boundary-panel，定义多个 Boundary Interface 时孔位也可能不随转子正确更新**。

## 15.8 叶轮机械描述（Turbomachinery Description，pp. 2091–2092）

- 众多模型/功能需要叶轮信息（建模行数、每行通道/扇区数、整轮叶片数）。两种定义方式：**Turbo Setup 工作流自动定义**；或手动 `/define/turbo-models/create-turbomachine-description`（提示行数；每行给名称、cell ID、360° 轮扇区数、CFD 模型建模扇区数）。**谐波导出（p. 2058）与 Fourier 谐波后处理（p. 2100）的前置步骤**。`list-turbomachine-description` 打印当前描述；`delete-turbomachine-description` 删除。**注意手册命令路径不一致**：本节作 `turbo-models/`（带 s），p. 2058/p. 2353 处作 `turbo-model/`（无 s）——实际以控制台可补全者为准。

## 15.9 叶轮专属数值（TSN，pp. 2092–2094）

- **TSN（Turbomachinery-Specific Numerics）**= 内置定制数值设置，帮助/加速叶轮流动收敛。条件：**Turbo Models 启用 + 压力基 + 定常**，且 **Pseudo Time Method 为 Global Time Step 选项**（p. 3815）。在 Solution Methods 任务页启用（图 15.23）。
- 激活内置定制 + 可选设置：**HOTR 高阶项欠松弛（p. 3717）——类型 Convection Only、全变量 Relaxation Factor 0.1**；**Apply Limiter Filter（修改参数版，p. 3764）**。关闭 TSN 恢复默认。**Note：Time Step Method = Automatic + 较大 Time Scale Factor + 默认伪时间设置时最有用；TSN 仍收敛困难 → 关闭 TSN 并把动量伪时间显式欠松弛从 0.5 降到 0.1（Solution Controls；更慢但可收敛）**。

## 15.10 叶轮机械后处理（pp. 2094–2124）

- **拓扑定义**（15.10.1）：后处理专用坐标系的前提。**不再限单排——多排可同时定义全部拓扑**、命名管理、对单个或全部拓扑执行后处理。**Important：叶轮坐标只在流体区边界条件对话框正确给出旋转轴时才能正确生成（p. 1373）**。Turbo Topology 对话框（Domain → Turbomachinery → Turbo Topology...）：选边界类型 → 选面（Group By Surface Type / Filter Text 过滤）→ 逐类型指认 → **Important：完整拓扑要求 inlet、outlet、hub、shroud、periodic、theta min/max（如有）构成封闭域** → 命名 Define（后处理功能激活）。**零角线**：`display/set/zero-angle-dir` 设域外位置矢量（默认 x 轴；若穿过域须另设，避免角坐标不连续）。Display 核对 / Modify / Delete。**拓扑随 case 保存**（读回无须重设）；用 BC 文件在相似 case 间传递拓扑可能失败 → 手动重设。TUI：`define/turbo-model/turbo-topology`（2020 R1 起）。
  - **边界类型**（15.10.1.1）：Hub（通道下壁、靠轴侧）、Shroud（上壁、离轴侧）、Theta Periodic（周向周期边界区）、**Theta Min/Theta Max（周向边界上最小/最大角位置的墙区）**、Inlet、Outlet、**Blade（叶片墙区——不能与周向边界相连；该情形用 Theta Min/Max 定义叶片）**。
  - **叶轮专属变量**（15.10.1.2）：Meridional Coordinate、Abs Meridional Coordinate、Spanwise Coordinate、Abs (H-C) / Abs (C-H) Spanwise Coordinate、Pitchwise Coordinate、Abs Pitchwise Coordinate——在变量列表 **Mesh...** 类（定义见 p. 4395）。
- **云图/矢量**（15.10.2）：先定义拓扑；**Turbo surface** 用 Iso-Surface 对话框（Surface of Constant → Mesh... → 叶轮变量；From Zones 选区；Compute → Iso-Values → Create；**建议每区单独建 iso 面**）。**Periodic Instancing**（15.10.2.2）：绕轴复制通道显示周期重复图样（Domain → Turbomachinery → Periodic Instancing...；详见 p. 4257/5492）。
- **通用 Fourier 系数后处理**（15.10.3）：**所有瞬态 case + Turbo Models 启用即可用**；累积变量：静压、温度、速度分量、k、ε、ω。
  - **理论**（15.10.3.1）：用 Fourier 系数实数表示，提供 Ā 与 B 变量；支持多（M 个）基频、各自谐波内容；**累积用移动平均法，等效闭区间积分形式（Eq 15.15）——积分周期必须为所有被捕获频率的公共周期**；重构信号（Eq 15.16）与附加变量（Eq 15.17/15.18，系数的时间步变化量）一并提供。
  - **前置**（15.10.3.2）：Turbo Model 启用；Turbomachine Description 完整；Run Calculation 用 **Fixed 时间推进**（建议 Frequency-Based/Period-Based、时间步足够小、Time Steps per Period ≈ 40）。
  - **两类场景**（15.10.3.3）：①一般 case（周期扇区或全轮）——进口/出口扰动、叶片颤振、TRS 三用例，可视化任意瞬态周期叶轮仿真的谐波状态；谱描述控件独立（可与 BC 谱不同）；②phase-lag 单通道——进口/出口扰动与叶片颤振两用例；cell-zone 系数与 phase-lag BC 系数非严格相同，但**谱内容一致时是良好近似**；已定义 phase-lag 边界时首个提示询问是否复制谱设置（`/define/turbo-models/create-graphics-spectral-content`，"Copy from phase lag spectral description? [yes]"）。
  - **创建图形谱内容**（15.10.3.4）：功能区 **Spectral Content** 下两项——**Update Graphics Spectral Content from Phase Lag Data**（从 phase-lag 谱原样复制，最常用）/ **Update Graphics Spectral Content from Disturbances**（从已定义扰动推导：进口/出口用边界 profile 的 NumberSectors360、颤振用振型频率）；不适用时手动 `/define/turbo-model/create-graphics-spectral-content`（逐行输入扰动/频率；可算 modal influence coefficients）。
  - **额外设置**（15.10.3.5）：`/define/turbo-model/graphics-extra-settings`：**Fourier 系数欠松弛（图形谱默认 1.0——注意与 phase-lag 的 0.7 不同）**；初始化周期数（默认 0）；每基频默认谐波数（默认 10）。多行 case 频率选择算法：**1 = nearest neighbors（仅紧邻上下游部件频率）、2 = extended neighbors（所有转子见所有静子频率、反之亦然）、3 = user selected**。辅助命令 list/append/delete-graphics-spectral-content。
  - **图形后处理**（15.10.3.6）：系数按流动变量分组、按模态与频率标注（图 15.28）。
- **周向平均 profile 提取**（15.10.4）：Turbo Models 启用后可写周向平均 profile——适用于 inlet、outlet、interfaces、planes、iso-surfaces、iso-clips 上的流动变量；**profile 类型（径向/轴向）由机器类型内部判定**（p. 987）。
- **Turbo Post**（15.10.5，Results → Model Specific → Turbo Post）：
  - **报告**（15.10.5.1，Turbo Report 对话框）：Averages 选 **Mass-Weighted 或 Area-Weighted**；选拓扑；Process 选 **Expansion（涡轮）或 Compression（泵/压气机）**；Compute 计算；Write 存文件。量：质量流量（**Eq 15.19** ∫ρv⃗·n⃗dA）；**Swirl Number（Eq 15.20**，r 为距转轴径向坐标、v_t 切向速度）；平均总压（面积分 **15.21** / 质量加权 **15.22**）；平均总温（**15.23/15.24**）；平均气流角（径向/切向，面积分 **15.25/15.26**、质量加权 **15.27/15.28**）；**通道损失系数**（工程式 **15.29** (p0,in − p0,out)/(½ρV²in) 与归一化式 **15.30** (p0,in − p0,out)/(p0,in − p_static,out)）；**轴向力（15.31**：旋转部件表面全应力张量在轴向投影积分）与**扭矩（15.32**：位置矢量叉乘应力投影的轴向分量积分）。**效率**（假设定常、进出口流量相等——不含气膜冷却/引气损失）：不可压泵/风机 = 水力效率（**15.33**：体积流量 × 总压升 / (扭矩 × 转速)；另有容积效率与机械效率合成总效率）；可压压缩机 = 绝热效率（**15.34** (h02s − h01)/(h02 − h01)；定 cp 时用总温形式 **15.35**；等熵关系 **15.36**；紧凑式 **15.37** 只需实际状态 1、2 数据）；**多变效率（15.38）**；涡轮不可压（**15.39**）与可压（**15.40–15.43**，紧凑式同理只需实际状态）、涡轮多变效率（**15.44**）。公式体均未提取、变量语义自正文记录。
  - **平均云图**（15.10.5.2）：变量周向平均后投影到 m-b 平面显示；拓扑选 All 或具体；Levels 最大 **100**；对话框 Min/Max 为**平均值极值**（与同时显示的 Domain Min/Max 不同）。
  - **2D 云图**（15.10.5.3）：等展向坐标面上的云图投影到平面（高度 3D 面更易评估）；Normalized Spanwise Coordinates 0–1。**Important：hub/shroud 为曲面时，极近的 iso 面可能含空隙（仅显示平面切割面）**。
  - **平均 XY 图**（15.10.5.4）：周向平均量沿展向/子午画图；X Axis Function 两选——**Hub to Casing Distance**（Fractional Distance = Inlet to Outlet）或 **Meridional Distance**（Fractional = Hub to Casing）；可 Write to File。
  - **全局拓扑**（15.10.5.5）：Turbo Options 对话框设 Current Topology（如建 iso 面用）。
- **Turbo Performance**（15.10.6，Domain → Turbomachinery → Turbo Performance... 或 `/define/turbo-model/performance`）：用**命名表达式**计算性能特性——效率、总压/总温比、进出口质量流量。对话框：进出口面列表（按支持类型过滤）；**Efficiency Type：Isentropic 或 Polytropic**；**Process：Expansion 或 Compression**；**Efficiency Ratio：Total to Total / Total to Static / Static to Static**；Define 生成表达式（默认名后自动加整数；Expression Manager 查看/编辑）；Report Definitions... 监视/打印/写/绘图（p. 4349）；Display 显示所选面。
  - **命名表达式效率**（15.10.6.2）：函数 **EfficiencyIsentropic / EfficiencyPolytropic**（Functions → Reduction）；位置可选各类可透边界（进口/出口/interfaces）、cut-plane、iso-surface 与面组；多进口合并为单股平均流（效率计算起点）。**限制：仅可压流——理想气体、单组分真实气体、凝结水蒸气（Wet Steam）**；支持位置清单：Pressure Inlet/Outlet、Mass-Flow Inlet/Outlet、Velocity Inlet、Pressure-far-field、Inlet/Outlet Vent、Intake/Exhaust Fan、Interior、Interface、Cut-plane、Iso-surface、面组。
  - **Turbo Report 效率**（15.10.6.3）：默认按**定 Cp、定 γ 的 Total to Total 等熵/多变效率**计算；`/report/efficiency/use-in-turbo-report?` 切换到 EfficiencyIsentropic/Polytropic 的通用公式——**定 Cp 理想气体两法几乎一致；其他工况只有函数法结果可靠**。
  - **总压/总温比**（15.10.6.4）：`MassFlowAveAbs(Field,['location_1']) / MassFlowAveAbs(Field,['location_2'])`；Field = TotalPressure 或 TotalTemperature；**Expansion 时 loc1 = 进口、loc2 = 出口；Compression 反过来**。
  - **质量流量**（15.10.6.5）：`MassFlowInt(1, ['locations'])`。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.15；本页覆盖批次 57（pp. 1993–2035，15.1–15.3）、批次 58（pp. 2036–2076，15.3.4.3 + 15.4–15.5）与批次 59（pp. 2077–2124，15.6–15.10），均 2026-10-18 读取。**Ch.15 全章已摄取完毕。**
- **公式体未提取**：Eq 15.1（legacy 欠松弛）、15.2–15.13（能量法/ICM/phase-lag）、15.14（孔内径向温度分布）、15.15–15.18（Fourier 系数定义/重构/变化量）、15.19–15.44（Turbo Report 各量与效率）公式体均为图形对象，仅按周边文字记录变量与语义，未杜撰形式；损失系数两式与效率各式的分子分母构成按正文变量清单记录。Figures 15.17–15.39 为图形元素未摄取。
- 本页数值（TSN HOTR 因子 0.1、图形谱欠松弛默认 1.0、谐波默认 10、Levels 上限 100、示例孔径 3.4 mm/注入温度 420 K、profile 参数示例等）为原文正文数值。
- 手册原文瑕疵三处已如实记录：p. 2070 小节标题跨章残留编号 "21.2.3.6"；`/define/turbo-mode/phase-lag-extra-settings` 路径疑为 turbo-model 之误；Turbomachine Description 命令路径在 `turbo-models/`（15.8 节）与 `turbo-model/`（p. 2058 等）间不一致——引用命令时建议先在控制台验证。
- 关联章节引用（CSV Profiles p. 1619、Profiles 对话框 p. 1624、zone motion/旋转轴 p. 1373、参考帧 p. 1202、损失系数 p. 1482、周向平均 profile p. 987、HOTR p. 3717、梯度限制器 p. 3764、伪时间 p. 3812/3815、Periodic Instancing p. 4257、表达式语言 p. 1059、表达式报告 p. 4349、Wet Steam 设置 p. 3288、Field Function p. 4395）仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 运动参考系]]（MRF/frozen rotor——GTI FR 的基础）
- [[Fluent 滑移与动网格]]（TRS = 滑移网格；Mesh Motion）
- [[Fluent Cell Zone 与边界条件设置]]（非一致界面与 Mesh Interfaces、径向平衡出口）
- [[index]]
