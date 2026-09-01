# Il Newsvendor e le sue varianti

**Classe:** convesso 1D / LP stocastico a scenari · **Script:** `python/lab12_newsvendor.py`

Scegliere una quantità **prima** di osservare la domanda: moda e stagionali,
freschi, farmaci, capacità alberghiera. È la porta d'ingresso dell'ottimizzazione
stocastica, con un risultato netto: **la quantità ottima non è la domanda media**.

**Il problema a parole.** *Decidiamo* la sola quantità $q$. *L'obiettivo*: minimo
costo atteso dell'errore — troppo ($c_o$ per unità invenduta) o troppo poco ($c_u$
per vendita persa).

## Modello base e regola del quantile

$$
\min_{q \ge 0}\; c_o\, \mathbb{E}[(q - D)^+] + c_u\, \mathbb{E}[(D - q)^+]
\qquad\Longrightarrow\qquad
F(q^*) = \alpha^* = \frac{c_u}{c_u + c_o}
$$

Ragionamento marginale: l'unità in più rende $c_u$ con probabilità $1 - F(q)$ e
costa $c_o$ con probabilità $F(q)$; conviene finché $F(q) \le \alpha^*$.

!!! example "Esempio a mano (domanda discreta)"
    $D \in \{80, 100, 120\}$ equiprobabili, $c_u = 9$, $c_o = 4$:
    $C(80) = 180$, $C(100) = 86{,}7$, $C(120) = \mathbf{80}$. Si ordina il
    **massimo**: con $c_u \gg c_o$ restare corti costa più del doppio che restare
    lunghi. (Regola discreta: il più piccolo $q$ con $F(q) \ge 0{,}6923$.)

## Caso di studio

Panetteria: $p = 15$, $c = 6$, $v = 2$ € → $c_u = 9$, $c_o = 4$; $D$ normale
$(100, 20)$.

```text
alpha* = 9/13 = 0,6923      q* = 110,05  (media = 100)
costo atteso in q*: 91,43 €   |   ordinando la media: 103,72 €
```

![Costo atteso e stabilità](img/cap12_quantile_stabilita.png)

## La formulazione lineare a scenari

$$
\min\; c_o \sum_{s \in S} \pi_s o_s + c_u \sum_{s \in S} \pi_s u_s
\quad\text{s.t.}\;\; o_s \ge q - d_s,\;\; u_s \ge d_s - q,\;\; q, o_s, u_s \ge 0
$$

Il **trucco delle parti positive**: l'obiettivo schiaccia $o_s$ e $u_s$ sui valori
$\max\{q - d_s, 0\}$ e $\max\{d_s - q, 0\}$ senza variabili binarie — lo stesso
meccanismo tornerà nel CVaR e nella SVM.

```text
LP con 600 scenari: q = 108,61 = quantile empirico al 69,23% (è un teorema)
VSS = 11,17 €/ciclo (-11%): il valore di modellare l'incertezza
Stabilità: con 30 scenari q balla di ±3,5 unità tra repliche
```

## Livelli di servizio e rischio

```text
Cycle service level 95%: q = 132,9 (costo +45,59 €)   Fill rate in q*: già 96%!
Media-CVaR (alpha=0,9): lambda 0 -> 1: q da 108,6 a 116,2
  costo medio +6,5 €  |  CVaR90 da 245,9 a 224,6 (-21,4 €)
```

![Frontiera costo-CVaR](img/cap12_frontiera.png)

!!! warning "Non confondere i livelli di servizio"
    In $q^*$ la probabilità di *non* avere stock-out è il 69%, ma il *fill rate*
    (domanda servita in media) è il 96%: promesse molto diverse a costi molto
    diversi. Leggere bene lo SLA.

**Multiprodotto** (3 prodotti, budget 1200 €, domande correlate $\rho = 0{,}7$): il
budget comprime le quantità sotto i quantili ottimi; duale del budget $-0{,}55$
(un euro in più rende 55 centesimi per ciclo). Con $\rho = 0$ il costo atteso scende
del 18%: **la correlazione è un costo**, e il modello lo quantifica.

## Esercizi

1. Penalità $b = 3$ €: $\alpha^* = 0{,}75$, $q^* = 113{,}5$.
2. Scenari da 24 osservazioni storiche vs distribuzione stimata: quale consigliare?
3. Deperibili ($v = -1$): $\alpha^* = 0{,}5625$, $q^* = 103{,}2$.
4. EVPI: quanto vale al massimo una previsione perfetta? (88,33 €/ciclo.)
5. Vincolo di fill rate al 98% vs cycle service level al 98%: confrontare.
6. Multiprodotto con $\rho = 0$: perché il costo scende?
