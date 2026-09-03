"""Calcoli di supporto per il fascicolo delle soluzioni degli esercizi.

Ogni sezione ristampa i numeri citati in soluzioni/soluzioni.tex, così che ogni
valore del fascicolo sia riproducibile con: python3 soluzioni_calcoli.py
"""
import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from scipy import stats

from stile import intestazione

rng = np.random.default_rng(42)


# ======================================================================
intestazione("Cap. 2, es. 2.1 — aumentare b1 pagando 12 per unita'")
def lp22(ore=90):
    m = gp.Model(); m.Params.OutputFlag = 0
    x1 = m.addVar(); x2 = m.addVar()
    c1 = m.addConstr(x1 + 3 * x2 <= ore)
    m.addConstr(2 * x1 + x2 <= 80)
    m.setObjective(30 * x1 + 50 * x2, GRB.MAXIMIZE)
    m.optimize()
    return m, m.ObjVal, c1


mtieni, base, c1 = lp22()
_, piu10, _ = lp22(100)
print(f"Con +10 ore: ricavo {piu10:.0f} vs {base:.0f} (+{piu10 - base:.0f}); "
      f"costo 10 ore = 120 -> guadagno netto {piu10 - base - 120:.0f}")
print(f"SARHSUp del vincolo ore = {c1.SARHSUp:.0f}: il prezzo ombra 14 vale fino a "
      f"{c1.SARHSUp:.0f} ore (Delta max = {c1.SARHSUp - 90:.0f})")

# ======================================================================
intestazione("Cap. 2, es. 2.2 — KKT con vincoli attivi")
mk = gp.Model(); mk.Params.OutputFlag = 0
xk = mk.addVar(); yk = mk.addVar()
mk.addConstr(xk + 2 * yk <= 2)
mk.setObjective((xk - 3) ** 2 + (yk - 1) ** 2, GRB.MINIMIZE)
mk.optimize()
print(f"ottimo ({xk.X:.4f}, {yk.X:.4f}), f = {mk.ObjVal:.4f} "
      f"(atteso: (2, 0), f = 2; attivi x+2y<=2 e y>=0; lambda=2, mu=2)")

# ======================================================================
intestazione("Cap. 4 — varianti del modello di produzione")
prodotti = ["1", "2", "3"]; mesi = list(range(1, 7))
domanda = {("1",1):110,("1",2):130,("1",3):150,("1",4):190,("1",5):210,("1",6):160,
           ("2",1):70,("2",2):80,("2",3):110,("2",4):140,("2",5):150,("2",6):100,
           ("3",1):50,("3",2):55,("3",3):60,("3",4):80,("3",5):95,("3",6):70}
cp = {"1":12.,"2":18.,"3":25.}; hg = {"1":.8,"2":1.2,"3":1.6}
au = {"1":.9,"2":1.4,"3":2.1}; cap = {1:420,2:420,3:460,4:460,5:460,6:420}
s0 = {"1":30,"2":20,"3":10}


def produzione(fatt_cap=1.0, pi_short=None, profitto=False, ss=0.0):
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(prodotti, mesi); s = m.addVars(prodotti, mesi)
    u = m.addVars(prodotti, mesi) if pi_short is not None else None
    y = m.addVars(prodotti, mesi) if profitto else None
    for i in prodotti:
        for t in mesi:
            ent = (s0[i] if t == 1 else s[i, t - 1]) + x[i, t]
            if profitto:
                m.addConstr(ent == y[i, t] + s[i, t])
                m.addConstr(y[i, t] <= domanda[i, t])
            elif pi_short is not None:
                m.addConstr(ent + u[i, t] == domanda[i, t] + s[i, t])
            else:
                m.addConstr(ent == domanda[i, t] + s[i, t])
            if ss > 0 and t < 6:
                m.addConstr(s[i, t] >= ss * domanda[i, t + 1])
    m.addConstrs(gp.quicksum(au[i] * x[i, t] for i in prodotti) <= cap[t] * fatt_cap
                 for t in mesi)
    if profitto:
        p = {"1": 20., "2": 30., "3": 42.}
        m.setObjective(gp.quicksum(p[i] * y[i, t] - cp[i] * x[i, t] - hg[i] * s[i, t]
                                   for i in prodotti for t in mesi), GRB.MAXIMIZE)
    else:
        obj = gp.quicksum(cp[i] * x[i, t] + hg[i] * s[i, t]
                          for i in prodotti for t in mesi)
        if pi_short is not None:
            obj += gp.quicksum(pi_short * u[i, t] for i in prodotti for t in mesi)
        m.setObjective(obj, GRB.MINIMIZE)
    m.optimize()
    return m, x, s, u, y


m0, *_ = produzione()
print(f"es. 4.2 — capacita' 90%, penalita' 40:")
m2, x2, s2, u2, _ = produzione(fatt_cap=0.9, pi_short=40.0)
persa = {i: sum(u2[i, t].X for t in mesi) for i in prodotti}
print(f"  costo {m2.ObjVal:.2f}; domanda persa: " +
      ", ".join(f"{i} {persa[i]:.1f}" for i in prodotti) +
      f"; nei mesi: " + str({t: round(sum(u2[i, t].X for i in prodotti), 1)
                             for t in mesi if sum(u2[i, t].X for i in prodotti) > .01}))
print("es. 4.3 — massimo profitto con servizio facoltativo:")
m3, x3, s3, _, y3 = produzione(profitto=True)
non_serv = {(i, t): domanda[i, t] - y3[i, t].X for i in prodotti for t in mesi
            if domanda[i, t] - y3[i, t].X > 0.01}
print(f"  profitto {m3.ObjVal:.2f}; domanda non servita: {non_serv}")
print("es. 4.5 — scorta di sicurezza 10%:")
m5, *_ = produzione(ss=0.10)
print(f"  costo {m5.ObjVal:.2f} (base {m0.ObjVal:.2f}, +{m5.ObjVal - m0.ObjVal:.2f})")

# ======================================================================
intestazione("Cap. 5 — perturbazioni sulla rete")
offerta = {"S1": 260, "S2": 240}
domanda5 = {"M1": 120, "M2": 90, "M3": 140, "M4": 100}
archi = {("S1","H1"):(220,4.,3.5),("S1","H2"):(180,6.5,1.2),("S2","H1"):(150,7.,1.5),
         ("S2","H2"):(220,3.5,4.),("H1","M1"):(130,3.,2.8),("H1","M2"):(100,4.5,1.),
         ("H1","M3"):(120,5.,1.2),("H1","M4"):(90,6.,1.),("H2","M1"):(80,6.,1.1),
         ("H2","M2"):(90,4.,2.5),("H2","M3"):(130,3.5,3.),("H2","M4"):(110,4.,2.4)}
A5 = list(archi); U5 = {a: archi[a][0] for a in A5}
c5 = {a: archi[a][1] for a in A5}; e5 = {a: archi[a][2] for a in A5}


def rete(dm4=100, u_h2m3=130, fatt_h2=1.0, tetto_E=None):
    m = gp.Model(); m.Params.OutputFlag = 0
    ub = dict(U5); ub[("H2", "M3")] = u_h2m3
    for a in A5:
        if fatt_h2 < 1 and "H2" in a:
            ub[a] = ub[a] * fatt_h2
    x = m.addVars(A5, ub=ub)
    m.addConstrs(x.sum(s, "*") <= offerta[s] for s in offerta)
    m.addConstrs(x.sum("*", h) == x.sum(h, "*") for h in ["H1", "H2"])
    dd = dict(domanda5); dd["M4"] = dm4
    m.addConstrs(x.sum("*", k) == dd[k] for k in dd)
    vE = None
    if tetto_E is not None:
        vE = m.addConstr(gp.quicksum(e5[a] * x[a] for a in A5) <= tetto_E)
    m.setObjective(gp.quicksum(c5[a] * x[a] for a in A5), GRB.MINIMIZE)
    m.optimize()
    em = sum(e5[a] * x[a].X for a in A5) if m.Status == GRB.OPTIMAL else None
    return m, vE, em


mb, _, _ = rete()
mM4, _, _ = rete(dm4=101)
mArc, _, _ = rete(u_h2m3=131)
print(f"es. 5.1 — M4 101: costo {mM4.ObjVal:.2f} (delta {mM4.ObjVal - mb.ObjVal:+.2f}); "
      f"arco H2->M3 +1: {mArc.ObjVal:.2f} (delta {mArc.ObjVal - mb.ObjVal:+.2f})")
mH2, _, _ = rete(fatt_h2=0.5)
print(f"es. 5.2 — hub H2 al 50%: costo {mH2.ObjVal:.2f} "
      f"(guasto costa {mH2.ObjVal - mb.ObjVal:+.2f})")
mE, vE, emE = rete(tetto_E=2000)
print(f"es. 5.4 — vincolo E<=2000: costo {mE.ObjVal:.2f}, duale {vE.Pi:.3f} EUR/kg, "
      f"emissioni {emE:.0f}")

# ======================================================================
intestazione("Cap. 6 — frontiera con u=0,2 e tracking error")
titoli = ["ENE","FIN","TEC","IND","SAN","CON","UTL","MAT"]; n6 = 8
beta6 = np.array([1.1,1.3,1.5,1.0,.6,.8,.4,1.2])
alfa6 = np.array([.05,.06,.11,.05,.045,.05,.035,.06])
sidio = np.array([.05,.055,.07,.04,.03,.035,.02,.06])
merc = rng.normal(.004, .035, 60)
R6 = alfa6[None,:]/12 + np.outer(merc, beta6) + rng.normal(0, sidio, (60, n6))
# NB: rng qui ha gia' generato i numeri del cap.4-5? no: default_rng(42) come lab06
mu6 = R6.mean(0) * 12; Q6 = np.cov(R6.T) * 12
print("(nota: usare gli stessi mu/Q di lab06 richiede lo stesso ordine di estrazione;")
print(" qui rng(42) e' vergine come in lab06, quindi i numeri coincidono)")


def mk(r_min=None, u=1.0, track=False):
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(n6, ub=u)
    m.addConstr(x.sum() == 1)
    if r_min is not None:
        m.addConstr(gp.quicksum(mu6[i]*x[i] for i in range(n6)) >= r_min)
    if track:
        xb = 1/8
        m.setObjective(gp.quicksum(Q6[i,j]*(x[i]-xb)*(x[j]-xb)
                                   for i in range(n6) for j in range(n6)), GRB.MINIMIZE)
    else:
        m.setObjective(gp.quicksum(Q6[i,j]*x[i]*x[j]
                                   for i in range(n6) for j in range(n6)), GRB.MINIMIZE)
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        return None, None
    w = np.array([x[i].X for i in range(n6)])
    return w, m.ObjVal


print(f"controllo: mu max = {mu6.max():.4f} (MAT, come lab06)")
for u in [1.0, 0.3, 0.2]:
    # rendimento massimo raggiungibile con tetto u
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(n6, ub=u); m.addConstr(x.sum() == 1)
    m.setObjective(gp.quicksum(mu6[i]*x[i] for i in range(n6)), GRB.MAXIMIZE)
    m.optimize()
    print(f"es. 6.2 — u = {u}: rendimento massimo {m.ObjVal:.2%}")
w_te, te = mk(r_min=0.12, track=True)
print(f"es. 6.4 — tracking error minimo con mu>=12%: TE = {np.sqrt(te):.2%}, "
      f"scostamenti max {np.abs(w_te - 1/8).max():.1%}")

# ======================================================================
intestazione("Cap. 7 — c=60 e ampliamenti")
a7, b7, K7 = 1200., 5., 400.
for cc in [20., 60.]:
    p_lib = (a7 / b7 + cc) / 2; q_lib = a7 - b7 * p_lib
    if q_lib > K7:
        p_st = (a7 - K7) / b7
        val = p_st - cc - K7 / b7
        print(f"c = {cc:.0f}: p libero {p_lib:.0f} (q {q_lib:.0f}); vincolato p* {p_st:.0f}, "
              f"profitto {(p_st - cc) * K7:.0f}, valore posto {max(val, 0):.0f}")
    else:
        print(f"c = {cc:.0f}: capacita' non attiva, p* = {p_lib:.0f}, q* = {q_lib:.0f}, "
              f"profitto {(p_lib - cc) * q_lib:.0f}, valore posto 0")


def multi7(K1=150., K2=300.):
    m = gp.Model(); m.Params.OutputFlag = 0; m.Params.NonConvex = 2
    p1 = m.addVar(ub=300); p2 = m.addVar(ub=300); q1 = m.addVar(); q2 = m.addVar()
    m.addConstr(q1 <= 500 - 2*p1 + .6*p2); m.addConstr(q2 <= 900 + .8*p1 - 4*p2)
    m.addConstr(q1 <= K1); m.addConstr(q2 <= K2)
    m.setObjective((p1-30)*q1 + (p2-15)*q2, GRB.MAXIMIZE); m.optimize()
    return m.ObjVal


b70 = multi7()
print(f"es. 7.5 — base {b70:.0f}; +50 platea: {multi7(K1=200) - b70:+.0f}; "
      f"+50 galleria: {multi7(K2=350) - b70:+.0f}")

# ======================================================================
intestazione("Cap. 8 — es. 8.1: esempio a mano con B = 80")
# 20/(1+0.2 x1) = 6/(1+0.1 x2), x1+x2=80
# risoluzione algebrica diretta: 20(1+0.1(80-x1)) = 6(1+0.2 x1)
# 20(9-0.1x1)=6+1.2x1 -> 180-2x1=6+1.2x1 -> x1=174/3.2
x1 = 174 / 3.2
lam = 20 / (1 + 0.2 * x1)
print(f"x1 = {x1:.2f}, x2 = {80 - x1:.2f}, lambda = {lam:.3f} (a B=50 era 2,46)")

# ======================================================================
intestazione("Cap. 9 — peso Q12 e raggio 2,1")
coord9 = np.array([[1,8.5],[2.5,6],[4,9],[5.5,7.5],[7,8],[9,9.5],
                   [1.5,3],[3,1.5],[5,3.5],[6.5,2],[8,4],[9.5,1]], float)
peso9 = np.array([12,18,9,22,15,6,14,8,25,10,16,5], float)


def localizza9(pesi=None, cabina=None, raggio=None):
    """Weber/minimax con Gurobi: cono dx^2 + dy^2 <= d^2 (come in lab09)."""
    m = gp.Model(); m.Params.OutputFlag = 0
    px = m.addVar(lb=-GRB.INFINITY); py = m.addVar(lb=-GRB.INFINITY)
    n = len(coord9); d = m.addVars(n)
    for k in range(n):
        dx = m.addVar(lb=-GRB.INFINITY); dy = m.addVar(lb=-GRB.INFINITY)
        m.addConstr(dx == px - coord9[k, 0]); m.addConstr(dy == py - coord9[k, 1])
        m.addQConstr(dx * dx + dy * dy <= d[k] * d[k])
    if cabina is not None:
        m.addQConstr((px - cabina[0]) ** 2 + (py - cabina[1]) ** 2 <= raggio ** 2)
    if pesi is not None:
        m.setObjective(gp.quicksum(pesi[k] * d[k] for k in range(n)), GRB.MINIMIZE)
    else:
        z = m.addVar(); m.addConstrs((d[k] <= z for k in range(n)))
        m.setObjective(z, GRB.MINIMIZE)
    m.optimize(); assert m.Status == GRB.OPTIMAL
    return np.array([px.X, py.X]), m.ObjVal


w0, _ = localizza9(peso9)
p2 = peso9.copy(); p2[11] = 40
w1, _ = localizza9(p2)
mm0, _ = localizza9()
print(f"es. 9.2 — Weber: da ({w0[0]:.2f},{w0[1]:.2f}) a ({w1[0]:.2f},{w1[1]:.2f}) "
      f"(spostamento {np.linalg.norm(w1 - w0):.2f} km); minimax invariato "
      f"({mm0[0]:.2f},{mm0[1]:.2f}) perche' ignora i pesi")
cab = np.array([7., 6.])
for R in [2.0, 2.1]:
    _, costo_R = localizza9(peso9, cabina=cab, raggio=R)
    print(f"es. 9.5 — R = {R}: costo {costo_R:.2f}")

# ======================================================================
intestazione("Cap. 10 — E1=47 e capacita' minima")
ore10 = list(range(24))
prezzo10 = np.array([.09,.08,.07,.07,.08,.10,.14,.18,.20,.19,.17,.16,.15,.15,.16,.18,
                     .21,.24,.26,.24,.20,.15,.12,.10])
base10 = np.array([22,20,19,19,20,24,35,48,60,63,65,64,62,61,62,64,66,68,62,55,45,36,
                   30,25], float)
flotta = {"V1":(18,7,46,11),"V2":(19,6,38,11),"V3":(20,8,55,22),"V4":(17,6,30,7.4),
          "V5":(21,7,42,11),"V6":(22,8,50,22)}
veic = list(flotta); eta10 = 0.95
disp10 = {(v,t): 1 if (flotta[v][0] <= t or t < flotta[v][1]) else 0
          for v in veic for t in ore10}


def ev(C=120., E1=46.):
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(veic, ore10)
    for v in veic:
        for t in ore10:
            x[v, t].UB = flotta[v][3] * disp10[v, t]
    for v in veic:
        E = E1 if v == "V1" else flotta[v][2]
        m.addConstr(eta10 * gp.quicksum(x[v, t] for t in ore10) >= E)
    m.addConstrs(gp.quicksum(x[v, t] for v in veic) <= C - base10[t] for t in ore10)
    m.setObjective(gp.quicksum(prezzo10[t] * x[v, t] for v in veic for t in ore10),
                   GRB.MINIMIZE)
    m.optimize()
    return m


mb10 = ev(); m47 = ev(E1=47.)
print(f"es. 10.1 — E1 47: costo {m47.ObjVal:.4f} vs {mb10.ObjVal:.4f} "
      f"(delta {m47.ObjVal - mb10.ObjVal:+.4f} ~ 0.09/0.95 = {0.09/0.95:.4f})")
lo, hi = 60., 70.
for _ in range(20):
    mid = (lo + hi) / 2
    lo, hi = (lo, mid) if ev(C=mid).Status == GRB.OPTIMAL else (mid, hi)
print(f"es. 10.5 — capacita' minima ammissibile: C* in [{lo:.2f}, {hi:.2f}] kW")

# ======================================================================
intestazione("Cap. 11 — costo d'attesa quadratico")
lam11, c11, h11 = 42., 3., 1.5
mu_q = lam11 + (2 * h11 / c11) ** (1 / 3)
mq11 = gp.Model(); mq11.Params.OutputFlag = 0
mq11.Params.NonConvex = 2; mq11.Params.MIPGap = 1e-9
mu11 = mq11.addVar(lb=lam11 + 1e-3, ub=4 * lam11)
v11 = mq11.addVar(lb=1e-3, ub=4 * lam11)      # v = mu - lam
s11 = mq11.addVar(lb=1e-6, ub=1e5)            # s = v^2
w11 = mq11.addVar(lb=1e-6, ub=1e6)            # w = 1/v^2
mq11.addConstr(v11 == mu11 - lam11)
mq11.addQConstr(s11 == v11 * v11)
mq11.addQConstr(w11 * s11 == 1)
mq11.setObjective(c11 * mu11 + h11 * w11, GRB.MINIMIZE)
mq11.optimize()
print(f"es. 11.2 — analitico mu* = lam + (2h/c)^(1/3) = {mu_q:.4f}; "
      f"Gurobi {mu11.X:.4f}; rho = {lam11 / mu_q:.1%} "
      f"(caso lineare: 90,2%)")

# ======================================================================
intestazione("Cap. 12 — varianti del newsvendor")
mu_d, s_d = 100., 20.
for nome, Cu, Co in [("base", 9., 4.), ("penalita' b=3", 12., 4.),
                     ("smaltimento v=-1", 9., 7.)]:
    al = Cu / (Cu + Co)
    print(f"es. 12.1/12.3 — {nome}: alpha* = {al:.4f}, "
          f"q* = {stats.norm.ppf(al, mu_d, s_d):.2f}")
rng12 = np.random.default_rng(42)
dom12 = np.maximum(rng12.normal(mu_d, s_d, 600), 0)
q_st = np.quantile(dom12, 9 / 13)
costi = 4 * np.maximum(q_st - dom12, 0) + 9 * np.maximum(dom12 - q_st, 0)
print(f"es. 12.4 — EVPI: wait-and-see costa 0, here-and-now {costi.mean():.2f} "
      f"-> una previsione perfetta vale fino a {costi.mean():.2f} EUR/ciclo")
# es 12.6: multiprodotto rho=0 vs 0.7
def multi12(rho):
    r = np.random.default_rng(7)
    mu_m = np.array([100., 80., 60.]); sig = np.array([20., 25., 15.])
    S = np.diag(sig) @ (np.full((3, 3), rho) + (1 - rho) * np.eye(3)) @ np.diag(sig)
    d = np.maximum(r.multivariate_normal(mu_m, S, 300), 0)
    cc = np.array([6., 5., 4.]); Cu = np.array([9., 7., 5.]); Co = np.array([4., 3.5, 2.5])
    m = gp.Model(); m.Params.OutputFlag = 0
    q = m.addVars(3); o = m.addVars(3, 300); u = m.addVars(3, 300)
    m.addConstrs(o[i, s] >= q[i] - d[s, i] for i in range(3) for s in range(300))
    m.addConstrs(u[i, s] >= d[s, i] - q[i] for i in range(3) for s in range(300))
    m.addConstr(gp.quicksum(cc[i] * q[i] for i in range(3)) <= 1200)
    m.setObjective(gp.quicksum((Co[i]*o[i,s] + Cu[i]*u[i,s]) / 300
                               for i in range(3) for s in range(300)), GRB.MINIMIZE)
    m.optimize()
    return m.ObjVal


print(f"es. 12.6 — costo atteso: rho=0,7 -> {multi12(0.7):.2f}; "
      f"rho=0 -> {multi12(0.0):.2f} (stessi margini, stesso budget, stesso seed)")

# ======================================================================
intestazione("Cap. 13 — es. 13.1: sei scenari con alpha = 0,90")
perd = np.array([2., 4., 5., 7., 12., 20.])
m13 = gp.Model(); m13.Params.OutputFlag = 0
eta = m13.addVar(lb=-GRB.INFINITY); xi = m13.addVars(6)
m13.addConstrs(xi[s] >= perd[s] - eta for s in range(6))
m13.setObjective(eta + gp.quicksum(xi[s] for s in range(6)) / (6 * 0.10), GRB.MINIMIZE)
m13.optimize()
print(f"VaR90 = 20 (cumulata 5/6 = 0,833 < 0,90); CVaR90 (LP) = {m13.ObjVal:.4f} "
      f"(la coda di massa 0,10 sta tutta sul punto 20)")

# ======================================================================
intestazione("Cap. 2 — costi ridotti sull'esempio 2x2 esteso (terza variabile)")
m2 = gp.Model(); m2.Params.OutputFlag = 0
x1 = m2.addVar(); x2 = m2.addVar(); x3 = m2.addVar()
m2.addConstr(x1 + 3*x2 + x3 <= 90); m2.addConstr(2*x1 + x2 + x3 <= 80)
m2.setObjective(30*x1 + 50*x2 + 20*x3, GRB.MAXIMIZE)
m2.optimize()
print(f"z* = {m2.ObjVal:.0f}, x = ({x1.X:.0f}, {x2.X:.0f}, {x3.X:.0f}); "
      f"RC = ({x1.RC:.0f}, {x2.RC:.0f}, {x3.RC:.0f}); SAObjUp(x3) = {x3.SAObjUp:.0f}")
assert (m2.ObjVal, x3.RC, x3.SAObjUp) == (1900.0, -2.0, 22.0)
m2b = gp.Model(); m2b.Params.OutputFlag = 0
z1 = m2b.addVar(); z2 = m2b.addVar(); z3 = m2b.addVar()
m2b.addConstr(z1 + 3*z2 + z3 <= 90); m2b.addConstr(2*z1 + z2 + z3 <= 80)
m2b.setObjective(30*z1 + 50*z2 + 23*z3, GRB.MAXIMIZE)
m2b.optimize()
print(f"controprova margine 23: z* = {m2b.ObjVal:.0f}, "
      f"x = ({z1.X:.0f}, {z2.X:.0f}, {z3.X:.0f})")
assert (m2b.ObjVal, z1.X, z2.X, z3.X) == (1975.0, 0.0, 5.0, 75.0)

# ======================================================================
intestazione("Cap. 2 — QP dell'esempio (svolto e KKT)")
for D_qp in [6.0, 7.0]:
    mqp = gp.Model(); mqp.Params.OutputFlag = 0
    q1 = mqp.addVar(); q2 = mqp.addVar()
    vq = mqp.addConstr(q1 + q2 >= D_qp)
    mqp.setObjective(q1 * q1 + 2 * q2 * q2, GRB.MINIMIZE)
    mqp.optimize()
    print(f"domanda {D_qp:.0f}: x = ({q1.X:.4f}, {q2.X:.4f}), f* = {mqp.ObjVal:.4f}, "
          f"lambda = {vq.Pi:.4f}")
assert abs(mqp.ObjVal - 98 / 3) < 1e-6   # f*(7) = 2/3 * 49

# ======================================================================
intestazione("Cap. 2/3 — LP 'tutti i casi' (620) ed es. 3.4 (log)")
mt = gp.Model(); mt.Params.OutputFlag = 0
t1 = mt.addVar(); t2 = mt.addVar(lb=-GRB.INFINITY)
t3 = mt.addVar(lb=-GRB.INFINITY, ub=0)
w1 = mt.addConstr(t1 + t2 >= 30); w2 = mt.addConstr(t1 + t2 - t3 == 100)
w3 = mt.addConstr(t1 - 2*t2 <= -20)
mt.setObjective(5*t1 + 8*t2 - 9*t3, GRB.MINIMIZE)
mt.optimize()
print(f"tutti i casi: z* = {mt.ObjVal:.0f}, x = ({t1.X:.0f}, {t2.X:.0f}, {t3.X:.0f}), "
      f"Pi = ({w1.Pi:.0f}, {w2.Pi:.0f}, {w3.Pi:.0f}), "
      f"RC = ({t1.RC:.0f}, {t2.RC:.0f}, {t3.RC:.0f}), SAObjUp(x3) = {t3.SAObjUp:.0f}")
assert (mt.ObjVal, w1.Pi, w2.Pi, w3.Pi, t3.RC, t3.SAObjUp) == (620., 0., 6., -1., -3., -6.)

ml = gp.Model(); ml.Params.OutputFlag = 0; ml.Params.FuncNonlinear = 1
xl = ml.addVar(ub=10.0); gl = ml.addVar(lb=1.0)
zl = ml.addVar(lb=-GRB.INFINITY)
ml.addConstr(gl == 1 + xl); ml.addGenConstrLog(gl, zl)
ml.setObjective(5*zl - xl, GRB.MAXIMIZE)
ml.optimize()
print(f"es. 3.4 — max 5 log(1+x) - x: x* = {xl.X:.4f}, f* = {ml.ObjVal:.4f} "
      f"(analitico: x = 4, f = 5 ln 5 - 4 = {5*np.log(5)-4:.4f})")
assert abs(xl.X - 4) < 1e-4

# ======================================================================
intestazione("Cap. 14 — arbitraggio: es. 14.1-14.3")
Rarb = 1.04
s1a = np.array([[Rarb, Rarb, Rarb], [10., 15., 13.], [30., 15., 25.]])


def lp_arb(s0, k=1.0):
    m = gp.Model(); m.Params.OutputFlag = 0; m.Params.DualReductions = 0
    xx = m.addVars(3, lb=-GRB.INFINITY)
    cc = m.addConstrs((gp.quicksum(s1a[i, j]*xx[i] for i in range(3)) >= 0
                       for j in range(3)))
    m.addConstr(gp.quicksum(s0[i]*xx[i] for i in range(3)) >= -k)
    m.setObjective(gp.quicksum(s0[i]*xx[i] for i in range(3)), GRB.MINIMIZE)
    m.optimize(); return m, cc


m14, _ = lp_arb([1, 6, 20], k=5)
print(f"es. 14.1 — normalizzazione a 5: ottimo {m14.ObjVal:.1f}; "
      f"strategia (-135, 5, 5): costo {-135 + 30 + 100}")
assert m14.ObjVal == -5.0

m14b, cc = lp_arb([1, 13, 21.538462])
q14 = [round(Rarb*cc[j].Pi, 2) for j in range(3)]
m14c, _ = lp_arb([1, 13, 21.60])
print(f"es. 14.2 — a 21.5385: ottimo {m14b.ObjVal:.4f}, q = {q14}; "
      f"a 21.60: ottimo {m14c.ObjVal:.1f}")
assert abs(m14b.ObjVal) < 1e-6 and m14c.ObjVal == -1.0 and q14 == [0.0, 0.26, 0.74]

d14 = gp.Model(); d14.Params.OutputFlag = 0
pp = d14.addVars(3)
d14.addConstr(gp.quicksum(Rarb*pp[j] for j in range(3)) == 1)
d14.addConstr(gp.quicksum(s1a[1, j]*pp[j] for j in range(3)) == 13)
d14.addConstr(gp.quicksum(s1a[2, j]*pp[j] for j in range(3)) == 18.692308)
h14 = np.maximum(s1a[2] - 20, 0)
d14.setObjective(gp.quicksum(h14[j]*pp[j] for j in range(3)), GRB.MINIMIZE)
d14.optimize()
print(f"es. 14.3 — call su titolo 2, strike 20: prezzo {d14.ObjVal:.4f} "
      f"(= 10 q1 / R = {10*0.296/1.04:.4f})")
assert abs(d14.ObjVal - 2.846154) < 1e-4

intestazione("Cap. 16 — regressione: es. 16.1-16.5")


def qr16(X, y, tau=0.5, budget=None):
    """Regressione quantile come LP (la stessa del capitolo 16)."""
    nn, pp = X.shape
    m = gp.Model(); m.Params.OutputFlag = 0
    w = m.addVars(pp, lb=-GRB.INFINITY); b = m.addVar(lb=-GRB.INFINITY)
    u = m.addVars(nn); v = m.addVars(nn)
    c = m.addConstrs(gp.quicksum(X[i, j]*w[j] for j in range(pp)) + b + u[i] - v[i]
                     == y[i] for i in range(nn))
    vb = None
    if budget is not None:
        z = m.addVars(pp)
        m.addConstrs(w[j] <= z[j] for j in range(pp))
        m.addConstrs(-w[j] <= z[j] for j in range(pp))
        vb = m.addConstr(gp.quicksum(z[j] for j in range(pp)) <= budget)
    m.setObjective(gp.quicksum(tau*u[i] + (1-tau)*v[i] for i in range(nn)), GRB.MINIMIZE)
    m.optimize()
    return m, np.array([w[j].X for j in range(pp)]), b.X, np.array([c[i].Pi for i in range(nn)]), vb


y16 = np.array([88., 96., 104., 112., 120., 132., 148.])
m16, _, b16, pi16, _ = qr16(np.zeros((7, 0)), y16, 0.5)
print(f"es. 16.1 — mediana {b16:.0f}, valore {m16.ObjVal:.0f}, "
      f"somma dei duali {pi16.sum():.6f}")
assert b16 == 112.0 and m16.ObjVal == 56.0 and abs(pi16.sum()) < 1e-9

rng16 = np.random.default_rng(16)
n16 = 60
temp16 = np.round(rng16.uniform(10, 34, n16), 1)
prezzo16 = rng16.choice([2.20, 2.60, 3.00, 3.40], n16)
week16 = (rng16.random(n16) < 0.30).astype(float)
dom16 = (258 - 3.7*temp16 - 19.0*prezzo16 + 33.0*week16 + rng16.normal(0, 9, n16))
sciop16 = [11, 22, 29, 41, 46]
dom16[sciop16] = rng16.uniform(18, 32, len(sciop16))
dom16 = np.round(dom16).astype(float)

Xt16 = temp16.reshape(-1, 1)
_, w16, bb16, _, _ = qr16(Xt16, dom16, 0.5)
res16 = dom16 - (Xt16 @ w16 + bb16)
app16 = np.where(np.abs(res16) < 1e-6)[0]
sopra16 = np.where(res16 > 1e-6)[0]
d_su = dom16.copy(); d_su[sopra16[0]] += 30
_, wA16, bA16, _, _ = qr16(Xt16, d_su, 0.5)
d_ap = dom16.copy(); d_ap[app16[0]] -= 30
_, wB16, bB16, _, _ = qr16(Xt16, d_ap, 0.5)
print(f"es. 16.2 — retta {bb16:.2f} {w16[0]:+.2f}t; +30 su un punto sopra: "
      f"{bA16:.2f} {wA16[0]:+.2f}t (invariata); -30 su un appoggio: "
      f"{bB16:.2f} {wB16[0]:+.2f}t")
assert len(app16) == 2 and abs(bA16 - bb16) < 1e-6 and abs(bB16 - 211.84) < 0.01

X3_16 = np.column_stack([temp16, prezzo16, week16])
_, w3_16, b3_16, _, _ = qr16(X3_16, dom16, 0.5)
puliti16 = np.abs(dom16 - (X3_16 @ w3_16 + b3_16)) <= 40
tipo16 = np.array([28.0, 3.00, 1.0])
prev16 = {}
for co, tau in ((4, 9/13), (2, 9/11)):
    _, wq, bq, _, _ = qr16(X3_16[puliti16], dom16[puliti16], tau)
    prev16[co] = float(tipo16 @ wq + bq)
print(f"es. 16.3 — co=4 (alpha*=9/13): {prev16[4]:.1f} pezzi; "
      f"co=2 (alpha*=9/11): {prev16[2]:.1f} pezzi (+{prev16[2]-prev16[4]:.1f})")
assert abs(prev16[4] - 132.1) < 0.1 and abs(prev16[2] - 139.6) < 0.1

foll16 = np.round(rng16.uniform(8, 20, n16), 1)
pio16 = np.round(rng16.uniform(0, 12, n16), 1)
bor16 = np.round(rng16.uniform(95, 115, n16), 1)
gm16 = rng16.integers(1, 29, n16).astype(float)
Xg16 = np.column_stack([temp16, prezzo16, week16, foll16, pio16, bor16, gm16])[puliti16]
Xs16 = (Xg16 - Xg16.mean(0)) / Xg16.std(0)
y3_16 = dom16[puliti16]
vals16, ombre16 = [], []
for t in np.arange(0, 60.5, 1.0):
    mt, wt, bt, _, vb = qr16(Xs16, y3_16, 0.5, budget=t)
    vals16.append(mt.ObjVal); ombre16.append(vb.Pi)
vals16 = np.array(vals16); ombre16 = np.array(ombre16)
convessa = all(vals16[i+1] - 2*vals16[i] + vals16[i-1] > -1e-6
               for i in range(1, len(vals16)-1))
rotture = sum(1 for i in range(1, 61) if abs(ombre16[i] - ombre16[i-1]) > 1e-6)
print(f"es. 16.4 — valore da {vals16[0]:.1f} a {vals16[-1]:.1f}, convesso: "
      f"{convessa}, {rotture} cambi di prezzo ombra")
assert convessa and np.all(np.diff(vals16) <= 1e-6) and rotture == 35

rs16 = np.random.default_rng(7)
idx16 = rs16.permutation(len(y3_16))
stima16, verif16 = idx16[:40], idx16[40:]
err16 = {}
for t in range(5, 60, 5):
    _, wt, bt, _, _ = qr16(Xs16[stima16], y3_16[stima16], 0.5, budget=t)
    err16[t] = (float(np.abs(y3_16[stima16] - (Xs16[stima16] @ wt + bt)).mean()),
                float(np.abs(y3_16[verif16] - (Xs16[verif16] @ wt + bt)).mean()))
mono = all(err16[t][0] >= err16[t+5][0] - 1e-9 for t in range(5, 55, 5))
print(f"es. 16.5 — stima monotona: {mono}; verifica 45: {err16[45][1]:.2f}, "
      f"50: {err16[50][1]:.2f}, 55: {err16[55][1]:.2f} (non monotona)")
assert mono and err16[50][1] > err16[45][1]


print("\nTutti i calcoli delle soluzioni completati.")
