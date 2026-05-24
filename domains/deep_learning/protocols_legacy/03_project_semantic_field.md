# Project Semantic Field Protocol

本文档用于把一个研究任务转化为可被 agent 长期进入、定位、验证和回流的项目结构。

核心原则：

> 项目不是文件集合。  
> 项目是语义化运行场。

---

## 1. 项目即上下文

agent 的真实上下文不只来自 prompt。

它来自：

- 项目路径；
- 核心文档；
- 实验记录；
- 运行结果；
- 配置；
- 数据版本；
- 环境；
- 用户裁决。

因此项目必须显式表达：

- 什么代表当前理解；
- 什么代表历史证据；
- 什么可以修改；
- 什么只能读取；
- 结果写到哪里；
- 失败如何记录；
- 结论如何回流。

---

## 2. 路径承担语义

路径不是收纳空间。

路径必须表达：

```text
身份
权威等级
生命周期
读写权限
回流关系
```

基本分区：

```text
src/          稳定能力代码
configs/      实验条件
data/         输入事实
scripts/      动作入口
tests/        验证约束
docs/         项目理解
runs/         运行证据
analysis/     二次分析
artifacts/    对外产物
checkpoints/  权重资产
external/     外部参考
```

---

## 3. 三类上下文

### 宪法型上下文

少量、高权威、持续更新。

例如：

```text
docs/core/project_objective.md
docs/core/benchmark_protocol.md
docs/core/current_state.md
docs/core/model_pipeline.md
```

### 过程型上下文

任务推进中的中间状态。

例如：

```text
docs/experiments/
docs/modules/
docs/runbooks/
```

### 证据型上下文

历史事实和运行结果。

例如：

```text
runs/
W&B runs
metrics
logs
visualizations
checkpoints
```

三者不能混在一起。

否则 agent 会把历史当原则，把草稿当事实，把输出当输入。

---

## 4. 核心文档演进，实验文档冻结

核心文档代表当前项目理解，应少量、稳定、持续更新。

实验文档代表一次历史状态，应按实验编号冻结。

原则：

> 实验冻结，结论回流，核心演进。

如果实验结果改变了理解，不能只停留在 runs 或 W&B。

它应回流到：

```text
docs/core/
docs/modules/
docs/decisions/
docs/failures/
```

---

## 5. 冲突处理

项目演化后一定会出现冲突：

```text
代码实际行为
测试结果
核心文档
模块文档
实验记录
运行日志
```

代码代表当前事实。

核心文档代表当前意图。

二者冲突时，不要静默修正。

应显式提出：

- 哪两处冲突；
- 冲突影响什么；
- 需要用户裁决以代码为准，还是以意图为准。

---

## 6. 文档分裂规则

文件承载对象。

目录承载对象族。

当一个文档内部出现多个稳定子问题时，应升级为目录。

例如：

```text
docs/modules/change_decoder.md
```

可以升级为：

```text
docs/modules/change_decoder/
├── overview.md
├── interface.md
├── failure_modes.md
└── verification.md
```

---

## 7. 最高原则

> 路径承担身份、权威、生命周期和权限。  
> 核心文档代表当前理解。  
> 实验文档保存历史证据。  
> runs 和 W&B 记录发生了什么。  
> docs 判断这说明什么。  
> 结果必须能回流，项目才会成长。
