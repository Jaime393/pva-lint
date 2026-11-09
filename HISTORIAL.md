# HISTORIAL — pva-lint

Repo: `Jaime393/pva-lint`, rama `main`.
Leído en vivo: 2026-11-09 ~07:50 -05.

## Commits (5, todos el 2026-09-10, todos de Jaime363)

| # | SHA | Fecha (UTC) | Autor | Mensaje |
|---|---|---|---|---|
| 1 | `867db8ee` | 2026-09-10T16:17:02Z | Jaime363 | V202 pva-lint real — tar.gz desde Download — ρ(x)>0 — sin cortes |
| 2 | `a3630de9` | 2026-09-10T16:22:24Z | Jaime363 | V202 pva-lint real — tar.gz desde Download — Dockerfile + Makefile + workflow — ρ(x)>0 |
| 3 | `9387523d` | 2026-09-10T16:29:38Z | Jaime363 | V202 pva-lint fix — sin tar.gz — Makefile reproduce + gitignore — ρ(x)>0 |
| 4 | `0d6151d0` | 2026-09-10T21:18:49Z | Jaime363 | regla Ki_band [0.55,0.62] colapso <0.3 — valida operacionalizacion.json — ρ(x)>0 |
| 5 | `cac7b5ce` | 2026-09-10T22:29:27Z | Jaime363 | lexicon_coherencia: valida LEXICON_CANONICO auditable — sin mapeo oculto — ρ(x)>0 |

## Lectura de la historia

- **Un solo día de construcción**: 5 commits entre las 16:17:02Z y las 22:29:27Z del 2026-09-10 (6 h 12 min). Muerto desde entonces (60 días a 2026-11-09).
- **El arco del tar.gz**: los 2 primeros commits traen un `tar.gz desde Download`; el 3º lo quita ("sin tar.gz") y añade el `.gitignore` que lo ignora. El tar.gz no sobrevive en el repo.
- **Las reglas llegan al final**: los commits 4 y 5 añaden los dos JSON de `rules/` (Ki_band y lexicon_coherencia), 5 horas después del código. Ninguno de los dos toca `cli.py`.
- **Autor vs dueño**: los 5 commits son de `Jaime363`; el dueño del repo es `Jaime393`. Registrado tal cual, sin interpretar. Es el mismo patrón que en los otros 6 repos PVA (todos con head 2026-09-10, autor Jaime363).
- **Head**: `cac7b5ce`, 2026-09-10T22:29:27Z.

## NO SÉ

- **NO SÉ — qué contenía el tar.gz eliminado.** Los mensajes dicen "desde Download"; el contenido no se ve en el historial leído (no se listaron archivos por commit).
- **NO SÉ — si hubo pushes a otras ramas.** Solo se leyó `main`.
