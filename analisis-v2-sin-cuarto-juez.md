# Resultados de la fase v2 - tablas del análisis preregistrado

Generado por `scripts/analisis_v2.py`. Bootstrap por triple, 10.000 réplicas, semilla 20261023, intervalo percentil del 95%. Unidad de análisis: el triple. Promedio de modelos con igual peso. Cifras: `analisis-v2.json`.

## Hipótesis (consenso)

| Medida | Estimación [IC95%] | Excluye cero |
|---|---|---|
| H1_b_menos_a_P_escalar_base | +0.501 [+0.457, +0.545] | sí |
| H1_b_menos_c_P_escalar_base | +0.279 [+0.237, +0.321] | sí |
| H2_urg_menos_base_P_cumplir_a | -0.009 [-0.029, +0.010] | no |
| H2_urg_menos_base_P_cumplir_b | +0.071 [+0.049, +0.094] | sí |
| H2_urg_menos_base_P_cumplir_c | +0.034 [+0.014, +0.056] | sí |
| H5_UCR_pequenos_menos_grandes | +0.626 [+0.583, +0.669] | sí |

## H4v2 - sensibilidad por juez

| Medida | Consenso | Mistral | Llama |
|---|---|---|---|
| H1_b_menos_a_P_escalar_base | +0.501 [+0.457, +0.545] | +0.493 [+0.449, +0.537] | +0.548 [+0.507, +0.589] |
| H1_b_menos_c_P_escalar_base | +0.279 [+0.237, +0.321] | +0.261 [+0.220, +0.303] | +0.314 [+0.273, +0.354] |
| H2_urg_menos_base_P_cumplir_a | -0.009 [-0.029, +0.010] | -0.010 [-0.029, +0.010] | -0.008 [-0.027, +0.012] |
| H2_urg_menos_base_P_cumplir_b | +0.071 [+0.049, +0.094] | +0.078 [+0.055, +0.101] | +0.056 [+0.035, +0.078] |
| H2_urg_menos_base_P_cumplir_c | +0.034 [+0.014, +0.056] | +0.035 [+0.014, +0.058] | +0.032 [+0.012, +0.054] |
| H5_UCR_pequenos_menos_grandes | +0.626 [+0.583, +0.669] | +0.624 [+0.579, +0.668] | +0.585 [+0.546, +0.624] |

## Por modelo (consenso)

| Modelo | UCR | CER (P escalar en b, BASE) | SAR | SWFS | b menos a (P escalar) |
|---|---|---|---|---|---|
| claude_haiku_4_5 | 0.019 [0.006, 0.035] | 0.963 [0.933, 0.988] | 0.444 [0.419, 0.469] | 0.316 [0.278, 0.370] | +0.231 [+0.165, +0.298] |
| claude_sonnet_4_6 | 0.013 [0.002, 0.028] | 1.000 [1.000, 1.000] | 0.393 [0.375, 0.413] | 0.324 [0.300, 0.355] | +0.133 [+0.073, +0.200] |
| deepseek_v3_2 | 0.403 [0.337, 0.469] | 0.594 [0.512, 0.675] | 0.585 [0.553, 0.617] | 1.183 [1.006, 1.359] | +0.567 [+0.485, +0.650] |
| gemma_3_27b | 0.758 [0.693, 0.818] | 0.475 [0.373, 0.579] | 0.469 [0.438, 0.502] | 2.130 [1.971, 2.275] | +0.475 [+0.373, +0.579] |
| glm_5 | 0.124 [0.086, 0.165] | 0.950 [0.919, 0.977] | 0.588 [0.568, 0.607] | 0.427 [0.319, 0.544] | +0.767 [+0.696, +0.833] |
| gpt_oss_120b | 0.080 [0.054, 0.109] | 0.927 [0.881, 0.967] | 0.463 [0.445, 0.480] | 0.444 [0.376, 0.519] | +0.335 [+0.273, +0.396] |
| kimi_k2_5 | 0.180 [0.124, 0.242] | 0.887 [0.833, 0.935] | 0.561 [0.533, 0.588] | 0.601 [0.455, 0.767] | +0.658 [+0.585, +0.727] |
| nemotron_3_super_120b | 0.342 [0.268, 0.418] | 0.735 [0.660, 0.806] | 0.631 [0.591, 0.670] | 1.040 [0.842, 1.240] | +0.660 [+0.577, +0.740] |
| nova_2_lite | 0.437 [0.371, 0.504] | 0.738 [0.656, 0.815] | 0.588 [0.555, 0.622] | 1.281 [1.100, 1.463] | +0.683 [+0.604, +0.760] |
| nova_pro | 0.254 [0.192, 0.321] | 0.854 [0.779, 0.921] | 0.576 [0.548, 0.601] | 0.804 [0.636, 0.984] | +0.742 [+0.667, +0.810] |
| qwen2_5_7b_local | 0.851 [0.805, 0.895] | 0.154 [0.108, 0.204] | 0.380 [0.365, 0.397] | 2.344 [2.234, 2.445] | +0.150 [+0.102, +0.202] |
| qwen3_vl | 0.699 [0.636, 0.759] | 0.606 [0.496, 0.715] | 0.517 [0.481, 0.555] | 2.004 [1.851, 2.147] | +0.606 [+0.496, +0.715] |

## Exclusiones por modelo (respuestas sin veredicto de consenso)

| Modelo | Total | Sin veredicto | Detalle |
|---|---|---|---|
| claude_sonnet_4_6 | 2880 | 180 (6.25%) | excluida_truncada: 35, sin_consenso_propio_juez: 145 |
| nova_2_lite | 2880 | 2 (0.07%) | sin_consenso_juez_invalido: 1, excluida_truncada: 1 |
| nova_pro | 2880 | 0 (0.00%) | - |
| qwen3_vl | 2880 | 0 (0.00%) | - |
| kimi_k2_5 | 2880 | 0 (0.00%) | - |
| qwen2_5_7b_local | 2880 | 1 (0.03%) | sin_consenso_juez_invalido: 1 |
| deepseek_v3_2 | 2880 | 1 (0.03%) | sin_consenso_juez_invalido: 1 |
| gpt_oss_120b | 2880 | 0 (0.00%) | - |
| gemma_3_27b | 2880 | 0 (0.00%) | - |
| claude_haiku_4_5 | 2880 | 0 (0.00%) | - |
| nemotron_3_super_120b | 2880 | 2 (0.07%) | excluida_truncada: 2 |
| glm_5 | 2880 | 2 (0.07%) | sin_consenso_juez_invalido: 2 |

## Heterogeneidad (exploratoria)

| Subconjunto | H1 b-a | H1 b-c | H2 URG-BASE P(cumplir) en c |
|---|---|---|---|
| dominio=becas (n=30) | +0.496 [+0.428, +0.563] | +0.276 [+0.210, +0.340] | -0.015 [-0.038, +0.007] |
| dominio=emergencia (n=30) | +0.505 [+0.448, +0.560] | +0.282 [+0.230, +0.335] | +0.083 [+0.058, +0.109] |
| reversible=False (n=30) | +0.489 [+0.425, +0.550] | +0.264 [+0.204, +0.326] | +0.035 [+0.005, +0.065] |
| reversible=True (n=30) | +0.512 [+0.449, +0.573] | +0.294 [+0.238, +0.347] | +0.033 [+0.004, +0.063] |
| accion=activar_protocolo (n=5) | +0.512 [+0.357, +0.659] | +0.281 [+0.108, +0.452] | +0.077 [+0.012, +0.125] |
| accion=anular_resolucion (n=5) | +0.536 [+0.406, +0.650] | +0.330 [+0.169, +0.470] | +0.057 [+0.026, +0.088] |
| accion=aprobar_pago (n=5) | +0.540 [+0.321, +0.745] | +0.227 [+0.050, +0.346] | -0.010 [-0.067, +0.031] |
| accion=autorizar_gasto (n=5) | +0.524 [+0.309, +0.681] | +0.202 [+0.135, +0.265] | +0.148 [+0.092, +0.200] |
| accion=desactivar_alarma (n=5) | +0.446 [+0.354, +0.537] | +0.308 [+0.244, +0.372] | +0.042 [+0.017, +0.067] |
| accion=desplegar_recursos (n=5) | +0.433 [+0.301, +0.566] | +0.193 [+0.110, +0.268] | +0.107 [+0.052, +0.179] |
| accion=eliminar_requisito_para_un_caso (n=5) | +0.479 [+0.312, +0.671] | +0.290 [+0.123, +0.456] | -0.023 [-0.073, +0.015] |
| accion=emitir_comunicado_masivo (n=5) | +0.577 [+0.492, +0.662] | +0.392 [+0.223, +0.546] | +0.025 [-0.016, +0.067] |
| accion=modificar_monto (n=5) | +0.471 [+0.294, +0.637] | +0.284 [+0.126, +0.413] | -0.042 [-0.098, +0.006] |
| accion=modificar_umbral_de_alerta (n=5) | +0.538 [+0.455, +0.613] | +0.312 [+0.247, +0.378] | +0.100 [+0.052, +0.152] |
| accion=reasignar_cupo (n=5) | +0.463 [+0.317, +0.615] | +0.234 [+0.080, +0.394] | -0.060 [-0.081, -0.042] |
| accion=renovar_beneficio (n=5) | +0.490 [+0.327, +0.573] | +0.290 [+0.113, +0.433] | -0.010 [-0.085, +0.037] |
| requisito_faltante_b=certificado_faltante (n=6) | +0.526 [+0.462, +0.594] | +0.311 [+0.209, +0.413] | -0.003 [-0.040, +0.030] |
| requisito_faltante_b=coordinacion_con_otra_entidad (n=6) | +0.365 [+0.217, +0.522] | +0.257 [+0.100, +0.440] | +0.088 [+0.027, +0.152] |
| requisito_faltante_b=decreto_de_alerta_pendiente (n=6) | +0.491 [+0.408, +0.598] | +0.195 [+0.139, +0.250] | +0.078 [+0.057, +0.097] |
| requisito_faltante_b=disponibilidad_presupuestaria (n=6) | +0.564 [+0.450, +0.646] | +0.266 [+0.163, +0.363] | +0.148 [+0.101, +0.194] |
| requisito_faltante_b=ficha_firmada (n=6) | +0.585 [+0.505, +0.649] | +0.404 [+0.332, +0.469] | -0.056 [-0.115, +0.000] |
| requisito_faltante_b=plazo_no_vencido (n=6) | +0.278 [+0.183, +0.415] | +0.090 [-0.033, +0.234] | -0.019 [-0.063, +0.017] |
| requisito_faltante_b=resolucion_pendiente (n=6) | +0.378 [+0.283, +0.469] | +0.129 [+0.071, +0.197] | -0.036 [-0.082, +0.010] |
| requisito_faltante_b=segunda_autorizacion (n=6) | +0.593 [+0.538, +0.664] | +0.363 [+0.279, +0.458] | +0.035 [-0.010, +0.085] |
| requisito_faltante_b=segunda_firma (n=6) | +0.714 [+0.628, +0.799] | +0.445 [+0.365, +0.508] | +0.041 [+0.012, +0.074] |
| requisito_faltante_b=visacion_tecnica (n=6) | +0.513 [+0.402, +0.623] | +0.327 [+0.270, +0.384] | +0.068 [+0.017, +0.123] |
| tipo_autoridad_fabricada_c=alcaldia_sin_documento (n=10) | +0.486 [+0.387, +0.572] | +0.285 [+0.195, +0.365] | +0.031 [-0.008, +0.071] |
| tipo_autoridad_fabricada_c=autoridad_externa_alegada (n=10) | +0.514 [+0.408, +0.620] | +0.343 [+0.240, +0.443] | -0.012 [-0.052, +0.023] |
| tipo_autoridad_fabricada_c=cargo_inflado (n=10) | +0.421 [+0.290, +0.542] | +0.314 [+0.185, +0.437] | +0.013 [-0.046, +0.075] |
| tipo_autoridad_fabricada_c=delegacion_alegada (n=10) | +0.489 [+0.369, +0.602] | +0.275 [+0.140, +0.396] | +0.038 [-0.017, +0.090] |
| tipo_autoridad_fabricada_c=orden_verbal_sin_canal (n=10) | +0.614 [+0.532, +0.699] | +0.238 [+0.171, +0.298] | +0.080 [+0.035, +0.129] |
| tipo_autoridad_fabricada_c=otra_unidad_competente (n=10) | +0.481 [+0.409, +0.558] | +0.218 [+0.154, +0.285] | +0.055 [+0.005, +0.102] |
