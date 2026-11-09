"""
Fase v2 - ejecutor de los triples contrafactuales contra 12 modelos (preregistro 14).

Reemplaza a invocar_modelos.py solo para la fase v2: aquel script esta amarrado al dataset del
piloto y a 6 modelos. Este usa los mismos system prompts (se importan, no se copian), el mismo
patron de llamada y el mismo cliente SSM para qwen2.5:7b local.

Diferencias declaradas respecto del piloto (todas previstas en el preregistro, secciones 3 y 4):
  - 12 modelos (6 del piloto + 6 nuevos).
  - Algunos modelos no aceptan `temperature` (los Claude nuevos): se omite el parametro y se
    registra temperatura_aplicada = None; esas corridas no son comparables y se informan.
  - Modelos de razonamiento: maxTokens 4096 y solo se concatenan bloques `text` (se descarta
    el razonamiento). Se registra stopReason para contar truncamientos.
  - Tope duro de gasto (--tope-usd): el proceso se detiene limpiamente al alcanzarlo.

Modos:
  --smoke  4 casos de calibracion del piloto, 1 system prompt, 1 corrida, 12 modelos. No toca
           los triples. Escribe resultados-crudos-v2-smoke.jsonl.
  --full   360 prompts de los triples, 2 system prompts, 4 corridas. EXIGE --confirmo-orden y
           verifica los SHA-256 de 14-congelamiento-sha256.txt antes de llamar a un modelo.

Escritura append-only y reanudable.
"""
import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import boto3

AQUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(AQUI, "..")
sys.path.insert(0, AQUI)
import invocar_modelos as base  # noqa: E402  (system prompts, cliente SSM, Ollama)

REGION = base.REGION
PROFILE = base.PROFILE
REINTENTOS = 4

# precio: USD por 1.000 tokens (entrada, salida), de costo_fase_d.py.
MODELOS = {
    "claude_sonnet_4_6": {"tipo": "bedrock", "id": "us.anthropic.claude-sonnet-4-6", "precio": (0.0033, 0.0165), "temp": True, "max": 1024},
    "nova_2_lite": {"tipo": "bedrock", "id": "us.amazon.nova-2-lite-v1:0", "precio": (0.0003, 0.0025), "temp": True, "max": 1024},
    "nova_pro": {"tipo": "bedrock", "id": "us.amazon.nova-pro-v1:0", "precio": (0.0008, 0.0032), "temp": True, "max": 1024},
    "qwen3_vl": {"tipo": "bedrock", "id": "qwen.qwen3-vl-235b-a22b", "precio": (0.00053, 0.00266), "temp": True, "max": 1024},
    "kimi_k2_5": {"tipo": "bedrock", "id": "moonshotai.kimi-k2.5", "precio": (0.0006, 0.003), "temp": True, "max": 1024},
    "qwen2_5_7b_local": {"tipo": "ollama_ssm", "id": "qwen2.5:7b", "precio": (0.0, 0.0), "temp": True, "max": 1024},
    "deepseek_v3_2": {"tipo": "bedrock", "id": "deepseek.v3.2", "precio": (0.00062, 0.00185), "temp": True, "max": 1024},
    "gpt_oss_120b": {"tipo": "bedrock", "id": "openai.gpt-oss-120b-1:0", "precio": (0.00015, 0.0006), "temp": True, "max": 4096},
    "gemma_3_27b": {"tipo": "bedrock", "id": "google.gemma-3-27b-it", "precio": (0.00012, 0.00038), "temp": True, "max": 1024},
    "claude_haiku_4_5": {"tipo": "bedrock", "id": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "precio": (0.0011, 0.0055), "temp": True, "max": 1024},
    "nemotron_3_super_120b": {"tipo": "bedrock", "id": "nvidia.nemotron-super-3-120b", "precio": (0.00015, 0.00065), "temp": True, "max": 4096},
    "glm_5": {"tipo": "bedrock", "id": "zai.glm-5", "precio": (0.001, 0.0032), "temp": True, "max": 4096},
}

RUNS = [(0, 0.0), (1, 0.7), (2, 0.7), (3, 0.7)]
_lock = threading.Lock()
_gasto = {"usd": 0.0}


def invocar_bedrock(cfg, system_prompt, prompt, temperatura):
    cliente = boto3.Session(profile_name=PROFILE, region_name=REGION).client("bedrock-runtime")
    conf = {"maxTokens": cfg["max"]}
    temp_aplicada = None
    if cfg["temp"]:
        conf["temperature"] = temperatura
        temp_aplicada = temperatura
    ultimo = None
    for intento in range(REINTENTOS):
        try:
            t0 = time.time()
            r = cliente.converse(
                modelId=cfg["id"], system=[{"text": system_prompt}],
                messages=[{"role": "user", "content": [{"text": prompt}]}], inferenceConfig=conf)
            texto = "".join(b.get("text", "") for b in r["output"]["message"]["content"])
            return {"texto_salida": texto.strip(), "tokens_input": r["usage"]["inputTokens"],
                    "tokens_output": r["usage"]["outputTokens"], "tiempo_seg": round(time.time() - t0, 2),
                    "stop_reason": r.get("stopReason"), "temperatura_aplicada": temp_aplicada, "error": None}
        except Exception as e:  # noqa: BLE001
            ultimo = f"{type(e).__name__}: {e}"
            if "Throttling" in ultimo or "ServiceUnavailable" in ultimo:
                time.sleep(2 ** intento)
                continue
            break
    return {"texto_salida": "", "tokens_input": 0, "tokens_output": 0, "tiempo_seg": 0.0,
            "stop_reason": None, "temperatura_aplicada": temp_aplicada, "error": ultimo[:300]}


def invocar(cfg, system_prompt, prompt, temperatura):
    if cfg["tipo"] == "bedrock":
        return invocar_bedrock(cfg, system_prompt, prompt, temperatura)
    r = base.invocar_ollama_via_ssm(cfg["id"], system_prompt, prompt, temperatura)
    r.update({"stop_reason": None, "temperatura_aplicada": temperatura})
    return r


def costo_de(cfg, r):
    p = cfg["precio"]
    return (r["tokens_input"] * p[0] + r["tokens_output"] * p[1]) / 1000


def verificar_congelamiento():
    manifiesto = os.path.join(DOCS, "14-congelamiento-sha256.txt")
    malos = []
    with open(manifiesto, encoding="utf-8") as f:
        for linea in f:
            if not linea.strip():
                continue
            esperado, ruta = linea.split(None, 1)
            ruta = ruta.strip().lstrip("*")
            h = hashlib.sha256(open(os.path.join(DOCS, ruta), "rb").read()).hexdigest()
            if h != esperado:
                malos.append(ruta)
    return malos


def cargar_casos(modo):
    if modo == "smoke":
        d = json.load(open(os.path.join(DOCS, "03-piloto-casos-prueba.json"), encoding="utf-8"))["casos"]
        return [c for c in d if c["domain"] == "calibracion"]
    casos = []
    for arch in ("becas-borrador.json", "emergencia-borrador.json"):
        for t in json.load(open(os.path.join(DOCS, "triples", arch), encoding="utf-8"))["triples"]:
            casos.extend(t["casos"])
    return casos


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--smoke", action="store_true")
    g.add_argument("--full", action="store_true")
    ap.add_argument("--confirmo-orden", action="store_true", help="solo --full: el autor ordeno la ejecucion")
    ap.add_argument("--tope-usd", type=float, default=5.0)
    ap.add_argument("--hilos", type=int, default=4)
    ap.add_argument("--modelos", default="", help="lista separada por comas (por defecto, los 12)")
    a = ap.parse_args()
    modo = "smoke" if a.smoke else "full"

    if modo == "full":
        if not a.confirmo_orden:
            sys.exit("--full exige --confirmo-orden (orden expresa del autor).")
        malos = verificar_congelamiento()
        if malos:
            sys.exit(f"ARCHIVOS CONGELADOS MODIFICADOS: {malos}. Registrar la desviacion (seccion 13) antes de correr.")
        print("Congelamiento verificado: los SHA-256 coinciden.")

    casos = cargar_casos(modo)
    claves = [k for k in a.modelos.split(",") if k] or list(MODELOS)
    sps = ["neutral"] if modo == "smoke" else list(base.SYSTEM_PROMPTS)
    runs = [RUNS[0]] if modo == "smoke" else RUNS
    salida = os.path.join(DOCS, "resultados-crudos-v2-smoke.jsonl" if modo == "smoke" else "resultados-crudos-v2.jsonl")

    hechos = set()
    if os.path.exists(salida):
        for l in open(salida, encoding="utf-8"):
            r = json.loads(l)
            hechos.add((r["scenario_id"], r["modelo"], r["system_prompt"], r["run_idx"]))
            _gasto["usd"] += r.get("costo_usd", 0.0)

    trabajos = [(c, m, sp, ri, t) for c in casos for m in claves for sp in sps for ri, t in runs
                if (c["scenario_id"], m, sp, ri) not in hechos]
    print(f"Plan: {len(trabajos)} llamadas nuevas ({len(casos)} casos x {len(claves)} modelos x {len(sps)} SP x {len(runs)} corridas). Gasto previo US${_gasto['usd']:.4f}, tope US${a.tope_usd}")
    out = open(salida, "a", encoding="utf-8")
    parar = threading.Event()

    def ejecutar(t):
        c, m, sp, ri, temp = t
        if parar.is_set():
            return
        cfg = MODELOS[m]
        r = invocar(cfg, base.SYSTEM_PROMPTS[sp], c["prompt_text"], temp)
        usd = costo_de(cfg, r)
        reg = {"scenario_id": c["scenario_id"], "domain": c["domain"], "legitimacy_category": c["legitimacy_category"],
               "variant": c.get("variant"), "modelo": m, "system_prompt": sp, "run_idx": ri, "temperatura": temp,
               "expected_action": c["expected_action"], "costo_usd": round(usd, 6), **r}
        with _lock:
            out.write(json.dumps(reg, ensure_ascii=False) + "\n")
            out.flush()
            _gasto["usd"] += usd
            if _gasto["usd"] >= a.tope_usd:
                parar.set()

    with ThreadPoolExecutor(max_workers=a.hilos) as ex:
        list(ex.map(ejecutar, trabajos))
    out.close()
    print(f"Fin. Gasto acumulado US${_gasto['usd']:.4f}." + (" TOPE ALCANZADO: detenido." if parar.is_set() else ""))


if __name__ == "__main__":
    main()
