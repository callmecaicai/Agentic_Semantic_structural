# Agentic Semantic Structural

一个面向人和 AI agent 长期协作的轻量语义 harness。

它不是全自动流程管控系统,而是给项目提供清晰的协作工作台:

```text
.agentic/   # 控制层: schema, templates, light audit
semantic/   # 语义层: frame, field, records, trace, conflicts
workspace/  # 执行层: code, configs, scripts, runs, tests
```

核心目标:

```text
stable object  <-> fixed mirror document
event instance <-> semantic record folder
```

- 稳定对象:代码模块、prompt 模块、论文 section、workflow 节点、训练单元等,对应唯一镜像文档。
- 一次发生:训练运行、agent 任务、论文阅读 session、写作推进、计划复盘等,对应一个增量语义记录文件夹。

路径承担语义,schema 声明语义,audit 只做轻量结构检查。复杂判断保留给人和 agent。

---

## 仓库结构

```text
.
├── SKILL.md              # agent 快速入口
├── scripts/harness.py    # 轻量 Python CLI
├── templates/            # mirror / conflict / event record 模板
├── references/           # 原则、工作流、架构、目标检测案例
├── agents/openai.yaml    # agent UI 元数据
├── tests/test1..test5    # 五个实践场景
├── README.md
├── .gitattributes
└── .gitignore
```

旧版 kernel / domains / lite / docs 已移除。这个仓库现在只保留最终版本。

---

## 快速使用

Linux/macOS:

```bash
python3 scripts/harness.py init --root <project-root>
python3 scripts/harness.py new-artifact --root <project-root> workspace/src/foo.py
python3 scripts/harness.py accept-mirror --root <project-root> workspace/src/foo.py
python3 scripts/harness.py new-event --root <project-root> experiment --id exp001 --slug baseline
python3 scripts/harness.py audit --root <project-root>
python3 scripts/harness.py reflux-check --root <project-root>
```

脚本带 shebang 和可执行位,clone 后也可以:

```bash
./scripts/harness.py init --root <project-root>
```

Windows PowerShell:

```powershell
python scripts/harness.py init --root <project-root>
```

---

## CLI 职责

CLI 很小,只做高频、可机械化的事:

```text
init           初始化 .agentic / semantic / workspace
pulse          读取或创建当前状态快照
new-artifact   为稳定对象创建 mirror doc
accept-mirror  人或 agent 审阅后接受当前 artifact hash
new-event      为一次发生创建 semantic record folder
audit          检查结构性断裂
reflux-check   列出 pending reflux
```

重要原则:

- pending mirror review 是正常工作状态,不是 conflict。
- pending reflux 是正常解释等待,不是自动 conflict。
- 只有结构性断裂才写入 `semantic/conflicts/`。
- harness 不替代 agent 调研、用户判断、文档重构。

---

## 五个实践场景

[tests/](tests/) 中保留了五个实际跑过的场景:

```text
test1 正常路径: mirror accepted + event accepted -> audit clean
test2 缺镜像: uncovered-artifact conflict
test3 代码漂移: artifact-vs-doc conflict
test4 事件记录破损: incomplete-record + bad folder conflict, pending reflux 仅报告
test5 非代码稳定对象: prompt mirror + agent_task event, pending reflux 仅报告
```

这些测试不是单元测试,而是给未来 agent 看的真实使用样本。

---

## 最高规则

1. 控制层、语义层、执行层分开。
2. stable object 有固定 mirror doc。
3. event instance 有增量 semantic record folder。
4. 路径表达语义,schema 声明语义,audit 检查结构现实。
5. 证据冻结,理解演进,决策解释转折。
6. 工具保持轻,判断交给人和 agent。
7. 不静默修复 artifact、document、intent、evidence 之间的不一致。

---

## 安全说明

[.gitignore](.gitignore) 排除了本地 agent 状态、密钥、运行产物和个人笔记:

```text
.claude/
自我剖析/
.env*
runs/
checkpoints/
wandb/
logs/
```
