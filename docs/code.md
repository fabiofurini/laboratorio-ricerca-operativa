# Capacità di servizio e tempi di attesa

**Classe:** NLP convesso (coda M/M/1) · **Script:** `python/lab11_code.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab11_code.ipynb)

Quanta capacità assegnare a un call center, uno sportello, un servizio cloud? Più
capacità costa; poca capacità fa esplodere le attese. Messaggio centrale,
contro-intuitivo per chi ragiona "a efficienza": **l'utilizzazione ottima non è il
100%**.

**Il problema a parole.** *Decidiamo* la capacità $\mu$. *L'obiettivo*: costo di
capacità + valore del tempo dei clienti nel sistema. *Il vincolo*: stabilità
$\mu > \lambda$.

## Modello

Usiamo il modello di coda più semplice, la **M/M/1**: arrivi *markoviani* (processo
di Poisson), tempi di servizio *markoviani* (esponenziali) e *un* servente. La novità
è trattare la capacità $\mu$ come una variabile di ottimizzazione.

**Dati (input del modello).**

| Simbolo | Tipo | Significato |
|---|---|---|
| $\lambda$ | $\in \mathbb{Q}_{> 0}$ | tasso medio di arrivo dei clienti (richieste/ora) |
| $c$ | $\in \mathbb{Q}_{> 0}$ | costo di un'unità di capacità (€ per unità di $\mu$ all'ora) |
| $h$ | $\in \mathbb{Q}_{> 0}$ | valore di un'ora di permanenza di un cliente nel sistema (€) |

**Variabile decisionale e grandezze derivate.** Introduciamo una variabile continua:

$$
\mu = \text{capacità del servizio (tasso di servizio, richieste/ora)},
$$

con il requisito di stabilità $\mu > \lambda$. Dalla teoria delle code M/M/1 derivano
il tempo medio nel sistema $w(\mu) = 1/(\mu - \lambda)$ (in letteratura: $W$) e il
numero medio di clienti nel sistema $l(\mu) = \lambda/(\mu - \lambda)$ (legge di
Little; in letteratura: $L$).

Usando questa variabile, il modello per il problema è il seguente:

$$
\begin{aligned}
\min ~~ c\,\mu + h\,\frac{\lambda}{\mu - \lambda} & & \\
\text{soggetto a} \quad \mu &> \lambda. &
\end{aligned}
$$

Descrizione della funzione obiettivo e del vincolo:

- la funzione obiettivo è la somma di due termini: il primo, $c\,\mu$, compra la
  capacità; il secondo, $h \cdot l(\mu)$, monetizza il tempo complessivo che i
  clienti passano nel sistema; è convessa su $(\lambda, +\infty)$;
- il vincolo di **stabilità** definisce la variabile e garantisce che la coda non
  diverga: con $\mu \le \lambda$ la fila cresce senza limite.

Annullando la derivata dell'obiettivo si ottiene la soluzione in forma chiusa:

$$
C'(\mu) = c - \frac{h\,\lambda}{(\mu - \lambda)^2} = 0
\qquad\Longrightarrow\qquad
\tilde\mu = \lambda + \sqrt{h\,\lambda/c}
$$

"Capacità = domanda + **scorta di sicurezza**": il margine $\sqrt{h\lambda/c}$ cresce
con il valore del tempo dei clienti, decresce con il costo della capacità, e scala
come $\sqrt\lambda$ (economie di scala nel cuscinetto → pooling).

!!! example "Esempio a mano"
    $\lambda = 8$/h, $c = 2$ €, $h = 4$ €/h: $\tilde\mu = 8 + \sqrt{4 \cdot 8/2} = 12$
    clienti/ora, $\rho = 8/12 = 66{,}7\%$, $w = 1/(12 - 8) = 15$ min, costo
    $2 \cdot 12 + 4 \cdot 8/4 = 32$ €/h. "Tagliare gli sprechi" a $\mu = 9$
    ($\rho = 89\%$) costerebbe $18 + 32 = 50$ €/h: l'apparente spreco del 33% di
    capacità inutilizzata è ciò che tiene corte le code.

## Caso di studio

$\lambda = 42$ richieste/ora, $c = 3$ €, $h = 1{,}5$ €.

```text
Analitico : mu* = 42 + sqrt(1,5*42/3) = 46,583   costo 153,495 EUR/h
Gurobi    : mu* = 46,582 (bilineare w(mu-lam) = 1, NonConvex=2: coincide)
All'ottimo: rho = 90,2%   w = 13,1 minuti
```

![Costo convesso e muro dell'utilizzazione](img/cap11_costo_muro.png)

Tra $\rho = 90\%$ e $\rho = 99\%$ il tempo di attesa **si moltiplica per dieci**:
"saturare le risorse" e "dare un buon servizio" sono in conflitto matematico, non
organizzativo.

## Il prezzo di una promessa di servizio

Se il marketing promette "tempo medio sotto $w_{\max}$", serve
$\mu \ge \lambda + 1/w_{\max}$: il vincolo diventa attivo quando è più stringente
dell'ottimo economico (13,1 minuti).

```text
w_max = 12 min: mu = 47,00  costo 153,60   (quasi gratis)
w_max =  9 min: mu = 48,67  costo 155,45
w_max =  6 min: mu = 52,00  costo 162,30
w_max =  4 min: mu = 57,00  costo 175,20
w_max =  3 min: mu = 62,00  costo 189,15
w_max =  2 min: mu = 72,00  costo 218,10   (+42% sul costo base)
```

![Costo della promessa](img/cap11_promessa.png)

Il prezzo ombra del vincolo cresce in modo esplosivo: passare da 12 a 9 minuti costa
1,85 €/h, da 3 a 2 minuti costa 28,95 €/h. Quando il vincolo è attivo,
$\mu = \lambda + 1/w_{\max}$ e $C = c\lambda + c/w_{\max} + h\lambda\, w_{\max}$, da
cui $dC/dw_{\max} = -c/w_{\max}^2 + h\lambda$ (con $w_{\max}$ in ore): a
$w_{\max} = 6$ minuti vale $-300 + 63 = -237$ €/h per ora di promessa — il numero da
dare al marketing *prima* che firmi lo SLA (*Service Level Agreement*).

**Robustezza:** se $\lambda$ è incerto in $[36, 48]$, dimensionare sull'ottimo
nominale $\tilde\mu = 46{,}58$ è **instabile**: con $\lambda = 48 > \tilde\mu$ la coda
diverge (costo infinito). Minimizzare il costo del caso peggiore dà
$\mu_{\text{rob}} = 52{,}90$ con costo worst-case 173,39 €/h: si paga un premio
assicurativo di circa il 13% per essere protetti da un disastro.


## Codice

Lo script completo del capitolo — dati, modello, soluzione, sensitività e figure —
è [`python/lab11_code.py`](https://github.com/fabiofurini/laboratorio-ricerca-operativa/blob/main/python/lab11_code.py)
(riproducibile con `python3 python/lab11_code.py` dalla cartella `python/`).

Lo stesso codice è disponibile come notebook — [`notebooks/lab11_code.ipynb`](https://github.com/fabiofurini/laboratorio-ricerca-operativa/blob/main/notebooks/lab11_code.ipynb) — che si apre in Colab dal badge in cima alla pagina e gira nel browser, senza installare niente.

??? example "Mostra lo script completo — `lab11_code.py`"

    ```python
    """Capitolo 11 — Capacità di servizio e tempi di attesa (NLP convesso, M/M/1).

    Caso di studio: dimensionare gli operatori di un servizio clienti.
    Arrivi lambda = 42 richieste/ora; ogni "unità di capacità" mu costa c = 3 €/ora;
    un'ora di permanenza nel sistema di un cliente vale h = 1,5 €.

    Contenuto:
      1. Costo totale c·mu + h·lambda/(mu-lambda): analitica vs Gurobi (globale)
      2. Il muro dell'utilizzazione: rho → 1 fa esplodere l'attesa
      3. Vincolo di service level W <= W_max e suo prezzo ombra
      4. Robustezza: lambda incerto nell'intervallo [36, 48]
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB

    from stile import (ARANCIO, GRIGIO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dat,
                       salva_dati, salva_figura)

    lam, c, h = 42.0, 3.0, 1.5

    # ----------------------------------------------------------------------
    # 1. COSTO TOTALE: analitico vs numerico
    # ----------------------------------------------------------------------
    intestazione("Ottimo analitico e numerico")


    def costo(mu):
        return c * mu + h * lam / (mu - lam)


    def mu_ottimo(lams):
        """min c·mu + max_l h·l/(mu - l) con Gurobi (globale, NonConvex=2).

        Il termine 1/(mu - l) si linearizza con la variabile w_l e il vincolo
        bilineare w_l·(mu - l) = 1; con un solo l è il modello M/M/1 base, con
        più valori di l è la versione robusta (minimizza il caso peggiore)."""
        m = gp.Model("mm1")
        m.Params.OutputFlag = 0
        m.Params.NonConvex = 2
        m.Params.MIPGap = 1e-9
        lam_max = max(lams)
        mu = m.addVar(lb=lam_max + 1e-3, ub=4 * lam_max, name="mu")
        t = m.addVar(name="t")                       # t = costo d'attesa peggiore
        for l in lams:
            w = m.addVar(lb=1e-6, ub=1e5)            # w = 1/(mu - l)
            v = m.addVar(lb=1e-3, ub=4 * lam_max)    # v = mu - l
            m.addConstr(v == mu - l)
            m.addQConstr(w * v == 1)                 # bilineare: risolto globalmente
            m.addConstr(t >= h * l * w)
        m.setObjective(c * mu + t, GRB.MINIMIZE)
        m.optimize()
        assert m.Status == GRB.OPTIMAL
        return mu.X, m.ObjVal


    mu_star = lam + np.sqrt(h * lam / c)               # dall'annullare la derivata
    mu_num, costo_num = mu_ottimo([lam])
    print(f"Analitico : mu* = lambda + sqrt(h·lambda/c) = {mu_star:.3f}  → costo {costo(mu_star):.3f} €/h")
    print(f"Gurobi    : mu* = {mu_num:.3f}  → costo {costo_num:.3f} €/h")
    rho = lam / mu_star
    W = 1 / (mu_star - lam)
    print(f"All'ottimo: utilizzazione rho = {rho:.1%}, tempo medio nel sistema w = {W * 60:.1f} minuti")
    print("Nota: l'ottimo NON è rho ≈ 100%: conviene tenere capacità di sicurezza.")

    # ----------------------------------------------------------------------
    # 2. VINCOLO DI SERVICE LEVEL: W <= W_max
    # ----------------------------------------------------------------------
    intestazione("Service level: W <= W_max")
    righe = []
    for W_max_min in [12, 9, 6, 4, 3, 2]:               # minuti
        W_max = W_max_min / 60
        mu_sl = max(mu_star, lam + 1 / W_max)            # vincolo attivo se più stringente
        prezzo_ombra = 0.0
        if mu_sl > mu_star + 1e-9:                       # vincolo attivo: costo marginale
            # dC/dW_max = derivata del costo ottimo rispetto alla promessa
            eps = 1e-6
            mu_eps = lam + 1 / (W_max + eps)
            prezzo_ombra = (costo(mu_eps) - costo(mu_sl)) / eps
        righe.append((W_max_min, mu_sl, costo(mu_sl), lam / mu_sl, prezzo_ombra))
        print(f"  w_max = {W_max_min:4.1f} min: mu = {mu_sl:7.3f}, costo = {costo(mu_sl):8.3f} €/h, "
              f"rho = {lam / mu_sl:6.1%}, prezzo della promessa = {prezzo_ombra:9.1f} €/h per ora di W")
    sl = pd.DataFrame(righe, columns=["W_max_min", "mu", "costo", "rho", "prezzo_ombra"])
    salva_dati(sl, "code_service_level")

    # ----------------------------------------------------------------------
    # 3. ROBUSTEZZA: lambda incerto in [36, 48]
    # ----------------------------------------------------------------------
    intestazione("Robustezza: domanda incerta lambda in [36, 48]")
    lam_lo, lam_hi = 36.0, 48.0


    mu_rob, costo_rob = mu_ottimo([lam_lo, lam_hi])
    print(f"mu robusto = {mu_rob:.3f} (vs {mu_star:.3f} nominale)")
    print(f"Costo nel caso peggiore: {costo_rob:.3f} €/h")
    print(f"Il piano nominale con lambda = 48 costerebbe: "
          f"{c * mu_star + h * 48 / (mu_star - 48) if mu_star > 48 else float('inf'):.3f} €/h → "
          + ("ok" if mu_star > 48 else "INSTABILE (mu* < lambda massimo!)"))

    # ----------------------------------------------------------------------
    # 4. FIGURE
    # ----------------------------------------------------------------------
    mus = np.linspace(lam + 0.4, lam + 22, 400)
    salva_dat(pd.DataFrame({"mu": mus, "capacita": c * mus, "attesa": h * lam / (mus - lam),
                            "totale": [costo(mm) for mm in mus]}), "cap11_costo")
    rhos_ = np.linspace(0.5, 0.995, 300)
    salva_dat(pd.DataFrame({"rho": rhos_ * 100, "W_min": 1 / (lam / rhos_ - lam) * 60}),
              "cap11_muro")
    salva_dat(sl, "cap11_promessa")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
    ax1.plot(mus, c * mus, ls="--", color=GRIGIO, label="costo capacità $c\\mu$")
    ax1.plot(mus, h * lam / (mus - lam), ls=":", color=ARANCIO,
             label="costo attesa $h\\lambda/(\\mu-\\lambda)$")
    ax1.plot(mus, [costo(mm) for mm in mus], color=TEAL, lw=2, label="costo totale")
    ax1.axvline(mu_star, color=ROSSO, ls="-.", label=f"$\\mu^*$ = {mu_star:.1f}")
    ax1.set_xlabel("capacità $\\mu$ (richieste/ora)")
    ax1.set_ylabel("€/ora")
    ax1.set_ylim(0, 260)
    ax1.set_title("Il costo totale è convesso in $\\mu$")
    ax1.legend(fontsize=8)

    rhos = np.linspace(0.5, 0.995, 300)
    ax2.plot(rhos * 100, 1 / (lam / rhos - lam) * 60, color=TEAL, lw=2)
    ax2.axvline(rho * 100, color=ROSSO, ls="-.", label=f"ottimo $\\rho$ = {rho:.0%}")
    ax2.set_xlabel("utilizzazione $\\rho = \\lambda/\\mu$ (%)")
    ax2.set_ylabel("tempo medio nel sistema W (minuti)")
    ax2.set_title("Il muro dell'utilizzazione: W esplode per $\\rho \\to 1$")
    ax2.legend(fontsize=8)
    salva_figura(fig, "cap11_costo_muro")

    fig, ax = plt.subplots()
    ax.plot(sl["W_max_min"], sl["costo"], "-o", color=TEAL)
    ax.axhline(costo(mu_star), color=GRIGIO, ls="--", label="costo senza promessa")
    ax.set_xlabel("promessa di servizio $W_{max}$ (minuti)")
    ax.set_ylabel("costo ottimo (€/ora)")
    ax.set_title("Quanto costa una promessa di servizio più ambiziosa")
    ax.invert_xaxis()
    ax.legend(fontsize=8)
    salva_figura(fig, "cap11_promessa")

    print("\nFatto: capitolo 11.")
    ```

## Esercizi

1. Ricavare $dC/dw_{\max} = -c/w_{\max}^2 + h\lambda$ e verificarla a 4 e 9 minuti.
2. Costo d'attesa quadratico $h/(\mu - \lambda)^2$: $\tilde\mu = \lambda + (2h/c)^{1/3}$.
3. Pooling: due code separate ($\lambda = 21$ ciascuna) vs una unica ($\lambda = 42$)
   a parità di capacità totale.
4. Frontiera (costo, $w$): dove ogni minuto promesso in meno costa più di 10 €/h?
   (Sotto ~4 minuti.)
