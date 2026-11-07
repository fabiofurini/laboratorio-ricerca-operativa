# Programma

<!-- collana-dalla-fascia -->
Ogni capitolo parte da un problema gestionale concreto — quanto produrre, dove
localizzare un servizio, quale prezzo fissare, quanto rischio accettare — lo
trasforma in un modello di ottimizzazione, lo risolve con Gurobi chiamato da Python e, soprattutto, lo
*interroga*: quanto vale un'ora di capacità in più? La soluzione resiste se i dati
cambiano del 5%?

Tutti i modelli si possono eseguire **subito nel browser**: ogni capitolo ha il
suo [notebook che si apre in Colab](notebook.md), senza installare niente.

!!! tip "La domanda giusta"
    Alla fine di ogni esercitazione la domanda non è soltanto *«qual è l'ottimo?»*,
    ma *«quale decisione suggeriamo e quanto è robusta?»*. Tutte le variabili di
    decisione sono **continue**; a seconda della classe del modello la soluzione
    si legge con la dualità LP/QP, con i prezzi ombra o con le condizioni KKT.
<!-- /collana-dalla-fascia -->

L'elenco completo dei capitoli del laboratorio, nell'ordine in cui si affrontano.
Ogni capitolo ha la sua pagina, il suo script Python e il suo
[notebook che si apre in Colab](notebook.md).

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
11. [Data Envelopment Analysis](dea.md) — LP e dualità

**[Decisioni sotto incertezza](decisioni-incertezza.md)**

12. [Il Newsvendor e le sue varianti](newsvendor.md) — LP stocastico
13. [VaR e CVaR](var-cvar.md) — LP a scenari
14. [Arbitraggio e prezzatura](arbitraggio.md) — LP e dualità che prezza

**[Ottimizzazione e machine learning](ottimizzazione-ml.md)**

15. [Support Vector Machine](svm.md) — QP
16. [Regressione robusta e quantile](regressione.md) — LP

**Il corso**

17. [Organizzazione del laboratorio](organizzazione.md) — laboratori ed errori da
    evitare

---

Le quattro parti e a che cosa serve ciascuna sono descritte nella
[prima pagina](index.md).
