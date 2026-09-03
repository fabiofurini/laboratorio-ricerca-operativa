# Portafoglio di Markowitz

**Classe:** QP convesso · **Script:** `python/lab06_markowitz.py`

Quanto investire in ciascun titolo per bilanciare rendimento atteso e rischio? Il
risultato non è un numero ma una **frontiera efficiente**: il menu completo dei
compromessi tra cui il decisore sceglie.

**Il problema a parole.** *Decidiamo* le quote di capitale $x_i$. *L'obiettivo*:
minima varianza del portafoglio. *I vincoli*: quote a somma 1, rendimento atteso
minimo $\bar r$, limiti $\ell_i \le x_i \le u_i$.

## Modello

**Dati (input del modello).**

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di titoli; i titoli sono indicizzati da $i \in \{1, 2, \dots, n\}$ |
| $\mu_i$ | $\in \mathbb{Q}$ | rendimento atteso del titolo $i$ (per anno) |
| $q_{ij}$ | $\in \mathbb{Q}$ | covarianza tra i rendimenti dei titoli $i$ e $j$; la matrice $\boldsymbol Q = (q_{ij})$ è semidefinita positiva ($\boldsymbol Q \succeq 0$) |
| $\bar r$ | $\in \mathbb{Q}$ | rendimento atteso minimo richiesto |
| $\ell_i,\, u_i$ | $\in \mathbb{Q},\ 0 \le \ell_i \le u_i \le 1$ | quota minima e massima investibile nel titolo $i$ |

**Variabili decisionali.** Introduciamo le seguenti $n$ variabili non negative:

$$
x_i = \text{quota di capitale investita nel titolo } i,
\qquad \forall i \in \{1, 2, \dots, n\}.
$$

Usando queste variabili, un modello QP per il problema è il seguente:

$$
\begin{aligned}
\min ~~ \sum_{i=1}^{n} \sum_{j=1}^{n} q_{ij}\, x_i\, x_j & & \\
\text{soggetto a} \quad \sum_{i=1}^{n} \mu_i\, x_i &\ge \bar r, & \\
\sum_{i=1}^{n} x_i &= 1, & \\
x_i &\le u_i, & \forall i \in \{1, 2, \dots, n\}, \\
x_i &\ge \ell_i, & \forall i \in \{1, 2, \dots, n\}.
\end{aligned}
$$

Descrizione della funzione obiettivo e dei vincoli:

- la funzione obiettivo quadratica minimizza la varianza del rendimento del
  portafoglio; contiene le covarianze $q_{ij}$, ed è qui che nasce la
  diversificazione: combinare titoli poco correlati abbassa il rischio complessivo
  sotto quello dei singoli componenti;
- il vincolo lineare di **rendimento** impone che il rendimento atteso del
  portafoglio raggiunga la soglia $\bar r$: è la "manopola" con cui si percorre la
  frontiera efficiente, e il suo moltiplicatore dice quanta varianza costa ogni punto
  di rendimento in più (un vincolo lineare);
- il vincolo lineare di **budget** impone di investire tutto il capitale (un vincolo
  lineare);
- i vincoli lineari di **tetto** $x_i \le u_i$ sono i limiti per titolo, tipici
  vincoli regolamentari o di mandato ($n$ vincoli lineari);
- i vincoli $x_i \ge \ell_i$ definiscono le variabili del modello (con $\ell_i = 0$:
  divieto di vendita allo scoperto).

Formulazioni equivalenti:
$\max\, \sum_{i=1}^{n} \mu_i x_i - \lambda \sum_{i=1}^{n}\sum_{j=1}^{n} q_{ij} x_i x_j$
(media-varianza) e $\max\, \sum_{i=1}^{n} \mu_i x_i$ con varianza $\le \bar\sigma^2$
(massimo rendimento a rischio limitato). Variando $\bar r$ (o $\lambda$, o
$\bar\sigma$) si percorre la stessa frontiera.

Ogni matrice di covarianza è semidefinita positiva, quindi il QP è convesso e
l'ottimo trovato è **globale certificato**.

!!! example "Esempio a mano (2 titoli non correlati)"
    $\sigma_1 = 20\%$, $\sigma_2 = 30\%$: minimizzando
    $0{,}04 x_1^2 + 0{,}09 (1 - x_1)^2$ si ottiene $x_1 = 9/13 = 69{,}2\%$ e
    volatilità di portafoglio $16{,}6\%$ — **meno di entrambi i titoli**.

## Caso di studio

Otto ETF settoriali, $\boldsymbol\mu$ e $\boldsymbol Q$ **stimati** da 60 rendimenti
mensili simulati (`dati/markowitz_rendimenti.csv`). Statistiche annualizzate:

```text
ENE: mu = 19,12%  vol = 18,65%      SAN: mu =  2,80%  vol = 11,93%
FIN: mu =  8,27%  vol = 19,59%      CON: mu = 11,25%  vol = 11,67%
TEC: mu =  1,58%  vol = 29,27%      UTL: mu = 11,99%  vol =  7,53%
IND: mu =  9,97%  vol = 16,60%      MAT: mu = 20,93%  vol = 23,93%
```

```text
Minima varianza globale : rendimento 11,06%, volatilita'  6,03%
Equipesato (1/n)        : rendimento 10,74%, volatilita' 10,13%
Composizione min varianza: ENE 5,2%  IND 1,9%  SAN 11,5%  CON 22,3%  UTL 58,3%
```

![Frontiera efficiente](img/cap06_frontiera.png)

![Composizione lungo la frontiera](img/cap06_composizione.png)

Tre messaggi: (1) il portafoglio di minima varianza (volatilità 6%) è molto meno
rischioso del miglior titolo singolo (UTL, 7,5%) pur rendendo l'11%; (2) l'equipesato
$1/n$ — la strategia "non so nulla" — è nettamente dominato: stessa area di
rendimento ma quasi il doppio della volatilità; (3) il tetto $u_i = 30\%$ taglia la
parte alta della frontiera — il costo dei vincoli di mandato *si vede* come distanza
tra le due curve.

## Sensitività

```text
r_min =  6%: vol 6,03%   (vincolo NON attivo: coincide col min varianza)
r_min =  8%: vol 6,03%   (idem)
r_min = 10%: vol 6,03%   (idem)
r_min = 12%: vol 6,10%   d(varianza)/d(r_min) ~ 0,0221
```

Fino a $\bar r = 11\%$ il vincolo di rendimento è *inattivo*: il portafoglio di
minima varianza rende già l'11,06%, quindi chiedere "almeno l'8%" non costa nulla e
il moltiplicatore è zero. Solo oltre l'11,06% il vincolo morde e ogni punto di
rendimento in più si paga in varianza (moltiplicatore $\approx 0{,}022$ a
$\bar r = 12\%$).

!!! warning "La fragilità delle stime"
    Nei dati simulati il titolo TEC ha $\alpha$ vero dell'11% annuo, ma su 60 mesi il
    rendimento *stimato* è 1,6%: il rumore domina. Le stime dei rendimenti attesi
    sono molto più instabili di quelle delle covarianze, e i portafogli ottimizzati
    inseguono gli errori di stima. Rimedi: vincoli $u_i$, shrinkage delle stime,
    oppure ottimizzare solo il rischio (minima varianza).


## Codice

Lo script completo del capitolo — dati, modello, soluzione, sensitività e figure —
è [`python/lab06_markowitz.py`](https://github.com/fabiofurini/laboratorio-ricerca-operativa/blob/main/python/lab06_markowitz.py)
(riproducibile con `python3 python/lab06_markowitz.py` dalla cartella `python/`).

??? example "Mostra lo script completo — `lab06_markowitz.py`"

    ```python
    """Capitolo 6 — Portafoglio di Markowitz (QP convesso).

    Caso di studio: 8 titoli (ETF settoriali), 60 rendimenti mensili simulati con
    un modello a un fattore di mercato + rumore idiosincratico.

    Contenuto:
      1. Stima di mu e Q dai dati storici
      2. Portafoglio a minima varianza globale e con rendimento minimo
      3. Frontiera efficiente e composizione lungo la frontiera
      4. Effetto dei limiti massimi per titolo (u_i)
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB

    from stile import (ARANCIO, CICLO, GRIGIO, ROSSO, TEAL, intestazione, plt, salva_dat,
                       salva_dati, salva_figura)

    rng = np.random.default_rng(42)

    # ----------------------------------------------------------------------
    # 1. DATI: 60 mesi di rendimenti simulati (modello a un fattore)
    # ----------------------------------------------------------------------
    titoli = ["ENE", "FIN", "TEC", "IND", "SAN", "CON", "UTL", "MAT"]
    n, T = len(titoli), 60
    beta = np.array([1.1, 1.3, 1.5, 1.0, 0.6, 0.8, 0.4, 1.2])       # esposizione al mercato
    alfa_ann = np.array([0.05, 0.06, 0.11, 0.05, 0.045, 0.05, 0.035, 0.06])  # extra-rendimento
    sigma_idio = np.array([0.05, 0.055, 0.07, 0.04, 0.03, 0.035, 0.02, 0.06])  # vol. mensile idio

    mercato = rng.normal(0.004, 0.035, T)                 # fattore di mercato mensile
    R = (alfa_ann[None, :] / 12 + np.outer(mercato, beta)
         + rng.normal(0, sigma_idio, (T, n)))             # matrice T x n dei rendimenti

    rend = pd.DataFrame(R, columns=titoli)
    rend.insert(0, "mese", range(1, T + 1))
    salva_dati(rend, "markowitz_rendimenti")

    mu = R.mean(axis=0) * 12                # rendimento atteso annualizzato
    Q = np.cov(R.T) * 12                    # covarianza annualizzata
    vol = np.sqrt(np.diag(Q))

    intestazione("Statistiche dei titoli (annualizzate)")
    for i, tt in enumerate(titoli):
        print(f"  {tt}: mu = {mu[i]:6.2%}   vol = {vol[i]:6.2%}")


    def portafoglio(r_min=None, u=1.0):
        """QP: minima varianza con eventuale rendimento minimo e limite per titolo."""
        m = gp.Model("markowitz")
        m.Params.OutputFlag = 0
        x = m.addVars(n, ub=u, name="x")
        m.addConstr(x.sum() == 1, name="budget")
        if r_min is not None:
            m.addConstr(gp.quicksum(mu[i] * x[i] for i in range(n)) >= r_min, name="rendimento")
        m.setObjective(gp.quicksum(Q[i, j] * x[i] * x[j]
                                   for i in range(n) for j in range(n)), GRB.MINIMIZE)
        m.optimize()
        if m.Status != GRB.OPTIMAL:
            return None, None, None
        w = np.array([x[i].X for i in range(n)])
        return w, float(mu @ w), float(np.sqrt(w @ Q @ w))


    # ----------------------------------------------------------------------
    # 2. PORTAFOGLI NOTEVOLI
    # ----------------------------------------------------------------------
    intestazione("Portafogli notevoli")
    w_mv, r_mv, v_mv = portafoglio()
    print(f"Minima varianza globale : rendimento {r_mv:6.2%}, volatilità {v_mv:6.2%}")
    w_eq = np.ones(n) / n
    print(f"Equipesato (1/n)        : rendimento {mu @ w_eq:6.2%}, "
          f"volatilità {np.sqrt(w_eq @ Q @ w_eq):6.2%}")
    r_obb = 0.08
    w_8, r_8, v_8 = portafoglio(r_min=r_obb)
    print(f"Rendimento minimo 8%    : rendimento {r_8:6.2%}, volatilità {v_8:6.2%}")
    print("\nComposizione (quote > 1%):")
    for nome, w in [("min varianza", w_mv), ("rend. min 8%", w_8)]:
        quote = ", ".join(f"{titoli[i]} {w[i]:.1%}" for i in range(n) if w[i] > 0.01)
        print(f"  {nome:>14}: {quote}")

    # ----------------------------------------------------------------------
    # 3. FRONTIERA EFFICIENTE (con e senza limite u_i = 30%)
    # ----------------------------------------------------------------------
    intestazione("Frontiera efficiente")
    r_grid = np.linspace(r_mv, mu.max() * 0.999, 30)
    frontiere = {}
    for u, etich in [(1.0, "senza limiti"), (0.30, "u_i = 30%")]:
        punti, composizioni = [], []
        for r in r_grid:
            w, rr, vv = portafoglio(r_min=r, u=u)
            if w is not None:
                punti.append((vv, rr))
                composizioni.append(w)
        frontiere[etich] = (np.array(punti), np.array(composizioni))
        print(f"  frontiera '{etich}': {len(punti)} punti calcolati")

    pf = frontiere["senza limiti"][0]
    salva_dati(pd.DataFrame({"volatilita": pf[:, 0], "rendimento": pf[:, 1]}),
               "markowitz_frontiera")

    # ----------------------------------------------------------------------
    # 4. FIGURE (dati pgfplots + anteprima matplotlib)
    # ----------------------------------------------------------------------
    pf_lim = frontiere["u_i = 30%"][0]
    salva_dat(pd.DataFrame({"vol": pf[:, 0] * 100, "rend": pf[:, 1] * 100}), "cap06_front_libera")
    salva_dat(pd.DataFrame({"vol": pf_lim[:, 0] * 100, "rend": pf_lim[:, 1] * 100}),
              "cap06_front_limiti")
    salva_dat(pd.DataFrame({"titolo": titoli, "vol": vol * 100, "mu": mu * 100}), "cap06_titoli")
    salva_dat(pd.DataFrame({
        "nome": ["minvar", "equipesato"],
        "vol": [v_mv * 100, float(np.sqrt(w_eq @ Q @ w_eq)) * 100],
        "rend": [r_mv * 100, float(mu @ w_eq) * 100],
    }), "cap06_speciali")
    punti_sl, comp_sl = frontiere["senza limiti"]
    salva_dat(pd.DataFrame({"rend": punti_sl[:, 1] * 100,
                            **{titoli[i]: comp_sl[:, i] * 100 for i in range(n)}}),
              "cap06_composizione")

    fig, ax = plt.subplots()
    for (etich, (punti, _)), colore in zip(frontiere.items(), [TEAL, ARANCIO]):
        ax.plot(punti[:, 0] * 100, punti[:, 1] * 100, "-", color=colore, lw=2, label=etich)
    ax.scatter(vol * 100, mu * 100, color=GRIGIO, s=28, zorder=3, label="titoli singoli")
    for i, tt in enumerate(titoli):
        ax.annotate(" " + tt, (vol[i] * 100, mu[i] * 100), fontsize=8, color=GRIGIO)
    ax.scatter([v_mv * 100], [r_mv * 100], marker="*", s=200, color=ROSSO, zorder=4,
               label="minima varianza")
    ax.scatter([np.sqrt(w_eq @ Q @ w_eq) * 100], [mu @ w_eq * 100], marker="D", s=60,
               color="#8E44AD", zorder=4, label="equipesato 1/n")
    ax.set_xlabel("volatilità annua (%)")
    ax.set_ylabel("rendimento atteso annuo (%)")
    ax.set_title("Frontiera efficiente: la diversificazione domina i titoli singoli")
    ax.legend(fontsize=8)
    salva_figura(fig, "cap06_frontiera")

    punti, comp = frontiere["senza limiti"]
    fig, ax = plt.subplots()
    ax.stackplot(punti[:, 1] * 100, (comp.T * 100), labels=titoli, colors=CICLO, alpha=0.9)
    ax.set_xlabel("rendimento richiesto $\\bar r$ (%)")
    ax.set_ylabel("composizione del portafoglio (%)")
    ax.set_title("Composizione ottima lungo la frontiera")
    ax.legend(fontsize=7, ncol=4, loc="lower left")
    ax.set_ylim(0, 100)
    salva_figura(fig, "cap06_composizione")

    # sensitività: prezzo del vincolo di rendimento (moltiplicatore ~ pendenza frontiera)
    intestazione("Sensitività: costo (in varianza) del rendimento richiesto")
    for r in [0.06, 0.08, 0.10, 0.12]:
        w, rr, vv = portafoglio(r_min=r)
        if w is None:
            print(f"  r_min = {r:.0%}: inammissibile (oltre il rendimento massimo)")
            continue
        eps = 0.002
        w2, _, vv2 = portafoglio(r_min=r + eps)
        pend = (vv2**2 - vv**2) / eps if w2 is not None else float("nan")
        print(f"  r_min = {r:5.1%}: vol {vv:6.2%}  |  d(varianza)/d(r_min) ≈ {pend:7.4f}")

    print("\nFatto: capitolo 6.")
    ```

## Esercizi

1. Due titoli con $\rho = 0{,}5$: la diversificazione conviene ancora?
   ($x_1 = 6/7$, vol 19,6%)
2. Frontiere con $u = 1$, $0{,}3$, $0{,}2$: rendimento massimo 20,9% / 16,7% / 14,7%.
3. Rieseguire con seed diverso: quanto cambiano le composizioni?
4. Tracking error minimo con rendimento ≥ 12% (TE = 1,1% annuo).
5. Costi di transazione quadratici dal portafoglio equipesato.
