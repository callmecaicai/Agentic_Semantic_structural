# Object Detection Example

Virtual project: `remote-sensing-detection`, currently searching for a reliable baseline.

```text
remote-sensing-detection/
├── .agentic/
├── semantic/
└── workspace/
```

## workspace

```text
workspace/
├── configs/{datasets,models,train,experiments}/
├── src/{core,data,models,losses,metrics,engine,utils}/
├── scripts/{train.py,evaluate.py,sweep_baselines.py}
├── tests/
├── probes/
├── runs/
└── checkpoints/
```

Keep `train.py` thin. Prefer configs over `train1.py/train2.py` until the training logic is truly a different pipeline.

## semantic

```text
semantic/
├── field/
│   ├── contracts/
│   │   ├── detection_dataset_contract.md
│   │   ├── detection_pipeline_contract.md
│   │   └── evaluation_protocol.md
│   ├── mirrors/
│   └── baseline_board.md
└── records/{experiments,evaluations}/
```

Stable mirrors:

```text
workspace/src/models/detectors/faster_rcnn.py
  -> semantic/field/mirrors/workspace/src/models/detectors/faster_rcnn.md

workspace/src/metrics/coco_map.py
  -> semantic/field/mirrors/workspace/src/metrics/coco_map.md
```

Each training run:

```text
semantic/records/experiments/YYYY-MM-DD_exp001_dataset_a_frcnn/
├── index.md
├── input.md
├── process.md
├── output.md
├── analysis.md
└── reflux.md
```

Only after `reflux.md` is accepted should the result update `semantic/field/baseline_board.md`:

```text
| exp_id | dataset | model | backbone | schedule | mAP | AP50 | status | conclusion |
```

Suggested commands:

```bash
python agentic-structural-harness/scripts/harness.py init --root remote-sensing-detection
python agentic-structural-harness/scripts/harness.py new-artifact --root remote-sensing-detection workspace/src/models/detectors/faster_rcnn.py
python agentic-structural-harness/scripts/harness.py new-event --root remote-sensing-detection experiment --id exp001 --slug dataset_a_frcnn --trigger workspace/scripts/train.py
python agentic-structural-harness/scripts/harness.py audit --root remote-sensing-detection
```
