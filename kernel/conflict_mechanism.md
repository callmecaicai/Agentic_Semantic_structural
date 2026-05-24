---
name: conflict-mechanism
description: 项目内任何"应一致而实际不一致"的两件事都必须显式登记为 conflict,不静默修正。
metadata:
  kernel_rule: E
---

# 冲突机制

不静默修正。所有不一致显式登记,等待裁决。

---

## 什么算 conflict

项目内部"按当前理解应一致,但实际不一致"的任意两件事:

- 工件事实 vs 镜像文档(由耦合审计自动检测 —— 见 [coupling_principle.md](coupling_principle.md))
- 已发生事件 vs 语义记录文件夹(由 event 审计检测 —— 见 [semantic_duality.md](semantic_duality.md))
- 当前 frame 意图 vs 已观察证据
- 已跑的事件没有进入 trace 解释(pending reflux —— 见 [reflux_mechanism.md](reflux_mechanism.md))
- 已知失败没有进入 failures 记录
- 任意两份文档对同一对象给出不同结论
- 用户手动指出的任意不一致

不属于 conflict:
- git merge 冲突(那是版本控制层)
- 风格、措辞、格式偏好
- 单纯"我觉得应该重写"

---

## 来源

| 来源 | 触发方式 |
|---|---|
| 耦合审计 | 自动产出文件,类型见 [coupling_principle.md](coupling_principle.md) 表 |
| 用户 | 手动写入,type=`manual` |
| agent 在开局检查或 reflux 时观察到 | type=`frame-vs-evidence` / `evidence-not-refluxed` / `failure-not-recorded` |

---

## 文件 schema

每个 conflict 一个文件,命名:`YYYY-MM-DD_<short_name>.md`。
使用模板 [templates/conflict.md](templates/conflict.md)。

front-matter 必含:
```yaml
---
type: <conflict type>
discovered: YYYY-MM-DD
discovered_by: <audit name | user | agent>
target_artifact: <被影响的工件路径或空>
target_doc: <被影响的文档路径或空>
status: open | resolved
---
```

body 必含三段:
1. **What conflicts** —— 具体两件事在哪里分歧
2. **Why it matters** —— 继续放任会有什么后果
3. **Resolve by** —— 选择一种处理:更新文档 / 更新工件 / 标记豁免 / 重新 clarify

---

## 处理流程

1. 来源产出 conflict 文件,默认 status=open。
2. 在开局检查 [pulse.md](../pulse.md) 的"冲突"行登记。
3. 进入 clarify(若涉及任务定义) 或 locate(若涉及结构) 解决。
4. 解决后:
   - 在文件追加 Resolution 段:日期、所采取动作、关联 commit / run。
   - status 改为 resolved。
   - 一段时间后可归档到 `_resolved/` 或删除。

---

## 重复出现

审计不覆盖已存在的同名 conflict。

同一个 conflict 反复出现 → 根本原因未消除,不是审计 bug。需在 clarify 中重新审视任务定义,或在 locate 中重新审视耦合规则。

---

## 与三动作的接口

- conflict 进入 pulse 后,必然触发下一动作:clarify 或 locate(很少 reflux,除非这条 conflict 本身需要靠新证据来回流判断)。
- agent 在任一动作前观察到新 conflict → 不能跳过,必须先写入 conflicts 区再继续。
- agent 不应自己裁决"以工件为准还是以文档为准"——这是用户裁决权。

---

## 最高规则

不静默修正 = 不允许 agent 自作主张让一边对齐另一边。

> 看到不一致 → 写 conflict → 等裁决。
> 不要为了"代码看起来整洁"或"文档看起来更新"而抹去差异。

差异里通常藏着用户尚未澄清的判断。
