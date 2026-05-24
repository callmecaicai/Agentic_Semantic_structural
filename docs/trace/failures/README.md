# Failures

记录有复现性和结构警示价值的失败模式。

每个失败一个文件:`YYYY-MM-DD_<short_failure_name>.md`。

---

## 何时记录

- 一类反复出现的项目失败,其原因可命名。
- 某个沉默失败只有通过探针、审计、回看或用户指出才显现。
- 某条 kernel 规则或 adapter 规则不足以承载真实工作。
- 某次推进暴露出路径、模板、验证桥或 reflux 机制的结构性缺口。

---

## 不记录

- 一次性的拼写、格式或路径错误,修复后没有结构启发。
- 已由 conflict 文件完整承载且不需要额外教训的单次不一致。

---

## 模板

```markdown
---
discovered: YYYY-MM-DD
related_source: <证据来源路径或事件 id>
related_artifact: <相关工件路径,若有>
status: open | mitigated | fixed
---

# Failure: <name>

## Symptom
<观察到的现象>

## Root cause
<根本原因。若未明则写"未明,假设是...">

## How it surfaced
<怎么被发现:审计、用户反馈、复盘、运行记录、外部证据等>

## Mitigation
<目前如何避免或修复>

## Lesson
<结构层面的启示。例如:某类失败需要新模板、验证桥或 path authority>
```
