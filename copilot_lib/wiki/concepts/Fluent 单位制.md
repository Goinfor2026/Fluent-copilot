---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - units
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 单位制

## 摘要

User's Guide 2026 R1 Part III / Chapter 4（PDF pp. 1055–1058）：Fluent 允许任意单位制（含不一致单位）——用户提供与 SI 的换算因子，**求解器内部一律以 SI 存储/计算**，界面层做转换；case/data 文件中存的也是 SI。四个内置单位制与自定义方法见下。

## 单位机制与中途切换（PDF p. 1055）

- 工作单位制由"所填量 × 换算因子 = SI 值"实现；所有带维度的输入都会提示所需单位。
- **可中途切换**：SI 切 British 时，已输入的参数与默认提示都转换到新单位制；算完后再改单位制，结果显示层全部转换。
- 内部 SI 存储意味着 case/data 文件中的参数是 SI 值。

## 4.1 单位限制（PDF pp. 1055–1056）

无论使用什么单位制，以下内容**必须始终以 SI 定义**：

- 边界 profile（印刷页码 p. 1616）
- 源项（p. 1433）
- Custom field functions（p. 4519）
- 外部创建的 XY plot 数据文件中的数据（p. 4287）
- 用户自定义函数（UDF，见 Fluent Customization Manual）

**温度相关多项式材料属性**：函数中的温度恒为 Kelvin 或 Rankine——单位制用 Celsius/Kelvin 时多项式系数按 Kelvin 填；用 Fahrenheit/Rankine 时按 Rankine 填（印刷页码 p. 1670）。

## 4.2 网格文件中的单位（PDF p. 1056）

部分网格生成器允许定义网格尺寸单位，但**读入 Fluent 时长度单位总是假设为米**；不符时须缩放网格（Scaling the Mesh，印刷页码 p. 1332）。（与 1.6.9.1 CAD 导入"切 solution 后还原 CAD 单位"的规则互补。）

## 4.3 内置单位制（PDF pp. 1056–1057）

四个内置单位制：**British、SI、CGS、default**——树中 Setup → General → Units... 打开 Set Units 对话框，用 Set All to 下的按钮选择；点击立即生效，影响之后所有带单位的输入。**default 制类似 SI，但角度用度（degree）而非弧度（radian）**。

## 4.4 自定义单位（PDF pp. 1057–1058）

- **List** 按钮把所有量及其当前单位、换算因子与偏移打印到文本窗口。
- **改单个量的单位**：Quantities 列表（字母序）选量 → Units 列表选新单位；Factor/Offset 自动更新。示例：SI 下把 length 改 `in` → Factor 0.0254；把 temperature 改 `c` → Factor 1、Offset 273.15。
- **定义新单位**：选量 → New... → Define Unit 对话框填 Unit 名、Factor、Offset（示例：时间量定义 `hr`、Factor 3600）。
- **换算因子定义**：Factor = SI units / custom units，即自定义值 × Factor = SI 值。示例：length 用 inch → 0.0254；velocity 用 ft/min → 0.3048/60 = 0.0051（式 4.1 为公式图形，其数值结果由正文文字给出）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part III / Chapter 4，PDF pp. 1055–1058；目录范围至此完成（Ch.5 自 p. 1059 起）。Figures 4.1/4.2 与式 (4.1) 为图形元素；换算因子示例数值以正文文字为准。
- "必须用 SI 定义"的清单与温度多项式规则为手册明确陈述；印刷页码引用指向未摄取章节，仅作定位。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part III - Solution Mode]]
- [[Fluent 表达式语言]]（表达式的单位验证规则）
- [[Fluent 求解模式文件读写]]（mesh 读入的米假设）
- [[CFD 仿真工作流与验证]]（单位与尺度核查工作流）
- [[index]]
