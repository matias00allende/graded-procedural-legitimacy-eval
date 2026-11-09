# Legitimidad procedimental graduada bajo autoridad jerárquica: datos, código y preregistro

Estudio independiente de Matías Allende (matias00allende). Contacto: matias.allende.contreras@gmail.com.

Este repositorio contiene los datos, el código y el preregistro del estudio. Se basa en los aprendizajes del autor al ejecutar un piloto previo en su trabajo profesional, así como en los problemas y las mejoras que ese piloto dejó planteados. El diseño, los análisis y las conclusiones son del autor; ninguna institución patrocina ni respalda el estudio.

## Qué evalúa

El estudio evalúa si un modelo de lenguaje distingue tres situaciones cuando una instrucción invoca autoridad jerárquica dentro de un trámite municipal: (a) autoridad legítima y trámite completo (debe cumplir), (b) autoridad legítima con una brecha procedimental (debe escalar o condicionar) y (c) autoridad fabricada o inflada (debe rechazar o verificar). Todos los escenarios son sintéticos y están escritos en español de Chile; no se usó ningún dato personal real.

La fase v2 incluye 60 triples contrafactuales (30 de becas y 30 de emergencia), 12 modelos, 2 system prompts y 4 corridas por celda, es decir, 34.560 respuestas. Mistral Large 3 y Llama 4 Maverick juzgan todas las respuestas; Claude Sonnet 4.6 solo resuelve los empates. Se agregó un cuarto juez (Qwen3 Next 80B A3B) para 145 filas después de ver los resultados. El análisis está prerregistrado: bootstrap por triple, 10.000 réplicas, semilla 20261023, intervalos percentil 95%, sin valores p.

Resultados principales (promedio de los 12 modelos): P(escalar) en la categoría (b) supera a la de (a) en +0,500 [+0,457, +0,545] y a la de (c) en +0,282 [+0,240, +0,324]. La redacción con urgencia se asocia con un mayor cumplimiento en (b) y (c). El cumplimiento inseguro (UCR) varía de 0,019 a 0,851 según el modelo. Los modelos Claude evaluados casi no cumplen de forma insegura, pero esto se debe a que escalan casi todo. Las limitaciones se detallan en la sección correspondiente y en `14-desviaciones.md`.

## Contenido

| Ruta | Qué es |
|---|---|
| `14-preregistro-v2.md`, `15-especificacion-triples.md` | Preregistro y especificación de los escenarios (en español; traducción al inglés en `en/`) |
| `14-desviaciones.md` | Registro de adiciones y desviaciones posteriores al congelamiento |
| `14-congelamiento-sha256-ORIGINAL.txt` | Manifiesto SHA-256 original de los archivos congelados |
| `MANIFIESTO-SHA256.txt`, `TRANSFORMACION.md` | Verificación de esta copia y detalle de lo que se generalizó |
| `triples/` | Los 60 triples y su validación mecánica |
| `resultados-crudos-v2.jsonl` | 34.560 respuestas de los 12 modelos |
| `resultados-juzgados-v2-*.jsonl`, `consenso-v2*.jsonl` | Veredictos de cada juez y consenso (vigente y sin el cuarto juez) |
| `analisis-v2*.json`, `analisis-v2*.md` | Resultados del análisis (vigente y estrictamente prerregistrado) |
| `16-auditoria-adicion-4.md` | Recálculo de las cifras del cuarto juez a partir de los archivos |
| `*-piloto*`, `metricas-piloto.json` | Piloto previo (40 casos, 6 modelos), como referencia |
| `scripts/` | Código de generación, juicio, consenso y análisis |
| `en/` | Traducciones al inglés de los documentos |

## Reproducir el análisis

```
python scripts/analisis_v2.py
```

Este comando recalcula todas las cifras a partir de los datos incluidos y reproduce `analisis-v2.json`. Solo requiere Python 3. Volver a generar o juzgar respuestas requiere acceso a los modelos mediante Amazon Bedrock, tiene un costo y utiliza un servidor local para el modelo qwen2.5:7b. Los scripts de generación se publican como registro del método y dependen de un asistente de costos (`scripts/registro_costos.py`, versión mínima) y de infraestructura propia, cuyos identificadores se reemplazaron por valores de ejemplo.

## Limitaciones

Los jueces conocen la acción esperada; los escenarios fueron redactados por modelos Anthropic; la incorporación del cuarto juez se decidió después de ver los resultados; no hay validación humana de esta fase; no hay valores p ni corrección por comparaciones múltiples; los datos son sintéticos y abarcan dos dominios y un idioma. Los resultados son válidos para los identificadores de modelo y la fecha de ejecución (2026-11-04). Los detalles se encuentran en la publicación y en `14-desviaciones.md`.

## Edición pública

En esta copia se generalizaron nombres propios de lugares y organizaciones, y se reemplazaron identificadores de infraestructura. Se trata de una edición del texto evaluado: los prompts y las respuestas no son idénticos, byte a byte, a los que vieron los modelos. Esta edición no modifica etiquetas, categorías, veredictos ni cifras, y la ejecución de `analisis_v2.py` sobre esta copia reproduce las cifras originales. Ver `TRANSFORMACION.md`.

## Verificación del congelamiento del preregistro

El preregistro se congeló el 2026-11-04, antes de generar cualquier respuesta de la fase v2. Los hashes SHA-256 de los archivos congelados están en `14-congelamiento-sha256-ORIGINAL.txt`. Los archivos de esta copia fueron editados (ver `TRANSFORMACION.md`, que lista los hashes originales y los de la copia lado a lado), por lo que no coinciden con esos hashes. La fecha del congelamiento se sustenta, entonces, en los registros del autor y en el historial de este repositorio, no en una marca de tiempo independiente de un tercero.

## Alcance y uso responsable

Los resultados describen identificadores de modelo, un formato de prompt y una fecha de ejecución específicos. No son una certificación, un ranking de idoneidad ni una afirmación sobre los proveedores. Los nombres de modelos y empresas pertenecen a sus titulares. Estos resultados no deben usarse para aprobar un sistema en producción sin una validación propia.

## Dependencias

`scripts/analisis_v2.py` usa solo la biblioteca estándar de Python. Volver a generar o juzgar respuestas requiere además `boto3` (ver `requirements.txt`).

## Licencias y cita

El código (`scripts/`) se publica bajo la licencia MIT (`LICENSE`). Los datos y textos se publican bajo CC BY 4.0 (`LICENSE-DATA.md`). Las respuestas fueron generadas por modelos de terceros; quien las reutilice debe revisar los términos de uso de cada proveedor.

Hay una cita legible por máquina en `CITATION.cff`.

Cita sugerida: Allende, M. (2026). *Graded procedural legitimacy under hierarchical authority: evaluation data, code and preregistration*. GitHub, matias00allende/graded-procedural-legitimacy-eval.
