# Strumenti

Gli strumenti che servono prima dei modelli: la teoria che permette di
*interrogare* una soluzione (dualità, prezzi ombra, KKT) e il solver con cui si
costruiscono e si risolvono i modelli.

<div class="grid cards" markdown>

-   :material-function-variant: **Teoria: programmazione lineare**

    ---

    Coppia primale-duale in forma generale, regole della dualità, teoremi debole e
    forte, scarti complementari, prezzi ombra e analisi di sensitività.

    [:octicons-arrow-right-24: Vai alla pagina](teoria-lp.md)

-   :material-chart-bell-curve: **Teoria: ottimizzazione non lineare**

    ---

    Convessità, programmazione quadratica e condizioni KKT — l'estensione non
    lineare della teoria degli LP. Chiude il protocollo di sensitività.

    [:octicons-arrow-right-24: Vai alla pagina](teoria-non-lineare.md)

-   :material-console: **Solver: modelli lineari**

    ---

    I cinque passi per costruire un modello con `gurobipy`, come farlo girare,
    come leggere soluzione, prezzi ombra, costi ridotti e intervalli di validità.

    [:octicons-arrow-right-24: Vai alla pagina](solver-lp.md)

-   :material-function: **Solver: modelli non lineari**

    ---

    Vincoli funzionali (`log`, `exp`, potenze), termini bilineari, tolleranze e
    scalatura: un solo solver, ottimo globale certificato.

    [:octicons-arrow-right-24: Vai alla pagina](solver-non-lineare.md)

</div>

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
