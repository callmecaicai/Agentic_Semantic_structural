---
name: reflux-mechanism
description: 证据 → 理解的升级日志;一切新证据必须留条目,verdict=pending 即 conflict。
metadata:
  kernel_rule: F
---

# 回流机制

证据进入项目不会自动改变理解。回流是把证据升级为理解的显式动作。

---

## 主载体

`docs/trace/reflux_journal.md` 是单一回流日志。

每条 reflux 一行,记录:

```
| date | source | what changed | updated docs | verdict |
```

| 字段 | 含义 |
|---|---|
| date | 观察到证据的日期 |
| source | 证据出处(run id / 实验文档 / 外部资料 / 用户观察) |
| what changed | 一句话:这次证据带来什么新理解 |
| updated docs | 被升级的 frame/field 文档路径 |
| verdict | accepted / pending / rejected / superseded |

---

## verdict 的含义

| verdict | 含义 | 后续 |
|---|---|---|
| **accepted** | 解释已写入对应 doc | 关闭条目 |
| **pending** | 证据已观察但解释未完成 | 是 conflict 的子类,见下 |
| **rejected** | 审视后决定不更新理解 | 必须在备注说明为什么 |
| **superseded** | 已被后续条目取代 | 保留供追溯 |

---

## pending = conflict

verdict=pending 的条目本身就是一种 conflict:**应有解释而尚无**。

- 审计应能捕获 pending 条目超过阈值。
- 开局检查的"冲突"行应登记 pending 条目数。
- pending 不应长期存在;长期 pending 意味着 frame 已经不再覆盖正在发生的事。

---

## 什么必须回流

任何"已发生且可能改变理解"的事件:

- 一次实验/运行完成
- 一次决策的实际后果显现
- 一次失败的暴露
- 一次外部证据(论文、对手模型、用户反馈)的引入
- 任一动作完成后新观察到的事

不需要回流:
- 完全在预期内、不增加任何理解的事件(但即使如此,留 verdict=accepted 的条目以记录"已确认无更新")。

---

## reflux 与 clarify 的关系

reflux 是 trace → frame/field 的方向。

当 verdict=accepted 且涉及 frame 时:
- 不是简单覆盖 frame,而是触发一次 clarify 动作。
- 旧 frame 进入 task_history 留存。
- 新 frame 在 current_task 生效。

不绕过 clarify 直接改写 frame —— 否则证据可以无声地重塑任务,丢失审视机会。

---

## 与 decision 的关系

reflux 通常不写 ADR。只有当 reflux 引发了一次有备选项的判断时,才升级为 decision。

例如:
- run 跑出 X 指标低 → reflux:观察事实 + verdict
- 因为 X 低,决定换 backbone → 这是 decision,在 docs/trace/decisions/ 写 ADR

reflux 记录"看到什么、说明什么",decision 记录"因此选择什么"。
