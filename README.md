# Laboratorio di Ricerca Operativa

Modelli continui di ottimizzazione per l'Ingegneria Gestionale: **dispensa
completa, codice Python/Gurobi, dati, slide e casi di studio**, tutto riproducibile.

> Programmazione lineare, quadratica e non lineare; decisioni sotto incertezza
> (Newsvendor, VaR e CVaR); ottimizzazione per il machine learning (SVM).
> Nessuna variabile binaria: dualità, prezzi ombra e condizioni KKT su ogni modello.

## Struttura del repository

| Cartella | Contenuto |
|---|---|
| `dispensa/` | dispensa LaTeX (~85 pagine): teoria, esempi svolti a mano, casi di studio, codice, esercizi; figure pgfplots/TikZ che leggono i CSV generati dagli script |
| `python/` | uno script per capitolo (`lab04`–`lab14`); `esegui_tutti.py` rigenera dati, risultati e figure; `soluzioni_calcoli.py` verifica i numeri delle soluzioni |
| `dati/` | dati dei casi di studio in CSV (seed fissi) |
| `docs/` | il sito del corso: la versione online della dispensa (MkDocs Material) |
| `GUIDA_GUROBI.md` | guida autonoma al solver: costruire, risolvere, interpretare |

## Avvio rapido

```bash
python3 -m pip install gurobipy matplotlib pandas scipy
python3 python/esegui_tutti.py          # dati + risultati + figure (~15 s)
latexmk -pdf -cd dispensa/main.tex      # dispensa
```

La licenza `gurobipy` inclusa nel pacchetto pip (fino a 2000 variabili/vincoli)
basta per tutti i modelli; la licenza accademica gratuita si attiva da
<https://portal.gurobi.com>.

## Sito del corso

Il sito (cartella `docs/`) si costruisce con [MkDocs Material](https://squidfunk.github.io/mkdocs-material/):

```bash
python3 -m pip install mkdocs-material
mkdocs serve        # anteprima locale su http://127.0.0.1:8000
mkdocs gh-deploy    # pubblicazione su GitHub Pages
```

In alternativa, il workflow GitHub Actions incluso (`.github/workflows/site.yml`)
pubblica il sito a ogni push su `main` (attivare Pages → Source: GitHub Actions).

## Licenza e citazione

Materiale didattico di Fabio Furini (Sapienza Università di Roma). Il contenuto è
pensato per l'insegnamento; per usi diversi contattare l'autore.
Slide del corso e soluzioni degli esercizi vengono distribuite a lezione.
