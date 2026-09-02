# Richiami: LP, QP, NLP e analisi di sensitività

Gli strumenti teorici usati in tutto il laboratorio, in forma compatta.

## Le tre classi di modelli

- **LP** (*Linear Programming*): obiettivo e vincoli lineari;
- **QP** (*Quadratic Programming*): obiettivo quadratico, vincoli lineari;
- **NLP** (*Nonlinear Programming*): obiettivo o vincoli non lineari generali.

Un problema è **convesso** quando ogni minimo locale è anche globale: per gli LP è
sempre vero; per QP e NLP dipende dalle funzioni.

**Notazione.** Scalari e indici minuscoli ($x_{it}$, $\lambda$); gli oggetti dei
modelli (prodotti, canali, titoli, scenari…) sono **numerati** e gli indici corrono
su insiemi enumerati esplicitamente, $i \in \{1, 2, \dots, n\}$; i conteggi sono
interi ($n \in \mathbb{Z}_{\ge 1}$) e i dati razionali ($\mathbb{Q}$); vettori
minuscoli in grassetto ($\boldsymbol{x}$), matrici maiuscole in grassetto
($\boldsymbol{Q}$); le variabili duali si chiamano $\pi_i$, i costi ridotti
$\bar c_j$; la **barra** indica quantità valutate in una soluzione ammissibile, la
**tilde** una soluzione ottima ($\tilde{\boldsymbol x}$, $\tilde z$). Nei modelli la
dicitura è sempre «soggetto a», le variabili sono introdotte prima della
formulazione e i vincoli che le definiscono chiudono il modello.

## Programmazione lineare e dualità

I *dati* sono i costi $c_j$, i coefficienti $a_{ij}$ e i termini noti $b_i$, con
$i \in M = \{1, 2, \dots, m\}$ e $j \in N = \{1, 2, \dots, n\}$. Gli insiemi
$M_{\le}, M_{=}, M_{\ge}$ ripartiscono $M$ secondo il verso del vincolo; gli
insiemi $N_{\ge 0}, N_{\gtreqless 0}, N_{\le 0}$ ripartiscono $N$ secondo il segno
della variabile (non negative, libere, non positive). Le *variabili* sono le $x_j$
del primale e, nel duale, una $\pi_i$ per ciascun vincolo del primale.

$$
\begin{aligned}
\text{(P)} \qquad \max ~ \sum_{j \in N} c_j x_j & & \\
\text{soggetto a} \quad \sum_{j \in N} a_{ij} x_j &\le b_i, & \forall i \in M_{\le}, \\
\sum_{j \in N} a_{ij} x_j &= b_i, & \forall i \in M_{=}, \\
\sum_{j \in N} a_{ij} x_j &\ge b_i, & \forall i \in M_{\ge}, \\
x_j &\ge 0, & \forall j \in N_{\ge 0}, \\
x_j &\gtreqless 0, & \forall j \in N_{\gtreqless 0}, \\
x_j &\le 0, & \forall j \in N_{\le 0}; \\[1ex]
\text{(D)} \qquad \min ~ \sum_{i \in M} b_i \pi_i & & \\
\text{soggetto a} \quad \sum_{i \in M} a_{ij} \pi_i &\ge c_j, & \forall j \in N_{\ge 0}, \\
\sum_{i \in M} a_{ij} \pi_i &= c_j, & \forall j \in N_{\gtreqless 0}, \\
\sum_{i \in M} a_{ij} \pi_i &\le c_j, & \forall j \in N_{\le 0}, \\
\pi_i &\ge 0, & \forall i \in M_{\le}, \\
\pi_i &\gtreqless 0, & \forall i \in M_{=}, \\
\pi_i &\le 0, & \forall i \in M_{\ge}.
\end{aligned}
$$

**Le regole della dualità** — ogni vincolo del primale genera una variabile duale,
ogni variabile un vincolo duale:

| Primale (max) | Duale (min) |
|---|---|
| vincolo $\le b_i$ ($i \in M_{\le}$) | variabile $\pi_i \ge 0$ |
| vincolo $= b_i$ ($i \in M_{=}$) | variabile $\pi_i \gtreqless 0$ |
| vincolo $\ge b_i$ ($i \in M_{\ge}$) | variabile $\pi_i \le 0$ |
| variabile $x_j \ge 0$ ($j \in N_{\ge 0}$) | vincolo $\ge c_j$ |
| variabile $x_j \gtreqless 0$ ($j \in N_{\gtreqless 0}$) | vincolo $= c_j$ |
| variabile $x_j \le 0$ ($j \in N_{\le 0}$) | vincolo $\le c_j$ |

Le *uguaglianze* del primale danno duali *libere* (e viceversa); per un primale di
**minimo** la tabella si legge da destra a sinistra.

**Teorema (dualità debole).** Per ogni soluzione ammissibile $(\bar x_1, \dots, \bar x_n)$
di (P) e ogni soluzione ammissibile $(\bar\pi_1, \dots, \bar\pi_m)$ di (D):

$$
\sum_{j \in N} c_j \bar x_j \;\le\; \sum_{i \in M} b_i \bar\pi_i .
$$

**Teorema (dualità forte).** (P) ha una soluzione ottima $(\tilde x_1, \dots, \tilde x_n)$
**se e solo se** (D) ha una soluzione ottima $(\tilde\pi_1, \dots, \tilde\pi_m)$,
e in tal caso i valori ottimi coincidono:

$$
\sum_{j \in N} c_j \tilde x_j \;=\; \sum_{i \in M} b_i \tilde\pi_i .
$$

La dualità debole dice che ogni soluzione ammissibile del duale è un *limite
superiore* per il primale di massimo: se due soluzioni ammissibili hanno lo stesso
valore, sono entrambe ottime. La dualità forte garantisce che all'ottimo il
divario si chiude sempre (gli ottimi possono essere più d'uno, i valori ottimi
coincidono).

!!! example "Costruire il duale con le regole: l'LP 2×2"
    L'LP 2×2 è proprio nella forma canonica di massimo (vincoli ≤, variabili non
    negative):

    $$
    \begin{array}{r r@{\;}c@{\;}r c r l}
    \max & 30\,x_1 & + & 50\,x_2 & & & \\
    \text{soggetto a} & x_1 & + & 3\,x_2 & \le & 90, & \\
     & 2\,x_1 & + & x_2 & \le & 80, & \\
     & x_1, & & x_2 & \ge & 0. &
    \end{array}
    $$

    Ogni vincolo genera una variabile duale ($\le$ in un massimo ⇒
    $\pi_1, \pi_2 \ge 0$); ogni variabile genera un vincolo duale, con i
    coefficienti presi per **colonna** e i costi come termini noti; l'obiettivo
    scambia i ruoli:

    $$
    \begin{array}{r r@{\;}c@{\;}r c r l}
    \min & 90\,\pi_1 & + & 80\,\pi_2 & & & \\
    \text{soggetto a} & \pi_1 & + & 2\,\pi_2 & \ge & 30, & \\
     & 3\,\pi_1 & + & \pi_2 & \ge & 50, & \\
     & \pi_1, & & \pi_2 & \ge & 0. &
    \end{array}
    $$

!!! example "Costruire il duale con le regole: tutti i casi in un solo LP"
    Un LP di **minimo** con tutti i casi della tabella (tre versi, tre segni; la
    tabella si legge da destra a sinistra):

    $$
    \begin{array}{r r@{\;}c@{\;}r@{\;}c@{\;}r c r}
    \min & 5\,x_1 & + & 8\,x_2 & - & 9\,x_3 & & \\
    \text{soggetto a} & x_1 & + & x_2 & & & \ge & 30, \\
     & x_1 & + & x_2 & - & x_3 & = & 100, \\
     & x_1 & - & 2\,x_2 & & & \le & -20, \\
     & x_1 & & & & & \ge & 0, \\
     & & & x_2 & & & \gtreqless & 0, \\
     & & & & & x_3 & \le & 0.
    \end{array}
    $$

    Variabili duali: $\pi_1 \ge 0$ (vincolo $\ge$ in un minimo),
    $\pi_2 \gtreqless 0$ (uguaglianza), $\pi_3 \le 0$ (vincolo $\le$).
    Vincoli duali per colonna: da $x_1 \ge 0$ nasce
    $\pi_1 + \pi_2 + \pi_3 \le 5$; da $x_2 \gtreqless 0$ nasce
    $\pi_1 + \pi_2 - 2\pi_3 = 8$; da $x_3 \le 0$ nasce $-\pi_2 \ge -9$:

    $$
    \begin{array}{r r@{\;}c@{\;}r@{\;}c@{\;}r c r}
    \max & 30\,\pi_1 & + & 100\,\pi_2 & - & 20\,\pi_3 & & \\
    \text{soggetto a} & \pi_1 & + & \pi_2 & + & \pi_3 & \le & 5, \\
     & \pi_1 & + & \pi_2 & - & 2\,\pi_3 & = & 8, \\
     & & - & \pi_2 & & & \ge & -9, \\
     & \pi_1 & & & & & \ge & 0, \\
     & & & \pi_2 & & & \gtreqless & 0, \\
     & & & & & \pi_3 & \le & 0.
    \end{array}
    $$

## Le condizioni di ottimalità dell'LP: gli scarti complementari

A ogni vincolo associamo lo *scarto* $\bar s_i$, a ogni variabile il *costo
ridotto* $\bar c_j$ (lo scarto del vincolo *duale*), valutati in soluzioni
ammissibili $(\bar x_1, \dots, \bar x_n)$, $(\bar\pi_1, \dots, \bar\pi_m)$:

$$
\bar s_i = \sum_{j \in N} a_{ij} \bar x_j - b_i, \quad \forall i \in M,
\qquad
\bar c_j = c_j - \sum_{i \in M} a_{ij} \bar\pi_i, \quad \forall j \in N.
$$

Una coppia di soluzioni ammissibili è ottima per entrambi i problemi **se e solo
se** valgono gli **scarti complementari**:

$$
\bar\pi_i \cdot \bar s_i = 0, \quad \forall i \in M,
\qquad
\bar x_j \cdot \bar c_j = 0, \quad \forall j \in N.
$$

In parole: **vincolo lasco ⇒ duale a zero**, e variabile diversa da zero ⇒ costo
ridotto nullo. All'ottimo sono *implicazioni*, non equivalenze (degenerazione:
può esistere una variabile a zero con costo ridotto nullo).

**Due letture da ricordare:**

- **prezzo ombra** $\tilde\pi_i = \partial \tilde z / \partial b_i$: il valore
  marginale del termine noto; vale nell'**intervallo di validità del termine
  noto** $[b_i^{\min}, b_i^{\max}]$, il più grande intervallo in cui, variando
  solo $b_i$, il prezzo ombra resta esattamente $\tilde\pi_i$. Vincolo non
  attivo ⇒ $\tilde\pi_i = 0$;
- **costo ridotto** $\bar c_j$: per una variabile a zero, di quanto deve
  migliorare $c_j$ perché convenga attivarla; vale nell'**intervallo di validità
  del coefficiente** $[c_j^{\min}, c_j^{\max}]$, il più grande intervallo in cui,
  variando solo $c_j$, la soluzione ottima non cambia (per una variabile a zero
  la soglia di convenienza è uno dei due estremi). Variabile diversa da zero ⇒
  $\bar c_j = 0$.

**I segni dei prezzi ombra.** Il segno di
$\tilde\pi_i = \partial \tilde z / \partial b_i$ si deduce con due domande:
*aumentare $b_i$ allarga o restringe la regione ammissibile?* (la allarga con
$\le$, la restringe con $\ge$); *una regione più ampia come cambia l'ottimo?*
(non può mai peggiorarlo).

| Verso del vincolo | minimo | massimo |
|---|---|---|
| $\le$ ($b_i$ ↑ ⇒ regione più ampia) | $\tilde\pi_i \le 0$ | $\tilde\pi_i \ge 0$ |
| $\ge$ ($b_i$ ↑ ⇒ regione più stretta) | $\tilde\pi_i \ge 0$ | $\tilde\pi_i \le 0$ |
| $=$ | segno qualunque | segno qualunque |

Un vincolo **non attivo** ha sempre $\tilde\pi_i = 0$ (complementarietà).

!!! example "Dualità sull'LP 2×2, svolta per intero"
    **Risolvendo si ottiene**: $(\tilde x_1, \tilde x_2) = (30, 20)$,
    $\tilde z = 1900$, $(\tilde\pi_1, \tilde\pi_2) = (14, 8)$,
    $(\bar c_1, \bar c_2) = (0, 0)$, con intervalli di validità
    $[b_1^{\min}, b_1^{\max}] = [40, 240]$, $[b_2^{\min}, b_2^{\max}] = [30, 180]$,
    $[c_1^{\min}, c_1^{\max}] = [50/3, 100]$, $[c_2^{\min}, c_2^{\max}] = [15, 90]$;
    entrambi i vincoli attivi.

    **Verifiche**: $x_1, x_2 \ne 0$ ⇒ vincoli duali attivi
    ($\bar c_1 = \bar c_2 = 0$) e dualità forte:

    $$
    14 + 16 = 30 = c_1, \qquad 42 + 8 = 50 = c_2,
    \qquad 90 \cdot 14 + 80 \cdot 8 = 1900 = \tilde z . \quad ✓
    $$

!!! example "Tutti i casi in un solo LP: verifica delle condizioni"
    **Risolvendo si ottiene**: $(\tilde x_1, \tilde x_2, \tilde x_3) = (60, 40, 0)$,
    $\tilde z = 620$, $(\tilde\pi_1, \tilde\pi_2, \tilde\pi_3) = (0, 6, -1)$,
    $(\bar c_1, \bar c_2, \bar c_3) = (0, 0, -3)$, con intervalli di validità dei termini
    noti $(-\infty, 100]$, $[30, +\infty)$, $[-200, +\infty)$ e dei coefficienti
    $(-\infty, 8]$, $[5, 17]$, $(-\infty, -6]$.

    **Verifiche con le regole**: $\tilde\pi_1 = 0$ per complementarietà (vincolo
    lasco: $60 + 40 = 100 > 30$); $\tilde\pi_2 = 6$ (uguaglianza → duale libera);
    $\tilde\pi_3 = -1 \le 0$ ($\le$ in un minimo). Vincoli duali di $x_1, x_2$
    attivi e dualità forte:

    $$
    0 + 6 - 1 = 5 = c_1, \qquad 0 + 6 - 2 \cdot (-1) = 8 = c_2,
    \qquad 30 \cdot 0 + 100 \cdot 6 + (-20)(-1) = 620 = \tilde z . \quad ✓
    $$

    **Costi ridotti, uno per segno**: $\bar c_1 = 5 - 5 = 0$,
    $\bar c_2 = 8 - 8 = 0$; $x_3$ è ferma al suo **bound superiore** (zero):

    $$
    \bar c_3 = -9 - (-1) \cdot 6 = -3 ,
    $$

    e si attiverebbe solo con coefficiente $\ge -6$ ($= c_3^{\max}$). Per
    perturbazione: $b_2 = 101 → 626$ ($+6$), $b_3 = -19 → 619$ ($-1$),
    $x_3$ forzata a $-1 → 623$ ($+3$) ✓.

## L'analisi di sensitività negli LP

Insieme alla soluzione arrivano gratis quattro numeri per ogni vincolo e variabile:

- il **prezzo ombra** $\tilde\pi_i$: valore marginale del termine noto;
- l'**intervallo di validità del termine noto** $[b_i^{\min}, b_i^{\max}]$
  (nell'esempio 2×2: il prezzo ombra 14 vale finché $b_1$ resta in $[40, 240]$);
- il **costo ridotto** $\bar c_j$: per una variabile a zero, quanto deve
  migliorare il suo coefficiente perché convenga attivarla;
- l'**intervallo di validità del coefficiente** $[c_j^{\min}, c_j^{\max}]$
  (nell'esempio 2×2: $c_1$ può variare in $[50/3, 100]$ e $c_2$ in $[15, 90]$
  senza spostare la soluzione).

!!! example "Prezzi ombra in pratica"
    Sull'LP 2×2 ($\tilde z = 1900$, $\tilde\pi_1 = 14$): una unità in più di
    $b_1$ vale 14; se costasse 12, converrebbe. Per perturbazione:

    $$
    b_1 = 91 \Rightarrow 1914 = 1900 + 14,
    \qquad
    b_1 = 100 \Rightarrow 2040 = 1900 + 10 \cdot 14,
    $$

    esatto perché $100 \in [40, 240]$. A $b_1 = 240$ la struttura cambia: oltre,
    ogni unità vale meno di 14. Con $b_1 = 300$ il vincolo sarebbe non attivo e
    il prezzo ombra $0$.

!!! example "Costi ridotti in pratica: conviene una terza variabile?"
    Aggiungiamo all'LP 2×2 una variabile $x_3 \ge 0$ con coefficiente $c_3 = 20$
    e consumi $a_{13} = a_{23} = 1$. Ai prezzi ombra le risorse assorbite valgono

    $$
    1 \cdot 14 + 1 \cdot 8 = 22 > 20 = c_3 ,
    \qquad
    \bar c_3 = 20 - 22 = -2 :
    $$

    la soluzione resta $(30, 20, 0)$ con $\tilde z = 1900$ e $c_3^{\max} = 22$ —
    il coefficiente deve salire almeno a 22. Controprova con $c_3 = 23$: la
    soluzione cambia in $(0, 5, 75)$, valore 1975.

## Convessità e programmazione quadratica

Un **QP** ha obiettivo $\tfrac12 \boldsymbol x' \boldsymbol Q\, \boldsymbol x +
\boldsymbol c' \boldsymbol x$ e vincoli lineari; è convesso se e solo se
$\boldsymbol Q \succeq 0$. In un problema convesso ogni minimo locale è globale:
l'ottimalità si può *certificare*.

!!! example "Un QP 2×2, svolto per intero"
    Obiettivo quadratico separabile e un vincolo di soglia sulla somma:

    $$
    \begin{array}{r r@{\;}c@{\;}r c r l}
    \min & x_1^2 & + & 2\,x_2^2 & & & \\
    \text{soggetto a} & x_1 & + & x_2 & \ge & 6, & \\
     & x_1, & & x_2 & \ge & 0. &
    \end{array}
    $$

    $\boldsymbol Q = \mathrm{diag}(2, 4) \succ 0$: convesso, ottimo globale.
    **Risolvendo si ottiene**: $\tilde x_1 = 4$, $\tilde x_2 = 2$,
    $\tilde f = 24$, $\lambda = 8$.
    **Verifica**: vincolo attivo ($4 + 2 = 6$) e derivate parziali coincidenti:

    $$
    2\tilde x_1 = 8 = 4\tilde x_2 = \lambda . \quad ✓
    $$

    **Per perturbazione**: con termine noto 7, $\tilde f = 32{,}67 \approx 24 + 8$
    (più il termine di curvatura).

## Le condizioni di ottimalità non lineari: le KKT

Per $\min f(\boldsymbol x)$ soggetto a $g_i(\boldsymbol x) \le 0$, $h_j(\boldsymbol x) = 0$,
in un ottimo regolare $\tilde{\boldsymbol x}$ esistono $\lambda_i \ge 0$, $\nu_j$ con:

$$
\nabla f + \sum_i \lambda_i \nabla g_i + \sum_j \nu_j \nabla h_j = \boldsymbol 0,
\qquad \lambda_i\, g_i(\tilde{\boldsymbol x}) = 0, \;\; \forall i \in \{1, 2, \dots,m\} .
$$

Se il problema è convesso le KKT sono anche sufficienti. **Nel caso lineare le
KKT sono esattamente gli scarti complementari** della coppia (P)–(D): la
stazionarietà è l'ammissibilità del duale (moltiplicatori = $\pi_i$, e i
moltiplicatori dei vincoli di segno sono i costi ridotti), la complementarietà è
$\bar\pi_i \cdot \bar s_i = 0$. I moltiplicatori generalizzano i prezzi ombra;
quando i duali non sono disponibili, si stimano **per perturbazione** (aumentare
il termine noto di $\varepsilon$, ri-ottimizzare, rapporto incrementale).

!!! example "Le KKT sul QP dell'esempio"
    Sul modello $\min x_1^2 + 2x_2^2$ soggetto a $x_1 + x_2 \ge 6$:
    stazionarietà $2x_1 = \lambda$, $4x_2 = \lambda$; il vincolo dev'essere attivo
    (altrimenti $x_1 = x_2 = 0$ lo viola): $\lambda = 8$, $\tilde x_1 = 4$,
    $\tilde x_2 = 2$, $\tilde f = 24$ — gli stessi numeri di prima, ora dalla
    procedura generale. Con termine noto $6 + \varepsilon$ l'ottimo cresce di
    $\approx 8\varepsilon$ (esatto: $\tilde f(d) = \tfrac{2}{3}d^2$, quindi
    $24 + 8\varepsilon + \tfrac{2}{3}\varepsilon^2$).

## Il protocollo di sensitività (usato in ogni capitolo)

1. **Scenario base**: risolvere, verificare, identificare i vincoli attivi.
2. **One-at-a-time**: variare un parametro chiave su una griglia.
3. **Prezzi ombra e costi ridotti**: confrontare il duale con una ri-ottimizzazione
   perturbata; leggere $\bar c_j$ di ogni variabile a zero (la sua soglia di
   convenienza).
4. **Scenari**: pessimistico, centrale, ottimistico.
5. **Trade-off**: costruire una frontiera (costo-servizio, rischio-rendimento…).
6. **Stabilità**: dati ±5% → la raccomandazione regge?
