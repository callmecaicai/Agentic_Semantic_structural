---
name: coupling-principle
description: 工件 ⇄ 镜像文档,双向锚点,漂移审计,验证桥;任何持续推进的对象都必须有这套耦合。
metadata:
  kernel_rule: D
---

# 耦合原则

任何被持续推进的工件都必须有镜像文档与其相互绑定。这是 md 语义管理和工件推进机制相接的元规则。

本文件处理 [semantic_duality.md](semantic_duality.md) 中的第一组对偶:稳定工件 ⇄ 固定镜像文档。一次发生 ⇄ 增量语义记录文件夹由 semantic_duality 统一描述。

---

## 四件套

| 件 | 在工件侧 | 在文档侧 |
|---|---|---|
| **路径镜像** | 工件路径决定镜像 doc 路径 | 镜像 doc 路径决定它覆盖哪个工件 |
| **锚点** | 工件文件开头声明指向镜像 doc | 镜像 doc front-matter 声明 covers / verified_by |
| **漂移审计** | 工件被修改时 hash 改变 | front-matter 中存 `audit_hash`;审计比对 |
| **验证桥** | 测试 / 探针 / 度量 / 复现脚本 | front-matter `verified_by` 字段指向这些验证物 |

四件套缺一,工件就漂移成了**没有解释的事实**,文档就漂移成了**没有事实的解释**。

---

## 1. 路径镜像

每条工件路径 → 一条镜像 doc 路径。具体映射规则由 domain adapter 定义。

通用形式:
- 工件: `<work_root>/<a>/<b>/<c>.<ext>`
- 镜像: `<doc_root>/<mirror_class>/<a>/<b>/<c>.md`

例:
- 代码 adapter:`src/x/y/z.py` ↔ `docs/field/module_contracts/x/y/z.md`
- 论文 adapter:`sections/intro.tex` ↔ `docs/field/section_contracts/intro.md`
- 训练 adapter:`programs/week_03.md` ↔ `docs/field/cycle_contracts/week_03.md`

### 规则
- 新建工件 → 必须同步建镜像 doc(可只含 front-matter)。
- 删除工件 → 镜像 doc 移至 `_removed/`(冻结)。
- 镜像缺失由审计检测,产出 conflict。

### 豁免
某些工件不需要 doc(例如纯包装、自动生成、纯样板)。豁免清单单独维护,一行一条,由 adapter 决定。

---

## 2. 锚点

### 工件侧锚点

每个工件文件开头必须可机器解析地声明:

```
Doc:      <镜像 doc 路径>
Contract: <可选:实现的全局契约 section>
Verified: <验证物路径列表>
```

声明方式由工件类型决定(Python docstring、Markdown front-matter、LaTeX 注释块、YAML 头部等)。但字段名和顺序应在 adapter 中固定。

### 文档侧锚点

每个镜像 doc 以 front-matter 开头:

```yaml
---
covers:
  - <工件路径>
implements_contract: <可选:指向全局契约 section>
verified_by:
  - <验证物路径>
last_audited: YYYY-MM-DD
audit_hash: <7-char hash of covered artifact at last audit>
---
```

---

## 3. 漂移审计

审计脚本扫描全部已登记工件 + 镜像 doc 对,检测:

| 检测项 | 触发 | conflict 类型 |
|---|---|---|
| 镜像缺失(工件侧) | 工件存在,doc 不存在 | `uncovered-artifact` |
| 镜像缺失(文档侧) | doc 的 `covers` 指向不存在的工件 | `orphan-doc` |
| front-matter 缺失 | doc 无 `---` 块 | `no-front-matter` |
| covers 缺失 | front-matter 无 covers | `no-covers` |
| verified_by 不存在 | 引用的验证物不在磁盘 | `missing-verifier` |
| audit_hash 缺失 | doc 无法检测工件漂移 | `no-audit-hash` |
| 工件漂移 | 当前 hash ≠ doc 中 `audit_hash` | `artifact-vs-doc` |

每个检测到的问题在 conflicts 区产生一个文件。详见 [conflict_mechanism.md](conflict_mechanism.md)。

### 命令

每个 adapter 应提供自己的审计实现。通用接口:

```text
audit          # 检查;有漂移则非零退出
audit --update # 审计通过后更新 audit_hash
```

集成位置:
- pre-commit hook(推荐)
- CI 强制
- 任一 locate / reflux 动作完成后

---

## 4. 验证桥

文档中的契约声明(Rule、Input、Output、Invariant 等)必须有对应验证物。

通用要求:
- doc 写"输入形状 X" → 验证物有对应断言。
- doc 写"必须有限" → 验证物有 finite 检查。
- doc 写"梯度必须流通"或"引用必须存在"等 → 对应探针检测。

审计不必解析自然语言契约,但 `verified_by` 中声明的验证物文件必须存在。验证物的有效性(它是否真的检查了 doc 声明的契约)由用户裁决。

---

## 5. 工作流

### 新增工件
1. 在工件路径创建文件,加锚点。
2. 在镜像路径创建 doc,含 front-matter + body(可空)。
3. 在验证物路径创建对应 test/probe,确保 `verified_by` 指向有效。
4. 跑 `audit --update`,写入初始 audit_hash。

### 修改工件
1. 修改工件。
2. 跑 `audit`,会报 `artifact-vs-doc`。
3. 决策:
   - 语义未变 → 跑 `--update` 更新 hash。
   - 语义已变 → 同步改 doc,再跑 `--update`。
4. 验证通过后提交。

### 删除工件
1. 删除工件文件。
2. 把对应 doc 移至 `_removed/`,顶部加 `# REMOVED on YYYY-MM-DD`。
3. 清理 `verified_by` 中已不需要的验证物(或保留供回归)。
4. 跑审计确认无 orphan。

---

## 6. 全局契约 vs 单体契约

- **单体契约**(镜像 doc):一个工件一份,说明这个对象做什么。
- **全局契约**(管线/流程契约):跨多个工件的统一接口规范。

单体契约通过 `implements_contract` 字段指向全局契约的具体 section。

是否需要全局契约由 adapter 决定:
- 某些工程型 adapter 通常需要跨工件契约(例如数据边界、输入/输出、度量或验证边界)。
- 单文件论文写作可能不需要。
- 训练计划可能需要(一次 cycle 的接口规范)。

全局契约修改时:
1. 列出所有 `implements_contract` 指向该 section 的单体契约。
2. 同步更新。
3. 同步更新对应验证物。
4. 跑审计。
5. 在 decisions 写 ADR 说明为什么改。
