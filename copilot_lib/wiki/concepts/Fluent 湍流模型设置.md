---
type: concept
created: 2026-10-18
updated: 2026-10-18
tags:
  - Ansys Fluent
  - turbulence
  - RANS
  - SRS
  - LES
  - transition
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 湍流模型设置

## 摘要

User's Guide 2026 R1 Part III / Chapter 16 "Modeling Turbulence"（PDF pp. 2125–2220，共 20 节）讲湍流模型使用。**本页全章完成（批次 60–61，pp. 2125–2220，覆盖 16.1–16.20）**：引言与模型清单、RANS/SRS 选型指南（GEKO 四系数、转捩四模型、SRS 网格与数值设置、模型层级）、使用步骤、SA/k-ε/k-ω（GEKO/WJ-BSL-EARSM）/转捩/RSM/SAS/DES/LES/ELES 设置、模型常数、26 项通用设置选项、湍流边界条件、初值估算、求解策略与后处理变量清单。

## 16.1 引言与模型清单（pp. 2125–2128）

- 湍流 = 中高雷诺数流体的三维非定常随机运动；工程关注量（动量/能量/组分混合、换热、压损与效率、气动力）都依赖湍流。DNS 不可行 → 对 N-S 方程平均得 **RANS**（引入雷诺应力/通量需湍流封闭模型）；**模型选择与配套网格决定解质量**。替代路线 **SRS（Scale-Resolving Simulation）**——至少在部分域解析部分湍流谱（LES 最著名、大量混合模型涌现）；SRS 须时间精确解、时间步小 → **比 RANS 昂贵得多**。
- **模型清单**：Spalart-Allmaras；k-ε（Standard/RNG/Realizable）；k-ω（Standard/BSL/**SST（默认启用）**/GEKO）；k-ω 附加模型（WJ-BSL-EARSM）；Transition k-kl-ω；Transition SST；RSM（Linear pressure-strain / Quadratic pressure-strain / Stress-Omega / Stress-BSL）；**SAS**（配 SST k-ω / Standard k-ω / BSL k-ω / Transition SST / k-ω 基 RSM）；**DES**（SA / Realizable k-ε / SST / BSL / Transition SST）；**SDES**（SST / BSL / Transition SST）；**SBES**（SST / BSL / Transition SST）；**LES**（Smagorinsky-Lilly 可带 dynamic stress / WALE / Dynamic kinetic energy / WMLES 及其 ω 基变体——变体名公式符号未提取，以界面为准）。

## 16.2 湍流模型选型（pp. 2128–2145）

- **没有普适最优模型**——按物理、同类问题惯例、精度要求、算力与时间权衡。**默认 k-ω SST**；可在 Preferences → Simulation → Flow Model 改默认模型（加载网格/切入求解模式时生效；不影响已有 case）。
- **RANS**（16.2.1）：工业复杂湍流最经济——两方程 + 涡黏假设；RSM 直接解 6 个雷诺应力分量 + 尺度方程。
  - **Spalart-Allmaras**（16.2.1.1）：单方程解运动涡黏性输运；**为航空宇航壁面约束流动设计**；逆压梯度边界层效果好；叶轮机械应用渐多；**勿作通用模型——自由剪切流（射流）标定差、误差大**。已扩展 **y⁺ 不敏感壁面处理**（按 y⁺ 从黏性底层到对数律自动混合，含缓冲层标定）。
  - **k-ε**（16.2.1.2）：历史上工业 CFD 最常用（standard k-ε，Launder-Spalding [86]，稳健/经济/合理精度）。**缺点：对逆压梯度与边界层分离不敏感——分离偏迟偏弱 → 光滑面分离流动（翼型、扩压器）设计评估过于乐观；外流空气动力学少用**。**Fluent 推荐 Realizable k-ε 优于其他变体，并配 Enhanced Wall Treatment（EWT-ε）或 Menter-Lechner（ML-ε）近壁处理**；光滑面逆压分离工况一般不推荐 k-ε。
  - **k-ω**（16.2.1.3）：ω 方程可无附加项穿过黏性底层积分 → 稳健的 y⁺ 不敏感处理容易实现；逆压边界层与分离预测更好。**Standard k-ω 对自由来流值敏感 → 一般不推荐**；**BSL 与 SST 结合 ε/ω 方程要素消除来流敏感性；SST 经标定可准确算光滑面分离——k-ω 家族推荐 BSL 或 SST**；空气动力学最常用模型之一，壁面边界层细节通常比 SA 更准；全部用 y⁺ 不敏感壁面处理。**SST 自 2020 R1 起为默认：涡黏性低（对比 k-ε）→ 分离等物理现象更准，但部分工况稳定性略差、求解器设置可能需调整以保证收敛**。Wilcox low-Re 项为可选：非底层积分所必需、主要功能是模拟转捩但标定不足——壁面转捩用 SST + Transition SST / Intermittency / Transition k-kl-ω 更可靠，**不建议用 low-Re 项**。
  - **GEKO**（16.2.1.4，Generalized k-ω）：一个模型覆盖宽应用面——四个自由系数可按应用调整而不破坏基础标定；**默认值强，可不调参直接用；调参须有高质量实验数据支撑**。两版本：**GEKO_2015（原始）与 GEKO_2024（改进、默认）——2024 消除了 2015 版自由系数间的相互依赖**。多数情况只需调 **Csep**（边界层分离敏感性，对多数应用影响最大）：Csep = 0 时模型几乎同 SST（不分离）；扩压器算例 Csep = 1.75 与数据近乎完美吻合（同 SST [101]）；高升力翼型（SST 也低估分离强度）可更大。**Cmix**（自由剪切掺混）：增大 → 湍流度与扩展率增大。**Cnw**（近壁；后台阶再附着区）：强烈影响壁面剪切系数与 Stanton 数——增大使非平衡区两者升高；**多数情况保持默认**。**Cjet**（射流）：Cm = 0 时模型高估平面/圆射流扩展率（圆射流尤甚，似 standard k-ε）；**Cjet = 1.0 接近两组实验**；默认多够用；**Cjet 影响所有自由剪切流**。Cjet 作用区由混合函数界定——混合函数 = 1（近壁）区改 Cjet 无效果；混合函数可后处理显示、可经 expert 参数修改或 UDF 覆写（DEFINE_KW_GEKO）。GEKO 用 y⁺ 不敏感壁面处理。
  - **RSM**（16.2.1.5）：能捕捉涡黏模型难以处理的效应——**最重要的是强旋转与流线曲率引起的湍流稳定化（如旋风分离器）**；但计算时间显著增加（附加方程 + 收敛变慢），收益不一定抵成本 → **仅限已证明优越的场景，尤其强旋流与旋转**；壁面边界层重要时 **RSM + ω 或 BSL 方程比 RSM + ε 更准**（RSM+BSL 同时消除来流敏感性）。**EARSM（代数雷诺应力模型）是两方程模型的扩展——捕捉附加效应与计算成本的折中**。
  - **转捩模型**（16.2.1.6）：四个——**Transition SST（γ-Reθ，可配 SAS/DES/SBES/SDES）；Intermittency Transition（γ，可配 BSL/SST/GEKO 及其 SAS/DES/SBES/SDES）；Algebraic Intermittency（Alg-γ，同 γ 的可用范围）；Transition k-kl-ω**。多数测试例结果相近；**前三者（配 SST）优于 Transition k-kl-ω**。**Transition SST 非伽利略不变——不适用于相对坐标系运动的表面，也不适用于无自由来流的充分发展管/槽流（改用 γ 或 Alg-γ；γ 用于管/槽流可能需改底层关联式）**；**只有 Intermittency Transition 能计入横流不稳定性**。前三者同属 LCTM（局部关联转捩模型）。**方程数：Transition SST 加解 2 个输运方程、γ 加解 1 个、Alg-γ 不加**（省计算是后两者的开发动机）。Transition SST 最常用（航空领域近十年的标准 RANS 转捩模型）；γ 因公式更简单且伽利略不变渐获认可；Alg-γ 最新、较新、在"转捩由几何特征/层流气泡定义"的工业场景见长、亦伽利略不变——**建议三个都跑、比较成本/精度比**。Transition k-kl-ω 不再积极开发、只配 standard k-ε → 不建议作默认。**注意**：仅适用于壁面约束流（自由剪切流转捩不适用、会判为全湍流）；未对浮力、多相湍流等影响源项的物理做标定；与尺度解析方法组合也无专门标定（混合模型自由来流 LES 项激活会影响来流湍流衰减进而影响转捩位置）；**粗糙壁建议用 Transition SST（γ-Reθ）**；**网格精细度与进口湍流度设定对转捩预测至关重要**；**不推荐 tet/prism 网格**；需低 Re 网格（y⁺~1）+ 足够流向分辨率；**壁法向膨胀因子 < 1.15**（网格要求节又给出 ≤ 1.1）；层流分离区需额外加密；**跑解前先估算进口→前缘的湍流衰减**（转捩位置对边界层外湍流度高度敏感）。
  - **曲率修正**（16.2.1.7）：涡黏模型对流向曲率与系统旋转不敏感——可用修正的湍流生成项（SA 与两方程模型，Theory Guide）。
  - **角隅流动修正**（16.2.1.8）：涡黏模型倾向高估角隅分离——基于 ω 输运方程的简化二次非线性代数扩展，把动量驱入角隅（SA 与两方程）。
  - **生成项限制器**（16.2.1.9）：两方程模型在驻点附近 k 生成过量——可用两种公式之一限制生成项。
  - **模型增强项慎用**（16.2.1.10）：**Sarkar 可压缩效应**改善高 Mach 自由剪切层、但对壁面边界层有明显负面影响——**默认关闭（14.5 及更早版本非如此），非自由剪切工况建议保持关闭**（可压理想气体/真实气体启用时在 Viscous Model 对话框出现该选项）；**浮力**：受浮力影响的流动建议开启 **k 方程源项**（ε 方程源项认可度低、ω 方程源项慎用）。
  - **RANS 壁面处理**（16.2.1.11）：**所有可用的模型（SA、ε、ω）都推荐 y⁺ 不敏感壁面处理**——壁面剪切与换热预测最一致、对 y⁺ 最不敏感。**壁面函数：须避免近壁过细网格（全域建议 y⁺ 约 30 以上）；一般不推荐壁面函数（无法系统加密近壁网格）；低中雷诺数（Re~10⁴ 量级，符号未提取）扩展对数律假设失效、尤其有害——需要壁面函数时用 Scalable Wall Functions 解除网格限制**。
  - **RANS 网格分辨率**（16.2.1.12）：**相关剪切层法向至少 ~10 个单元**（自由剪切层位置未知时难保证，但分辨率不足模型性能退化）。**壁面流动：法向结构化网格覆盖整个边界层并延伸到层外**；**SA/SST 要发挥优势至少 10 层以上结构化（六面体/棱柱）单元在边界层内；棱柱层必须完全覆盖壁面边界层**。y⁺ 不敏感处理对壁面单元 y⁺ 相对不敏感——**边界层内单元覆盖充分比凑特定 y⁺ 更重要**；对壁面边界层高精度要求（尤其换热）→ y⁺ ~1；**壁面函数工况 y⁺ 低于 ~30 时壁面剪切/换热会严重恶化**。
- **SRS 模型**（16.2.2）：
  - **LES**（16.2.2.1）：全域解析到网格极限；学术界广泛、工业影响有限——**近壁分辨率要求过高**（壁面附近最大涡几何尺寸很小、须极细网格 + 小时间步 + 壁面平行面内也要解析；仅限很低 Re 或极小尺度，LES 域延展 ≤ 10–100 倍边界层厚度）。**LES 只推荐用于壁面边界层不相关或层流（低 Re）的流动；最均衡的 LES 模型是 WALE**（复杂度与通用性折中、可无模型影响地算层流剪切层）。**WMLES**：高 Re 壁面约束流 LES 而无须常规 LES 的网格量——每边界层体积所需网格数与 Re 基本无关；**增强版 WMLES（ω 基）**克服原 WMLES 的两缺点（常剪切流涡黏不为零 → 无法算转捩效应；分离剪切层涡黏过大）。
  - **混合 RANS-LES**（16.2.2.2）：附着壁面边界层由 RANS 覆盖、大分离区以"LES 模式"部分解析；**依赖足够强的流动不稳定性**在分离区生成湍流结构（钝体绕流典型：URANS 单模态周期涡脱 → 混合模型允许大结构破碎到网格极限——图 16.5 圆柱绕流 SST-URANS vs SST-SAS，Q 判据等值面按涡黏比着色、右图色标小 14 倍）。
    - **SAS**（16.2.2.2.1，Menter 等 [102][103]）：把 **von Karman 长度尺度 L_vk 引入湍流方程**（BSL/SST 进入 ω 方程）——**Eq 16.1：L_vk = κ·|U′|/|U″|（κ = 0.41，速度矢量一阶/二阶导数之比）**（公式体未提取，语义自正文）。使模型把长度尺度调整到已解析尺度 → 涡黏低到可进"LES 模式"。**优点：RANS 部分不受网格间距影响——不会像 DES 那样在"网格加密但不稳定性不足"区劣化；缺点：不稳定性不够强时停留在 RANS 模式、不产生非定常结构**（需要非定常信息如声学时是局限）→ 可用 ELES 内部界面把模拟湍流转化为解析湍流。
    - **DES**（16.2.2.2.2）：比较湍流长度尺度与网格间距 Δ、取最小者切换 RANS/LES——**Eq 16.2**（ω 方程中长度尺度替换为 min 形式，公式体未提取）。**Δ 显式进入模型**：在"灰区"（网格介于 RANS 与 LES 分辨率之间）和/或不稳定性不足区影响 RANS 解。**GIS（网格诱导分离）**：附着边界层网格加密到 DES 限制器激活并影响 RANS、而不稳定性不足以补足 → 网格加密处出现人为分离（发生在 Δ 相对边界层厚度 δ 过小时，具体比值符号未提取）。对策：Menter 用 SST-DES 的 F1 混合函数屏蔽边界层；Spalart 等 [157] 提出 DDES；**DDES 已针对 BSL/SST/k-ε 重标定——现为这些模型的推荐与默认设置**。**IDDES**（Strelets [145]）把 LES 区扩展到边界层外层 → 可按 **WMLES 模式**运行（当 LES 用、配非定常进口条件；网格要求远低于 LES）。全部屏蔽函数变体可用：SA 用原始 DDES；k-ε/BSL/SST 用重标定 DDES（默认、优于 F1/F2）。**IDDES 的 WMLES 模式为高级选项——须熟悉原始文献与网格要求**。**DES 与 DDES 已被 SDES、SBES 取代**。
    - **SDES/SBES**（16.2.2.2.3）：屏蔽函数优于 DDES/IDDES——RANS 边界层屏蔽更强、分离剪切层 RANS→LES 过渡更快、SBES 还可显式选择 LES 模型。设置见 p. 2198。**推荐取代旧 DES/DDES；SBES 被视为最优选择（RANS/LES 区分最清晰）**。
  - **分区建模与 ELES**（16.2.2.3）：混合模型依赖不稳定性、不稳定时不可靠 → **在预定义区分别用 RANS/LES 并给出明确界面**：上游 RANS 的模拟湍动能在内界面显式转化为 LES 区的解析尺度；LES 区可限于感兴趣区。ELES 可组合多数 RANS 模型与经典 LES；**LES 区内必须满足完整 LES 分辨率；LES 区推荐 WALE**。
- **SRS 网格分辨率**（16.2.3）：**壁面边界层**：RANS 模式要求同 RANS；**壁面解析 LES** 建议间距按壁面单位在 x/y/z 方向同量级缩放（公式符号未提取；复杂应用分不清流向/展向时要求更严）——体现 LES 对 Re 的强依赖。**WMLES 模式（仅 IDDES 与 SBES 可靠）**：间距按边界层厚度 δ 缩放（推荐比例符号未提取）；**壁法向分辨率按精细 RANS——y⁺ ~1 且边界层内约 30 个节点**。**octree 网格在边界层内三向接近均匀 → 适合 WFLES（壁面函数 LES）；边界层体积内最低 5×5×5 单元**。**自由剪切流**：目标均匀各向同性单元（三向边长接近）；剪切层覆盖 ~10–20 单元。
- **SRS 数值设置**（16.2.4）：SRS 在网格分辨率极限运行、最小尺度与网格/时间分辨率同阶——数值设置须在精度与稳健间最优平衡；以下为基于不可压单相无反应流的起点建议（复杂物理 → 方程耦合更费力：更小时间步、更低欠松弛、更多迭代、更严残差）。**从（基本）收敛的 RANS 解初始化**。
  - **时间离散**（16.2.4.1）：时间步保证 **主 SRS 区 CFL ≈ 1（Eq 16.3，公式体未提取）**；CFL 由求解器计算、可先用初始 RANS 检查；**非数值限制**（求解器能承受更大）；不要因个别细单元/高速区限制 CFL；配均匀各向同性网格按主 SRS 区 CFL=1 选时间步；**按应用类型试不同时间步找最优——可大幅省算力**。时间导数用**二阶隐式**。
  - **空间离散**（16.2.4.2）：**最小化数值耗散**以免数值耗散抹掉最小尺度。压力基可选 **CD（中心差分，最少耗散、最小尺度分辨率最高——声学高频谱重要时理想；但速度场易棋盘振荡 → 须高质量网格（无网格跳跃、各向同性、关键区高分辨率）+ 主 SRS 区 CFL < 1 + 定期目视监视；振荡时改善网格/减时间步/换 BCD）与 BCD（有界中心差分——复杂应用的首选：耗散足够低让结构演化、又稳健到能处理工业非最优网格；适用于 SAS/DES/SDES/SBES 并在 RANS 区、高拉伸网格、CFL > 1 下稳定）**；密度基仅 BCD（配 Roe-FDS 或 AUSM 通量）。**ELES 的 LES 区格式可独立于 RANS 区选**（RANS 区标准高阶迎风、LES 区 CD 或 BCD）。梯度：**Least Squares Cell Based 或 Green-Gauss Node Based**（非正交网格二阶插值）。压力插值：**二阶或 body-force-weighted；PRESTO! 不推荐用于 SRS**（耗散高 → 结构延迟形成或被阻尼）。
  - **迭代格式**（16.2.4.3）：**NITA 最快**——适合有限 LES 区 + 高质量网格 + CFL < 1 时间步；显式欠松弛默认全 1；无复杂物理用 fractional step 法、否则 PISO 更优；LES 可开 accelerated time marching（改进 NITA）进一步提速。**NITA 不适用 → SIMPLEC 或 PISO（优于 SIMPLE：每步收敛更快、欠松弛可更激进 ≈ 1）**；不收敛 → 检查 SRS 区 CFL < 1、必要时减时间步；仍不行 → 欠松弛降到默认值与 1 之间；**偏斜/质量问题网格：压力校正显式松弛 1 → 0.7 非常有效**。
    - **收敛控制**：每时间步收敛判据影响成本；**最相关的残差是连续性——CFL ~1 时每步约降 2 个量级；无附加物理时每步 5–10 次最大迭代可达**；须核查残差水平对解的影响。**小 CFL 时 Run Calculation 的 Extrapolate Variables 选项可把每步迭代数减最多 40%**。燃烧/多相等附加物理 → 可能需降欠松弛、增最大迭代。**混合 RANS/LES 中 RANS 部分限制收敛（如网格质量差）→ 考虑耦合求解器**（单次迭代比 SIMPLEC 贵但收敛快补偿；残差建议同 SIMPLEC；高度非定常流最大迭代可低至 2–5、较温和流动与声学 5–10）。
- **模型层级**（16.2.5）：**尽量用 RANS（默认 k-ω SST）**——多年内仍是主力；RANS 内涡黏模型满足多数工程；RSM 仅用于已证明有系统收益的流动。**定常 RANS/URANS 精度或非定常信息不足 → SAS**（对网格宽容、分辨率不足不劣化；只在强不稳定性存在时给尺度解析；**用 Q 判据等值面目视判断是否够非定常；不足时用 ELES 内部界面转换**）。**DDES（DES 不推荐）**可在 SAS 保持稳定时也产生非定常；LES 区网格需更精心（DES 网格影响 RANS 解）；DES-BSL/SST 用默认 DDES 混合函数屏蔽。**SDES/SBES 屏蔽更强、RANS→LES 过渡更快；SBES + WALE 组合推荐取代 DES/DDES/IDDES**。**ELES** 适合大 RANS 区内嵌高精度小区；RANS/LES 界面上用 **Vortex Method 或 Spectral Synthesizer** 生成非定常湍流；壁面约束流 ELES 的 LES 区须极细近壁分辨率。**纯 LES 只用于自由剪切流（如无壁影响的燃烧室）或极小域 + 精细 LES 近壁网格；壁面高 Re → IDDES 的 WMLES 模式（配指定非定常进口）**。

## 16.3 使用步骤（pp. 2145–2148）

默认 k-ω SST。① **Viscous Model 对话框**（Setup → Models → Viscous → Edit）选模型：Model 列表 = Spalart-Allmaras / k-epsilon / k-omega / Transition k-kl-omega / Transition SST / Reynolds Stress / SAS / DES / LES；k-epsilon 子选 Standard/RNG/Realizable；k-omega 子选 Standard/GEKO/BSL/SST。**Important：LES 仅 3D。**有壁且用 k-ε 或 ω 基 RSM → Near-Wall Treatment 选：Standard Wall Functions / Scalable Wall Functions / Non-Equilibrium Wall Functions / Enhanced Wall Treatment / Menter-Lechner（仅 ε 系）/ User-Defined Wall Functions（UDF 挂 Law of the Wall 下拉）；**默认 standard wall function**。SA 与 ω 基模型自动定义近壁处理。**LES 近壁处理三选：Kader blending Wall Functions（当前默认）/ Harmonic blending Wall Functions based on r⁺（推荐）/ Werner-Wengle Wall Treatment**。②按需启用其他湍流选项（16.16，p. 2186）。③在边界条件对话框给湍流求解变量边界条件（p. 2201）。④Solution Initialization 给初值（p. 2205）；**雷诺应力自动由 k 初始化、无须显式初始化**。

## 16.4 Spalart-Allmaras 设置（pp. 2148–2149）

选项：**vorticity-based production / strain-vorticity-based production**（二选一，p. 2193）；**viscous work**（密度基恒启用）；**curvature correction**（p. 2189）。图 16.7。

## 16.5 k-ε 设置（pp. 2149–2153）

- **Standard/Realizable k-ε** 选项：viscous work（密度基恒启用）；**浮力对 k 的影响**；curvature correction；compressibility effects；production limiters。近壁处理六选同 16.3（standard/scalable/non-equilibrium 壁面函数、enhanced wall treatment、Menter-Lechner、user-defined）；EWT 附加选项：**pressure gradient effects 与 thermal effects**（p. 2195）。
- **RNG k-ε** 额外选项：**differential viscosity model**（p. 2193）与 **swirl modification**（p. 2194）；其余同 Standard/Realizable（viscous work、浮力、曲率修正、可压缩效应、生成限制器、六种近壁处理）。

## 16.6 k-ω 设置（pp. 2153–2162）

- **Standard k-ω** 选项：low-Re corrections；shear flow corrections；**turbulence damping**（VOF/Mixture 及 Multi-Fluid VOF 的 Eulerian 多相可用）；近壁处理；viscous work；curvature correction；compressibility effects；production limiters；**SAS 选项**。
- **GEKO**（16.6.2）：k-omega (2 eqn) + GEKO 启用（TUI `/define/models/viscous/kw-geko?`）。选项：turbulence damping；近壁处理；viscous work；curvature correction；**corner flow correction**；compressibility effects；production limiters；**Intermittency Transition**；SRS 四选（SAS / DES / SBES / SDES）。**与 RSM 组合：先选基于 BSL ω 方程的 Stress-BSL RSM，再启用 GEKO 选项**（TUI `/define/models/viscous/rsm-or-earsm-geko-option?`）。**多数情况只调 Csep（分离，影响最大）与 Cmix（自由剪切掺混）**；两系数均可通过表达式或 UDF 给出（可分区不同）；其余参数一般保持默认。**默认 Full model 提供全部系数与混合函数（GEKO Options 组框；图 16.11）；wall-distance free 模型仅可用部分系数**。geko-options 子菜单：wall-distance-free?、version、**csep、cnw、cmix、cjet**、blending-function；**默认版本 2024**；辅助系数 TUI：creal、cnw_sub、cjet_aux、cbf_lam、cbf_tur；恢复默认：geko-defaults。
- **BSL k-ω** 选项：low-Re corrections；turbulence damping；近壁处理；viscous work；curvature correction；compressibility effects；production limiters；Intermittency Transition；SRS 四选（SAS/DES/SBES/SDES）。
- **SST k-ω** 选项：low-Re corrections；turbulence damping；近壁处理；viscous work；curvature correction；compressibility effects；production limiters；Intermittency Transition；**SRS 仅 SBES 或 SDES**。
- **WJ-BSL-EARSM**（16.6.5）：选 k-omega 后在 k-omega Model 列表出现；选项：近壁处理；viscous work；production limiters；**经 Options 勾 GEKO 可组合 GEKO**。**仅 3D；不支持 gap model**。为 BSL 的扩展——捕捉**雷诺应力各向异性与二次流**。

## 16.7–16.9 转捩模型设置（pp. 2162–2166）

- **Transition k-kl-ω**（16.7）选项：近壁处理；viscous work。图 16.15。
- **Transition SST（γ-Reθ）**（16.8）选项：**roughness correlation（粗糙壁关联，Theory Guide）**；近壁处理；viscous work；curvature correction；production limiters；SRS 四选（SAS/DES/SBES/SDES）。**转捩关联可经 UDF 定制：F_length（转捩长度函数）、Re_thetac（临界动量厚度雷诺数）、Re_thetat（转捩起始动量厚度雷诺数）——DEFINE_TRANS 系列（Customization Manual）**。图 16.16。
- **Algebraic / Intermittency Transition（Alg-γ / γ）**（16.9）：作为 **Transition Options 组框中的 Transition Model** 挂到：BSL k-ω、SST k-ω、GEKO k-ω、SAS（BSL/SST）、DES（BSL/SST）、SDES（BSL/SST）、SBES（BSL/SST）。**默认无转捩模型**；选项（接批次 61，p. 2167 起）。图 16.17。

- **Algebraic / Intermittency Transition（Alg-γ / γ）**（16.9）：作为 **Transition Options 组框中的 Transition Model** 挂到：BSL k-ω、SST k-ω、GEKO k-ω、SAS（BSL/SST）、DES（BSL/SST）、SDES（BSL/SST）、SBES（BSL/SST）。**默认无转捩模型**；两个转捩选项：**γ-algebraic 模型（Alg-γ）——可自定义 Critical Reynolds Number Correlation 取代内置配方；γ-transport-eqn 模型（Intermittency Transition）——可勾 Include Crossflow Transition 计入横流不稳定性**。与代数/输运转捩模型组合时使用底层湍流模型的 y⁺ 不敏感壁面处理。

## 16.10–16.15 RSM、SAS、DES、LES、ELES 设置（pp. 2167–2186）

- **RSM**（16.10）：子模型两组——**ε 基 RSM**（linear pressure-strain / quadratic pressure-strain）与 **ω 基 RSM**（Stress-Omega / Stress-BSL）。ε 基专属：雷诺应力墙边界条件取自 k 方程（16.16.17；线性和二次压力-应变模型）；**壁面反射效应**（16.16.16，仅 linear pressure-strain）；近壁处理：standard/scalable/non-equilibrium 壁面函数、**enhanced wall treatment（仅 linear pressure-strain）**（EWT 附加 pressure gradient/thermal effects）。**Stress-Omega 与 Stress-BSL 用 y⁺ 不敏感壁面处理，推荐低 Re（LRN）网格**；Stress-Omega 可选 low-Re corrections 与 shear flow corrections；Stress-BSL 可与 GEKO 组合；两者均可配 SAS。两族通用选项：viscous work（密度基恒启用）、compressibility effects、浮力对 k 的影响。**Note：ε 基 RSM 与 Eulerian 多相模型不兼容**。
- **SAS**（16.11）：SST k-ω 时直接在 Model 列表选 Scale-Adaptive Simulation (SAS)；也可与 Standard k-ω、BSL k-ω、GEKO、Transition SST、WJ-BSL-EARSM、ω 基 RSM 组合——选模型后在 **Scale-Resolving Simulation Options 组框**勾 SAS。**动量离散推荐 BCD（默认）**；用底层模型的 y⁺ 不敏感壁面处理。
- **DES**（16.12）：底层 RANS 五选：SA、Realizable k-ε、SST k-ω、BSL k-ω、Transition SST；动量离散推荐 BCD（默认）。
  - **DES-SA**：DES + Spalart-Allmaras（RANS Model 列表）；长度尺度按 Theory Guide Eq 4.290；**Cdes 默认 0.65**（Model Constants 的 Cdes 字段可改）；选项：vorticity/strain-vorticity 生成、delayed DES、viscous work、曲率修正。DES 专属 TUI `/define/models/viscous/detached-eddy-simulation?`：**只修改 ν̃ 方程破坏项中的长度尺度（默认修改方程中全部长度尺度）**。
  - **DES-Realizable k-ε**：选项 delayed DES、viscous work、compressibility effects；**Cdes = 0.61；EWT-ε 恒启用**。
  - **DES-SST / DES-BSL**（16.12.3/16.12.4；SST 在 DES 下选 SST k-omega，BSL 为 k-omega → BSL → Scale-Resolving 组框勾 DES）：选项 low-Re corrections、近壁处理、delayed DES、viscous work、曲率修正、compressibility effects（BSL）/production limiters、Intermittency Transition；**delayed DES 启用后可选屏蔽函数 F1 / F2 / DDES / IDDES（16.16.27）**；**两者 Cdes 均为 0.61**。
  - **DES-Transition SST**（16.12.5）：Transition SST + Scale-Resolving 组框勾 DES；DES Options 组框可开 Delayed DES 并选屏蔽函数；用底层 y⁺ 不敏感壁面处理。
- **LES**（16.13）：亚格子模型五选：Smagorinsky-Lilly / **WALE（默认）** / WMLES / WMLES S-Omega / Kinetic-Energy Transport。Smagorinsky-Lilly 附加选项：**Dynamic Stress**（启用后即"dynamic Smagorinsky"）+ 其下的 Dynamic Energy Flux 与 Dynamic Scalar Flux；Kinetic-Energy Transport 自带 Dynamic Energy/Scalar Flux（恒运行为动态模型）。**Dynamic Fvar**（动态混合分数方差）在选 Non-Premixed / Partially Premixed 燃烧时对所有亚格子模型可用。**Near Wall RANS Layer (WMLES) 选项适用于 Smagorinsky-Lilly（含动态）与 WALE**。近壁处理：Kader blending（当前默认）/ **Harmonic blending based on r⁺（推荐；TUI `near-wall-treatment/harmonic-blend-rplus-wf?`）** / Werner-Wengle（TUI `.../werner-wengle-wall-fn?`）。
- **模型常数**（16.14）：可改但多数应用无必要；C1-PS/C2-PS 为线 性压力-应变近似常数（Theory Guide Eq 4.250/4.251）、C1'-PS/C2'-PS（Eq 4.252）、C1-SSG-PS…C5-SSG-PS 为二次压力-应变近似常数（Eq 4.261）。
- **ELES**（16.15）：大 RANS 域内嵌小 LES 区。①Viscous Model 启用任意 RANS 模型或选 DES/SAS/SDES/SBES——**唯一与 ELES 不兼容的 RANS 模型是 Spalart-Allmaras**（单方程无法向界面方法提供所需湍流长度尺度）。**纯 RANS 模型全局施加、但湍流变量值在 ELES 区内被冻结**（冻结态用于确定下游 LES-RANS 界面处的流动条件——**须以收敛较好的全局 RANS 解起步**）；**DES/SAS/SDES/SBES 作全局模型时不冻结、在 ELES 区后台运行**以取得下游界面条件。②瞬态求解器下在 Fluid 对话框勾 **LES Zone**（出现 Embedded LES 页；仅瞬态求解器显示；RANS 模型须手动；全局为 DES/SAS/SDES/SBES 时此两步可跳过——记住 DES 在无壁自由流中的局限）。③Embedded LES 页选 **Embedded Subgrid-Scale Model**（Smagorinsky-Lilly / **WALE 默认** / Dynamic Smagorinsky / WMLES / WMLES S-Omega；WALE 给 Cwale、S-L 给 Cs）与 **Momentum Spatial Discretization（BCD / CD）**。④把合适的 interior 界面区类型改为 **rans-les-interface**（树中右键边界区 → Type 子菜单）→ RANS/LES Interface 对话框：命名 + **Fluctuating Velocity Algorithm**（No Perturbations / Spectral Synthesizer / **Vortex Method**）+ **Number Of Vortices**（随机撒布在面区生成湍流脉动的涡数；须大到面区无"盲点"；增大仅略增 CPU 不损结果；**建议最少 ≈ LES 侧界面单元面数的 1/4**）。非保形界面：用 Mesh Interfaces 对话框 List 按钮查 interior 区名。**Important：RANS-LES 界面应置于无倒流区域**。

## 16.16 通用设置选项（pp. 2186–2201）

- **viscous work**（16.16.1）：Theory Guide + p. 2222。
- **浮力对湍流**（16.16.2）：非零重力 + 非等温时可选——**Off / Only Turbulence Production（默认：k 或雷诺应力输运方程计入浮力；ω 基模型同时在 ω 方程计入来自 k 方程的贡献项）/ Full**（ε 基再计入 ε 方程浮力项；ω 基再计入 ω 方程中来自 ε 方程的贡献项）。适用：三个 k-ε；三个 k-ω（含配 SRS 或 Intermittency）；GEKO（同）；Transition SST；RSM。
- **曲率修正**（16.16.3）：修改湍流生成项；适用 SA、三个 k-ε、四个 k-ω、SAS、DES-BSL/SST/SA/rke、SDES、SBES。**RNG 与 Realizable 自带旋转/旋流项——曲率修正慎用（主要为完整性提供）**。Options 勾选；**CCURV 强度系数**可给常数/表达式/UDF。
- **角隅流动修正**（16.16.4）：针对矩形通道/非圆管/翼身结合部的角隅二次流；适用 SA（SA、SA-DES）、Standard k-ω（+SAS）、BSL/SST/GEKO/Transition-SST（+SAS/DES/SBES）。**CCORNER** 系数：常数/表达式/UDF（DEFINE_CORNER_FLOW_CORRECTION_CCORNER）。
- **可压缩效应**（16.16.5）：大多数 ε 基/ω 基/RSM 在可压理想气体或真实气体启用时可用；改善高 Mach 自由剪切层（取舍见 16.2.1.10）。
- **生成限制器**（16.16.6）两种公式：**Production Limiter（Theory Guide Eq 4.460；系数 Production Limiter Clip Factor 默认 10**，启用后在 Model Constants 改）与 **Production Kato-Launder（Eq 4.464）**。TUI：`turbulence-expert/production-limiter?[yes]`、`turbulence-expert/kato-launder-model?[yes]`。Production Limiter 适用 k-ε 三种/k-ω 四种/SAS/DES-BSL/DES-SST/DES-rke/SDES/SBES——**ω 方程基模型默认启用**；Kato-Launder 适用面略窄（Standard/RNG k-ε、四个 k-ω、SAS、DES-BSL/SST、SDES、SBES）——**仅 Transition SST 默认启用**。
- **SA 生成项**（16.16.7）：Vorticity-Based（变形张量 S 按 Eq 4.22）或 Strain/Vorticity-Based（Eq 4.24）；仅 SA 启用时显示。
- **Delayed DES**（16.16.8）：使用 DES 时推荐开启——在整个边界层内保持 RANS 模型。
- **RNG 专属**（16.16.9/16.16.10）：**Differential Viscosity Model**（有效黏度微分式，Eq 4.44，计入低 Re 效应；RNG Options 勾选）；**Swirl Dominated Flow**（旋流修正默认对全部 3D 及带旋流的轴对称流动生效；**旋流常数默认 0.07**（Eq 4.46）适合弱到中等旋流——强旋流须先勾 Swirl Dominated Flow 再改大该常数）。
- **Low-Re corrections**（16.16.11）：k-ω 系与 Stress-Omega RSM 的 k-omega Options 下可选；**默认不启用（阻尼系数 = 1）**。
- **Shear flow corrections**（16.16.12）：Standard k-ω 与 Stress-Omega RSM 改善自由剪切流精度；**默认启用**（标准 k-ω 模型已含 [176]）；关闭时 α∞ 与其导数置 1。
- **Turbulence damping**（16.16.13）：VOF/Mixture/Multi-Fluid VOF 的 Eulerian 可用；更好地解析流体-流体界面附近速度梯度；**Damping Factor 默认 10**；**仅推荐 sharp 与 sharp/dispersed 界面建模类型**。
- **EWT 附加效应**（16.16.14/16.16.15）：Pressure Gradient Effects 与 Thermal Effects（均计入 Theory Guide Eq 4.396 的系数；密度用理想气体时 Thermal Effects 还引入附加系数）。
- **壁面反射项**（16.16.16）：linear pressure-strain RSM 默认计入（Eq 4.252 → 4.249）；quadratic pressure-strain、Stress-Omega、Stress-BSL 不需要也不计入。**Important：反射项常数与函数按单壁简单规范流动（槽道、平板边界层）标定——多壁且壁面显著弯曲（轴对称管、曲形管道）时可能不改善精度，可在 Reynolds-Stress Options 关闭 Wall Reflection Effects**。
- **k 方程求墙边界条件**（16.16.17）：ε 基 RSM 默认墙处雷诺应力显式边界条件（Eq 4.279）+ k 由各正应力方程求和得到的 k 方程求解；关闭 Wall BC from k Equation 改用 Eq 4.280。仅 RSM 启用时显示。
- **Quadratic pressure-strain**（16.16.18）：Reynolds-Stress Options 勾选；启用后 **Wall Reflection Effects 与 Enhanced Wall Treatment 不可用**。
- **Stress-Omega/Stress-BSL**（16.16.19）：Reynolds-Stress Model 列表选；不可用：Wall BC from k Equation、Wall Reflection Effects、四种近壁处理（standard/scalable/non-equilibrium 壁面函数、EWT）；可用：Low-Re Corrections 与 Shear Flow Corrections（仅 Stress-Omega）、SAS。
- **亚格子模型**（16.16.20）：五选同 16.13；Dynamic Stress 使 Smagorinsky-Lilly 成为 dynamic Smagorinsky；Kinetic-Energy Transport 恒动态；Dynamic Fvar 配燃烧；Near Wall RANS Layer (WMLES) 适用 Smagorinsky-Lilly（含动态）与 WALE。
- **自定义湍流黏度**（16.16.21）：SA/k-ε/k-ω/DES/LES 可挂 UDF（LES 可实现全新亚格子模型；挂 Subgrid-Scale Turbulent Viscosity 下拉）；**SBES+BSL/SST 的 UDF 只能定制 RANS 区的 ν̃ 公式、不能定制 LES 区亚格子模型**。
- **自定义湍流 Prandtl/Schmidt 数**（16.16.22）：UDF 挂 Prandtl Numbers / Prandtl and Schmidt Numbers 组框——TKE Prandtl（standard/realizable k-ε 与 standard k-ω）、TDR/SDR Prandtl、Energy Prandtl（除 RNG k-ε 外全部）、Wall Prandtl（全部）、Turbulent Schmidt Number（启用组分输运时；除 RNG k-ε）；**LES 开 Dynamic Energy/Scalar Flux 时能量 Prandtl 与组分 Schmidt 数不能用 UDF**；可用性受能量/多相/燃烧设置影响。
- **非牛顿流体湍流**（16.16.23）：`define/models/viscous/turbulence-expert/turb-non-newtonian?` 启用材料黏度的非牛顿选项（p. 1693）。
- **SDES/SBES 挂接**（16.16.26）：Scale-Resolving Simulation Options 勾 **Stress Blending (SBES) / Shielded DES**；**仅 3D 瞬态**；适用 GEKO、BSL k-ω、SST k-ω、Transition SST、**Realizable k-ε（配 scalable wall functions 或 enhanced wall treatment）**。Hybrid Model：**SDES（仅屏蔽函数）/ SBES（屏蔽 + 应力混合）/ SBES with User-Defined Function（自定义分区混合函数——DEFINE_SBES_BF）**。SBES 系可再选亚格子模型：Smagorinsky-Lilly / Dynamic Smagorinsky-Lilly / **WALE（推荐——2D 区涡黏最低、分离剪切层快速建立 3D 湍流结构）/ WMLES S-Omega**（**SBES + WMLES S-Omega 组合可能无用——SBES-WALE 本身就能起 WMLES 模式**）。**Update Interval k-omega（1–10，Realizable k-ε 不可用）**：每 N 步才算一次 k/ω 方程（动量与 LES 涡黏部分每步都更新）——LES 部分所需时间步对 RANS 部分过小，降低 k/ω 更新频率省时且影响极小，**最优值 5**。限制：仅 ω 方程基 RANS；不兼容多相；不兼容自适应时间步；变密度或动网格时 k/ω 时间格式自动一阶（其他方程不受影响）。**SDES/SBES 动量离散推荐 BCD（默认）**。
- **屏蔽函数**（16.16.27）：BSL/SST/Transition SST 的 DES：F1（Eq 4.108）与 F2（Eq 4.119）——**F2 比 F1 更保守**；另有 DDES 与 IDDES；**DDES 推荐且为默认**。

## 16.17–16.20 边界条件、初值、求解策略与后处理（pp. 2201–2220）

- **湍流边界条件**（16.17）：墙的湍流量边界条件由 Fluent 内部处理，用户只需给进口（velocity/pressure inlet 等）——进口湍流显著影响下游流动。
  - **壁面粗糙度**（16.17.1）：在墙对话框给粗糙高度与粗糙常数（p. 1509）。**粗糙壁不可用于**：ε 方程模型 + EWT 或 Menter-Lechner（涉及全部 k-ε、linear pressure-strain RSM、DES-Realizable）；Stress-Omega/Stress-BSL RSM；transition k-kl-ω；**LES**。
  - **SA**（16.17.2）：只需给进口 ν̃ 边界条件。**k-ε/k-ω**（16.17.3）：进口给 k & ε（或 k & ω）（方法见 p. 1446）。**层流区**：`define/boundary-conditions/fluid` 的 **Set Turbulent Viscosity to zero within laminar zone?** 设 yes → 该区湍流生成项与 μt 置零；Fluid 对话框 Laminar Zone 选项同样默认。**Important：层流区功能对 SA 与 RSM 同样可用**。
  - **RSM**（16.17.4）：入流边界默认输入与 k-ε 相同——**湍流量经各向同性假设换算成雷诺应力（Eqs 16.4/16.5：正应力分量 = 2k/3 形式，公式体未提取）**；ε 同 k-ε；指定方法选 **K 或 Turbulent Intensity** 作 Reynolds-Stress Specification Method；或选 **Reynolds-Stress Components 直接给应力分量**（常数/坐标 profile/UDF）。
  - **SRS**（16.17.5）：可在 velocity/pressure inlet 指定**非定常脉动速度**生成真实湍流内容（Theory Guide）。
- **k/ε（或 k/ω）初值**（16.18）：收敛解与初值无关，但合理初值改善收敛；y⁺ 不敏感壁面处理下**给定合适的湍流场至关重要**：①能给出合理进口边界条件时从边界值算全域初值（p. 3765）；②复杂流动按 **Turbulent Intensity（典型 1–10%）与 Turbulent Viscosity Ratio（典型 1–100）** 给初值——**k 由 I 与特征速度算（Eq 16.6）；涡黏取分子黏度的 1–100 倍反推 ω（Eq 16.7）；ε 同理（Eq 16.8）**（公式体未提取，语义自正文）；RSM 雷诺应力按 Eqs 16.4/16.5 自动初始化。
- **求解策略**（16.19）：
  - 网格（16.19.1）：先设想流动、识别主要特征、按特征划网格；壁面约束流格外小心（pp. 2136/2141）。
  - 精度（16.19.2）：选合适模型；**对流项用高阶格式**（湍流平均量梯度更大；三角/四面体网格尤甚；过度数值扩散即使最好的模型也救不回）；进口值要真实（下游常由进口边界条件主导）。
  - 收敛（16.19.3）：初值过差可能发散——从保守（小）欠松弛与（密度基）保守 Courant 起步渐增；k/ε 初场要合理（y⁺ 不敏感处理尤甚）；**RNG k-ε：先用 standard k-ε 得解再切 RNG（RNG 非线性更强、需更低欠松弛/Courant）**。**EWT-ε：全域 y* < 200 时 ε 改由代数式（Eq 4.390）而非输运方程计算——此时 ε 残差显示为零属正常现象**。
  - **RSM 专属**（16.19.4）：动量与湍流应力耦合更强 → 稳定性/收敛更难：**先用 standard k-ε 算，再开 RSM 以 k-ε 解为初值**；**强旋/复杂流动用低欠松弛 0.2–0.3 + 低 Courant（速度与全部应力都要降）**；强旋流另参考旋流策略（p. 1815）。雷诺应力欠松弛（16.19.4.1）：默认 0.5 推荐多数工况、开始收敛后可提高；只调部分欠松弛有时优于整体缩放。暂停雷诺应力更新（16.19.4.2）：Equations 对话框（Solution → Controls → Equations...）冻结当前应力场解其他方程。残差（16.19.4.3）：各雷诺应力输运方程分别报告；归一化残差约 10⁻⁴ 量级通常即实用收敛（具体数值符号未提取），完全收敛需更严标准。
  - **LES 专属**（16.19.5）：瞬态 + 细网格 + 合适时间步；须跑到与初值无关且能统计。五步：①先跑定常 RANS（standard k-ε/k-ω/RSM）至基本收敛，然后**在启用 LES 之前**执行 `solve/initialize/init-turb-vel-fluctuations` 从 RANS 结果生成瞬时速度场（SA 除外全部 RANS 基模型可用；初场更真实、更快进入统计稳定；可选）；②启用 LES 自动开瞬态 + 二阶隐式；压力基动量自动选 **BCD**（LES 下全部方程可选 BCD 与纯 CD；密度基可用 BCD 但非默认）；③跑到统计定常（监视选定位置的力与变量）；④**`solve/initialize/init-flow-statistics` 清零初始统计，重启前在 Run Calculation 开 Data Sampling for Time Statistics**（可设 Sampling Interval；Sampled Time 显示已采样时长——定时间步时除以时间步即样本组数；变时间步自动按当前时间步加权）；⑤跑到统计稳定——时长按平均驻留时间 L/U 估算、**至少跑几个平均驻留时间**。时间离散推荐二阶；空间离散避免过度耗散格式（一阶迎风抹平解析涡），**全方程推荐中心差分类格式；选 LES/SAS/DES/SDES/SBES 时动量默认 BCD**。
- **后处理**（16.20）：各模型的湍流量清单（Turbulence... 类别；定义见 p. 4395）：
  - **SA**：Modified/Turbulent Viscosity、Effective Viscosity、TVR、有效导热/Prandtl、Wall Yplus、fr（曲率修正启用时）。**DES+SA**：另加 DES TKE Dissipation Multiplier（Eq 4.291 的函数）、Q Criterion Normalized/Raw、Lambda 2 Criterion。
  - **k-ε**：k、Turbulent Intensity、ε、Production of k、Turbulent Viscosity、Effective Viscosity、TVR、有效导热/Prandtl、Wall Ystar/Yplus、Re_y（仅 EWT）、fr。**DES-Realizable**：另加 DES TKE Dissipation Multiplier、Q、Lambda 2。
  - **k-ω**：k、Intensity、ε、**Intermittency**、ω、Production of k、黏度类、Wall Ystar/Yplus、Re_y、fr。**SAS（配 Standard/BSL k-ω）**：另加 Q/Lambda 2。**DES（配 BSL/SST）**：另加 DES TKE Dissipation Multiplier（Eq 4.302/4.306——LES 区放大 k 输运方程破坏项、降低涡黏）。**SDES/SBES（配 BSL/SST）**：另加 Shielding Function for SBES/SDES、Q、Lambda 2。
  - **Transition k-kl-ω**：k、**Laminar Kinetic Energy、Total Fluctuation Energy**、Intensity、ε、ω、Production of k、**Production of laminar k**、Turbulent Viscosity（含 large-scale/small-scale 两分量）等。**Transition SST**：k、Intensity、ε、**Intermittency、Intermittency Effective、Momentum Thickness Re、Geometric Roughness Height**、ω 等；配 SAS/DES/SDES/SBES 再加相应结构量（Q/Lambda 2、DES TKE Dissipation Multiplier 或 Shielding Function）。
  - **RSM**：k、Intensity、**UU/VV/WW/UV/VW/UW Reynolds Stress**、ε、ω（ω 基专属）、Production of k、黏度类、Wall Ystar/Yplus、Re_y（ε 基专属）。**SAS 配 ω 基 RSM**：另加 Q/Lambda 2。**SAS 配 SST**：k/Intensity/ε/Intermittency/ω/Production of k 等加 Q/Lambda 2。
  - **LES**：TKE、Turbulence Intensity、**Subgrid Kinetic Energy、Production of k、Subgrid Turbulent Viscosity、Subgrid Effective Viscosity、Subgrid TVR、Subgrid Filter Length、Subgrid Test-Filter Length、Subgrid Dissipation Rate、Subgrid Dynamic Viscosity Const、Subgrid Dynamic Prandtl Number、Subgrid Dynamic Sc of Species、Subtest Kinetic Energy**、有效导热/Prandtl、Wall Ystar/Yplus、Q/Lambda 2。
  - **ELES 附加说明**（Note）：ELES 区内模拟涡黏由代数亚格子模型给出；全局模型冻结或（SAS/DES/SDES/SBES 配两方程 RANS 时）以"passive 模式"运行不影响动量。**区内有两个模拟涡黏要区分：冻结/被动全局模型的（Turbulent Viscosity、TVR——全局模型无法被动运行时为零）与实际作用于动量的局部代数亚格子模型的（LES Subgrid Turbulent Viscosity）**；动态量（Test-Filter Length、Dynamic Viscosity Const、Subtest KE）在 ELES 区用 Dynamic Smagorinsky 时可得（全局 LES 的 Dynamic Stress 或 Kinetic-Energy Transport 亦然）。
  - **自定义场函数**（16.20.1）：Custom Field Function Calculator——常用：P/ε 比、平均流/湍流时间尺度比、Boussinesq 公式导出的雷诺应力。
  - **湍流统计后处理**（16.20.2）：开 Data Sampling for Time Statistics 后收集均值 + RMSE；**Unsteady Statistics...**（Resolved UV/UW/VW Reynolds Stress、Resolved UT/VT/WT Heat Flux、组分 RMSE/Mean Mass Fraction 等）；**Unsteady Wall Statistics...**（Mean Pressure Coefficient、Mean Wall Shear Stress、Mean X/Y/Z-Wall Shear Stress、Mean Skin Friction Coefficient、Mean Surface Heat Flux、Mean Surface Heat Transfer Coef.、Mean Surface Nusselt Number、Mean Surface Stanton Number）。**这些量只是采样解的统计评估、不含任何模拟湍流脉动**。**Important：均值统计只在内部单元收集、不在壁面上——壁面上画的均值其实是紧邻壁面单元的值**。采样变量集控制：Sampling Options 与 Zone-Specific Sampling Options 两个对话框（Solution → Run Calculation → Sampling Options... / Sampling Options (Zone Selection)...）；**Important：增删统计变量后建议重新初始化流场统计**。
  - **排错**（16.20.3）：画 k 云图查异常大小（生成大的区域 k 应高）；**画湍流黏度比场确认湍流是否充分起作用——RANS（非 LES）充分发展湍流的 μt/μ 通常至少高两个量级**；y⁺ 不敏感处理下核查近壁网格（p. 2136）；**EWT-ε 可画 Re_y（湍流雷诺数）填充云图叠加网格显示**。

## 证据与适用条件

- 来源：[[Ansys Fluent Users Guide 2026 R1]]（[[Ansys Fluent Users Guide 2026 R1|来源记录]]）Part III / Ch.16；本页覆盖批次 60（pp. 2125–2166，16.1–16.9）与批次 61（pp. 2167–2220，16.9 尾段 + 16.10–16.20），均 2026-10-18 读取。**Ch.16 全章已摄取完毕。**
- **公式体未提取**：Eq 16.1–16.3（批次 60 段）与 16.4–16.8（RSM 进口雷诺应力各向同性式、k/ω/ε 初值估算式）为图形对象，仅按周边文字记录语义（如正应力 = 2k/3 形式、涡黏取分子黏度 1–100 倍等）。**希腊字母符号在提取文本中系统性丢失**——模型名/系数名按标准名称补全（Csep/Cnw/Cmix/Cjet、Cdes、CCURV、CCORNER、Cwale、Cs 等自 TUI/正文核实），RSM 残差收敛量级等个别数值符号未提取处以语义标注；WMLES ω 基变体名经批次 61 的 LES 设置节核实为 **WMLES S-Omega**（补全批次 60 清单处的存疑项）。
- 本页数值（Cdes 0.65/0.61、旋流常数 0.07、Damping Factor 10、Clip Factor 10、Update Interval 最优 5 且范围 1–10、涡数 ≥ LES 侧面数 1/4、I 1–10%、TVR 1–100、RSM URF 0.2–0.3 与默认 0.5、驻留时间若干倍、湍流黏度比两个量级等）为原文正文数值。
- 引用的 Theory Guide 公式编号（Eq 4.22/4.24/4.44/4.46/4.75/4.85/4.92/4.108/4.119/4.224 系列/4.245/4.249–4.261/4.279/4.280/4.290–4.306/4.367/4.390/4.396/4.460/4.464/7.4）仅作定位、未核验内容。
- 关联章节引用（近壁处理 p. 2193–2196、屏蔽函数 p. 2201、湍流参数确定 p. 1446、壁面粗糙度 p. 1509、层流区 p. 1372、非牛顿黏度 p. 1693、旋流策略 p. 1815、传热问题 p. 2222、初始化 p. 3765、瞬态设置 p. 3784、时间统计后处理 p. 3808、场函数 p. 4395、Viscous Model 对话框 p. 4922、Species Model 对话框 p. 4975、Run Calculation p. 5422、Operating Conditions p. 5189、Mesh Interfaces p. 5755）仅作定位。
- 版本敏感：LES 近壁默认 Kader blending（推荐 r⁺ harmonic）；LES/SAS/DES/SDES/SBES 动量默认 BCD；Production Limiter 默认启用面（ω 基全部）、Kato-Launder 仅 Transition SST 默认；WALE 为 LES 与 ELES 默认亚格子模型；SBES 可选亚格子模型清单含 WMLES S-Omega。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 基本流动建模]]（Ch.10 旋流数选湍流模型的衔接）
- [[Fluent 物理属性]]（湍流相关材料属性）
- [[Fluent Cell Zone 与边界条件设置]]（湍流边界条件所在的边界条件体系）
- [[Fluent 叶轮机械流动]]（phase-lag 仅支持 k-ε/k-ω/SST；TSN）
- [[index]]
