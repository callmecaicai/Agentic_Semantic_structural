# Legacy Protocols (Deep Learning)

本目录存放 DL adapter 的旧版六个 protocol 文档。

它们已被 [../../../kernel/](../../../kernel/) 的 9 条元规则和 [../README.md](../README.md) 中的 DL 实例化替代,但作为详细规则参考保留(冻结,不修改)。

---

## 文件与新位置映射

| 旧 protocol | 主要新位置 | 关键细则保留 |
|---|---|---|
| 01_problem_alignment.md | [kernel/three_actions.md](../../../kernel/three_actions.md) 的 clarify 动作 | "显影/切断/展开/回流" 四个子动作仍适用 |
| 02_structure_design.md | [kernel/three_actions.md](../../../kernel/three_actions.md) 的 locate × frame→field | "分化/定位/约束/反噬/回流" 仍可作为结构设计 checklist |
| 03_project_semantic_field.md | [kernel/path_authority.md](../../../kernel/path_authority.md) + [../path_table.md](../path_table.md) | 三类上下文(宪法/过程/证据)已嵌入 kernel/three_contexts.md |
| 04_model_research_engineering.md | [../README.md](../README.md) + [../pipeline_contracts.md](../pipeline_contracts.md) | W&B、Sample Contract、模块变化分级、探针清单等 DL 具体规则保留在此 |
| 05_external_reference.md | 仍生效,external/ 的 SOURCE.md / ANALYSIS.md 规则不变 | 整篇仍是 external/ 的 authoritative 规则 |
| 06_document_memory.md | [kernel/reflux_mechanism.md](../../../kernel/reflux_mechanism.md) + [kernel/conflict_mechanism.md](../../../kernel/conflict_mechanism.md) | "实验冻结、核心演进"原则继承到 kernel/frozen_vs_evolving.md |

---

## 何时查阅

- 写 module_contract 时,如果 pipeline 边界细节不确定 → 查 04。
- 引入 external 项目时 → 查 05。
- 写 ADR 或处理 frame/field 冲突时 → 查 02。
- 任务被推回为模糊状态 → 查 01。
- 不知道某 doc 算什么类型 → 查 06。

---

## 不修改

本目录的文件冻结,不再更新。
如发现旧规则与新版冲突,在 `docs/trace/decisions/` 写 ADR 说明取舍,而不是修改 legacy 文件。
