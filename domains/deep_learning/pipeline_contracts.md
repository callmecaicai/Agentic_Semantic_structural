# Pipeline Contracts

定义深度学习项目 pipeline 各边界的数据契约。

每个 module contract 通过 `implements_contract:` 字段指向本文件的具体 section。

---

## 1. 概览

```text
raw input
  -> [#sample-contract]       Dataset Adapter
  -> [#transform-contract]    Transform / Collate
  -> [#model-input-contract]  Model Input
  -> [#feature-contract]      Backbone / Encoder
  -> [#prediction-contract]   Decoder / Head
  -> [#loss-contract]         Loss
  -> [#metric-contract]       Metric
  -> [#visualization-contract] Visualization
```

每个边界必须回答: 输入是什么、输出是什么、shape/dtype/value range、是否需要梯度、失败如何向下游传播、如何测试。

---

## 2. Sample Contract <a id="sample-contract"></a>

`Dataset Adapter` 必须把任意原始格式转换为统一的 sample dict。

### 必含字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `image` | `np.ndarray` 或 `torch.Tensor`, HWC 或 CHW | 原始图像 |
| `mask` | `np.ndarray`,HW,int 或 float | 标签(分割任务) |
| `class_id` | int 或 None | 类别(分类任务) |
| `ignore_index` | int | 忽略像素的标记值,默认 255 |
| `sample_id` | str | 全局唯一,跨 dataset 不冲突 |
| `dataset_id` | str | 来源数据集标识 |
| `original_path` | str | 原始文件路径,便于回溯 |
| `metadata` | dict | 任意附加信息,不进入模型 |

### 不变量

- `image` 和 `mask` 的 H、W 必须对齐。
- `class_id` 与 `mask` 中出现的类别集合必须一致(分割中通过 mask 的 unique 验证)。
- `sample_id` 在整个项目内全局唯一。

### 验证

- `tests/datasets/test_sample_contract.py`
- `probes/check_dataset_sample.py`

---

## 3. Transform Contract <a id="transform-contract"></a>

`Transform / Collate` 接受 sample dict,输出模型可直接消费的 batch。

### 不变量

- image 和 mask 同步几何变换(crop、flip、rotate 必须同步)。
- ignore_index 在 mask 增强后保持不变(不被插值打乱)。
- 输出 batch 的 image 是 float tensor,mask 是 long tensor。

### 验证

- `tests/transforms/test_mask_alignment.py`
- `probes/check_mask_alignment.py`

---

## 4. Model Input Contract <a id="model-input-contract"></a>

进入模型 forward 的 tensor 契约。

| 张量 | shape | dtype | range |
|---|---|---|---|
| `image` | `[B, 3, H, W]` 或 `[B, T, 3, H, W]`(多时相) | float32 | 归一化后约 `[-3, 3]` |
| `mask` | `[B, H, W]` | int64 | 类别 id ∪ {ignore_index} |

H 和 W 必须能被 backbone 的最大 stride 整除。

---

## 5. Feature Contract <a id="feature-contract"></a>

`Backbone / Encoder` 输出特征。

### 规则

- 返回 dict 或有序 list,key/index 对应不同 stride 的 feature。
- 每个 feature shape `[B, C_i, H/s_i, W/s_i]`。
- 不暴露第三方库内部格式(timm、mmseg 的 feature 必须经 adapter 标准化)。

### 验证

- `tests/models/backbones/test_feature_shapes.py`

---

## 6. Prediction Contract <a id="prediction-contract"></a>

`Decoder / Head` 输出 prediction。

| 任务 | 输出 shape | dtype | 含义 |
|---|---|---|---|
| 语义分割 | `[B, num_classes, H, W]` | float32 logits | 未 softmax |
| 二值分割 | `[B, 1, H, W]` 或 `[B, H, W]` | float32 logits | 未 sigmoid |
| 变化检测 | `[B, 1, H, W]` | float32 logits | 未 sigmoid |
| 分类 | `[B, num_classes]` | float32 logits | 未 softmax |

### 不变量

- 不在模型内部做 softmax/sigmoid;loss 和 metric 内部处理。
- 输出 spatial size 与输入对齐(必要时上采样到原 H/W)。

---

## 7. Loss Contract <a id="loss-contract"></a>

### 规则

- 输入: prediction + target,均符合上述契约。
- 输出: scalar tensor,requires_grad=True。
- 必须 finite(NaN/Inf 触发训练终止)。
- 多 loss 加权返回 `{name: tensor, ...}` 加 `total`。

### 验证

- `tests/losses/test_loss_finite.py`
- `tests/losses/test_gradient_flow.py`
- `probes/check_gradient_flow.py`

---

## 8. Metric Contract <a id="metric-contract"></a>

### 规则

- 在 evaluation 流程中独立计算,不混入训练 loss。
- 每个 metric 必须实现 `update(pred, target)` 和 `compute() -> dict`。
- 输出 dict 的 key 形如 `<metric_name>/<subset>`,例如 `miou/val`。

---

## 9. Visualization Contract <a id="visualization-contract"></a>

### 规则

- 输入: image + ground truth + prediction(可选 error map)。
- 输出: 可写入 W&B Tables 或 Media 的工件。
- 必须包含 `sample_id` 以便追溯。

---

## 10. 多数据集统一

原则: dataset adapter 负责差异,training pipeline 接收统一语义。

```text
Raw Dataset A/B/C
  -> Dataset Adapter (A/B/C 各一)
  -> Sample Contract (统一)
  -> Transform / Collate
  -> Model Input Contract (统一)
```

类别映射在 adapter 中完成,不在 transform 或 loss 中。
ignore_index 在 adapter 中确定,不在下游修改。

---

## 11. 契约变化处理

修改本文件中任何 contract 必须:

1. 列出所有 `implements_contract:` 指向该 section 的 module contracts。
2. 同步更新这些 module contracts。
3. 同步更新对应测试。
4. 跑 `python domains/deep_learning/audit_coupling.py` 确认无遗漏。
5. 在 `docs/trace/decisions/` 写一份 ADR 说明为什么改。
