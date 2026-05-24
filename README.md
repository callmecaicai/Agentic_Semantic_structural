# Agentic Semantic Structural

一个面向长期 AI 协作项目的结构主义语义 harness。

它不是普通的项目模板,而是一套让 agent 在多轮、多任务、多项目中保持结构一致性的协作规范:

```text
frame     = 当前意图
field     = 当前结构
trace     = 历史证据与解释
conflicts = 未解决的不一致
```

核心目标:让 Markdown 语义系统和可执行工程系统并行运转、相互校验、可持续回流。

---

## 核心思想

本仓库维护两组对偶结构:

```text
stable object  <-> fixed mirror document
event instance <-> semantic record folder
```

也就是:

- 稳定对象:代码模块、prompt 模块、论文 section、workflow 节点、训练单元等,对应唯一镜像文档。
- 一次发生:训练运行、agent 任务、论文阅读 session、写作推进、计划复盘等,对应一个增量语义记录文件夹。

路径不是收纳空间,路径承担语义。校验闭环是:

```text
path -> schema -> new-artifact/new-event -> audit -> conflict -> reflux
```

发现不一致时不静默修复,先记录 conflict,再由用户或明确决策裁决。

---

## 仓库结构

```text
.
├── SKILL.md                    # 完整版入口 skill
├── kernel/                     # 抽象元规则
├── domains/                    # 领域 adapter
│   └── deep_learning/          # 深度学习实验工程 adapter
├── docs/                       # frame / trace / conflicts 记录
├── structural-kernel-lite/     # 十分之一体积的精简 skill
├── pulse.md                    # 当前状态快照
└── .gitignore
```

---

## 两套规范

### 完整包

入口:[SKILL.md](SKILL.md)

适合沉淀完整方法论、扩展 adapter、维护复杂长期项目。

核心 kernel:

- [three_actions.md](kernel/three_actions.md):`clarify / locate / reflux`
- [three_contexts.md](kernel/three_contexts.md):宪法型 / 过程型 / 证据型
- [path_authority.md](kernel/path_authority.md):路径权威
- [coupling_principle.md](kernel/coupling_principle.md):工件与镜像文档耦合
- [semantic_duality.md](kernel/semantic_duality.md):稳定对象与事件实例的语义对偶
- [conflict_mechanism.md](kernel/conflict_mechanism.md):冲突显式化
- [reflux_mechanism.md](kernel/reflux_mechanism.md):证据回流

### 精简包

入口:[structural-kernel-lite/SKILL.md](structural-kernel-lite/SKILL.md)

适合高频加载、迁移到其他项目、快速交给 agent 使用。它约为完整核心文档集的十分之一,但保留核心操作循环。

---

## 使用方式

进入一个项目时,先写或读取五行 pulse:

```text
任务: <当前真问题和成功条件>
位置: <当前对象/路径>
最近: <最近相关 trace,无则 none>
冲突: <open conflict,无则 none>
动作: <clarify | locate | reflux> 在 <frame | field | trace>
```

然后按优先级选择动作:

```text
clarify > reflux > locate
```

- `clarify`:任务对象、目标、成功标准、失败下界不清楚时使用。
- `reflux`:已有证据尚未升级为理解时使用。
- `locate`:新增或修改稳定对象 / 一次事件时使用。

---

## 深度学习 adapter

深度学习实验工程规则在 [domains/deep_learning/](domains/deep_learning/)。

推荐模式:

```text
src/models/backbones/resnet.py
  <-> docs/field/module_contracts/models/backbones/resnet.md

一次训练运行
  <-> docs/experiments/YYYY-MM-DD_<exp_id>_<slug>/
```

每次训练新增实验语义文件夹;稳定组件只维护唯一镜像文档。

审计脚本:

```bash
python domains/deep_learning/audit_coupling.py --no-conflicts
```

---

## 适用场景

- 深度学习实验工程
- 目标检测 baseline 管理
- 论文阅读与攻坚
- 论文写作推进
- 生活训练计划
- 长期计划管理
- 任意需要持续记录、持续解释、持续回流的 agentic 项目

---

## 最高规则

1. frame / field / trace / conflicts 必须分开。
2. 稳定对象必须有固定镜像文档。
3. 一次发生必须有增量语义记录文件夹。
4. 路径表达语义,schema 声明语义,audit 检查现实。
5. 证据冻结,理解演进,决策解释转折。
6. 不静默修复 artifact、document、intent、evidence 之间的不一致。

---

## 安全说明

本仓库的 [.gitignore](.gitignore) 已排除本地 agent 状态、密钥、运行产物和个人笔记:

```text
.claude/
自我剖析/
.env*
runs/
checkpoints/
wandb/
logs/
```
