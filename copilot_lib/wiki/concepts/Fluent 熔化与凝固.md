---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - solidification-melting
  - continuous-casting
  - mushy-zone
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 熔化与凝固

## 摘要

User's Guide 2026 R1 Part III / Chapter 28 "Modeling Solidification and Melting"（PDF pp. 3335–3342，共 5 节）。**本页全章完成（批次 89，pp. 3335–3342）**：焓-多孔介质法熔化/凝固模型的设置（Mushy Zone 参数、Lever/Scheil 规则、材料属性）、连续铸造 pull velocity 三种做法、热溶质浮力、求解策略（液相分数 URF）与后处理变量。理论见 Theory Guide "Solidification and Melting"（Chapter 15，式号 15.x 由本章引用）。

## 28.1 设置流程（pp. 3335–3338）

- 启用：**Setup → Models → Solidification & Melting → Edit**，勾选 **Solidification/Melting**（Figure 28.1）。启用后**自动打开能量方程**，无需再手动开 Energy。
- **Mushy Zone Parameter**（A_mush，Theory Guide Eq 15.6）：常量或 UDF（`DEFINE_SOLIDIFICATION_PARAMS`）。**推荐取值 10⁴–10⁷**（2026 R1 明确印出）；值越大阻尼曲线越陡、凝固时速度降到零越快；**过大会因单元在固/液间反复切换而振荡**。
- **Include Pull Velocities**：连续铸造拉坯速度开关；配合 **Compute Pull Velocities**（按 Eq 15.22 由速度边界条件自动计算）与 **Flow Iterations Per Pull Velocity Iteration**（默认 1 = 每次迭代后解 pull velocity 方程；液相分数接近收敛时可调大以提速，但更新时残差会跳动）。
- **Lever Rule / Scheil Rule** 二选一：**仅在启用 Species Transport 时可用**。Scheil 规则下可启用 **Back Diffusion**（参数 γ，Eq 15.19；常量或 `DEFINE_SOLIDIFICATION_PARAMS` UDF；**取值必须 0–1**）。
- 材料（Create/Edit Materials，Figure 28.2）：**Pure Solvent Melting Heat**（L，Eq 15.4；**必须为正的非零值才会凝固**）、**Solidus Temperature**、**Liquidus Temperature**（Eq 15.3）。
- 多组分凝固（Species Transport）：mixtures 需指定固/液相线温度的计算方法——默认 **mixing-law**（Eq 15.8/15.9，由各溶质的液相线斜率/分配系数算出），也可用 `DEFINE_PROPERTY` UDF；**强烈建议固相线与液相线用同一方法**。还需：混合物的 **Mass Diffusivity**（Eq 15.15/15.18）、**Eutectic Temperature**（Eq 15.10）、溶剂（Selected Species 列表最后一个组分）的 Pure Solvent Melting Heat 与 **Pure Solvent Melting Temperature**；每个溶质指定 **Slope of Liquidus Line**、**Partition Coefficient**（Eq 15.8）、**Eutectic Mass Fraction**（Eq 15.10），Lever Rule 下另加 **Diffusion in Solid** 系数（Eq 15.15）；溶剂不需这些参数。
- 边界条件附加项：①壁面与凝固层之间的**气隙接触阻力**——Wall 对话框 Thermal Conditions 下设 **Contact Resistance**（Eq 15.23；非零常量/profile/UDF）；②壁面**表面张力温度梯度**——Shear Condition 选 **Marangoni Stress**（详见 User's Guide Marangoni Stress 节，p. 1518）；③若让 Fluent 计算 pull velocity，注意速度边界条件如何进入该计算。

## 28.2 连续铸造 pull velocity 三种做法（pp. 3338–3339）

1. **指定常量/变量 pull velocity**（默认做法）：不勾 Compute Pull Velocities；初始化后用 **Solution → Initialization → Patch** 打常量值或 custom field function。可对全域 patch——**patch 值只在液相分数 < 1 的单元生效**。
2. **让 Fluent 全程计算**（Eq 15.22）：勾 Compute Pull Velocities；计算代价高，**仅当 pull velocity 强烈依赖固液界面位置时推荐**。
3. **只算一次**：先开 Compute Pull Velocities 迭代一步，再关闭继续算；此后全程沿用第一步算出的值。

## 28.3 热浮力与溶质浮力（pp. 3339–3340）

- 多组分凝固中密度变化来自温度与固液界面附近的组分梯度；在 Solidification and Melting 对话框勾 **Include Thermal Buoyancy** 与 **Include Solutal Buoyancy**（Figure 28.3）。**这两项仅在"凝固 + Species Transport"组合下可用**。
- 热浮力：按自然对流流程设操作条件与密度模型（User's Guide Buoyancy-Driven Flows 节，p. 1438）。
- 溶质浮力：在 Create/Edit Materials 给**除最后一个组分外的所有组分**设 **Solutal Expansion Coefficient**。
- 参考质量分数：默认用溶质的**共晶质量分数**作参考，无需额外输入；需自定义时走 TUI：`define/models/solidification-melting? yes` → `Include Thermal Buoyancy? yes` → `Include Solutal Buoyancy? yes` → `Use reference mass fraction of solutes? yes` → 逐组分 `Reference mass fraction of the species-i "value"`。

## 28.4 求解流程（pp. 3340–3341）

- 初始化建议：先 patch 初始温度或**先解稳态纯导热**作为初场；稳态/瞬态均可解，但**因问题强非线性，多数情况推荐瞬态**。
- 液相分数方程欠松弛因子（Solution → Controls → Under-Relaxation Factors → **Liquid Fraction Update**，即 α_β）控制迭代间更新：**β_{n+1} = β_n + α_β·Δβ**（Eq 28.1，Δβ 为预测的液相分数变化）。多数情况无需改默认 α_β（本页未印出数值）；收敛困难时调小可改善。**易收敛困难的四类工况**：稳态计算、连续铸造、多组分凝固、mushy zone 常数取值过大。

## 28.5 后处理（pp. 3341–3342）

- **Solidification/Melting...** 变量类别下可用：**Liquid Fraction**、**Contact Resistivity**（所有算例）；**Pull Velocity**（X/Y/Z/Axial/Radial/Swirl 分量，仅启用 pull velocity 时）；**Liquidus Temperature**、**Solidus Temperature**（仅多组分凝固即 Species 模型时）。场函数完整定义见 Field Function Definitions（p. 4395）。
- Figure 28.4 为连续晶体生长算例的液相分数云图（图形元素）。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3335–3342（批次 89，2026-10-20，pypdf layout 模式提取 + p. 3336/3341 以 fitz 300 dpi 渲染核对数值）。
- Mushy Zone 推荐范围 10⁴–10⁷、Back Diffusion 参数 γ 与 Eq 28.1 形式经渲染页面核实；α_β 数值默认值未在本章印出，未照录猜测值。
- 理论公式（Eq 15.3–15.23，Theory Guide Chapter 15）公式体未提取，仅按本章引用记录变量与语义；Figures 28.1–28.4 为图形元素未摄取。
- 版本敏感：设置路径、TUI 与默认控制以 2026 R1 为准。
