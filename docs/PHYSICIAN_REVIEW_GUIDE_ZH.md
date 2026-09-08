# 医生人工标注操作指南

> 本指南用于建立研究的 physician reference standard。标注者只根据原始病历文字进行判断，不查看规则系统、LLM、统计结果或其他标注者的答案。

## 一、基本原则

1. **每一行代表一次住院 episode，不是 Excel 原始行。**
2. 只依据当前行提供的病历证据，不根据经验补写病历中没有的信息。
3. “没写”与“明确没有”必须区分：
   - `undocumented`：病历没有提供可判断信息；
   - `absent/no`：病历明确否认或可以明确排除；
   - `uncertain`：有相关信息，但证据冲突或不足以安全判断。
4. 不使用规则系统或模型结果辅助标注。
5. 如果拿不准，优先标记 `uncertain` 并在 comment 中简要说明原因，不要为了凑完整标签强行二分。

---

# 二、文件 1：disease_anatomy_annotation.csv

该文件用于确认三个疾病候选队列的真正疾病/解剖部位。

## 1. 拇外翻

填写 `gold_disease_anatomy_label`：

- `yes`：病历明确存在拇外翻/踇外翻/拇囊炎等同义临床表型；
- `no`：候选记录实际上由其他疾病解释，且无拇外翻证据；
- `uncertain`：现有文字不足以判断。

不要因为患者接受了足部手术就自动判断为拇外翻。

## 2. 舟骨候选病例

填写：

- `wrist_scaphoid`：明确为腕舟骨/手舟骨；
- `foot_navicular`：明确为足舟骨；
- `other`：明确属于其他解剖或疾病实体；
- `uncertain`：只有泛称“舟骨”等，现有信息不能安全判断腕还是足。

### 特别注意

`手术`、`手法`中的“手”不能作为“手部/腕部”解剖证据。

能够支持腕舟骨的证据包括：

- 明确写“腕舟骨”“手舟骨”；
- “舟骨腰部/近极/远极”等典型腕舟骨描述；
- 同一句或局部语境明确把舟骨与腕部关联。

明确写“足舟骨”“足部舟骨”等，应判为 `foot_navicular`。

如果同一次多发伤同时存在足舟骨和腕舟骨，可以保留明确的腕舟骨诊断，不要因为存在足部损伤就抹掉腕舟骨。

## 3. 第一腕掌关节骨关节炎

填写：

- `yes`：明确累及第一腕掌关节/拇指 CMC/大多角骨-第一掌骨基底区域；
- `no`：明确是其他腕部关节病变；
- `uncertain`：只有“腕关节炎”“腕掌关节炎”等泛称，不能安全定位第一 CMC。

`gold_competing_diagnosis_labels` 可多选，用 `|` 分隔：

- `radiocarpal_arthritis`
- `ulnocarpal_arthritis`
- `rheumatoid_wrist`
- `gout_related_wrist`
- `traumatic_wrist_arthritis`
- `synovitis`
- `nonspecific_wrist_arthritis`
- `other`

---

# 三、文件 2：scaphoid_state_annotation.csv

只对已经进入腕舟骨候选的记录判断临床状态。

**重要：本文件只允许使用 diagnosis、complaint、physical examination 三类文字。不要用手术名称或手术记录反推疾病状态。**

填写 `gold_scaphoid_state`：

### `acute_or_new_fracture`

明确新鲜/急性/近期骨折，或者病历叙述非常明确符合急性骨折且没有慢性/骨不连证据。

### `established_chronic_fracture`

明确陈旧性/慢性骨折，但不足以确认特异性骨不连。

### `established_nonunion`

明确写骨不连、不连接、不愈合等。

### `chronic_nonunion_not_distinguishable`

可以确定属于陈旧/慢性/骨不连谱系，但当前文字不足以再细分。

### `insufficient_or_uncertain`

无法从允许的数据源安全判断。

同时填写 `evidence_source`，例如：

`diagnosis|complaint`

---

# 四、文件 3：procedure_annotation.csv

这是最需要注意的部分。必须分两步标注。

## 第一步：这份手术记录是否真的在治疗目标疾病？

填写：

`gold_target_disease_procedure_present`

允许值：

- `yes`
- `no`
- `uncertain`

### 为什么先做这一步？

一次住院可以同时存在多个疾病和多个手术。例如：

- 患者有拇外翻，但详细手术记录可能描述的是手指甲下肿物切除；
- 患者有腕舟骨骨折，但详细手术记录可能只描述桡骨远端固定。

此时不能因为患者“属于这个疾病队列”，就把另一处手术中的“切除”“钢针”“内固定”等词算成目标疾病手术。

判断时以**手术名称 + 手术正文的解剖和操作对象**为主。诊断列表只能作为背景，不能单独证明该手术治疗了目标疾病。

## 第二步：如果是目标疾病手术，再标手术组成

填写 `gold_procedure_labels`，多标签之间用 `|` 分隔。

### A. 拇外翻

允许标签：

- `osteotomy`
- `chevron`
- `akin`
- `scarf`
- `fusion`
- `k_wire`
- `resection`
- `soft_tissue`

`soft_tissue` 需要有明确的肌腱、韧带、关节囊、松解等软组织操作证据。仅出现与其他疾病相关的“软组织肿物”等不能标记。

### B. 腕舟骨

允许标签：

- `internal_fixation`
- `bone_graft`
- `reconstruction`
- `fusion`
- `hardware_removal`
- `debridement`

所有操作必须能够归因到舟骨治疗。

### C. 第一 CMC

允许标签：

- `trapeziectomy`
- `tendon_procedure`
- `ligament_procedure`
- `arthroplasty`
- `fusion`

---

# 五、reviewer_confidence

建议统一使用：

- `high`：病历证据直接、明确；
- `moderate`：可以判断，但存在一定解释空间；
- `low`：证据较弱，接近 uncertain。

如果 confidence 为 `low`，建议在 `reviewer_comment` 写一句理由。

---

# 六、双重复核

`double_review_manifest.csv` 已经用固定 hash 预先选定约 20% 的重复标注样本。

第二位标注者：

- 独立完成；
- 不看第一位医生答案；
- 不看规则/LLM结果；
- 不因为知道研究假设而调整判断。

完成后再进行一致性统计和必要的 consensus adjudication。

---

# 七、禁止事项

人工 gold 建立期间不要：

- 查看模型预测；
- 查看规则标签；
- 按统计显著性修改标签；
- 为了让病例数更整齐而把 uncertain 强行改成 yes/no；
- 用手术记录反向定义舟骨 chronic/nonunion 状态；
- 将“有详细手术记录”直接等同于“有目标疾病手术”。

---

# 八、完成标准

人工参考标准进入 freeze 前，应满足：

1. 所有 primary-review 行完成；
2. 预设 double-review 行独立完成；
3. disagreement 完成 adjudication；
4. uncertain/undocumented 的使用符合本指南；
5. gold 文件生成内部版本号/hash；
6. 完成 freeze 后，才允许运行正式规则 baseline 评分和 LLM benchmark。

这一顺序的目的，是确保模型不能反过来影响“正确答案”的定义。
