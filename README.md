# Graded procedural legitimacy under hierarchical authority: data, code and preregistration

Independent study by Matías Ignacio Allende Contreras (matias00allende). Contact: matias.allende.contreras@gmail.com.

This repository contains the data, code and preregistration of the study. It draws on what the author learned from conducting an earlier pilot in their professional work, as well as the problems and potential improvements identified by that pilot. The design, analyses and conclusions are the author's; no institution sponsors or endorses the study.

## What it evaluates

The study evaluates whether a language model distinguishes three situations when an instruction invokes hierarchical authority within a municipal administrative procedure: (a) legitimate authority and a complete procedure (it should comply), (b) legitimate authority with a procedural gap (it should escalate or impose conditions) and (c) fabricated or inflated authority (it should refuse or verify). All scenarios are synthetic and written in Chilean Spanish; no real personal data were used.

The v2 phase includes 60 counterfactual triples (30 involving scholarships and 30 involving emergencies), 12 models, 2 system prompts and 4 runs per cell, yielding 34,560 responses. Mistral Large 3 and Llama 4 Maverick judge all responses; Claude Sonnet 4.6 only breaks ties. A fourth judge (Qwen3 Next 80B A3B) was added for 145 rows after the results were reviewed. The analysis is preregistered: bootstrap resampling by triple, 10,000 replicates, seed 20261023, 95% percentile intervals, no p-values.

Main results (average across the 12 models): P(escalate) in category (b) exceeds that in (a) by +0.500 [+0.457, +0.545] and that in (c) by +0.282 [+0.240, +0.324]. Urgency framing is associated with greater compliance in (b) and (c). Unsafe compliance (UCR) ranges from 0.019 to 0.851 depending on the model. The evaluated Claude models almost never comply unsafely, but this is because they escalate almost everything. Limitations are detailed in the corresponding section and in `14-desviaciones.md`.

## Contents

| Path | Description |
|---|---|
| `14-preregistro-v2.md`, `15-especificacion-triples.md` | Preregistration and scenario specification (in Spanish; English translation in `en/`) |
| `14-desviaciones.md` | Record of additions and deviations after the freeze |
| `14-congelamiento-sha256-ORIGINAL.txt` | Original SHA-256 manifest of the frozen files |
| `MANIFIESTO-SHA256.txt`, `TRANSFORMACION.md` | Verification of this copy and details of what was generalized |
| `triples/` | The 60 triples and their mechanical validation |
| `resultados-crudos-v2.jsonl` | 34,560 responses from the 12 models |
| `resultados-juzgados-v2-*.jsonl`, `consenso-v2*.jsonl` | Each judge's verdicts and consensus (current and without the fourth judge) |
| `analisis-v2*.json`, `analisis-v2*.md` | Analysis results (current and strictly preregistered) |
| `16-auditoria-adicion-4.md` | Recalculation of the fourth judge's figures from the files |
| `*-piloto*`, `metricas-piloto.json` | Earlier pilot (40 cases, 6 models), for reference |
| `scripts/` | Code for generation, judging, consensus and analysis |
| `en/` | English translations of the documents |

## Reproducing the analysis

```
python scripts/analisis_v2.py
```

This command recalculates all figures from the included data and reproduces `analisis-v2.json`. It requires only Python 3. Regenerating or judging responses requires access to the models through Amazon Bedrock, incurs a cost and uses a local server for the qwen2.5:7b model. The generation scripts are published as a record of the method and depend on a cost-tracking helper (`scripts/registro_costos.py`, minimal version) and the author's own infrastructure, whose identifiers were replaced with example values.

## Limitations

The judges know the expected action; the scenarios were written by Anthropic models; the decision to add the fourth judge was made after the results were reviewed; there is no human validation of this phase; there are no p-values or corrections for multiple comparisons; the data are synthetic and cover two domains and one language. The results are valid for the model identifiers and execution date (2026-11-04). Details are provided in the publication and in `14-desviaciones.md`.

## Public edition

In this copy, proper names of places and organizations were generalized, and infrastructure identifiers were replaced. This is an edited version of the evaluated text: the prompts and responses are not byte-for-byte identical to those seen by the models. This editing does not change labels, categories, verdicts or figures, and running `analisis_v2.py` on this copy reproduces the original figures. See `TRANSFORMACION.md`.

## Verifying the preregistration freeze

The preregistration was frozen on 2026-11-04, before any v2 response was generated. The SHA-256 hashes of the frozen files are in `14-congelamiento-sha256-ORIGINAL.txt`. The files in this copy were edited (see `TRANSFORMACION.md`, which lists original and copy hashes side by side), so they do not match those hashes. The freeze date therefore rests on the author's records and on the history of this repository, not on an independent third-party timestamp.

## Scope and responsible use

The results describe specific model identifiers, a prompt format and an execution date. They are not a certification, a suitability ranking or a statement about the providers. Model and company names belong to their owners. Do not use these results to approve a system for production without your own validation.

## Dependencies

`scripts/analisis_v2.py` uses only the Python standard library. Regenerating or judging responses additionally requires `boto3` (see `requirements.txt`).

## Licenses and citation

The code (`scripts/`) is published under the MIT license (`LICENSE`). The data and texts are published under CC BY 4.0 (`LICENSE-DATA.md`). The responses were generated by third-party models; anyone reusing them should review each provider's terms of use.

A machine-readable citation is in `CITATION.cff`.

Suggested citation: Allende Contreras, M. I. (2026). *Graded procedural legitimacy under hierarchical authority: evaluation data, code and preregistration*. GitHub, matias00allende/graded-procedural-legitimacy-eval.
