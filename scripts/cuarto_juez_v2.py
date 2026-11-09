"""
Fase v2 - cuarto juez para las respuestas de claude_sonnet_4_6 sin consenso (Adicion 4 en 14-desviaciones.md).

Contexto: en juez_v2.py un juez no vota sobre sus propias respuestas, por lo que las 145 respuestas de
claude_sonnet_4_6 donde Mistral y Llama discrepan quedaron `sin_consenso_propio_juez`. Por decision del
el autor (2026-11-05) se agrega un cuarto juez, Qwen3 Next 80B A3B (temperatura 0, no es uno de los 12
modelos evaluados), que desempata SOLO esas filas con la misma rubrica y plantillas (mayoria 2 de 3).

Etapas:
  python cuarto_juez_v2.py juzgar      # escribe resultados-juzgados-v2-qwen3_next_80b.jsonl (reanudable)
  python cuarto_juez_v2.py consenso    # respalda consenso-v2.jsonl y lo regenera con el cuarto juez
"""
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez_v2 as j  # noqa: E402

JUEZ = "qwen3_next_80b"
# precio NO verificado en lista oficial: estimacion para el tope de gasto; el cierre real es la consola de facturacion
j.JUECES[JUEZ] = {"id": "qwen.qwen3-next-80b-a3b", "precio": (0.00015, 0.0012)}
CONS = os.path.join(j.DOCS, "consenso-v2.jsonl")
RESPALDO = os.path.join(j.DOCS, "consenso-v2-sin-cuarto-juez.jsonl")


def main():
    etapa = sys.argv[1] if len(sys.argv) > 1 else ""
    if etapa == "juzgar":
        ref = RESPALDO if os.path.exists(RESPALDO) else CONS
        claves = {(r["scenario_id"], r["modelo"], r["system_prompt"], r["run_idx"])
                  for r in j.leer(ref) if r["estado"] == "sin_consenso_propio_juez"}
        filas = [r for r in j.leer(j.CRUDOS) if j.clave(r) in claves]
        print(f"filas a juzgar: {len(filas)}")
        j.juzgar_filas(JUEZ, filas, j.cargar_prompts(), 5.0, 4)
    elif etapa == "consenso":
        if not os.path.exists(RESPALDO):
            shutil.copy(CONS, RESPALDO)
        q = {j.clave(r): r for r in j.leer(j.ruta_juez(JUEZ))}
        out, cuenta = [], {"2_de_3_cuarto_juez": 0, "sin_consenso_cuarto_juez": 0}
        for r in j.leer(RESPALDO):
            if r["estado"] == "sin_consenso_propio_juez":
                k = (r["scenario_id"], r["modelo"], r["system_prompt"], r["run_idx"])
                v = q.get(k, {}).get("accion_clasificada")
                r["cuarto_juez"] = v
                if v in (r["mistral"], r["llama"]):
                    r["accion_consenso"], r["estado"] = v, "consenso_2_de_3_cuarto_juez"
                    cuenta["2_de_3_cuarto_juez"] += 1
                else:
                    r["estado"] = "sin_consenso_cuarto_juez"
                    cuenta["sin_consenso_cuarto_juez"] += 1
            out.append(r)
        with open(CONS, "w", encoding="utf-8") as f:
            for r in out:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(json.dumps(cuenta, ensure_ascii=False))
    else:
        sys.exit("uso: cuarto_juez_v2.py juzgar|consenso")


if __name__ == "__main__":
    main()
