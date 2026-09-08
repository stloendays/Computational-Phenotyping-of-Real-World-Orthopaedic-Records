# 腕舟骨主论文医生人工复核指南 v0.4

**本版本与 `SCAPHOID_ANALYSIS_PLAN_V0_3.md` 对齐。**

## 1. 研究问题

主问题：

> 在医生确认的腕舟骨手术病例中，established chronic/nonunion 相比 acute/new fracture 是否更多使用 bone-graft augmentation，而 internal fixation 在两组中仍然普遍存在？

次级探索问题：

> 在 established chronic/nonunion 内部，植骨病例是否具有更长的、病历明确记录的腕部受伤/症状持续时间？

医生只依据病历原文标注，不查看规则预测、duration parser、统计结果或当前分组。

---

## 2. Stage 1：88例候选先做解剖判定

每例选择一个：

- `wrist_scaphoid`
- `foot_navicular`
- `other`
- `uncertain`

可以综合诊断、主诉、查体、手术名称和手术记录中的**解剖上下文**。

关键原则：

- “手术”中的“手”不是手部解剖证据；
- 只有“舟骨骨折”但缺乏腕/足上下文时，不强行归类；
- 同次住院可能有多部位损伤，应判断舟骨本身的位置；
- 无法可靠判断时选择 `uncertain`。

Stage 1 完成、双重复核和裁决后先冻结 anatomy Gold，再生成 Stage 2。

---

## 3. Stage 2A：腕舟骨临床状态

只对 Stage-1 医生确认的 `wrist_scaphoid` 进行。

**只使用诊断、主诉、专科查体。不要用手术名称或手术记录判断状态。**

选择：

### `acute_or_new_fracture`

有明确证据支持本次为新鲜/近期骨折，例如“急性”“新鲜”或明确近期外伤后数小时、数天、数周。

### `established_chronic_fracture`

明确陈旧性/慢性舟骨骨折，但现有文字不足以确认骨不连。

### `established_nonunion`

明确写骨不连、骨折不连接、骨折不愈合或等同表达。

### `chronic_nonunion_not_distinguishable`

明确长期/陈旧问题，但不能可靠区分陈旧骨折与明确骨不连。

### `insufficient_or_uncertain`

现有非手术文本不足以确定以上状态。

### 重要分析规则

最终主临床比较直接使用：

- established chronic/nonunion：上述 chronic / nonunion 三类合并；
- comparison：**仅 `acute_or_new_fracture`**。

`insufficient_or_uncertain` 不进入状态相关临床推断。

没有另外一套“acute-only sensitivity”，因为 acute/new 本身就是最终主对照定义。

---

## 4. Stage 2B：腕舟骨相关病程时长

填写：

- `gold_relevant_duration_present = yes / no / uncertain`
- 如 yes：数值
- unit：`hours / days / weeks / months / years`
- basis：
  - `injury_since_event`
  - `wrist_symptom_duration`
  - `both`
  - `uncertain`

原则：

- 只记录能够明确归因于当前腕舟骨问题的时长；
- 若多个时长同时存在，记录最长的明确 index injury 或相关腕部症状时长；
- 数年前明确相关外伤 + 最近数天加重时，不用近期 flare 覆盖长期 index duration；
- “很久”“多年”但无法量化时，标 `uncertain`；
- 与其他疾病/其他部位相关的时长不使用；
- 自动 duration parser 的结果不会显示给医生。

示例：

- “1个半月” → value `1.5`, unit `months`
- “半年” → value `0.5`, unit `years`
- “1年半” → value `1.5`, unit `years`

最终统计连续分析时长，不要求医生判断任何 graft cutoff。

---

## 5. Stage 2C：手术是否真正针对腕舟骨

对 physician-confirmed wrist scaphoid 且具有详细手术记录的病例，先标：

`gold_target_disease_procedure_present = yes / no / uncertain`

- `yes`：手术明确治疗腕舟骨；
- `no`：详细记录实际治疗其他部位/疾病；
- `uncertain`：无法可靠判断。

通用词如“内固定”“螺钉”“钢针”本身不足以证明操作对象是舟骨。

---

## 6. Stage 2D：腕舟骨手术成分

仅在 procedure relevance = `yes` 时标：

### `gold_internal_fixation`

腕舟骨螺钉、空心钉、钢针/克氏针或其他明确内固定。

### `gold_bone_graft`

明确用于腕舟骨治疗的植骨或供骨获取。只有“取骨”但不能确认用于舟骨时，不标 yes。

### `gold_reconstruction`

明确属于腕舟骨治疗的重建性操作。

### `gold_fusion`

明确与该舟骨问题相关的融合/关节融合。

如果 target-disease procedure 明确存在，但某个具体成分无法可靠判断，可将该成分标 `uncertain`，不能自动当作 no。

---

## 7. 双人复核与裁决

约20%的每层记录由 Reviewer 2 独立复核。

Reviewer 2：

- 不看 Reviewer 1；
- 不看规则/LLM；
- 不看 duration parser；
- 不看研究效应量。

Reviewer-1 和 Reviewer-2 文件永久保留。系统另建 adjudication 文件：

- 未双重复核 → Reviewer-1 进入待冻结 Gold；
- 双重复核完全一致 → 一致结果进入待冻结 Gold；
- 任何不一致 → Gold 留空，由裁决医生重新判断。

最终临床分析只读取 adjudicated Gold。

---

## 8. 最重要原则

**只标病历明确支持的内容。**

宁可保留 `uncertain`，也不要为了增加病例数把证据不足者判成 acute/new、chronic/nonunion 或某个手术成分。人工复核的作用是确定固定数据支持什么，而不是让结果更显著。
