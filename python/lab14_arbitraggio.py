"""Capitolo 14 — Arbitraggio e prezzatura senza arbitraggio (LP).

Caso di studio: un mercato a uno stadio con 3 stati del mondo, un titolo privo
di rischio (rendimento lordo R = 1,04) e 2 titoli rischiosi.

Contenuto:
  1. Rilevare un arbitraggio (LP normalizzato): prezzi (6, 20) -> guadagno 1 oggi
  2. Prezzi coerenti (13, 18.6923): ottimo 0 e probabilita' neutrali al rischio
     dai duali dei vincoli di stato
  3. Intervallo di prezzo senza arbitraggio per il titolo 2 (due LP + griglia)
  4. Prezzatura di una call: mercato completo (prezzo unico) vs incompleto (range)
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from stile import ARANCIO, GRIGIO, ROSSO, TEAL, intestazione, plt, salva_dat, salva_dati, salva_figura

# ----------------------------------------------------------------------
# 1. DATI: payoff s1[i][j] del titolo i nello stato j; titolo 0 privo di rischio
# ----------------------------------------------------------------------
r = 0.04
R = 1 + r                                     # rendimento lordo del titolo 0
s1 = np.array([[R, R, R],                     # titolo 0
               [10.0, 15.0, 13.0],            # titolo 1
               [30.0, 15.0, 25.0]])           # titolo 2
n1, n_stati = s1.shape                        # 3 titoli (0,1,2), 3 stati

salva_dati(pd.DataFrame(s1, columns=[f"stato_{j+1}" for j in range(n_stati)],
                        index=["titolo_0", "titolo_1", "titolo_2"]).reset_index(names="titolo"),
           "arbitraggio_payoff")


def lp_arbitraggio(s0, normalizza=True):
    """min sum s0_i x_i  soggetto a  payoff >= 0 in ogni stato (x libere).

    Con `normalizza` aggiunge  sum s0_i x_i >= -1  (incasso oggi al piu' 1):
    senza, in presenza di arbitraggio di tipo A il modello e' illimitato."""
    m = gp.Model("arbitraggio")
    m.Params.OutputFlag = 0
    m.Params.DualReductions = 0               # distingue UNBOUNDED da INFEASIBLE
    x = m.addVars(n1, lb=-GRB.INFINITY, name="x")
    v_stato = m.addConstrs(
        (gp.quicksum(s1[i, j] * x[i] for i in range(n1)) >= 0
         for j in range(n_stati)), name="stato")
    if normalizza:
        m.addConstr(gp.quicksum(s0[i] * x[i] for i in range(n1)) >= -1,
                    name="normalizzazione")
    m.setObjective(gp.quicksum(s0[i] * x[i] for i in range(n1)), GRB.MINIMIZE)
    m.optimize()
    return m, x, v_stato


# ----------------------------------------------------------------------
# 2. RILEVARE UN ARBITRAGGIO: prezzi (1, 6, 20)
# ----------------------------------------------------------------------
intestazione("Prezzi (6, 20): c'e' arbitraggio?")
s0_arb = np.array([1.0, 6.0, 20.0])
m_nb, _, _ = lp_arbitraggio(s0_arb, normalizza=False)
print(f"LP senza normalizzazione: status {m_nb.Status} "
      f"({'UNBOUNDED: arbitraggio di tipo A' if m_nb.Status == GRB.UNBOUNDED else 'ottimo'})")
m_a, x_a, _ = lp_arbitraggio(s0_arb)
print(f"LP normalizzato: valore ottimo {m_a.ObjVal:.4f} "
      f"(= incasso oggi di 1 senza alcun rischio)")
print("Strategia:", {f"x{i}": round(x_a[i].X, 4) for i in range(n1)})
payoff = s1.T @ np.array([x_a[i].X for i in range(n1)])
print("Payoff nei tre stati:", np.round(payoff, 4), "(tutti >= 0)")
# la strategia "a mano" del capitolo: (-27, 1, 1)
x_libro = np.array([-27.0, 1.0, 1.0])
print(f"Strategia (-27, 1, 1): costo {s0_arb @ x_libro:.0f}, "
      f"payoff {np.round(s1.T @ x_libro, 2)} (equivalente, in scala diversa)")

# ----------------------------------------------------------------------
# 3. PREZZI COERENTI: ottimo 0 e probabilita' neutrali al rischio
# ----------------------------------------------------------------------
intestazione("Prezzi (13, 18.6923): niente arbitraggio e prezzatura")
s0_ok = np.array([1.0, 13.0, 18.692308])
m_b, x_b, v_stato = lp_arbitraggio(s0_ok, normalizza=False)
print(f"Valore ottimo: {m_b.ObjVal:.4f}  (strategia nulla: nessun arbitraggio)")
p = np.array([v_stato[j].Pi for j in range(n_stati)])
q = R * p
print(f"Duali dei vincoli di stato p* = {np.round(p, 4)}")
print(f"Probabilita' neutrali al rischio q = R p* = {np.round(q, 4)} "
      f"(somma = {q.sum():.4f})")
print("Verifica prezzatura: s0_i = sum_j p_j s1_ij =",
      np.round(s1 @ p, 4))

# ----------------------------------------------------------------------
# 4. INTERVALLO DI PREZZO SENZA ARBITRAGGIO PER IL TITOLO 2
# ----------------------------------------------------------------------
intestazione("Intervallo di prezzo senza arbitraggio per il titolo 2")


def bound_prezzo(payoff_nuovo, quotati, senso):
    """min/max di sum_j p_j payoff_j sulle misure p >= 0 coerenti coi quotati."""
    d = gp.Model("prezzatura")
    d.Params.OutputFlag = 0
    pp = d.addVars(n_stati, name="p")
    for i, prezzo in quotati:
        d.addConstr(gp.quicksum(s1[i, j] * pp[j] for j in range(n_stati)) == prezzo)
    d.setObjective(gp.quicksum(payoff_nuovo[j] * pp[j] for j in range(n_stati)), senso)
    d.optimize()
    assert d.Status == GRB.OPTIMAL
    return d.ObjVal


quotati_01 = [(0, 1.0), (1, 13.0)]
lo = bound_prezzo(s1[2], quotati_01, GRB.MINIMIZE)
hi = bound_prezzo(s1[2], quotati_01, GRB.MAXIMIZE)
print(f"Con titolo 0 e titolo 1 quotati (1 e 13): prezzo del titolo 2 "
      f"senza arbitraggio in [{lo:.4f}, {hi:.4f}]")

griglia = np.linspace(15, 25, 201)
valori = []
for prezzo2 in griglia:
    mg, _, _ = lp_arbitraggio(np.array([1.0, 13.0, prezzo2]))
    valori.append(mg.ObjVal)
curva = pd.DataFrame({"prezzo_titolo2": griglia, "valore_lp": valori})
salva_dati(curva, "arbitraggio_curva_prezzo")
salva_dat(curva, "cap14_arbitraggio_curva")
print(f"Griglia {griglia[0]:.0f}..{griglia[-1]:.0f}: valore LP = 0 solo dentro "
      f"l'intervallo, negativo fuori (arbitraggio)")

# ----------------------------------------------------------------------
# 5. PREZZATURA DI UNA CALL SUL TITOLO 1 (STRIKE 12)
# ----------------------------------------------------------------------
intestazione("Prezzatura di una call sul titolo 1, strike 12")
call = np.maximum(s1[1] - 12.0, 0.0)
print("Payoff della call nei tre stati:", call)
quotati_012 = [(0, 1.0), (1, 13.0), (2, 18.692308)]
lo_c = bound_prezzo(call, quotati_012, GRB.MINIMIZE)
hi_c = bound_prezzo(call, quotati_012, GRB.MAXIMIZE)
print(f"Mercato completo (titoli 0, 1, 2 quotati): prezzo unico "
      f"[{lo_c:.4f}, {hi_c:.4f}]")
lo_i = bound_prezzo(call, quotati_01, GRB.MINIMIZE)
hi_i = bound_prezzo(call, quotati_01, GRB.MAXIMIZE)
print(f"Mercato incompleto (solo titoli 0 e 1):    intervallo    "
      f"[{lo_i:.4f}, {hi_i:.4f}]")

# ----------------------------------------------------------------------
# 6. FIGURA: guadagno da arbitraggio al variare del prezzo del titolo 2
# ----------------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(curva["prezzo_titolo2"], curva["valore_lp"], color=TEAL, lw=2)
ax.axvspan(lo, hi, color=TEAL, alpha=0.10)
ax.axvline(lo, color=GRIGIO, ls=":", lw=1)
ax.axvline(hi, color=GRIGIO, ls=":", lw=1)
ax.axhline(0, color=GRIGIO, lw=0.8)
ax.annotate(f"nessun arbitraggio\n[{lo:.2f}, {hi:.2f}]",
            ((lo + hi) / 2, -0.25), ha="center", color=GRIGIO)
ax.plot([6], [0], alpha=0)  # noop
ax.set_xlabel("prezzo del titolo 2")
ax.set_ylabel("valore ottimo dell'LP normalizzato")
ax.set_title("Fuori dall'intervallo di prezzo coerente compare l'arbitraggio")
salva_figura(fig, "cap14_arbitraggio_curva")

print("\nFatto: capitolo 14 (arbitraggio).")
