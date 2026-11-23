---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags:
  - Ansys Fluent
  - meshing
  - shortcut-keys
  - repair
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 快捷键与实体信息（Meshing）

## 摘要

User's Guide 2026 R1 Part II 附录 C（PDF pp. 893–906）汇编 Fluent Meshing 图形窗口的键盘快捷键（C.1）与实体信息（Ctrl+I，C.1.1）。快捷键按"屏幕工具/功能组"组织，覆盖选择过滤、CAD 对象管理、面标记与局部重划、边界修复原语（创建/删除/移动/交换/合并/坍缩节点面）、投影与目标、几何 primitive 构造、节点环选择等。**多数快捷键是上下文相关的：同一组合在不同模式（选择/标记/环选择/列表选择等）下功能不同**。

## 使用前提与通用行为（PDF p. 893）

- 使用方式：先在图形窗口显示几何、**点击图形窗口**，再按键组合；多数快捷键同时以图形窗口左侧与底部的屏幕工具按钮形式存在。
- **重复执行**：按键组合后，按住 Ctrl 并用右键做多次选择，可重复同一操作——仅部分操作支持；热键帮助会提示多次选择时将执行的（上一个）操作。
- `Ctrl+H`：把可用热键清单打印到消息窗口与图形窗口。

## 按功能组的关键快捷键（PDF pp. 893–904）

- **选择过滤器**：Ctrl+B 对象、Ctrl+C 单元（仅 Linux 版）、Ctrl+E 边、Ctrl+F 面、Ctrl+N 节点、Ctrl+X 位置、Ctrl+Y 尺寸（基于 size field）、Ctrl+Z zone；CAD 上下文：Ctrl+B CAD 对象、Ctrl+Z CAD zone、Ctrl+X 位置。
- **CAD 对象/树**（对 CAD Assemblies 与 Geometry/Mesh Objects）：F6/F7 高亮父/子 CAD 对象；Ctrl+C/L/S 隔离相似曲率/更小面积/相似面积对象；Ctrl+G 删除未激活/被抑制 CAD 对象；Ctrl+Y 清空树选择；Ctrl+Shift+P 显示 CAD 对象路径；Ctrl+P/Q/Shift+B 加入对象/替换对象/创建对象；Ctrl+Shift+N 重命名、Ctrl+Shift+R 更新、Ctrl+Shift+S 抑制 CAD 对象；Ctrl+Shift+F 提取 edge zones。
- **显示边界与查询**：Up/Down 箭头增减显示范围；Ctrl+L 打印所选面质心/边中心/节点坐标到 console；Ctrl+D 计算并显示两选择实体间距离（zone 间距离按各 zone facet 全局平均质心计算，平面与曲面基准不同）；Ctrl+G 显示所选实体的相邻面 zone；Ctrl+/ 在所选实体质心处插入裁剪面。
- **面标记（Marking options）**：Ctrl+Shift+J 按选择与参数标记（帮助文本显示标记选项说明）；Ctrl+S 标记所选面；Ctrl+D 泛洪（flood fill）标记；Ctrl+R 选区环带标记；Ctrl+Q 按质量标记；Ctrl+G 按角度标记；Ctrl+L 标记岛状面；Ctrl+U 取消标记（全部/所选）；Ctrl+I 打开 Mark Settings 对话框。
- **局部/Zone 重划**：Ctrl+Shift+R 打开 Local Remesh 或 Zone Remesh 对话框——选面时重划该面与指定径向层数；选 face zone 时按 Zone Remesh 重划该 zone；无选择时重划已标记面。
- **zone 分离（Ctrl+Shift+S，上下文相关）**：多区域 face zone → 按区域分离；单区域 face zone → 按角度分离；选面/边 → 按 seed 分离；edge zone + 面种子 → 按 edge loop 分离；无选择 → 按标记分离。
- **实体操作原语（Entities）**：F5 创建所选实体、F6 平滑、F7 split（仅面/边）、F8 swap（仅面/边）、F9 合并对、Ctrl+J 或 Ctrl+^ 坍缩（节点/边/面）、Ctrl+W 不经确认直接删除所选实体（节点/面/zone/对象）、Ctrl+Shift+Z 切换 edge zone 选择模式。
- **节点**：Ctrl+V 把节点从原位置移到新位置。
- **倾斜面检查**：Right 箭头按 skewness 降序显示（网格/活动组或标记面）；Left 箭头清除；F11 只显示最差倾斜面及其 ID 并在 console 打印 skewness 值。
- **视图与显示**：F12 撤销最近操作（如可撤销）；Ctrl+A 适配窗口；F3 切换鼠标 dolly 与右键当前功能；F4 切换 mouse-probe 多边形选择；Ctrl+Shift+E 在所选 zone/对象上独立于选择模式显示/隐藏边；Ctrl+_ 显示上一视图；F10 切换裁剪面 triad 显示；Ctrl+Shift+G 对齐对象；Ctrl+Shift+X 常视图/爆炸视图切换；Ctrl+Shift+T 透明切换（无选择时整个几何透明）。
- **隐藏/隔离类（不影响网格）**：Ctrl+Shift+H 隐藏、Ctrl+Shift+I 隔离、Ctrl+Shift+U 反转上次显示/隐藏、Ctrl+Shift+A 显示全部隐藏项、Ctrl+[ 或 Esc 取消最后选择、F2 清除全部选择与可视化辅助。
- **对象**：Ctrl+K 移除边界间隙（先设 target zone 再选 source zone）；Ctrl+Shift+M 合并所选对象/zone（对象须同类型；zone 须同类型或同属一对象，结果 zone 继承最先选中的名字）；Ctrl+Shift+N 打开 Change Object/Zone Properties；Ctrl+Shift+O 随机配色；Ctrl+Shift+V 选择全部可见对象/zone；鼠标左键点选/框选/多边形选。
- **投影与目标**：Ctrl+S 设置/取消投影目标（线/面/zone/对象；目标用于对象修改、面重划、节点或 zone 投影、间隙移除）；Ctrl+P 把所选节点/节点环/zone 投影到目标；Ctrl+I 显示目标信息并切换标识色。
- **补洞**：Ctrl+R 自动补洞（选 face zone 补全部自由边关联孔洞；选紧邻孔洞的单个面补冲孔；详见印刷页码 p. 651）。
- **zone 传递**：Ctrl+Shift+Y 把所选 zone 转入目标对象（未设目标时按 Create Geometry Object 对话框新建几何对象）；Ctrl+O 把所选面/单元重划入目标 zone。
- **构造几何 primitive**：Ctrl+Shift+K 进入 Construct Geometry 模式：Ctrl+B 包围盒、Ctrl+C 圆柱、Ctrl+F 圆台，F5 打开 Create Object 对话框完成创建。
- **节点环选择（Loop Selection 模式，Ctrl+Shift+L 进入）**：选节点环用于探针选择或创建 edge loop/封口面；Ctrl+O 开/闭环切换；Ctrl+D/E/B/P/F/Z 在首末节点间的直连、node loop、feature、zone boundary 等路径间切换；Ctrl+J 选中环路径上全部节点；Ctrl+K 按所选节点创建封口面；Ctrl+L 创建 edge loop；F2 退出。
- **列表选择选项模式（Ctrl+Shift+B 进入）**：基于图形窗口选择控制对话框列表——zone：Ctrl+Q 加入/Ctrl+S 移除/Ctrl+D 设为当前；对象：Ctrl+J/K/L 同理；树中 face zone label：Ctrl+F/G/R 加入/移除/设为当前；F2 退出。
- **颜色选项模式（Ctrl+Shift+C 进入）**：Ctrl+G 按几何恢复属性、Ctrl+O 按对象、Ctrl+Z 按 zone、Ctrl+N 按法向着色；Ctrl+P 切换调色板；Ctrl+R 随机化颜色；F2 退出。
- **条件显示选项模式（Ctrl+Shift+D 进入）**：Ctrl+S 隔离相似表面积项、Ctrl+I 隔离面积 ≤ 所选、Ctrl+C 相似曲率、Ctrl+N 邻域；Ctrl+Shift+A 显示全部；F2 退出。
- **杂项工具模式（Ctrl+T 进入；仅在存在 geometry 和 meshing objects 时可用）**：Ctrl+P 预览尺寸、Ctrl+C 画尺寸等值线、Ctrl+T 追踪实体间路径、Ctrl+J 以 Join 对话框连接所选面 zone、Ctrl+I 以 Intersect 对话框求交。
- **wrap face zones（Ctrl+Shift+F）**：改进特征捕捉和/或重划 wrap 面 zone——仅选 wrap 面 zone 时重划；wrap 面 zone + edge zone 时改进特征捕捉并重划；wrap 面 zone + edge 实体时仅改进特征捕捉。
- **Skewed faces 工具**：Right 箭头按 skewness 降序显示（网格/活动组或标记面）；Left 箭头清除。
- **Mesh/active group**：F11 只显示最差倾斜面及其 ID，并在 console 打印 skewness 值；F12 撤销最近操作（若可能）。

## C.1.1 实体信息（Ctrl+I，PDF pp. 904–905）

Ctrl+I 对所选实体显示的信息：

- **Zone**：zone 名、zone ID、位置、zone 类型、所属对象、所属 face zone labels、所属 regions、size functions。
- **Face**：面名、zone ID、节点、相邻单元、面 skewness（如适用）、周期孪生面（如适用）、子面（如适用）。
- **Edge**：边名、zone ID、相邻面。
- **Cell**：单元名、zone ID、节点、面、单元中心、skewness、simplex radius、单元尺寸。
- **Node**：节点名、zone ID、位置、相邻面（如适用）、相邻单元（如适用）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1（[[Ansys Fluent Users Guide 2026 R1]]）Part II / Appendix C，PDF pp. 893–906；p. 906 为版权页脚，无正文；条目 C.1–C.1.1 至此全部完成。
- 手册原表为三列（Onscreen Tool / Keys / Action / Feature）并大量使用图标按钮：**部分屏幕工具名是图形元素未被文本提取捕获**；同一快捷键在不同功能组下动作不同（如 Ctrl+S 在 CAD 隔离/面标记/投影/列表选择中各异）——本页按功能组归位，逐键用于脚本前应回查原表或用 `Ctrl+H` 在会话中核对。
- 印刷页码引用（p. 651 补洞、p. 735 提取边 zone）属 Chapter 7 范围（已摄取，见 [[Fluent 高级网格主题]]）。
- 仅覆盖 Meshing 模式快捷键；solution mode 的界面约定另见 Using This Manual（[[Fluent 手册排版与数学约定]]）。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]（来源记录）
- [[Part II - Meshing Mode]]
- [[Fluent 网格模式入门]]（工具栏与鼠标探针基础）
- [[Fluent 网格质量诊断]]（skewness 检查与 F11/箭头键互补）
- [[Fluent 高级网格主题]]（补洞/提取边 zone 所在章）
- [[index]]
