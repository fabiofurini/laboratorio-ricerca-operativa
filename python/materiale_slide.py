"""Slide dei capitoli: copia i PDF sul sito e scrive la sezione «Le slide»
della pagina del materiale (it: docs/materiale.md, en: docs/downloads.md).

Le slide stanno in slides/<nome>/<nome>.tex (it/slides e en/slides), una
cartella per gruppo di slide, compilate lì; sul sito va solo il PDF.
La sezione è fra i segnaposto <!-- slide:inizio --> e <!-- slide:fine -->.

Uso: python3 python/materiale_slide.py     (fa italiano e inglese)
"""
import re
import shutil
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]

# (titolo del gruppo it, en), [(nome it, nome en, titolo it, titolo en)]
GRUPPI = [
    (("Strumenti", "Tools"), [
        ("slide-01-introduzione", "slides-01-introduction", "Introduzione al laboratorio", "Introduction to the laboratory"),
        ("slide-02-richiami", "slides-02-background", "Richiami di teoria", "Theory background"),
        ("slide-03-python-gurobi", "slides-03-python-gurobi", "Il solver: costruire, risolvere, interpretare", "The solver: building, solving, interpreting"),
    ]),
    (("Modelli deterministici", "Deterministic models"), [
        ("slide-04-produzione", "slides-04-production", "Produzione e scorte multiperiodali", "Multi-period production and inventory"),
        ("slide-05-supply-chain", "slides-05-supply-chain", "Supply chain con congestione e sostenibilità", "Supply chain with congestion and sustainability"),
        ("slide-06-markowitz", "slides-06-markowitz", "Portafoglio di Markowitz", "The Markowitz portfolio"),
        ("slide-07-pricing", "slides-07-pricing", "Pricing e revenue management", "Pricing and revenue management"),
        ("slide-08-budget", "slides-08-budget", "Allocazione del budget pubblicitario", "Advertising budget allocation"),
        ("slide-09-localizzazione", "slides-09-location", "Localizzazione continua di un servizio", "Continuous location of a service"),
        ("slide-10-ricarica-ev", "slides-10-ev-charging", "Ricarica intelligente di veicoli elettrici", "Smart charging of electric vehicles"),
        ("slide-11-code", "slides-11-queues", "Capacità di servizio e tempi di attesa", "Service capacity and waiting times"),
    ]),
    (("Decisioni sotto incertezza", "Decisions under uncertainty"), [
        ("slide-12-newsvendor", "slides-12-newsvendor", "Il Newsvendor e le sue varianti", "The Newsvendor and its variants"),
        ("slide-13-var-cvar", "slides-13-var-cvar", "VaR e CVaR", "VaR and CVaR"),
        ("slide-14-arbitraggio", "slides-14-arbitrage", "Arbitraggio e prezzatura", "Arbitrage and pricing"),
    ]),
    (("Ottimizzazione e machine learning", "Optimization and machine learning"), [
        ("slide-15-svm", "slides-15-svm", "Support Vector Machine", "Support Vector Machine"),
        ("slide-16-regressione", "slides-16-regression", "Regressione robusta e quantile", "Robust and quantile regression"),
    ]),
]
PAGINA = {"it": "materiale.md", "en": "downloads.md"}
TESTO = {
    "it": ("## Le slide", "Le slide delle lezioni, una per capitolo delle dispense (PDF)."),
    "en": ("## Slides", "The lecture slides, one deck per chapter of the notes (PDF)."),
}


def sezione(lingua):
    k = 0 if lingua == "it" else 1
    repo = RADICE / lingua
    titolo, intro = TESTO[lingua]
    righe = ["<!-- slide:inizio -->", titolo, "", intro, "", '<div class="grid cards" markdown>', ""]
    n = 0
    for nome_gruppo, decks in GRUPPI:
        voci = []
        for d in decks:
            nome, tit = d[k], d[2 + k]
            pdf = repo / "slides" / nome / f"{nome}.pdf"
            if pdf.exists():
                shutil.copy(pdf, repo / "docs" / "pdf" / f"{nome}.pdf")
                voci.append(f"    - [{tit}](pdf/{nome}.pdf)")
                n += 1
        if voci:
            righe += [f"-   :material-presentation: **{nome_gruppo[k]}**", "", "    ---", ""] + voci + [""]
    righe += ["</div>", "", "<!-- slide:fine -->"]
    return "\n".join(righe), n


if __name__ == "__main__":
    for lingua in ("it", "en"):
        p = RADICE / lingua / "docs" / PAGINA[lingua]
        s = p.read_text()
        blocco, n = sezione(lingua)
        if "<!-- slide:inizio -->" in s:
            s = re.sub(r"<!-- slide:inizio -->.*?<!-- slide:fine -->", lambda m: blocco, s, flags=re.S)
        else:
            raise SystemExit(f"{p}: manca il segnaposto <!-- slide:inizio -->")
        p.write_text(s)
        print(f"[{lingua}] {p.name}: {n} gruppi di slide")
