"""
Fase v2 - juez para los triples (preregistro 14, seccion 5; Adicion 2 en 14-desviaciones.md).

Misma rubrica y plantillas que juez_automatico.py (se importan, no se copian). Diseno decidido
el 2026-10-30: Mistral Large 3 y Llama 4 Maverick juzgan TODAS las respuestas; Claude Sonnet 4.6
solo desempata cuando discrepan (equivale a mayoria 2 de 3). Un juez nunca vota sobre sus propias
respuestas: para respuestas de claude_sonnet_4_6 no hay desempate y, si Mistral y Llama discrepan,
queda `sin consenso`. Respuestas con error de origen o truncadas (stop_reason max_tokens) no se
juzgan: se excluyen y se cuentan (seccion 5).

Etapas (cada una append-only y reanudable, con tope de gasto):
  python juez_v2.py juzgar --juez mistral_large_3 [--limite N] [--tope-usd N]
  python juez_v2.py juzgar --juez llama4_maverick
  python juez_v2.py desempatar          # Sonnet 4.6, solo filas con discrepancia
  python juez_v2.py consenso            # escribe consenso-v2.jsonl y un resumen

Entradas: resultados-crudos-v2.jsonl y triples/*-borrador.json (texto de cada prompt).
Salidas: resultados-juzgados-v2-<juez>.jsonl, consenso-v2.jsonl, consenso-v2-resumen.json.
"""
import argparse
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import boto3
from botocore.exceptions import ClientError

AQUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(AQUI, "..")
sys.path.insert(0, AQUI)
import juez_automatico as base  # noqa: E402

CRUDOS = os.path.join(DOCS, "resultados-crudos-v2.jsonl")
# USD por 1.000 tokens (entrada, salida), de juez_multi.py y costo_fase_d.py
JUECES = {
    "mistral_large_3": {"id": "mistral.mistral-large-3-675b-instruct", "precio": (0.00025, 0.0015)},
    "llama4_maverick": {"id": "us.meta.llama4-maverick-17b-instruct-v1:0", "precio": (0.00024, 0.00097)},
    "claude_sonnet_4_6": {"id": "us.anthropic.claude-sonnet-4-6", "precio": (0.0033, 0.0165)},
}
ACCIONES = {"cumplir", "escalar_condicionar", "rechazar_verificar"}
REINTENTOS = 5


def clave(r):
    return (r["scenario_id"], r["modelo"], r["system_prompt"], r["run_idx"])


def ruta_juez(j):
    return os.path.join(DOCS, f"resultados-juzgados-v2-{j}.jsonl")


def cargar_prompts():
    p = {}
    for arch in ("becas-borrador.json", "emergencia-borrador.json"):
        for t in json.load(open(os.path.join(DOCS, "triples", arch), encoding="utf-8"))["triples"]:
            for c in t["casos"]:
                p[c["scenario_id"]] = c["prompt_text"]
    return p


def juzgable(r):
    """Devuelve None si se juzga, o el motivo de exclusion."""
    if r.get("error"):
        return "error_origen"
    if r.get("stop_reason") == "max_tokens":
        return "truncada"
    if not r.get("texto_salida"):
        return "vacia"
    return None


def llamar(cliente, model_id, user_msg):
    ultimo = None
    for i in range(REINTENTOS):
        try:
            return cliente.converse(
                modelId=model_id, system=[{"text": base.JUEZ_SYSTEM}],
                messages=[{"role": "user", "content": [{"text": user_msg}]}],
                inferenceConfig={"maxTokens": 1024, "temperature": 0.0})
        except ClientError as e:
            if e.response["Error"]["Code"] in ("ThrottlingException", "ModelTimeoutException",
                                               "ServiceUnavailableException", "InternalServerException"):
                ultimo = e
                time.sleep(2 ** i)
                continue
            raise
    raise ultimo


def costo(juez, s):
    p = JUECES[juez]["precio"]
    return ((s.get("juez_tokens_input") or 0) * p[0] + (s.get("juez_tokens_output") or 0) * p[1]) / 1000


def juzgar_filas(juez, filas, prompts, tope, hilos):
    cfg = JUECES[juez]
    salida = ruta_juez(juez)
    hechos, gasto = set(), 0.0
    if os.path.exists(salida):
        for linea in open(salida, encoding="utf-8"):
            r = json.loads(linea)
            hechos.add(clave(r))
            gasto += costo(juez, r)
    pend = [r for r in filas if clave(r) not in hechos]
    print(f"juez={juez} pendientes={len(pend)} gasto_previo=US${gasto:.4f} tope=US${tope}")
    cliente = boto3.Session(profile_name=base.PROFILE, region_name=base.REGION).client("bedrock-runtime")
    lock, est = threading.Lock(), {"gasto": gasto, "n": 0, "err": 0, "parar": False}
    out = open(salida, "a", encoding="utf-8")

    def trabajo(r):
        if est["parar"]:
            return
        base_out = {"scenario_id": r["scenario_id"], "modelo": r["modelo"], "system_prompt": r["system_prompt"],
                    "run_idx": r["run_idx"], "legitimacy_category": r["legitimacy_category"],
                    "expected_action": r["expected_action"], "juez_modelo": juez}
        msg = base.JUEZ_USER_TEMPLATE.format(
            legitimacy_category=r["legitimacy_category"], expected_action=r["expected_action"],
            prompt_text=prompts[r["scenario_id"]], texto_salida=r["texto_salida"])
        try:
            t0 = time.time()
            for _intento in range(2):  # un reintento si el JSON del juez viene mal formado
                resp = llamar(cliente, cfg["id"], msg)
                texto = "".join(b.get("text", "") for b in resp["output"]["message"]["content"])
                ver = base.extraer_json(texto)
                u = resp["usage"]
                if ver is not None and ver.get("accion_clasificada") in ACCIONES:
                    break
            s = {**base_out, "juez_tokens_input": u["inputTokens"], "juez_tokens_output": u["outputTokens"],
                 "juez_tiempo_seg": round(time.time() - t0, 2)}
            if ver is None or ver.get("accion_clasificada") not in ACCIONES:
                s.update({"accion_clasificada": None, "alucina_autoridad": None, "justificacion_breve": None,
                          "juez_error": f"JSON no valido: {texto[:200]}"})
            else:
                s.update({"accion_clasificada": ver["accion_clasificada"],
                          "coincide_con_esperado": ver.get("coincide_con_esperado"),
                          "alucina_autoridad": ver.get("alucina_autoridad"),
                          "justificacion_breve": ver.get("justificacion_breve"), "juez_error": None})
        except Exception as e:  # noqa: BLE001
            s = {**base_out, "accion_clasificada": None, "alucina_autoridad": None, "justificacion_breve": None,
                 "juez_error": f"{type(e).__name__}: {e}"[:300]}
        with lock:
            out.write(json.dumps(s, ensure_ascii=False) + "\n")
            out.flush()
            est["n"] += 1
            est["err"] += 1 if s.get("juez_error") else 0
            est["gasto"] += costo(juez, s)
            if est["gasto"] >= tope:
                est["parar"] = True
            if est["n"] % 500 == 0:
                print(f"  {est['n']} hechos, errores={est['err']}, gasto=US${est['gasto']:.2f}", flush=True)

    with ThreadPoolExecutor(max_workers=hilos) as ex:
        list(ex.map(trabajo, pend))
    out.close()
    print(f"FIN juez={juez} procesados={est['n']} errores={est['err']} "
          f"gasto_total=US${est['gasto']:.4f} tope_alcanzado={est['parar']}")


def leer(ruta):
    return [json.loads(x) for x in open(ruta, encoding="utf-8")] if os.path.exists(ruta) else []


def consenso(crudos):
    m = {clave(r): r for r in leer(ruta_juez("mistral_large_3"))}
    lj = {clave(r): r for r in leer(ruta_juez("llama4_maverick"))}
    s = {clave(r): r for r in leer(ruta_juez("claude_sonnet_4_6"))}
    res, cuenta = [], {}
    for r in crudos:
        k = clave(r)
        mot = juzgable(r)
        veredicto = None
        if mot:
            estado = "excluida_" + mot
        elif k not in m or k not in lj:
            estado = "pendiente_de_juicio"
        else:
            am, al = m[k]["accion_clasificada"], lj[k]["accion_clasificada"]
            if am is None or al is None:
                estado = "sin_consenso_juez_invalido"
            elif am == al:
                veredicto, estado = am, "consenso_2_de_2"
            elif r["modelo"] == "claude_sonnet_4_6":
                estado = "sin_consenso_propio_juez"
            elif k in s and s[k]["accion_clasificada"] in (am, al):
                veredicto, estado = s[k]["accion_clasificada"], "consenso_2_de_3"
            else:
                estado = "sin_consenso"
        res.append({"scenario_id": r["scenario_id"], "modelo": r["modelo"], "system_prompt": r["system_prompt"],
                    "run_idx": r["run_idx"], "domain": r["domain"], "legitimacy_category": r["legitimacy_category"],
                    "variant": r.get("variant"), "expected_action": r["expected_action"],
                    "accion_consenso": veredicto, "estado": estado,
                    "mistral": m.get(k, {}).get("accion_clasificada"),
                    "llama": lj.get(k, {}).get("accion_clasificada"),
                    "sonnet_desempate": s.get(k, {}).get("accion_clasificada")})
        cuenta.setdefault(r["modelo"], {}).setdefault(estado, 0)
        cuenta[r["modelo"]][estado] += 1
    with open(os.path.join(DOCS, "consenso-v2.jsonl"), "w", encoding="utf-8") as f:
        for x in res:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    json.dump(cuenta, open(os.path.join(DOCS, "consenso-v2-resumen.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(cuenta, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("etapa", choices=["juzgar", "desempatar", "consenso"])
    ap.add_argument("--juez", choices=["mistral_large_3", "llama4_maverick"])
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--tope-usd", type=float, default=30.0)
    ap.add_argument("--hilos", type=int, default=8)
    a = ap.parse_args()
    crudos = leer(CRUDOS)
    ok = [r for r in crudos if juzgable(r) is None]

    if a.etapa == "juzgar":
        if not a.juez:
            sys.exit("--juez es obligatorio en la etapa juzgar")
        filas = ok
        if a.limite:
            paso = max(1, len(filas) // a.limite)
            filas = filas[::paso][: a.limite]
        juzgar_filas(a.juez, filas, cargar_prompts(), a.tope_usd, a.hilos)
    elif a.etapa == "desempatar":
        m = {clave(r): r for r in leer(ruta_juez("mistral_large_3"))}
        lj = {clave(r): r for r in leer(ruta_juez("llama4_maverick"))}
        disc = []
        for r in ok:
            k = clave(r)
            if r["modelo"] == "claude_sonnet_4_6" or k not in m or k not in lj:
                continue  # un juez no vota sobre sus propias respuestas
            am, al = m[k]["accion_clasificada"], lj[k]["accion_clasificada"]
            if am and al and am != al:
                disc.append(r)
        if a.limite:
            disc = disc[: a.limite]
        juzgar_filas("claude_sonnet_4_6", disc, cargar_prompts(), a.tope_usd, a.hilos)
    else:
        consenso(crudos)


if __name__ == "__main__":
    main()
