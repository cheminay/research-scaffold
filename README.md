# research-scaffold —— 学术研究项目脚手架插件

面向 Codex、ZCode 等编码代理的**多会话学术研究协作框架**。一条命令把普通仓库改造成受纪律约束的研究项目：事实纪律防幻觉、上下文分层防污染、目标三层锚定防漂移、脚本关卡防偷懒。

## 插件内容

| 组件 | 说明 |
|---|---|
| 技能 `research-scaffold` | 按模板初始化脚手架，并引导冷启动基线定稿 |
| 命令 `/research-init` | 显式触发同一初始化流程 |
| 模板（7 件） | `AGENTS.md`、`GOAL.md`、`STATE.md`、`prompts/ROLE-{MAIN,SUBTASK,DECISION}.md`、`scripts/kb_check.py` |

## 安装

### ZCode

1. **插件市场 → 添加 → 添加插件市场**，粘贴本仓库地址（GitHub URL 或本地克隆目录）。
2. 在 **个人 → research-scaffold** 中找到「学术研究脚手架」，点击**安装**。
3. 新建任务，在输入框选择该技能（或输入 `/research-init`）即可使用。

仓库根目录的 `.claude-plugin/marketplace.json` 为分发清单；
`plugins/marketplace.json` 为本地开发用清单，两者均可作为市场根目录添加。

## 使用

在目标项目目录新建任务并发送：

> 初始化研究项目脚手架

或使用 `/research-init`（可附目标目录路径）。完成后脚手架包含：

```
project/
├── AGENTS.md            # 全局会话纪律（启动协议/事实纪律/上下文纪律/DoD/红线）
├── GOAL.md              # 研究目标宪章（北极星句的唯一定义处）
├── STATE.md             # 唯一权威状态（仅主会话可写）
├── prompts/             # 主会话 / 子课题会话 / 决策会话 角色提示词
├── scripts/kb_check.py  # 验收关卡（宪章指纹/任务卡版本/产出元数据/git 状态）
├── kb/                  # 知识库（inbox + tools/snippets/domain/envs/lessons/deadends/decisions）
├── subtasks/            # 子课题任务卡与完成报告
└── outputs/             # 产出物
```

随后按冷启动引导完成：起草**北极星句**（≤60 字）→ 填 GOAL.md 全部字段 → 指纹两遍定稿（模板内注释已说明顺序）→ `git commit -m "goal: baseline v1.0"`。

## 日常循环

- 主会话（常驻）：「分解本轮」→ 产出各 `TASK.md`
- 子会话（≤3 并行）：「执行 SR-xx」→ 完成后回主会话
- 主会话验收：`python scripts/kb_check.py SR-xx` 绿灯 + rubric 逐条核对 + 目标对齐三问 → 解锁下游
- 遇升级触发器 → 开决策会话裁决 → 结论入 `kb/decisions/`

参数速查：产出上限 5000字/500行 · 决策点 ≤3 · B级抽检 20% · 验证重试 2 次 · 轮换阈值 20 轮 · 重锚阈值 15 轮 · 并行 ≤3 · 漂移审计每 5 决策一次。

## 兼容性

- 脚手架仓库以 `AGENTS.md` 承载纪律，**Codex 与 ZCode 均原生识别**，开箱即用；
- 其他工具若使用不同的项目级指令文件名（如 Claude Code 的 `CLAUDE.md`），初始化流程会创建内容一致的副本。

## 已知留白

未内置数据脱敏规则——若涉及未发表数据接入外部 MCP，请先在 `AGENTS.md` 事实纪律节补充脱敏规则。
