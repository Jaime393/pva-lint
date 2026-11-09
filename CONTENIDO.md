# CONTENIDO — pva-lint

Repo: `Jaime393/pva-lint`, rama `main`.
Leído en vivo 2026-11-09 ~07:50 -05. Todos los números abajo se leyeron
o se calcularon de los archivos del repo, no de memoria.

## Qué hace

Es un linter de línea de comandos (`cli.py`, 3.242 B, librerías `click` y
`requests`) que puntúa un repo de paper con 6 comprobaciones, cada una 1
punto. Score: `round(puntos/6, 3)`. La "transición de fase" se anuncia
cuando el score supera 0.999 — en la práctica, solo con 6/6 = 1.0, porque
5/6 = 0.833.

## Las 6 comprobaciones, cómo funcionan de verdad

| Check | Condición en el código | Borde |
|---|---|---|
| `doi` | Hay DOIs en `*.tex`/`*.md` de la raíz y todos resuelven por GET a `doi.org` (timeout 5 s) | Sin DOIs, el check no se puede ganar: el código exige `dois` no vacío. Un repo sin DOIs tiene como máximo 5/6 = 0.833 |
| `datos` | Existe `data/` o `data.csv` o algún `*GRACE*.csv` | Solo existencia, no contenido |
| `codigo` | Existe `.git` | Depende de cómo se obtuvo el repo: en un checkout o en CI pasa; en una descarga sin `.git` falla |
| `docker` | Existe `Dockerfile` o `docker-compose.yml` | Solo existencia |
| `reproduce` | El `Makefile` contiene la palabra `reproduce` | Solo la palabra; no se ejecuta nada |
| `figuras` | Existe algún `fig*.py` o `plot*.py` en la raíz | Solo raíz (glob no recursivo); no se verifica que generen las figuras |

## Auto-puntuación, verificada ejecutando

Corrido `cli.py` en local (venv, click + requests) sobre los archivos
del propio repo, 2026-11-09 ~07:52 -05:

| Condición | Score | Carencias reportadas |
|---|---|---|
| Con `.git` (checkout normal / CI) | **0.5** | `0 DOIs rotos de 0`, `datos no publicos con DOI/URL`, `figuras sin codigo fuente` |
| Sin `.git` (descarga plana) | **0.333** | Las 3 anteriores + `codigo no en repo abierto` |

El 0.5 coincide con el valor que `pva-orchestrator` lista para
`pva-lint` en su MVP (ver FAMILIA.md): la auto-puntuación medida
converge con la declarada por el hermano.

## Defectos verificados

- **"0 DOIs rotos de 0"**: con cero DOIs en el repo, el linter reporta
  una carencia que dice 0 rotos de 0. Es un mensaje falso: no hay nada
  roto, pero la carencia existe y el punto no se gana.
- **El umbral es inalcanzable sin DOIs**: un repo sin DOIs no puede
  pasar de 5/6 = 0.833, por debajo del 0.999 anunciado. La "transición
  de fase" exige DOIs presentes y resolubles, además de los otros 5
  puntos.
- **`cli.py` nunca lee `rules/`**: el programa importa `re, json,
  requests, click, pathlib` y no referencia `rules/`, `ki_band` ni
  `lexicon` en ninguna línea. Los dos JSON de reglas son datos que
  ningún código consume.
- **Las reglas citan archivos que no existen**: `ki_band.json` dice
  validar `operacionalizacion.json` (no está en el repo); el commit
  `0d6151d0` lo afirma igual. `lexicon_coherencia.json` cita
  `docs/MIU/LEXICON_CANONICO.md` (no hay `docs/` en el repo).
- **El `test` del Makefile no prueba nada**: `test: python cli.py
  --json` — corre el linter, no hay asserts ni archivos de test.
- **El workflow no frena nada**: `.github/workflows/pva.yml` es YAML
  real, corre `cli.py --json` y sube `pva_report.json` como artefacto,
  pero no hay ninguna condición de fallo: un score 0.0 pasa igual.
- **La comprobación DOI necesita red**: `check_doi` hace GET a
  `doi.org` por cada DOI (timeout 5 s). Sin red, todo DOI falla
  (la excepción devuelve `False`). En esta minería no se ejecutó esa
  ruta: el auto-test tenía 0 DOIs y no se hizo ninguna llamada.

## Lo que NO hace

- No valida el léxico ni la banda Ki: las reglas JSON existen, el
  código no las aplica.
- No genera figuras ni verifica que existan: solo mira si hay archivos
  `fig*.py` / `plot*.py`.
- No calcula `phi_global` (9158.79, literal en los dos JSON) ni lo usa:
  la fórmula usa `phi^-1`, no `phi_global`.

## NO SÉ

- **NO SÉ — si la comprobación DOI funciona contra un DOI real.**
  La ruta de red no se ejecutó aquí (el auto-test tenía 0 DOIs).
- **NO SÉ — si algún repo alcanzó alguna vez el score 1.0.** No hay
  reportes guardados en este repo ni en los otros 6 PVA leídos.
- **NO SÉ — si el workflow corrió alguna vez.** No hay logs en el
  repo; las ejecuciones de Actions no se verifican desde aquí.
