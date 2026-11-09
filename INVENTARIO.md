# INVENTARIO — pva-lint

Repo: `Jaime393/pva-lint`, rama `main`.
Leído en vivo: 2026-11-09 ~07:50 -05. Todos los archivos leídos íntegros.

## Archivos (9 archivos, 4.965 B)

| Archivo | Tamaño | Qué es |
|---|---|---|
| `README.md` | 328 B | Presentación: linter PVA, score 0-1, transición de fase >0.999 |
| `cli.py` | 3.242 B | El linter: 6 checks, score, salida JSON o texto |
| `Dockerfile` | 115 B | `python:3.11-slim`, instala `requests click`, CMD `python cli.py` |
| `Makefile` | 135 B | 5 objetivos (`repro`, `dev`, `test`, `lint`, `reproduce`), todos corren `cli.py` |
| `.gitignore` | 30 B | Ignora `pva-lint-real.tar.gz` y `*.tar.gz` |
| `rules/ki_band.json` | 364 B | Regla Ki_band: fórmula, banda [0.55, 0.62], colapso <0.3, `phi_global` 9158.79 |
| `rules/lexicon_coherencia.json` | 338 B | Regla de léxico: 5 checks, ruta `docs/MIU/LEXICON_CANONICO.md`, `phi_global` 9158.79 |
| `.github/workflows/pva.yml` | 413 B | Workflow real: en push/PR instala deps, corre `cli.py --json`, sube el reporte como artefacto |

## Directorios

| Directorio | Contenido |
|---|---|
| `rules/` | 2 archivos JSON (arriba) |
| `.github/workflows/` | 1 archivo YAML (arriba) |

## Lo que NO hay

- Sin `LICENSE`.
- Sin directorio `tests/` ni archivos de test.
- Sin `requirements.txt` (las dependencias se instalan en Dockerfile y workflow: `requests click`).
- Sin `docs/` (la ruta `docs/MIU/LEXICON_CANONICO.md` citada en `rules/lexicon_coherencia.json` no existe en el repo).
- Sin `operacionalizacion.json` (el commit `0d6151d0` dice que la regla Ki_band lo valida; el archivo no está en el repo).
- Sin datos: sin `data/`, sin `*.csv`, sin `*.tex`.
- Sin `pva-lint-real.tar.gz`: existió en los 2 primeros commits y se quitó en el 3º ("sin tar.gz"); el `.gitignore` lo sigue ignorando.

## NO SÉ

- **NO SÉ — si el workflow corrió alguna vez con éxito.** No hay logs ni artefactos en el repo; las ejecuciones de Actions no se verifican desde aquí.
- **NO SÉ — dónde está `pva_report.json`.** El workflow lo genera y lo sube como artefacto; el artefacto no está en el repo.
- **NO SÉ — si el tar.gz eliminado sobrevive en algún lado.** Se quitó del repo en el commit `9387523d`; fuera del repo no se buscó.
