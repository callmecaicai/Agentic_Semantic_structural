---
name: semantic-duality
description: 稳定工件 ⇄ 固定镜像文档,一次发生 ⇄ 增量语义记录文件夹;这是 agentic harness 的双重对偶结构。
metadata:
  kernel_rule: J
---

# 语义对偶

足够工程化的代码/工件系统天然已经语义化:它把世界拆成组件、接口、流程、配置、运行、结果和失败。

MD 系统不是给代码写旁注。MD 系统是可执行结构的对偶面:代码负责可执行性,文档负责可解释性、可追溯性、可回流性。

---

## 两种对偶

| 可执行侧 | 语义侧 | 生命周期 | 核心动作 |
|---|---|---|---|
| **稳定对象** artifact / module / component / section / plan unit | **固定镜像文档** mirror doc | 一一对应,随对象演进 | `new-artifact` |
| **一次发生** run / session / iteration / task execution / training event | **增量语义记录文件夹** semantic record folder | 每发生一次新增一次,不覆盖历史 | `new-event` |

这两种对偶共同构成 agentic harness 的核心骨架。

---

## 稳定对象对偶

稳定对象是会被反复引用、修改、组合和验证的东西。

抽象形式:

```text
artifact
  <-> mirror.md
```

例:

- 代码组件 -> 组件契约文档
- prompt 模块 -> prompt 契约文档
- 论文 section -> section 意图文档
- 训练计划单元 -> cycle / block 契约文档
- workflow 节点 -> 节点语义文档

要求:

- 一一对应。
- 路径可推导。
- 文档 front-matter 指向工件。
- 工件侧可通过锚点指向文档。
- 工件变化触发审计;语义漂移时产生 conflict。

细则见 [coupling_principle.md](coupling_principle.md)。

---

## 一次发生对偶

一次发生是系统真实执行过的一次过程。

抽象形式:

```text
event instance
  <-> semantic_record_folder/
```

例:

- 一次训练
- 一次 agent 任务
- 一次论文阅读 session
- 一次写作推进
- 一次计划复盘
- 一次系统运行

要求:

- 每发生一次就新增一个文件夹。
- 不覆盖历史。
- 文件夹命名表达日期、事件 id、语义名。
- 文件夹内部结构稳定。
- 记录输入、过程、输出、分析、回流。

通用文件夹形态:

```text
docs/<event_class>/
└── YYYY-MM-DD_<event_id>_<slug>/
    ├── index.md
    ├── input.md
    ├── process.md
    ├── output.md
    ├── analysis.md
    └── reflux.md
```

adapter 可以扩展这些文件名,但不能丢掉五个语义位置:总览、输入、过程、输出、解释、回流。

模板见 [templates/semantic_record/](templates/semantic_record/)。

---

## 路径、schema、audit、conflict 的分工

路径承载语义,但路径本身不校验自己。

闭环如下:

```text
路径表达语义
schema 声明语义
CLI / agent 按 schema 创建对象
audit 按 schema 检查现实
conflict 承载断裂
reflux 把证据升级为理解
```

| 部件 | 承担 |
|---|---|
| **path** | 让人和 agent 从位置读出对象类型、身份、生命周期 |
| **schema** | 声明 artifact/event 的路径模式、必填文件、front-matter 字段 |
| **new-artifact** | 按 schema 创建稳定对象和镜像文档 |
| **new-event** | 按 schema 创建一次发生的语义记录文件夹 |
| **audit** | 检查路径、镜像、必填文件、锚点、hash、reflux 状态 |
| **conflict** | 保存 audit 发现的不一致,等待裁决 |

schema 是规则声明,audit 是现实检查,conflict 是不一致案卷。

---

## 典型 audit 检查

### 对稳定对象

- artifact 存在但 mirror doc 不存在 -> `uncovered-artifact`
- mirror doc 指向不存在的 artifact -> `orphan-doc`
- front-matter 缺失 -> `no-front-matter`
- artifact hash 与 doc 中 `audit_hash` 不同 -> `artifact-vs-doc`
- `verified_by` 指向的验证物不存在 -> `missing-verifier`

### 对一次发生

- event 已发生但 semantic record folder 不存在 -> `unrecorded-event`
- record folder 缺必填文件 -> `incomplete-record`
- `index.md` 没有 trigger / input / output 引用 -> `record-no-anchor`
- `reflux.md` 仍 pending 且超过阈值 -> `evidence-not-refluxed`
- record 声称引用的 artifact / config / result 不存在 -> `record-broken-reference`

---

## 与三动作的关系

| 动作 | 在对偶结构中的表现 |
|---|---|
| **clarify** | 重新界定什么算稳定对象、什么算一次发生、什么必须被记录 |
| **locate** | 执行 `new-artifact` 或 `new-event`,把对象放入路径-schema 中 |
| **reflux** | 从 semantic record folder 提炼理解,更新 frame/field 或产出 conflict |

没有对偶结构,agent 只能临时记忆。
有对偶结构,agent 可以反复接力,因为语义已经外化为路径、模板、schema 和审计。

---

## 最高规则

凡是工程系统中稳定可引用的对象,都应在语义系统中有固定镜像。

凡是工程系统中一次性发生的过程,都应在语义系统中有增量记录。

稳定对象不堆历史;一次发生不覆盖历史。
