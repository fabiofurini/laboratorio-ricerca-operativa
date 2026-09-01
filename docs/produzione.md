# Produzione e scorte multiperiodali

**Classe:** LP / QP convesso · **Script:** `python/lab04_produzione.py`

Un'azienda decide quanto produrre oggi e quanto conservare a scorta per la domanda
futura. Produrre in anticipo costa giacenza; produrre all'ultimo momento rischia di
sbattere contro il limite di capacità proprio nei mesi di picco.

**Il problema a parole.** *Decidiamo* quante unità di ogni prodotto produrre in ogni
mese e quante tenerne a scorta. *L'obiettivo* è minimizzare produzione + giacenza.
*I vincoli*: bilancio di magazzino mese per mese (con domanda servita per intero) e
ore macchina disponibili.

## Modello

Dati: domanda $d_{it} \ge 0$, costi unitari $c_{it}, h_{it} \ge 0$, ore per unità
$a_i > 0$, ore disponibili $b_t \ge 0$, scorta iniziale $s_{i0}$.
Variabili continue: $x_{it} \ge 0$ (produzione), $s_{it} \ge 0$ (scorta di fine mese).

$$
\begin{aligned}
\min\;& \sum_{i \in I}\sum_{t \in T} \bigl( c_{it}\, x_{it} + h_{it}\, s_{it} \bigr)\\
\text{s.t.}\;\;& s_{i,t-1} + x_{it} = d_{it} + s_{it} && \forall i \in I,\ t \in T\\
& \sum_{i \in I} a_i\, x_{it} \le b_t && \forall t \in T
\end{aligned}
$$

Il **bilancio** è la contabilità di magazzino e lega i mesi tra loro; la **capacità**
è la risorsa scarsa condivisa, e il suo prezzo ombra dirà quanto vale un'ora in più.

!!! example "Esempio a mano (1 prodotto, 2 mesi)"
    $d = (60, 100)$, capacità $80$/mese, $c = 10$, $h = 1$. L'unico piano ammissibile
    è $x = (80, 80)$ con $s_1 = 20$: costo $1620$ €. Con un'ora in più nel mese 2 il
    costo scende di 1 € (un'unità evita un mese di giacenza): il duale del mese 2 è
    $-1$; quello del mese 1 è $0$.

## Caso di studio

Tre prodotti × sei mesi, domanda con picco nei mesi 4–5, capacità 420–460 ore/mese
(dati in `dati/produzione_domanda.csv`).

```text
Costo totale ottimo: 32.889,33 EUR
mese       1      2      3      4      5      6
prod.1  80.0  130.0  150.0  190.0  210.0  160.0
prod.2  50.0   80.0  110.0  140.0  150.0  100.0
prod.3  89.5   91.0   81.4   44.3   29.0   64.8     (scorte fino a 107 unità)
```

![Piano di produzione e scorte](img/cap04_piano_scorte.png)

Il solver scopre da solo il **pre-build**: il prodotto 3 (2,1 ore/unità) viene
prodotto in anticipo e accumulato per liberare capacità nei mesi di picco; le scorte
tornano a zero nel mese finale.

## Sensitività

```text
mese 1: uso 330/420 | Pi =  0,000 €/ora
mese 2: uso 420/420 | Pi = -0,762     mese 5: uso 460/460 | Pi = -3,048
mese 3: uso 460/460 | Pi = -1,524     mese 6: uso 420/420 | Pi = -3,810
Verifica: +1 ora nel mese 6 -> costo -3,810 (esatto)
```

I duali crescono di $0{,}762 = h_3/a_3$ al mese: un'ora in più nel mese $t$ permette
di produrre $1/a_3$ unità del prodotto 3 *un mese più tardi*, risparmiando un mese di
giacenza. La curva del valore della capacità è convessa e decrescente; sotto il 97%
della capacità attuale il problema diventa **inammissibile**.

![Effetto dello smoothing](img/cap04_smoothing.png)

La variante QP con $\gamma \sum_{t>1} (X_t - X_{t-1})^2$ appiattisce il profilo
produttivo (variazione mensile massima da 81 a 1 unità) per soli +114 € (+0,35%).

!!! tip "Take-away manageriale"
    Conviene comprare ore straordinarie nei mesi 5–6 fino a 3–3,8 €/ora sotto il
    prezzo interno; il piano livellato costa lo 0,35% in più; sotto il 97% della
    capacità il servizio completo non è garantibile.

## Esercizi

1. **Verifica** — verificare per perturbazione i duali dei mesi 3 e 4; perché il
   duale del mese 1 è nullo?
2. **Domanda persa** — aggiungere $u_{it}$ con penalità 40 €/unità e capacità al 90%:
   quanta domanda si perde, di quale prodotto, in quali mesi?
3. **Massimo profitto** — ricavi $(20, 30, 42)$ € e servizio facoltativo: quale
   domanda conviene *non* servire?
4. **Emissioni** — aggiungere $\tau \sum_{i,t} e_i x_{it}$ e tracciare la frontiera
   costo-emissioni.
5. **Scorta di sicurezza** — imporre $s_{it} \ge 0{,}1\, d_{i,t+1}$: quanto costa la
   politica?
