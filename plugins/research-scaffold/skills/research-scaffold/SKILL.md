---
name: research-scaffold
description: 在指定目录初始化学术研究项目脚手架（多会话研究协作框架），落盘 AGENTS.md 全局会话纪律（委派优先、任务路由、子智能体回执纪律、上下文长度硬控制）、GOAL.md 目标宪章（北极星句）、STATE.md 权威状态、prompts/ 三角色提示词（执行类请求自动分解派发子智能体，回执只收摘要）、kb/ 知识库与 scripts/kb_check.py 验收关卡，并引导冷启动基线定稿。当用户要求搭建、初始化学术研究/科研协作项目、研究脚手架，或使用 /research-init 命令时使用；已初始化仓库的日常运行以仓库内 AGENTS.md 为准，不由本技能接管。
---

# 学术研究项目脚手架

把一个普通仓库改造成受纪律约束的多会话研究项目。全部模板在本技能目录的
`templates/` 下，**逐字复制，不得改写措辞**（这些是行为约束提示词，措辞即语义）。

## 目标结构

```
project/
├── AGENTS.md            # 全局会话纪律（Codex/ZCode 等均识别）
├── GOAL.md              # 研究目标宪章（唯一定义处）
├── STATE.md             # 唯一权威状态（仅主会话可写）
├── prompts/
│   ├── ROLE-MAIN.md     # 主会话：调度、验收与目标守卫
│   ├── ROLE-SUBTASK.md  # 子课题会话：研究与执行
│   └── ROLE-DECISION.md # 临时决策会话
├── scripts/
│   └── kb_check.py      # 验收关卡（赋可执行权限）
├── kb/
│   ├── inbox/  tools/  snippets/  domain/
│   ├── envs/  lessons/  deadends/  decisions/   （各放 .gitkeep）
├── subtasks/
└── outputs/
```

## 初始化步骤（按序执行）

1. 确认目标项目目录（默认当前工作目录；若不确定，先问用户）。
2. 落盘前冲突检查：若目标目录已存在 AGENTS.md / GOAL.md / STATE.md /
   prompts/ROLE-*.md / scripts/kb_check.py 中的任何一个，停止并向用户
   报告差异，由用户决定覆盖、跳过该文件或另选目录——禁止静默覆盖。
3. 将 `templates/` 下的 7 个文件按上述结构复制进目标目录：
   `AGENTS.md`、`GOAL.md`、`STATE.md`、`prompts/ROLE-*.md`（3 个）、
   `scripts/kb_check.py`。逐字复制，禁止"顺手优化"。
4. `chmod +x scripts/kb_check.py`。
5. 创建 `kb/` 下 8 个子目录（inbox、tools、snippets、domain、envs、
   lessons、deadends、decisions），各放一个 `.gitkeep`；
   创建空的 `subtasks/` 与 `outputs/`。
6. 若目标目录不是 git 仓库：`git init`。提交脚手架：全新仓库用
   `git add -A && git commit -m "init: 研究项目脚手架"`；已有提交
   历史的仓库只 `git add` 本脚手架新增的文件再提交，禁止卷入用户
   其他未提交变更。
7. 运行 `python3 scripts/kb_check.py --print-fingerprint` 确认脚本可运行。
8. ZCode 与 Codex 均原生识别仓库根目录的 AGENTS.md，无需副本；仅当
   目标工具的项目级指令文件名不同（如 Claude Code 用 CLAUDE.md）时，
   创建内容一致的对应名称副本。
9. 向用户报告脚手架就绪，并引导进入冷启动第 2 步（见下）。

## 冷启动（初始化之后，引导用户完成）

1. 请用户亲自起草**北极星句**（≤60 字。写不进去说明目标该拆成
   "主目标 + 约束"两栏，这是试金石）。
2. 用户确认后填写 GOAL.md 全部字段（范围边界/成功判据/非目标/目标史）。
3. 基线定稿（注意顺序，指纹是自引用，必须算两次）：
   a. 填好 GOAL.md 后运行 `python3 scripts/kb_check.py --print-fingerprint`，
      将得到的指纹填入 GOAL.md 头部 `fingerprint:` 行；
   b. 再次运行同一命令得到新指纹，写入 STATE.md 的 `goal_fingerprint:`
      （kb_check 的 G1 关卡只比对 STATE.md 与 GOAL.md 当前内容）；
   c. `git commit -m "goal: baseline v1.0"`。
   此步完成前 G1 检查会红，属预期。
4. 之后进入日常循环：主会话讨论方案 → 分解 → 拿一个 1–2 小时量级的
   真实小课题（如"为某批 SMILES 建标准化流水线"）走完整闭环 → 首轮复盘调参。

## 日常循环速查

- 用户提出执行类请求 → 主会话当场分解为 TASK.md 并**立即派发**
  （无需"分解本轮"口令；边界内免逐次确认，无子智能体工具时输出
  派发单请用户开新会话）；禁止在会话内直接执行
- 主会话（常驻）："分解本轮" → 批量产出本轮各 TASK.md → 逐个
  **主动用子智能体工具派发执行**（默认路径，≤3 并行，回执只收
  ≤20 行摘要）
- 子课题执行中同样委派优先：批量/检索/重复验证类工作由子会话
  派发子智能体（并行 ≤2，回执 ≤20 行，回收后亲自核对）
- 手动模式（仅用户明确要求时）：另开终端子会话 "执行 SR-07" →
  完成后回主会话
- 主会话："验收 SR-07" → kb_check + rubric + 目标对齐三问 → 解锁下游
- 遇 ESCALATION → 开决策会话，用户裁决 → 结论入 kb/decisions/
- 主会话上下文过半即瘦身、约20轮即建议轮换 → 同意 → 落盘摘要 →
  开新主会话

参数速查：产出上限 5000字/500行 · 决策点 ≤3 · B级抽检 20% ·
验证重试 2 次 · 轮换阈值 20 轮 · 重锚阈值 15 轮 · 主会话派发并行 ≤3 ·
子课题内派发并行 ≤2 · 回执 ≤20 行 · 上下文 40% 瘦身 / 50% 轮换 ·
派发失败重试 ≤2 次 · 漂移审计每 5 决策一次

## 与已初始化仓库的关系

本技能只负责初始化与冷启动引导。项目一旦初始化，日常运行（角色判定、
验收、再基线等）以仓库内的 AGENTS.md 与 prompts/ROLE-*.md 为准；若
本技能文本与仓库文件不一致，以仓库为准（仓库可能已按流程再基线，
本技能模板停留在初始版本）。

## 已知留白

套件未内置数据脱敏规则——若涉及未发表数据接入外部 MCP，
在 AGENTS.md 事实纪律节补一条脱敏规则后再接入。

后续增强（脚手架跑顺后再追加，本插件暂不实现）：sync_check.py（git
审计产出↔KB 同步）、工具 canary 体系、kb_harvest.py（环境快照自动化）。
