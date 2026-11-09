"""
Segundo juez (y tercero) para el piloto de AI Safety - mejora de validez del juez.

Re-juzga resultados-crudos-piloto.jsonl con un juez de OTRA familia, usando la MISMA
rubrica y plantillas que juez_automatico.py (se importan, no se copian), de modo que
la diferencia entre jueces mida al juez y no una rubrica distinta. No toca los archivos
existentes: escribe resultados-juzgados-<alias>.jsonl (append-only, reanudable).

Tope de gasto duro: se suma el costo de lo ya escrito en el archivo de salida mas lo
nuevo; si supera --tope-usd el proceso se detiene limpiamente.

Precios: AWS Pricing API (AmazonBedrock, us-east-1, on-demand standard, lista vigente
desde 2026-10-01, verificados 2026-10-23), USD por 1.000 tokens.

Uso:
    python juez_multi.py --juez mistral_large_3 --limite 20     # prueba de humo
    python juez_multi.py --juez mistral_large_3 --tope-usd 2.5  # pase completo
    python juez_multi.py --juez llama4_maverick --tope-usd 2.5
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import juez_automatico as base  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(AQUI, "..")

JUECES = {
    "mistral_large_3": {
        "model_id": "mistral.mistral-large-3-675b-instruct",
        "usd_1k_in": 0.000250, "usd_1k_out": 0.001500,
    },
    "llama4_maverick": {
        "model_id": "us.meta.llama4-maverick-17b-instruct-v1:0",
        "usd_1k_in": 0.000240, "usd_1k_out": 0.000970,
    },
}

REINTENTOS = 5
HILOS = 4


def costo(juez, t_in, t_out):
    j = JUECES[juez]
    return (t_in / 1000) * j["usd_1k_in"] + (t_out / 1000) * j["usd_1k_out"]


def clave_de(r):
    return (r["scenario_id"], r["modelo"], r["system_prompt"], r["run_idx"])


def cargar_salida(ruta):
    hechos, gasto = set(), 0.0
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                r = json.loads(linea)
                hechos.add(clave_de(r))
    return hechos, gasto


def llamar(cliente, model_id, user_msg):
    ultimo = None
    for intento in range(REINTENTOS):
        try:
            return cliente.converse(
                modelId=model_id,
                system=[{"text": base.JUEZ_SYSTEM}],
                messages=[{"role": "user", "content": [{"text": user_msg}]}],
                inferenceConfig={"maxTokens": 1024, "temperature": 0.0},
            )
        except ClientError as e:
            codigo = e.response["Error"]["Code"]
            if codigo in ("ThrottlingException", "ModelTimeoutException",
                          "ServiceUnavailableException", "InternalServerException"):
                ultimo = e
                time.sleep(2 ** intento)
                continue
            raise
    raise ultimo


def juzgar_uno(cliente, juez, registro, prompt_text):
    user_msg = base.JUEZ_USER_TEMPLATE.format(
        legitimacy_category=registro["legitimacy_category"],
        expected_action=registro["expected_action"],
        prompt_text=prompt_text,
        texto_salida=registro["texto_salida"],
    )
    inicio = time.time()
    resp = llamar(cliente, JUECES[juez]["model_id"], user_msg)
    seg = round(time.time() - inicio, 2)
    usage = resp["usage"]
    # Solo bloques de texto: los de razonamiento (reasoningContent) se ignoran.
    texto = "".join(b.get("text", "") for b in resp["output"]["message"]["content"])
    return base.extraer_json(texto), usage, seg, texto


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--juez", required=True, choices=sorted(JUECES))
    ap.add_argument("--limite", type=int, default=0, help="procesar solo N filas (humo)")
    ap.add_argument("--tope-usd", type=float, default=2.5)
    args = ap.parse_args()

    salida_path = os.path.join(DOCS, f"resultados-juzgados-{args.juez}.jsonl")
    prompts = base.cargar_prompts()
    hechos, _ = cargar_salida(salida_path)

    # Gasto ya incurrido (reanudacion): se reconstruye desde los tokens registrados.
    gasto = 0.0
    if os.path.exists(salida_path):
        with open(salida_path, encoding="utf-8") as f:
            for linea in f:
                r = json.loads(linea)
                gasto += costo(args.juez, r.get("juez_tokens_input") or 0,
                               r.get("juez_tokens_output") or 0)

    with open(base.CRUDOS_PATH, encoding="utf-8") as f:
        filas = [json.loads(x) for x in f]
    pendientes = [r for r in filas if clave_de(r) not in hechos]
    if args.limite:
        paso = max(1, len(pendientes) // args.limite)
        pendientes = pendientes[::paso][: args.limite]  # muestra repartida entre modelos
    print(f"juez={args.juez} total={len(filas)} ya_hechos={len(hechos)} "
          f"pendientes={len(pendientes)} gasto_previo=US${gasto:.4f} tope=US${args.tope_usd}")

    cliente = boto3.Session(profile_name=base.PROFILE, region_name=base.REGION).client("bedrock-runtime")
    candado = threading.Lock()
    estado = {"gasto": gasto, "n": 0, "errores": 0, "parar": False}
    f_out = open(salida_path, "a", encoding="utf-8")

    def trabajo(registro):
        if estado["parar"]:
            return
        base_out = {**registro, "juez_modelo": args.juez}
        if registro.get("error"):
            salida = {**base_out, "accion_clasificada": None, "coincide_con_esperado": None,
                      "alucina_autoridad": None, "justificacion_breve":
                      f"Sin clasificar - respuesta original con error: {registro['error']}",
                      "juez_error": None}
        else:
            try:
                ver, usage, seg, crudo = juzgar_uno(
                    cliente, args.juez, registro, prompts.get(registro["scenario_id"], ""))
                if ver is None:
                    salida = {**base_out, "accion_clasificada": None, "coincide_con_esperado": None,
                              "alucina_autoridad": None, "justificacion_breve": None,
                              "juez_error": f"JSON no parseable: {crudo[:200]}",
                              "juez_tokens_input": usage["inputTokens"],
                              "juez_tokens_output": usage["outputTokens"]}
                else:
                    salida = {**base_out, **ver, "juez_error": None,
                              "juez_tokens_input": usage["inputTokens"],
                              "juez_tokens_output": usage["outputTokens"],
                              "juez_tiempo_seg": seg}
            except Exception as e:  # noqa: BLE001
                salida = {**base_out, "accion_clasificada": None, "coincide_con_esperado": None,
                          "alucina_autoridad": None, "justificacion_breve": None,
                          "juez_error": f"{type(e).__name__}: {e}"}
        with candado:
            f_out.write(json.dumps(salida, ensure_ascii=False) + "\n")
            f_out.flush()
            estado["n"] += 1
            if salida.get("juez_error"):
                estado["errores"] += 1
            estado["gasto"] += costo(args.juez, salida.get("juez_tokens_input") or 0,
                                     salida.get("juez_tokens_output") or 0)
            if estado["gasto"] >= args.tope_usd:
                estado["parar"] = True
            if estado["n"] % 100 == 0:
                print(f"  {estado['n']} hechos, errores={estado['errores']}, "
                      f"gasto=US${estado['gasto']:.4f}", flush=True)

    with ThreadPoolExecutor(max_workers=HILOS) as ex:
        list(ex.map(trabajo, pendientes))
    f_out.close()

    print(f"FIN juez={args.juez} procesados={estado['n']} errores={estado['errores']} "
          f"gasto_total=US${estado['gasto']:.4f} tope_alcanzado={estado['parar']}")


if __name__ == "__main__":
    main()
