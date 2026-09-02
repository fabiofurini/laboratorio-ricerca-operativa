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
($\boldsymbol{Q}$). Nei modelli la dicitura è sempre «soggetto a», le variabili
sono introdotte prima della formulazione e i vincoli che le definiscono chiudono il
modello.

## Programmazione lineare e dualità

I *dati* sono i costi $c_j$, i coefficienti $a_{ij}$ e i termini noti $b_i$, con
$i \in M = \{1, 2, \dots, m\}$ e $j \in N = \{1, 2, \dots, n\}$. Gli insiemi
$M_1, M_2, M_3$ ripartiscono $M$ secondo il verso del vincolo ($\ge$, $=$, $\le$);
gli insiemi $N_1, N_2, N_3$ ripartiscono $N$ secondo il segno della variabile (non
negative, libere $\gtreqless 0$, non positive). Le *variabili* sono le $x_j$ del primale e, nel duale, una
$y_i$ per ciascun vincolo del primale.

$$
\begin{aligned}
\text{(P)} \qquad \min ~ \sum_{j \in N} c_j x_j & & \\
\text{soggetto a} \quad \sum_{j \in N} a_{ij} x_j &\ge b_i, & \forall i \in M_1, \\
\sum_{j \in N} a_{ij} x_j &= b_i, & \forall i \in M_2, \\
\sum_{j \in N} a_{ij} x_j &\le b_i, & \forall i \in M_3, \\
x_j &\ge 0, & \forall j \in N_1, \\
x_j &\gtreqless 0, & \forall j \in N_2, \\
x_j &\le 0, & \forall j \in N_3; \\[1ex]
\text{(D)} \qquad \max ~ \sum_{i \in M} b_i y_i & & \\
\text{soggetto a} \quad \sum_{i \in M} a_{ij} y_i &\le c_j, & \forall j \in N_1, \\
\sum_{i \in M} a_{ij} y_i &= c_j, & \forall j \in N_2, \\
\sum_{i \in M} a_{ij} y_i &\ge c_j, & \forall j \in N_3, \\
y_i &\ge 0, & \forall i \in M_1, \\
y_i &\gtreqless 0, & \forall i \in M_2, \\
y_i &\le 0, & \forall i \in M_3.
\end{aligned}
$$

**Le regole della dualità** — ogni vincolo del primale genera una variabile duale,
ogni variabile un vincolo duale:

| Primale (min) | Duale (max) |
|---|---|
| vincolo $\ge b_i$ ($i \in M_1$) | variabile $y_i \ge 0$ |
| vincolo $= b_i$ ($i \in M_2$) | variabile $y_i \gtreqless 0$ |
| vincolo $\le b_i$ ($i \in M_3$) | variabile $y_i \le 0$ |
| variabile $x_j \ge 0$ ($j \in N_1$) | vincolo $\le c_j$ |
| variabile $x_j \gtreqless 0$ ($j \in N_2$) | vincolo $= c_j$ |
| variabile $x_j \le 0$ ($j \in N_3$) | vincolo $\ge c_j$ |

All'ottimo i due valori coincidono (**dualità forte**) e $y_i$ è il **prezzo ombra**
della risorsa $i$: di quanto migliora l'ottimo se $b_i$ aumenta di una unità. Il
segno dice il verso in cui la risorsa aiuta: in un minimo, un vincolo $\le$ di
capacità ha $y_i \le 0$, un vincolo $\ge$ di domanda ha $y_i \ge 0$.

## L'analisi di sensitività negli LP

Per ogni vincolo e variabile il solver fornisce gratis:

- **prezzo ombra** ($y_i$, attributo `Pi`): il valore marginale del termine noto,
  $y_i = \partial z^* / \partial b_i$;
- **range di validità** (`SARHSLow/Up`): intervallo del termine noto in cui il prezzo
  ombra resta esatto (nell'esempio 2×2: il prezzo ombra 14 vale finché $b_1$ resta
  in $[40, 240]$);
- **costo ridotto** ($\mathrm{RC}_j$, attributo `RC`): il coefficiente al netto del
  valore, ai prezzi ombra, delle risorse consumate,
  $\mathrm{RC}_j = c_j - \sum_{i \in M} a_{ij} y_i$; per una variabile a zero,
  quanto deve migliorare $c_j$ perché convenga attivarla;
- **range di validità del coefficiente in obiettivo** (`SAObjLow/Up`): l'intervallo
  in cui il coefficiente può variare senza che la base ottima cambi — il "gemello"
  di `SARHSLow/Up` per i costi ridotti (nell'esempio 2×2: $c_1$ può variare in
  $[50/3 \approx 16{,}7,\, 100]$ e $c_2$ in $[15, 90]$ senza spostare la
  soluzione; per una variabile a zero `SAObjUp` è la soglia di convenienza).

Attenzione alla **degenerazione**: può esistere una variabile *in base a valore
zero*, con `RC = 0` pur non essendo usata; vale solo l'implicazione
`RC ≠ 0` ⇒ variabile su un suo bound.

**I segni dei prezzi ombra.** Gurobi usa un'unica convenzione:
$\texttt{Pi}_i = \partial z^* / \partial b_i$, la derivata dell'ottimo rispetto
al termine noto. Il segno si deduce con due domande: *aumentare $b_i$ allarga o
restringe la regione ammissibile?* (la allarga con $\le$, la restringe con
$\ge$); *una regione più ampia come cambia l'ottimo?* (non può mai peggiorarlo).

| Verso del vincolo | minimo | massimo |
|---|---|---|
| $\le$ ($b_i$ ↑ ⇒ regione più ampia) | `Pi ≤ 0` | `Pi ≥ 0` |
| $\ge$ ($b_i$ ↑ ⇒ regione più stretta) | `Pi ≥ 0` | `Pi ≤ 0` |
| $=$ | segno qualunque | segno qualunque |

Un vincolo **non attivo** ha sempre `Pi = 0` (complementarietà).

!!! example "Esempio 2×2, svolto"
    $$
    \begin{array}{r r@{\;}c@{\;}r c r l}
    \max & 30\,x_1 & + & 50\,x_2 & & & \\
    \text{soggetto a} & x_1 & + & 3\,x_2 & \le & 90, & \\
     & 2\,x_1 & + & x_2 & \le & 80, & \\
     & x_1, & & x_2 & \ge & 0. &
    \end{array}
    $$

    **I valori li dà il solver**: $\boldsymbol x = (30, 20)$, $z^* = 1900$,
    `Pi` $= (14, 8)$, `RC` $= (0, 0)$, con range `SARHS`
    $[40, 240]$ e $[30, 180]$, `SAObj` $[50/3, 100]$ e $[15, 90]$; entrambi i
    vincoli attivi.

    **Verifiche delle proprietà**, $\boldsymbol A' \boldsymbol y = \boldsymbol c$
    sulle variabili in base e dualità forte:

    $$
    14 + 16 = 30 = c_1, \qquad 42 + 8 = 50 = c_2,
    \qquad 90 \cdot 14 + 80 \cdot 8 = 1900 = z^* . \quad ✓
    $$

    **Costi ridotti**: $\mathrm{RC}_j = c_j - \sum_i a_{ij} y_i$, il coefficiente
    al netto delle risorse consumate valutate ai prezzi ombra. Qui
    $\mathrm{RC}_1 = 30 - (1 \cdot 14 + 2 \cdot 8) = 0$ e
    $\mathrm{RC}_2 = 50 - (3 \cdot 14 + 1 \cdot 8) = 0$: nulli, come per ogni
    variabile positiva all'ottimo («in base»).

!!! example "Costi ridotti, svolti: conviene una terza variabile?"
    Nell'esempio 2×2 entrambe le variabili sono positive: i loro costi ridotti sono
    $0$ (variabili «in base»). Aggiungiamo una variabile $x_3 \ge 0$ con
    coefficiente $c_3 = 20$ e consumi $a_{13} = a_{23} = 1$.

    Ai prezzi ombra, le risorse assorbite da un'unità valgono
    $1 \cdot 14 + 1 \cdot 8 = 22 > 20$: non conviene. Il solver conferma: soluzione
    invariata $(30, 20, 0)$, $z^* = 1900$, `x3.RC = -2` e `SAObjUp = 22` — il
    coefficiente deve salire di almeno 2 (cioè a 22) perché $x_3$ entri in
    soluzione. Controprova con $c_3 = 23$: la soluzione cambia in $(0, 5, 75)$,
    valore 1975.

    In codice, per ogni variabile a zero (solo LP):

    ```python
    for v in m.getVars():
        if v.X < 1e-6:
            print(v.VarName, v.RC)
    ```

!!! example "Tutti i casi in un solo LP: tre versi di vincolo, tre segni di variabile"
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

    **I valori li dà il solver**: $\boldsymbol x = (60, 40, 0)$, $z^* = 620$,
    `Pi = (0, 6, -1)`, `RC = (0, 0, -3)`, con range `SARHS` $(-\infty, 100]$,
    $[30, +\infty)$, $[-200, +\infty)$ e range `SAObj` $(-\infty, 8]$,
    $[5, 17]$, $(-\infty, -6]$.

    **Verifiche a mano, con le regole della dualità**: $y_1 = 0$ per
    complementarietà (vincolo lasco: $x_1 + x_2 = 100 > 30$); $y_2 = 6$
    (uguaglianza → duale libera); $y_3 = -1 \le 0$ come da regola per un $\le$
    in un minimo. Proprietà $\boldsymbol A' \boldsymbol y = \boldsymbol c$
    sulle variabili in base ($x_2$ libera → uguaglianza) e dualità forte:

    $$
    0 + 6 - 1 = 5 = c_1, \qquad 0 + 6 - 2 \cdot (-1) = 8 = c_2,
    \qquad 30 \cdot 0 + 100 \cdot 6 + (-20)(-1) = 620 = z^* . \quad ✓
    $$

    **Costi ridotti**: $\mathrm{RC}_1 = 5 - 5 = 0$, $\mathrm{RC}_2 = 8 - 8 = 0$
    (in base); $x_3$ è ferma al suo **bound superiore** (zero):

    $$
    \mathrm{RC}_3 = -9 - (-1) \cdot 6 = -3 ,
    $$

    e si attiverebbe solo con coefficiente $\ge -6$ (= `SAObjUp`). Per
    perturbazione: $b_2 = 101 → 626$ ($+6$), $b_3 = -19 → 619$ ($-1$),
    $x_3$ forzata a $-1 → 623$ ($+3$) ✓.

## Convessità e programmazione quadratica

Un **QP** ha obiettivo $\tfrac12 \boldsymbol x' \boldsymbol Q\, \boldsymbol x +
\boldsymbol c' \boldsymbol x$ e vincoli lineari; è convesso se e solo se
$\boldsymbol Q \succeq 0$. In un problema convesso ogni minimo locale è globale:
il solver può *certificare* l'ottimalità.

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

    **I valori li dà il solver**: $x_1 = 4$, $x_2 = 2$, $f^* = 24$, $\lambda = 8$.

    **Verifica del prezzo ombra**: vincolo attivo ($4 + 2 = 6$) e derivate
    parziali coincidenti:

    $$
    2x_1 = 8 = 4x_2 = \lambda . \quad ✓
    $$

    **Verifica per perturbazione**: con termine noto 7 il solver dà
    $f^* = 32{,}67 \approx 24 + 8$ (più il termine di curvatura).

## Condizioni KKT (da Karush, Kuhn e Tucker)

Per $\min f(\boldsymbol x)$ soggetto a $g_i(\boldsymbol x) \le 0$, $h_j(\boldsymbol x) = 0$,
in un ottimo regolare esistono $\lambda_i \ge 0$, $\nu_j$ con:

$$
\nabla f + \sum_i \lambda_i \nabla g_i + \sum_j \nu_j \nabla h_j = \boldsymbol 0,
\qquad \lambda_i\, g_i(\boldsymbol x^*) = 0, \;\; \forall i \in \{1, 2, \dots,m\} .
$$

Se il problema è convesso le KKT sono anche sufficienti. I moltiplicatori
generalizzano i prezzi ombra; quando il solver non li fornisce, si stimano **per
perturbazione** (aumentare il termine noto di $\varepsilon$, ri-ottimizzare,
rapporto incrementale).

!!! example "Le KKT sul QP dell'esempio"
    Sul modello $\min x_1^2 + 2x_2^2$ soggetto a $x_1 + x_2 \ge 6$:
    stazionarietà $2x_1 = \lambda$, $4x_2 = \lambda$; il vincolo dev'essere attivo
    (altrimenti $x_1 = x_2 = 0$ lo viola): $\lambda = 8$, $x_1 = 4$, $x_2 = 2$,
    $f^* = 24$ — gli stessi numeri dati dal solver, ora dalla procedura generale.
    Lettura: con termine noto $6 + \varepsilon$ l'ottimo cresce di
    $\approx 8\varepsilon$ (esatto: $f^*(d) = \tfrac{2}{3}d^2$, quindi
    $24 + 8\varepsilon + \tfrac{2}{3}\varepsilon^2$).

## Il protocollo di sensitività (usato in ogni capitolo)

1. **Scenario base**: risolvere, verificare, identificare i vincoli attivi.
2. **One-at-a-time**: variare un parametro chiave su una griglia.
3. **Prezzi ombra e costi ridotti**: confrontare il duale con una ri-ottimizzazione
   perturbata; leggere `RC` di ogni variabile a zero (la sua soglia di convenienza).
4. **Scenari**: pessimistico, centrale, ottimistico.
5. **Trade-off**: costruire una frontiera (costo-servizio, rischio-rendimento…).
6. **Stabilità**: dati ±5% → la raccomandazione regge?
