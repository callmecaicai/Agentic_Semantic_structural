# Reflux Journal

记录"证据 -> 理解"的每一次升级。

每行一次回流。当某次证据改变了项目对 frame、field 或某个工件的理解,在这里登记并指向相关更新。

---

## Format

```text
| date | source | what changed | updated docs | verdict |
```

verdict:

- `accepted`:解释已写入对应 doc。
- `pending`:证据已观察但解释未完成;本身就是 conflict。
- `rejected`:经过审视决定不更新理解,需说明原因。
- `superseded`:已被后续条目取代,保留供追溯。

---

## Entries

| date | source | what changed | updated docs | verdict |
|---|---|---|---|---|
| 2026-05-24 | 用户提出 agentic harness 的对偶结构 | 将"稳定对象 -> 固定镜像文档"与"一次发生 -> 增量语义记录文件夹"升级为 kernel 规则 | [kernel/semantic_duality.md](../../kernel/semantic_duality.md), [SKILL.md](../../SKILL.md), [domains/deep_learning/README.md](../../domains/deep_learning/README.md) | accepted |
| 2026-05-24 | 用户指出当前版本过于具体,违背第一性抽象目标 | 将元规则提升为 kernel,把深度学习规则收纳为 domain adapter | [SKILL.md](../../SKILL.md), [kernel/](../../kernel/), [domains/deep_learning/](../../domains/deep_learning/) | accepted |
| 2026-05-23 | SKILL v2 初始耦合机制 | 引入路径镜像、锚点、审计作为工件-文档耦合雏形;该版本被 kernel + adapter 结构取代 | [kernel/coupling_principle.md](../../kernel/coupling_principle.md), [domains/deep_learning/audit_coupling.py](../../domains/deep_learning/audit_coupling.py) | superseded |

---

## Pending Slots

verdict=pending 的条目即未回流的 conflict。pending 不应长期存在。

<!-- 示例:
| 2026-06-01 | source id | (待解释的证据) | (待更新) | pending |
-->
