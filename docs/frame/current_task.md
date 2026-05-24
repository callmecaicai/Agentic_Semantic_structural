# Current Task

本文件描述当前正在解决的任务。同一时间只有一个 current task,旧版本进入 [task_history.md](task_history.md)。

---

## Object

优化本 skill 工具包的第一性元结构: [SKILL.md](../../SKILL.md)、[kernel/](../../kernel/)、[domains/](../../domains/) 与 `docs/` 中的协作记录。

## Goal

把"基于 Markdown 的语义管理机制"和"基于工件/代码的项目推进机制"沉淀为抽象 kernel;把深度学习等具体规则降级为 domain adapter。

## Success Criteria

- [SKILL.md](../../SKILL.md) 是 domain-neutral 入口,不再把深度学习当默认项目形态。
- [kernel/](../../kernel/) 中九条元规则完整、可独立阅读,且不依赖某个具体领域。
- 具体领域规则只出现在 [domains/](../../domains/) 下;当前 DL 规则集中在 [domains/deep_learning/](../../domains/deep_learning/)。
- `docs/frame/`、`docs/trace/`、`docs/conflicts/` 的 README 与模板引用都指向 kernel 或 adapter 的新位置。
- 旧路径引用只允许出现在 legacy/migration 说明中,不能作为当前规则入口。

## Worst Acceptable Outcome

最不可接受的是:表面上拆出了 kernel,但入口和核心规则仍然把某个具体领域当作默认世界。

## Constraints

- 保留已有工作成果,不回滚上一轮已生成的 kernel 与 adapter。
- 不把生活训练、论文阅读、论文写作、计划管理等未来用法提前具体化;只留下能承载它们的元规则。
- 具体 adapter 只能实例化 kernel,不能覆盖 kernel。

## Out of Scope

- 不为生活训练、论文阅读、论文写作、计划管理立即创建完整 adapter。
- 不重写 legacy protocol 的历史内容;只修正其位置和引用。
- 不把本 skill 安装到全局 Codex skills 目录。

## Related

- pulse: [../../pulse.md](../../pulse.md)
- kernel: [../../kernel/](../../kernel/)
- adapters: [../../domains/](../../domains/)
- reflux: [../trace/reflux_journal.md](../trace/reflux_journal.md)
- conflicts: [../conflicts/](../conflicts/)
