# Laboratorio di Ricerca Operativa

Materiale didattico ideato e sviluppato da **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)**, professore
associato al [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.

**Modelli continui di ottimizzazione** — la dispensa
del corso in versione online, con codice Python/Gurobi, dati e casi di studio
riproducibili.

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

## Il laboratorio in breve

**13 capitoli applicativi · 4 capitoli di strumenti · LP, QP e NLP · un notebook
Colab per capitolo · codice Python/Gurobi riproducibile.** L'elenco completo,
capitolo per capitolo, sta nel [programma](programma.md).

## Scarica in PDF

- 📘 **[Dispensa completa](pdf/dispensa-laboratorio-ricerca-operativa.pdf)** — 114 pagine: modelli, esempi svolti, casi di studio, analisi di sensitività
- 📊 **[Slide del corso](pdf/slide-laboratorio-ricerca-operativa.pdf)** — 83 slide, tutto il materiale della dispensa in forma sintetica

## Per cominciare

Non serve installare niente: ogni capitolo ha il suo
[notebook che si apre in Colab](notebook.md) e gira nel browser. Chi preferisce
lavorare in locale trova i comandi e le note sulla licenza Gurobi nella stessa
pagina.

---

Dello stesso autore: **[Modellazione MIP](https://fabiofurini.github.io/modellazione-mip/)** —
il modulo sui modelli a variabili intere, con gli stessi strumenti e lo stesso
stile — e **[Analisi Matematica 1](https://fabiofurini.github.io/analisi-matematica-1/)** — le dispense
di analisi, con i grafici interattivi.

Materiale didattico di **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)** —
[DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
