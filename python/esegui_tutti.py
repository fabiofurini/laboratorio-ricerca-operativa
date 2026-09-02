"""Esegue in sequenza tutti gli script del laboratorio.

Rigenera: dati (dati/*.csv), dati per le figure pgfplots (dispensa/figure/dat/*.csv),
diagrammi TikZ (dispensa/figure/*.tex) e anteprime matplotlib (dispensa/figure/*.pdf).

Uso:  python3 esegui_tutti.py
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPT = [
    "lab04_produzione.py",
    "lab05_supplychain.py",
    "lab06_markowitz.py",
    "lab07_pricing.py",
    "lab08_budget.py",
    "lab09_localizzazione.py",
    "lab10_ricarica_ev.py",
    "lab11_code.py",
    "lab12_newsvendor.py",
    "lab13_var_cvar.py",
    "lab14_arbitraggio.py",
    "lab15_svm.py",
]

base = Path(__file__).resolve().parent
inizio = time.time()
for s in SCRIPT:
    print(f"\n{'#' * 72}\n# {s}\n{'#' * 72}")
    esito = subprocess.run([sys.executable, str(base / s)], cwd=base)
    if esito.returncode != 0:
        print(f"ERRORE in {s}: interrompo.")
        sys.exit(1)
print(f"\nTutti gli script completati in {time.time() - inizio:.1f} s.")
