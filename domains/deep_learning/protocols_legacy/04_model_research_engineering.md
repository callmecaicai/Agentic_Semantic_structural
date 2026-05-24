# Model Research Engineering Protocol

本文档用于深度学习研究项目的实验代码、W&B 证据系统、模型 pipeline、测试探针和可视化设计。

核心原则：

> 代码不是为了看起来整洁。  
> 代码是为了让模型行为持续可理解。

---

## 1. 代码语义单元

深度学习实验代码有强先验。

基本规则：

```text
路径承担 pipeline 位置和工程责任。
模块名承担功能对象。
接口承担输入输出契约。
代码内容承担具体可运行机制。
配置承担实验条件。
测试、探针、可视化承担验证与显影。
W&B 承担证据记录。
md 承担解释和回流。
```

---

## 2. 推荐项目结构

```text
project/
├── AGENTS.md
├── README.md
├── configs/
│   ├── datasets/
│   ├── models/
│   ├── training/
│   ├── losses/
│   ├── augmentations/
│   ├── evaluation/
│   └── experiments/
├── src/
│   ├── contracts/
│   ├── datasets/
│   ├── transforms/
│   ├── models/
│   │   ├── backbones/
│   │   ├── encoders/
│   │   ├── necks/
│   │   ├── decoders/
│   │   └── heads/
│   ├── losses/
│   ├── metrics/
│   ├── training/
│   ├── evaluation/
│   ├── inference/
│   ├── visualization/
│   ├── runtime/
│   └── registry/
├── scripts/
├── tests/
├── probes/
├── analysis/
├── docs/
├── runs/
├── checkpoints/
└── external/
```

判断目录是否存在，不看常见程度。

看它是否承担稳定语义责任。

---

## 3. Pipeline 是第一组织对象

深度学习项目的核心不是单个模型类。

核心是 pipeline：

```text
raw input
  -> dataset adapter
  -> sample contract
  -> transform / collate
  -> model input
  -> backbone / encoder
  -> feature interface
  -> neck / fusion
  -> decoder / head
  -> prediction contract
  -> loss
  -> metric
  -> visualization
  -> run artifact
```

每个关键边界都应能回答：

- 输入是什么；
- 输出是什么；
- shape / dtype / value range 是什么；
- 是否需要梯度；
- 梯度是否真的流通；
- 失败会污染下游哪里；
- 如何测试；
- 如何可视化。

---

## 4. 多数据集必须通过 Sample Contract 统一

不同数据集可以有不同原始格式。

但进入训练 pipeline 前必须变成统一 sample contract。

```text
Raw Dataset A/B/C
  -> Dataset Adapter
  -> Sample Contract
  -> Transform / Collate
  -> Model Input Contract
```

sample contract 至少明确：

- image；
- mask / label；
- class id；
- ignore index；
- sample id；
- dataset id；
- original path；
- metadata；
- 坐标系；
- 空值策略。

原则：

> dataset adapter 负责差异，training pipeline 接收统一语义。

---

## 5. 模块变化分级

### 参数变化

例如 learning rate、batch size、loss weight、resolution。

进入：

```text
configs/
```

### 组合变化

例如 backbone、decoder、loss、augmentation 的替换或消融。

进入：

```text
configs/experiments/
src/registry/
```

### 能力变化

例如新增 decoder、dataset adapter、metric、loss。

进入：

```text
src/
tests/
docs/modules/
```

原则：

> 参数不改代码。  
> 组合不复制脚本。  
> 能力变化必须留下测试边界。

---

## 6. 测试和探针

测试证明结构可信，不证明效果好。

最小测试：

- config loading；
- dataset sample contract；
- collate；
- model forward shape；
- loss finite；
- gradient flow；
- metric computation；
- checkpoint save/load；
- minimal train step；
- visualization smoke test。

探针用于显影沉默失败：

```text
probes/check_dataset_sample.py
probes/check_mask_alignment.py
probes/check_model_forward.py
probes/check_gradient_flow.py
probes/check_prediction_distribution.py
```

沉默失败包括：

- 梯度断流；
- mask 全零；
- prediction 全背景；
- label 映射错位；
- loss NaN；
- feature range 漂移。

---

## 7. W&B 是主证据系统

W&B 是本工程的核心实验管理工具。

它负责记录：

- run；
- config；
- metrics；
- curves；
- images；
- masks；
- tables；
- artifacts；
- checkpoints；
- sweeps；
- registry。

但 W&B 不解释结果。

原则：

> W&B 记录发生了什么。  
> md 判断这说明什么。

### Run

一次训练、评估、推理或可视化任务。

对应：

```text
runs/<run_id>/
```

### Group

一个实验问题下的一组 runs。

例如：

```text
exp042_decoder_ablation
exp057_loss_weight_search
exp061_multi_dataset_transfer
```

### Sweep

只用于大规模搜索。

普通对比实验不要滥用 sweep。

### Artifacts

管理 dataset、split、processed data、checkpoint、prediction table 的版本和 lineage。

特别是 split 必须版本化。

### Tables / Media

用于诊断：

- image；
- ground truth；
- prediction；
- error map；
- failure tag；
- sample id。

### Registry

只放晋级产物。

不要把所有 checkpoint 放进 Registry。

只有通过 benchmark protocol 的 candidate、best、released model 才进入。

---

## 8. 常用生态能力

### timm

PyTorch 视觉模型库。

主要用于 backbone 和预训练权重。

应通过 adapter 接入：

```text
src/models/backbones/timm_backbone.py
```

不要让 timm 的内部 feature 格式泄漏到整个项目。

### Albumentations

计算机视觉数据增强库。

适合语义分割中的 image / mask 同步增强。

应通过：

```text
src/transforms/albumentations_adapter.py
configs/augmentations/
```

必须测试 mask 类别 id、ignore index、同步变换是否正确。

### MMSegmentation

主要作为参考生态。

用于学习 segmentation pipeline、decoder/head、benchmark 配置和评估习惯。

不要直接让项目依赖其内部结构。

---

## 9. 最高原则

> 稳定能力进入 src。  
> 实验条件进入 configs。  
> 执行动作进入 scripts。  
> 结构验证进入 tests。  
> 临时显影进入 probes。  
> 运行证据进入 runs 和 W&B。  
> 结果解释进入 docs。  
> 晋级产物进入 W&B Registry。  
> 外部参考进入 external。

如果代码只能跑出结果，却不能帮助我们理解模型行为，它还没有完成研究工程的使命。
