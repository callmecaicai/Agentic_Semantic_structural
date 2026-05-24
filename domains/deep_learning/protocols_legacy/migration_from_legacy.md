# Migration from Legacy

本文档说明旧版六个 protocol 如何映射到当前 kernel + DL adapter 的结构。

---

## 两段迁移

项目经历过两次迁移:

1. **第一次**(旧 → SKILL v2):六个 protocol → 三动作 × 三层 + 耦合协议(集中在 SKILL.md + docs/field/coupling_protocol.md)。
2. **第二次**(SKILL v2 → kernel + adapter):把抽象元规则提取到 [../../../kernel/](../../../kernel/),把 DL 具体内容收纳为本 adapter。

本文档主要记录第一次,因为它的概念映射对未来 adapter 仍有参考价值。

---

## 概念对应(第一次迁移)

| 旧概念 | 新概念 |
|---|---|
| 状态路由器(6 个 state) | 三动作 × 三层 + 路由表 |
| problem alignment | `clarify` 动作 |
| structure design | `locate` × frame→field |
| project semantic field | path_authority + 项目级路径表 |
| model research engineering | `locate` × pipeline + `reflux` × trace;DL 契约见 ../pipeline_contracts.md |
| external reference | `locate` × external/;细则保留在 05_external_reference.md |
| document memory | `reflux` × trace + conflict 机制 |
| 行动前最低输出(5 行模板) | 开局检查 → pulse.md(kernel/pulse_protocol.md) |
| "结构、回流、反噬"等抽象动作 | 收紧为 clarify / locate / reflux 三个 |
| 显式冲突指出 | conflicts/ 目录 + 审计自动产出 |

---

## 第二次迁移的强制变化

| 项 | SKILL v2 中 | kernel + adapter 中 |
|---|---|---|
| 抽象规则 | 散落在 SKILL.md + coupling_protocol.md + path_authority.md | 集中在 [kernel/](../../../kernel/),九条元规则一文件一条 |
| DL 具体内容 | 与抽象规则混在 docs/field/ | 收纳在 domains/deep_learning/ |
| 路径表 | docs/field/path_authority.md(混元规则 + DL 实例) | 拆为 kernel/path_authority.md(原则)+ ../path_table.md(DL 实例) |
| 耦合规则 | docs/field/coupling_protocol.md | kernel/coupling_principle.md(原则)+ adapter 决定具体字段 |
| 审计脚本 | scripts/audit_coupling.py | ../audit_coupling.py(DL adapter 内) |
| 模板 | docs/field/templates/ 混 conflict/decision/experiment/module_contract | kernel/templates/(三个抽象)+ ../templates/(DL 特化) |

---

## 不变的事

- 三类上下文(宪法/过程/证据)分区。
- 实验文档冻结,核心文档演进。
- W&B 记录事实,docs 解释含义(DL 特化)。
- external/ 不污染 src/。
- 路径承担身份与权限。

---

## 接入已有 DL 项目

接入新项目时:

1. 在项目根放 SKILL.md(指向 kernel + adapter)。
2. 创建 docs/frame/、docs/trace/、docs/conflicts/。
3. 根据 ../path_table.md 建顶层目录。
4. 对 src/ 每个非豁免文件,补 Python docstring 锚点 + 在 docs/field/module_contracts/ 建镜像 doc(可初始为空 body + 完整 front-matter)。
5. 运行 `python domains/deep_learning/audit_coupling.py --update` 写入初始 audit_hash。
6. 后续每次提交前跑审计。
