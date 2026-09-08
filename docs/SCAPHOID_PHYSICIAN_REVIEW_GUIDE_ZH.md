# 腕舟骨主论文医生人工复核指南 v0.4

## 目的

本次人工复核只服务于一个临床问题：

> **在医生确认的腕舟骨手术病例中，与急性/新鲜腕舟骨骨折相比，已建立的慢性骨折/骨不连是否更常加入植骨，而内固定在两组中仍然普遍存在？**

另有一个预先冻结的探索性次级问题：

> 在已经属于 established chronic/nonunion 的病例中，植骨病例是否具有更长的、病历明确记录的腕部受伤/症状持续时间？

请只按病历原文判断，不参考规则、模型预测、自动 duration parser、当前统计结果或现有分组。

---

# 一、为什么采用两阶段复核

最终临床队列不能由 deterministic rule 先决定，否则只复核规则阳性病例会产生 verification bias。

因此：

1. **Stage 1：88例宽泛“舟骨”候选全部进行解剖判定。**
2. **Stage 2：仅对 Stage 1 经医生确认的 `wrist_scaphoid` 病例生成状态、时长和手术复核表。**

Stage 2 样本量由医生 Gold 决定，不预设等于当前规则得到的68例。

---

# 二、Stage 1：解剖部位

每例只能选择一个标签：

- `wrist_scaphoid`：明确为腕舟骨/手舟骨；
- `foot_navicular`：明确为足舟骨/足舟状骨；
- `other`：明确为其他疾病或其他部位；
- `uncertain`：现有文本不足以可靠判断。

可综合诊断、主诉、专科查体、手术名称和手术记录中的解剖上下文。

支持腕舟骨的典型证据包括：

- 明确写“腕舟骨”“手舟骨”；
- “左腕/右腕 + 舟骨”；
- 舟骨腰部、近极、远极且上下文明显属于腕部；
- 鼻烟窝相关描述。

支持足舟骨的典型证据包括：

- 足舟骨/足舟状骨；
- 足背、跗骨、踝部等明确足部上下文中的舟骨。

注意：

- “手术”中的“手”不能作为手部解剖证据；
- 仅写“舟骨骨折”且没有腕/足上下文时，不强行判为腕舟骨；
- 同一次住院可能存在多部位损伤，应根据舟骨本身的上下文判断；
- 无法确定时选择 `uncertain`。

Stage 1 完成并裁决后先冻结 anatomy Gold，再生成 Stage 2。

---

# 三、Stage 2：腕舟骨临床状态

只使用：

- 诊断；
- 主诉；
- 专科查体。

**不要使用手术名称和手术记录判断临床状态。**

每例选择一个：

### `acute_or_new_fracture`

有明确证据支持本次为新鲜/近期腕舟骨骨折，例如：

- “急性”“新鲜”；
- 明确近期外伤后数小时、数天或数周；
- 整体语义清楚描述本次新发骨折。

### `established_chronic_fracture`

明确为陈旧性/慢性骨折，但不足以确认骨不连。

### `established_nonunion`

明确写骨不连、骨折不连接、骨折不愈合或同义表达。

### `chronic_nonunion_not_distinguishable`

明确为长期/陈旧问题，但现有记录不足以可靠区分陈旧骨折和骨不连。

### `insufficient_or_uncertain`

现有诊断、主诉和查体不足以可靠确定状态。

重要原则：

- 没写“陈旧性”**不等于**急性；
- “术后”“取内固定”等术后信息不自动归入急性；
- 仅有模糊病程、无法确认本次是否新发时，选择 `insufficient_or_uncertain`；
- 不为了扩大对照组而把证据不足病例归为 acute/new。

## 主分析的状态分组

最终主分析只比较：

- **established chronic/nonunion**：`established_chronic_fracture`、`established_nonunion`、`chronic_nonunion_not_distinguishable`；
- **acute/new**：`acute_or_new_fracture`。

`insufficient_or_uncertain` 不进入主要状态比较。

因此，本研究**不再设置一个与主分析重复的“acute-only sensitivity analysis”**。急性/新鲜骨折本身就是最终主对照组。

---

# 四、腕舟骨相关病程时长

这组字段用于探索性次级分析，自动 duration parser 的结果不会显示给医生。

### `gold_relevant_duration_present`

- `yes`：有明确、可归因于当前腕舟骨问题的受伤或腕部症状持续时间；
- `no`：没有可用明确时长；
- `uncertain`：存在时间表达，但无法确认其临床含义或是否属于腕舟骨问题。

### `gold_relevant_duration_value`

仅 `present=yes` 时填写数值，不自行换算成天。

### `gold_relevant_duration_unit`

- `hours`
- `days`
- `weeks`
- `months`
- `years`

例如：

- “1个半月” → `1.5 months`
- “半年” → `0.5 years`
- “1年半” → `1.5 years`

### `gold_duration_basis`

- `injury_since_event`
- `wrist_symptom_duration`
- `both`
- `uncertain`

如果同时存在较早 index injury 与近期症状加重，且较早外伤明确与当前腕舟骨问题相关，应记录较长的 index-injury / related-symptom duration；若归因不清，选择 `uncertain`。

最终论文只使用医生确认的时长。自动 parser 仅用于预验证工程审计。

---

# 五、手术记录是否真正属于腕舟骨治疗

procedure 表只包含医生确认的腕舟骨病例中存在详细手术记录模块的病例。

首先判断：

`gold_target_disease_procedure_present`

- `yes`：该详细手术记录明确治疗腕舟骨；
- `no`：该记录实际治疗其他部位/疾病；
- `uncertain`：无法可靠判断。

出现“内固定”“钢针”“切除”等通用词不能单独证明手术针对腕舟骨。

---

# 六、腕舟骨手术成分

仅在 `target_disease_procedure_present=yes` 时标注。

### `gold_internal_fixation`

针对腕舟骨的螺钉、空心钉、钢针/克氏针或其他明确内固定。

### `gold_bone_graft`

明确进行植骨，或取髂骨/桡骨等供骨并明确用于腕舟骨治疗。

### `gold_reconstruction`

明确写重建性操作且属于腕舟骨治疗的一部分。

### `gold_fusion`

明确存在融合/关节融合且属于舟骨相关治疗。

对每个成分使用 `yes / no / uncertain`。如果 procedure relevance 不是 `yes`，这些成分字段应留空。

---

# 七、主论文最关键的人工标签

Primary conclusion 依赖：

1. 是否 `wrist_scaphoid`；
2. 是否 `acute_or_new_fracture` 或 established chronic/nonunion；
3. 手术记录是否真正属于腕舟骨治疗；
4. 是否 internal fixation；
5. 是否 bone graft。

Secondary duration conclusion 额外依赖：

6. 是否存在明确相关病程；
7. 时长数值与单位；
8. 时长代表 injury duration 还是 wrist symptom duration。

文字不足时选择 `uncertain`，不要根据经验补全病历没有写出的事实。

---

# 八、第二复核者与最终裁决

Stage 1 和 Stage 2 均约20%的记录由第二位医生独立复核。

第二位复核者：

- 不看第一位医生标签；
- 不看规则/LLM结果；
- 不看自动 duration parser；
- 不看当前统计关联；
- 独立完成相同标签。

Reviewer 1 与 Reviewer 2 的原始标签必须保留。双复核一致的病例可进入待冻结 Gold；不一致病例不得自动多数表决，必须由预先指定 adjudicator 或共识讨论裁决。

---

# 九、复核完成后的分析边界

主分析：

> physician-confirmed established chronic/nonunion vs physician-confirmed acute/new fracture → bone-graft augmentation。

关键对照结果：internal fixation。

次级结果：augmentation composite、major component count。

探索性次级机制分析：

> established chronic/nonunion 内部，bone graft yes vs no 的 physician-adjudicated relevant duration。

不会根据本地数据寻找最佳 duration cutoff。

本研究不回答：未来骨不连风险、术后愈合、治疗疗效、哪种植骨方式更优或因果治疗选择。

---

## 总原则

**只标病历明确支持的内容。**

本研究宁愿保留 `uncertain`，也不为了样本量强制二分。人工复核的目的不是让结果更显著，而是确定现有数据究竟能支持什么结论。
