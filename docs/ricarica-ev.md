# Ricarica intelligente di veicoli elettrici

**Classe:** LP / QP convesso · **Script:** `python/lab10_ricarica_ev.py`

Una flotta deve arrivare carica al mattino sfruttando le ore economiche — ma se
tutti caricano insieme, il picco di prelievo esplode. Un problema che *sembra*
richiedere variabili di accensione/spegnimento e invece è un LP puro: la decisione
vera — quanta potenza — è continua.

**Il problema a parole.** *Decidiamo* la potenza $x_{vt}$ per veicolo e ora.
*L'obiettivo*: minima spesa energetica. *I vincoli*: energia richiesta entro la
partenza, ricarica solo quando collegati e sotto la potenza del caricatore,
prelievo totale sotto la potenza del contatore.

## Modello

Dati: prezzi orari $\pi_t$, disponibilità $a_{vt} \in \{0,1\}$, energia $e_v$,
potenza massima $\bar p_v$, carico di base $b_t$, limite contatore $k$, rendimento
$\eta$.

$$
\begin{aligned}
\min\;& \sum_{v \in V}\sum_{t \in T} \pi_t\, \Delta t\, x_{vt}\\
\text{s.t.}\;\;& \eta \sum_{t \in T} \Delta t\, x_{vt} \ge e_v && \forall v \in V\\
& 0 \le x_{vt} \le a_{vt}\, \bar p_v && \forall v, t\\
& \sum_{v \in V} x_{vt} + b_t \le k && \forall t \in T
\end{aligned}
$$

!!! example "Esempio a mano (1 veicolo, 2 ore)"
    $e = 10$ kWh, prezzi $(0{,}10;\, 0{,}20)$, $\bar p = 8$ kW: si carica 8 nell'ora
    economica e 2 in quella cara (costo 1,20 €). Duale del fabbisogno = 0,20 €/kWh
    (il prezzo dell'*ora marginale*); duale della potenza = 0,10 €/kW. Con
    $\bar p = 12$: tutto nell'ora economica, duale 0,10.

## Caso di studio

Sei furgoni con finestre notturne diverse, contatore $k = 120$ kW, $\eta = 0{,}95$.

```text
Costo minimo : 20,36 €/notte   picco 103,4 kW
Peak shaving : picco minimo possibile 68,0 kW
Duali fabbisogno: 0,0842 = 0,08/η  oppure  0,0947 = 0,09/η  a seconda del veicolo
```

![Profili di prelievo](img/cap10_profili.png)

I duali sono i prezzi delle **ore marginali** di ciascun veicolo, corretti per il
rendimento: la finestra di disponibilità determina quale prezzo orario "vede"
l'ultimo kWh.

## Sensitività

![Frontiera costo-picco](img/cap10_frontiera.png)

```text
rho = 0    : costo 20,36  picco 103,4      k = 60–65 kW : INAMMISSIBILE
rho = 0,10 : costo 21,39  picco  74,9      k = 70 kW    : 21,93 €
rho = 0,20 : costo 22,15  picco  68,0      k* minimo    : 68 kW
```

Tagliare il picco del 28% costa un euro a notte. Il minimax puro spenderebbe
27,79 €: il compromesso costo + $\rho\,\cdot$ picco ottiene lo stesso picco a
22,15 € — mai ottimizzare un solo obiettivo quando ce ne sono due.

!!! warning "Un bug istruttivo (capitato davvero)"
    Nel vincolo `quicksum(x) + base[t] <= C` Gurobi sposta la costante nel termine
    noto: il RHS memorizzato è `C - base[t]`. Chi scrive `v.RHS = nuovaC` sta
    allentando il vincolo sbagliato. Quando una sensitività non cambia nulla,
    sospettare del proprio codice prima che del modello.

## Esercizi

1. $e_1: 46 \to 47$ kWh: costo $+0{,}0947 = 0{,}09/0{,}95$ (verificato).
2. V3 arriva alle 23: come cambiano costo e picco?
3. Profilo regolare QP con $\gamma \sum_t (z_t - z_{t-1})^2$.
4. Frontiera costo-emissioni con intensità carbonica oraria $g_t$.
5. Capacità minima ammissibile per bisezione: $k^* = 68$ kW.
