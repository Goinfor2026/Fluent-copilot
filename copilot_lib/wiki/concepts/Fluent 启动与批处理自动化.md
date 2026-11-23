---
type: concept
created: 2026-10-15
updated: 2026-10-15
tags:
  - Ansys Fluent
  - automation
  - command-line
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 启动与批处理自动化

## 摘要

Fluent User's Guide 2026 R1 记载了跨平台启动参数、Journal 启动方式和批处理行为。自动化时要明确求解器维度/精度、图形模式、输入 Journal、输出记录及错误退出策略，并区分 Windows 和 Linux 的差异。

## 启动选项

- Linux 可用 `fluent 2d`、`3d`、`2ddp`、`3ddp` 指定二维/三维与单/双精度；例如 `fluent 3d -t4` 指定 4 个进程。网格模式可用 `-meshing`；网格进程数用 `-tmN`，与求解进程数 `-tN` 分开指定（PDF p. 198）。具体可用参数需以目标平台和安装版本为准。
- `-i <journal>` 在启动时读取 Journal；`-case <path>` 读取 case，可附 `-data` 读取同目录同基名 data 文件（PDF pp. 199–205）。
- `-g` 无 GUI 且无图形；`-gr` 无图形；`-gu` 无 GUI 但可显示图形，且显示对象不能交互（PDF p. 204）。这几个模式不可互换，选择前需确认 Journal 是否要生成图像。
- `-sifile=<name>.txt` 用于启动 Fluent 并启动 PyFluent 所用的服务器（PDF p. 202）。若涉及 gRPC 远程连接，指南另列允许远程主机、TLS 证书目录和 insecure mode 选项；指南明确不建议使用 insecure mode（PDF p. 202）。网络暴露与证书配置应按组织安全要求设置。

## 批处理与错误处理

- Linux 后台执行可使用 `-g` 配合标准输入/输出重定向；也可用 `-g -i <journal>` 并把输出重定向到日志（PDF pp. 212–213）。禁用 GUI 时，输入文件应使用 TUI 文本命令。指南示例通过 Journal 读取 case、初始化、分段迭代并写 data。
- Windows 指南列出 `-g -i journal`、`-wait -i journal` 和 `-hidden -i journal` 等形式；在 DOS 批处理或脚本需要等待 Fluent 完成时使用 `-wait`。Windows 后台运行若要留 transcript，Journal 需显式启动 transcript（PDF pp. 213–214）。这些选项含义受平台影响，调用方式要在目标 Windows 版本验证。
- Batch Options 可控制文件覆盖确认、隐藏问题对话框及出错时退出。指南记载启用 Exit on Error 时，正常结束返回 0，文本命令错误/类型错误返回 1，许可错误返回 2；Windows 下需使用 `-wait`。无效文本命令的行为有专门说明，不能简单假定每种命令错误都会立即结束进程（PDF pp. 214–215）。
- Batch Options 仅对当前 Fluent 会话有效，不会保存进 case 文件。因此可复用的自动化 Journal 应显式设置所需批处理选项（PDF p. 215）。

## 限制与适用条件

此页只归纳启动和批处理章节，不构成某台机器、调度器或 Fluent 安装环境的完整启动脚本。并行、调度器、图形驱动和许可证选项有平台限制；使用前对照来源页面和实际 `fluent -help` 输出。关于 Journal 命令本身的语法与菜单路径，应继续读取 Part III 的 Journal/TUI 章节。

## Launcher、工作区与启动配置

- Fluent Launcher 可从命令行（不带参数）、Windows 开始菜单/桌面启动，也可由 Workbench 打开。Launcher 支持 Meshing、Solution、Aero、Icing、Polyflow 等工作区；可用工作区取决于安装与许可证。选择 case、case+data、mesh 或 journal 可决定启动时加载的对象；选择最近的 case 只保证加载 case，不应假设同目录 data 会自动载入（PDF pp. 186–190）。
- Case File Info 可查看保存版本、精度、维度以及单元/面数量。Launcher 的工作目录和部分选项会保留到下次会话。Meshing 默认双精度；Solution 默认单精度。指南指出，尺度差异很大、狭窄连接管内压差、强导热率比/高长宽比共轭传热，或 PBM 矩跨越多个数量级时，双精度可能有益；这不是所有算例都必须双精度的要求（pp. 188–192）。
- Launcher 的 General Options 可启用仅前/后处理模式；可设置 Fluent 根目录、读取网格后显示网格、批处理提交模式、ACT，以及启动 Web Server。显示网格选项仅对 volume mesh 生效，显示边界而非内部区域。批处理图形模式中，Only Graphics 使用 `-gu`，No GUI No Graphics 使用 `-g`，Hidden Mode 使用 `-hidden`；应按是否需要绘图、交互和求解性能选择（pp. 190–192）。
- Remote gRPC Host 需要相应证书配置；指南不建议 insecure mode，并提醒远程访问可能控制机器和数据。仅在可信网络与合适安全配置下启用（p. 192）。Windows 区域设置下，小数分隔符应为句点；逗号可能导致其后数字被忽略。Windows UNC 路径不能直接设为工作目录，需映射为驱动器（pp. 189、192）。
- Launcher 的并行设置区分 Meshing 与 Solution 进程数；在 Linux Intel MPI 下切换工作区可能额外启动进程，且 Solution 进程数应不少于 Meshing 进程数。Remote 选项可从 Windows 界面提交到 Linux 集群，调度器类型包括 Microsoft Job Scheduler、LSF、SGE、PBS、Slurm；部分 UDF 编译环境选项仅适用于 Windows（pp. 193–196）。
- Windows 命令行可用 `fluent 2d`、`3d`、`2ddp`、`3ddp` 选择维度/精度；`-tN` 设置求解进程数，`-meshing` 进入网格模式，`-tmN` 设置网格进程数。Windows 下从 Meshing 切换到 Solution 时不能再更改进程数（p. 197）。

## 并行、调度器与执行命令

- 指南列出平台相关的并行启动选项，包括 CPU/GPU 选择、主机列表、MPI、网络互连、进程绑定/亲和性和异步启动等；Windows 与 Linux 的支持范围和写法不同。`-post` 用于仅前/后处理；`-sifile` 可启动 PyFluent server。应按安装平台核对该版命令行帮助，不要将平台专属标志直接移植（PDF pp. 206–207）。
- Linux 集群可通过 `-scheduler={lsf,pbs,sge,slurm}` 选择调度器，并可配置队列、节点、账户、每节点进程数/GPU 数、调度器附加参数及自定义提交脚本。部分参数只对特定调度器或 tight-coupled 运行方式有效；例如 exclusive 默认行为仅适用于指南注明的 Slurm/SGE 情形。使用调度器参数前应先确认集群策略（pp. 208–209）。
- `-command="<TUI command>"` 可在启动时执行完整命令；若同时使用 `-i`，这些命令先于 Journal 执行，且最多接受 10 个选项。适合明确的启动准备步骤，但命令次序会影响后续 Journal 的状态（p. 209）。

## 运行检查点与清理

- 运行中保存检查点可使用调度器的原生机制，或通过工作目录中的触发文件：Linux 创建 `check-fluent`、Windows 创建 `check-fluent.txt` 会请求保存并继续；`exit-fluent` / `exit-fluent.txt` 会请求保存并退出。多个会话共用目录时，保存触发可能作用于多个会话；退出文件可用 PID 指定目标会话。PID 可从 transcript 文件名或操作系统工具获取（PDF p. 216）。
- 检查点数据文件带迭代编号。非定常计算可用 `(ckpt/time-step? #t)` 将检查点放在时间步末尾；默认 `#f` 表示迭代末尾。指南不建议在 Workbench 中使用该独立会话检查点机制；Workbench 场景应使用 Interrupt（p. 217）。
- Fluent 会在工作目录创建清理脚本；无写权限时可能放在用户主目录。Linux 可运行对应 `cleanup-fluent-...` 脚本，Windows 使用生成的批处理脚本。正常退出时脚本自动删除，异常残留时可手动清理。若 Windows 会话挂起且需要完整 transcript，指南建议从 DOS 使用 `taskkill`，而非任务管理器（p. 218）。退出 GUI 时会提示保存尚未写出的 case/data（p. 218）。

## 证据与适用条件

来源：[[Ansys Fluent Users Guide 2026 R1]]。PDF pp. 186–197（Launcher 与 Windows 启动）、pp. 198–205（启动参数与 PyFluent 服务）、pp. 206–209（并行/调度器选项）、pp. 210–218（后台执行、批处理、检查点与清理）。

## 关联页面

- [[CFD 仿真工作流与验证]]
- [[Ansys Fluent Users Guide 2026 R1]]
- [[index]]
