#!/usr/bin/env python3
import requests, re, pathlib, json, click
#!/usr/bin/env python3
"""
pva-lint — Linter PVA V202
Verifica DOI, datos públicos, código abierto, Dockerfile, make reproduce
Salida: PVA score 0-1 + carencias
ρ(x)>0 — EL SUELO ES
"""
import re, json, sys, requests, pathlib, click
from pathlib import Path

def check_doi(doi):
    try:
        r = requests.get(f"https://doi.org/api/handles/{doi}", timeout=5)
        return r.status_code == 200
    except:
        return False

def scan_repo(path="."):
    p = Path(path)
    report = {"pva_score": 0.0, "carencias": [], "checks": {}}
    score = 0
    total = 6
    
    # 1. DOI verificable
    tex_files = list(p.glob("*.tex")) + list(p.glob("*.md"))
    dois = []
    for f in tex_files:
        try:
            dois += re.findall(r"10\.\d{4,}/[^\s}]+", f.read_text(errors='ignore'))
        except: pass
    doi_ok = sum(1 for d in dois if check_doi(d)) if dois else 0
    report["checks"]["doi"] = f"{doi_ok}/{len(dois)} verificables"
    if doi_ok == len(dois) and dois: score += 1
    else: report["carencias"].append(f"{len(dois)-doi_ok} DOIs rotos")
    
    # 2. Datos públicos
    has_data = (p/"data").exists() or (p/"data.csv").exists() or any(p.glob("*GRACE*.csv"))
    report["checks"]["datos"] = "publicos" if has_data else "faltan"
    if has_data: score += 1
    else: report["carencias"].append("datos no públicos con DOI/URL")
    
    # 3. Código abierto
    has_code = (p/".git").exists()
    report["checks"]["codigo"] = "repo abierto" if has_code else "no git"
    if has_code: score += 1
    else: report["carencias"].append("código no en repo abierto")
    
    # 4. Dockerfile
    has_docker = (p/"Dockerfile").exists() or (p/"docker-compose.yml").exists()
    report["checks"]["docker"] = "presente" if has_docker else "ausente"
    if has_docker: score += 1
    else: report["carencias"].append("falta Dockerfile reproducible")
    
    # 5. make reproduce
    has_make = (p/"Makefile").exists()
    has_repro = False
    if has_make:
        try:
            has_repro = "reproduce" in (p/"Makefile").read_text()
        except: pass
    report["checks"]["reproduce"] = "make reproduce existe" if has_repro else "falta"
    if has_repro: score += 1
    else: report["carencias"].append("falta make reproduce")
    
    # 6. Figuras con código fuente
    has_fig_code = len(list(p.glob("fig*.py"))) + len(list(p.glob("plot*.py"))) > 0
    report["checks"]["figuras"] = "con código" if has_fig_code else "sin código fuente"
    if has_fig_code: score += 1
    else: report["carencias"].append("figuras sin código fuente")
    
    report["pva_score"] = round(score/total, 3)
    return report

@click.command()
@click.option("--path", default=".", help="Path repo paper")
@click.option("--json", "json_out", is_flag=True, help="Salida JSON")
def main(path, json_out):
    r = scan_repo(path)
    if json_out:
        print(json.dumps(r, indent=2))
    else:
        print(f"🧬 PVA-LINT V202 — Score: {r['pva_score']} — ρ(x)>0")
        for k,v in r["checks"].items():
            print(f"  {k}: {v}")
        if r["carencias"]:
            print("  Carencias:")
            for c in r["carencias"]:
                print(f"   - {c}")
        else:
            print("  ✅ Sin carencias — transición de fase alcanzada")

if __name__ == "__main__":
    main()
