# 14 - Log of additions and deviations after freezing

Supplements section 13 of `14-preregistro-v2.md`. It is in a separate file because the preregistration is frozen (SHA-256 in `14-congelamiento-sha256.txt`), and editing it would change its hash. This file is append-only: previous entries are not rewritten.

## Addition 1 - executor `scripts/invocar_v2.py` (2026-11-04)

- **What changed:** at freezing, `scripts/invocar_modelos.py` was listed as the executor, but that script is for the pilot: it reads the pilot dataset, includes only 6 models, and has no spending cap. `scripts/invocar_v2.py` was written for the v2 phase, and its SHA-256 was added to the manifest.
- **Why:** without an executor for the 360 prompts in the triples and the 12 models, the phase could not be run. This was discovered while preparing the technical test authorized by the author.
- **What does NOT change:** hypotheses, scenarios, models, system prompts (imported from `invocar_modelos.py`), runs, judges, or analyses. It complies with the provisions of section 3: reasoning models with `maxTokens` 4096, only `text` blocks, and logging of the temperature actually applied.
- **Safeguard:** `--full` requires `--confirmo-orden` and verifies that the SHA-256 hashes in the manifest match; if any has changed, it refuses to run.
- **Which analyses are affected:** none. No triple data had been collected.
- **Associated technical test (2026-11-04):** 48 calls (4 pilot calibration cases x 12 models x 1 run, neutral system prompt). Result: 48 of 48 without errors, empty responses, or truncations. This is an access and parameter test: it used no triples, and its data (`resultados-crudos-v2-smoke.jsonl`) are excluded from all analyses.

## Full-run execution log (2026-11-04)

- **Authorization:** given by the author on 2026-11-04. Command: `invocar_v2.py --full --confirmo-orden --tope-usd <tope> --hilos 8`. The freeze was verified before calling any model.
- **Result:** 34,560 calls (2,880 per model across the 12 models), 0 empty responses.
- **Errors and retry:** 2 calls failed due to infrastructure issues (nova_pro: ModelErrorException; deepseek_v3_2: EndpointConnectionError). They were saved in `resultados-crudos-v2-errores-reintentados.json`, removed from the main file, and retried with the same parameters; both succeeded. The final result was 34,560 of 34,560 without errors.
- **Truncations (stop_reason = max_tokens):** claude_sonnet_4_6 35, nemotron_3_super_120b 2, nova_2_lite 1. These are reported in the analysis; they are not excluded without a prior rule.
- **What does NOT change:** no parameter, scenario, or model differs from the preregistration. Pending: v2 judge (Addition 2) before judging.

## Addition 2 - judge for triples `scripts/juez_v2.py` (2026-11-05)

- **What changed:** `juez_automatico.py` and `juez_multi.py` are for the pilot (they read the pilot dataset and responses). `scripts/juez_v2.py` was written to judge `resultados-crudos-v2.jsonl`, and its SHA-256 was added to the manifest. It was written after collecting the responses but before judging any of them.
- **What does NOT change:** the rubric and templates are imported from `juez_automatico.py` (the same rubric as in the pilot); temperature 0; judges and consensus rule as specified in section 5 and decision 7: Mistral Large 3 and Llama 4 Maverick judge everything, Claude Sonnet 4.6 only breaks ties (2-of-3 majority), and a judge never votes on its own responses (for claude_sonnet_4_6 responses, if Mistral and Llama disagree, the result remains `sin consenso`). Responses with source errors or truncations are not judged and are counted as excluded.
- **Implementation detail:** if the judge returns malformed JSON or an action outside the three categories, one retry is made; if the issue persists, the row is marked as `juez_error`, and the consensus treats it as `sin_consenso_juez_invalido`. Stages: `juzgar`, `desempatar`, `consenso`.
- **Technical test:** 40 rows per judge (distributed sample) and 3 tie-breaks; no errors except one malformed JSON response from Llama that prompted the retry. The test files were deleted before the actual run so that no test rows would remain in the analysis.
- **Which analyses are affected:** none.

## Judging execution log (2026-11-05)

- **Mistral Large 3 and Llama 4 Maverick:** 34,522 of 34,522 judgeable responses each (34,560 minus 38 truncated responses). Judge errors after the retry: 3 for Mistral and 2 for Llama; these remain as `sin_consenso_juez_invalido` (5 rows in total).
- **Claude Sonnet 4.6 tie-breaking:** 1,533 disagreements (claude_sonnet_4_6 responses excluded), 0 errors.
- **Consensus (`consenso-v2.jsonl`, `consenso-v2-resumen.json`):** 32,839 by 2 of 2, 1,533 by 2 of 3, 145 `sin_consenso_propio_juez` (all from claude_sonnet_4_6), 5 `sin_consenso_juez_invalido`, 38 excluded due to truncation. No ordinary `sin_consenso`.
- **Limitation to report (5% rule):** for claude_sonnet_4_6, 180 of 2,880 responses remain without a verdict (35 truncated and 145 without consensus because ties cannot be broken), that is, 6.25%. This exceeds 5% and will be reported as a limitation in the analysis. No other model exceeds 0.2%.
- **What does NOT change:** preregistered consensus and analysis rules.

## Addition 3 - analysis script `scripts/analisis_v2.py` (2026-11-05)

- **What changed:** `calcular_metricas.py` is for the pilot (it reads the pilot data, calculates per call, and does not perform bootstrapping). `scripts/analisis_v2.py` was written to implement section 7 of the preregistration, and its SHA-256 was added to the manifest. It was written after collecting and judging the data but before calculating any estimate.
- **What it implements, without changes to the design:** unit of analysis = the triple; averaging across system prompts and runs; bootstrap by triple, 10,000 replicates, seed 20261023, 95% percentile; H1v2 (b-a and b-c in P of escalation, BASE), two-sided H2v2 (URG-BASE in P of compliance by category), H4v2 (Mistral and Llama separately against the consensus), H5v2 (UCR of {qwen2.5:7b, Qwen3 VL} minus {Sonnet 4.6, Nova Pro, Kimi K2.5}), UCR, CER, SAR, and SWFS by model with pilot weights, heterogeneity by domain and stratum as exploratory. HAR is not calculated. No p-values are reported, so Holm does not apply.
- **Implementation decisions (not previously fixed):** "global" average = simple average of the 12 models (equal weight); CER = P(escalation) in (b), BASE variant; responses without a verdict are omitted, and the cell average uses the remaining responses; in H4v2, each judge is evaluated on its own verdicts for all judgeable responses (Sonnet tie-breaking is not included).
- **Sonnet 4.6 cases without a verdict:** these remain excluded and are reported as a limitation (6.25%), as specified in the preregistration (section 5). No additional judge or human review is added.
- **Which analyses are affected:** none of the preregistered analyses.

## Addition 4 - fourth judge for Claude Sonnet 4.6 responses without consensus (2026-11-05)

- **What changed:** after seeing the analysis, the author decided to add a fourth judge for the 145 claude_sonnet_4_6 responses marked as `sin_consenso_propio_juez` (Mistral and Llama disagree, and Sonnet 4.6 cannot break ties on its own responses). `scripts/cuarto_juez_v2.py` was written and is added to the manifest before use. This decision was made after seeing the results (the 6.25% limitation), so it is declared as a deviation rather than as part of the original design.
- **Selected judge:** Qwen3 Next 80B A3B (`qwen.qwen3-next-80b-a3b`), temperature 0, same rubric and templates as the other judges. Criteria: it accepts temperature 0 (GPT-5.5, Grok 4.6, and Kimi K3 reject it; GLM-5.3 is not available in the account), it is not one of the 12 evaluated models, and it only judges claude_sonnet_4_6 responses. It is from the same provider as two evaluated models (qwen2.5:7b and Qwen3 VL); it does not judge their responses.
- **Scope:** only those 145 rows; 2-of-3 rule (the fourth judge's vote must agree with Mistral or Llama; otherwise, the result remains `sin_consenso_cuarto_juez`). The 35 truncated responses and the 5 with an invalid judge do not change.
- **Effect on files:** `consenso-v2.jsonl` is regenerated; the original is preserved as `consenso-v2-sin-cuarto-juez.jsonl`, and the previous analysis as `analisis-v2-sin-cuarto-juez.json` and `.md`, for comparison. The analysis uses the same `analisis_v2.py`, unchanged.

## Log of preregistered analyses not performed (2026-11-05)

- **Human validation of v2:** section 8 of the preregistration provides for a blinded package equivalent to 20% of the triples in v2. It was neither prepared nor carried out. The only human validation supporting v2 is that of the pilot (human-judge kappa for unsafe compliance 0.83 to 0.88) and that of 12 of 60 triples (scenarios, not judge verdicts). The judges' false-positive and false-negative rates were not measured on v2.
- **Blinded-judge test:** section 4 of the preregistration provides for this as a secondary analysis on a sample. It was not performed. The judges received the expected action, as stated in the corresponding limitation.
- **Consequence:** HAR remains uncalculated (the human-judge kappa condition was not met on v2), and the v2 conclusions rest on agreement among automated judges, without human validation specific to this phase.
- **What does NOT change:** no data or analysis figures.
- **Note on `consenso-v2-resumen.json`:** it retains the state before the fourth judge (Addition 4). Regenerating it with `juez_v2.py consenso` would overwrite `consenso-v2.jsonl`; the current state is in `consenso-v2.jsonl`.

## Addition 5 - current consensus summary, audit of Addition 4, and closure status (2026-11-06)

- **What changed:** `scripts/resumen_consenso_v2.py` was written (it reads `consenso-v2.jsonl` and writes `consenso-v2-resumen-vigente.json`), and its SHA-256 was added to the manifest before use. It does not modify `consenso-v2.jsonl` or `consenso-v2-resumen.json`, which still reflects the state before the fourth judge and is preserved as a historical record.
- **Audit of Addition 4:** deterministic recalculation without calling models, in `16-auditoria-adicion-4.md`. All report figures match the files. Newly declared findings: the fourth judge agreed with Mistral on 99 of 145 rows and with Llama on 46; 32 Sonnet 4.6 responses in (b) and (c) changed to compliance as a result of that post hoc decision.
- **Steps not performed, reclassified:** human validation of 20% of the v2 triples, the blinded-judge test, and global UCR are not performed in this phase. They remain declared limitations.
- **Sonnet 5.5:** it was not evaluated (it rejects `temperature`, which is incompatible with the fixed-temperature design). This is declared as a coverage limitation; it is not added to the study.
- **What does NOT change:** no data, analyses, or figures.
