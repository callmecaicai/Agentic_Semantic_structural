# Path Table (Deep Learning Adapter)

本表是 [kernel/path_authority.md](../../kernel/path_authority.md) 在深度学习工作中的实例化。

任一 agent 进入 DL 项目时,通过本表理解每条路径的责任和约束。

---

## 路径权威表

| 路径 | 身份 | 权威等级 | 生命周期 | 写权限 | 主要读者 |
|---|---|---|---|---|---|
| `src/` | 稳定能力代码 | 当前事实 | 持续演进 | 开发者 | 所有 agent + 训练 |
| `configs/` | 实验条件 | 当前实验定义 | 短期 + 历史归档 | 开发者 | 训练脚本、scripts/ |
| `data/` | 输入事实 | 不可变 | 长期,版本化 | 数据负责人 | 训练、评估 |
| `scripts/` | 动作入口 | 工具 | 持续演进 | 开发者 | 用户、CI |
| `tests/` | 结构验证 | 行为约束 | 与 src/ 同步 | 开发者 | CI、审计 |
| `probes/` | 沉默失败显式化 | 诊断 | 持续演进 | 开发者 | 用户调试 |
| `docs/frame/` | 当前任务定义 | 当前意图 | 持续演进 | 用户裁决 | 所有 agent |
| `docs/field/` | 项目结构契约 | 当前理解 | 持续演进 | 用户裁决 + agent locate | 所有 agent |
| `docs/field/module_contracts/` | 镜像 src 的模块文档 | 当前理解 | 与 src/ 同步 | agent locate + 用户 | agent、审计 |
| `docs/trace/` | 运行记录 + 解释 | 历史证据 + 当前解释 | 追加为主 | agent reflux + 用户 | 所有 agent |
| `docs/trace/decisions/` | ADR(决策) | 决策权威 | 冻结,可标记 superseded | 用户 + agent 提议 | 所有 agent |
| `docs/trace/failures/` | 已知失败模式 | 警示 | 追加 | agent + 用户 | 所有 agent |
| `docs/conflicts/` | 未解决冲突 | 待裁决 | 直到解决 | 审计脚本 + 用户 | 所有 agent |
| `docs/experiments/` | 训练事件语义记录文件夹 | 历史证据 + 解释 | 每次训练新增,完成后冻结 | 训练入口 + agent reflux | 所有 agent |
| `runs/` | 运行证据 | 历史事实 | 不可改 | 训练系统 | 分析、reflux |
| `checkpoints/` | 权重资产 | 资产 | 长期,按版本 | 训练系统 | 推理、评估 |
| `external/` | 外部参考 | 参考世界,非本项目事实 | 按版本冻结 | 引入时,不再改源码 | 学习、对照 |
| `pulse.md` | 当前状态快照 | 临时 | 覆盖式 | agent 开局检查 | 进入项目第一读 |
| `SKILL.md` | 路由表 | 协作规则 | 稳定 | 用户裁决 | 所有 agent |

---

## 与三类上下文的对应

按 [kernel/three_contexts.md](../../kernel/three_contexts.md):

- **宪法型**:`docs/frame/` + `docs/field/` 核心契约 + `SKILL.md`
- **过程型**:`docs/trace/reflux_journal.md`、`docs/field/module_contracts/`、`pulse.md`
- **证据型**:`runs/`、W&B、`docs/experiments/<event>/output.md`、`checkpoints/`

`docs/experiments/<event>/analysis.md` 与 `reflux.md` 是证据到理解的解释层;完成后冻结,若改变当前理解,通过 reflux 升级到 frame/field。

---

## external/

`external/` 是外部参考世界,不承载本项目运行事实。

详细规则见 [protocols_legacy/05_external_reference.md](protocols_legacy/05_external_reference.md)。

简短:
- 每个外部项目必须有 `SOURCE.md`(origin / version / license / purpose)。
- 每个重要外部项目应有 `ANALYSIS.md`。
- 不让本项目 `src/` 直接 import `external/`;通过 adapter 重新表达。
