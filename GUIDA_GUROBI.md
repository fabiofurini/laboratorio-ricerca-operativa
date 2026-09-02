# Guida a Gurobi in Python (`gurobipy`)

Guida autonoma per il Laboratorio di Ricerca Operativa: **come si costruisce un modello, come si
fa girare, come si recupera la soluzione e come si interpreta l'output**. Tutti gli esempi sono
copia-incollabili in un terminale Python.

---

## 1. Installazione e licenza

```bash
python3 -m pip install gurobipy
```

Il pacchetto pip include una **licenza dimostrativa** (fino a 2000 variabili e 2000 vincoli):
sufficiente per tutti i modelli di questo laboratorio. All'avvio compare la riga
`Restricted license - for non-production use only`: è normale.

**Licenza accademica completa (gratuita):**
1. registrarsi su <https://portal.gurobi.com> con l'email istituzionale (`@uniroma1.it`);
2. richiedere una *Named-User Academic License*;
3. eseguire il comando `grbgetkey XXXXXXXX-...` mostrato dal portale (serve la rete di ateneo o VPN);
4. la licenza viene salvata in `~/gurobi.lic` e da quel momento non ci sono limiti di dimensione.

Verifica rapida:

```python
import gurobipy as gp
print(gp.gurobi.version())        # es. (13, 0, 3)
```

---

## 2. Come si costruisce un modello

Un modello di programmazione matematica in `gurobipy` si costruisce **sempre negli stessi
cinque passi**. Usiamo come esempio un piccolo LP generico di massimo, con due
variabili non negative e due vincoli di tipo ≤ — lo stesso LP 2×2 dei richiami
(gli esempi con dati reali arrivano nei capitoli applicativi):

```
max         30 x_1 + 50 x_2
soggetto a   1 x_1 +  3 x_2 ≤ 90    (vincolo 1)
             2 x_1 +  1 x_2 ≤ 80    (vincolo 2)
               x_1,     x_2 ≥ 0
```

### Passo 1 — creare il contenitore del modello

```python
import gurobipy as gp
from gurobipy import GRB

m = gp.Model("lp_2x2")
```

`m` è un oggetto vuoto a cui aggiungeremo variabili, vincoli e obiettivo.

### Passo 2 — aggiungere le variabili decisionali

```python
x1 = m.addVar(lb=0, name="x1")        # lb = lower bound (default 0)
x2 = m.addVar(lb=0, name="x2")
```

Punti importanti:
- il **default** è variabile continua con `lb=0` e `ub=+inf`: per variabili non negative basta `m.addVar(name=...)`;
- `vtype=GRB.CONTINUOUS` è il default; in questo laboratorio **non usiamo mai** `GRB.BINARY`/`GRB.INTEGER`;
- per una variabile libera (anche negativa, es. l'intercetta `b` della SVM o la soglia `η` del CVaR): `m.addVar(lb=-GRB.INFINITY)`.

Per **famiglie di variabili indicizzate** (il caso normale nei modelli veri):

```python
I = ["1", "2", "3"]              # indici (es. oggetti numerati)
T = range(6)                     # indici (es. periodi)
x = m.addVars(I, T, name="x")    # crea x["1",0], x["1",1], ...
```

`addVars` restituisce un dizionario `tupledict`: si accede con `x["1", 3]`.

### Passo 3 — aggiungere i vincoli

```python
v1 = m.addConstr(1*x1 + 3*x2 <= 90, name="vincolo1")
v2 = m.addConstr(2*x1 + 1*x2 <= 80, name="vincolo2")
```

- si scrive il vincolo **come una disuguaglianza Python** tra espressioni lineari;
- conservare l'oggetto restituito (`v1`) serve dopo, per leggere il **prezzo ombra**;
- per famiglie di vincoli:

```python
m.addConstrs((x.sum(i, "*") <= b[i] for i in I), name="cap")
```

- le somme si scrivono con `gp.quicksum(...)` oppure con `x.sum(i, "*")`
  (somma su tutti i valori del secondo indice).

### Passo 4 — impostare la funzione obiettivo

```python
m.setObjective(30*x1 + 50*x2, GRB.MAXIMIZE)
```

Il secondo argomento è `GRB.MAXIMIZE` o `GRB.MINIMIZE`. Obiettivi **quadratici** (Markowitz,
SVM, smoothing) si scrivono in modo naturale:

```python
m.setObjective(x @ Q @ x, GRB.MINIMIZE)                  # forma matriciale (numpy)
m.setObjective(gp.quicksum(q[i,j]*x[i]*x[j] for i in I for j in I), GRB.MINIMIZE)
```

### Passo 5 — (facoltativo) controllare quello che abbiamo scritto

```python
m.write("lp_2x2.lp")         # scrive il modello in formato leggibile
```

Il file `.lp` mostra esattamente il modello che il solver vede: **è il primo strumento di
debug** quando l'ottimo "non torna".


### L'esempio completo, da cima a fondo

Il ciclo intero — costruzione, risoluzione, lettura di TUTTO quello che il solver
restituisce — sull'LP 2×2:

```python
import gurobipy as gp
from gurobipy import GRB

m = gp.Model("lp_2x2")
m.Params.OutputFlag = 0
x1 = m.addVar(name="x1")
x2 = m.addVar(name="x2")
v1 = m.addConstr(1*x1 + 3*x2 <= 90, name="vincolo1")
v2 = m.addConstr(2*x1 + 1*x2 <= 80, name="vincolo2")
m.setObjective(30*x1 + 50*x2, GRB.MAXIMIZE)
m.optimize()
assert m.Status == GRB.OPTIMAL

print(f"Valore ottimo: {m.ObjVal:.1f}")
for v in m.getVars():
    print(f"  {v.VarName}: X = {v.X:.1f}   RC = {v.RC:.1f}   "
          f"SAObj = [{v.SAObjLow:.1f}, {v.SAObjUp:.1f}]")
for c in m.getConstrs():
    print(f"  {c.ConstrName}: Slack = {c.Slack:.1f}   Pi = {c.Pi:.1f}   "
          f"SARHS = [{c.SARHSLow:.1f}, {c.SARHSUp:.1f}]")
```

Output (verificato):

```
Valore ottimo: 1900.0
  x1: X = 30.0   RC = 0.0   SAObj = [16.7, 100.0]
  x2: X = 20.0   RC = 0.0   SAObj = [15.0, 90.0]
  vincolo1: Slack = 0.0   Pi = 14.0   SARHS = [40.0, 240.0]
  vincolo2: Slack = 0.0   Pi = 8.0   SARHS = [30.0, 180.0]
```

La sezione 5 spiega come leggere ciascuno di questi numeri; l'esempio "tutti i
casi" (sezione 5.3 bis) copre anche vincoli `=`/`≥` e variabili libere o `≤ 0`.


---

## 3. Come si fa girare

```python
m.optimize()
```

Tutto qui. Parametri utili da impostare **prima** di `optimize()`:

```python
m.Params.OutputFlag = 0      # 1 = log a video (default), 0 = silenzioso
m.Params.TimeLimit  = 60     # secondi massimi
m.Params.NonConvex  = 2      # consente QP non convessi (es. pricing p*q)
```

### Il log spiegato

```
Gurobi Optimizer version 13.0.3 ...
Optimize a model with 2 rows, 2 columns and 4 nonzeros   ← 2 vincoli, 2 variabili
Coefficient statistics:
  Matrix range  [1e+00, 3e+00]                            ← ordini di grandezza dei dati:
  Objective range [3e+01, 5e+01]                            se molto diversi (1e-6 e 1e+9)
  RHS range     [8e+01, 9e+01]                              il modello è mal scalato
Iteration    Objective       Primal Inf.    Dual Inf.      Time
       2    1.9000000e+03   0.000000e+00   0.000000e+00      0s
Optimal objective  1.900000000e+03                          ← valore ottimo trovato
```

Le righe da guardare sempre: il numero di righe/colonne (il modello ha la dimensione attesa?),
i *range* dei coefficienti (dati scalati bene?) e l'ultima riga (esito).

---

## 4. Come si recupera la soluzione

**Prima di leggere qualunque valore, controllare sempre lo stato:**

```python
if m.Status == GRB.OPTIMAL:
    print("Valore ottimo:", m.ObjVal)
    print("x1 =", x1.X, " x2 =", x2.X)      # .X = valore della variabile all'ottimo
elif m.Status == GRB.INFEASIBLE:
    print("Modello inammissibile")
elif m.Status == GRB.UNBOUNDED:
    print("Modello illimitato")
```

| Attributo | Su cosa | Significato |
|---|---|---|
| `m.Status` | modello | esito: `OPTIMAL` (2), `INFEASIBLE` (3), `UNBOUNDED` (5), `TIME_LIMIT` (9) |
| `m.ObjVal` | modello | valore della funzione obiettivo all'ottimo |
| `v.X` | variabile | valore ottimo della variabile |
| `v.RC` | variabile | **costo ridotto** (solo LP) |
| `c.Pi` | vincolo | **prezzo ombra / variabile duale** (solo LP) |
| `c.Slack` | vincolo | scarto: 0 ⇒ vincolo attivo (stringente) |
| `v.SAObjLow`, `v.SAObjUp` | variabile | intervallo del coefficiente di costo in cui la base ottima non cambia |
| `c.SARHSLow`, `c.SARHSUp` | vincolo | intervallo del termine noto in cui il prezzo ombra resta valido |

Per famiglie di variabili:

```python
for i in I:
    for t in T:
        if x[i, t].X > 1e-6:              # stampa solo le variabili non nulle
            print(i, t, x[i, t].X)
```

Con **pandas**, per portare la soluzione in un DataFrame:

```python
import pandas as pd
sol = pd.DataFrame([(i, t, x[i, t].X) for i in I for t in T],
                   columns=["i", "t", "valore"])
```

---

## 5. Come si interpreta l'output

### 5.1 L'esito

- **OPTIMAL** — soluzione ottima certificata. Nei modelli convessi di questo laboratorio
  l'ottimo è **globale**; anche in un QP dichiarato non convesso (`NonConvex=2`) e nei
  modelli con vincoli non lineari (`FuncNonlinear=1`) Gurobi certifica il globale.
- **INFEASIBLE** — i vincoli si contraddicono. Diagnosi:
  `m.computeIIS(); m.write("conflitto.ilp")` — il file elenca un sottoinsieme minimale di
  vincoli in conflitto tra loro. Errore tipico: domanda totale > capacità totale senza
  variabile di shortage.
- **UNBOUNDED** — l'obiettivo può migliorare all'infinito: quasi sempre manca un vincolo o
  un bound (es. max profitto senza vincolo di capacità).

### 5.2 Prezzi ombra (`Pi`) — "quanto vale un'unità in più di risorsa?"

Nell'LP 2×2: all'ottimo `x_1 = 30, x_2 = 20`, valore 1900, entrambi i vincoli
attivi. I duali valgono:

```python
print(v1.Pi)   # 14.0  → una unità in più di b_1 vale 14
print(v2.Pi)   # 8.0   → una unità in più di b_2 vale 8
```

Lettura: se procurare una unità in più di b_1 costa meno di 14, conviene.
**Validità**: solo marginale e solo dentro l'intervallo `SARHSLow ≤ b ≤ SARHSUp`; oltre,
la base cambia e il prezzo ombra non è più quello.

Un vincolo **non attivo** (`Slack > 0`) ha sempre `Pi = 0`: la risorsa avanza, un'unità in
più non vale nulla.

### 5.3 Costi ridotti (`RC`) — "perché questa variabile è a zero?"

Le variabili in base hanno `RC = 0` (attenzione: può esistere una variabile **in
base a valore zero** — base *degenere* — quindi `RC = 0` da solo non dice che la
variabile è usata); per una variabile a zero il costo ridotto dice **di quanto deve
migliorare il suo coefficiente in obiettivo perché convenga attivarla**.
Nell'LP 2×2: una terza variabile con coefficiente 20 e consumi 1 e 1 assorbe risorse
che ai prezzi ombra valgono 1·14 + 1·8 = 22 → il solver dà `x3.X = 0` e
`x3.RC = -2` (e `SAObjUp = 22`): il coefficiente deve salire di almeno 2.
Controprova: con coefficiente 23 la soluzione ottima cambia in (0, 5, 75), valore 1975.

Anche il costo ridotto ha il suo range di validità, `SAObjLow/Up`: l'intervallo in cui
il coefficiente in obiettivo può variare senza che la base ottima cambi (nell'esempio:
`c_1` può stare in [16,7, 100] senza spostare la soluzione; per una variabile a zero
`SAObjUp` è la soglia di convenienza).

Il ciclo standard per leggerli (solo LP):

```python
for v in m.getVars():
    if v.X < 1e-6:
        print(v.VarName, v.RC)
```

### 5.3 bis — Il caso generale: segni e lettura

**Prezzi ombra** (`Pi`): sempre la "derivata dell'ottimo rispetto al termine noto".
In un **massimo**: vincolo `≤` di risorsa → `Pi ≥ 0`; vincolo `≥` → `Pi ≤ 0`. In un
**minimo**: vincolo `≥` di domanda → `Pi ≥ 0`; vincolo `≤` di capacità → `Pi ≤ 0`.
Uguaglianza → segno qualunque (duale libera); vincolo non attivo → `Pi = 0`;
validità in `SARHSLow–SARHSUp`.

**Costi ridotti** (`RC`): variabile in base → `RC = 0`; al bound inferiore →
`RC ≥ 0` in un minimo, `RC ≤ 0` in un massimo (soglia di convenienza, validità in
`SAObjLow–SAObjUp`); al bound **superiore** → `RC` è il prezzo ombra del bound (un
arco saturo in un flusso di minimo costo ha `RC < 0`: una unità di capacità in più
fa risparmiare `|RC|`).

```python
for v in m.getConstrs():
    print(v.ConstrName, v.Pi, v.SARHSLow, v.SARHSUp)
for v in m.getVars():
    print(v.VarName, v.X, v.RC, v.SAObjLow, v.SAObjUp)
```

**L'esempio "tutti i casi"** — tre versi di vincolo e tre segni di variabile nello
stesso LP, per vedere ogni regola all'opera:

```python
m = gp.Model("tutti_i_casi")
x1 = m.addVar(name="x1")                          # x1 >= 0 (default)
x2 = m.addVar(lb=-GRB.INFINITY, name="x2")        # x2 libera
x3 = m.addVar(lb=-GRB.INFINITY, ub=0, name="x3")  # x3 <= 0
v1 = m.addConstr(x1 >= 30,            name="vincolo1")  # verso >=
v2 = m.addConstr(x1 + x2 - x3 == 100, name="vincolo2")  # verso  =
v3 = m.addConstr(x1 <= 60,            name="vincolo3")  # verso <=
m.setObjective(5*x1 + 8*x2 - 9*x3, GRB.MINIMIZE)
m.optimize()
```

```
Status: 2 (OPTIMAL)    ObjVal: 620.0
x1: X =  60.0  RC =  0.0  SAObj = [-inf, 8.0]
x2: X =  40.0  RC =  0.0  SAObj = [5.0, 9.0]
x3: X =   0.0  RC = -1.0  SAObj = [-inf, -8.0]
vincolo1: Slack = -30.0  Pi =  0.0  SARHS = [-inf, 60.0]
vincolo2: Slack =   0.0  Pi =  8.0  SARHS = [-inf, inf]
vincolo3: Slack =   0.0  Pi = -3.0  SARHS = [30.0, inf]
```

Tutti i casi in un colpo solo: vincolo non attivo → `Pi = 0` (vincolo1);
uguaglianza → duale libera, qui `+8`; `≤` in un minimo → duale `-3 ≤ 0`; due
variabili in base con `RC = 0`; la variabile `x3` ferma al suo **bound superiore**
(zero) con `RC = -1` e soglia `SAObjUp = -8`. Verifiche per perturbazione:
`b_2 = 101 → 628` (+8), `b_3 = 61 → 617` (−3), `x3` forzata a −1 → `621` (+1).

### 5.4 Nei modelli non lineari

Per QP/NLP convessi i moltiplicatori (`Pi` sui vincoli lineari, condizioni KKT in generale)
hanno la stessa lettura marginale dei prezzi ombra. Verifica numerica consigliata nel
laboratorio: perturbare il termine noto di ε e ricontrollare che
`nuovo_ottimo ≈ vecchio_ottimo + Pi·ε`.

### 5.5 Checklist di interpretazione (da usare in ogni esercitazione)

1. Lo stato è `OPTIMAL`? Se no, fermarsi e diagnosticare.
2. Il valore ottimo ha l'ordine di grandezza atteso?
3. Quali vincoli sono attivi (`Slack = 0`)? Sono quelli che ci aspettavamo?
4. Quanto valgono i prezzi ombra? Quale risorsa conviene potenziare per prima?
5. Ci sono variabili a zero? Leggere il loro costo ridotto (`RC`): la soglia di
   convenienza oltre la quale entrerebbero in soluzione.
6. La soluzione è stabile? (rieseguire con dati perturbati del 5%)
7. Tradurre tutto in una **raccomandazione manageriale di tre righe**.

---

## 6. Errori tipici e come riconoscerli

| Sintomo | Causa probabile | Rimedio |
|---|---|---|
| `KeyError` su `x[i,t]` | indici diversi da quelli usati in `addVars` | controllare tipi (stringa vs int) |
| ottimo = 0, tutte variabili nulle | obiettivo non impostato o verso sbagliato | controllare `setObjective(..., GRB.MAXIMIZE)` |
| `INFEASIBLE` inatteso | vincolo scritto con verso sbagliato, dati incoerenti | `computeIIS()` + leggere il `.ilp` |
| `UNBOUNDED` | manca un bound o un vincolo di capacità | scrivere il `.lp` e cercare la variabile libera |
| valori attesi ma `Pi` non disponibile | il modello è QP/MIP, i duali LP non esistono | per QP usare `m.Params.QCPDual = 1` o verifica per perturbazione |
| numeri "quasi zero" tipo `1e-13` | normale tolleranza numerica | filtrare con `> 1e-6` nelle stampe |
| `Model too large for size-limited license` | superati i limiti della licenza pip | attivare la licenza accademica (sez. 1) |

---

## 7. Scheletro standard da riutilizzare

Ogni script del laboratorio segue questo scheletro:

```python
import gurobipy as gp
from gurobipy import GRB

# 1. DATI ------------------------------------------------------
# leggere i CSV o definire i parametri

# 2. MODELLO ---------------------------------------------------
m = gp.Model("nome")
x = m.addVars(...)                     # variabili
m.addConstrs(...)                      # vincoli
m.setObjective(..., GRB.MINIMIZE)      # obiettivo

# 3. SOLUZIONE -------------------------------------------------
m.optimize()
assert m.Status == GRB.OPTIMAL, f"stato inatteso: {m.Status}"

# 4. RISULTATI -------------------------------------------------
# leggere .X, .Pi, .RC e stampare un report leggibile

# 5. SENSITIVITÀ -----------------------------------------------
# ciclo su un parametro chiave, ri-ottimizzare, salvare figure
```

**Un solver solo: anche gli NLP generali si risolvono con Gurobi** (dalla versione 12).
Funzioni non lineari come vincoli funzionali su variabili ausiliarie — `addGenConstrLog`,
`addGenConstrExp`, `addGenConstrPow` con `m.Params.FuncNonlinear = 1` — e termini bilineari
con `m.Params.NonConvex = 2`: l'ottimo resta **globale certificato**. Esempi nel laboratorio:
budget pubblicitario (`log`), pricing a elasticità costante (`Pow` + bilineare), code M/M/1
(vincolo bilineare `w·(mu - lam) = 1`), Weber (vincoli conici `dx² + dy² ≤ d²`, un QCP
convesso). Per le analisi marginali stringere `MIPGap`, `FeasibilityTol` e `OptimalityTol`
a `1e-9`; riformulare per evitare quantità minuscole (es. `q·p^eps ≤ A` invece di
`q ≤ A·p^(-eps)`).
