# 腕舟骨主论文医生人工复核指南 v0.3

## 目的

本次人工复核只服务于主论文的临床问题：

> 已建立的慢性/骨不连腕舟骨表型，是否与术中增加植骨成分有关，而内固定在两组中仍然普遍存在？

另有一个**预先冻结的探索性次级问题**：

> 在已经属于 established chronic/nonunion 的病例中，植骨病例是否具有更长的、病历明确记录的腕部受伤/症状持续时间？

次级问题不会替代 primary，也不会根据本地数据选择“最佳时长阈值”。

请按病历原文判断，不参考任何规则、模型预测、自动 duration parser、统计结果或当前分组。

---

## 为什么采用两阶段复核

最终临床队列不能由 deterministic rule 先决定，否则只复核规则判定为腕舟骨的病例会产生 verification bias。

因此人工复核分两阶段：

1. **Stage 1：88例舟骨候选全部做解剖判定。**
2. **Stage 2：只有 Stage 1 经医生确认的 `wrist_scaphoid` 病例，再生成临床状态、病程时长和手术复核表。**

Stage 2 的样本量由医生解剖 Gold 决定，不预设一定等于当前 deterministic 的68例。

---

# Stage 1：解剖部位复核

## 一、88例舟骨候选

每例只能选择一个主标签：

- `wrist_scaphoid`：明确为腕舟骨/手舟骨；
- `foot_navicular`：明确为足舟骨/足舟状骨；
- `other`：明确属于其他疾病或其他解剖部位；
- `uncertain`：现有文字不足以可靠判断。

### 可使用的信息

Stage 1 的任务只是判断解剖部位，可以综合：

- 诊断；
- 主诉；
- 专科查体；
- 手术名称；
- 手术记录中的解剖上下文。

此阶段不判断“急性/慢性/骨不连”，也不判断手术成分。

### 支持腕舟骨的证据

例如：

- 明确写“腕舟骨”“手舟骨”；
- “左腕/右腕 + 舟骨”；
- 舟骨腰部、近极、远极且上下文明显属于腕部；
- 鼻烟窝相关舟骨描述。

### 支持足舟骨的证据

例如：

- 足舟骨；
- 足舟状骨；
- 足背/跗骨/踝部上下文中的舟骨。

### 禁止推断

- “手术”中的“手”不能作为手部解剖证据；
- 只有“舟骨骨折”且无腕/足上下文时，不强行判腕舟骨；
- 同一次住院可能存在多部位损伤，应根据舟骨本身的上下文判断；
- 如果确实无法确定，选择 `uncertain`。

### Stage 1 完成条件

88例全部完成 anatomy label 后，冻结该文件，再由脚本根据 `gold_anatomy_label = wrist_scaphoid` 自动生成 Stage 2 标注包。

---

# Stage 2：医生确认腕舟骨后的临床状态、病程时长与手术复核

## 二、腕舟骨临床状态复核

Stage 2 的 state 表只包含 **Stage 1 经医生确认的 wrist-scaphoid 病例**。

判断状态时只使用：

- 诊断；
- 主诉；
- 专科查体。

**不要使用手术名称和手术记录判断临床状态。**

每例选择一个：

### 1. `acute_or_new_fracture`

有明确证据提示新鲜/近期骨折，例如：

- “急性”“新鲜”；
- 明确近期外伤后数小时、数天或数周；
- 文字整体明确描述本次新发骨折。

### 2. `established_chronic_fracture`

明确为陈旧性/慢性骨折，但没有足够文字确认已经达到骨不连定义。

### 3. `established_nonunion`

病历明确写骨不连、骨折不连接、骨折不愈合或等同表达。

### 4. `chronic_nonunion_not_distinguishable`

文字明确说明是长期/陈旧问题，但现有记录不足以可靠区分“陈旧骨折”还是已经明确骨不连。

### 5. `insufficient_or_uncertain`

不能根据现有诊断、主诉和查体可靠确定状态。

### 特别说明

- 没写“陈旧性”不等于急性；
- “术后”“取内固定”等术后信息不应自动被归入急性；
- 仅写“数月/数年”时，应结合完整语义判断；若无法确定，选择 `insufficient_or_uncertain`。

---

## 三、腕舟骨相关病程时长复核

这组字段用于**次级探索性分析**，自动 duration parser 的结果不会显示给医生。

### `gold_relevant_duration_present`

选择：

- `yes`：文本中存在明确、可归因于本次腕舟骨问题的受伤或腕部症状持续时间；
- `no`：没有可用的明确时长；
- `uncertain`：有时间表达，但无法确认是否属于腕舟骨问题或含义不清。

### `gold_relevant_duration_value`

仅当 `present = yes` 时填写数字，例如：

- `3`
- `1.5`
- `10`

不要自行统一换算成天。

### `gold_relevant_duration_unit`

仅当 `present = yes` 时选择：

- `hours`
- `days`
- `weeks`
- `months`
- `years`

例如：

- “1个半月” → value=`1.5`, unit=`months`
- “半年” → value=`0.5`, unit=`years`
- “1年半” → value=`1.5`, unit=`years`

### `gold_duration_basis`

选择：

- `injury_since_event`：从明确的相关外伤/受伤事件至当前；
- `wrist_symptom_duration`：腕部疼痛、肿胀、活动受限等症状持续时间；
- `both`：文本明确同时给出受伤时长和持续症状，且二者指向同一腕舟骨问题；
- `uncertain`：无法判断时长所代表的临床含义。

### 多个时长同时存在时怎么选

记录**最长的、能够明确归因于腕舟骨 index injury 或相关腕部症状的时长**。

如果病历同时写：

- 数年前腕部外伤；
- 最近几天疼痛加重；

只要数年前外伤明确与当前腕舟骨问题相关，应优先记录 index injury 的长期时长，而不是近期 flare。

如果无法确认哪个时间与舟骨相关，选择 `uncertain`，不要凭经验猜测。

### 为什么要人工复核

病历中的“1年半”“1个半月”“术后X月”“近期加重X天”等表达容易被简单正则误读，而且“有时间”不代表“这个时间就是舟骨病程”。因此最终论文只使用医生确认的相关时长。

---

## 四、手术记录是否属于腕舟骨治疗

Stage 2 的 procedure 表只包含 **医生确认的 wrist-scaphoid 病例中，确有详细手术记录模块的病例**。

首先判断：

`gold_target_disease_procedure_present`

- `yes`：手术内容明确治疗腕舟骨；
- `no`：详细手术记录实际治疗其他部位/其他疾病；
- `uncertain`：现有手术记录不足以判断。

病历中出现“内固定”“钢针”“切除”等通用手术词，不能单独证明该操作针对腕舟骨。

---

## 五、腕舟骨手术成分

仅在 `target_disease_procedure_present = yes` 时标注。

### `internal_fixation`

出现针对腕舟骨的螺钉、空心钉、钢针/克氏针或其他明确内固定。

### `bone_graft`

出现针对腕舟骨治疗的植骨，或取髂骨/桡骨等供骨并明确用于舟骨。

仅仅出现“取骨”但无法确认用于舟骨时，不标 yes。

### `reconstruction`

明确写重建性操作，且属于腕舟骨治疗的一部分。

### `fusion`

明确存在融合/关节融合，并属于该舟骨相关治疗。

---

## 六、主论文最关键的人工标签

Primary 结论最依赖：

1. 是否 wrist scaphoid；
2. 是否 established chronic/nonunion；
3. 手术记录是否真正属于腕舟骨治疗；
4. 是否 internal fixation；
5. 是否 bone graft。

Secondary duration 结论额外依赖：

6. 是否有明确相关病程；
7. 时长数值与单位；
8. 时长代表 injury duration 还是 wrist symptom duration。

如果文字不足，请选择 `uncertain`，不要依据经验补全病历没有写出的事实。

---

## 七、主分析与敏感性分析

主分析比较：

- established chronic/nonunion；
- 其他 physician-adjudicated、非 established chronic/nonunion 的 classifiable wrist-scaphoid comparison records。

预先规定的 acute-only 敏感性分析：

- established chronic/nonunion；
- **仅 physician-confirmed `acute_or_new_fracture`**。

探索性 duration 分析：

- 仅限 physician-confirmed established chronic/nonunion；
- 仅限 disease-concordant detailed operative records；
- 比较 bone graft yes vs no 的 physician-adjudicated relevant duration；
- 不根据本地数据寻找“最佳 cutoff”。

---

## 八、第二复核者

Stage 1 和 Stage 2 均约20%的记录由第二位医生独立复核。

第二位复核者：

- 不看第一位医生标签；
- 不看规则/LLM结果；
- 不看自动 duration parser；
- 不看当前统计关联；
- 独立完成相同标签。

不一致病例由预先指定的高级别医生或共识讨论完成最终裁决。

---

## 九、复核原则总结

**只标病历明确支持的内容。**

本研究宁愿保留 `uncertain`，也不为了样本量强制二分。人工复核的目的不是让结果更显著，而是确定现有数据究竟能支持什么结论。
