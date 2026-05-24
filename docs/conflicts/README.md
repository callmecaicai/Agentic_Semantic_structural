# Conflicts

存放未解决的项目级冲突。每个 conflict 一个文件:`YYYY-MM-DD_<short_name>.md`。

conflict 指项目内部"按当前理解应一致,但实际不一致"的关系失败;不是 git merge conflict。

完整规则见 [../../kernel/conflict_mechanism.md](../../kernel/conflict_mechanism.md)。

---

## 来源

| 来源 | 类型示例 |
|---|---|
| adapter 审计脚本 | artifact-vs-doc, orphan-doc, uncovered-artifact, missing-verifier, no-front-matter, no-covers, no-audit-hash |
| 用户手动指出 | manual |
| agent 在 pulse 或 reflux 中发现 | frame-vs-evidence, evidence-not-refluxed, failure-not-recorded |

---

## 文件格式

使用 [../../kernel/templates/conflict.md](../../kernel/templates/conflict.md)。

front-matter 必含:

- `type`
- `discovered`
- `discovered_by`
- `target_artifact`
- `target_doc`
- `status`

status:

- `open`:未解决。
- `resolved`:已解决,保留供追溯。可在解决一段时间后归档到 `_resolved/`。

---

## 处理流程

1. 审计、用户或 agent 产出 conflict 文件。
2. 在 [../../pulse.md](../../pulse.md) 的"冲突"行登记。
3. 进入 clarify 或 locate 动作解决。
4. 解决后填写 Resolution 段,把 status 改为 resolved。

---

## 最高规则

不静默修正。

看到不一致时,先登记 conflict,再由用户裁决以哪一侧为准。
