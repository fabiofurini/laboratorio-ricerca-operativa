"""Capitolo 12 — Data Envelopment Analysis (LP).

Caso di studio: 12 filiali di una banca (filiali 1, 2, ..., 12) confrontate su
2 input (personale in FTE, costi operativi in migliaia di €) e 2 output
(prestiti e depositi in milioni di €). Dati sintetici realistici generati con
seme fisso.

Contenuto:
  1. Dati delle filiali (generatore con seme fisso)
  2. Esempio a mano: 5 unità, un input e un output
  3. CCR orientato all'input: forma dei moltiplicatori (primale)
  4. CCR: forma di inviluppo (duale), theta = efficienza, peer e lambda
  5. BCC (rendimenti di scala variabili) ed efficienza di scala
  6. Scarti, efficienza debole e forte, target degli input
  7. Sensitività: prezzi ombra verificati per perturbazione e stabilità
  8. Figure (dati per pgfplots + anteprima matplotlib)
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from stile import (ARANCIO, BLU, GRIGIO, ROSSO, TEAL, intestazione, plt, salva_dat,
                   salva_dati, salva_figura)

TOL = 1e-6

# ----------------------------------------------------------------------
# 1. DATI DELLE FILIALI
# ----------------------------------------------------------------------
# Generatore: personale tra 8 e 30 FTE; costi proporzionali al personale con
# una quota fissa; output da una funzione di produzione a rendimenti di scala
# decrescenti, moltiplicata per un'inefficienza casuale exp(-|N(0, 0,25)|) e
# ripartita fra prestiti e depositi.
rng = np.random.default_rng(42)
n = 12                                                    # filiali
personale = rng.integers(8, 31, n).astype(float)          # FTE
costi = np.round(personale * rng.uniform(38, 52, n) + rng.uniform(80, 260, n), -1)  # k€
efficienza_vera = np.exp(-np.abs(rng.normal(0, 0.25, n)))
volume = 9.0 * personale ** 0.55 * (costi / 100) ** 0.30 * efficienza_vera
quota = rng.uniform(0.38, 0.62, n)
prestiti = np.round(volume * quota, 1)                    # M€
depositi = np.round(volume * (1 - quota) * 1.3, 1)        # M€

filiali = list(range(1, n + 1))
X = np.vstack([personale, costi])                         # input:  m x n
Y = np.vstack([prestiti, depositi])                       # output: p x n
nomi_in = ["personale", "costi"]
nomi_out = ["prestiti", "depositi"]

dati = pd.DataFrame({"filiale": filiali, "personale": personale.astype(int),
                     "costi_operativi": costi.astype(int),
                     "prestiti": prestiti, "depositi": depositi})
salva_dati(dati, "dea_filiali")
intestazione("Dati delle filiali")
print(dati.to_string(index=False))


def moltiplicatori(X, Y, o):
    """CCR orientato all'input, forma dei moltiplicatori (LP di Charnes-Cooper)."""
    m_, n_ = X.shape
    p_ = Y.shape[0]
    md = gp.Model("dea_moltiplicatori")
    md.Params.OutputFlag = 0
    md.Params.FeasibilityTol = 1e-9
    md.Params.OptimalityTol = 1e-9
    u = md.addVars(p_, name="u")                            # pesi degli output
    v = md.addVars(m_, name="v")                            # pesi degli input
    norm = md.addConstr(gp.quicksum(v[i] * X[i, o] for i in range(m_)) == 1,
                        name="normalizzazione")
    rapp = md.addConstrs(
        (gp.quicksum(u[r] * Y[r, j] for r in range(p_))
         - gp.quicksum(v[i] * X[i, j] for i in range(m_)) <= 0 for j in range(n_)),
        name="rapporto")
    md.setObjective(gp.quicksum(u[r] * Y[r, o] for r in range(p_)), GRB.MAXIMIZE)
    md.optimize()
    assert md.Status == GRB.OPTIMAL
    return (md.ObjVal, np.array([u[r].X for r in range(p_)]),
            np.array([v[i].X for i in range(m_)]), norm.Pi,
            np.array([rapp[j].Pi for j in range(n_)]))


def inviluppo(X, Y, o, vrs=False, rhs_out=None):
    """Forma di inviluppo orientata all'input: CCR (vrs=False) o BCC (vrs=True).

    rhs_out sostituisce, se dato, il termine noto dei vincoli sugli output."""
    m_, n_ = X.shape
    p_ = Y.shape[0]
    md = gp.Model("dea_inviluppo")
    md.Params.OutputFlag = 0
    md.Params.FeasibilityTol = 1e-9
    md.Params.OptimalityTol = 1e-9
    theta = md.addVar(lb=-GRB.INFINITY, name="theta")
    lam = md.addVars(n_, name="lambda")
    c_in = md.addConstrs(
        (theta * X[i, o] - gp.quicksum(lam[j] * X[i, j] for j in range(n_)) >= 0
         for i in range(m_)), name="input")
    b = Y[:, o] if rhs_out is None else rhs_out
    c_out = md.addConstrs(
        (gp.quicksum(lam[j] * Y[r, j] for j in range(n_)) >= b[r] for r in range(p_)),
        name="output")
    if vrs:
        md.addConstr(lam.sum() == 1, name="convessita")
    md.setObjective(theta, GRB.MINIMIZE)
    md.optimize()
    assert md.Status == GRB.OPTIMAL
    return md, theta, lam, c_in, c_out


def scarti(X, Y, o, theta, vrs=False):
    """Seconda fase: con theta fissato massimizza la somma degli scarti."""
    m_, n_ = X.shape
    p_ = Y.shape[0]
    md = gp.Model("dea_scarti")
    md.Params.OutputFlag = 0
    md.Params.FeasibilityTol = 1e-9
    md.Params.OptimalityTol = 1e-9
    lam = md.addVars(n_, name="lambda")
    s_in = md.addVars(m_, name="s_meno")
    s_out = md.addVars(p_, name="s_piu")
    md.addConstrs((gp.quicksum(lam[j] * X[i, j] for j in range(n_)) + s_in[i]
                   == theta * X[i, o] for i in range(m_)), name="input")
    md.addConstrs((gp.quicksum(lam[j] * Y[r, j] for j in range(n_)) - s_out[r]
                   == Y[r, o] for r in range(p_)), name="output")
    if vrs:
        md.addConstr(lam.sum() == 1, name="convessita")
    md.setObjective(s_in.sum() + s_out.sum(), GRB.MAXIMIZE)
    md.optimize()
    assert md.Status == GRB.OPTIMAL
    pulisci = lambda a: np.where(np.abs(a) < TOL, 0.0, a)
    return (pulisci(np.array([lam[j].X for j in range(n_)])),
            pulisci(np.array([s_in[i].X for i in range(m_)])),
            pulisci(np.array([s_out[r].X for r in range(p_)])))


def testo_peer(lam):
    return " ".join(f"{j + 1}:{l:.3f}" for j, l in enumerate(lam) if l > TOL)


# ----------------------------------------------------------------------
# 2. ESEMPIO A MANO: 5 unità, un input e un output
# ----------------------------------------------------------------------
intestazione("Esempio a mano: 5 unità, un input e un output")
Xe = np.array([[2.0, 4.0, 6.0, 5.0, 2.0]])
Ye = np.array([[2.0, 6.0, 7.0, 3.0, 1.0]])
for o in range(Xe.shape[1]):
    h, u, v, pi_norm, pi_rapp = moltiplicatori(Xe, Ye, o)
    md, th, lam, _, _ = inviluppo(Xe, Ye, o)
    mb, thb, _, _, _ = inviluppo(Xe, Ye, o, vrs=True)
    lam_b, sm_b, sp_b = scarti(Xe, Ye, o, thb.X, vrs=True)
    lam_c, _, _ = scarti(Xe, Ye, o, th.X)
    print(f"unità {o + 1}: x = {Xe[0, o]:.0f}, y = {Ye[0, o]:.0f}, y/x = {Ye[0, o] / Xe[0, o]:.4f} | "
          f"CCR h = {h:.4f} (u = {u[0]:.4f}, v = {v[0]:.4f}), theta = {th.X:.4f}, "
          f"lambda = {testo_peer(lam_c)} | "
          f"BCC theta = {thb.X:.4f}, lambda = {testo_peer(lam_b)}, "
          f"scarto output = {sp_b[0]:.4f}")

# ----------------------------------------------------------------------
# 3. CCR: FORMA DEI MOLTIPLICATORI (primale)
# ----------------------------------------------------------------------
intestazione("CCR orientato all'input: forma dei moltiplicatori")
ris = {}
for o in range(n):
    h, u, v, pi_norm, pi_rapp = moltiplicatori(X, Y, o)
    ris[o] = {"h": h, "u": u, "v": v, "pi_norm": pi_norm, "pi_rapp": pi_rapp}
    print(f"filiale {o + 1:2d}: h = {h:.4f} | u = ({u[0]:.5f}, {u[1]:.5f}) "
          f"v = ({v[0]:.5f}, {v[1]:.6f}) | Pi normalizzazione = {pi_norm:.4f}")

# ----------------------------------------------------------------------
# 4. CCR: FORMA DI INVILUPPO (duale), peer e lambda
# ----------------------------------------------------------------------
intestazione("CCR: forma di inviluppo (duale) e confronto con i moltiplicatori")
for o in range(n):
    md, th, lam, c_in, c_out = inviluppo(X, Y, o)
    ris[o]["ccr"] = th.X
    # dualità forte: theta = h; i Pi della forma di inviluppo sono i pesi u e v
    assert abs(th.X - ris[o]["h"]) < 1e-7
    assert abs(ris[o]["pi_norm"] - th.X) < 1e-7
    pi_in = np.array([c_in[i].Pi for i in range(2)])
    pi_out = np.array([c_out[r].Pi for r in range(2)])
    print(f"filiale {o + 1:2d}: theta = {th.X:.4f} = h = {ris[o]['h']:.4f} | "
          f"Pi output = ({pi_out[0]:.5f}, {pi_out[1]:.5f}) "
          f"Pi input = ({pi_in[0]:.5f}, {pi_in[1]:.6f})")
print("Verifica: theta (inviluppo) = h (moltiplicatori) e Pi della normalizzazione = theta "
      "per tutte le 12 filiali.")

# ----------------------------------------------------------------------
# 5. BCC (rendimenti di scala variabili) ed efficienza di scala
# ----------------------------------------------------------------------
intestazione("Efficienze CCR, BCC e di scala")
print("filiale    CCR     BCC   scala  somma lambda (CCR)   rendimenti")
righe_eff = []
for o in range(n):
    mb, thb, _, _, _ = inviluppo(X, Y, o, vrs=True)
    lam, s_in, s_out = scarti(X, Y, o, ris[o]["ccr"])
    ris[o].update({"bcc": thb.X, "lam": lam, "s_in": s_in, "s_out": s_out})
    scala = ris[o]["ccr"] / thb.X
    somma = lam.sum()
    if abs(ris[o]["ccr"] - 1) < TOL:
        rts = "costanti"
    else:
        rts = "crescenti" if somma < 1 - TOL else ("decrescenti" if somma > 1 + TOL else "costanti")
    righe_eff.append((o + 1, ris[o]["ccr"], thb.X, scala, somma))
    print(f"{o + 1:7d}  {ris[o]['ccr']:.4f}  {thb.X:.4f}  {scala:.4f}  {somma:18.3f}   {rts}")
eff = pd.DataFrame(righe_eff, columns=["filiale", "ccr", "bcc", "scala", "somma_lambda"])
salva_dati(eff.round(6), "dea_efficienze")
print(f"Filiali CCR-efficienti: {[o + 1 for o in range(n) if abs(ris[o]['ccr'] - 1) < TOL]}")
print(f"Filiali BCC-efficienti: {[o + 1 for o in range(n) if abs(ris[o]['bcc'] - 1) < TOL]}")
print(f"Efficienza CCR media: {eff['ccr'].mean():.4f}; BCC media: {eff['bcc'].mean():.4f}")

# ----------------------------------------------------------------------
# 6. SCARTI, EFFICIENZA DEBOLE E FORTE, TARGET
# ----------------------------------------------------------------------
intestazione("Scarti e target degli input (CCR, seconda fase)")
righe_t = []
for o in range(n):
    r = ris[o]
    deb = abs(r["ccr"] - 1) < TOL and (r["s_in"].sum() + r["s_out"].sum()) > TOL
    if deb:
        print(f"filiale {o + 1}: debolmente efficiente (theta = 1 con scarti positivi)")
    if abs(r["ccr"] - 1) < TOL:
        continue
    t_in = r["ccr"] * X[:, o] - r["s_in"]
    t_out = Y[:, o] + r["s_out"]
    righe_t.append((o + 1, r["ccr"], testo_peer(r["lam"]), *t_in, *t_out, *r["s_in"], *r["s_out"]))
    print(f"filiale {o + 1:2d}: theta = {r['ccr']:.4f} | peer {testo_peer(r['lam'])} | "
          f"scarti input ({r['s_in'][0]:.2f}, {r['s_in'][1]:.2f}) output ({r['s_out'][0]:.2f}, {r['s_out'][1]:.2f}) | "
          f"target personale {t_in[0]:.2f} (da {X[0, o]:.0f}), costi {t_in[1]:.1f} (da {X[1, o]:.0f})")
deboli = [o + 1 for o in range(n) if abs(ris[o]["ccr"] - 1) < TOL
          and ris[o]["s_in"].sum() + ris[o]["s_out"].sum() > TOL]
print(f"Filiali efficienti con scarti positivi (debolmente efficienti): {deboli if deboli else 'nessuna'}")
target = pd.DataFrame(righe_t, columns=[
    "filiale", "theta", "peer", "personale_target", "costi_target", "prestiti_target",
    "depositi_target", "scarto_personale", "scarto_costi", "scarto_prestiti", "scarto_depositi"])
salva_dati(target.round(4), "dea_target")

efficienti = [j for j in range(n) if abs(ris[j]["ccr"] - 1) < TOL]
conta = {j + 1: sum(1 for o in range(n) if abs(ris[o]["ccr"] - 1) > TOL and ris[o]["lam"][j] > TOL)
         for j in efficienti}
print("Quante volte ogni filiale efficiente è peer di una inefficiente: "
      + ", ".join(f"{j}: {c}" for j, c in conta.items()))

# ----------------------------------------------------------------------
# 7. SENSITIVITÀ: prezzi ombra verificati per perturbazione e stabilità
# ----------------------------------------------------------------------
intestazione("Sensitività: prezzi ombra dei vincoli sugli output (filiale meno efficiente)")
o_min = int(eff["ccr"].idxmin())
md, th, lam, c_in, c_out = inviluppo(X, Y, o_min)
print(f"filiale {o_min + 1}: theta = {th.X:.4f}")
for r in range(2):
    c = c_out[r]
    print(f"  output {nomi_out[r]:8s}: y = {Y[r, o_min]:.1f} | Pi = {c.Pi:.5f} | "
          f"valido per il termine noto in [{c.SARHSLow:.2f}, {c.SARHSUp:.2f}]")
r_star = int(np.argmax([c_out[r].Pi for r in range(2)]))
nuovo = Y[:, o_min].copy()
nuovo[r_star] += 1
md2, th2, _, _, _ = inviluppo(X, Y, o_min, rhs_out=nuovo)
print(f"Verifica: termine noto di {nomi_out[r_star]} da {Y[r_star, o_min]:.1f} a {nuovo[r_star]:.1f} "
      f"-> theta da {th.X:.4f} a {th2.X:.4f} (variazione {th2.X - th.X:+.5f} = Pi {c_out[r_star].Pi:.5f})")
print(f"Confronto: peso u del primale = ({ris[o_min]['u'][0]:.5f}, {ris[o_min]['u'][1]:.5f})")

intestazione("Stabilità: si toglie il peer più citato e si ricalcola la CCR")
j_peer = max(conta, key=conta.get) - 1
resto = [j for j in range(n) if j != j_peer]
Xr, Yr = X[:, resto], Y[:, resto]
cambi = []
for k, o in enumerate(resto):
    md, th, _, _, _ = inviluppo(Xr, Yr, k)
    cambi.append((o + 1, ris[o]["ccr"], th.X))
    seg = "  <- cambia" if th.X - ris[o]["ccr"] > 1e-6 else ""
    print(f"  filiale {o + 1:2d}: CCR {ris[o]['ccr']:.4f} -> {th.X:.4f}{seg}")
print(f"Senza la filiale {j_peer + 1}: {sum(1 for c in cambi if c[2] - c[1] > 1e-6)} filiali "
      f"cambiano efficienza; nuove efficienti: "
      f"{[c[0] for c in cambi if abs(c[2] - 1) < TOL and abs(c[1] - 1) > TOL]}")

# ----------------------------------------------------------------------
# 8. FIGURE (dati per pgfplots + anteprima matplotlib)
# ----------------------------------------------------------------------
salva_dat(eff[["filiale", "ccr", "bcc"]], "cap12_efficienze")

# vista a un input e un output: personale -> prestiti
Xp, Yp = X[[0], :], Y[[0], :]
bcc_p = []
for o in range(n):
    md, th, _, _, _ = inviluppo(Xp, Yp, o, vrs=True)
    _, s_in, s_out = scarti(Xp, Yp, o, th.X, vrs=True)
    bcc_p.append((th.X, s_in.sum() + s_out.sum()))
ccr_p = []
for o in range(n):
    md, th, _, _, _ = inviluppo(Xp, Yp, o)
    ccr_p.append(th.X)
frontiera = sorted((Xp[0, o], Yp[0, o]) for o in range(n)
                   if abs(bcc_p[o][0] - 1) < TOL and bcc_p[o][1] < TOL)
pend = max(Yp[0] / Xp[0])
x_max = 32.0
vrs = [(frontiera[0][0], 0.0)] + frontiera + [(x_max, frontiera[-1][1])]
salva_dat(pd.DataFrame({"filiale": filiali, "personale": Xp[0], "prestiti": Yp[0],
                        "ccr": np.round(ccr_p, 6), "bcc": np.round([b[0] for b in bcc_p], 6)}),
          "cap12_frontiera_punti")
salva_dat(pd.DataFrame(vrs, columns=["personale", "prestiti"]), "cap12_frontiera_vrs")
salva_dat(pd.DataFrame({"personale": [0.0, x_max], "prestiti": [0.0, pend * x_max]}),
          "cap12_frontiera_crs")
intestazione("Vista a un input e un output: personale -> prestiti")
print(f"Pendenza della frontiera CCR (prestiti per FTE): {pend:.4f}")
print("Efficienze nella vista (CCR/BCC): "
      + "; ".join(f"{o + 1}: {ccr_p[o]:.3f}/{bcc_p[o][0]:.3f}" for o in range(n)))
print("Vertici della frontiera BCC: " + ", ".join(f"({a:.0f}, {b:.1f})" for a, b in frontiera))

fig, ax = plt.subplots()
ax.plot([0, x_max], [0, pend * x_max], "--", color=ROSSO, label="frontiera CCR (scala costante)")
ax.plot([a for a, _ in vrs], [b for _, b in vrs], "-", color=TEAL, lw=2,
        label="frontiera BCC (scala variabile)")
ax.scatter(Xp[0], Yp[0], color=BLU, zorder=3, label="filiali")
for o in range(n):
    ax.annotate(str(o + 1), (Xp[0, o], Yp[0, o]), textcoords="offset points", xytext=(4, 4),
                fontsize=8)
ax.set_xlim(0, x_max); ax.set_ylim(0, 75)
ax.set_xlabel("personale (FTE)"); ax.set_ylabel("prestiti (M€)")
ax.set_title("Frontiere efficienti CCR e BCC: personale e prestiti")
ax.legend(fontsize=8)
salva_figura(fig, "cap12_frontiera")

fig, ax = plt.subplots()
larg = 0.38
ax.bar(np.array(filiali) - larg / 2, eff["ccr"], width=larg, color=TEAL, label="CCR")
ax.bar(np.array(filiali) + larg / 2, eff["bcc"], width=larg, color=ARANCIO, label="BCC")
ax.axhline(1, color=GRIGIO, ls=":")
ax.set_xticks(filiali)
ax.set_ylim(0.6, 1.12)
ax.set_xlabel("filiale"); ax.set_ylabel("efficienza")
ax.set_title("Efficienze CCR e BCC delle 12 filiali")
ax.legend(fontsize=8, loc="upper center", ncol=2)
salva_figura(fig, "cap12_efficienze")

print("\nFatto: capitolo 12.")
