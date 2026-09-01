# Laboratorio di Ricerca Operativa

Modelli continui di ottimizzazione per l'Ingegneria Gestionale — la dispensa del
corso in versione online, con codice Python/Gurobi, dati e casi di studio.

**📖 Dispensa online: [fabiofurini.github.io/laboratorio-ricerca-operativa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/)**

## Indice

**Strumenti**

- [Il solver, passo per passo](https://fabiofurini.github.io/laboratorio-ricerca-operativa/guida-gurobi/) — costruire il modello, farlo girare, leggere e interpretare la soluzione
- [Richiami di teoria](https://fabiofurini.github.io/laboratorio-ricerca-operativa/richiami/) — LP e dualità, prezzi ombra, KKT, protocollo di sensitività

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

**Ottimizzazione e machine learning**

- [Support Vector Machine](https://fabiofurini.github.io/laboratorio-ricerca-operativa/svm/) — QP

**Il corso**

- [Organizzazione del laboratorio](https://fabiofurini.github.io/laboratorio-ricerca-operativa/organizzazione/) — laboratori, consegne, valutazione

## Eseguire i modelli

Ogni capitolo ha il suo script in [`python/`](python/) (`lab04`–`lab14`), con i dati
in [`dati/`](dati/):

```bash
python3 -m pip install gurobipy matplotlib pandas scipy
python3 python/esegui_tutti.py     # tutti i modelli: dati, risultati e figure
```

La licenza `gurobipy` inclusa nel pacchetto pip basta per tutti i modelli del corso;
la licenza accademica gratuita si attiva da [portal.gurobi.com](https://portal.gurobi.com).

---

Materiale didattico di **Fabio Furini** (Sapienza Università di Roma).
Slide del corso e soluzioni degli esercizi vengono distribuite a lezione.
