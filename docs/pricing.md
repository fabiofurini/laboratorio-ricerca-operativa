# Pricing e revenue management

**Classe:** NLP concavo / non convesso · **Script:** `python/lab07_pricing.py`

Quale prezzo massimizza il profitto quando la domanda diminuisce al crescere del
prezzo? Qui il prezzo è una *variabile*: la domanda diventa endogena e il profitto
$p \cdot q$ introduce un termine bilineare — il primo incontro con la non convessità.

**Il problema a parole.** *Decidiamo* prezzo $p$ e quantità $q$. *L'obiettivo*:
massimo profitto $(p - c)q$. *I vincoli*: $q \le d(p)$ (domanda) e $q \le k$
(capacità).

## Modello

$$
\max\; p\,q - c\,q
\quad\text{s.t.}\quad q \le d(p), \qquad q \le k, \qquad p, q \ge 0
$$

Domande usate: lineare $d(p) = a - bp$; elasticità costante
$d(p) = \theta p^{-\varepsilon}$; logistica $d(p) = m/(1 + e^{-\alpha + \beta p})$.
Con domanda lineare il profitto ridotto $(p - c)(a - bp)$ è una parabola concava;
Gurobi risolve comunque la forma bilineare all'ottimo globale (`NonConvex=2`).

!!! example "Esempio a mano (concerto)"
    $d(p) = 1200 - 5p$, $c = 20$ €, $k = 400$ posti.

    1. Senza capacità: $p^\circ = (a/b + c)/2 = 130$ €, $q^\circ = 550$.
    2. La capacità morde ($550 > 400$): $p^* = (a - k)/b = 160$ €, profitto 56.000 €.
    3. Valore di un posto in più: $\frac{d\Pi}{dk} = (p^* - c) + k \frac{dp^*}{dk}
       = 140 - 80 = 60$ € — **non** il margine pieno: per riempire il posto si
       abbassa il prezzo a tutti.

## Risultati

```text
Gurobi:  p* = 160 €, q* = 400, profitto 56.000 €
Valore marginale di un posto: 59,80 € (teoria: 60)
Elasticità costante: p* = 79,11 €   (ottimo nel punto di spigolo d(p) = k)
Logistica          : p* = 138,29 €, profitto 47.317 €
Due categorie con sostituzione: p = (234, 197) €, profitto 85.149 €
```

![Profitto e valore della capienza](img/cap07_profitto.png)

![Tre funzioni di domanda](img/cap07_domande.png)

!!! tip "L'ottimo nel punto di spigolo"
    Con elasticità costante l'ottimo non vincolato sarebbe
    $c\varepsilon/(\varepsilon - 1) = 36{,}67$ €, ma lì la domanda esplode oltre la
    capienza: l'ottimo vero è nello spigolo $d(p) = k$, cioè
    $p^* = (\theta/k)^{1/\varepsilon} = 79{,}11$ € — dove nessuna derivata si
    annulla. Mai cercare l'ottimo solo tra i punti stazionari.

Nel **multiprodotto** (platea/galleria con sostituzione) i prezzi vanno decisi
congiuntamente: il modello tiene cara la platea per spingere domanda in galleria.

## Esercizi

1. Verificare il valore del posto per $k = 300$ (100 €) con Gurobi e con la formula.
2. Costo marginale $c = 60$: $p^*$ resta 160 (capacità ancora attiva), profitto
   40.000 €, valore posto 20 €.
3. Penalità reputazionale $-2(p - 120)^2$: il problema resta concavo? Cambia l'ottimo?
4. $p^*(\varepsilon)$ per $\varepsilon \in [1{,}3;\, 3]$ con $k = 400$.
5. +50 posti di platea (+3.287 €) o di galleria (+3.838 €): quale ampliamento
   conviene?
