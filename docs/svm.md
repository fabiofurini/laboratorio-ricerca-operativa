# Support Vector Machine: ottimizzazione per il machine learning

**Classe:** QP convesso · **Script:** `python/lab14_svm.py`

La SVM collega l'ottimizzazione convessa al machine learning: il classificatore si
ottiene risolvendo un QP. Qui **niente librerie di ML**: ogni modello è un QP
scritto e risolto con Gurobi, per capire *che cosa* ottimizza un classificatore.
Le etichette $y_i \in \{-1, +1\}$ sono **dati**; le variabili (coefficienti,
intercetta, scarti, moltiplicatori) tutte continue.

## Hard margin

Dati $n$ punti $\boldsymbol x_i \in \mathbb{R}^p$ con etichette $y_i$:

$$
\min_{\boldsymbol w, b}\; \tfrac12 \|\boldsymbol w\|^2
\quad\text{s.t.}\quad
y_i \Bigl( \sum_{j=1}^{p} w_j x_{ij} + b \Bigr) \ge 1 \quad \forall i = 1, \dots, n
$$

Il margine geometrico è $2/\|\boldsymbol w\|$: minimizzare la norma = massimizzare
il margine.

!!! example "Esempio a mano (2 punti)"
    $\boldsymbol x_1 = (0,0)$, $y_1 = -1$; $\boldsymbol x_2 = (2,2)$, $y_2 = +1$:
    $\boldsymbol w = (0{,}5;\, 0{,}5)$, $b = -1$, margine $2\sqrt2$ = distanza tra i
    punti; entrambi support vector.

## Soft margin e il ruolo di C

$$
\min\; \tfrac12\|\boldsymbol w\|^2 + C \sum_{i=1}^{n} \xi_i
\quad\text{s.t.}\;\;
y_i \Bigl( \sum_j w_j x_{ij} + b \Bigr) \ge 1 - \xi_i,\;\; \xi_i \ge 0 .
$$

Caso di studio (90 clienti, rischio di credito):

```text
C =  0,05: margine 2,42 | errori 2 | nel margine 22   (regolarizzato)
C =  1,00: margine 1,28 | errori 2 | nel margine  7
C = 20,00: margine 0,36 | errori 0 | nel margine  3   (insegue ogni punto)
```

![Soft margin e support vector](img/cap14_svm.png)

## Il duale e i support vector

$$
\max_{\boldsymbol\alpha}\; \sum_{i=1}^{n} \alpha_i
- \tfrac12 \sum_{i=1}^{n}\sum_{j=1}^{n} \alpha_i \alpha_j y_i y_j\,
\boldsymbol x_i^{\mathsf T} \boldsymbol x_j
\quad\text{s.t.}\;\; \sum_{i=1}^{n} \alpha_i y_i = 0,\;\; 0 \le \alpha_i \le C
$$

```text
w e b dal duale = identici al primale; valore 4,7868 (dualità forte)
alpha = 0     : 83 punti -> irrilevanti per la frontiera
0 < alpha < C :  2 punti -> ESATTAMENTE sul margine (da loro si ricava b)
alpha = C     :  5 punti -> dentro il margine (xi > 0)
```

La soluzione dipende solo dai punti con $\alpha_i > 0$: i **support vector**.
E il duale dipende dai dati solo tramite i prodotti scalari: la porta del kernel.

## Kernel RBF

Sostituendo $\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$ con
$K(\boldsymbol x, \boldsymbol z) = e^{-\gamma\|\boldsymbol x - \boldsymbol z\|^2}$
si ottengono frontiere curve **restando in un QP convesso**.

```text
gamma = 0,1: errori 1, support vector 20   (frontiera regolare)
gamma = 0,7: errori 0, support vector 15
gamma = 5,0: errori 0, support vector 61   <- "memorizza" i punti (overfitting)
```

Convessità del *training* ≠ capacità di *generalizzare*: $C$ e $\gamma$ vanno scelti
per cross-validation.

## Classi sbilanciate e SVR

```text
costi uguali            : precision 1,00   recall insolventi 0,94
costo 10x su insolventi : precision 0,97   recall insolventi 1,00
```

I pesi devono riflettere i **costi decisionali**, non le frequenze delle classi.

![Support Vector Regression](img/cap14_svr.png)

**SVR**: tubo di tolleranza $\pm\varepsilon$ senza penalità; sui dati
prezzo→domanda recupera $-10{,}86\,p + 220{,}3$ (vera: $-11p + 220$) usando solo i
14 punti fuori dal tubo.

## Esercizi

1. Hard margin con $\boldsymbol x_2 = (4, 0)$: $\boldsymbol w = (0{,}5;\, 0)$,
   $b = -1$, margine 4.
2. Verificare le tre condizioni di complementarietà sui 7 support vector.
3. Curva di validazione in $C$: training monotono, validazione a U.
4. Soglia decisionale $\theta$ con costi 10:1: tracciare precision/recall.
5. One-Class SVM sul dataset a corona al variare di $\nu$.
