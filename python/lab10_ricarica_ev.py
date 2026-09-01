"""Capitolo 10 — Ricarica intelligente di veicoli elettrici (LP / QP convesso).

Caso di studio: deposito aziendale con 6 furgoni elettrici da ricaricare
durante la notte; prezzi orari dell'energia; carico di base dell'edificio.

Contenuto:
  1. LP a costo minimo: la ricarica insegue le ore economiche
  2. Peak shaving: minimizzare il picco di prelievo (minimax)
  3. Profilo regolare (QP) e confronto multiobiettivo costo-picco
  4. Prezzi ombra: capacità di rete e fabbisogno energetico
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from stile import (ARANCIO, GRIGIO, ROSSO, TEAL, intestazione, plt, salva_dat, salva_dati,
                   salva_figura)

# ----------------------------------------------------------------------
# 1. DATI
# ----------------------------------------------------------------------
ore = list(range(24))                      # ora t = [t, t+1)
# prezzo €/kWh: alto di giorno e nel picco serale, basso di notte
prezzo = np.array([0.09, 0.08, 0.07, 0.07, 0.08, 0.10, 0.14, 0.18, 0.20, 0.19,
                   0.17, 0.16, 0.15, 0.15, 0.16, 0.18, 0.21, 0.24, 0.26, 0.24,
                   0.20, 0.15, 0.12, 0.10])
# carico di base dell'edificio (kW)
base = np.array([22, 20, 19, 19, 20, 24, 35, 48, 60, 63, 65, 64,
                 62, 61, 62, 64, 66, 68, 62, 55, 45, 36, 30, 25], dtype=float)

veicoli = [f"V{k}" for k in range(1, 7)]
# (ora arrivo, ora partenza, energia richiesta kWh, potenza max kW)
flotta = {
    "V1": (18, 7, 46, 11), "V2": (19, 6, 38, 11), "V3": (20, 8, 55, 22),
    "V4": (17, 6, 30, 7.4), "V5": (21, 7, 42, 11), "V6": (22, 8, 50, 22),
}
eta = 0.95            # rendimento di carica
C_rete = 120.0        # potenza massima prelevabile dal contatore (kW)

disp = {(v, t): 1 if (flotta[v][0] <= t or t < flotta[v][1]) else 0
        for v in veicoli for t in ore}      # finestre a cavallo della mezzanotte

salva_dati(pd.DataFrame({"ora": ore, "prezzo": prezzo, "carico_base": base}), "ev_prezzi_base")
salva_dati(pd.DataFrame([(v, *flotta[v]) for v in veicoli],
                        columns=["veicolo", "arrivo", "partenza", "energia_kWh", "pmax_kW"]),
           "ev_flotta")


def costruisci():
    m = gp.Model("ricarica_ev")
    m.Params.OutputFlag = 0
    x = m.addVars(veicoli, ore, name="x")       # potenza di carica (kW)
    for v in veicoli:
        for t in ore:
            x[v, t].UB = flotta[v][3] * disp[v, t]     # 0 se non collegato
    v_ene = m.addConstrs((eta * gp.quicksum(x[v, t] for t in ore) >= flotta[v][2]
                          for v in veicoli), name="energia")
    v_rete = m.addConstrs((gp.quicksum(x[v, t] for v in veicoli) + base[t] <= C_rete
                           for t in ore), name="rete")
    return m, x, v_ene, v_rete


def profilo(x):
    return np.array([sum(x[v, t].X for v in veicoli) for t in ore])


# ----------------------------------------------------------------------
# 2. LP COSTO MINIMO
# ----------------------------------------------------------------------
intestazione("LP: costo energetico minimo")
m, x, v_ene, v_rete = costruisci()
m.setObjective(gp.quicksum(prezzo[t] * x[v, t] for v in veicoli for t in ore), GRB.MINIMIZE)
m.optimize()
assert m.Status == GRB.OPTIMAL
prof_costo = profilo(x)
costo_min = m.ObjVal
picco_costo = (prof_costo + base).max()
print(f"Costo di ricarica: {costo_min:.2f} €   picco di prelievo: {picco_costo:.1f} kW "
      f"(limite {C_rete:.0f})")
print("\nPrezzi ombra del fabbisogno (costo marginale di 1 kWh in più per veicolo):")
for v in veicoli:
    print(f"  {v}: {v_ene[v].Pi:.4f} €/kWh")

# ----------------------------------------------------------------------
# 3. PEAK SHAVING (minimax) e PROFILO REGOLARE (QP)
# ----------------------------------------------------------------------
intestazione("Peak shaving: minimizzare il picco di prelievo")
mp, xp, _, _ = costruisci()
z = mp.addVar(name="picco")
mp.addConstrs((gp.quicksum(xp[v, t] for v in veicoli) + base[t] <= z for t in ore),
              name="def_picco")
mp.setObjective(z, GRB.MINIMIZE)
mp.optimize()
prof_picco = profilo(xp)
costo_picco = sum(prezzo[t] * prof_picco[t] for t in ore)
print(f"Picco minimo possibile: {mp.ObjVal:.1f} kW   costo: {costo_picco:.2f} € "
      f"(+{costo_picco - costo_min:.2f} € rispetto al costo minimo)")

intestazione("Compromesso: costo + rho · picco")
compromessi = []
for rho in [0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]:
    mc, xc, _, _ = costruisci()
    zc = mc.addVar(name="picco")
    mc.addConstrs((gp.quicksum(xc[v, t] for v in veicoli) + base[t] <= zc for t in ore))
    mc.setObjective(gp.quicksum(prezzo[t] * xc[v, t] for v in veicoli for t in ore)
                    + rho * zc, GRB.MINIMIZE)
    mc.optimize()
    cc = sum(prezzo[t] * xc[v, t].X for v in veicoli for t in ore)
    compromessi.append((rho, cc, zc.X))
    print(f"  rho = {rho:4.2f}: costo {cc:6.2f} €, picco {zc.X:6.1f} kW")
salva_dati(pd.DataFrame(compromessi, columns=["rho", "costo", "picco"]), "ev_compromessi")

# ----------------------------------------------------------------------
# 4. SENSITIVITÀ: capacità del contatore
# ----------------------------------------------------------------------
intestazione("Sensitività: capacità della connessione alla rete")
# attenzione: nel vincolo "somma x + base[t] <= C" Gurobi sposta la costante base[t]
# nel termine noto; il RHS memorizzato è C - base[t], quindi va aggiornato così:
for CC in [60, 65, 70, 80, 90, 120]:
    ms, xs_, _, vr = costruisci()
    for t in ore:
        vr[t].RHS = CC - base[t]
    ms.setObjective(gp.quicksum(prezzo[t] * xs_[v, t] for v in veicoli for t in ore),
                    GRB.MINIMIZE)
    ms.optimize()
    esito = f"costo {ms.ObjVal:6.2f} €" if ms.Status == GRB.OPTIMAL else "INAMMISSIBILE"
    print(f"  C_rete = {CC:3d} kW: {esito}")

# ----------------------------------------------------------------------
# 5. FIGURE (dati pgfplots + anteprima matplotlib)
# ----------------------------------------------------------------------
salva_dat(pd.DataFrame({"ora": ore, "prezzo_cent": prezzo * 100, "base": base,
                        "totcosto": base + prof_costo, "totpicco": base + prof_picco}),
          "cap10_profili")
salva_dat(pd.DataFrame(compromessi, columns=["rho", "costo", "picco"]), "cap10_frontiera")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.2, 6.4), sharex=True)
ax1.bar(ore, prezzo * 100, color=GRIGIO, alpha=0.6)
ax1.set_ylabel("prezzo (c€/kWh)")
ax1.set_title("Prezzo orario dell'energia")
ax2.plot(ore, base, color=GRIGIO, ls="--", label="carico di base")
ax2.plot(ore, base + prof_costo, color=TEAL, lw=2, drawstyle="steps-mid",
         label="costo minimo")
ax2.plot(ore, base + prof_picco, color=ARANCIO, lw=2, drawstyle="steps-mid",
         label="peak shaving")
ax2.axhline(C_rete, color=ROSSO, ls=":", label=f"limite rete {C_rete:.0f} kW")
ax2.set_xlabel("ora del giorno"); ax2.set_ylabel("prelievo totale (kW)")
ax2.set_title("Profilo di prelievo: inseguire i prezzi crea un picco notturno")
ax2.legend(fontsize=8, ncol=2)
salva_figura(fig, "cap10_profili")

comp = pd.DataFrame(compromessi, columns=["rho", "costo", "picco"])
fig, ax = plt.subplots()
ax.plot(comp["picco"], comp["costo"], "-o", color=TEAL)
for _, r in comp.iterrows():
    ax.annotate(f"  $\\rho$={r['rho']:.2f}", (r["picco"], r["costo"]), fontsize=8)
ax.set_xlabel("picco di prelievo (kW)")
ax.set_ylabel("costo di ricarica (€)")
ax.set_title("Frontiera costo-picco: ridurre il picco costa poco all'inizio")
salva_figura(fig, "cap10_frontiera")

print("\nFatto: capitolo 10.")
