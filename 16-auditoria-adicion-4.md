# 16 - Auditoría de las cifras de la Adición 4 (cuarto juez)

**Fecha:** 2026-11-06. **Método:** recálculo determinista en Python sobre `consenso-v2.jsonl`, `consenso-v2-sin-cuarto-juez.jsonl`, `resultados-juzgados-v2-qwen3_next_80b.jsonl`, `analisis-v2.json` y `analisis-v2-sin-cuarto-juez.json`. No se llamó a ningún modelo.

## Resultado: las cifras del reporte coinciden con los archivos

| Afirmación del reporte | Recálculo | Estado |
|---|---|---|
| El cuarto juez resolvió 145 filas, todas de Claude Sonnet 4.6 | 145 filas con estado `consenso_2_de_3_cuarto_juez`; las únicas filas que cambian respecto del consenso previo son esas 145, todas de claude_sonnet_4_6 | CONFIRMADA |
| 0 filas quedaron sin consenso tras el cuarto juez | 0 con `sin_consenso_cuarto_juez`; 0 errores del juez (`juez_error`) | CONFIRMADA |
| Claude Sonnet 4.6 baja de 6,25% a 1,22% sin veredicto | 35 de 2.880 (1,22%), todas truncadas | CONFIRMADA |
| Total sin veredicto: 43 respuestas | 38 truncadas + 5 con juez inválido = 43 | CONFIRMADA |
| Tokens del cuarto juez: 182.964 de entrada y 20.697 de salida | Coinciden | CONFIRMADA |
| Sonnet 4.6: UCR 0,013 a 0,023; CER 1,000 a 0,992; SAR 0,393 a 0,401; SWFS 0,324 a 0,349; b menos a +0,133 a +0,131 | Coinciden con `analisis-v2-sin-cuarto-juez.json` y `analisis-v2.json` | CONFIRMADA |
| Las hipótesis no cambian de conclusión | H1 b-a +0,501 a +0,500; b-c +0,279 a +0,282; H2 a -0,009 en ambos; H2 b +0,071 a +0,072; H2 c +0,034 a +0,035; H5 +0,626 a +0,623. Los intervalos siguen excluyendo cero en las mismas medidas | CONFIRMADA |

## Hallazgos nuevos para declarar (no estaban en el reporte)

1. **El cuarto juez se alineó más con Mistral que con Llama:** de las 145 filas, coincidió con Mistral en 99 y con Llama en 46 (siempre con uno de los dos, por la regla 2 de 3). No hay manera de saber con estos datos si eso refleja mejor criterio o afinidad de familia; se declara.
2. **Qué decidió el cuarto juez:** 43 cumplir, 37 escalar y 65 rechazar. Por categoría: (a) 11 cumplir, 16 escalar, 18 rechazar; (b) 22 cumplir, 6 escalar; (c) 10 cumplir, 15 escalar, 47 rechazar. En (b) y (c) hay 32 respuestas de Sonnet 4.6 clasificadas como cumplir por consenso, lo que explica el alza del UCR de 0,013 a 0,023. Esas 32 respuestas son la parte del UCR de Sonnet 4.6 que depende de la decisión post hoc.
3. **Origen de los desacuerdos:** en 62 de las 145 filas Mistral dijo cumplir y Llama escalar; en 42, Mistral rechazar y Llama escalar; en 37, Mistral escalar y Llama rechazar; en 4, Mistral escalar y Llama cumplir.

## Conclusión

La Adición 4 no cambia ninguna conclusión de hipótesis. Su efecto se limita a la fila de Claude Sonnet 4.6 y a diferencias de centésimas en las medidas globales. La auditoría no valida la calidad de los veredictos del cuarto juez (eso exige revisión humana, no ejecutada).
