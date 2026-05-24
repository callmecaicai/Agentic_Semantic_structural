---
name: three-actions
description: clarify / locate / reflux × frame / field / trace — 三动作 × 三层的元结构;任何 AI 协作推进的项目都通过这个矩阵路由动作。
metadata:
  kernel_rule: A
---

# 三动作 × 三层

任何持续推进、持续记录的协作项目都在三层上运行,通过三动作产生改变。

---

## 三层

| 层 | 承担 | 状态特征 |
|---|---|---|
| **frame** | 当前意图(任务对象、目标、成功标准、不可承受的失败) | 当前生效,可被改写 |
| **field** | 当前结构理解(对象族、路径权威、契约、耦合规则) | 持续演进,改动需留痕 |
| **trace** | 历史证据 + 解释(运行记录、回流日志、决策、失败) | 追加为主,历史不静默改 |

第四个域 **conflicts** 不是层,是任何层之间出现不一致时的承载位置。详见 [conflict_mechanism.md](conflict_mechanism.md)。

三层互不替代:
- 不把证据当原则(trace 不能假冒 frame)。
- 不把过程稿当事实(field 草图不能假冒 trace 证据)。
- 不把意图当输入(frame 不能假冒 field 已有结构)。

详细分区规则见 [three_contexts.md](three_contexts.md)。

---

## 三动作

| 动作 | 含义 | 触发 |
|---|---|---|
| **clarify** | 重新定义任务对象、目标、成功标准 | 任务模糊;反复失败;证据动摇原 frame |
| **locate** | 在结构中放置新对象,或修订对象的位置/契约/接口 | 新增工件;接口变化;新引入外部参考 |
| **reflux** | 把证据回流到当前理解,可能升级 frame 或 field | 一轮工作完成;新证据累积;模块行为变化 |

任一动作可作用于任一层:
- **clarify × frame** = 重写当前任务定义
- **clarify × field** = 重新命名某结构对象的身份
- **clarify × trace** = 重新解读一条历史证据
- **locate × frame** = 给某目标分配承载位置
- **locate × field** = 新建工件 + 镜像文档(见 [coupling_principle.md](coupling_principle.md))
- **locate × trace** = 给一条历史证据归类登记
- **reflux × frame** = 证据迫使任务定义更新
- **reflux × field** = 证据迫使结构理解更新
- **reflux × trace** = 在 reflux_journal 追加一条;verdict 决定是否升级到 frame/field

---

## 退出条件

只有满足退出条件才能进入下一动作。

- **clarify 完成**:任务对象、目标、成功标准、不可承受的失败 都明确。
- **locate 完成**:工件就位 + 镜像文档建立 + 双向锚点齐全 + 验证桥指向有效文件;耦合审计通过。
- **reflux 完成**:reflux_journal 当前条目填完,verdict 已下;若 verdict=accepted,对应 frame/field 文档已同步更新;若 pending,已登记为 conflict。

未满足退出条件就推进下一动作 → 累积漂移 → 未来 conflict 倍增。

---

## 路由的优先级

当多个动作同时似乎适用时,按以下优先级:

1. **clarify 优先**:任务不清楚,任何 locate/reflux 都是空转。
2. **reflux 次之**:有未消化的证据,任何 locate 都在旧理解上叠加。
3. **locate 最后**:前两者都清空,才进入构造性动作。

这个顺序保护项目不被自身产出淹没。

---

## 与其他元规则的接口

- 开局检查在动作之前;输出 5 行,写入 [pulse.md](../pulse.md)。
- 任一动作过程中观察到不一致 → 不静默修正 → 写入 [conflict_mechanism.md](conflict_mechanism.md) 描述的 conflicts 区。
- 任一动作产生的工件必须满足 [coupling_principle.md](coupling_principle.md):工件 ⇄ 镜像文档,双向锚点,验证桥。
