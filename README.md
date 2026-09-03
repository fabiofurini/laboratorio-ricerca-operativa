<h3 align="center">Materiale didattico di
<a href="https://sites.google.com/view/fabiofurini/home-page">Fabio Furini</a></h3>
<p align="center">
  Professore associato di Ricerca Operativa ·
  <a href="https://www.diag.uniroma1.it/">DIAG</a>, Sapienza Università di Roma ·
  <a href="https://sites.google.com/view/fabiofurini/home-page">sito personale</a>
</p>

# Laboratorio di Ricerca Operativa

> **L'autore.** Fabio Furini è professore associato al DIAG della Sapienza dal
> settembre 2021. Dottorato in Automatica e Ricerca Operativa all'Università di
> Bologna (2011) e assegno di ricerca fino al 2012; postdoc all'Université
> Paris-13 (2012–2013); dal 2013 al 2019 *Maître de Conférences* all'Université
> Paris-Dauphine. *Habilitation à Diriger des Recherches* in Francia nel 2017 e
> Abilitazione Scientifica Nazionale a professore ordinario in Ricerca Operativa
> nel 2019. Nel 2020 ricercatore CNR presso l'IASI-CNR di Roma.
> Sito personale: <https://sites.google.com/view/fabiofurini/home-page>

Modelli continui di ottimizzazione per l'Ingegneria Gestionale — la dispensa del
corso in versione online, con codice Python/Gurobi, dati e casi di studio.

**📖 Dispensa online: [fabiofurini.github.io/laboratorio-ricerca-operativa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/)**

## Scarica in PDF

- [Dispensa completa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/pdf/dispensa-laboratorio-ricerca-operativa.pdf) (114 pagine)
- [Slide del corso](https://fabiofurini.github.io/laboratorio-ricerca-operativa/pdf/slide-laboratorio-ricerca-operativa.pdf) (83 slide)

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
- [Regressione robusta e quantile](https://fabiofurini.github.io/laboratorio-ricerca-operativa/regressione/) — LP, stimare i parametri

**Il corso**

- [Organizzazione del laboratorio](https://fabiofurini.github.io/laboratorio-ricerca-operativa/organizzazione/) — laboratori, consegne, valutazione

## Eseguire i modelli

Ogni capitolo ha il suo script in [`python/`](python/) (`lab04`–`lab16`), con i dati
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

Materiale didattico di **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)** — [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
Slide del corso e soluzioni degli esercizi vengono distribuite a lezione.
