# Phenotype definition changelog

## v0.3 - explicit scaphoid anatomy uncertainty

Generation of the private physician-annotation packet exposed a second anatomy-specific error mode in the v0.2 wrist-scaphoid rule. The previous heuristic allowed the generic Chinese character `手` to contribute hand/wrist context. In long operative records this caused words such as `手术` (operation) and `手法` (manual manoeuvre) to generate false wrist-scaphoid evidence for explicit **foot navicular** cases.

A second review also showed the converse problem: some genuine wrist-scaphoid records use constructions such as `左腕桡骨、舟骨骨折` that are not captured by an exact `腕舟骨` phrase.

v0.3 therefore replaces the binary shortcut with a three-state anatomy classifier:

- `wrist_scaphoid` - high-specificity wrist/hand-scaphoid evidence, scaphoid waist/pole terminology, or generic scaphoid wording plus explicit wrist context in the absence of foot evidence;
- `foot_navicular` - explicit foot/navicular evidence without strong wrist-scaphoid evidence;
- `ambiguous` - generic `舟骨` wording that cannot be assigned safely.

`手术` and `手法` are explicitly prohibited from acting as hand-anatomy evidence. Genuine multi-site trauma may still retain a wrist-scaphoid phenotype when an explicit phrase such as `左手舟骨` is present alongside foot injury.

Consequences in the fixed 88-candidate scaphoid retrieval:

- **68** deterministic high-specificity wrist-scaphoid episodes;
- **13** explicit foot-navicular episodes;
- **7** anatomically ambiguous episodes reserved for physician adjudication;
- among the 68 strict wrist-scaphoid episodes, **23** carry an established chronic/nonunion phenotype from non-operative clinical text and **45** form the comparison group;
- detailed operative notes are available for **31** strict wrist-scaphoid episodes.

The previously reported 72-case scaphoid cohort is therefore superseded for primary analysis. It is retained in repository history as an audit trace rather than silently overwritten.

No rule was changed in response to a P value or treatment effect. The revision was triggered by discordance between independent pipeline components during annotation-packet generation.

## v0.2 - cohort-audit freeze

The v0.1 audit exposed a circularity risk in the scaphoid analysis: if chronic/nonunion status is allowed to be assigned from the operative note, then operative-note availability and treatment components can become mechanically associated with case status.

v0.2 therefore changes the scaphoid chronic/nonunion source scope to **diagnosis, complaint and physical-examination text only**. Operative names and operative-note contents remain available as downstream treatment phenotypes but cannot assign scaphoid case status in the treatment-comparison analysis.

At the v0.2 stage the then-current anatomy rule produced 72 wrist-scaphoid episodes, including 23 established chronic/nonunion phenotypes. That anatomy count is superseded by v0.3 after the later false-context audit described above.

The 2023-2025 period was prespecified as the internally consistent documentation-era sensitivity analysis because operative, examination and laboratory capture is markedly incomplete in 2019-2022.

## v0.1

Initial preregistration draft defining strict disease terms, anatomical disambiguation and procedure labels.
