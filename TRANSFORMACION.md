# Transformación aplicada a esta copia pública

Esta copia es una edición del material original: se generalizaron nombres propios y se retiraron identificadores internos. No se tocaron etiquetas, categorías, veredictos ni cifras; `analisis_v2.py` ejecutado sobre esta copia reproduce `analisis-v2.json` sin diferencias. Los prompts y las respuestas no son byte a byte los que vieron los modelos el 2026-11-04. El registro de desviaciones omite entradas de carácter administrativo que no afectan ningún dato ni análisis, y `14-congelamiento-sha256-ORIGINAL.txt` conserva el manifiesto original. También se retiró de los archivos de respuestas un campo auxiliar de contabilidad por respuesta.

Sustituciones por tipo:

- Identificadores de cuenta e infraestructura, y dependencias internas: 34590
- Nombres propios de lugares y organizaciones: 1059
- Dominios web: 101
- Referencias a cargos y a la unidad de trabajo: 45
- Ediciones manuales de contenido administrativo interno: 34
- Referencias a documentos internos no publicados: 9

Se agregó `scripts/registro_costos.py`, una versión mínima del asistente de costos del que dependían los scripts de generación.

| Archivo | SHA-256 original | SHA-256 copia | Cambios |
|---|---|---|---|
| `14-preregistro-v2.md` | `61dfa8c8f27dc589` | `15354ef1a9b33522` | 32 |
| `15-especificacion-triples.md` | `15e962ffa88f94da` | `0eb9586b5dcfb296` | 17 |
| `14-desviaciones.md` | `b6e14416f4218f07` | `3d8f34a790320d56` | 45 |
| `14-congelamiento-sha256.txt` | `80eb4582aa790627` | `2a8a345691a65f91` | 0 |
| `16-auditoria-adicion-4.md` | `f1a3557b89c10fa8` | `0413d1a6f7f4d5b3` | 1 |
| `triples/becas-borrador.json` | `aeb990f3b16c61f7` | `18237ed94ef5658b` | 1 |
| `triples/emergencia-borrador.json` | `48f1255cb0c599d7` | `48f1255cb0c599d7` | 0 |
| `triples/validacion-becas.json` | `422769ada7af3408` | `422769ada7af3408` | 0 |
| `triples/validacion-emergencia.json` | `e1f39e060d1ff10a` | `e1f39e060d1ff10a` | 0 |
| `resultados-crudos-v2.jsonl` | `0abfdec3578a4c93` | `cf8ff08020d16026` | 35240 |
| `resultados-crudos-v2-errores-reintentados.json` | `4aad77af21c01874` | `4aad77af21c01874` | 0 |
| `resultados-juzgados-v2-mistral_large_3.jsonl` | `46ecabc03ebc7fc1` | `f7a3befaa4b527f5` | 160 |
| `resultados-juzgados-v2-llama4_maverick.jsonl` | `2f7291ddfe74457e` | `31c148eebcf95cb7` | 161 |
| `resultados-juzgados-v2-claude_sonnet_4_6.jsonl` | `d33a06377503e404` | `16798661fd577511` | 9 |
| `resultados-juzgados-v2-qwen3_next_80b.jsonl` | `a10ad36c4b57e8f2` | `76ed488e6afeb5d9` | 3 |
| `consenso-v2.jsonl` | `17801c404cd54843` | `17801c404cd54843` | 0 |
| `consenso-v2-sin-cuarto-juez.jsonl` | `3d3e3a3a144f7e6c` | `3d3e3a3a144f7e6c` | 0 |
| `consenso-v2-resumen-vigente.json` | `e6103f1e86773753` | `e6103f1e86773753` | 0 |
| `analisis-v2.json` | `f284e7a1eb21e415` | `f284e7a1eb21e415` | 0 |
| `analisis-v2.md` | `94ce3f3c6619dda3` | `94ce3f3c6619dda3` | 0 |
| `analisis-v2-sin-cuarto-juez.json` | `6099ef49497196ba` | `6099ef49497196ba` | 0 |
| `analisis-v2-sin-cuarto-juez.md` | `06ab3c905b1e1ca9` | `06ab3c905b1e1ca9` | 0 |
| `03-piloto-casos-prueba.json` | `75a6bfc3c98325fb` | `4ff4f85c4f566198` | 2 |
| `resultados-crudos-piloto.jsonl` | `1edf39593f0f650a` | `53c1c5d2dbbc3745` | 27 |
| `resultados-juzgados-piloto.jsonl` | `3daec02ebdbb906c` | `5de4197e9cc70a51` | 33 |
| `resultados-juzgados-mistral_large_3.jsonl` | `3eb9b5324cece8b6` | `bf57a3810ce60fa3` | 31 |
| `resultados-juzgados-llama4_maverick.jsonl` | `e560258cf466e25b` | `1364b6ab44355569` | 32 |
| `metricas-piloto.json` | `14c0151afe570087` | `339eddb3d5c57f88` | 21 |
| `scripts/invocar_v2.py` | `ccc0fd819ee5a48a` | `e23183edbeb4f94e` | 3 |
| `scripts/juez_v2.py` | `46bac4b7ff9870b7` | `46bac4b7ff9870b7` | 0 |
| `scripts/cuarto_juez_v2.py` | `245130720771420e` | `be01cf4218b15d21` | 2 |
| `scripts/analisis_v2.py` | `1627708f35d5980f` | `1627708f35d5980f` | 0 |
| `scripts/resumen_consenso_v2.py` | `47f1cf87d643ff5e` | `47f1cf87d643ff5e` | 0 |
| `scripts/validar_triples.py` | `8a527fbb9b2ed979` | `8a527fbb9b2ed979` | 0 |
| `scripts/juez_automatico.py` | `aecc4f2fae808fd3` | `0217667a5ffb7489` | 1 |
| `scripts/juez_multi.py` | `1655fd9cc5ca9204` | `1655fd9cc5ca9204` | 0 |
| `scripts/invocar_modelos.py` | `5ffc42ab1e588df3` | `cad97e2830260e94` | 15 |
| `scripts/calcular_metricas.py` | `4ef3a64bf4ac5da3` | `4ef3a64bf4ac5da3` | 0 |
| `scripts/acuerdo_jueces.py` | `329a2f87311d6e02` | `329a2f87311d6e02` | 0 |
| `scripts/generar_esqueleto_triples.py` | `c51b1fef52f961e7` | `c51b1fef52f961e7` | 0 |
| `scripts/ensamblar_becas.py` | `48e059df8df3cc71` | `a1ee690e0d7c2b99` | 2 |
