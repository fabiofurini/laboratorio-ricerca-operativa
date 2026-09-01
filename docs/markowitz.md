# Portafoglio di Markowitz

**Classe:** QP convesso · **Script:** `python/lab06_markowitz.py`

Quanto investire in ciascun titolo per bilanciare rendimento atteso e rischio? Il
risultato non è un numero ma una **frontiera efficiente**: il menu completo dei
compromessi tra cui il decisore sceglie.

**Il problema a parole.** *Decidiamo* le quote di capitale $x_i$. *L'obiettivo*:
minima varianza del portafoglio. *I vincoli*: quote a somma 1, rendimento atteso
minimo $\bar r$, limiti $\ell_i \le x_i \le u_i$.

## Modello

Dati: rendimenti attesi $\mu_i$, covarianze $q_{ij}$ (matrice
$\boldsymbol Q \succeq 0$).

$$
\min \sum_{i \in I}\sum_{j \in I} q_{ij}\, x_i x_j
\quad\text{s.t.}\quad
\sum_{i \in I} \mu_i x_i \ge \bar r,\qquad
\sum_{i \in I} x_i = 1,\qquad \ell_i \le x_i \le u_i .
$$

La varianza contiene le **covarianze**: è lì che nasce la diversificazione. Ogni
matrice di covarianza è semidefinita positiva → QP convesso, ottimo globale
certificato.

!!! example "Esempio a mano (2 titoli non correlati)"
    $\sigma_1 = 20\%$, $\sigma_2 = 30\%$: minimizzando
    $0{,}04 x_1^2 + 0{,}09 (1 - x_1)^2$ si ottiene $x_1 = 9/13 = 69{,}2\%$ e
    volatilità di portafoglio $16{,}6\%$ — **meno di entrambi i titoli**.

## Caso di studio

Otto ETF settoriali, $\mu$ e $\boldsymbol Q$ **stimati** da 60 rendimenti mensili
simulati (`dati/markowitz_rendimenti.csv`).

```text
Minima varianza globale : rendimento 11,06%, volatilità  6,03%
Equipesato (1/n)        : rendimento 10,74%, volatilità 10,13%   (dominato!)
Composizione min varianza: ENE 5%  IND 2%  SAN 12%  CON 22%  UTL 58%
```

![Frontiera efficiente](img/cap06_frontiera.png)

![Composizione lungo la frontiera](img/cap06_composizione.png)

Tre messaggi: (1) la minima varianza è meno rischiosa del miglior titolo singolo;
(2) l'equipesato $1/n$ è dominato; (3) il tetto $u_i = 30\%$ taglia la parte alta
della frontiera — il costo dei vincoli di mandato *si vede*.

## Sensitività

```text
r_min =  6…10%: vol 6,03%  (vincolo NON attivo: coincide col min varianza)
r_min = 12%   : vol 6,10%  d(varianza)/d(r_min) ≈ 0,022
```

Fino all'11,06% (rendimento della minima varianza) il vincolo di rendimento è
inattivo e non costa nulla; oltre, ogni punto di rendimento si paga in varianza.

!!! warning "La fragilità delle stime"
    Su 60 mesi l'errore standard del rendimento stimato è ≈2,6% annuo per titolo: i
    portafogli ottimizzati inseguono gli errori di stima. Rimedi: vincoli $u_i$,
    shrinkage, o ottimizzare solo il rischio.

## Esercizi

1. Due titoli con $\rho = 0{,}5$: la diversificazione conviene ancora?
   ($x_1 = 6/7$, vol 19,6%)
2. Frontiere con $u = 1$, $0{,}3$, $0{,}2$: rendimento massimo 20,9% / 16,7% / 14,7%.
3. Rieseguire con seed diverso: quanto cambiano le composizioni?
4. Tracking error minimo con rendimento ≥ 12% (TE = 1,1% annuo).
5. Costi di transazione quadratici dal portafoglio equipesato.
