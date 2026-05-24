---
name: frozen-vs-evolving
description: 证据冻结,理解演进,转折由 decision 留痕;这三条共同保护项目不被自己的产出无声重塑。
metadata:
  kernel_rule: G
---

# 冻结 vs 演进

任何持续运转的项目都同时存在三种时间线。

---

## 三条时间线

| 时间线 | 内容 | 写入方式 |
|---|---|---|
| **冻结** | 历史证据(运行记录、实验文档、外部参考引入快照、过去 frame) | 一次性写入,后续追加 correction,不静默改 |
| **演进** | 当前理解(frame、field 核心契约) | 持续更新,改动可见 |
| **留痕** | 从一种理解切到另一种(ADR / decision) | 单次写入,标记 superseded 时保留 |

三者错配 = 项目记忆失真:
- 冻结被改 → 历史被改写,失去对比基准。
- 演进被冻 → 当前理解过时,新证据无承载位置。
- 转折无 ADR → 理解变化没有"为什么",未来回看只见结果。

---

## 冻结的对象

| 类型 | 冻结特征 |
|---|---|
| 单次实验 / run 记录 | status=done → frozen 后只允许 follow-up 链接和 correction 追加 |
| 已 accepted 的 decision | 即使被 superseded,原文件保留,在新 ADR 中引用 |
| task_history 中的 frame 快照 | 一旦覆盖 pulse 后追加,不能改写 |
| 外部参考的特定版本快照 | 引入时记录 commit/version,不再随上游变 |

---

## 演进的对象

| 类型 | 演进特征 |
|---|---|
| 当前 frame(current_task) | 旧版本进入 task_history,新版本生效 |
| field 核心契约(路径表、耦合规则) | 每次改动应触发 ADR |
| 镜像文档 | 跟随工件变化更新,通过 audit_hash 锁定版本 |
| reflux_journal | 每条 reflux 追加,verdict 可后续从 pending 转 accepted |

---

## 改写检测

任何对冻结对象的修改 = 一个 conflict。

实现方式:
- 实验文档加 `status: frozen`;agent 修改前必须看到 status 然后拒绝。
- decision 加 `status: accepted | superseded`;不修改原 decision,写新 ADR 标记 superseded。
- task_history 是追加日志,从结构上不允许中间插入。
- 镜像文档由 `audit_hash` 守护;hash 改变即工件改变,需要 ADR 或同步更新。

---

## 演进的低成本规则

为了让"演进"不变成"维护负担":

- agent 不主动扫描全项目找冲突 —— 只在 pulse 或 reflux 时观察当前路径。
- agent 不主动拆分文档 —— 只在自然出现稳定子问题时升级为目录。
- 核心理解的更新只由用户裁决或明确动作产出。

详见 [conflict_mechanism.md](conflict_mechanism.md) 的"不主动治理"。
