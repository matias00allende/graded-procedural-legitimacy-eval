"""Version minima del asistente de costos que usan los scripts de generacion.

El estudio original usaba un modulo interno de contabilidad de costos. Esta version solo agrega cada evento
a un archivo JSON local, con la misma firma, para que los scripts de generacion puedan importarse.
"""
import json
import os


def registrar_evento(ruta, proyecto, categoria, modelo_key, tokens_in, tokens_out, tiempo_seg, descripcion):
    eventos = []
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            eventos = json.load(f)
    eventos.append({"proyecto": proyecto, "categoria": categoria, "modelo": modelo_key,
                    "tokens_in": tokens_in, "tokens_out": tokens_out, "tiempo_seg": tiempo_seg,
                    "descripcion": descripcion})
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=1)
