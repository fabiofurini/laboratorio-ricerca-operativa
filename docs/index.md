# Laboratorio di Ricerca Operativa

**Modelli continui di ottimizzazione per l'Ingegneria Gestionale** — dispensa,
codice Python/Gurobi, dati, slide e casi di studio, tutto riproducibile.

Ogni capitolo parte da un problema gestionale concreto — quanto produrre, dove
localizzare un servizio, quale prezzo fissare, quanto rischio accettare — lo
trasforma in un modello di ottimizzazione, lo risolve in Python e, soprattutto, lo
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

    [:octicons-arrow-right-24: Guida al solver](guida-gurobi.md) ·
    [Richiami di teoria](richiami.md)

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
    [VaR e CVaR](var-cvar.md)

-   :material-robot: **Dal solver al machine learning**

    ---

    La SVM come QP convesso: margine, duale, support vector e kernel — senza
    librerie di ML.

    [:octicons-arrow-right-24: Support Vector Machine](svm.md)

</div>

## Indice completo

**Strumenti**

1. [Il solver, passo per passo](guida-gurobi.md) — costruire il modello, farlo
   girare, recuperare la soluzione, interpretare l'output
2. [Richiami di teoria](richiami.md) — LP e dualità, prezzi ombra, KKT, protocollo
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

**Ottimizzazione e machine learning**

13. [Support Vector Machine](svm.md) — QP

**Il corso**

14. [Organizzazione del laboratorio](organizzazione.md) — laboratori, consegne,
    valutazione, errori da evitare

## Avvio rapido

```bash
python3 -m pip install gurobipy matplotlib pandas scipy
python3 python/esegui_tutti.py        # rigenera dati, risultati e figure
latexmk -pdf dispensa/main.tex        # compila la dispensa (~85 pagine)
```

Nel [repository](https://github.com/fabiofurini/laboratorio-ricerca-operativa)
trovi anche le **slide beamer** complete (60 slide), le **soluzioni degli
esercizi** per i docenti e tutti i **dati** in CSV.
