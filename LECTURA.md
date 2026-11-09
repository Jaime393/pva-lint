# LECTURA — pva-lint

Repo: `Jaime393/pva-lint`, rama `main`.
Leído en vivo: 2026-11-09 ~07:50 -05 (los 9 archivos, íntegros).

## Qué dice el README (íntegro)

> `# pva-lint V202 — ρ(x)>0`
>
> `Linter PVA — Score 0-1 — Transición de fase >0.999`
>
> `Verifica DOI, datos públicos, código abierto, Dockerfile, make reproduce, figuras con código.`
>
> `## Uso`
>
> `    pip install requests click`
> `    python cli.py --json`
>
> `Parte del ecosistema PVA — 5 capas — validación como transición de fase.`

## Qué dice el docstring de `cli.py` (literal)

> `pva-lint — Linter PVA V202 — ρ(x)>0 — EL SUELO ES`
> `Verifica DOI, datos públicos, código abierto, Dockerfile, make reproduce, figuras con código`
> `Score 0-1 — transición fase >0.999`

## Las 6 comprobaciones (según el código)

1. **doi**: busca DOIs (`10\.\d{4,}/[^\s}]+`) en `*.tex` y `*.md` de la raíz; verifica cada uno con GET a `https://doi.org/api/handles/{doi}` (timeout 5 s). Suma 1 solo si hay DOIs y todos resuelven.
2. **datos**: existe `data/` o `data.csv` o algún `*GRACE*.csv`.
3. **codigo**: existe `.git` (el repo es un checkout git).
4. **docker**: existe `Dockerfile` o `docker-compose.yml`.
5. **reproduce**: el `Makefile` contiene la palabra `reproduce`.
6. **figuras**: existe algún `fig*.py` o `plot*.py` en la raíz.

Score: `round(puntos/6, 3)`. La salida `--json` imprime `pva_score`, `carencias` y `checks`; sin `--json` imprime `PVA-LINT V202 Score: X rho(x)>0` y la lista.

## Qué dicen las reglas (`rules/`, íntegras)

`rules/ki_band.json`:

```json
{
  "rule": "Ki_band",
  "formula": "Ki = phi^-1 * (Df/2.5) * (l_corr/l0)",
  "resiliencia": [0.55, 0.62],
  "colapso": "<0.3",
  "metricas": ["DFA alpha 0.5 ruido 1.0 criticalidad 1.5 browniano", "Higuchi k_max 10-20", "box-counting 2-100mm", "l_corr fMRI"],
  "falsador": "Ki bajo con conciencia reportada => MIU falla",
  "phi_global": 9158.79,
  "rho": ">0"
}
```

`rules/lexicon_coherencia.json`:

```json
{"rule":"lexicon_coherencia","lexicon_path":"docs/MIU/LEXICON_CANONICO.md","checks":["rho>0 savia primordial","Ki in [0.55,0.62] anillo crecimiento","Phi>Phi_c 0.31 savia circulante","beta≈0.5 curva crecimiento","ningun termino mapea a deploy_worker — solo conceptos MIU"],"phi_global":9158.79,"rho":">0","transparencia":"auditable"}
```

## Qué dice el workflow (íntegro, `.github/workflows/pva.yml`)

```yaml
name: PVA lint
on: [push, pull_request]
jobs:
  pva:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install deps
        run: pip install requests click
      - name: Run pva-lint
        run: python cli.py --json > pva_report.json
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: pva-report
          path: pva_report.json
```

## Qué dice el Makefile (íntegro)

```make
repro:
	python cli.py --json

dev:
	python cli.py

test:
	python cli.py --json

lint:
	python cli.py

reproduce:
	python cli.py --json
```

## NO SÉ

- **NO SÉ — cuáles son "las 5 capas" del ecosistema PVA.** El README las nombra sin listarlas. En este rincón los 7 repos PVA conocidos son docker-template, ledger, lean-bridge, orchestrator, swarm, lint y api — si esas son las 5 capas o no, no se dice en ningún archivo leído.
- **NO SÉ — si algún repo alcanzó alguna vez el score 1.0.** No hay reportes guardados en este repo ni en los otros 6 PVA leídos.
