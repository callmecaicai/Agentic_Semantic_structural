---
name: templates-as-schema
description: 镜像契约 / conflict / decision 各有稳定 schema;schema 即合约,不是装饰。
metadata:
  kernel_rule: I
---

# 模板即模式

项目中重复出现的对象(conflict、decision、镜像契约、语义记录文件夹...)必须有稳定 schema。

---

## kernel 级模板

| 模板 | 位置 | 用途 |
|---|---|---|
| **mirror_contract** | [templates/mirror_contract.md](templates/mirror_contract.md) | 任意工件的镜像 doc;前述四件套的承载 |
| **semantic_record** | [templates/semantic_record/](templates/semantic_record/) | 任意一次发生的语义记录文件夹;输入/过程/输出/分析/回流 |
| **conflict** | [templates/conflict.md](templates/conflict.md) | conflicts 区的任意条目 |
| **decision** | [templates/decision.md](templates/decision.md) | ADR;一切转折点的留痕 |

domain adapter 可在此之上派生特化模板(例如 experiment、module_contract);但 kernel 模板不被废止。

---

## schema 的最小要求

每个模板必含:

1. **front-matter** —— 让审计能机器读取关键字段。
2. **必填段** —— body 中不可省略的段(标题、对象、结论)。
3. **可选段** —— 可省略但保留位置以提示作者。
4. **链接位** —— 指向相关 frame/field/trace 文档的具体位置。

---

## schema 即合约

- 不要把字段藏在自由文本里(例如把 covers 写在正文段落) —— 审计读不到。
- 不要把 free-form 段当 schema(例如"杂记") —— 失去模式,即失去可读性。
- 不要为单次任务破坏 schema —— 破坏一次,后续模板权威崩塌。

需要增字段时,在 ADR 里说明,然后改 kernel 模板。所有已存在的实例不强制回填,但新建必须用新 schema。

---

## 何时建一个新模板

只有当一个对象类型:
- 出现 ≥ 3 次,且
- 每次都需要同一组字段,且
- 字段足够稳定到值得固化

—— 才升级为新模板,放入 domain adapter 的 templates/。

否则用 free-form md + 链接到模板,等模式自然显现。

---

## 模板的演进

模板本身也演进。每次 kernel 模板变更,必须:

1. 在 decisions 写 ADR。
2. 旧实例不强制升级,但通过 front-matter 字段可识别 schema 版本。
3. 新建必须用新版。

参见 [frozen_vs_evolving.md](frozen_vs_evolving.md)。
