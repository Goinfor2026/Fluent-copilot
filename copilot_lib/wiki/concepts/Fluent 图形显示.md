---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - graphics
  - contours
  - mesh-display
  - postprocessing
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 图形显示

## 摘要

User's Guide 2026 R1 Part III / Chapter 41 "Displaying Graphics"（PDF pp. 4079–4324，14 节）。**本页全章完成（批次 111–115，pp. 4079–4324）：41.1–41.14 全 14 节——基本图形（网格/等值线/矢量/迹线/LIC/体渲染/场景/扫掠面）、显示定制（标注/色标/灯光/渲染）、增强效果与光线追踪、鼠标/窗口/测量/显示状态与视图、高级场景、关键帧动画、直方图与 XY/FFT/累积绘图/瞬态后处理。**

## 41.1 基本图形生成（pp. 4079–4130+）

- 图形对象两类：**persistent**（随 case 保存——Results → Graphics → 各项 → **New...**）与 **non-persistent**（**已弃用**、GUI 默认隐藏——Preferences → Graphics 勾 **Expose legacy non-persistent graphics** 恢复）。数据文件缺变量时取默认值——**跑一步迭代**即可得绘图所需值。远程显示慢：Xterm `xset -display :0 dpms force on`；glxgears 不达数千帧/秒需 IT 协助。离散相可显示颗粒轨迹（p. 2939）。
- **41.1.1 图形性能**：现代驱动 OpenGL2（Linux/Windows）或 DX11（Windows）；无硬件驱动时用 **OpenGL2 Mesa**（软件渲染、较慢）。Preferences → Graphics：**Surface Caching**（缓存表面加速重显示）；**Optimize for**（外观 vs 性能）；**Optimize Input Data**（大表面拆分提升交互性能——代价是分区线恒可见）；**Minimum Frame Rate**（最低交互帧率，可能损渲染质量）；**Fast Interactive Display**（按模型规模自动简化显示——首次带周边线的显示会延迟生成；交互中对象可能部分消失，可关闭该选项避免；**与 Minimum Frame Rate 不兼容**）。**(3D) 不建议显示 default-interior 面——负影响性能**。
- **41.1.2 网格显示**：四种视图——Outline（周边线）/Edges（网格线）/Faces（填充网格，3D）/Nodes（节点）。Mesh Display 对话框（Results → Graphics → Mesh → New...）：选面（Group By Surface Type 树状分组；Filter Text 过滤）→ Options 勾 Edges（Edge Type 选 **Outline** 或 **All** 或 **Feature**）/Faces/Nodes → Save/Display。填充网格平滑着色需开光照且插值法非 Flat；节点符号在 Display Options 改 Point Symbol。**并行**：Edges + Feature/Outline 默认不显示分区线（Preferences → Graphics 的 Remove partition lines 控制；模型缺面/分区线残留时调 Partition line removal tolerance）。
  - **41.1.2.2 网格配色**：两套调色板 **Classic / Pastel**（Preferences → Appearance 的 Model Color Scheme 控制）。非持久版经 Mesh Colors 对话框；持久版三种——**By Type**（按区类型配色；Zone Type Color and Material Assignment 对话框；surface type 适用于除 zone surfaces 外的所有表面网格）、**By Surface**（按面随机色（按 ID）；Surface Rendering Properties 对话框逐面定颜色/材质并保留；**Use Inherent Material Color 为全局选项**）、**Uniform**（所选面统一色/材质）。右键 Color by 逐面着色 + **Save as Scene** 存场景（含显示状态）。**默认墙颜色跟随偏好主题**（Gray Gradient ↔ Black 时自动黑白切换以保持可见性）。**Ctrl+Shift+O 随机化网格色**——仅 By Surface 生效；wall 在 Color by Type 时取偏好色不随机。
  - **41.1.2.3 真实感材质**：给网格对象指派材质（By Surface/By Type/Uniform 三途径）；**边界标记与真实感渲染不兼容**。
  - **41.1.2.4 网格透明**：全局 Mesh Display 对话框（工具栏按钮 / General 任务页 Mesh → Display... / Domain ribbon → Mesh → Display...）的 **Transparency** 滑块；透明工具栏按钮；或场景含网格对象。**默认只透视 2 层透明面**——Transparency Algorithm 与 **Depth Peeling Layers**（Preferences → Graphics）控制层数。
  - **41.1.2.5 显示选项**：**Feature 轮廓**——封闭 3D 几何标准 Outline 只画"外侧"边（复杂管道只现进出口）；开 Feature 并设 **Feature Angle**（默认 20°——相邻面法向夹角超阈值画边；调小更多细节）。**Partitions** 选项画分区边界。**Shrink Factor**（默认 0 相邻面/单元边重叠；1 退化为点；0.01 即可分辨相邻面/单元）。
  - **41.1.2.6 网格绘图定义**：命名网格对象随 case 保存（同 contour 定义流程）。
- **41.1.3 等值线与剖面**：contour = 变量等值线；profile = 等值线沿参考向量按值比例投影（地毯图）。注意：**In Memory 动画不含 contour lines**；黑线问题 → Preferences → Graphics 的 Display Lists 改 Geometry；**等值线只画变量有意义且相关的区域**（FSI——挠度不在流体区显示；表达式与自定义场函数则全区显示）。等值线面默认无反射——Appearance 的 Surface specularity for Contours 可调。
  - **41.1.3.1 快速着色**：Ctrl+左键选面 → 右键 **Color by > Variable | Color**——多面可不同色/变量加到同一窗口；**Save as Scene** 存为场景（同时保存显示状态——方位/效果/标尺等）。
  - **41.1.3.2 生成步骤**：Contours of 选变量（两下拉）→ Surfaces 选面（**2D 不选面=全域；3D 必选至少一面**）→ **Levels**（等值线数，最大 **100**）→ profile 勾 **Draw Profiles**（Profile Options 对话框：**Reference Value**（零高度参考值——值等于参考值的点画在定义面上）与 **Scale Factor**（投影缩放）——300–310 K 温度例：参考 300、缩放 5 放大 10 K 变化；**Projection Dir.** 投影方向——全域压力投影成地毯图、切片线 y 速度投影成速度剖面族）→ 选项（下）→ Save/Display →（可选）**Display State** 关联（Use Active 或下拉选既有）。
  - **41.1.3.3 选项**：**Filled**（填充等值线/地毯图；平滑着色需非 Flat 光照、**Clip to Range 开着得不到平滑填充**、填充剖面无平滑着色；**Draw Profile 设置不存入定义**）。**范围**：默认全域范围——Auto Range 关掉后 Min/Max 可编辑（Compute 恢复默认）；**Clip to Range**（默认开——范围外留白；关=范围外取色标端色）；**Global Range**（关=按所选面范围——Auto Range 关时不自动更新，点 Compute 或 Display 更新）。**Draw Mesh**（等值线叠网格作参照——设置不存入定义；要持久化用 mesh 定义 + 场景组合）。**Node Values / Boundary Values**：默认 Node Values 开（显示插值节点值）；线等值线恒用节点值。四种组合——Node+Boundary=节点值由边界面值插值；仅 Boundary=边界面值（不插值）；仅 Node=节点值由邻单元插值；都关=单元值。**有 "bnv" 标记的变量才有边界节点值**（Table 43.2–43.21）；开 Boundary Values 且选速度时壁面报用户指定壁面速度。face-only 函数（如壁面剪切应力）边界面显示的"单元值"实为面值（更准）。**多孔介质/2D fan/激波等不连续量用单元值**（节点平均会抹平间断）。**与报告/XY 图对比边界值时必须开 Boundary Values**；相交耦合壁与其 wall-shadow 结果可能随 Node Values 开关不同。**Setup 存储**（非持久版）：Setup 编号 1–10 存 Options/Contours of/Min/Max/Surfaces（Levels、Draw Mesh、Draw Profiles 设置不存、Setup 不存 case）。**41.1.3.4 等值线定义**：Contour Name 命名（**须唯一**）→ Save/Display；右键菜单 Edit/Copy/Delete/Display/**Add to**（保留当前窗口内容叠加）；colormap 可拖动/缩放（位置不存定义）；2D 下未选面时 Save/Display 自动为无表面的流体区建新表面。TUI：display/objects。
- **41.1.4 矢量显示**（节起于 p. 4122 末——默认每单元/面片中心画一矢量，长度与颜色……正文续下段，待批次 112）。

## 41.1.4（续）自定义矢量与矢量定义（pp. 4131–4132）

- **Custom Vectors**：Define 后经 **Vector Definitions** 对话框（Manage...）管理——查看定义（只读；改定义须删除重建）、Delete、Rename（**不得与标准矢量同名**，如 velocity/relative-velocity）、**Save.../Load**（自定义矢量在 case 间转移；其为合法 Scheme 函数，也可经 File/Read/Scheme... 载入）。
- **41.1.4.5 矢量绘图定义**：命名矢量对象随 case 保存（同等值线定义流程）；colormap 可拖动/缩放（位置不存定义）。

## 41.1.5 迹线（Pathlines）（pp. 4132–4144）

无质量颗粒流动可视化——从自建表面释放（**line/rake 最常用**）；离散相颗粒轨迹显示见 p. 2939。Pathlines 对话框（Results → Graphics → Pathlines → New...）：
- **生成步骤**：①Release From Surfaces 选释放面；②（仅 Eulerian 多相）Track in Phase 选相（all-phase 或默认主相）；③**Step Size**（计算下一位置的长度间隔；**进出单元时总会计算颗粒位置**——步长再大 entry/exit 也会显示）与 **Steps**（最大步数；**经验法则：Step Size × Steps ≈ 域长 L**）；④选项（下）；⑤**Save/Display** 画迹线或 **Pulse** 动画（Stop! 停止）；（可选）关联 Display State。
- **选项**：**Draw Mesh**（叠网格作参照——设置不存入迹线定义；要会话内持久用非持久 Pathlines 对话框 Edit...）。**Style 十种**——line / line-arrows / point / sphere / refined-sphere / ribbon / triangle / coarse-cylinder / medium-cylinder / fine-cylinder；**Pulse 仅支持 point/sphere/refined-sphere/line**。Style Attributes：line 设 Line Width（line-arrows 另有 Spacing Factor 与箭头 Scale）；point 设 Marker Size；sphere 设 Diameter + Detail（**refined-sphere 只设 Diameter——更高质量且帧率更好；直径过大（≥10）性能下降；无反射与阴影**；直径建议 ≈ 平均单元尺寸或步长的 1/4，单位=网格量纲单位）；Detail 4–50（小值如 6–8 性能好；球面渲染需开光照——Gouraud 比 Flat 平滑、比 Phong 快）；triangle 设半底宽、cylinder 设半径；**ribbon** 设 Width + **Twist By**（按标量场扭转，如 helicity——场只在单元中心算、扭转显示可能不平滑）+ Twist Scale（放大/缩小扭转）+ Compute 显示范围。**配色**：默认按 **Particle ID**；可按释放面 surface ID 或任意标量场；Auto Range 关掉手动 Min/Max（范围外取端色）。**Path Skip**（默认 0——所选面每面一条迹线；1 = 隔一画一；**面顺序决定跳哪些——自适应会改变迹线显示外观**）。**Path Coarsen** 粗化因子 n（每 n 点画一个；**进出单元的点恒画**）。**Reverse**（反向追踪来源——释放面变终点）。**Oil Flow**（壁面油流线——勾后 On Zone 选边界区，迹线约束在该面上）。**Pulse Mode**——Single（单波）或 Continuous（连续释放）；**Save Pulse Animation**（Write/Record Format 选视频/图片；**Continuous 脉冲视频长 5 秒、Single 一个完整周期**；Video Options.../Picture Options...）。**Accuracy Control**（大时间步时给 Tolerance 控制迹线误差）。**Relative Pathlines**（相对移动参考系的迹线）。**XY Plot along trajectories**——勾 XY Plot 后 Color by 变为 **Y Axis Function + X Axis Function**（Y 选量、X 选 **Time 或 Path Length**）→ Plot；**Write to File** 存数据（后续经 Plot Data Sources 读回绘图或叠加）。**保存迹线数据**：Type 三选——**Standard**（FIELDVIEW `.fvp`；稳态 ASCII、瞬态必须 BINARY；格式见 FIELDVIEW Reference Manual Appendix K）；**Geometry**（`.ibl`，GAMBIT 可读——Closed Index Arclength + Begin curve 系列格式照录）；**EnSight**（生成 `.mpg`（每时间步的颗粒坐标文件，格式照录）+ `.mscl`（每时间步标量（Color By 所选）文件）+ 新 `.encas`（原名加 `.new`——汇总原 EnSight Case Gold 文件与 mpg/mscl，**应读入这个新文件**）；须先用 File/Export... 写 EnSight Case Gold 相关文件；EnSight Encas File Name + Time Steps For EnSight Export 决定 EnSight 动画时间层数）。TUI：`display/path-lines/write-to-files`。**Node Values**：默认开（插值节点值）；face-only 函数（壁面剪切）的单元值 = 该单元作为 c0 的面值面积加权平均；不连续量（多孔/2D fan/激波）用单元值。**迹线定义**：命名保存（同 contour 定义）；**XY Plot 开启的迹线不能进场景**；colormap 可拖动。
- **41.1.6 LIC（线积分卷积）**（pp. 4144–4146）：用流场对贴到面上的纹理做卷积模糊——类似流动烟雾的静帧；一般用速度场、可用任意矢量场。**标准 LIC 各向同性卷积**——密集纹理（似浓烟）、能显示流线但**无方向性**（左右流看起来相同）。**限制：LIC 图上鼠标探针不可用**。**须先建 plane surface**。Results → Graphics → LICs → New...：Name；Color by 选着色变量；**Vectors of** 选 velocity 或 relative velocity；**Plane Surfaces** 选平面（New Plane... 可建）；（可选）Display State；**Range** 三选——Global / Local to the selected surface(s) / Custom；**Texture Size** 滑块（纹理图尺寸，以百像素计）→ Display → **Save** 持久化。
- **41.1.7 体渲染（Volume Renderings）**（pp. 4146–4153）：对整个域体积按场变量着色（可配透明与裁剪）；常与网格同场景提供参照。Volume Rendering 对话框（Results → Graphics → Volumes → New...）：**Home 选项卡**——Volume Of 选变量；Data Source 选 **Cell Centers 或 Nodes**；Range 选 Global/Local/Custom；Cell Zones 选区——即可 Save/Display。**Transparencies 选项卡**——关 Use range from Home tab 自定义；Count 增加透明区间数；Min/Max/Transparency Range（**透明度 1 = 全透明、0 = 全不透明**）。**Iso-Values 选项卡**——Count 设高亮等值数；逐个给 Value/Color/Transparency。**Clipping 选项卡**——Count 设盒/球数；Selection 选 **Inside/Outside**；给盒/球坐标。**注意：施加于体的裁剪作用于整个 3D 图形窗口——窗口内其他图形对象也被裁**。高质量图：体渲染与 raytracer 同窗口——**Rendering Options...（Home 选项卡）打开 Raytracing Display 的 Rendering 选项卡**同样适用于体渲染；**Quality 设 Best、Max Rendering Time 设长（如 300 秒以上）**。
- **41.1.8 场景（Scenes）**（pp. 4153–4156）：多图形对象单窗合成（如阀门口压力等值线 + 速度矢量 + 网格叠加），逐对象调透明度。"make selected faces transparent" 工具栏按钮是**临时**透明——要随 case 持久须用 scene 对象。Results → Scene → New...：Name；Title（图形窗口标签显示）；**Graphics Objects** 选对象（New Object 下拉可即建 mesh/contour/vector/pathline；**XY Plot 开启的迹线不兼容场景**）；**Transparency** 滑块逐对象调（**真实感材质渲染的网格面不受滑块作用**——需在 Material Editor 建更高透明的自定义材质）；Save 或 Save & Display。图形窗口右键 Save as Scene 亦可（含显示状态）。场景 colormap 可拖动/缩放（位置不存）；**每个图形对象可设不同 colormap 尺度**（其对话框的 Colormap Options...）。
- **41.1.9 扫掠面（Sweep Surface）**（pp. 4156–4158）：不显式建面即查看网格/等值线/矢量在各截面的变化。Results → Animations → Sweep Surface → Edit...：**Sweep Axis** 给 (X,Y,Z) 轴向 → **Compute** 更新 Min/Max Value → Display Type 选 Mesh/Contours/Vectors（首次选 Contours/Vectors 会打开相应对话框设置；后续 Properties 重开）→ 拖 **Value** 滑块（松开才更新；或输入值回车）→ **Create...** 把当前扫掠面存为面（Create Surface 对话框给名——**生成的是基于网格坐标的等值面；等值线/矢量设置不存入该面**）。**动画**：**仅 legacy 非持久/"global" 图形对象支持**（须开 Expose legacy non-persistent graphics 后经 Edit... 使用）——Animation 组给 Initial/Final Value + Frames → **Animate**。
- **41.1.10 隐藏图形窗口**（pp. 4158–4159）：命令行启动用 `fluent -driver null`；已运行会话 TUI `display/set/rendering-options/driver` → **null**（**先关全部图形窗口**）。驱动为 null 仍可 Save Picture 存图（**速度显著变慢、存图可能与开窗时不同**）。恢复：同命令 → driver> 回车列驱动 → 选（如 opengl）；有隐藏窗口开着会提示——Scheme `(close-all-open-windows)` 关闭后重试。**远程登录时部分驱动可能不工作——用 x11（Linux）或 msw（Windows）**。

## 41.2 自定义图形显示（pp. 4159 起）

叠加多图、加文字/灯光、裁剪面看内部、改图例等。**图形窗口可能标记 [Out of Date]**——右键 **Refresh Display** 刷新（右键无菜单时检查 View ribbon Mouse 组的右键设置非 Zoom/probe）；网格显示刷新用全局 Mesh Display 对话框当前所选面——可能与原显示不一致。
- **41.2.1 嵌入式图形窗口仪表板**：多图形窗口嵌入另一窗口（"picture in picture"——残差与报告绘图嵌入 Solution View）；自动按间隔更新父窗口，便于监视/后处理/演示；可做成仪表板动画存 **MP4** 等视频。（节续下段。）

## 41.2.7（续）标注管理（pp. 4183–4185）

- **编辑/删除既有标注**：Annotate 对话框 Names 列表选项（显示文本、Add 变 Edit）→ 改字体规格后 Edit 修改 / **Delete Text** 删除（可全选批量）；标注可在图形窗口**左键拖动**移动（带引线时引线自动跟随指向原位置）。
- **隐藏标注**：图形窗口右键 **Hide Annotations**（**Show Annotations** 恢复）；或 Annotate 对话框的 **Show/Hide**。
- **与图形对象关联**：图形对象显示时定义的标注**自动关联**该对象；也可在图形对象对话框点 **Annotations...** 打开 Annotations 对话框选用既有/定义新标注。

## 41.2.8 色标（Colormap）与范围（pp. 4185–4206）

默认色标蓝（最小）→红（最大）；有多个预定义色标，也可自建。Colormap 对话框（Results → Graphics → Colormap...；图形对象对话框内打开比 Views ribbon 或 Outline View 右键**选项更多**）；已显示对象可**双击色标**打开 Quick-Edit 面板就地改属性（离开编辑域即保存，含范围）；色标右上角悬浮 **X** 临时隐藏（拍照用）——右键 **Show Colormap** 恢复。**偏好**：Preferences → Graphics → Colormap Settings 控制字体/字号/尺寸/位置/物理尺寸/数字格式与精度等。等值线颜色数临时改动走 Contours 对话框的 Levels。**灰度注意**：要存灰度图应**存彩色图**（存灰度图时 Fluent 用内部灰度而非所选色标；存彩色图才用你的灰度色标）。
- **41.2.8.1 术语**：Diverging（转灰度后中间亮两端暗）；Field（按变量推荐——多场同图各用各色标）；**Flow-feature-N-bright-peak**（N 个亮峰助辨流动特征）；Fringes（亮度多次交替）；Highlights（后缀——9 个高亮分 10 级）；Sequential（转灰度下暗上亮）；Split（两色标合一、中点分上下）；Stacked（三色标堆叠、中间灰度、中点对比色线）；Striped（多对比条纹示量值）；Symmetric（中点对称）；Value（指示值区间内彩色、区间外单色）。
- **41.2.8.2 预定义色标清单**（约 60 个，名称照录）：aero、bgr（-highlights/-modern/-modern-highlights/-more-red/-pale/-pink/-bgr）、blue（-highlights/-light）、chromatic（-reverse）、cyan-yellow、diverging-*（blue-yellow-red/cool-to-warm(+highlights)/darkred-green/red-yellow-blue/spectral/warm-to-cool）、fea、field-*（granular-particles/liquid/phase-fraction/pressure/scalars/species/temperature/velocity）、flame、flow-features-1-bright-peak、green（-highlights/-light）、purple-magenta、red（-highlights/-light）、rgb（-modern）、sequential-*（black-body/cividis/inferno/panifex/plasma/viridis/water）、split-*（bgr-gray/bgr-modern(+black/inverted/white)/blue-gray-red/blue-green/cool-to-warm/rainbow/shaded-bgr/viridis-gray-inferno）、stacked-*（blue-green-red/blue-red-green/green-yellow-purple）、striped-*（cartoon/gray/shaded/wide-white）、symmetric-*（copper/platinum）、values-*（details-near-maximum/high/high-and-low/low/middle）。色标名两色之间的插值色数取决于色标尺寸。
- **41.2.8.3 选择**：Currently Defined 下拉选（含自定义）→ 设尺寸与刻度 → **Apply**（此后所有显示用新色标）。**Colormap Size**（建议 10 的倍数——色标中不同颜色数）；**Log Scale**（对数刻度——颜色代表值的对数、指数增长）；**Colormap Dimensions** 的 Length/Width Ratio 控制外观（物理尺寸/对齐走 Preferences）。**数字格式**：Type 三选——float（Precision 设小数位）/exponential（mantissa+指数）/general（按数值大小与精度自动）。
- **41.2.8.4 标签与标题**：默认标题 = 变量名 + 单位 + 图形对象名；标签数按屏幕分辨率自动。**Titles** 下拉——Variable and Object Name / Variable Only / None（只留单位）。**标签数**：关 **Automatic Skip** 后设 **Skip**（整数；如 Skip=10 即隔 9 个标签——首尾恒显示）；恢复 Automatic Skip 即复位。
- **41.2.8.5 自定义色标**：Colormap 对话框 **Edit...** 打开 Colormap Editor——命名 → **Base Colormap** 选起点 → 拖动 color stops 自定义分布（**insert stop** 加新锚点/点击色标区直接加——新 stop 颜色=点击处颜色；**remove stop** 删；双击 stop 或 Selected Color 改色；Selected Position 直输位置）→（可选）**Distribute** 均布锚点（**颜色总数不得少于锚点数**）→（可选）**Reverse** 反序 → **Apply** 保存 →（可选）**Reset** 回基础色标。**自定义色标存入 case 文件**。
- **41.2.8.6 参考文献**：Moreland Color Map Advice、Farge 两篇、Zeller & Rogers、Mikhailov Turbo、Toet Turbo（Bibliography 条目照录）。

## 41.2.9 灯光（pp. 4206–4209）

可加指定颜色与方向的灯光增强 3D 外观；默认已定义一盏灯。默认光照行为经 Preferences → Graphics → Lighting 控制（Lighting method、Headlight 行为与强度、Ambient light 强度）。**告诫**：只显示网格面时边可能显圆（第三方问题）——开 Mesh Display 的 Edges 或把 Lighting Method 设 **Flat**（View ribbon 下拉或偏好设置）。自动光照默认开；手动经两条路径：
- **Display Options 对话框**（Results → Graphics → Options...）：**Lights On** 开关 + Lighting 下拉（改后 Apply）。插值方法三种——**Flat**（面内不插值、最基础）/ **Gouraud** / **Phong**（面内插值、渐变更平滑）。
- **Lights 对话框**（Results → Graphics → Lights...）：**Headlight On** 手动开关（头灯 = 视线方向恒定照明，默认自动按对象优化）；Lighting Method 手动三选（Apply 生效）。
- **定义光源**：默认 light 0 = 深灰色、方向 (1,1,1)（平行光、似太阳——方向指从 (1,1,1) 指向原点的平行光线）。加灯步骤：①Light ID 增至新值；②勾 **Light On**；③Color 填颜色串（如 lavender）或 RGB 滑块（默认深灰）；④方向三法——Direction 输 (X,Y,Z)；Active Lights 球面上中键点选/拖动（左键转球）；图形窗口转到期望视位后点 **Use View Vector**；⑤重复加灯；⑥**Apply** 保存。**移除**：Light ID 选中后取消 Light On（定义保留、可随时重开——可预定义多盏灯按场景启用）；**Reset** 回上次 Apply/打开时状态。

## 41.2.10 渲染选项（pp. 4209–4211）

Display Options 对话框（Results → Graphics → Options...）Rendering 组——改后 **Apply** 生效（线宽与 logo 即时全窗更新）：**Line Weight**（默认 1 像素）；**Marker**（Symbol 默认圆内 + 号；Weight 默认 1 像素）；**Animation Options**——交互时 **All**（实心着色）或 **Wireframe**（线框；有图形加速卡时可能反而慢）；**Double Buffering**（大幅减闪烁；硬件不支持时软件双缓冲、耗内存）；**Front Faces Transparent**（不显示壳/网格外向面——用于双面看 slit wall 与双侧壁；**注意可能从某些视角遮住非预期面**，如等值线只从一侧可见）；**Hidden Surface Removal**（3D 建议开；2D/无重叠几何关闭以求性能）——**Hidden Surface Method** 四选：**Hardware Z-buffer**（硬件支持时最快；不可用自动回退 Software）、**Painters**（边缘锯齿少于 HW-Z；内存受限时代替 Software-Z）、**Software Z-buffer**（精确软件法最快、耗内存）、**Z-sort only**（快但不如 Software-Z 准）。**41.2.10.1 图形设备信息**：Display Options 的 **Info** 按钮打印驱动与硬件信息到控制台；**保持显卡驱动最新**（避免显示颠倒等问题）。

## 41.3 增强图形视觉效果（pp. 4211–4215+）

File → Preferences → Graphics 启用各视觉效果（**前提：Linux 用 OpenGL2、Windows 用 DX11 或 OpenGL2；无显卡要质量用 OpenGL2 Mesa**）。
- **41.3.1 图形优先级**（Preferences → Performance）四选：**Automatic**（按当前驱动平衡图形与性能）；**Enhanced Graphics**（重图形——开启全部 Graphics Effects）；**Enhanced Performance**（重性能——关全部效果 + Fast Interactive Display 自动对大模型启用）；**Custom**。
- **41.3.2 效果选项**（可单项启停；开 Reflections/Static shadows/Ground plane grid 会新增 **Plane direction**（影/反射/地面网格所在平面）与 **Plane offset**（模型与平面距离）两字段）：**Anti-aliasing**（模型边线与文字抗锯齿）；**Reflections**（指定平面镜像反射）；**Static shadows**（基面上静态影——不受当前光照影响、显卡渲染快、性能影响小）；**Dynamic shadows**（按当前光照在相应面上投影——随模型移动重算、比静态更耗算力）。（其余效果续下段。）

## 41.3.2（续）效果尾（p. 4215–4216）

**Ground plane grid**（基平面显示有限网格 + 新增 **Grid Lines Color** 字段定网格线颜色）；**Update after mouse interactions**（每次视图变化后重显图形效果）。

## 41.4 光线追踪真实感渲染（pp. 4217–4240）

（41.4 节体起于 p. 4217，属上段尾部跨入本段。）Raytracing Display 对话框（View → Graphics → Raytracing Display...）：步骤含 **Keep Effects (Hide Environment)**（保留环境光照/反射效果但不显示环境本身）；**3D HDRI Images** 选环境（要光照效果必须选环境）；backplate 可选颜色或图片背景；环境属性——**Vertical/Horizontal/Spin**（基于当前视点而非固定 XYZ，同值不保证一致外观）、**View Zoom**（显示环境比例）与 **Model Scaling Factor**（模型缩放匹配环境）、**Lock Model Location in Environment**（旋转时固定模型在环境中的位置——可能畸变，用 **Ground Height (distortion mitigation)** 滑 slider 缓解）、光照 **Intensity/Color**；Show Backplate（颜色或静态图）；Display 渲染 / Save 只存设置不显示。**Rendering 选项卡**：CPU Threads（超过核数取最大）；Quality（越高越久）；渲染时长（到时捕获存文件）。**41.4.1 动画两法**（动画定义须在求解前建）：①**Runtime 捕获**——动画定义勾 **Raytracer Image**（只存 PNG/JPEG 等 2D 格式）+ 打开 Raytracing Display 选环境 + Rendering 选项卡 Save Picture... 设 Resolution 并 Apply；②**Playback 转换**——求解时存 **HSF** 动画（避免拖慢求解），事后 Playback 对话框读取转换（可用替代算力追求视频质量）。**环境清单（照录）**：env——Mixed Texture Studio Apartment、Night Sky with Ground、Snowy Path；backplate——Desert Road、Ground and Mostly Sky、Industrial Workshop Floor、Mountains at Night、Salt Flats、Space、Warehouse with Skylights、Water and Mostly Sky。**41.4.4 限制**：含 raytracer 的嵌入式仪表板对象不存 case；**不能正交视图**；与 Save Picture 的 **Monochrome** 不兼容（嵌入时 Fluent 窗单色、raytracer 窗仍彩色）；**仅含 3D 表面的窗口可光线追踪**（纯 2D 绘图/动画不行）；**keyframe 场景动画与 raytracing 不兼容**。

## 41.5 鼠标按键功能（pp. 4241–4244）

Preferences → **Navigation** 分支定按键映射；**Theme** 多预设、改动后变 Custom。功能集：**Box Select / Box Select Add / Box Select Toggle**（左→右拖 = 完全包围才选；右→左 = 接触即选；Add 累加；Toggle 再选取消）、Pan（平移）、**Probe**（短/长描述；**悬浮值**需点探针工具栏按钮 + Preferences → Appearance → Selections 的 **Hover-Over Probe Values**；**告诫**：悬浮值为插值、点击探针打印值基于色标——手动设范围时两者可能不一致）、Roll-Zoom（横拖旋转、纵拖缩放）、Rotate (Pan in 2D)（横拖绕屏幕竖轴、竖拖绕横轴）、Set View Center（点移到窗口中心）、Zoom（框选放大：左→右放大、右→左缩小；**Mouse wheel 设为 Zoom 时表现为滚轮缩放**；**求解迭代中滚轮缩放无效**——把 Zoom/Roll-Zoom 指给其他组合键）。**Esc 取消全选**；**3Dconnexion Space 系列（Mouse/Pilot/Navigator）不支持**。

## 41.6 应用窗口查看（p. 4244）

标准工具栏按钮切换工具栏/任务页/控制台/图形窗口可见性；ribbon 与树不可全隐（内容可藏、标签恒显）；多图形窗口见 Managing Multiple Windows（p. 4173）；详见 GUI（p. 917）。

## 41.7 测量距离与角度（pp. 4245–4246）

View → Display → **Measure...**：Distance 或 Angle；Options——**Snap to Node**（点击吸附最近节点）、**Print to Console**；**Select 2 Points**（测距）或 **Select 3 Points**（测角——**第一点为角顶点**）；Clear / Esc / 工具栏清除按钮清除。

## 41.8 显示状态与视图（pp. 4246–4263）

**Ctrl+L 或 TUI `view last` 回退上一视图（可回退过去 20 个）**。
- **41.8.1 Display State**：可含字段——View、Front Faces Transparent、Projection、Axes、Ruler、Boundary Markers、Titles、Light ID（Use Active 时仅一盏活动灯才填 Light ID、多盏则 Don't Save）、Headlight、Lighting、Anti-Aliasing、Reflections、Static/Dynamic Shadows、Grid Plane。常用做法：布置好后图形窗口右键 **Save State**；或图形对象对话框 **Use Active** + Save/Display 关联；或下拉选既有状态。**重要：除 view 外的 display state 设置作用于所有用户（非 2D 绘图）窗口**——一窗开标尺、另一窗带关标尺的状态会把两窗标尺都关掉；**Display State 选 None = 沿用上一个显示对象的设置**。
- **41.8.2 选视图**：Views 对话框 / 工具栏下拉（3D）/ **交互式 triad**——单击轴/半球指向正/负向、右击反向、**青色 iso-ball = 等轴测**、白色旋转箭头 = 面内 ±90°、按住 triad 附近左键自由旋转（点 X 轴 = +X 朝向自己）。2D 无下拉与 triad——front 视图 X 右 Y 上、Z 右手定则。
- **41.8.3 操作**：**Auto Scale**（不改方向缩放居中）；旋转（默认左键；Shift 限制单方向；Roll-Zoom 绕屏法轴；Camera Parameters 对话框刻度/表盘——**滑块/指针松手回位、不反映累计旋转**）；**auto-spin 连续旋转**：TUI `display/set/rendering-options/auto-spin?` + Apply——Rotate 按键拖动中松开即启动自旋（速度=松开时拖速；点任意键停止；建议开 Double Buffering）；平移（2D 默认左键 Pan；3D 用中键点目标点居中）；缩放（中键 Zoom 框选左→右放大/右→左缩小；Roll-Zoom 拖下放大拖上缩小；Camera 刻度；**迭代中滚轮无效——先给左键指派 Zoom In/Out**）。
- **41.8.4 透视与相机**：Views 对话框 Projection——**Perspective（默认）/ Orthographic**。相机四参数（Figure 41.97）：**Position / Target / Up Vector（从 (0,0,0) 指向给定点）/ Field（水平与垂直视野）**——Camera 下拉逐个改坐标、**每改一项都要 Apply**。
- **41.8.5 保存与恢复视图**：**Default** 回默认 front 视图；**Previous** 回上一视图；Save Name + **Save** 存视图（重名询问覆盖；**覆盖默认视图须存 view 文件否则读 case 时被重算覆盖**——所有视图存 case，但默认视图读 case 时自动重算）；**Write...**（Write Views 对话框选视图）存视图文件、**Read...** 读入（重名询问覆盖）；Delete 删除（慎删预定义）。
- **41.8.6 镜像与周期重复**：对称/周期子域显示完整几何（亦可纯显示用途）。对称——Views 对话框 **Mirror Planes** 列表选对称边界；非对称域 **Define Plane...**（Mirror Planes 对话框给式 41.1 系数 a/b/c + Distance）→ Add → 选中并 Apply 显示；Delete 永久移除。周期——View ribbon 直接 **Periodic Instancing...**：Number of Reppeats（原文拼写照录；90° 扇区显示全管设 4）；多排不同周期（叶轮机 mixing plane 例：20 叶 18°/15 叶 24°）**逐 cell zone 设 repeats**；Detect Surfaces 自动判选（跨多流体区的 iso-surface 不被检测——**应在每个流体区内独立建切割面**）；Rotational（轴原点/方向、Angle；2D 只给原点、轴为 z 向）或 Translational（XYZ 平移量）；负数反向重复；Save 逐区设、Views 对话框 Display 显示、**Clear Repeats** 清除。**注意**：多周期区 3D 域只能重复 mesh/contour/vector（**pathlines 与 particle tracks 不能**）；与单元区关联的 iso/clip 面按该区周期重复、无关联面无法指定周期性；Scene 对话框的透明度**不作用于重复面**。

## 41.9 高级场景合成（pp. 4263–4272）

Scene Description 对话框（View → Graphics → **Compose...**）比 Scene 对话框更复杂——逐对象旋转/平移/缩放、改色与可见性；配 Display Properties、Transformations、Iso-Value、Pathline Attributes 对话框；显隐控制对做动画特别有用（逐个增删对象）。**不能控制 XY plot 与直方图显示**。**41.9.1 选对象**：Names 列表（含隐藏对象；多选 = 组操作；探针右键可直接选；Type 字段报 mesh/surface/contour/vector/path/text——多选显 Group）。**41.9.2 显示属性（Display...）**：Visibility——Visible 开关、Lighting（逐对象受光；等值线开光照则颜色与色标不完全一致）、Faces、**Outer Faces**（slit wall 双面显示，同 Front Faces Transparent）、Edges、Perimeter Edges、Feature Edges、Lines（迹线/线等值线/矢量）、Nodes——Apply 更新。**Colors**——Color 下拉 face-color/edge-color/line-color/node-color + RGB 滑块（面与边异色可同时看填充与网格线）；**Transparency**（face-color 下 0–100；0 不透 100 全透；软件 buffer 全平台可用、硬件 buffer 更高效——Display Options 里选；**透明面存图勿选 Vector 文件类型**）。**41.9.3 变换（Transform...）**：**Translate**（XYZ 距离；**非累积**——归零即回原位）；**Rotate By**（绕各轴角度，±范围；Rotate About 给自定义转心；非累积）；**Scale**（XYZ 同值防畸变；非累积——归 1 复原）；**Meridional**（子午视图；仅 3D、有转轴的工况，叶轮机尤佳——投影到恒定角坐标面、θ 取实体最小 (r,θ) 点）。**41.9.4 改等值**：选中 isosurface 或其上的对象 → **Iso-Value...** → Value 新值 → Apply——面上的等值线/矢量/迹线随之更新（做动画快照用）。**41.9.5 迹线属性**：选迹线 → **Pathlines...** → 改 **Max Steps** → Apply 重算重绘（动画推进用）。**41.9.6 删除对象**：Names 选中 → **Delete Geometry**（叠加失误时单独删、不影响场景其他对象；亦可临时隐而删）。**41.9.7 边界框**：**Frame Options...** → Bounding Frame 对话框——Frame Extents 选 **Domain**（全域）或 **Display**（仅显示部分）；Axes 组点白方块选要显示的包围平面（变红生效）、点棱边定测量标注位置；Display 预览、OK 保存；**勾 Scene Description 的 Draw Frame + Apply 使其出现在后续显示**（否则仅当前显示，除非开 Overlays）。包围面与标注出现在 Names 列表——可像其他对象一样改色/透明。

## 41.10 关键帧动画（pp. 4272–4279+）

基于静态关键帧（相机角度/缩放、光照、所显图形可变）由软件插值。**两法**：①**HSF/In Memory 关键帧**——Playback 对话框读 `.cxa`（**无需 case/data**；可存 **MP4 等视频**；缺点是须在求解前定义 HSF 动画或用 In Memory 存储）——Playback → Read... 选 cxa → Animation Sequences 选中 → **View Mode 选 Key Frames** → 后续同 Creating an Animation。②**当前 case/data 关键帧**——无需预存特殊文件（缺点：须全量 case+data；**视频只能存 MPEG**）。Results → Animations → Scene Animation → Edit... 打开 **Animate** 对话框：场景布置好定义一帧 → 改场景（移动/缩放/显隐/换色/换视图）再定义下一帧 → 软件平滑插值中间帧。解随时间的图形动画另用 Animation Definition（p. 3865）。**注意**：Animate 对话框的关键帧动画**与 iso-surfaces 不兼容**；**迹线关键帧动画仅支持非持久/"global" 版 Pathlines 对话框**（须开 Expose legacy non-persistent graphics）。
- **41.10.2.1 创建**：关键帧最多 **3000**；示例流程照录（31 帧动画、3 关键帧 = front 1 / side 16 / rear 31——用 Scene Description 与 Views 布景后设 Frame 号点 **Add**；**务必先改 Frame 号再 Add，否则覆盖上一关键帧**）；Keys 列表选中即预览；Delete / Delete All。
- **41.10.2.2 播放**：play / play reverse / Frame 滑块跳帧；Start/End Frame 播片段；**Increment** 快进快退（例：1–15、Increment 2 → 1,3,5,…,15）；Playback Mode——**Auto Repeat**（循环）/ **Auto Reverse**（往复）/ Play Once（默认）；stop（复杂场景有延迟）；逐帧±1。
- **41.10.2.3 保存**三式：**Key Frames**（动画文件 `.anm`——只含关键帧描述，**回放时须有引用的 case/data**；Write...）；**Picture Files**（每帧一图供 ImageMagick 等；Picture Options... 设参勿点其 Save...；Write... 时自动重放逐帧存）；**MPEG**（省盘但画质低；Ubuntu 不支持保存；**MPEG 不能读回 Fluent**）。
- **41.10.2.4 读取**：Read... 读 `.anm`（前置：当前 case/data 含所引用的面等信息）。
- **41.10.2.5 注意事项**：清单起于 p. 4279 末（续下批）。

## 41.11（续）直方图与 XY 绘图（pp. 4287–4301）

- **并行 Write 注意**：Solution XY Plot 勾 **Order Points**（按 x 升序排序）消除分区导致的绘图外观差异；导出文件可能含重复点——散点图可正确显示。
- **41.11.3 多数据源 XY 绘图**：Plot Data Sources 对话框（Results → Plots → Data Sources）——**Load...**（报告文件与 .xy 文件）、**Add XY Plot...**、**Add Report Plot...**；Curve Information 列表勾选数据集与轴分配、Remove 删曲线；**Change Legend Entry** 改图例名；Axes.../Curves...；Title/Legend Label/X-Y Axis Label；**Plot**；Remove Data Source。**注意：该对话框绘图恒为 SI 单位**。
- **41.11.4 边界 profile 绘图**：两选项——**Plot Profile Data**（Results → Plots → Profile Data → Set Up...；画 profile 文件**原始数据点**——Profile 选、Y/X Axis Function（x/y/z/r/time））与 **Plot Interpolated Data**（... → Interpolated Data → Set Up...；须先读 profile 并在边界条件对话框选用 profile 场、初始化后画**边界单元面插值**值——Zones 限已设 profile 的区、Y 为边界对话框中的参数名）。须有有效数据。
- **41.11.5 周向平均 XY 绘图**：TUI `plot/circum-avg-radial` 或 `plot/circum-avg-axial`——给平均变量名（回车列清单）、面名（**回车不列表面清单，用 Mesh Display 查**；2D 用 interior volume 建轴向/径向带——外部区表面会使 mass-weighted 平均为 0）、**带数（默认 5**——将面按径/轴向等距 iso-clip；坐标取自 Reference Values 任务页参考区转轴）、面积加权（默认）或质量加权；生成 `radial-bands`/`axial-bands` 新表面可复用。自定义外观：`plot/file-set/plot-to-file` 存数据 → Plot Data Sources 重绘 + Axes/Curves 对话框。
- **41.11.6 XY 文件格式**：`(title "...")` + `(labels "..." "...")` + 每曲线 `((xy/key/label "...") (xy/key/visible? #t) (xy/line/pattern "--") x y x y ...)`——Cortex 变量可省（导入实验数据示例照录）；导入后 Axes/Curves 定制。
- **41.11.7 残差绘图**：残差史 XY 图——横轴迭代数、纵轴对数残差；Residual Monitors 的 **Plot** 按钮。
- **41.11.8 直方图**：柱状图（或控制台打印）——横轴为所选量、纵轴为单元数百分比。Results → Plots → Histogram → Edit...：Histogram of 选量 → **Divisions**（默认 **10** 区间）→ Zones/Zone Types 选区 → Auto Range 关掉手动 Min/Max（Global Range 关掉按所选面）、**Add to Simulation Report** + Add to Report；Plot 显示 / Print 打印 / Compute 计算。
- **41.11.9 轴属性**（Axes 对话框，逐绘图类型独立）：X/Y 独立设——Axis Title 与字号；Number Format（float/exponential/general + Precision + Size）；**Log 刻度**（残差图 y 轴默认对数；对数下 Range 值为指数——1 到 10000 输 min 1 max 4）；关 **Automatic** 手动 Range（系列图统一坐标范围用）；Major/Minor Gridlines（颜色/Weight（1.0=1 像素）/间距——Major 可 Units 或 No. of Divisions、Minor 只能 divisions）。
- **41.11.10 曲线属性**（Curves 对话框，逐曲线 Curve # 从 0 计）：Line Style——Pattern（**blank = 无连线纯标记**；center/phantom 线型不显示示例）、Color、Weight（1.0=1 像素）；Marker Style——Symbol（blank = 无标记）、Color、Size（1.0 = 屏高 3.0%，"." 恒 1 像素）；**Sample 窗口预览**。

## 41.12 FFT 后处理（pp. 4301–4316）

瞬态时序数据的频谱分析（涡脱落主频、表面压力谱、湍动能谱）——傅里叶变换把时序数据分解为正弦/余弦和，Fluent 用 **FFT 算法**。
- **41.12.1 限制**：输入文件格式仅五种——Fluent report file、monitor、x-y file、Kirchhoff 信号 `*.ark`、FW-H 信号 `*.ard`；**假定输入等间隔且时间递增连续**；最低可分辨频率 = 1/T（T 总采样时长；更低频率混叠到高频）；最高可分辨频率 = 1/(2Δt)（Δt 采样间隔）。
- **41.12.2 窗函数**：离散 FFT 假设输入为周期信号单周期——首尾不重合产生大间断→高频混叠误差；**加窗**（输入 N 点序列 x_k 乘窗函数 w_k，Eqs 41.2–41.3）四选——**Hamming / Hanning / Bartlett / Blackman**（Eqs 41.4–41.7；保留大部分数据、只影响两端）。
- **41.12.3 FFT**：N 点周期采样的离散傅里叶变换对（Eqs 41.8/41.9）；k 从 0 到 N/2 对应正频率、N/2 到 N 为负频率、k=0 为零频；实际计算用 **prime-factor FFT 算法**（支持的数据点数表 Table 41.2 照录——39 到 720720 等素因子数）。
- **41.12.4 FFT 工具**：Fourier Transform 对话框（Results → Plots → FFT → Set Up...）；**enhanced interactive plots 的阈值回退不适用于 FFT 图**。
  - **加载数据**：**Load Input File...**（移除用 Free File Data）；**"on the fly" 声学信号**——Process Options 选 **Process File Data**（文件）或 **Process Receiver**（内存中接收器数据；FW-H 与 Kirchhoff 信号并存时取当前激活模型）；**Plot FFT** 显示频谱 +（开 Acoustics Analysis 时）按 Reference Acoustic Pressure 算总声压级 dB 打印控制台；输入 report file 含多报告定义时可指定 X/Y 轴变量。
  - **Plot/Modify Input Signal**：分析信号片段、查看 **Signal Statistics**（Min/Max/Mean/Variance/样本总数/Min Frequency——最细频率分辨率）、标题与轴标签；**Clip to Range + X Axis Range Min/Max** 截取片段；**Subtract Mean Value** 去均值；Set Defaults 复位。**频谱平滑（分段平均）**：长宽带噪声信号频谱有伪波动——勾 **Subdivide into Segments** 分成多段重叠段、逐段 FFT 后**对傅里叶幅值平方做算术平均**（保信号能量），代价是频率分辨率变粗；Segment Control 的 Control Method——**Samples**（每段样本数）或 **Frequency**（目标频率分辨率 Δf Hz，段长=1/Δf）；**Overlap** 重叠（窗口函数建议 ≥0.125、**一般推荐 0.5**）；hop size（相邻段起点样本距、最小 1）打印控制台；最终段长按支持样本数调整、实际信号长度与段数打印。
  - **输出定制**：**全部输出为正频率单边谱**。**Y Axis Function**——Power Spectral Density（PSD；详细谱单位为信号平方/Hz，Eq 41.10–41.11；倍频程分析为信号平方，Eq 41.12）、Magnitude（幅值，Eqs 41.13–41.14，含均值扣除）、Sound Pressure Level (dB)（Eq 41.15；参考声压默认 **2×10⁻⁵ Pa** 可改）、Sound Amplitude (dB)（Eq 41.16 幅值对数转换）、A/B/C-Weighted SPL（dB A/B/C——A 计权 <55 phon 最常用、B 55–85 phon 少用、C >85 phon 高强度；**仅 Octave/1/3-Octave Band 可用**；声学类函数均 dB 且需开 Acoustics Analysis）。**X Axis Function**——Frequency (Hz)（Eq 41.17）、Strouhal Number（Eq 41.18 无量纲化，参考长度/速度取自 Reference Values 任务页）、Fourier Mode（式 41.8/41.9 的索引 k）、Octave Band (Hz) 与 1/3-Octave Band (Hz)（频带表 Table 41.3 照录：16–16000 Hz 中心频率及 A/B/C 计权值）；Write FFT to File + Write FFT 存数据（开声学时同样打印总声压级）。**Window** 下拉选窗函数（默认 **None**）。Plot Title/Y/X Axis Label 自定。
- **41.13 累积力/力矩/系数绘图（p. 4316–4317）**：航空航天/汽车——力与力矩沿某方向（如车长）的累积分布，定位贡献大的区域。Cumulative Plot 对话框（Results → Plots → Cumulative Plot → New...）：Name；Options 四选——**Cumulative Force / Force Coefficient / Moments / Moment Coefficient**；**Direction**（切片面垂直方向）与 **Number of Divisions**（垂直该方向的切片数）；Force Direction 或 Moment Center + Moment Axis；（可选）**Compute from Force Statistics**（用平均值——需 Sampling Options 已开 Force Statistics）；Zones 选面 → **Save/Plot**。
- **41.14 瞬态后处理（pp. 4317–4322）**：求解结束后分析——补建漏定义的监视器/动画、比较不同时间步的等值线并生成差值图。**启用**：Transient Postprocessing ribbon 选项卡（**General 任务页须已选 Transient**）。**重要：不用于查看单步结果**（看单步就最后载入该时间步的 data 文件）。**功能**：**Timestep Selector**——选择参与报表绘图与动画的数据（**不是**选单步；单独评估 post 对象显示的恒为最后时间步的值）；**Transient Display**——相当于不存储的动画（Reverse/Play/Pause/Reset 控制；**要保存动画或绘图数据必须用 ribbon 的 Animation.../Monitor...**）；**Animation...**——基于所选时间步为 contours/vectors/scenes/plots 建动画；**Monitor...**——基于所选时间步建报告文件；**Compare Results...**——选 2 个时间步并排比较等值线 + 差值图。**41.14.2 创建瞬态动画五步**：Timestep Selector 选数据 → 建后处理对象（支持 Report Definition+File+Plot、Contour、Vector、Scene、XY Plot；**Scene 不得含不支持图形（如 Pathlines/Particle Tracks）否则不生成**）→ 逐对象建动画定义 → （可选）TUI `transient-post-processing/compute-and-clip-range` 把色标范围统一到全数据集 → ribbon Animation... 选对象 OK。**注意**：仪表板动画在图形窗口播放时基础窗与嵌入窗可能不同步——存成文件（MP4）后回放正确。**41.14.3 瞬态监视与报告**：逐量建 report definition（含 Report File/Plot）→ ribbon **Monitors...** 选要写的报告文件 OK；**Stop Writing Files** 停止。

**Ch.41 全章完成（pp. 4079–4324）。**

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 4079–4130（批次 111，2026-10-20，pypdf layout 模式提取）。
- 本段以界面流程为主；默认值（Feature Angle 20、Levels 100、URF 等）与弃用状态以 2026 R1 为准。
- Figures 41.1–41.36（示例图与对话框截图）为图形元素未摄取；p. 4118 的交叉引用原文为 "XREF" 占位照录。
- 相关页面：[[Fluent 表面与单元寄存器]]（表面类型）、[[Fluent GPU 求解器]]（GPU 后处理限制）。
