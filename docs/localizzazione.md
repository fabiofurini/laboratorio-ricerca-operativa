# Localizzazione continua di un servizio

**Classe:** NLP convesso · **Script:** `python/lab09_localizzazione.py`

Dove collocare una stazione di ricarica, un micro-hub, un presidio sanitario per
essere "vicini" alla domanda? Dipende da cosa significa vicini: distanza **media**
(efficienza), **massima** (equità) o **quadratica** (baricentro). Tre obiettivi,
tre punti diversi sulla mappa.

**Il problema a parole.** *Decidiamo* le coordinate $(x, y)$. *L'obiettivo* è la
vera scelta manageriale (media / massimo / quadratica). *I vincoli* delimitano
l'area ammissibile.

## Modello

**Dati (input del modello).**

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di punti di domanda (quartieri), indicizzati da $i \in \{1, 2, \dots, n\}$ |
| $(a_i, b_i)$ | $\in \mathbb{Q}^2$ | coordinate del quartiere $i$ (km) |
| $w_i$ | $\in \mathbb{Q}_{\ge 0}$ | peso del quartiere $i$: popolazione, domanda o priorità |
| $(a_0, b_0)$, $r$ | $\in \mathbb{Q}^2$, $\in \mathbb{Q}_{>0}$ | centro e raggio dell'eventuale vincolo geografico (distanza massima da un'infrastruttura) |

**Variabili decisionali.** Introduciamo le seguenti $2$ variabili libere (possono
assumere qualunque valore reale) e, per la versione minimax, una variabile ausiliaria
non negativa:

$$
\begin{cases}
x = \text{coordinata est della nuova struttura (km)}\\[1ex]
y = \text{coordinata nord della nuova struttura (km)}\\[1ex]
z = \text{distanza massima dal quartiere più lontano (solo minimax)}
\end{cases}
$$

Usando queste variabili, i modelli per i tre obiettivi classici sono i seguenti.
Modello di **Weber** (distanza media pesata):

$$
\begin{aligned}
\min ~~ \sum_{i=1}^{n} w_i \sqrt{(x - a_i)^2 + (y - b_i)^2} & & \\
\text{soggetto a} \quad x &\gtreqless 0, & \\
y &\gtreqless 0. &
\end{aligned}
$$

Modello **minimax** (distanza massima):

$$
\begin{aligned}
\min ~~ z & & \\
\text{soggetto a} \quad \sqrt{(x - a_i)^2 + (y - b_i)^2} &\le z, & \forall i \in \{1, 2, \dots, n\}, \\
x &\gtreqless 0, & \\
y &\gtreqless 0, & \\
z &\ge 0. &
\end{aligned}
$$

Descrizione delle funzioni obiettivo e dei vincoli dei due modelli:

- la funzione obiettivo convessa del modello di Weber minimizza la distanza totale
  pesata dai quartieri (efficienza); i vincoli su $x$ e $y$ definiscono le variabili,
  libere;
- la funzione obiettivo del modello minimax minimizza la distanza del quartiere più
  lontano (equità); i vincoli convessi di **copertura** impongono che ogni quartiere
  disti al più $z$ dalla struttura ($n$ vincoli); i vincoli su $x$, $y$ e $z$
  definiscono le variabili;
- terza variante, **quadratica**: minimizzare
  $\sum_{i=1}^{n} w_i \bigl[ (x - a_i)^2 + (y - b_i)^2 \bigr]$, che ha soluzione in
  forma chiusa (il baricentro pesato $\tilde x = \sum_{i=1}^{n} w_i\, a_i \big/ \sum_{i=1}^{n} w_i$,
  e analogamente per $y$).

Vincoli geografici convessi tipici, da aggiungere a qualunque variante: zona
rettangolare $x^{L} \le x \le x^{U}$, $y^{L} \le y \le y^{U}$; distanza massima da
un'infrastruttura $(x - a_0)^2 + (y - b_0)^2 \le r^2$.

Il modello di Weber non ha forma chiusa e la sua funzione obiettivo non è
differenziabile nei punti $(a_i, b_i)$: all'ottimo i "tiri" unitari pesati dei
quartieri si annullano. L'ottimo del minimax è invece il centro del *cerchio minimo*
che racchiude tutti i punti: dipende solo dai quartieri estremi e ignora i pesi — per
questo protegge le periferie.

!!! example "Esempio a mano (1D)"
    Clienti nei km 0, 4, 10 con pesi 1, 1, 3. Weber = **mediana pesata** = 10;
    baricentro = 6,8; minimax = 5. Tre obiettivi ragionevoli, tre risposte diverse:
    la scelta dell'obiettivo *è* la decisione manageriale.

## Caso di studio

12 quartieri (pesi 5–25 mila abitanti), vincolo: entro 2 km dalla cabina elettrica
in (7, 6). Dati in `dati/localizzazione_quartieri.csv`.

Il trucco di modellazione: una variabile $d_k \ge$ distanza euclidea dal quartiere
$k$, imposta con il vincolo conico (convesso) $d_x^2 + d_y^2 \le d_k^2$; Weber
minimizza $\sum_k w_k d_k$, il minimax una $z$ con $d_k \le z$.

```text
Baricentro pesato : (4,897, 5,397)
Weber             : (4,886, 5,310)  dist. media 3,344 km  max 6,314 km
Minimax           : (5,496, 5,029)  dist. media 3,391 km  max 5,680 km
Weber vincolato   : (5,083, 5,429)  costo +0,2% (vincolo attivo, ottimo sul bordo)
```

![Mappa delle localizzazioni](img/cap09_mappa.png)

Weber e baricentro quasi coincidono (i pesi sono distribuiti in modo bilanciato), ma
il minimax si sposta di oltre mezzo km verso sud-est per proteggere i quartieri
periferici; il vincolo della cabina costa pochissimo (+0,2%): scoprire che un vincolo
temuto è quasi gratis è un risultato manageriale importante quanto l'ottimo.

## Sensitività: frontiera efficienza-equità

Metodo ε-constraint: minima distanza media con tetto $D$ sulla massima.

![Frontiera efficienza-equità](img/cap09_frontiera.png)

```text
tetto D = 5,680 km: media 3,391   (soluzione minimax)
tetto D = 5,997 km: media 3,351
tetto D = 6,314 km: media 3,344   (soluzione Weber)
```

La frontiera è quasi piatta: garantire al quartiere più lontano 0,63 km in meno
costa solo 47 metri di distanza media — l'equità qui è "quasi gratis", un argomento
fortissimo in una discussione pubblica. Il caso opposto (frontiera ripida)
segnalerebbe un vero conflitto efficienza-equità.


## Codice

Lo script completo del capitolo — dati, modello, soluzione, sensitività e figure —
è [`python/lab09_localizzazione.py`](https://github.com/fabiofurini/laboratorio-ricerca-operativa/blob/main/python/lab09_localizzazione.py)
(riproducibile con `python3 python/lab09_localizzazione.py` dalla cartella `python/`).

??? example "Mostra lo script completo — `lab09_localizzazione.py`"

    ```python
    """Capitolo 9 — Localizzazione continua di un servizio (NLP convesso).

    Caso di studio: dove collocare una stazione di ricarica rapida in una città
    con 12 quartieri, pesati per popolazione.

    Contenuto:
      1. Baricentro pesato (distanza quadratica): soluzione in forma chiusa
      2. Punto di Weber (distanza euclidea): Gurobi (riformulazione conica)
      3. Minimax (protegge il quartiere più lontano): riformulazione con variabile z
      4. Compromesso alpha·media + (1-alpha)·massimo: curva efficienza-equità
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB

    from stile import (ARANCIO, GRIGIO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dat,
                       salva_dati, salva_figura, salva_tikz)

    rng = np.random.default_rng(7)

    # ----------------------------------------------------------------------
    # 1. DATI: 12 quartieri (coordinate km, peso = popolazione in migliaia)
    # ----------------------------------------------------------------------
    nomi = [f"Q{k}" for k in range(1, 13)]
    coord = np.array([
        [1.0, 8.5], [2.5, 6.0], [4.0, 9.0], [5.5, 7.5], [7.0, 8.0], [9.0, 9.5],
        [1.5, 3.0], [3.0, 1.5], [5.0, 3.5], [6.5, 2.0], [8.0, 4.0], [9.5, 1.0]])
    peso = np.array([12.0, 18.0, 9.0, 22.0, 15.0, 6.0, 14.0, 8.0, 25.0, 10.0, 16.0, 5.0])
    salva_dati(pd.DataFrame({"quartiere": nomi, "x": coord[:, 0], "y": coord[:, 1], "peso": peso}),
               "localizzazione_quartieri")


    def dist(p):
        return np.sqrt(((coord - p) ** 2).sum(axis=1))


    def f_weber(p):
        return float(peso @ dist(p))


    def f_max(p):
        return float(dist(p).max())


    def localizza(pesi=None, tetto=None, cabina=None, raggio=None):
        """Localizzazione con Gurobi (SOCP convesso, ottimo globale certificato).

        Il trucco: una variabile d_k >= distanza euclidea dal quartiere k, imposta
        con il vincolo conico dx_k^2 + dy_k^2 <= d_k^2 (d_k >= 0). Con pesi minimizza
        la distanza media pesata (Weber); senza pesi minimizza la massima (minimax).
        `tetto` impone d_k <= tetto; `cabina`/`raggio` il vincolo geografico."""
        m = gp.Model("localizzazione")
        m.Params.OutputFlag = 0
        px = m.addVar(lb=-GRB.INFINITY, name="px")
        py = m.addVar(lb=-GRB.INFINITY, name="py")
        n = len(coord)
        d = m.addVars(n, name="d")
        for k in range(n):
            dx = m.addVar(lb=-GRB.INFINITY)
            dy = m.addVar(lb=-GRB.INFINITY)
            m.addConstr(dx == px - coord[k, 0])
            m.addConstr(dy == py - coord[k, 1])
            m.addQConstr(dx * dx + dy * dy <= d[k] * d[k])   # cono: d_k >= distanza
        if tetto is not None:
            m.addConstrs((d[k] <= tetto for k in range(n)))
        if cabina is not None:
            m.addQConstr((px - cabina[0]) ** 2 + (py - cabina[1]) ** 2 <= raggio ** 2)
        if pesi is not None:                     # Weber: media pesata
            m.setObjective(gp.quicksum(pesi[k] * d[k] for k in range(n)), GRB.MINIMIZE)
        else:                                    # minimax: distanza massima
            z = m.addVar(name="z")
            m.addConstrs((d[k] <= z for k in range(n)))
            m.setObjective(z, GRB.MINIMIZE)
        m.optimize()
        assert m.Status == GRB.OPTIMAL
        return np.array([px.X, py.X]), m.ObjVal


    # ----------------------------------------------------------------------
    # 2. TRE OBIETTIVI CLASSICI
    # ----------------------------------------------------------------------
    intestazione("Tre localizzazioni ottime")
    baricentro = (peso[:, None] * coord).sum(axis=0) / peso.sum()   # forma chiusa
    print(f"Baricentro pesato (dist. quadratica): ({baricentro[0]:.3f}, {baricentro[1]:.3f}) km")

    weber, costo_weber = localizza(pesi=peso)
    print(f"Punto di Weber (dist. media pesata) : ({weber[0]:.3f}, {weber[1]:.3f}) km, "
          f"costo {costo_weber:,.1f} (migliaia ab · km)")

    minimax, dist_minimax = localizza()
    print(f"Minimax (quartiere più lontano)     : ({minimax[0]:.3f}, {minimax[1]:.3f}) km, "
          f"distanza massima {dist_minimax:.3f} km")

    print(f"\nCon il punto di Weber: distanza media pesata {f_weber(weber) / peso.sum():.3f} km, "
          f"massima {f_max(weber):.3f} km")
    print(f"Con il minimax      : distanza media pesata {f_weber(minimax) / peso.sum():.3f} km, "
          f"massima {f_max(minimax):.3f} km")

    # ----------------------------------------------------------------------
    # 3. FRONTIERA EFFICIENZA-EQUITÀ (metodo del vincolo, epsilon-constraint):
    #    minimizzare la distanza media pesata imponendo dist_max <= D
    # ----------------------------------------------------------------------
    intestazione("Frontiera efficienza-equità (min media con tetto sulla massima)")
    media_pesi = peso.sum()
    D_grid = np.linspace(f_max(minimax) + 1e-4, f_max(weber), 21)
    punti = []
    for D in D_grid:
        pos, _ = localizza(pesi=peso, tetto=D)
        punti.append((D, pos[0], pos[1], f_weber(pos) / media_pesi, f_max(pos)))
    comp = pd.DataFrame(punti, columns=["D_max", "x", "y", "dist_media", "dist_max"])
    salva_dati(comp, "localizzazione_frontiera")
    for _, r in comp.iloc[::5].iterrows():
        print(f"  tetto D = {r['D_max']:5.3f} km: posizione ({r['x']:5.2f}, {r['y']:5.2f}), "
              f"media {r['dist_media']:5.3f} km, max {r['dist_max']:5.3f} km")

    # ----------------------------------------------------------------------
    # 4. VINCOLO GEOGRAFICO: entro 2 km da una cabina elettrica
    # ----------------------------------------------------------------------
    intestazione("Weber con vincolo: entro R = 2 km dalla cabina in (7, 6)")
    cabina, R = np.array([7.0, 6.0]), 2.0
    pos_v, costo_v = localizza(pesi=peso, cabina=cabina, raggio=R)
    print(f"Ottimo vincolato: ({pos_v[0]:.3f}, {pos_v[1]:.3f}), costo {costo_v:,.1f}")
    print(f"Costo del vincolo: +{costo_v - costo_weber:,.1f} rispetto al Weber libero "
          f"({(costo_v / costo_weber - 1) * 100:.1f}%)")
    attivo = np.isclose(((pos_v - cabina) ** 2).sum(), R**2, rtol=1e-3)
    print(f"Il vincolo è {'attivo (ottimo sul bordo del cerchio)' if attivo else 'non attivo'}")

    # ----------------------------------------------------------------------
    # 5. FIGURE (TikZ generato + dati pgfplots + anteprima matplotlib)
    # ----------------------------------------------------------------------
    salva_dat(comp, "cap09_frontiera")

    r = ["% Mappa dei quartieri e localizzazioni ottime (generato da lab09_localizzazione.py)",
         "\\begin{tikzpicture}[scale=0.82, >=stealth]",
         "  \\draw[black!20, very thin] (0,0) grid[step=1] (10.5,10);",
         "  \\draw[->, black!50] (0,0) -- (10.8,0) node[below left, font=\\scriptsize] {km est};",
         "  \\draw[->, black!50] (0,0) -- (0,10.3) node[below left, rotate=90, font=\\scriptsize] {km nord};"]
    for k, nome in enumerate(nomi):
        raggio = 0.11 * np.sqrt(peso[k])
        r.append(f"  \\fill[teal, opacity=0.45] ({coord[k, 0]:.2f},{coord[k, 1]:.2f}) "
                 f"circle ({raggio:.2f});")
        r.append(f"  \\node[font=\\tiny, text=black!55, anchor=west] at "
                 f"({coord[k, 0] + raggio:.2f},{coord[k, 1]:.2f}) {{{nome}}};")
    r.append("  % traiettoria del compromesso efficienza-equità")
    traj = " -- ".join(f"({rr['x']:.3f},{rr['y']:.3f})" for _, rr in comp.iterrows())
    r.append(f"  \\draw[black!45, thick, densely dotted] {traj};")
    r.append(f"  % vincolo geografico: cerchio della cabina")
    r.append(f"  \\draw[viola, dashed, thick] ({cabina[0]},{cabina[1]}) circle ({R});")
    r.append(f"  \\node[rectangle, fill=viola, minimum size=2.2mm, inner sep=0] at "
             f"({cabina[0]},{cabina[1]}) {{}};")
    # etichette con angoli diversi per evitare sovrapposizioni (i punti sono vicini)
    punti_not = [(weber, "rossomattone", 190, "Weber"),
                 (minimax, "arancio", -55, "minimax"),
                 (baricentro, "verde", 120, "baricentro"),
                 (pos_v, "viola", 35, "Weber vincolato")]
    for pt, colore, angolo, etich in punti_not:
        r.append(f"  \\node[star, star points=5, fill={colore}, minimum size=3.2mm, inner sep=0pt,"
                 f" label={{[font=\\scriptsize, text={colore}, label distance=2.5mm]"
                 f"{angolo}:{etich}}}] at ({pt[0]:.3f},{pt[1]:.3f}) {{}};")
    r.append("\\end{tikzpicture}")
    salva_tikz("\n".join(r), "cap09_mappa")

    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    ax.scatter(coord[:, 0], coord[:, 1], s=peso * 28, color=TEAL, alpha=0.55,
               label="quartieri (area = popolazione)")
    for k, nome in enumerate(nomi):
        ax.annotate(f" {nome}", coord[k], fontsize=8, color=GRIGIO)
    ax.scatter(*weber, marker="*", s=300, color=ROSSO, zorder=5, label="Weber (media)")
    ax.scatter(*minimax, marker="P", s=160, color=ARANCIO, zorder=5, label="minimax (equità)")
    ax.scatter(*baricentro, marker="X", s=140, color=VERDE, zorder=5, label="baricentro (quadratica)")
    ax.plot(comp["x"], comp["y"], ".-", color=GRIGIO, lw=1, ms=4, alpha=0.8,
            label="traiettoria del compromesso")
    cerchio = plt.Circle(cabina, R, fill=False, color="#8E44AD", ls="--")
    ax.add_patch(cerchio)
    ax.scatter(*cabina, marker="s", s=70, color="#8E44AD", label="cabina + raggio 2 km")
    ax.scatter(*pos_v, marker="*", s=200, color="#8E44AD", zorder=5)
    ax.set_xlabel("km est"); ax.set_ylabel("km nord")
    ax.set_title("Dove mettere la stazione? Dipende dall'obiettivo")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_aspect("equal")
    salva_figura(fig, "cap09_mappa")

    fig, ax = plt.subplots()
    ax.plot(comp["dist_max"], comp["dist_media"], "-o", color=TEAL, ms=4)
    for idx, etich in [(0, "minimax"), (20, "Weber")]:
        r = comp.iloc[idx]
        ax.annotate(f"  {etich}", (r["dist_max"], r["dist_media"]), fontsize=9)
    ax.set_xlabel("distanza massima (km) — equità")
    ax.set_ylabel("distanza media pesata (km) — efficienza")
    ax.set_title("Frontiera efficienza-equità")
    salva_figura(fig, "cap09_frontiera")

    print("\nFatto: capitolo 9.")
    ```

## Esercizi

1. Ricalcolare a mano il baricentro pesato dai CSV.
2. Peso di Q12 da 5 a 40: Weber migra di 1,23 km; il minimax **non si muove**
   (ignora i pesi).
3. Due strutture con assegnazione al più vicino: perché il problema non è più
   convesso?
4. Distanza Manhattan: mostrare che Weber diventa un LP (mediane pesate per
   coordinata).
5. Moltiplicatore del raggio: con $r = 2 \to 2{,}1$ il costo scende da 535,79 a
   535,22.
