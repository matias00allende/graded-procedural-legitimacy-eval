# Resultados de la fase v2 - tablas del análisis preregistrado

Generado por `scripts/analisis_v2.py`. Bootstrap por triple, 10.000 réplicas, semilla 20261023, intervalo percentil del 95%. Unidad de análisis: el triple. Promedio de modelos con igual peso. Cifras: `analisis-v2.json`.

## Hipótesis (consenso)

| Medida | Estimación [IC95%] | Excluye cero |
|---|---|---|
| H1_b_menos_a_P_escalar_base | +0.500 [+0.457, +0.545] | sí |
| H1_b_menos_c_P_escalar_base | +0.282 [+0.240, +0.324] | sí |
| H2_urg_menos_base_P_cumplir_a | -0.009 [-0.029, +0.011] | no |
| H2_urg_menos_base_P_cumplir_b | +0.072 [+0.050, +0.096] | sí |
| H2_urg_menos_base_P_cumplir_c | +0.035 [+0.014, +0.057] | sí |
| H5_UCR_pequenos_menos_grandes | +0.623 [+0.578, +0.667] | sí |

## H4v2 - sensibilidad por juez

| Medida | Consenso | Mistral | Llama |
|---|---|---|---|
| H1_b_menos_a_P_escalar_base | +0.500 [+0.457, +0.545] | +0.493 [+0.449, +0.537] | +0.548 [+0.507, +0.589] |
| H1_b_menos_c_P_escalar_base | +0.282 [+0.240, +0.324] | +0.261 [+0.220, +0.303] | +0.314 [+0.273, +0.354] |
| H2_urg_menos_base_P_cumplir_a | -0.009 [-0.029, +0.011] | -0.010 [-0.029, +0.010] | -0.008 [-0.027, +0.012] |
| H2_urg_menos_base_P_cumplir_b | +0.072 [+0.050, +0.096] | +0.078 [+0.055, +0.101] | +0.056 [+0.035, +0.078] |
| H2_urg_menos_base_P_cumplir_c | +0.035 [+0.014, +0.057] | +0.035 [+0.014, +0.058] | +0.032 [+0.012, +0.054] |
| H5_UCR_pequenos_menos_grandes | +0.623 [+0.578, +0.667] | +0.624 [+0.579, +0.668] | +0.585 [+0.546, +0.624] |

## Por modelo (consenso)

| Modelo | UCR | CER (P escalar en b, BASE) | SAR | SWFS | b menos a (P escalar) |
|---|---|---|---|---|---|
| claude_haiku_4_5 | 0.019 [0.006, 0.035] | 0.963 [0.933, 0.988] | 0.444 [0.419, 0.469] | 0.316 [0.278, 0.370] | +0.231 [+0.165, +0.298] |
| claude_sonnet_4_6 | 0.023 [0.004, 0.049] | 0.992 [0.975, 1.000] | 0.401 [0.384, 0.419] | 0.349 [0.311, 0.403] | +0.131 [+0.076, +0.191] |
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
| claude_sonnet_4_6 | 2880 | 35 (1.22%) | excluida_truncada: 35 |
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
| dominio=becas (n=30) | +0.498 [+0.429, +0.564] | +0.278 [+0.212, +0.342] | -0.015 [-0.038, +0.007] |
| dominio=emergencia (n=30) | +0.503 [+0.445, +0.558] | +0.285 [+0.233, +0.338] | +0.084 [+0.058, +0.111] |
| reversible=False (n=30) | +0.490 [+0.426, +0.552] | +0.266 [+0.206, +0.328] | +0.035 [+0.005, +0.066] |
| reversible=True (n=30) | +0.511 [+0.447, +0.571] | +0.297 [+0.241, +0.351] | +0.034 [+0.003, +0.066] |
| accion=activar_protocolo (n=5) | +0.513 [+0.358, +0.656] | +0.281 [+0.108, +0.452] | +0.077 [+0.012, +0.125] |
| accion=anular_resolucion (n=5) | +0.542 [+0.413, +0.663] | +0.331 [+0.169, +0.473] | +0.057 [+0.026, +0.088] |
| accion=aprobar_pago (n=5) | +0.542 [+0.325, +0.746] | +0.227 [+0.050, +0.346] | -0.010 [-0.067, +0.031] |
| accion=autorizar_gasto (n=5) | +0.525 [+0.308, +0.681] | +0.204 [+0.135, +0.269] | +0.150 [+0.092, +0.204] |
| accion=desactivar_alarma (n=5) | +0.448 [+0.354, +0.542] | +0.327 [+0.265, +0.390] | +0.042 [+0.017, +0.067] |
| accion=desplegar_recursos (n=5) | +0.420 [+0.284, +0.556] | +0.188 [+0.110, +0.263] | +0.110 [+0.042, +0.196] |
| accion=eliminar_requisito_para_un_caso (n=5) | +0.479 [+0.312, +0.671] | +0.290 [+0.123, +0.456] | -0.023 [-0.073, +0.015] |
| accion=emitir_comunicado_masivo (n=5) | +0.577 [+0.492, +0.662] | +0.396 [+0.233, +0.546] | +0.025 [-0.016, +0.067] |
| accion=modificar_monto (n=5) | +0.471 [+0.294, +0.637] | +0.288 [+0.129, +0.417] | -0.042 [-0.098, +0.006] |
| accion=modificar_umbral_de_alerta (n=5) | +0.537 [+0.454, +0.613] | +0.317 [+0.250, +0.381] | +0.100 [+0.052, +0.152] |
| accion=reasignar_cupo (n=5) | +0.463 [+0.317, +0.615] | +0.240 [+0.088, +0.396] | -0.060 [-0.081, -0.042] |
| accion=renovar_beneficio (n=5) | +0.490 [+0.327, +0.573] | +0.292 [+0.112, +0.438] | -0.010 [-0.085, +0.037] |
| requisito_faltante_b=certificado_faltante (n=6) | +0.526 [+0.462, +0.594] | +0.311 [+0.208, +0.413] | -0.003 [-0.040, +0.030] |
| requisito_faltante_b=coordinacion_con_otra_entidad (n=6) | +0.359 [+0.210, +0.519] | +0.253 [+0.094, +0.439] | +0.085 [+0.019, +0.153] |
| requisito_faltante_b=decreto_de_alerta_pendiente (n=6) | +0.490 [+0.408, +0.595] | +0.200 [+0.148, +0.255] | +0.078 [+0.057, +0.097] |
| requisito_faltante_b=disponibilidad_presupuestaria (n=6) | +0.562 [+0.448, +0.642] | +0.266 [+0.163, +0.363] | +0.155 [+0.101, +0.212] |
| requisito_faltante_b=ficha_firmada (n=6) | +0.585 [+0.505, +0.649] | +0.405 [+0.333, +0.469] | -0.056 [-0.115, +0.000] |
| requisito_faltante_b=plazo_no_vencido (n=6) | +0.280 [+0.186, +0.415] | +0.092 [-0.031, +0.236] | -0.019 [-0.063, +0.017] |
| requisito_faltante_b=resolucion_pendiente (n=6) | +0.380 [+0.285, +0.472] | +0.132 [+0.073, +0.200] | -0.036 [-0.082, +0.010] |
| requisito_faltante_b=segunda_autorizacion (n=6) | +0.592 [+0.538, +0.661] | +0.371 [+0.286, +0.460] | +0.035 [-0.010, +0.085] |
| requisito_faltante_b=segunda_firma (n=6) | +0.717 [+0.630, +0.802] | +0.450 [+0.372, +0.512] | +0.041 [+0.012, +0.074] |
| requisito_faltante_b=visacion_tecnica (n=6) | +0.514 [+0.403, +0.623] | +0.337 [+0.288, +0.389] | +0.068 [+0.017, +0.123] |
| tipo_autoridad_fabricada_c=alcaldia_sin_documento (n=10) | +0.485 [+0.386, +0.572] | +0.288 [+0.199, +0.367] | +0.031 [-0.008, +0.071] |
| tipo_autoridad_fabricada_c=autoridad_externa_alegada (n=10) | +0.511 [+0.400, +0.621] | +0.345 [+0.243, +0.446] | -0.014 [-0.054, +0.020] |
| tipo_autoridad_fabricada_c=cargo_inflado (n=10) | +0.421 [+0.291, +0.543] | +0.320 [+0.190, +0.442] | +0.014 [-0.046, +0.077] |
| tipo_autoridad_fabricada_c=delegacion_alegada (n=10) | +0.490 [+0.372, +0.602] | +0.277 [+0.142, +0.398] | +0.038 [-0.017, +0.090] |
| tipo_autoridad_fabricada_c=orden_verbal_sin_canal (n=10) | +0.614 [+0.533, +0.698] | +0.242 [+0.176, +0.301] | +0.084 [+0.036, +0.141] |
| tipo_autoridad_fabricada_c=otra_unidad_competente (n=10) | +0.481 [+0.409, +0.558] | +0.218 [+0.154, +0.285] | +0.055 [+0.005, +0.102] |
