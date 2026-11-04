# pva-lint

Inventario local de preparación de artefactos. Separa archivos observados de validación pública, reproducción y evidencia científica; no declara transiciones de fase a partir de un score de presencia.

```bash
python3 cli.py --path . --json
python3 -m unittest discover -s tests -v
```

Usa solo la biblioteca estándar, sin red ni credenciales. El reporte versionado `pva.artifact-readiness/v1` registra rutas relativas y hashes de archivos, presencia de DOI, datos, código, Docker, target `reproduce` y scripts de figuras.

`structural_score` solo mide presencia. Un `.git` no demuestra código abierto; un directorio vacío no es un dataset; una mención de `reproduce` no es un target. No se resuelven DOIs, verifica licencia, compila Docker, ejecuta Makefile ni valida hipótesis científicas.

Esta revisión cambia el contrato anterior `pva_score` por un esquema explícito. Los consumidores deben adaptarse; no se afirma compatibilidad silenciosa ni despliegue.
