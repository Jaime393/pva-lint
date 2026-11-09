# FAMILIA — pva-lint

Repo: `Jaime393/pva-lint`, rama `main`.
Leído en vivo: 2026-11-09 ~07:50 -05.

## Dónde está

Es el linter del ecosistema PVA: la herramienta que puntúa a los demás
repos con el score 0-1 y la "transición de fase >0.999". El README lo
sitúa en "el ecosistema PVA — 5 capas".

## Los 7 PVA (todos con head 2026-09-10, un solo día de construcción)

| Repo | Bloque | Head | Relación con pva-lint |
|---|---|---|---|
| `pva-docker-template` | reproducibilidad | 2026-09-10 | Su `Makefile` depende de pva-lint solo si está al lado; su README promete "PVA score esperado: 1.0" sin que ningún archivo calcule un score |
| `pva-ledger` | memoria inmutable (Bloque 4) | 2026-09-10 | Sin relación de código; comparte marca V202 y firma `rho(x)>0` |
| `pva-lean-bridge` | formalización (Bloque 2) | 2026-09-10 | La fórmula K_i con banda [0.55, 0.62] circula en su commit "nutriente formal" y en `rules/ki_band.json` de este repo (según la minería de pva-lean-bridge, 2026-11-09) |
| `pva-orchestrator` | orquestación (bloque 5) | 2026-09-10 | Lo lista en su MVP como `pva-lint 0.5`. Ese 0.5 coincide con la auto-puntuación medida aquí (0.5 con `.git`, ver CONTENIDO.md): la cifra declarada por el hermano converge con la ejecución |
| `pva-swarm` | validación adversarial (Bloque 3) | 2026-09-10 | Su README promete "validación adversarial"; este linter no la verifica: ninguno de sus 6 checks mira revisores, refutaciones ni tableros |
| `pva-api` | oráculo (V203) | 2026-09-10 | La fórmula K_i con banda [0.55, 0.62] circula también ahí (según la minería de pva-lean-bridge, 2026-11-09) |
| `pva-lint` | puntuación | 2026-09-10 | Este repo |

## Números que circulan sin reconciliar

- **`phi_global` 9158.79**: literal en los dos JSON de `rules/` de
  este repo y en el `pva.yml` de `pva-orchestrator`. El `cli.py` de
  ese repo trae otro phi, 5478.42 (según la minería de
  pva-orchestrator, 2026-11-09). Dos valores distintos, ningún archivo
  los reconcilia. Este linter no usa ninguno de los dos.
- **La fórmula K_i**: `Ki = phi^-1 * (Df/2.5) * (l_corr/l0)`, banda
  [0.55, 0.62], colapso <0.3. Está en `rules/ki_band.json` de este
  repo y circula en pva-lean-bridge y pva-api. La fórmula usa
  `phi^-1` (0.618, misma convención que el Grimorio), no el
  `phi_global` 9158.79 que la acompaña en el mismo JSON.
- **El léxico y `deploy_worker`**: `lexicon_coherencia.json` exige
  que "ningun termino mapea a deploy_worker". El término
  `deploy_worker` no aparece en ningún otro archivo de este repo
  salvo en esa propia regla. Nada verifica el léxico: la regla es
  una lista, no un programa.

## Patrón de la familia

- Los 7 repos PVA se construyeron el 2026-09-10, todos con autor
  Jaime363 y dueño Jaime393, marca V202 (pva-api en V203).
- El patrón se repite en cada uno: el README promete más de lo que
  el código hace (docker-template: score 1.0 sin calcularlo; ledger:
  DOI sin ser DOI; lean-bridge: teoremas `True`; orchestrator: MVP
  5/5 con lint en 0.5; swarm: FastAPI sin FastAPI; lint: transición
  de fase que exige DOIs que el propio repo no tiene).
- Este repo es el único PVA cuyo código se ejecutó en esta minería
  y reprodujo su propio número: 0.5 con `.git`.

## NO SÉ

- **NO SÉ — cuáles son "las 5 capas".** El README las nombra sin
  listarlas; los 7 repos PVA conocidos no se mapean a 5 capas en
  ningún archivo leído.
- **NO SÉ — si `pva-lint` se usó alguna vez para puntuar a sus
  hermanos.** No hay reportes (`pva_report.json`) guardados en
  ningún repo PVA leído.
