---
adr_id: 002
title: add_semantic_duality_to_kernel
date: 2026-05-24
status: accepted
superseded_by:
---

# ADR 002: add_semantic_duality_to_kernel

## Context

用户指出 agentic harness 的核心不只是代码-文档耦合,而是两组对偶:

- 稳定可引用对象与固定镜像文档一一对应。
- 一次性发生的执行过程与增量语义记录文件夹一一对应。

这个结构不只适用于深度学习训练,也适用于论文阅读、论文写作、生活训练规划、计划管理和任意持续推进系统。

## Decision

将该原则提升为 kernel 规则 J:[../../../kernel/semantic_duality.md](../../../kernel/semantic_duality.md)。

同时新增通用语义记录文件夹模板:[../../../kernel/templates/semantic_record/](../../../kernel/templates/semantic_record/)。

## Alternatives considered

- 只写进 deep_learning adapter:不选,因为该结构是跨领域 agentic harness 原则。
- 合并进 coupling_principle.md:不选,因为 coupling 只覆盖稳定对象,不能充分表达一次发生的增量记录。
- 只依赖 agent 记忆:不选,因为该系统目标就是把语义外化到路径、模板、schema、audit 和 conflict。

## Consequences

- 立即影响:SKILL 入口新增 semantic duality;locate 的退出条件同时覆盖 artifact mirror 与 event record。
- 长期影响:未来 adapter 必须声明稳定对象和事件实例两类对象的路径模式与校验方式。
- 风险:如果过早为不稳定事件创建复杂模板,会增加维护负担;adapter 应只固化重复出现的模式。

## What would refute this decision

如果未来多个项目证明"一次发生"不需要语义记录文件夹也能可靠 reflux、复盘和接力,则可以降低该规则的强度。

## Related

- frame: [../../frame/current_task.md](../../frame/current_task.md)
- 涉及工件: [../../../SKILL.md](../../../SKILL.md)
- 涉及文档: [../../../kernel/semantic_duality.md](../../../kernel/semantic_duality.md)
- 涉及 reflux: [../reflux_journal.md](../reflux_journal.md)
