# Domains

每个 domain adapter 是 [kernel/](../kernel/) 元规则的一个具体化实例。

kernel 定义"工件 ⇄ 镜像文档 ⇄ 锚点 ⇄ 审计 ⇄ 验证桥"的元规则;adapter 定义在某个具体工作类型下,这五项具体长什么样。

---

## 现有 adapter

| adapter | 工作类型 | 工件载体 | 验证桥 |
|---|---|---|---|
| [deep_learning/](deep_learning/) | 深度学习实验工程 | src/ + configs/ + runs/ | tests/ + probes/ + W&B |

---

## 写一个新 adapter

在 `domains/<name>/` 下产出至少以下内容:

1. **README.md** —— 一段话:本 adapter 服务于哪种工作类型。
2. **path_table.md** —— 本类工作下,具体路径的五项声明(身份/权威/生命周期/写权限/读者),实例化 [path_authority.md](../kernel/path_authority.md)。
3. **耦合实现** —— 决定具体的路径镜像规则、锚点字段名、审计实现,实例化 [coupling_principle.md](../kernel/coupling_principle.md)。
4. **templates/** —— 在 kernel 三个模板之上,本域特化的派生模板(例如 experiment 模板含 wandb 字段)。

可选:
- **全局契约** —— 如果本类工作有跨工件的统一接口规范(类似 DL 的 pipeline_contracts)。
- **协议遗产** —— 若 adapter 由旧版本迁移而来,旧规则可冻结在 `protocols_legacy/`。

---

## adapter 不可破坏的事

- kernel 的 9 条元规则不可在 adapter 中被否定,只能被具体化。
- conflict / decision / mirror_contract 三个 kernel 模板不可被废止;adapter 模板只能扩展,不能砍字段。
- 三类上下文(宪法 / 过程 / 证据)分区不可在 adapter 中合并。

---

## adapter 之间

不同 adapter 在同一项目根中可共存。例:
- 一个研究者的项目可能同时是"DL 实验"和"论文写作"。
- 根目录的 `docs/frame/` 由 frame 层接管,跨 adapter 共享。
- 各 adapter 在自己的子树下管理工件和镜像。

跨 adapter 冲突进入根目录的 [docs/conflicts/](../docs/conflicts/)。
