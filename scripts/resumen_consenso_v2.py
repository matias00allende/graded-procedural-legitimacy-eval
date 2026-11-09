"""
Fase v2 - resumen de consenso vigente (Adicion 5 en 14-desviaciones.md).
Lee consenso-v2.jsonl (con cuarto juez) y escribe consenso-v2-resumen-vigente.json
(conteo por modelo y estado). No modifica consenso-v2.jsonl ni consenso-v2-resumen.json.
Uso: python scripts/resumen_consenso_v2.py
"""
import json
import os
from collections import Counter, defaultdict

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
res = defaultdict(Counter)
for linea in open(os.path.join(DOCS, "consenso-v2.jsonl"), encoding="utf-8"):
    r = json.loads(linea)
    res[r["modelo"]][r["estado"]] += 1
salida = {m: dict(c) for m, c in res.items()}
json.dump(salida, open(os.path.join(DOCS, "consenso-v2-resumen-vigente.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("OK", sum(sum(c.values()) for c in res.values()), "respuestas")
