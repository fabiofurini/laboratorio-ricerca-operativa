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


## Codice

Lo script completo del capitolo — dati, modello, soluzione, sensitività e figure —
è [`python/lab07_pricing.py`](https://github.com/fabiofurini/laboratorio-ricerca-operativa/blob/main/python/lab07_pricing.py)
(riproducibile con `python3 python/lab07_pricing.py` dalla cartella `python/`).

??? example "Mostra lo script completo — `lab07_pricing.py`"

    ```python
    """Capitolo 7 — Pricing e revenue management (NLP, in parte non convesso).

    Caso di studio: prezzo del biglietto di un concerto in un teatro da 400 posti.

    Contenuto:
      1. Domanda lineare: soluzione analitica e QP (bilineare) con Gurobi
      2. Valore marginale di un posto in più (per perturbazione)
      3. Domanda a elasticità costante e logistica (scipy, ottimo locale vs studio funzione)
      4. Versione multiprodotto (2 categorie con sostituzione)
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB
    from scipy.optimize import minimize_scalar

    from stile import (ARANCIO, GRIGIO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dat,
                       salva_dati, salva_figura)

    # ----------------------------------------------------------------------
    # 1. DOMANDA LINEARE: D(p) = a - b p
    # ----------------------------------------------------------------------
    a, b, c, K = 1200.0, 5.0, 20.0, 400.0   # domanda, pendenza, costo unitario, capienza

    intestazione("Domanda lineare: analitico vs Gurobi (QP bilineare)")
    p_libero = (a / b + c) / 2                 # ottimo senza vincolo di capacità
    q_libero = a - b * p_libero
    print(f"Ottimo NON vincolato: p* = {p_libero:.2f} €, q* = {q_libero:.0f} biglietti")
    if q_libero > K:
        p_vinc = (a - K) / b
        print(f"La capienza K = {K:.0f} è vincolante → p* = (a-K)/b = {p_vinc:.2f} €, q* = {K:.0f}")

    m = gp.Model("pricing_lineare")
    m.Params.OutputFlag = 0
    m.Params.NonConvex = 2                      # obiettivo bilineare p*q
    p = m.addVar(lb=0, ub=a / b, name="p")
    q = m.addVar(lb=0, name="q")
    m.addConstr(q <= a - b * p, name="domanda")
    v_cap = m.addConstr(q <= K, name="capienza")
    m.setObjective(p * q - c * q, GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    print(f"Gurobi:  p* = {p.X:.2f} €, q* = {q.X:.0f}, profitto = {m.ObjVal:,.2f} €")

    # valore marginale di un posto (perturbazione: non ci sono duali LP in un QP non convesso)
    v_cap.RHS = K + 1
    m.optimize()
    val_posto = m.ObjVal - (p_vinc - c) * K if False else None
    m2_obj = m.ObjVal
    v_cap.RHS = K
    m.optimize()
    print(f"Valore marginale di un posto in più: {m2_obj - m.ObjVal:.2f} € "
          f"(teoria: p - c + K·dp/dK = {p_vinc - c - K / b:.2f} €)")

    # ----------------------------------------------------------------------
    # 2. SENSITIVITÀ: prezzo e profitto al variare della capienza
    # ----------------------------------------------------------------------
    intestazione("Sensitività alla capienza")
    capienze = np.arange(200, 901, 50)
    righe = []
    for KK in capienze:
        q_opt = min(KK, q_libero)
        p_opt = (a - q_opt) / b
        profitto = (p_opt - c) * q_opt
        marg = (p_opt - c - q_opt / b) if q_opt < q_libero else 0.0
        righe.append((KK, p_opt, q_opt, profitto, max(marg, 0)))
        print(f"  K = {KK:3.0f}: p* = {p_opt:6.2f} €, profitto = {profitto:9.2f} €, "
              f"valore posto = {max(marg, 0):5.2f} €")
    sens = pd.DataFrame(righe, columns=["K", "prezzo", "quantita", "profitto", "valore_posto"])
    salva_dati(sens, "pricing_sensitivita_capienza")

    # ----------------------------------------------------------------------
    # 3. ALTRE FUNZIONI DI DOMANDA (scipy)
    # ----------------------------------------------------------------------
    intestazione("Elasticità costante e domanda logistica (scipy)")
    A_el, eps = 6.0e6, 2.2                     # D(p) = A p^-eps
    M_log, alfa, beta_l = 900.0, 6.0, 0.045    # D(p) = M / (1 + exp(alfa + beta*p... ))


    def profitto_el(pp):
        return -(pp - c) * min(A_el * pp ** (-eps), K)


    def profitto_log(pp):
        return -(pp - c) * min(M_log / (1 + np.exp(-alfa + beta_l * pp)), K)


    res_el = minimize_scalar(profitto_el, bounds=(c, 400), method="bounded")
    res_log = minimize_scalar(profitto_log, bounds=(c, 400), method="bounded")
    print(f"Elasticità costante (eps = {eps}): p* = {res_el.x:7.2f} €, profitto = {-res_el.fun:9.2f} €")
    print(f"  teoria senza capacità: p* = c·eps/(eps-1) = {c * eps / (eps - 1):.2f} €")
    print(f"Logistica: p* = {res_log.x:7.2f} €, profitto = {-res_log.fun:9.2f} €")

    # ----------------------------------------------------------------------
    # 4. MULTIPRODOTTO: 2 categorie con sostituzione (QP non convesso)
    # ----------------------------------------------------------------------
    intestazione("Due categorie (platea/galleria) con sostituzione")
    # D1 = a1 - b11 p1 + b12 p2 ; D2 = a2 + b21 p1 - b22 p2
    a1, a2 = 500.0, 900.0
    b11, b12, b21, b22 = 2.0, 0.6, 0.8, 4.0
    c1, c2, K1, K2 = 30.0, 15.0, 150.0, 300.0

    mm = gp.Model("pricing_multi")
    mm.Params.OutputFlag = 0
    mm.Params.NonConvex = 2
    p1 = mm.addVar(lb=0, ub=300, name="p1")
    p2 = mm.addVar(lb=0, ub=300, name="p2")
    q1 = mm.addVar(lb=0, name="q1")
    q2 = mm.addVar(lb=0, name="q2")
    mm.addConstr(q1 <= a1 - b11 * p1 + b12 * p2, name="dom1")
    mm.addConstr(q2 <= a2 + b21 * p1 - b22 * p2, name="dom2")
    mm.addConstr(q1 <= K1, name="cap1")
    mm.addConstr(q2 <= K2, name="cap2")
    mm.setObjective((p1 - c1) * q1 + (p2 - c2) * q2, GRB.MAXIMIZE)
    mm.optimize()
    assert mm.Status == GRB.OPTIMAL
    print(f"platea   : p1* = {p1.X:6.2f} €, q1* = {q1.X:5.1f} / {K1:.0f}")
    print(f"galleria : p2* = {p2.X:6.2f} €, q2* = {q2.X:5.1f} / {K2:.0f}")
    print(f"profitto totale: {mm.ObjVal:,.2f} €")

    # ----------------------------------------------------------------------
    # 5. FIGURE
    # ----------------------------------------------------------------------
    pp = np.linspace(20, 240, 400)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
    prof_nc = (pp - c) * (a - b * pp)
    prof_c = (pp - c) * np.minimum(a - b * pp, K)
    salva_dat(pd.DataFrame({"p": pp, "senza": prof_nc, "con": prof_c}), "cap07_profitto")
    salva_dat(sens, "cap07_capienza")
    salva_dat(pd.DataFrame({
        "p": pp,
        "lineare": np.maximum(a - b * pp, 0),
        "elast": np.minimum(A_el * pp ** (-eps), 1400),
        "logistica": M_log / (1 + np.exp(-alfa + beta_l * pp)),
    }), "cap07_domande")
    ax1.plot(pp, prof_nc, color=GRIGIO, ls="--", label="senza vincolo di capienza")
    ax1.plot(pp, prof_c, color=TEAL, lw=2, label=f"con capienza K = {K:.0f}")
    ax1.axvline(p_vinc, color=ROSSO, ls=":", label=f"p* = {p_vinc:.0f} €")
    ax1.set_xlabel("prezzo (€)"); ax1.set_ylabel("profitto (€)")
    ax1.set_title("Domanda lineare: profitto concavo")
    ax1.legend(fontsize=8)
    ax2.plot(sens["K"], sens["profitto"], "-o", color=TEAL)
    ax2.axvline(q_libero, color=GRIGIO, ls="--")
    ax2.annotate(" oltre q* la capienza\n non vale più nulla", (q_libero, sens["profitto"].min()),
                 fontsize=8, color=GRIGIO)
    ax2.set_xlabel("capienza K (posti)"); ax2.set_ylabel("profitto ottimo (€)")
    ax2.set_title("Curva valore della capienza")
    salva_figura(fig, "cap07_profitto")

    fig, ax = plt.subplots()
    D_lin = np.maximum(a - b * pp, 0)
    D_el = A_el * pp ** (-eps)
    D_log = M_log / (1 + np.exp(-alfa + beta_l * pp))
    ax.plot(pp, D_lin, label="lineare $a-bp$", color=TEAL)
    ax.plot(pp, np.minimum(D_el, 1400), label="elasticità costante $Ap^{-\\varepsilon}$", color=ARANCIO)
    ax.plot(pp, D_log, label="logistica $M/(1+e^{\\alpha+\\beta p})$", color=VERDE)
    ax.axhline(K, color=GRIGIO, ls=":", label=f"capienza K = {K:.0f}")
    ax.set_xlabel("prezzo (€)"); ax.set_ylabel("domanda attesa (biglietti)")
    ax.set_ylim(0, 1400)
    ax.set_title("Tre funzioni di domanda a confronto")
    ax.legend(fontsize=8)
    salva_figura(fig, "cap07_domande")

    print("\nFatto: capitolo 7.")
    ```

## Esercizi

1. Verificare il valore del posto per $k = 300$ (100 €) con Gurobi e con la formula.
2. Costo marginale $c = 60$: $p^*$ resta 160 (capacità ancora attiva), profitto
   40.000 €, valore posto 20 €.
3. Penalità reputazionale $-2(p - 120)^2$: il problema resta concavo? Cambia l'ottimo?
4. $p^*(\varepsilon)$ per $\varepsilon \in [1{,}3;\, 3]$ con $k = 400$.
5. +50 posti di platea (+3.287 €) o di galleria (+3.838 €): quale ampliamento
   conviene?
