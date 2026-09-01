# Allocazione del budget pubblicitario

**Classe:** NLP convesso · **Script:** `python/lab08_budget.py`

Come ripartire una campagna da 100.000 € tra canali con rendimenti marginali
decrescenti? La teoria dice qualcosa di forte e verificabile: **all'ottimo i
rendimenti marginali si eguagliano** — ed è esattamente ciò che il solver
restituisce, cifra per cifra.

**Il problema a parole.** *Decidiamo* la spesa $x_i$ per canale. *L'obiettivo*:
massima risposta totale. *I vincoli*: budget $b$ e tetti $u_i$.

## Modello

Risposta concava $r_i(x) = a_i \log(1 + k_i x)$ per ogni canale:

$$
\max \sum_{i \in I} r_i(x_i)
\quad\text{s.t.}\quad \sum_{i \in I} x_i \le b, \qquad 0 \le x_i \le u_i .
$$

**Condizione KKT all'ottimo:** $r_i'(x_i^*) = \lambda$ per ogni canale interno:
l'ultimo euro rende lo stesso ovunque; i canali al tetto hanno marginale
$> \lambda$, quelli a zero marginale iniziale $< \lambda$.

!!! example "Esempio a mano (2 canali, b = 50)"
    $r_1 = 100\log(1 + 0{,}2x)$, $r_2 = 60\log(1 + 0{,}1x)$. Eguagliando i marginali
    con $x_2 = 50 - x_1$: $x_1 = 35{,}6$, $x_2 = 14{,}4$, $\lambda = 2{,}46$.

## Risultati e verifica delle KKT

```text
     canale |  spesa | tetto | marginale
     social |   24,3 |    60 |  8,2693
     search |   34,8 |    80 |  8,2693
         TV |   22,9 |   120 |  8,2693
 influencer |   18,0 |    35 |  8,2693
Verifica: +1000 € di budget -> risposta +8,244 ≈ lambda
```

I quattro marginali coincidono alla quarta cifra. Nota manageriale: la TV riceve
*meno* dei social nonostante il tetto più alto — non conta la dimensione del canale
ma la velocità con cui satura ($k_i$).

![Curve di risposta e valore del budget](img/cap08_curve.png)

![Mix ottimo al crescere del budget](img/cap08_mix.png)

## Sensitività

```text
b =  20: lambda = 18,97      b = 180: lambda = 5,54
b = 100: lambda =  8,24      b = 300: lambda = 0,00  (tutti ai tetti)
```

La curva di $\lambda$ è l'argomento quantitativo per negoziare il budget: si
finanzia il marketing finché $\lambda$ supera il rendimento di un euro investito
altrove.

## Esercizi

1. Esempio a mano con $b = 80$: $x = (54{,}4;\, 25{,}6)$, $\lambda = 1{,}68$.
2. Risposta esponenziale satura per la TV: serve ancora il tetto $u_i$?
3. Canale con marginale iniziale $5 < \lambda$: resta a zero; interpretarne il
   "costo ridotto".
4. Copertura equa tra segmenti: $\max z$ con $z \le$ copertura di ogni segmento.
