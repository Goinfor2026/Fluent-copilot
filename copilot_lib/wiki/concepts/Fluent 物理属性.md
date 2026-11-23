---
type: concept
created: 2026-10-17
updated: 2026-10-17
tags:
  - Ansys Fluent
  - materials
  - density
  - viscosity
  - non-newtonian
  - solution-mode
  - automation
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 物理属性

## 摘要

User's Guide 2026 R1 Part III / Chapter 9 "Physical Properties"（PDF pp. 1651–1797，共 17 节）讲材料与物理属性定义。**本页已覆盖全章（批次 47–49，pp. 1651–1797）**：材料类型与三大数据库、温度函数四型（含 NASA-9）、密度全选项、黏度全选项（含四种非牛顿模型）、导热系数（含固体各向异性六法）、UDS 扩散率、电导率、热容、辐射属性与 WSGGM、质量扩散系数、标准态焓/熵、未燃热扩散率、动能理论参数、操作压力与参考压力、真实气体模型三方案（立方 EOS/NIST/UDRGM）与 RGP 表文件。

## 9.1 材料定义（pp. 1651–1670）

- **属性清单**：密度/分子量、黏度、热容、导热系数、UDS 扩散系数、质量扩散系数、标准态焓、动能理论参数。属性可为温度和/或组分依赖（多项式/分段线性/分段多项式；组分属性可自给或动能理论算）。Materials 任务页按激活模型显示所需属性；**定义需要能量方程的属性（理想气体律密度、温度函数黏度等）会自动开启能量方程**（热边界条件仍须自己设）。
- **固体材料**（9.1.1）：只定义密度、导热系数、热容（半透明介质另加辐射属性）。导热系数：常数/温度函数/UDF；热容：常数/温度函数；**密度：仅常数**。压力基下固体密度与热容仅在瞬态或固体区运动时必需——稳态时热容只用于焓后处理。
- **材料类型与数据库**（9.1.2）：六类——fluid、solid、mixture、combusting-particle、droplet-particle、inert-particle。组分输运 → 定义 mixture 材料（含各 species）；DPM 用三种颗粒材料。内置库：①Fluent 全局库约 **675 种材料**（`path/ansys_inc/v261/fluent/fluent26.1.0/cortex/lib/propdb.scm`）；②**GRANTA MDS** 700+ 固体（**需单独许可证**；license 持有 30 分钟或至程序关闭；无 license 时只显描述、复制中止）。**Important**：本地材料清单随 case 文件保存；同一材料可同时作为纯流体与某 mixture 的 species——**两者是独立对象、属性独立**（改纯流体不影响 mixture 里的版本）；建议复制纯流体改名后用于 mixture。
- **Create/Edit Materials 对话框**（9.1.3，Setup → Materials）：默认本地清单 = air（fluid）+ aluminum（solid）；mixture 材料仅在开启组分输运后出现；**从库复制 mixture 时其全部组分 species 自动一并复制**。改属性：选类型 → 选材料 → 改 Properties → Change/Create。改名/新建：**Name 字段最长 29 字符**（超长报错）；Question 对话框 Yes = 覆盖改名、No = 保留原材料并新建（新建会要求输入化学式，可留空）。从 Fluent Database 复制：Fluent Database... → 选 → Copy（库中原件不受本地修改影响）。**保存**：本地清单随 case 写出。删除：任务页/树/对话框均可——只删本地、不动全局库。排序：Order Materials By 选 Name 或 Chemical Formula（两对话框各自独立设置）。
- **用户自定义材料库**（9.1.4）：.scm 文本文件，格式示例（air/aluminum）：
  ```scheme
  ((air fluid (chemical-formula . #f)
     (density (constant . 1.225) (premixed-combustion 1.225 300))
     (specific-heat (constant . 1006.43)) ...))
  ```
  功能：浏览/复制/新建库与材料/从 case 复制材料入库（Copy Materials From Case...——**Note：不要逐个复制，先复制的会被后复制的覆盖；应全选后一次 Copy**）/改库中材料（Edit → Material Properties → Edit Property Methods）/删库中材料（改后 Save）。同名冲突弹 New Material Name 对话框改名。

## 9.2 温度函数属性（pp. 1670–1679）

- 四种函数：**polynomial**（9.1，最多 8 系数，系数数 = 阶数+1，1 个系数即常数）；**piecewise-linear**（9.2，n 段）；**piecewise-polynomial**（9.3）；**nasa-9-piecewise-polynomial**（9.4，**仅热容 Cp 可用**——高超声速/双温模型，分段多项式不适用时）。**Important：polynomial 与 piecewise-polynomial 的温度一律按 K 或 R 计算——温度单位用 ℃/K 时系数按 K 输入，℉/R 时按 R 输入**。
- 输入要点：piecewise-linear 最多 **50 个点**、数据对按温度升序手输（**求解器不排序**）；**外推规则：T 超出最大值用最大值处的值、低于最小值用最小值处的值**。piecewise-polynomial 最多 **3 个温度区间**（升序输入），每区间最多 8 系数；NASA-9 最多 **8 个区间**、每区间最多 8 系数（Static Temperature 自动选为自变量）。**Important：用多项式给定材料属性时应设置解限值，保证多项式返回值物理有效（如密度非负），见 Setting Solution Limits（p. 3759）**。检查/修改已有函数：属性旁 Edit...；**Fluent Database Materials 对话框里只能 View... 不能编辑**。

## 9.3 密度（pp. 1678–1688）

- **按流态选型**（9.3.1）：可压 → ideal-gas；不可压 → 常数 / incompressible-ideal-gas（自然对流，压变可忽略但要用理想气体温度关系）/ 温度函数（polynomial/piecewise-linear/piecewise-polynomial）/ **boussinesq**（小温差自然对流）/ **compressible-liquid**（高压可压液体）。
- **多区混用限制**（9.3.1.1）：压力基（非通用多相）下**可压理想气体律不得与其他密度方法混用——一种材料用了就全部要用**（密度基无此限制）；全模型只有一个操作压力与一个操作温度（多材料理想气体共享操作压力、多材料 Boussinesq 共享操作温度）。
- **Boussinesq**（9.3.3）：Density 下拉选 boussinesq + 常数密度 + Thermal Expansion Coefficient + 操作条件（见 8.3.1.2）。
- **可压液体 compressible-liquid**（9.3.4）：**Tait 状态方程**（等温密度-压力非线性关系，9.7–9.10；系数由参考压力/参考密度/参考体积模量确定，n 为密度指数）；**密度比被限制在 [最小， 最大] 密度比限内**（9.11）；声速可后处理（9.12；多相按混合/相级别；用户自定义密度给了声速也可）。用途：高压液体可压缩性；**减少动/动网格应用（固-流相互作用）中的非物理压力尖峰**。输入六项：Reference Pressure、Reference Density、Reference Bulk Modulus、Density Exponent、Maximum/Minimum Density Ratio Limit。**Note**：部分材料 Fluent 按公开文献自动填值（无数据填零——必须核实）；自动填充的密度指数接近水值；**密度指数一般按密度/压力/体积模量/声速数据标定；未知时建议用 1（密度-压力线性关系）**。TUI 示例（water-liquid 默认）：Ref Pressure 101325、Ref Density 998.2、Ref Bulk Modulus 2.2e9、Density Exponent 7.15、Max/Min Ratio 1.1/0.9。**可用性**：流体材料或 mixture 组分（该组分密度法 = volume-weighted-mixing-law）；**密度基求解器不可用**。
- **温度函数密度**（9.3.5）：piecewise-linear / piecewise-polynomial / polynomial 三种。
- **不可压理想气体律**（9.3.6）：ρ = p_op·M/(R·T)（9.16）——**只依赖操作压力、不依赖局部相对压力场**。输入：incompressible-ideal-gas + Operating Pressure（默认 101325 Pa；取值建议见 9.15）+ 分子量。
- **可压理想气体律**（9.3.7）：ρ = (p_op + p)·M/(R·T)（9.17）——操作压力加到求解器算出的相对压力上得绝对静压。输入：ideal-gas + Operating Pressure + 分子量。
- **组分依赖密度**（9.3.8，多组分 mixture）：方法——**volume-weighted-mixing-law**（非理想气体混合物）；**compressible-volume-weighted**（可压混合、组分含 RGP 表真实流体和/或理想气体；**含至少一个 RGP 组分时推荐**；全理想气体 → 用 ideal-gas；需先建 RGP 材料表，p. 1794；密度公式同 volume-weighted 但用可压热物性算法）；ideal-gas（可压流）；incompressible-ideal-gas；user-defined / **user-defined-mixing-law**（区别：后者可逐 species 给属性；species 侧只有 constant/polynomial/user-defined）。混合物密度公式：非理想气体 1/ρ = Σ(m_i/ρ_i)（9.18）；可压混合理想气体 ρ = p_op·Σ(m_i M_i)/(R T)（9.19）；不可压理想气体 ρ = p_op/(R T Σ(m_i/M_i))（9.20）。

## 9.4 黏度（pp. 1688–1699）

- **输入的是动力黏度 μ（SI kg/m-s）**——Fluent 不要求运动黏度。选项：常数、温度/组分依赖、动能理论、非牛顿、UDF。默认 air：1.7894e-05 kg/m-s。
- **温度函数五种**（9.4.2）：piecewise-linear / piecewise-polynomial / polynomial / **Sutherland 律** / **幂律**（此幂律≠非牛顿幂律）。**Sutherland**（9.4.2.1）：两系数式 μ = C1·T^(3/2)/(T+C2)（9.24；中等温压空气 C1 = 1.458×10⁻⁶ kg/m-s-√K、C2 = 110.4 K）或三系数式 μ = μ0(T/T0)^(3/2)·(T0+S)/(T+S)（9.25；空气 μ0 = 1.716×10⁻⁵ kg/m-s、T0 = 273.11 K、S = 110.56 K）；输入选 Two/Three Coefficient Method（**两系数法必须 SI**）。**幂律**（9.4.2.2）：稀释气体常用、精度略逊 Sutherland；两系数 μ = B·T^n（9.26；空气 B = 1.458×10⁻⁶、n = 2/3）或三系数 μ = μ_ref(T/T_ref)^n（9.27；空气 μ_ref = 1.716×10⁻⁵、T_ref = 273.11 K、n = 2/3）；两系数法必须 SI。
- **动能理论黏度**（9.4.3）：配理想气体律；μ = 2.67×10⁻⁶·√(M·T)/(σ²·Ω_μ)（9.28–9.29；μ kg/m-s、T K、σ 埃、M 分子量、Ω_μ 碰撞积分）；输入 Lennard-Jones 参数 σ 与 ε/k（见 9.14）。
- **Gupta 曲线拟合**（9.4.4）：高超声速单温模型，空气混合物至 30 000 K（p. 2397）。
- **组分依赖黏度**（9.4.5）：mixture 选 **mass-weighted-mixing-law** 或（密度为理想气体时）**ideal-gas-mixing-law**；UDF 两法同前（mixing-law 变体可逐 species 给属性）。理想气体混合物按动能理论算（9.30–9.31，摩尔分数）；非理想气体混合物按组分质量分数简单平均（9.32）。
- **非牛顿黏度**（9.4.6）：τ = μη（9.35）；**η 只取剪切率 γ̇ 的函数**（9.36，变形率张量第二不变量）。**温度依赖**（9.4.6.1）：总黏度 = H(T)·η(γ̇)（9.37）；**H(T) 为 Arrhenius 律**（9.38；α = 活化能/气体常数、T_alpha 参考温度（H=1）、ΔT 温度偏移默认 0 = 热力学最低可接受温度）；**仅在能量方程开启时计入；α 设 0 即忽略温度依赖**。四种模型：**Power law**（9.39：η = k·γ̇^(n−1)；k 稠度系数、n 幂律指数——**n=1 牛顿、n>1 剪切增稠（胀流）、n<1 剪切变稀（假塑性）**）；**Carreau**（9.40：η = η∞ + (η0−η∞)[1+(λγ̇)²]^((n−1)/2)；λ 时间常数、η0/η∞ 零剪/无限剪黏度、a 形状参数（默认 2 = 原始 Carreau））；**Cross**（9.41：η0 零剪黏度、λ 自然时间（牛顿→幂律转变的剪切率倒数）、n 幂律指数；常描述低剪切率行为）；**Herschel-Bulkley**（9.42–9.44：τ = τ0 + k·γ̇^n 的 Bingham 塑性——τ<τ0 刚性、τ>τ0 幂律流动；低剪切率下"刚性"材料表现为极高黏度流体；常用于混凝土、泥浆、面团、牙膏；选用时以式 9.43 定黏度）。各模型输入均含 Min/Max Viscosity Limit；温度依赖法另给 Reference Temperature T_alpha 与 Activation Energy/R alpha。**Important：四种非牛顿模型在湍流下均不可用；单流体表述的 non-Newtonian 模型可用于 mixture 模型——建议挂到主相**。

- **Herschel-Bulkley 输入**（9.4.6.5.1，p. 1700）：Consistency Index k、Power-Law Index n、**Yield Stress Threshold τ0、Critical Shear Rate γ̇0**；温度依赖法另加 T_alpha 与 alpha。该模型依 n 值也可表现剪切变稀/增稠。

## 9.5 导热系数（pp. 1700–1713）

- 传热激活时必须定义（能量 + 黏性流动建模）。单位 W/m-K。选项：常数（air 0.0242 W/m-K）；温度/组分依赖；动能理论；**各向异性（仅固体材料）**；UDF。
- 温度函数：piecewise-linear / piecewise-polynomial / polynomial 三种。
- **动能理论**（9.5.3）：配理想气体律；k 由 R、分子量 M、已定/已算的黏度 μ 与热容 Cp 计算（9.48，公式体未提取）。
- **Gupta 曲线拟合**（9.5.4）：高超声速空气混合物至 30 000 K（p. 2397）。
- **组分依赖**（9.5.5）：mixture 选 mass-weighted-mixing-law 或（理想气体时）ideal-gas-mixing-law；UDF 两法（mixing-law 变体可逐 species 给属性，仅 constant/polynomial/user-defined）。**Important：混合物导热用 ideal-gas-mixing-law 时，黏度必须用 ideal-gas-mixing-law 或 mass-weighted-mixing-law**（理想气体导热公式 9.49 需要组分黏度）。理想气体混合物按动能理论（9.49–9.50，摩尔分数）；非理想气体按质量分数平均（9.51）。
- **固体各向异性导热**（9.5.6）：热通量 q = κ·∇T 矩阵形式（9.52）。六种：**anisotropic**（直接给 2×2/3×3 矩阵 κ_ij，9.53，**可为非对称矩阵**，乘标量导热系数——常数/温度多项式/UDF；主轴与全局轴不对齐时要么自己变换张量、要么改用 orthotropic（轴正交）或 principal-axes-values（轴非正交））；**biaxial**（**仅壳导热固体**；Transverse 垂直壳面 + Planar 平行壳面（各向同性）两种导热）；**orthotropic**（主方向 a⃗0/a⃗1/a⃗2 互相正交 → 3D 只须给前两个方向；Conductivity 0/1/2 可为常数/多项式/分段函数/user-defined/expression/New Input Parameter——TUI 先 `define/parameters/enable-in-TUI? yes`；2D 只给 k0(x,y) 与 a⃗0）；**cyl-orthotropic**（柱坐标径/周/轴三向导热；3D 给原点+方向、2D 只给原点（方向恒 +Z）；Fluent 按单元位置自动算各向异性矩阵；**近壁处导热用壁旁单元而非壁本身计算**）；**principal-axes-values**（主轴 n1/n2/n3 线性无关但不须单位/正交 + 主值 K1/K2/K3，变换式 9.56–9.58）；**user-defined-anisotropic-k**（矩阵分量非常数/独立变化——DEFINE_ANISOTROPIC_CONDUCTIVITY UDF）。
- **Important：各向异性导热选项仅压力基可用（密度基不行）**。后处理：使用各向异性模型时 Thermal Conductivity 显示为零——改看 Thermal Conductivity XX…ZZ 分量（orthotropic 对称矩阵不提供 YX/ZX/ZY）。各向异性固体区的求解设置（热通量算法/温度梯度法/热通量系数松弛）见 p. 2237。

## 9.6 UDS 扩散率（pp. 1713–1720）

- 两类：**各向同性**与**各向异性**。各向同性两种给法：单个 user-defined 作用于全部 UDS 输运方程；或 defined-per-uds 逐标量给常数/温度多项式/UDF。
- **各向异性**：逐 UDS 给张量扩散矩阵 Γ（9.59，3D 为 3×3），**流体区与固体区都可用**；典型用途——多孔介质与固体中的组分输运。四种：anisotropic（Γ = Γ0·A，A 可非对称；Γ0 常数/多项式/UDF）、orthotropic（主方向 + 三向扩散率；3D 只须前两方向；2D 只有径/周向）、cyl-orthotropic（柱坐标径/周/轴；2D 方向恒 +z；按单元位置自动算）、user-defined-anisotropic（DEFINE_ANISOTROPIC_DIFFUSIVITY）。**Important：各向异性扩散选项压力基与密度基都可用；UDS 扩散系数只能在各向同性单元里后处理——其他单元显示为零**。各向同性默认 air 常数扩散系数值未提取。

## 9.7 电导率（pp. 1720–1722）

- 电位方程激活时必须定义；单位 S/m。选项：常数；温度函数（piecewise-linear/polynomial/piecewise-polynomial）；**各向异性（仅固体）**：anisotropic/orthotropic/cyl-orthotropic（矩阵形式同 9.53/9.54；对话框为模态须立即处理；2D 给两主方向导热与单位向量）；UDF（DEFINE_PROPERTY）与表达式。

## 9.8 热容（pp. 1722–1724）

- 能量方程激活时必须定义；单位 J/kg-K。**Important：燃烧应用推荐温度依赖 Cp**。选项：常数（air 1006.43 J/kg-K）；温度函数四种——piecewise-linear/piecewise-polynomial/**nasa-9-piecewise-polynomial**/polynomial（Cp 是唯一可用 NASA-9 的属性）；动能理论（9.67，需给气体储能模式数/自由度）；组分依赖：mixture 选 **mixing-law** + 逐 species 常数/温度函数/动能理论，混合物 Cp = 组分质量分数平均（9.68）。

## 9.9 辐射属性（pp. 1724–1728）

- 除 S2S（无需附加属性）外，激活辐射模型即需设置。**按模型**：P-1 → 吸收系数 + 散射系数；Rosseland → 吸收 + 散射；DTRM → 仅吸收系数；DO 与 MC → 吸收 + 散射 + （半透明介质）折射率——**DO 与 MC 可给固体材料的辐射属性（半透明介质用）**。
- **吸收系数**（9.9.1）：常数/温度函数/组分依赖/UDF；RTE 吸收-发射项为其函数；仅吸收时服从 Lambert 定律 I = I0·e^(−κx)（9.69）；单位 1/长度；可由 CO2/H2O 发射率表算。**非灰 P-1/DO/MC**：可逐灰带给常数（gray-band 选项 → Gray-Band Absorption Coefficient 对话框）。**组分依赖 = WSGGM**（加权灰气体和模型）：须开启组分计算且 mixture 含 CO2 与 H2O；三选项——**wsggm-domain-based**（路径长度 = Fluent 按域平均尺寸算的平均光程，无需输入）、**wsggm-user-specified**（用户给 Path Length）、**user-defined-wsggm**（初值同 domain-based、可挂 DEFINE_WSGGM_ABS_COEFF UDF 定制，含烟灰吸收系数定制）。**颗粒/烟灰影响**：DPM 对话框开 Particle Radiation Interaction（**仅 P-1 与 DO**）；Soot 对话框开 Soot-Radiation Interaction（任意辐射模型，但须用 WSGGM；user-defined-wsggm 可定制烟灰项）。
- **散射系数**（9.9.2）：默认 0、各向同性；常数/温度函数/UDF；单位 1/长度；燃烧含颗粒物时可调大。相函数：isotropic（默认）/ linear-anisotropic（给相函数系数）/ **Delta-Eddington（仅 DO**；Forward Scattering Factor + Asymmetry Factor）/ user-defined（仅 DO）。
- **折射率**（9.9.3）：介质光速/真空光速；默认 1；常数；非灰 DO/P-1/MC 用 refractive-band 逐带给。
- 后处理（9.9.4）：Radiation... 类的 Absorption Coefficient / Scattering Coefficient / Refractive Index。

## 9.10 质量扩散系数（pp. 1728–1735）

- 组分输运扩散两种模型：**Fickian 扩散**（默认；多数应用足够）与**完整多组分扩散**（扩散主导层流如 CVD 推荐；Species Model 对话框勾选；**计算代价高**）。求解器默认：层流按 Theory Guide 式 7.2、湍流按式 7.4；开完整多组分后用式 7.8。
- **Mass Diffusivity 七法**（单位 m²/s）：①**constant-dilute-appx**（所有 D_im 一个常数；Fickian；不适用于完整多组分）；②**dilute-approx**（逐 species 常数或温度多项式；Fickian；不适用于完整多组分）；③**unity-lewis-number**（无输入；全组分 Le=1；高湍流度、层流扩散贡献小时合理；不适用于完整多组分）；④**kinetic-theory**（逐对二元扩散 D_ij 动能理论；**仅理想气体**）；⑤**multicomponent**（逐 species 对 D_ij 常数/温度多项式）；⑥**expression**（表达式作用于全部扩散系数，p. 1077）；⑦**user-defined**（单个 DEFINE_DIFFUSIVITY UDF）。稀释混合物（各组分质量分数远小于主组分）→ ①或②；非稀释 → 逐对 D_ij。
- **湍流**（9.10.2）：另可调 **Turbulent Schmidt Number**（Viscous Model 对话框 Model Constants）——**默认 0.7；经验常数、对分子物性不敏感，一般无理由修改**；**完整多组分扩散不推荐用于湍流**。
- **多孔介质各向异性组分扩散**（9.10.3）：Fluid 对话框勾 Porous Zone → Porous Zone 页勾 Anisotropic Species Diffusion → 给扩散矩阵 D 分量（默认单位阵 = 各向同性；可改分量计入孔隙迂曲度）。
- **热扩散系数**（9.10.4）：Species Model 开 Thermal Diffusion 后在 Create/Edit Materials 给——kinetic-theory（经验式 7.17，无输入）/ specified（逐 species 在 Thermal Diffusion Coefficients 对话框给）/ user-defined；（输入步骤 2 起延续至 p. 1735，由批次 49 补记）。

- **热扩散系数输入续**（p. 1735，9.10.4 收尾）：specified 法逐 species 在 Species Thermal Di 列表选择后给系数——constant（默认）或温度多项式。

## 9.11–9.14 燃烧与动能理论参数（pp. 1735–1737）

- **标准态焓**（9.11）：有限速率/涡耗散反应流须逐 species 给标准态焓（生成焓）h°_i；混合焓 = Σ(m_i/M_i)·[h°_i + ∫c_p,i dT]（9.72；M_i kg/kmol、T_ref 为定义参考温度）；单位 J/kmol（SI）；Create/Edit Materials 中逐 species 设 Standard State Enthalpy + Reference Temperature。
- **标准态熵**（9.12）：**有限速率 + 可逆反应**时须逐 species 给 s°_i（9.73 同构）；单位 J/kmol-K；同样带 Reference Temperature。
- **未燃热扩散率**（9.13）：预混燃烧时流体材料应赋未燃混合物物性，含 α_u = k/(ρc_p)（Theory Guide 式 8.79）；标准条件值查燃烧手册（[85]）；非标准条件须第三方一维详细化学程序；Create/Edit Materials 中设 Unburnt Thermal Diffusivity。
- **动能理论参数**（9.14）：理想气体开启时可用动能理论定义黏度/导热/热容（流体）与质量扩散系数（多组分 mixture）。所需输入：黏度 → L-J 特征长度 σ（埃）与能量参数 ε/k（绝对温度）；**仅导热用动能理论 → 无需输入**；热容 → 自由度数（无量纲）；mixture 质量扩散 → 逐 species 的 σ 与 ε/k。参数值查文献（如 [67]）。

## 9.15 操作压力（pp. 1737–1739）

- **意义随流态而变**（9.15.1）：不可压理想气体——直接决定密度 ρ = p_op/(R T/M)，必须设对；**低 Mach 可压**——总压降相对绝对静压很小、易受舍入误差影响（相对压力变化 ~M²，M→0 时趋于零）——操作压力的作用是避免舍入误差；平均压力随时间变化的低 Mach 瞬态可压流可用**浮动操作压力**（p. 1825）；**较高 Mach 可压**——不敏感，惯例用绝对压力 → 操作压力设 0（表压 = 绝对）；密度为常数或温度 profile 时密度计算不用操作压力。默认 101325 Pa。
- **三种压力关系**（9.15.2）：绝对压力 = 操作压力 + 表压（9.74）；**Fluent 中所有输入/计算/报告的压力都是表压**。
- **设置建议**（9.15.3，Table 9.1）：理想气体 + 可压高 Mach → 0 或平均流动压力；理想气体 + 低 Mach → 平均流动压力；温度 profile / 常数密度（不可压）→ 不使用；不可压理想气体 → 平均流动压力。设置入口：Operating Conditions 对话框。

## 9.16 参考压力（pp. 1739–1740）

- **机制**：无压力边界的 cell zone（组）的不可压流或（稳态）可压流——Fluent 每次迭代后调整表压场防"悬空"：把参考压力位置处（或最近）单元的压力值从整个表压场减去 → 参考单元表压恒为零。**Note：不可压/稳态可压封闭域 patch 压力场后，参考压力会被减去——压力场将偏离指定值**。
- **默认方法（2020R2+）**：同时处理连通与不连通流体区——连通 = 经 interior/fan/porous-jump/radiator/rans-les-interface/overset 边界或共享网格界面互通；**每个连通组各用一个参考压力单元；一组里有压力边界不影响其他组做压力调整**（示例：两个盖驱动方腔组 + 一个带压力出口的通道组，只有方腔组被调整）。
- 参考压力位置默认 (0,0,0)；在 Operating Conditions 对话框改（如放在已知绝对静压点便于对比实验）。`define/operating-conditions/used-ref-pressure-location` 打印参考单元坐标、分组数、调整组数与各组 zone ID。**2020R2 前的旧 case**：默认方法假设全区连通——`define/operating-conditions/reference-pressure-method 2` 切到新方法。

## 9.17 真实气体模型（pp. 1741–1797）

- **三方案 + RGP 表**：立方 EOS（气/液/超临界，**不建模相包络线下两相区**）、NIST（液/气/超临界，不建模两相区）、UDRGM（提供关系后任意区域）；RGP 表文件可并入外部物性。均支持单组分或多组分；反应流：立方 EOS 与 UDRGM 可、NIST 不可。
- **基础概念**（9.17.1–9.17.2）：PT/PV 图、三相点、临界点（T_c/P_c——气液平衡的最高温压）、超临界流体；饱和穹顶与 spinodal 线之间的过热液体/过冷蒸气为**亚稳态**（快速泄压等瞬态局部存在）；理想气体适用条件 T ≫ T_c 或 P ≪ P_c；近临界/超临界须真实气体关系。
- **立方 EOS**（9.17.3）：Redlich-Kwong 原型（1949）及三种改进——**Soave-RK**（三参数：T_c、P_c、偏心因子 ω；油气工业主流）、**Peng-Robinson**（三参数同上；液体密度预测更优）、**Aungier-RK**（四参数：+临界比容；近临界与负偏心因子更好）。**共同限制**：进出口边界仅 pressure-inlet/mass-flow-inlet/pressure-outlet；密度基下 NRBC 不兼容（要 NRBC+真实气体 → 压力基）；**兼容 Eulerian 多相**；兼容 DPM（不考虑近临界现象，液滴温度须低于限值，见下）；**不兼容预混/惰性/组分 PDF 输运燃烧模型**；组分输运可用（有限速率+涡耗散；Dimension Reduction 不可用）；非预混/部分预混须开 Compressibility Effects（经验流不可用、冷凝组分须排除出 PDF 表、层流火焰速度按理想气体）；**亚临界近穹顶/穹顶下不建模两相——须选 Vapor 或 Liquid；亚临界与超临界可在同一仿真共存**。
  - EOS 通式 P = RT/(V−b) − αa/(V²+u b V + w b²)（9.76；各模型系数 9.77–9.87：RK u=1/w=0、SRK 的 α(T) 修吸引系数、PR u=2/w=−1、ARK 加 c0 项）。焓/熵/Cp = 理想气体部分 + **偏离函数**（9.88–9.96）。
  - 纯组分临界常数：propdb.scm 编自文献；缺者用 CRANIUM 估算；自由基按 Tang-Brezinsky/Joback 修正；煤挥发分按 CO/H2/CO2/N2/H2O 混合假设；柴油与 Jet-A = 癸烷、煤油 = 十二烷。
  - **混合物 = 伪临界法**：混合物按带伪临界常数的纯组分处理。两法：**摩尔分数平均**（9.97；各组分临界性质相近时推荐）与 **one-fluid van der Waals 混合规则**（9.98–9.103；SRK/PR 与 RK/ARK 的混合 T_c 公式不同）。
  - **启用**（9.17.3.5.1）：Density 下拉选 real-gas-soave-redlich-kwong / real-gas-peng-robinson / real-gas-aungier-redlich-kwong / real-gas-redlich-kwong。单组分输入：理想比热、分子量、标准态熵、参考温度、临界 T/P/比容、偏心因子（**Important：Cp 输入用于算理想部分 h0/cp0/s0，偏离部分自动叠加得真实气体 h/cp/s**）。混合物输入：混合材料的理想比热 + 临界 T/P/比容 + 偏心因子（方法：constant / **mole-weighted-mixing-law** / **one-fluid-van-der-waals-mixing-law**），逐组分给分子量/标准态熵/参考温度；**Important：务必点 Change/Create 让全部属性上载到界面；理想比热选 mixing-law 要逐组分给；临界性质非 constant 要给纯组分临界性质**。**Real Gas State**：亚临界工况在 Operating Conditions 对话框选 Vapor（默认）或 Liquid（TUI `define/operating-conditions/set-state`）；逐 zone/相：`define boundary-conditions modify-zones change-zone-state`（-1 全局 / 0 liquid / 1 vapor）。
  - **求解策略**（9.17.3.5.2）：真实气体收敛更慢——先一阶离散收敛再切二阶。亚临界时相态由摩尔体积立方根选取决定；spinodal 点（∂p/∂V=0）以外的穹顶内区域为亚稳态；**求解器不做两相限制——穹顶内不设限，越出气相 spinodal 发警告（"temperature is below the spinodal point in N cells"）**。多组分开 Diffusion Energy Source 时，超临界液态区与气液边界上的组分能量扩散默认被抑制——`define/models/species/liquid-energy-diffusion?` 可开。
  - **与 DPM 联用**（9.17.3.5.3）：按工况分区处理——T > T_c 无液相；T < T_c 且 P < P_sat 可直接边界条件给流股；液相存在于 P ≥ P_sat 或 T < T_b。远离临界点（T < T_lim）DPM 液滴/多组分模型足够；近临界区（T_lim < T < T_c）DPM 可用但**不考虑近临界行为、蒸发/沸腾速率方程适用性存疑**；P > 临界时液滴密度建议用 **compressible-liquid** 法。**Table 9.2 液滴材料温度限 T_lim（K）**：Argon 135.77、Benzene 505.80、Helium 4.77、Hydrogen 29.68、Methyl-alcohol 460.80、Heptanes 486.80、Hexane 456.30、Octane 512.10、Pentane 423.00、Nitrogen 113.40、Oxygen 138.60、Toluene 532.80、**Water 582.30**（附 T_c/P_c/正常沸点列）。超临界压力下 DPM 仍可用只要液滴 T < T_lim。沸点由蒸气压数据直接算（饱和蒸气压 = 域压力处温度）；蒸发潜热随液滴温度变化（9.104，按 NBP 与 NBP 处潜热）；液滴-颗粒材料须给 Normal Boiling Point 与 Latent Heat at NBP。**Important：使用真实气体时 Saturation Vapor Pressure 的常数选项被禁用；蒸气压数据须覆盖模型全部压力/温度范围**。蒸发→沸腾切换条件 P ≥ P_sat（9.105；Psat > P 切回蒸发）；超临界下该条件永不满足（蒸气压曲线止于临界点）。多组分超临界：饱和温度计算失败可能指示已达临界温度——`define/models/dpm/options/treat-multicomponent-saturation-temperature-failure?` yes → 把颗粒质量倾倒进连续相。
  - **后处理**（9.17.3.5.4）：密度/焓/熵/声速/比热及派生量；另可报压缩因子、对比温度/压力、spinodal 温度、亚临界条件；混合物可报组分依赖的混合临界 T/P/v 与偏心因子。
- **NIST 真实气体模型**（9.17.4）：REFPROP v10.0 数据库，约 **152 种流体**（.FLD 纯流体 + .PPF 伪流体，Table 9.3 全列：Air(dry)、R 系制冷剂、CO2、水、氮、氦、烃类、硅氧烷 D4/D5/D6 等）；共享库动态加载；激活后物性评估权交 REFPROP。EOS：MBWR / Helmholtz 能量 / ECS 三类；混合物用 Helmholtz 混合规则。**限制**：仅过热蒸气/超临界/液体（**不支持亚临界两相**）；**全部流体区必须是该真实气体**（不能真实气体+其他流体混用）；边界仅 pressure-inlet/mass-flow-inlet/pressure-outlet；密度基 NRBC 不兼容；混合物流**不允许化学反应**；多组分 NIST 不能配任何多相模型（单组分多相可以；DPM 仅 massless/inert 颗粒）；不能改 REFPROP 或加自定义材料；**一个仿真只能有一种 NIST 纯流体或一种混合物（第三方限制）**。**带 \* 的流体（NF3、Orthohydrogen、R404A、R407C、R410A、R507A）无输运性质模型 → 只能算无黏流**。
  - **用法**：纯流体 Density 选 real-gas-nist → Edit → NIST Fluid Data 对话框选流体（显示适用 P/T 范围）；混合物先开 Species Transport → Density 选 real-gas-nist-mixture → 逐 species 选 NIST 数据。**Important：并非所有组分组合都允许（缺二元对数据 → NIST 报错、不能建材料；混合数据为估算 → 警告但允许）；水摩尔浓度 >5% 的混合物不支持输运性质计算（告警）；氨/水混合物与含醇混合物无输运方程 → 只能无黏流**。Cp/导热/黏度自动设为 real-gas-nist(-mixture)。无表时要液态：Operating Conditions 设 Real Gas State = liquid；逐 zone 用 change-zone-state。
  - **NIST 查找表**（9.17.4.3.1）：默认每次物性更新直接调 NIST 函数；查找表省时。指定 **P/T 边界（严格在加载时显示的适用范围内）与 P/T 点数（最少 12、无上限——表越大内存/耗时越高，试跑平衡）**；单组分另给饱和（泡/露点）点数；多组分给质量/摩尔组成（**和须为 1；最多 20 species**）。越界自动回落原 NIST 函数；**表外计算 >10% 时打印百分比**（提示调整范围）。**限制**：泡/露点有 UDF 宏；表适用于物性 = f(局部 P, T) 的可压流体、含液气两相物性；闪蒸用饱和条件 + 质量传递模型；**表按固定组成创建——组成恒定、无反应、无不同组成流体混合（含相间）**；仅单相流；结构化表在临界点附近高分辨率需求下可能不适用。**多组分全表（TUI 9.17.4.4.3）不随 case 保存——重启 Fluent 需重建**；泡/露点写 Bubble_PT.xy/Dew_PT.xy。二元混合物饱和表（9.17.4.4.4）：Full? no → Binary Mixture Only? yes；质量分数点数与每条饱和曲线点数（默认 12；实际可能少）；摩尔密度上下限（默认 0.1/25 mol/l）；允许的组合由安装目录 **hmx.bnc** 决定；文件结构 = 质量分数行 + 点数行 + P-T 对（最后一对为临界条件，示例 0.0 → 4.8722e6 Pa/305.322 K）。
  - **求解策略**（9.17.4.5）：收敛远慢于理想气体；密度基用低得多的 Courant、压力基用低得多的欠松弛；先一阶后二阶。**NIST 物性定义在有界范围内——工况必须落在数据库范围内**；越界即发散或报错；过渡性越界可降 Courant/欠松弛避免。初始化时物性程序报错 = 工况超出数据库范围。写 case：共享库链接 + 材料物性数据随 case 保存；`/define/materials/list-properties <material-name>` 可查。后处理：密度/焓/熵/分子量/分子黏度/声速/比热/导热 + 压缩因子及派生量。
- **UDRGM 用户自定义真实气体**（9.17.5）：C 语言函数库自定义真实气体；支持单组分/多组分/多相/体积反应。**限制**：一个问题只能有一种用户自定义真实气体材料（可与其他材料共存）；材料以 real-gas-fluid / real-gas-mixture 出现且物性输入禁用（仍可设：混合物质量扩散率、化学反应、辐射属性、其他材料属性）；**Note：UDRGM 与 Fluent 库材料在 DPM/多相联用时 UDF 参考温度须与 Fluent 一致 = 298.15 K**；边界仅 pressure-inlet/mass-flow-inlet/pressure-outlet；密度基 NRBC 不兼容；Eulerian 多相可用；DPM 可用（按 9.17.3.5.3 指南）；不兼容非预混/部分预混/组分 PDF 输运燃烧（有限速率+涡耗散可以；Dimension Reduction 不可用）；**无壁面表面反应（不支持 site/solid species）**。
  - **代码要求**（9.17.5.2）：含 udf.h；至少一个 DEFINE 宏（如 DEFINE_ON_DEMAND）以便用编译 UDF 工具；**一律 SI**；主函数集：`ANYNAME_Setup(domain, vapor_phase, species_list, messagefunc, errorfunc)`、`ANYNAME_density(cell, thread, vapor_phase, T, P, yi[])`、specific_heat/enthalpy/entropy/mw/speed_of_sound/viscosity/thermal_conductivity/rho_t/rho_p/enthalpy_t/enthalpy_p、多组分反应加 `ANYNAME_enthalpy_prime`（输出逐 species 焓数组 hi[]；= 显焓+生成焓，须与 enthalpy 一致；无反应可省）。**Important：density 每迭代被调用多次——务必高效；函数实参优先于 cell/thread 解数组；单组分 yi[]=1.0**。结尾必须按固定顺序定义 `RGAS_Functions RealGasFunctionList` 结构（Setup → density → enthalpy → entropy → specific_heat → mw → speed_of_sound → viscosity → thermal_conductivity → rho_t → rho_p → enthalpy_t → enthalhy_p → enthalhy_prime）——**顺序错则加载失败**。
  - **编译/加载**：C 代码放 case 文件夹 → Fluent 读 case → define/user-defined/compiled-functions → compile（库名、C 源文件、头文件）→ 库落架构目录（libudf.so/.dll）；加载：define/user-defined/real-gas-models → user-defined-real-gas-model 或 user-defined-multispecies-real-gas-model → yes → 给库路径；成功打印 Opening user-defined realgas library...
  - **体积反应**（9.17.5.1 步骤 6）：Species Model → Species Transport + Volumetric + 选 TCI → 对 real-gas-mixture 编辑反应（同常规）；**反应须在 UDF 编译加载后开启；先跑冷流验证 UDF；UDF 适用范围须覆盖反应流的 T/P 范围**。
  - **示例**（9.17.5.4）：理想气体 EOS 完整代码清单（IDEAL_* 函数：ρ=p/(R T/M)、cp=1006.43、h=T·cp、s=cp·ln(T/288.15)+R·ln(101325/P)、声速 √(T·cp·R/(cp−R))、μ=1.7894e-05、k=0.0242、ρ_t=−ρ/T、ρ_p=1/(R T)、dh/dp=0）；Customization Manual 另有 Aungier-RK 单组分、多组分、含体积反应三例。
- **RGP 表文件**（9.17.6）：热物性+输运物性按 f(T, P) 二维表；等效于立方 EOS/NIST 的真实流体；**物性计算在预处理完成、求解时查表——计算高效**；亚临界可含液/汽或两者数据。**用法**：① 读入 RGP 表（p. 989；按 access key 自动生成各材料数据集，出现在 Table File Manager）；② Table Settings → **Create/update RGP material**（自动建/更同名材料并对可用属性自动设 rgp-table）或常规建材料；③ 可选 **Store in case file**（把 RGP 数据嵌进 case——便于共享但文件变大）；④ Density 下拉选 **rgp-table** → Edit 选表；**Cp/导热/黏度自动设为 rgp-table**。**饱和属性**（9.17.6.3）：可用 RGP 表给的饱和属性——空化模型蒸气压、蒸发-冷凝/沸腾模型饱和温度、Raoult 律饱和压力、相间作用表面张力系数（饱和温度依赖）、DPM 液滴蒸发饱和蒸气压——模型对话框相应下拉选 **rgp-table-sat** → 选饱和表。**连续性瞬态项线性化**（9.17.6.4）：瞬态真实气体表在密度变化极小时连续性瞬态算子出现舍入误差——线性化可改善收敛与精度；`solve/set/advanced/continuity-transient-term-linearization/linearize?` yes（单相/VOF/mixture、瞬态压力基）；阈值 `.../threshold`（默认相对密度阈值 [1]）。
- p. 1798 为空白版权页，无正文。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.9；本页覆盖批次 47（pp. 1651–1699，9.1–9.4）、批次 48（pp. 1700–1734，9.5–9.10）与批次 49（pp. 1735–1797，9.11–9.17），均为 2026-10-17 读取。**Ch.9 全章完成**（p. 1798 为空白版权页）。
- **公式体未提取**：Eq 9.1–9.114 的公式体均为图形对象、文本提取缺失；已按公式周边文字与变量定义记录结构与式号（Sutherland/幂律/非牛顿模型/NIST EOS 的标准形式按文字描述与系数值对应给出；Tait、动能理论、立方 EOS 系数、偏离函数、RGP 等仅记语义与式号）。需要精确公式时须回看 PDF 对应页（pp. 1670–1793）。
- 原文数值照录：空气物性、compressible-liquid 默认（7.15/1.1/0.9）、湍流 Schmidt 0.7、Table 9.1 操作压力建议、Table 9.2 液滴温度限 13 种材料、Table 9.3 NIST 152 流体清单、general NRBC σ=0.15/σ2=5.0、UDRGM fantest 式常数（288.15 K/101325 Pa/1006.43/1.7894e-05/0.0242）等。UDRGM ideal-gas 代码清单照录。坐标轴符号按 7.2.1 约定补全；Figures 9.1–9.52 为图形元素未摄取。
- 后续章节引用（Mixture Materials p. 2453、DPM 材料 p. 2919、Solution Limits p. 3759、RGP 表读取 p. 989、Gupta p. 2397、Equation Order p. 3738、各向异性固体区设置 p. 2237、Expressions p. 1077、浮动操作压力 p. 1825、多相操作密度 p. 3042、Sponge Layers p. 2767）仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent Cell Zone 与边界条件设置]]（8.3 操作压力/浮力与 9.15/9.3 互为引用）
- [[Fluent 表达式语言]]（表达式可替代部分属性函数）
- [[index]]
