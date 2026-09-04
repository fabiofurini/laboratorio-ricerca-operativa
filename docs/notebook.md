# I notebook del laboratorio

Ogni capitolo con un modello ha il suo **notebook**: si apre in Google Colab con
un clic sul badge, installa il solver da sé e gira nel browser — sul computer non
serve installare niente. È lo stesso codice degli script di `python/`, cella per
cella, con le figure che compaiono sotto le celle invece di finire in un file.

!!! tip "La licenza del pacchetto pip basta"
    La licenza inclusa in `gurobipy` è limitata a 2000 variabili e 2000 vincoli, e
    tutti i modelli del laboratorio ci stanno: il più grande — il newsvendor a
    scenari — ne usa 1803 e 1801. Aumentando il numero di scenari si può superarla:
    in quel caso si attiva la licenza accademica gratuita da
    [portal.gurobi.com](https://portal.gurobi.com).

| Capitolo | Classe | Notebook |
|---|---|---|
| [Produzione e scorte multiperiodali](produzione.md) | LP / QP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab04_produzione.ipynb) |
| [Supply chain con congestione e sostenibilità](supplychain.md) | LP / NLP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab05_supplychain.ipynb) |
| [Portafoglio di Markowitz](markowitz.md) | QP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab06_markowitz.ipynb) |
| [Pricing e revenue management](pricing.md) | NLP concavo / non convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab07_pricing.ipynb) |
| [Allocazione del budget pubblicitario](budget.md) | NLP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab08_budget.ipynb) |
| [Localizzazione continua di un servizio](localizzazione.md) | NLP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab09_localizzazione.ipynb) |
| [Ricarica intelligente di veicoli elettrici](ricarica-ev.md) | LP / QP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab10_ricarica_ev.ipynb) |
| [Capacità di servizio e tempi di attesa](code.md) | NLP convesso (coda M/M/1) | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab11_code.ipynb) |
| [Il Newsvendor e le sue varianti](newsvendor.md) | convesso 1D / LP stocastico a scenari | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab12_newsvendor.ipynb) |
| [VaR e CVaR: misurare e ottimizzare il rischio](var-cvar.md) | LP a scenari | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab13_var_cvar.ipynb) |
| [Arbitraggio e prezzatura senza arbitraggio](arbitraggio.md) | LP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab14_arbitraggio.ipynb) |
| [Support Vector Machine: ottimizzazione per il machine learning](svm.md) | QP convesso | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab15_svm.ipynb) |
| [Regressione robusta e quantile](regressione.md) | LP (confronto con QP) | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab16_regressione.ipynb) |

## Come sono fatti

I notebook non si scrivono a mano: si generano dagli script con

```bash
python3 python/genera_notebook.py
```

Lo script del capitolo resta l'unica sorgente del codice — il notebook ne riprende
docstring, sezioni e commenti — e chi preferisce la riga di comando continua a
lanciare, dalla cartella `python/`:

```bash
python3 lab06_markowitz.py
```
