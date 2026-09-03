# Laboratorio di Ricerca Operativa

Materiale didattico ideato e sviluppato da **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)**, professore
associato al [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.

**Modelli continui di ottimizzazione per l'Ingegneria Gestionale** — la dispensa
del corso in versione online, con codice Python/Gurobi, dati e casi di studio
riproducibili.

Ogni capitolo parte da un problema gestionale concreto — quanto produrre, dove
localizzare un servizio, quale prezzo fissare, quanto rischio accettare — lo
trasforma in un modello di ottimizzazione, lo risolve con Gurobi chiamato da Python e, soprattutto, lo
*interroga*: quanto vale un'ora di capacità in più? La soluzione resiste se i dati
cambiano del 5%?

!!! tip "La domanda giusta"
    Alla fine di ogni esercitazione la domanda non è soltanto *«qual è l'ottimo?»*,
    ma *«quale decisione suggeriamo e quanto è robusta?»*. Tutti i modelli usano
    **solo variabili continue**: valgono dualità, prezzi ombra e condizioni KKT.

## Le quattro parti del laboratorio

<div class="grid cards" markdown>

-   :material-hammer-wrench: **Strumenti**

    ---

    Come si costruisce un modello, come si fa girare, come si leggono soluzione,
    prezzi ombra e costi ridotti: la teoria e il solver.

    [:octicons-arrow-right-24: I quattro capitoli](strumenti.md)

-   :material-factory: **Modelli deterministici**

    ---

    Produzione, supply chain, portafoglio, prezzi, budget, localizzazione,
    ricarica dei veicoli elettrici, code: tutti i dati sono noti.

    [:octicons-arrow-right-24: Gli otto problemi](modelli-deterministici.md)

-   :material-dice-multiple: **Decisioni sotto incertezza**

    ---

    Si decide prima di sapere: la regola del quantile, il rischio di coda e la
    dualità che dà il prezzo agli strumenti finanziari.

    [:octicons-arrow-right-24: I tre problemi](decisioni-incertezza.md)

-   :material-robot: **Ottimizzazione e machine learning**

    ---

    La SVM come QP convesso e la regressione robusta come LP: margine, duale,
    support vector e punti di appoggio — senza librerie di ML.

    [:octicons-arrow-right-24: I due problemi](ottimizzazione-ml.md)

</div>

## Indice completo

**[Strumenti](strumenti.md)**

1. [Teoria: programmazione lineare](teoria-lp.md) e [ottimizzazione non lineare](teoria-non-lineare.md) — dualità,
   prezzi ombra, KKT, protocollo di sensitività
2. [Solver, modelli lineari](solver-lp.md) e [non lineari](solver-non-lineare.md) — costruire il modello, farlo
   girare, recuperare la soluzione, interpretare l'output

**[Modelli deterministici](modelli-deterministici.md)**

3. [Produzione e scorte multiperiodali](produzione.md) — LP/QP
4. [Supply chain con congestione e CO₂](supplychain.md) — LP/NLP
5. [Portafoglio di Markowitz](markowitz.md) — QP
6. [Pricing e revenue management](pricing.md) — NLP
7. [Budget pubblicitario](budget.md) — NLP convesso
8. [Localizzazione continua](localizzazione.md) — NLP convesso
9. [Ricarica di veicoli elettrici](ricarica-ev.md) — LP/QP
10. [Code e capacità di servizio](code.md) — NLP convesso

**[Decisioni sotto incertezza](decisioni-incertezza.md)**

11. [Il Newsvendor e le sue varianti](newsvendor.md) — LP stocastico
12. [VaR e CVaR](var-cvar.md) — LP a scenari
13. [Arbitraggio e prezzatura](arbitraggio.md) — LP e dualità che prezza

**[Ottimizzazione e machine learning](ottimizzazione-ml.md)**

14. [Support Vector Machine](svm.md) — QP
15. [Regressione robusta e quantile](regressione.md) — LP

**Il corso**

16. [Organizzazione del laboratorio](organizzazione.md) — laboratori, consegne,
    valutazione, errori da evitare

## Notazione e classi di modelli

- **LP** (*Linear Programming*): obiettivo e vincoli lineari;
- **QP** (*Quadratic Programming*): obiettivo quadratico, vincoli lineari;
- **NLP** (*Nonlinear Programming*): obiettivo o vincoli non lineari generali.

Un problema è **convesso** quando ogni minimo locale è anche globale: per gli LP è
sempre vero; per QP e NLP dipende dalle funzioni.

**Notazione usata in tutto il corso.** Scalari e indici minuscoli ($x_{it}$,
$\lambda$); gli oggetti dei modelli (prodotti, canali, titoli, scenari…) sono
**numerati** e gli indici corrono su insiemi enumerati esplicitamente,
$i \in \{1, 2, \dots, n\}$; conteggi interi ($n \in \mathbb{Z}_{\ge 1}$), dati
razionali ($\mathbb{Q}$); vettori minuscoli in grassetto ($\boldsymbol{x}$),
matrici maiuscole in grassetto ($\boldsymbol{Q}$). Variabili duali $\pi_i$, costi
ridotti $\bar c_j$, scarti $\bar s_i$: la **barra** indica i valori di una
soluzione ammissibile, la **tilde** quelli di una soluzione ottima
($\tilde x_j$, $\tilde z$). Nei modelli la dicitura è sempre «soggetto a», le
variabili sono introdotte prima della formulazione e i vincoli che le definiscono
chiudono il modello.

## Scarica in PDF

- 📘 **[Dispensa completa](pdf/dispensa-laboratorio-ricerca-operativa.pdf)** — 114 pagine: modelli, esempi svolti, casi di studio, analisi di sensitività
- 📊 **[Slide del corso](pdf/slide-laboratorio-ricerca-operativa.pdf)** — 83 slide, tutto il materiale della dispensa in forma sintetica

## Installazione e licenza

```bash
python3 -m pip install gurobipy
```

Il pacchetto pip include una **licenza dimostrativa** (fino a 2000 variabili e 2000 vincoli):
sufficiente per tutti i modelli di questo laboratorio. All'avvio compare la riga
`Restricted license - for non-production use only`: è normale.

**Licenza accademica completa (gratuita):**
1. registrarsi su <https://portal.gurobi.com> con l'email istituzionale (`@uniroma1.it`);
2. richiedere una *Named-User Academic License*;
3. eseguire il comando `grbgetkey XXXXXXXX-...` mostrato dal portale (serve la rete di ateneo o VPN);
4. la licenza viene salvata in `~/gurobi.lic` e da quel momento non ci sono limiti di dimensione.

Verifica rapida:

```python
import gurobipy as gp
print(gp.gurobi.version())        # es. (13, 0, 3)
```

---

## Avvio rapido

```bash
python3 -m pip install gurobipy matplotlib pandas scipy   # scipy: solo funzioni statistiche
python3 python/esegui_tutti.py        # rigenera dati, risultati e figure
```

Nel [repository](https://github.com/fabiofurini/laboratorio-ricerca-operativa)
trovi tutti gli **script Python** e i **dati** in CSV dei casi di studio.

---

Materiale didattico di **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)** —
[DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
