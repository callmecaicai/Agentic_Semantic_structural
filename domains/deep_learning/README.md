# Deep Learning Adapter

本 adapter 是 [kernel/](../../kernel/) 在深度学习实验工程中的具体化。

---

## 工件类型

本 adapter 假设项目包含以下工件载体:

| 载体 | 承担 |
|---|---|
| `src/` | 稳定能力代码 |
| `configs/` | 实验条件 |
| `data/` | 输入事实 |
| `runs/` | 运行证据 |
| `checkpoints/` | 权重资产 |
| `external/` | 外部参考(对手模型、论文官方实现等) |

完整路径表见 [path_table.md](path_table.md)。

---

## 耦合实例

kernel 的[语义对偶](../../kernel/semantic_duality.md)和[耦合原则](../../kernel/coupling_principle.md)在本 adapter 中实例化为两类对象。

### 稳定组件:一一对应

| kernel 元规则 | DL 实例 |
|---|---|
| 路径镜像 | `src/<a>/<b>/<c>.py` ↔ `docs/field/module_contracts/<a>/<b>/<c>.md` |
| 工件侧锚点 | Python docstring 顶部声明 `Doc:` / `Contract:` / `Verified:` |
| 文档侧锚点 | YAML front-matter:`covers`, `implements_contract`, `verified_by`, `last_audited`, `audit_hash` |
| 漂移审计 | [audit_coupling.py](audit_coupling.py) 扫 Python 文件计算 sha1 hash |
| 验证桥 | `tests/<...>.py` + `probes/<...>.py` + W&B 记录 |

典型粒度:

- 一个 backbone 类型 -> 一个 mirror doc。
- 一个 decoder/head 范式 -> 一个 mirror doc。
- 一个可插拔创新模块 -> 一个 mirror doc。
- 一个 dataset adapter -> 一个 mirror doc。
- 一个 loss / metric / transform -> 一个 mirror doc。

这些文档不按运行次数增量堆叠。代码变更触发审计;若语义变化未同步,生成 conflict。

### 训练事件:增量文件夹

每次训练执行都是一次 event instance,必须新增一个语义记录文件夹,不覆盖历史。

通用形态:

```text
docs/experiments/
└── YYYY-MM-DD_<exp_id>_<slug>/
    ├── index.md
    ├── dataset.md
    ├── training.md
    ├── components.md
    ├── config.md
    ├── results.md
    ├── analysis.md
    └── reflux.md
```

这里 `scripts/train1.py`、`datasets/my_dataset_1.py`、`configs/exp001.yaml`、backbone/head/module 组合共同构成同一次训练事件的输入,进入同一个实验语义文件夹。

不再额外区分 training_flow 过渡层;训练组织方式如果只在一次运行中出现,进入 event record。只有当某种训练组织方式稳定复用、可独立引用、可被组合时,才升级为稳定对象并建立 mirror doc。

---

## 全局契约

[pipeline_contracts.md](pipeline_contracts.md) 定义 DL pipeline 各边界的数据契约:
sample / transform / model input / feature / prediction / loss / metric / visualization。

每个 module contract 通过 `implements_contract` 字段指向某个 section。

---

## 模板

特化模板(在 [kernel/templates/](../../kernel/templates/) 之上派生):

| 模板 | 路径 |
|---|---|
| 实验文档(含 W&B 字段) | [templates/experiment.md](templates/experiment.md) |
| 模块契约(DL 特化,Python 字段) | [templates/module_contract.md](templates/module_contract.md) |

kernel 模板(conflict, decision, mirror_contract, semantic_record)仍直接可用。

---

## 审计

```bash
python domains/deep_learning/audit_coupling.py              # 检查
python domains/deep_learning/audit_coupling.py --update     # 更新 audit_hash
python domains/deep_learning/audit_coupling.py --no-conflicts  # 仅检查,不写 conflict
```

豁免列表:[coupling_exempt.txt](coupling_exempt.txt)。

---

## 第三方生态

DL 项目通常涉及:

- **W&B** —— 主证据系统;记录 run、metrics、artifacts、tables、registry。
- **timm** —— backbone 库;必须通过 adapter 接入,不让内部 feature 格式泄漏。
- **Albumentations** —— image/mask 同步增强;必须测试 mask 类别 id、ignore_index、变换同步。
- **MMSegmentation** —— 主要作为参考生态,不直接依赖。

详细规则见 [protocols_legacy/04_model_research_engineering.md](protocols_legacy/04_model_research_engineering.md) 的第 7-8 节。

---

## 协议遗产

旧版六个 protocol 保留在 [protocols_legacy/](protocols_legacy/),作为本 adapter 的历史层和详细规则参考(冻结,不修改)。

迁移说明见 [protocols_legacy/migration_from_legacy.md](protocols_legacy/migration_from_legacy.md)。
