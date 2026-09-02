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
modello. Eccezioni dichiarate: variabili aleatorie ($D$, $L$), la funzione di
ripartizione $F$ e il parametro $C$ della SVM.

## Programmazione lineare e dualità

$$
\text{(P)}\;\; \min \sum_{j=1}^{n} c_j x_j
\;\;\text{soggetto a}\;\; \sum_{j=1}^{n} a_{kj} x_j \ge b_k \;\;\forall k \in \{1,\dots,m\}, \;\; x_j \ge 0 \;\;\forall j \in \{1,\dots,n\}
\qquad
\text{(D)}\;\; \max \sum_{k=1}^{m} b_k y_k
\;\;\text{soggetto a}\;\; \sum_{k=1}^{m} a_{kj} y_k \le c_j \;\;\forall j \in \{1,\dots,n\}, \;\; y_k \ge 0 \;\;\forall k \in \{1,\dots,m\}
$$

All'ottimo i due valori coincidono (**dualità forte**) e $y_k$ è il **prezzo ombra**
della risorsa $k$: di quanto migliora l'ottimo se $b_k$ aumenta di una unità.

!!! example "Esempio 2×2, svolto"
    $\max 30x_1 + 50x_2$ soggetto a $x_1 + 3x_2 \le 90$ (ore), $2x_1 + x_2 \le 80$ (kg).

    Entrambi i vincoli attivi all'ottimo: risolvendo il sistema, $x_2 = 20$,
    $x_1 = 30$, valore $z^* = 1900$ €. I duali risolvono $y_1 + 2y_2 = 30$,
    $3y_1 + y_2 = 50$: $y_1 = 14$ (€/ora), $y_2 = 8$ (€/kg). Verifica:
    $90 \cdot 14 + 80 \cdot 8 = 1900 = z^*$. ✓

## L'analisi di sensitività negli LP

Per ogni vincolo e variabile il solver fornisce gratis:

- **prezzo ombra** (`Pi`): valore marginale della risorsa;
- **range di validità** (`SARHSLow/Up`): intervallo del termine noto in cui il prezzo
  ombra resta esatto (per l'esempio: le ore valgono 14 €/ora finché restano in
  $[40, 240]$);
- **costo ridotto** (`RC`): per una variabile a zero, quanto deve migliorare il suo
  coefficiente perché convenga attivarla.

Un vincolo **non attivo** ha sempre prezzo ombra nullo. Nei problemi di *minimo* un
vincolo $\le$ ha `Pi` $\le 0$ (convenzione di Gurobi).

## Condizioni KKT (da Karush, Kuhn e Tucker)

Per $\min f(\boldsymbol x)$ soggetto a $g_i(\boldsymbol x) \le 0$, $h_j(\boldsymbol x) = 0$,
in un ottimo regolare esistono $\lambda_i \ge 0$, $\nu_j$ con:

$$
\nabla f + \sum_i \lambda_i \nabla g_i + \sum_j \nu_j \nabla h_j = \boldsymbol 0,
\qquad \lambda_i\, g_i(\boldsymbol x^*) = 0 \;\; \forall i \in \{1,\dots,m\} .
$$

Se il problema è convesso le KKT sono anche sufficienti. I moltiplicatori
generalizzano i prezzi ombra; quando il solver non li fornisce, si stimano **per
perturbazione** (aumentare il termine noto di $\varepsilon$, ri-ottimizzare,
rapporto incrementale).

!!! example "KKT svolte"
    $\min x^2 + y^2$ soggetto a $x + y \ge 4$. Stazionarietà: $x = y = \lambda/2$; il
    vincolo dev'essere attivo (altrimenti $x = y = 0$ lo viola): $x = y = 2$,
    $\lambda = 4$. Lettura: portando il termine noto a $4 + \varepsilon$, l'ottimo
    $f^* = 8$ cresce di $\approx 4\varepsilon$.

## Il protocollo di sensitività (usato in ogni capitolo)

1. **Scenario base**: risolvere, verificare, identificare i vincoli attivi.
2. **One-at-a-time**: variare un parametro chiave su una griglia.
3. **Prezzi ombra**: confrontare il duale con una ri-ottimizzazione perturbata.
4. **Scenari**: pessimistico, centrale, ottimistico.
5. **Trade-off**: costruire una frontiera (costo-servizio, rischio-rendimento…).
6. **Stabilità**: dati ±5% → la raccomandazione regge?
