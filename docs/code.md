# Capacità di servizio e tempi di attesa

**Classe:** NLP convesso (coda M/M/1) · **Script:** `python/lab11_code.py`

Quanta capacità assegnare a un call center, uno sportello, un servizio cloud? Più
capacità costa; poca capacità fa esplodere le attese. Messaggio centrale,
contro-intuitivo per chi ragiona "a efficienza": **l'utilizzazione ottima non è il
100%**.

**Il problema a parole.** *Decidiamo* la capacità $\mu$. *L'obiettivo*: costo di
capacità + valore del tempo dei clienti nel sistema. *Il vincolo*: stabilità
$\mu > \lambda$.

## Modello

Coda **M/M/1** (arrivi di Poisson a tasso $\lambda$, servizio esponenziale, un
servente): tempo medio nel sistema $w(\mu) = 1/(\mu - \lambda)$, clienti medi
$l(\mu) = \lambda/(\mu - \lambda)$.

$$
\min_{\mu > \lambda}\; c\,\mu + h\,\frac{\lambda}{\mu - \lambda}
\qquad\Longrightarrow\qquad
\mu^* = \lambda + \sqrt{h\lambda/c}
$$

"Capacità = domanda + **cuscinetto**": il cuscinetto cresce con il valore del tempo
dei clienti, decresce con il costo della capacità, e scala come $\sqrt\lambda$
(economie di scala → pooling).

!!! example "Esempio a mano"
    $\lambda = 8$/h, $c = 2$, $h = 4$: $\mu^* = 8 + \sqrt{16} = 12$, $\rho = 67\%$,
    $w = 15$ min, costo 32 €/h. "Tagliare gli sprechi" a $\mu = 9$ ($\rho = 89\%$)
    costerebbe 50 €/h.

## Caso di studio

$\lambda = 42$ richieste/ora, $c = 3$ €, $h = 1{,}5$ €.

```text
mu* = 46,583 (analitico = numerico)   costo 153,50 €/h
rho = 90,2%   w = 13,1 minuti
```

![Costo convesso e muro dell'utilizzazione](img/cap11_costo_muro.png)

Tra $\rho = 90\%$ e $\rho = 99\%$ il tempo di attesa **si moltiplica per dieci**:
"saturare le risorse" e "dare un buon servizio" sono in conflitto matematico, non
organizzativo.

## Il prezzo di una promessa di servizio

Con la promessa $w \le w_{\max}$ serve $\mu \ge \lambda + 1/w_{\max}$:

```text
w_max = 12 min: costo 153,60 (quasi gratis)     w_max = 3 min: 189,15
w_max =  6 min: costo 162,30                    w_max = 2 min: 218,10 (+42%)
```

![Costo della promessa](img/cap11_promessa.png)

Quando il vincolo è attivo, $dC/dw_{\max} = -c/w_{\max}^2 + h\lambda$: a 6 minuti
vale $-237$ €/h per ora di promessa — il numero da dare al marketing *prima* che
firmi lo SLA.

**Robustezza:** con $\lambda \in [36, 48]$ l'ottimo nominale ($\mu^* = 46{,}6 < 48$)
**diverge** nel caso peggiore; il dimensionamento robusto ($\mu = 52{,}9$) costa
+13% — un premio assicurativo contro il disastro.


## Codice

Lo script completo del capitolo — dati, modello, soluzione, sensitività e figure —
è [`python/lab11_code.py`](https://github.com/fabiofurini/laboratorio-ricerca-operativa/blob/main/python/lab11_code.py)
(riproducibile con `python3 python/lab11_code.py` dalla cartella `python/`).

??? example "Mostra lo script completo — `lab11_code.py`"

    ```python
    """Capitolo 11 — Capacità di servizio e tempi di attesa (NLP convesso, M/M/1).

    Caso di studio: dimensionare gli operatori di un servizio clienti.
    Arrivi lambda = 42 richieste/ora; ogni "unità di capacità" mu costa c = 3 €/ora;
    un'ora di permanenza nel sistema di un cliente vale h = 1,5 €.

    Contenuto:
      1. Costo totale c·mu + h·lambda/(mu-lambda): soluzione analitica vs numerica
      2. Il muro dell'utilizzazione: rho → 1 fa esplodere l'attesa
      3. Vincolo di service level W <= W_max e suo prezzo ombra
      4. Robustezza: lambda incerto nell'intervallo [36, 48]
    """
    import numpy as np
    import pandas as pd
    from scipy.optimize import minimize_scalar

    from stile import (ARANCIO, GRIGIO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dat,
                       salva_dati, salva_figura)

    lam, c, h = 42.0, 3.0, 1.5

    # ----------------------------------------------------------------------
    # 1. COSTO TOTALE: analitico vs numerico
    # ----------------------------------------------------------------------
    intestazione("Ottimo analitico e numerico")


    def costo(mu):
        return c * mu + h * lam / (mu - lam)


    mu_star = lam + np.sqrt(h * lam / c)               # dall'annullare la derivata
    res = minimize_scalar(costo, bounds=(lam + 1e-3, 4 * lam), method="bounded")
    print(f"Analitico : mu* = lambda + sqrt(h·lambda/c) = {mu_star:.3f}  → costo {costo(mu_star):.3f} €/h")
    print(f"Numerico  : mu* = {res.x:.3f}  → costo {res.fun:.3f} €/h")
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


    def costo_robusto(mu):
        if mu <= lam_hi:
            return np.inf
        return c * mu + max(h * ll / (mu - ll) for ll in (lam_lo, lam_hi))


    res_rob = minimize_scalar(costo_robusto, bounds=(lam_hi + 1e-3, 4 * lam_hi), method="bounded")
    print(f"mu robusto = {res_rob.x:.3f} (vs {mu_star:.3f} nominale)")
    print(f"Costo nel caso peggiore: {res_rob.fun:.3f} €/h")
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
2. Costo d'attesa quadratico $h/(\mu - \lambda)^2$: $\mu^* = \lambda + (2h/c)^{1/3}$.
3. Pooling: due code separate ($\lambda = 21$ ciascuna) vs una unica ($\lambda = 42$)
   a parità di capacità totale.
4. Frontiera (costo, $w$): dove ogni minuto promesso in meno costa più di 10 €/h?
   (Sotto ~4 minuti.)
