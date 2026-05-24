---
name: path-authority
description: 路径承担语义负载;每条路径必须能回答身份/权威等级/生命周期/写权限/主要读者五问。
metadata:
  kernel_rule: C
---

# 路径权威

路径不是收纳空间。路径是语义载体。

路径承载语义,但路径不校验自己。路径规则必须被 schema 声明,并由 audit 检查现实是否服从 schema。见 [semantic_duality.md](semantic_duality.md)。

---

## 五项声明

新增任一类路径前,必须能回答五个问题:

| 问题 | 含义 |
|---|---|
| **身份** | 这条路径承担什么对象族?(代码模块?实验?决策?证据?外部参考?) |
| **权威等级** | 它的话有多大分量?(当前事实 / 当前意图 / 当前理解 / 历史证据 / 外部参考) |
| **生命周期** | 它怎么变?(持续演进 / 追加为主 / 冻结 / 一次性 / 临时覆盖) |
| **写权限** | 谁能改它?(用户裁决 / agent 自主 / 训练系统 / 数据负责人 / 任何 agent) |
| **主要读者** | 谁会读它?进入项目时,这条路径在哪个读取优先级上? |

五问任一项答不出,这条路径不应进入项目根目录。

对于事件记录路径,还必须能回答:它是哪一次发生、由什么触发、输入/过程/输出/分析/回流分别落在哪些文件。

---

## 一条路径只属于一类上下文

按 [three_contexts.md](three_contexts.md):宪法型 / 过程型 / 证据型。

不能让一条路径同时承担"运行证据"和"项目原则"——读者无法判断当前一句话该不该被引用为规则。

需要混合时,拆为子目录。例如:
- 模块文档族里既有宪法型契约也有草稿 → 拆 `module_contracts/draft/` 和 `module_contracts/`(已审定的)。
- 实验目录里既有 done 和 frozen,也有 running → 在 front-matter status 字段区分,而不是在目录上区分。

---

## 路径名即权威声明

命名规则:

- **名字即类型**:`frame/`、`trace/`、`runs/`、`conflicts/` 都直接说明是哪一类。
- **禁止模糊词**:`notes/`、`misc/`、`temp/`、`final/`、`new/`、`old/` —— 这些不承担任何类型声明。
- **冻结即标注**:实验、决策、conflict 等已冻结的对象,文件名或 front-matter 必须能让人立刻看出"这是过去某时点的快照,不是当前真理"。

---

## 路径权威表(项目级别)

每个项目应在 field 层维护一份具体路径表,列出本项目所有顶层路径的五项声明。

这份表是本元规则在该项目的实例。

对 kernel 本身的实例,见本项目根目录下的 [SKILL.md](../SKILL.md)。
对各 domain adapter,见各 adapter 的 `path_table.md`(例如 [domains/deep_learning/path_table.md](../domains/deep_learning/path_table.md))。

---

## 路径冲突处理

工件事实(实际文件、实际行为)和文档意图(声明的契约、声明的位置)发生冲突时:

1. 不静默修正任一方。
2. 在 conflicts 区写入条目,引用 [conflict_mechanism.md](conflict_mechanism.md) 的 schema。
3. 由用户裁决:以工件为准 → 更新文档;以意图为准 → 修改工件。
4. 裁决后 conflict 标记 resolved。

工件漂移由耦合审计自动检测(见 [coupling_principle.md](coupling_principle.md))。

---

## 新路径加入规则

新增顶层目录或新增一类对象时:

1. 先在项目级 path_table 追加一行,声明五项。
2. 才允许在该路径下创建文件。
3. 未登记的路径不进入项目根目录。

这条规则防止项目目录被无声地长出新对象族。
