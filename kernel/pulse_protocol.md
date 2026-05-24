---
name: pulse-protocol
description: 任何 agent 进入项目第一件事;5 行覆盖式快照,同步写入 pulse.md。
metadata:
  kernel_rule: H
---

# 开局检查(Pulse)

任何 agent 进入项目,在执行任何动作前,先输出 5 行,同步覆盖到项目根 `pulse.md`。

---

## 5 行格式

```text
任务: <当前任务的真问题、成功标准 —— 来自 frame>
位置: <在哪个对象、哪条路径上工作>
最近: <最近一条相关 trace,无则 none>
冲突: <conflicts 中未解决的相关条目,无则 none>
动作: <clarify | locate | reflux> 在 <frame | field | trace>
```

无信息时填 none,不允许留空。
无法填某行 → 该 agent 还不具备进入本项目的最低上下文 → 不要执行动作,先读取 frame / trace / conflicts。

---

## 为什么是 pulse 而不是 status

- 不是历史记录,是当前心跳。
- 旧 pulse 不保留 —— 上一份覆盖式追加到 `docs/frame/task_history.md`。
- 任何 agent 进入项目第一读 = pulse.md;读完即知道自己在哪一拍上。

---

## 写入时机

- 每次 agent 接管任务时(开局)。
- frame 发生变化时(clarify 完成)。
- 主动作切换时(从 locate 切到 reflux 等)。

不在每次工具调用时写。pulse 不是日志,是节拍。

---

## pulse 的失败模式

- **行数不足 5 行** → agent 越过开局直接动作,常见漂移源。
- **任务行只复述用户最近一句话** → 没真正读 frame,只复读 prompt。
- **冲突行说"none"但 conflicts 区有 open 条目** → 没读 conflicts。

任一项失败,等同于动作未授权。
