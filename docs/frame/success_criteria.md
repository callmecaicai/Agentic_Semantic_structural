# Success Criteria

记录项目级长期成功标准。当前任务的即时成功条件见 [current_task.md](current_task.md)。

---

## Project-level Success

这个 skill 成功的标志:任何需要持续记录、推进、回看和再解释的项目,都能先用 kernel 建立协作秩序,再按需要引入 domain adapter。

适用对象包括但不限于:

- 生活力量训练规划
- 论文阅读和攻坚
- 论文写作与推进
- 计划管理和项目演进
- 研究工程和代码项目

---

## Operating Standards

- [SKILL.md](../../SKILL.md) 只承担入口路由,不承载领域细则。
- [kernel/](../../kernel/) 保持抽象:规则可迁移到任意持续项目。
- 领域细则只进入 [domains/](../../domains/) 下的 adapter。
- 三类上下文(宪法型 / 过程型 / 证据型)不混用。
- 任一可持续推进的工件必须能说明其镜像文档、锚点、审计方式和验证桥。
- 任一一次性发生的事件必须能说明其语义记录文件夹、输入、过程、输出、分析和回流状态。
- open conflict 不被静默修复;必须登记、裁决、留痕。
- evidence 进入 [../trace/reflux_journal.md](../trace/reflux_journal.md) 后,才能升级为 frame/field。
- legacy 内容冻结,只作为历史参考和迁移说明。

---

## Kernel Quality Bar

一条 kernel 规则只有在满足以下条件时才应留下:

- 不依赖某个具体领域或工具。
- 能回答一个稳定的结构问题,而不是一次性任务问题。
- 能通过 adapter 被具体化。
- 能产生可检查的退出条件或冲突类型。

不满足者应下放到 adapter、trace 或 legacy。

---

## Harness Duality Bar

本系统必须维持两组对偶:

- 稳定对象 -> 固定镜像文档。
- 一次发生 -> 增量语义记录文件夹。

稳定对象不把历史堆进自身;一次发生不覆盖历史。

校验责任不由路径单独承担。路径表达语义,schema 声明语义,audit 检查现实,conflict 承载断裂,reflux 升级理解。

---

## Adapter Quality Bar

一个 domain adapter 只有在某类项目反复出现同一组路径、契约、验证方式或模板时才应创建。

adapter 必须:

- 指向它实例化的 kernel 规则。
- 声明自己的 path table。
- 定义工件与镜像文档的映射。
- 提供必要模板或脚本。
- 不否定 kernel 的最高规则。
