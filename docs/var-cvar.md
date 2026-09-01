# VaR e CVaR: misurare e ottimizzare il rischio

**Classe:** LP a scenari · **Script:** `python/lab13_var_cvar.py`

Ottimizzare il valore medio può nascondere perdite rare e molto elevate. Il **VaR**
(*Value-at-Risk*) risponde a "qual è una soglia di perdita elevata?"; il **CVaR**
(*Conditional Value-at-Risk*) anche a "quanto perdiamo *in media* quando la soglia
viene superata?". Sorpresa didattica: il CVaR si ottimizza con un semplice LP.

## Definizioni

Per una perdita aleatoria $L$ e un livello $\alpha \in (0,1)$:

$$
\mathrm{VaR}_\alpha(L) = \inf\{\eta : \mathbb{P}(L \le \eta) \ge \alpha\}
\qquad
\mathrm{CVaR}_\alpha(L) = \text{media della coda peggiore di massa } 1 - \alpha .
$$

Il CVaR è **convesso** e subadditivo (premia la diversificazione); il VaR in
generale no, e non distingue code diverse con lo stesso quantile.

!!! example "Esempio a mano (6 scenari, α = 0,80)"
    Perdite equiprobabili $\{2, 4, 5, 7, 12, 20\}$: VaR $= 12$ (la cumulata tocca
    0,80 lì); CVaR $= 12 + \frac{1}{0{,}20}\cdot\frac{1}{6}(20 - 12) =
    \mathbf{18{,}67}$ — la formula tratta correttamente la massa "a cavallo" del
    quantile. Media $= 8{,}33$: tre numeri, tre storie.

## La formulazione lineare di Rockafellar–Uryasev

Con scenari $s \in S$ di probabilità $\pi_s$ e perdita lineare
$\ell_s(\boldsymbol x)$:

$$
\min_{\boldsymbol x,\, \eta,\, \boldsymbol\xi}\;
\eta + \frac{1}{1 - \alpha} \sum_{s \in S} \pi_s\, \xi_s
\quad\text{s.t.}\;\;
\xi_s \ge \ell_s(\boldsymbol x) - \eta,\;\; \xi_s \ge 0 \;\;\forall s \in S
$$

All'ottimo $\eta^*$ è un VaR e il valore obiettivo è il CVaR: **un solo LP, entrambe
le misure**. Attenzione: $\eta$ è una variabile *libera*
(`addVar(lb=-GRB.INFINITY)`).

## Caso di studio 1: portafoglio mean-CVaR vs Markowitz

220 scenari mensili con **code grasse** ($t$ di Student), rendimento richiesto 8%.

```text
            | perdita media | VaR90  | CVaR90
  mean-CVaR |       -0,0067 | 0,0327 | 0,0489
  Markowitz |       -0,0067 | 0,0329 | 0,0531   (-8% di coda per il mean-CVaR)
```

![Distribuzione delle perdite e frontiera](img/cap13_perdite_frontiera.png)

A parità di rendimento e perdita media, il mean-CVaR taglia la coda: la varianza
penalizza simmetricamente sopra e sotto la media, il CVaR guarda solo dove fa male.

## Caso di studio 2: supply chain a due stadi

Capacità prenotata *prima* dello scenario (F1 economico ma fragile: nel 12% degli
scenari crolla al 30%; F2 caro ma affidabile), flussi e shortage come ricorso.

```text
lambda = 0,0: F1 161,5  F2 134,2 | medio 1.724  CVaR90 2.902 | servizio 98,7%
lambda = 0,5: F1  92,7  F2 212,7 | medio 1.803  CVaR90 2.217 | servizio 99,9%
lambda = 1,0: F1  68,5  F2 236,9 | medio 1.906  CVaR90 2.139
```

Al crescere dell'avversione al rischio la capacità migra verso il fornitore
affidabile: **+79 € di costo medio comprano −685 € di CVaR** — il costo della
resilienza, quantificato.

!!! warning "Limiti statistici"
    Con $\alpha = 0{,}99$ e 220 scenari la coda contiene 2–3 scenari: il CVaR
    stimato è quasi rumore. Servono decine di scenari *oltre* il quantile; il VaR
    può non essere unico su distribuzioni discrete.

## Esercizi

1. Sei scenari con $\alpha = 0{,}90$: VaR = CVaR = 20 (la coda sta tutta
   sull'ultimo punto).
2. Costruire un esempio in cui il VaR viola la subadditività (due prestiti
   indipendenti) e verificare che il CVaR no.
3. CVaR ottimo per $\alpha \in \{0{,}8;\, 0{,}9;\, 0{,}95;\, 0{,}99\}$: quando
   iniziano le instabilità?
4. Forma vincolata $\max \sum_i \mu_i x_i$ s.t. $\mathrm{CVaR} \le k$: stessa
   frontiera, duale = rendimento marginale del rischio.
5. Stress test: scenario estremo con probabilità 1% — come cambia la prenotazione?
