# Decisions

存放项目决策记录(ADR: Architecture / Approach / Adapter Decision Record)。

每个决策一个文件,使用 [../../../kernel/templates/decision.md](../../../kernel/templates/decision.md)。

命名:`NNN_short_decision_name.md`,NNN 从 001 递增。

---

## Status

- `proposed`:已提出但未执行。
- `accepted`:已执行,生效中。
- `superseded`:已被后续决策替代,保留供追溯。

被 superseded 的决策不删除,只标记并在 front-matter 中指向取代它的 ADR。

---

## 何时写 ADR

- 修改 kernel 规则或模板。
- 新建、合并、拆分 domain adapter。
- 修改路径权威、耦合审计或 conflict 类型。
- 选择一种长期会影响项目推进方式的结构。
- reflux 产生了多个可选解释,并需要裁决采用哪一个。
- 以后回头会想知道"为什么当时这么选"。

---

## 不写 ADR

- 局部措辞或格式修正。
- 单次任务内的小调整。
- 已在 reflux_journal 中充分记录且没有备选项的事实升级。
