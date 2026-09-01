# Localizzazione continua di un servizio

**Classe:** NLP convesso · **Script:** `python/lab09_localizzazione.py`

Dove collocare una stazione di ricarica, un micro-hub, un presidio sanitario per
essere "vicini" alla domanda? Dipende da cosa significa vicini: distanza **media**
(efficienza), **massima** (equità) o **quadratica** (baricentro). Tre obiettivi,
tre punti diversi sulla mappa.

**Il problema a parole.** *Decidiamo* le coordinate $(x, y)$. *L'obiettivo* è la
vera scelta manageriale (media / massimo / quadratica). *I vincoli* delimitano
l'area ammissibile.

## Modello

Quartieri $i \in I$ in $(a_i, b_i) \in \mathbb{R}^2$ con pesi $w_i \ge 0$:

$$
\text{Weber:}\ \min \sum_{i \in I} w_i \sqrt{(x - a_i)^2 + (y - b_i)^2}
\qquad
\text{Minimax:}\ \min z \ \text{ s.t. } \ \sqrt{(x - a_i)^2 + (y - b_i)^2} \le z \ \forall i
$$

$$
\text{Quadratico:}\ \min \sum_{i \in I} w_i \left[ (x - a_i)^2 + (y - b_i)^2 \right]
\ \Rightarrow\ \text{baricentro pesato (forma chiusa)}
$$

Tutti convessi. Vincolo geografico tipico (convesso): entro raggio $r$ da
un'infrastruttura.

!!! example "Esempio a mano (1D)"
    Clienti nei km 0, 4, 10 con pesi 1, 1, 3. Weber = **mediana pesata** = 10;
    baricentro = 6,8; minimax = 5. Tre obiettivi ragionevoli, tre risposte diverse:
    la scelta dell'obiettivo *è* la decisione manageriale.

## Caso di studio

12 quartieri (pesi 5–25 mila abitanti), vincolo: entro 2 km dalla cabina elettrica
in (7, 6). Dati in `dati/localizzazione_quartieri.csv`.

```text
Baricentro : (4,90, 5,40)
Weber      : (4,89, 5,31)  dist. media 3,344 km   max 6,314 km
Minimax    : (5,50, 5,03)  dist. media 3,391 km   max 5,680 km
Weber vincolato: (5,08, 5,43)  costo +0,2% (vincolo attivo, ottimo sul bordo)
```

![Mappa delle localizzazioni](img/cap09_mappa.png)

Il minimax si sposta di oltre mezzo km per proteggere le periferie; il vincolo della
cabina costa quasi nulla (+0,2%): scoprire che un vincolo temuto è quasi gratis è un
risultato manageriale importante quanto l'ottimo.

## Sensitività: frontiera efficienza-equità

Metodo ε-constraint: minima distanza media con tetto $D$ sulla massima.

![Frontiera efficienza-equità](img/cap09_frontiera.png)

La frontiera è quasi piatta: garantire 0,63 km in meno al quartiere più lontano
costa solo 47 metri di distanza media — l'equità qui è "quasi gratis".

## Esercizi

1. Ricalcolare a mano il baricentro pesato dai CSV.
2. Peso di Q12 da 5 a 40: Weber migra di 1,23 km; il minimax **non si muove**
   (ignora i pesi).
3. Due strutture con assegnazione al più vicino: perché il problema non è più
   convesso?
4. Distanza Manhattan: mostrare che Weber diventa un LP (mediane pesate per
   coordinata).
5. Moltiplicatore del raggio: con $r = 2 \to 2{,}1$ il costo scende da 535,79 a
   535,22.
