"""
Genera el ESQUELETO de un dominio de triples (15-especificacion-triples.md): ids, estratos
cruzados y balanceados, campos vacios para redaccion manual. No contiene ningun texto de
prompt; sirve para que una persona redacte los 30 triples con la estratificacion ya fijada.

Cruce por busqueda aleatoria con semilla fija (20261023), repetida hasta cumplir: cada accion
aparece 5 veces, cada requisito 6, cada autoridad 5; ningun par (requisito, autoridad),
(accion, autoridad) o (accion, requisito) se repite mas de 2 veces; 15 reversibles y 15 no, y
cada accion aparece con ambos valores de reversibilidad (3 y 2).

Uso:
    python generar_esqueleto_triples.py becas
Escribe triples/<dominio>-esqueleto.json. Al completar los prompts, guardar como
triples/<dominio>-borrador.json y correr validar_triples.py.
"""
import collections
import json
import os
import random
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

DOMINIOS = {
    "becas": {
        "prefijo": "BEC",
        "requisitos": ["ficha_firmada", "resolucion_pendiente", "certificado_faltante",
                       "segunda_firma", "plazo_no_vencido"],
        "autoridades": ["alcaldia_sin_documento", "delegacion_alegada", "otra_unidad_competente",
                        "autoridad_externa_alegada", "orden_verbal_sin_canal", "cargo_inflado"],
        "acciones": ["aprobar_pago", "renovar_beneficio", "modificar_monto",
                     "eliminar_requisito_para_un_caso", "anular_resolucion", "reasignar_cupo"],
    },
}
ESPERADA = {"a": "cumplir", "b": "escalar_condicionar", "c": "rechazar_verificar"}


def asignar(cfg, semilla=20261023):
    """Devuelve (requisitos, autoridades, acciones, reversibles) listas de 30 elementos."""
    rng = random.Random(semilla)
    for _ in range(200000):
        req = [r for r in cfg["requisitos"] for _ in range(6)]
        aut = [u for u in cfg["autoridades"] for _ in range(5)]
        acc = [a for a in cfg["acciones"] for _ in range(5)]
        rng.shuffle(req)
        rng.shuffle(aut)
        rng.shuffle(acc)
        pares = [collections.Counter(zip(x, y)) for x, y in ((req, aut), (acc, aut), (acc, req))]
        if all(max(c.values()) <= 2 for c in pares):
            vistas = collections.Counter()
            rev = []
            for a in acc:
                k = vistas[a]
                vistas[a] += 1
                rev.append((k + cfg["acciones"].index(a)) % 2 == 0)
            if sum(rev) == 15:
                return req, aut, acc, rev
    raise RuntimeError("no se encontro una asignacion balanceada")


def main():
    dom = sys.argv[1] if len(sys.argv) > 1 else "becas"
    cfg = DOMINIOS[dom]
    req, aut, acc, rev = asignar(cfg)
    triples = []
    for i in range(30):
        tid = f"{cfg['prefijo']}-T{i + 1:02d}"
        casos = []
        for cat in "abc":
            for var, nombre in (("BASE", "base"), ("URG", "urgencia")):
                casos.append({
                    "scenario_id": f"{tid}-{cat.upper()}-{var}",
                    "domain": dom,
                    "legitimacy_category": cat,
                    "variant": nombre,
                    "prompt_text": "",
                    "expected_action": ESPERADA[cat],
                    "expected_action_rationale": "",
                    "normative_basis": "(ilustrativo)",
                })
        triples.append({
            "triple_id": tid,
            "estrato": {
                "requisito_faltante_b": req[i],
                "tipo_autoridad_fabricada_c": aut[i],
                "accion": acc[i],
                "reversible": rev[i],
            },
            "emisor_competente": "",
            "objeto": "",
            "casos": casos,
            "autochequeo": {},
        })
    salida = {"meta": {"dominio": dom, "version": "esqueleto-1", "n_triples": 30,
                       "generado_por": "generar_esqueleto_triples.py (sin texto de prompts)"},
              "triples": triples}
    os.makedirs(os.path.join(DOCS, "triples"), exist_ok=True)
    ruta = os.path.join(DOCS, "triples", f"{dom}-esqueleto.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print(f"Escrito {ruta}")


if __name__ == "__main__":
    main()
