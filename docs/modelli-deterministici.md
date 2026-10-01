# Modelli deterministici

Otto capitoli in cui tutti i dati sono noti: si decide con certezza, e il valore
sta nell'interrogare la soluzione (quanto vale una risorsa in più? dove si rompe
il piano?).

Dentro ci sono LP, QP, NLP convessi e un NLP non convesso: **cambia il linguaggio
del modello, non cambia il metodo di lavoro** --- si costruisce il modello, lo si
risolve, si leggono i duali, si muovono i dati e si guarda che cosa resta in
piedi.

<div class="grid cards" markdown>

-   :material-factory: **Produzione e scorte**

    ---

    LP multiperiodale con scorte: il solver scopre il pre-build, i duali dicono
    quanto vale un'ora di capacità. Variante QP con smoothing.

    [:octicons-arrow-right-24: LP / QP](produzione.md)

-   :material-truck-delivery: **Supply chain e CO₂**

    ---

    Flusso a costo minimo, congestione convessa e frontiera costo-emissioni con
    il prezzo interno della CO₂.

    [:octicons-arrow-right-24: LP / NLP](supplychain.md)

-   :material-chart-line: **Portafoglio di Markowitz**

    ---

    Il QP più famoso della storia: frontiera efficiente, diversificazione e
    fragilità delle stime.

    [:octicons-arrow-right-24: QP](markowitz.md)

-   :material-currency-eur: **Pricing e revenue management**

    ---

    Domanda endogena, obiettivo bilineare, ottimi di spigolo e il vero valore di
    un posto in più.

    [:octicons-arrow-right-24: NLP](pricing.md)

-   :material-bullhorn: **Budget pubblicitario**

    ---

    Rendimenti decrescenti, condizione KKT «stesso ritorno marginale su ogni
    canale attivo», curva valore-budget.

    [:octicons-arrow-right-24: NLP convesso](budget.md)

-   :material-map-marker: **Localizzazione continua**

    ---

    Baricentro, punto di Weber e minimax sulla mappa: efficienza contro equità,
    con vincolo geografico.

    [:octicons-arrow-right-24: NLP convesso](localizzazione.md)

-   :material-ev-station: **Ricarica di veicoli elettrici**

    ---

    Costo minimo contro peak shaving, prezzi orari dell'energia e duali dei
    fabbisogni.

    [:octicons-arrow-right-24: LP / QP](ricarica-ev.md)

-   :material-account-clock: **Code e capacità di servizio**

    ---

    Il muro dell'utilizzazione: capacità ottima, prezzo di una promessa di
    servizio, robustezza alla domanda incerta.

    [:octicons-arrow-right-24: NLP convesso](code.md)

</div>
