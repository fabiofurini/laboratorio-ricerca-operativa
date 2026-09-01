# Supply chain con congestione e sostenibilità

**Classe:** LP / NLP convesso · **Script:** `python/lab05_supplychain.py`

I prodotti attraversano una rete di stabilimenti, hub e mercati. Ogni tratta ha
costo, capacità e impronta di CO₂. Come instradare i flussi al minimo costo? Cosa
cambia penalizzando la congestione? Quanto deve valere la CO₂ perché le rotte
"pulite" diventino convenienti?

**Il problema a parole.** *Decidiamo* quante unità far viaggiare su ogni tratta.
*L'obiettivo*: minimo costo di trasporto. *I vincoli*: conservazione del flusso in
ogni nodo e capacità delle tratte.

## Modello

Su un grafo diretto $G = (N, A)$ con saldi $b_i$ (offerta $>0$, domanda $<0$,
transito $=0$), capacità $u_{ij}$, costi $c_{ij}$ ed emissioni $e_{ij}$:

$$
\min \sum_{(i,j) \in A} c_{ij}\, x_{ij}
\quad\text{s.t.}\quad
\sum_{j:(i,j) \in A} x_{ij} - \sum_{j:(j,i) \in A} x_{ji} = b_i \;\;\forall i \in N,
\qquad 0 \le x_{ij} \le u_{ij}
$$

Varianti sull'obiettivo: **congestione** $\sum (c_{ij} x_{ij} + \alpha c_{ij}
x_{ij}^2/u_{ij})$ (convessa); **prezzo interno della CO₂**
$\sum (c_{ij} + \tau e_{ij}) x_{ij}$; **minimax** dell'utilizzo.

!!! example "Esempio a mano (due rotte)"
    100 unità; rotta 1: $c_1 = 2$, $u_1 = 80$; rotta 2: $c_2 = 5$. L'LP riempie la
    rotta economica ($x = (80, 20)$, costo 260 €). Con congestione ($\alpha = 1$) si
    eguagliano i costi marginali: $2 + x_1/20 = 5 \Rightarrow x = (60, 40)$ — la
    rotta economica *non* viene più saturata.

## Caso di studio

2 stabilimenti → 2 hub → 4 mercati, 12 archi; le tratte economiche sono "su strada"
(inquinanti), quelle care "su ferro" (pulite). Dati in `dati/supplychain_archi.csv`.

```text
LP costo minimo : costo 3.385 €   emissioni 2.730 kg   3 archi saturi
Congestione a=1 : costo 3.703 €   emissioni 2.530 kg   utilizzo max 90%
Prezzi ombra domanda: M1 8,00  M2 9,50  M3 10,00  M4 10,50 €/unità
Minimax         : utilizzo massimo minimo possibile 58,4%
```

![Reti a confronto](img/cap05_reti.png)

I prezzi ombra della domanda sono i **costi marginali di servizio** dei mercati: la
base per accettare ordini e per i prezzi di trasferimento interni.

## Sensitività: il prezzo della CO₂

![Frontiera costo-emissioni](img/cap05_frontiera_co2.png)

```text
tau = 0 … 1,0 : costo 3.385  emissioni 2.730   (assetto "strada")
tau = 1,24    : costo 4.025  emissioni 2.173   (vertice intermedio)
tau = 1,5     : costo 4.705  emissioni 1.661   (assetto "ferro")
tau ≥ 4       : costo 4.745  emissioni 1.645   (stabile)
```

Le soluzioni degli LP stanno nei **vertici**: al crescere di $\tau$ l'ottimo salta
tra assetti; la soglia principale (verificata per bisezione) è $\tau^* = 1{,}25$
€/kg: sotto, il prezzo della CO₂ non cambia nulla; sopra, ristruttura la rete.

!!! warning "Minimax degenere"
    Il minimax "puro" ($\min z$) accetta qualunque instradamento con utilizzo
    $\le z^*$, anche costosissimo: combinare sempre con il costo.

## Esercizi

1. Verificare per perturbazione i prezzi ombra di M4 e dell'arco H2→M3 (quest'ultimo
   è saturo ma degenere: duale nullo).
2. Hub H2 al 50%: quanto costa il guasto? (+542,50 €) Quali mercati soffrono?
3. Riprodurre la soglia $\tau^* = 1{,}25$ e identificare gli archi che cambiano.
4. Vincolo $\sum e_{ij} x_{ij} \le 2000$ kg: verificare che il duale coincide con il
   $\tau$ di soglia.
5. Barriera $\alpha x/(u - x)$ al posto della congestione quadratica: confrontare.
