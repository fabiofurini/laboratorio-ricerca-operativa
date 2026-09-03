# Laboratorio di Ricerca Operativa

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

<div class="grid cards" markdown>

-   :material-hammer-wrench: **Per iniziare**

    ---

    Come si costruisce un modello, come si fa girare, come si leggono soluzione,
    prezzi ombra e costi ridotti.

    [:octicons-arrow-right-24: Teoria LP](teoria-lp.md) ·
    [Teoria non lineare](teoria-non-lineare.md) ·
    [Solver, modelli lineari](solver-lp.md) ·
    [Solver, non lineari](solver-non-lineare.md)

-   :material-factory: **Pianificare la produzione**

    ---

    LP multiperiodale con scorte: il solver scopre il pre-build e i duali dicono
    quanto vale un'ora di capacità.

    [:octicons-arrow-right-24: Produzione e scorte](produzione.md)

-   :material-truck-delivery: **Muovere i flussi**

    ---

    Flusso a costo minimo, congestione convessa e frontiera costo-emissioni con il
    prezzo interno della CO₂.

    [:octicons-arrow-right-24: Supply chain](supplychain.md)

-   :material-chart-line: **Investire**

    ---

    Il QP più famoso della storia: frontiera efficiente, diversificazione e
    fragilità delle stime.

    [:octicons-arrow-right-24: Markowitz](markowitz.md)

-   :material-currency-eur: **Decidere i prezzi**

    ---

    Domanda endogena, obiettivo bilineare, ottimi di spigolo e il vero valore di un
    posto in più.

    [:octicons-arrow-right-24: Pricing](pricing.md) ·
    [Budget pubblicitario](budget.md)

-   :material-map-marker: **Localizzare e dimensionare**

    ---

    Efficienza contro equità sulla mappa; il muro dell'utilizzazione nelle code;
    la ricarica intelligente di una flotta.

    [:octicons-arrow-right-24: Localizzazione](localizzazione.md) ·
    [Code](code.md) · [Ricarica EV](ricarica-ev.md)

-   :material-dice-multiple: **Decidere prima di sapere**

    ---

    La regola del quantile, gli scenari, il valore della soluzione stocastica e il
    rischio di coda ottimizzato con un LP.

    [:octicons-arrow-right-24: Newsvendor](newsvendor.md) ·
    [VaR e CVaR](var-cvar.md) ·
    [Arbitraggio](arbitraggio.md)

-   :material-robot: **Dal solver al machine learning**

    ---

    La SVM come QP convesso: margine, duale, support vector e kernel — senza
    librerie di ML.

    [:octicons-arrow-right-24: Support Vector Machine](svm.md)

</div>

## Indice completo

**Strumenti**

1. [Solver, modelli lineari](solver-lp.md) e [non lineari](solver-non-lineare.md) — costruire il modello, farlo
   girare, recuperare la soluzione, interpretare l'output
2. [Teoria: programmazione lineare](teoria-lp.md) e [ottimizzazione non lineare](teoria-non-lineare.md) — dualità, prezzi ombra, KKT, protocollo
   di sensitività

**Modelli deterministici**

3. [Produzione e scorte multiperiodali](produzione.md) — LP/QP
4. [Supply chain con congestione e CO₂](supplychain.md) — LP/NLP
5. [Portafoglio di Markowitz](markowitz.md) — QP
6. [Pricing e revenue management](pricing.md) — NLP
7. [Budget pubblicitario](budget.md) — NLP convesso
8. [Localizzazione continua](localizzazione.md) — NLP convesso
9. [Ricarica di veicoli elettrici](ricarica-ev.md) — LP/QP
10. [Code e capacità di servizio](code.md) — NLP convesso

**Decisioni sotto incertezza**

11. [Il Newsvendor e le sue varianti](newsvendor.md) — LP stocastico
12. [VaR e CVaR](var-cvar.md) — LP a scenari
13. [Arbitraggio e prezzatura](arbitraggio.md) — LP e dualità che prezza

**Ottimizzazione e machine learning**

13. [Support Vector Machine](svm.md) — QP

**Il corso**

14. [Organizzazione del laboratorio](organizzazione.md) — laboratori, consegne,
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

- 📘 **[Dispensa completa](pdf/dispensa-laboratorio-ricerca-operativa.pdf)** — 104 pagine: modelli, esempi svolti, casi di studio, analisi di sensitività
- 📊 **[Slide del corso](pdf/slide-laboratorio-ricerca-operativa.pdf)** — 80 slide, tutto il materiale della dispensa in forma sintetica

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
