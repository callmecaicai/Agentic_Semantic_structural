# External Reference Protocol

本文档规定 external/ 如何管理对手模型、同方向项目源码、论文材料、benchmark 说明和外部文档分析。

核心原则：

> external 是外部参考世界。  
> 它不承载当前项目运行事实。

---

## 1. external/ 的作用

external/ 用于存放：

- 对手模型源码；
- 同方向开源项目；
- 论文官方实现；
- benchmark protocol；
- 外部工具文档；
- 复现材料；
- license；
- 对外部项目的分析笔记。

它帮助我们学习、对照、复现和吸收外部思想。

但它不是本项目的 src。

---

## 2. 推荐结构

```text
external/
├── README.md
├── reference_projects/
│   ├── <project_name>__<owner>__commit_<sha>/
│   │   ├── SOURCE.md
│   │   ├── ANALYSIS.md
│   │   └── ...
│   └── ...
├── opponent_models/
│   ├── <model_name>/
│   │   ├── SOURCE.md
│   │   ├── PAPER.md
│   │   ├── REPRODUCTION.md
│   │   └── ANALYSIS.md
│   └── ...
├── papers/
├── benchmark_protocols/
├── reference_docs/
└── licenses/
```

---

## 3. SOURCE.md

每个外部项目必须有 SOURCE.md。

最少记录：

```markdown
# Source

Origin: <url>
Version: <tag / commit / date>
License: <license>
Imported At: <date>
Purpose: 为什么引入
Use As: 参考、对照、复现、benchmark、实现灵感
Do Not Use As: 当前项目事实源
Related Docs: docs/...
```

---

## 4. ANALYSIS.md

每个重要外部项目应有 ANALYSIS.md。

它不复述代码。

它回答：

- 这个项目解决什么问题；
- 它的核心 pipeline 是什么；
- 它的数据输入契约是什么；
- 它的模型结构如何分层；
- 它的训练和评估 protocol 是什么；
- 哪些设计可吸收；
- 哪些设计不适合本项目；
- 它和当前项目的差异是什么。

---

## 5. 吸收外部实现的路径

不要直接让本项目代码 import external。

正确路径：

```text
external/reference_projects/...
  -> 阅读 SOURCE.md 和 ANALYSIS.md
  -> 必要时写 docs/decisions/
  -> 按本项目 contract 在 src/ 中重新实现或适配
  -> 写 tests / probes 验证行为
  -> 用实验记录评估是否有效
```

如果必须 vendor 第三方代码，应单独使用：

```text
third_party/
vendor/
```

并明确 license、版本和修改记录。

---

## 6. 对手模型管理

对手模型不是普通参考材料。

它们用于：

- 对齐 benchmark；
- 分析 SOTA 差距；
- 复现 baseline；
- 比较 pipeline；
- 寻找结构启发。

每个对手模型至少记录：

- 论文；
- 官方代码；
- checkpoint；
- 数据协议；
- 训练协议；
- 评估指标；
- 复现状态；
- 与本项目差异；
- 是否纳入 benchmark table。

---

## 7. 最高原则

> external 可以启发 src，但不能污染 src。  
> external 可以提供证据，但不能替代本项目判断。  
> external 的实现思想必须经过本项目 contract 重新表达。  
> 对手模型必须被分析，而不是只被收藏。
