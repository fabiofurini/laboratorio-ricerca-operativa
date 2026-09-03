# Laboratorio di Ricerca Operativa

Modelli continui di ottimizzazione per l'Ingegneria Gestionale — la dispensa del
corso in versione online, con codice Python/Gurobi, dati e casi di studio.

**📖 Dispensa online: [fabiofurini.github.io/laboratorio-ricerca-operativa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/)**

## Scarica in PDF

- [Dispensa completa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/pdf/dispensa-laboratorio-ricerca-operativa.pdf) (104 pagine)
- [Slide del corso](https://fabiofurini.github.io/laboratorio-ricerca-operativa/pdf/slide-laboratorio-ricerca-operativa.pdf) (80 slide)

## Indice

**Strumenti**

- [Teoria: programmazione lineare](https://fabiofurini.github.io/laboratorio-ricerca-operativa/teoria-lp/) — dualità, scarti complementari, prezzi ombra e sensitività
- [Teoria: ottimizzazione non lineare](https://fabiofurini.github.io/laboratorio-ricerca-operativa/teoria-non-lineare/) — convessità, QP, condizioni KKT
- [Solver: modelli lineari](https://fabiofurini.github.io/laboratorio-ricerca-operativa/solver-lp/) — costruire il modello, farlo girare, leggere e interpretare la soluzione
- [Solver: modelli non lineari](https://fabiofurini.github.io/laboratorio-ricerca-operativa/solver-non-lineare/) — vincoli funzionali, bilineari, tolleranze

**Modelli deterministici**

- [Produzione e scorte multiperiodali](https://fabiofurini.github.io/laboratorio-ricerca-operativa/produzione/) — LP/QP
- [Supply chain con congestione e CO₂](https://fabiofurini.github.io/laboratorio-ricerca-operativa/supplychain/) — LP/NLP
- [Portafoglio di Markowitz](https://fabiofurini.github.io/laboratorio-ricerca-operativa/markowitz/) — QP
- [Pricing e revenue management](https://fabiofurini.github.io/laboratorio-ricerca-operativa/pricing/) — NLP
- [Budget pubblicitario](https://fabiofurini.github.io/laboratorio-ricerca-operativa/budget/) — NLP convesso
- [Localizzazione continua](https://fabiofurini.github.io/laboratorio-ricerca-operativa/localizzazione/) — NLP convesso
- [Ricarica di veicoli elettrici](https://fabiofurini.github.io/laboratorio-ricerca-operativa/ricarica-ev/) — LP/QP
- [Code e capacità di servizio](https://fabiofurini.github.io/laboratorio-ricerca-operativa/code/) — NLP convesso

**Decisioni sotto incertezza**

- [Il Newsvendor e le sue varianti](https://fabiofurini.github.io/laboratorio-ricerca-operativa/newsvendor/) — LP stocastico
- [VaR e CVaR](https://fabiofurini.github.io/laboratorio-ricerca-operativa/var-cvar/) — LP a scenari
- [Arbitraggio e prezzatura](https://fabiofurini.github.io/laboratorio-ricerca-operativa/arbitraggio/) — LP, la dualità che prezza

**Ottimizzazione e machine learning**

- [Support Vector Machine](https://fabiofurini.github.io/laboratorio-ricerca-operativa/svm/) — QP

**Il corso**

- [Organizzazione del laboratorio](https://fabiofurini.github.io/laboratorio-ricerca-operativa/organizzazione/) — laboratori, consegne, valutazione

## Eseguire i modelli

Ogni capitolo ha il suo script in [`python/`](python/) (`lab04`–`lab15`), con i dati
in [`dati/`](dati/):

```bash
python3 -m pip install gurobipy matplotlib pandas scipy
python3 python/esegui_tutti.py     # tutti i modelli: dati, risultati e figure
```

La licenza `gurobipy` inclusa nel pacchetto pip basta per tutti i modelli del corso;
la licenza accademica gratuita si attiva da [portal.gurobi.com](https://portal.gurobi.com).

## English version

The whole lab is also available in English:
**[fabiofurini.github.io/operations-research-lab](https://fabiofurini.github.io/operations-research-lab/)**
([repository](https://github.com/fabiofurini/operations-research-lab)).

---

Materiale didattico di **Fabio Furini** (Sapienza Università di Roma).
Slide del corso e soluzioni degli esercizi vengono distribuite a lezione.
