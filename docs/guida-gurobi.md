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
cinque passi**. Usiamo come esempio un piccolo problema di produzione:

> Un'azienda produce due prodotti, 1 e 2. Ogni unità del prodotto 1 rende 30 €, ogni unità del prodotto 2 50 €.
> Il prodotto 1 richiede 1 ora di lavorazione e 2 kg di materia prima; il prodotto 2 richiede 3 ore e 1 kg.
> Sono disponibili 90 ore e 80 kg. Quanto produrre per massimizzare il ricavo?

Il modello matematico:

```
max  30 x_1 + 50 x_2
s.t.  1 x_1 + 3 x_2 ≤ 90    (ore)
      2 x_1 + 1 x_2 ≤ 80    (materiale)
      x_1, x_2 ≥ 0
```

### Passo 1 — creare il contenitore del modello

```python
import gurobipy as gp
from gurobipy import GRB

m = gp.Model("produzione")
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
prodotti = ["A", "B", "C"]
mesi     = range(6)
x = m.addVars(prodotti, mesi, name="x")    # crea x["A",0], x["A",1], ...
```

`addVars` restituisce un dizionario `tupledict`: si accede con `x["A", 3]`.

### Passo 3 — aggiungere i vincoli

```python
v_ore = m.addConstr(1*x1 + 3*x2 <= 90, name="ore")
v_mat = m.addConstr(2*x1 + 1*x2 <= 80, name="materiale")
```

- si scrive il vincolo **come una disuguaglianza Python** tra espressioni lineari;
- conservare l'oggetto restituito (`v_ore`) serve dopo, per leggere il **prezzo ombra**;
- per famiglie di vincoli:

```python
m.addConstrs((x.sum(i, "*") <= capacita[i] for i in prodotti), name="cap")
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
m.write("produzione.lp")     # scrive il modello in formato leggibile
```

Il file `.lp` mostra esattamente il modello che il solver vede: **è il primo strumento di
debug** quando l'ottimo "non torna".

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
for i in prodotti:
    for t in mesi:
        if x[i, t].X > 1e-6:              # stampa solo le variabili non nulle
            print(i, t, x[i, t].X)
```

Con **pandas**, per portare la soluzione in un DataFrame:

```python
import pandas as pd
sol = pd.DataFrame([(i, t, x[i, t].X) for i in prodotti for t in mesi],
                   columns=["prodotto", "mese", "quantita"])
```

---

## 5. Come si interpreta l'output

### 5.1 L'esito

- **OPTIMAL** — soluzione ottima certificata. Nei modelli convessi di questo laboratorio
  l'ottimo è **globale**; in un QP dichiarato non convesso (`NonConvex=2`) Gurobi certifica
  comunque il globale, mentre con un solver locale (scipy) l'ottimo può essere solo locale.
- **INFEASIBLE** — i vincoli si contraddicono. Diagnosi:
  `m.computeIIS(); m.write("conflitto.ilp")` — il file elenca un sottoinsieme minimale di
  vincoli in conflitto tra loro. Errore tipico: domanda totale > capacità totale senza
  variabile di shortage.
- **UNBOUNDED** — l'obiettivo può migliorare all'infinito: quasi sempre manca un vincolo o
  un bound (es. max profitto senza vincolo di capacità).

### 5.2 Prezzi ombra (`Pi`) — "quanto vale un'unità in più di risorsa?"

Nell'esempio di produzione: all'ottimo `x_1 = 30, x_2 = 20`, ricavo 1900 €, ed entrambi i
vincoli sono attivi. I duali valgono:

```python
print(v_ore.Pi)   # 14.0  → un'ora in più di lavorazione vale 14 €
print(v_mat.Pi)   # 8.0   → un kg in più di materia prima vale 8 €
```

Lettura manageriale: se un'ora di straordinario costa meno di 14 €, conviene comprarla.
**Validità**: solo marginale e solo dentro l'intervallo `SARHSLow ≤ b ≤ SARHSUp`; oltre,
la base cambia e il prezzo ombra non è più quello.

Un vincolo **non attivo** (`Slack > 0`) ha sempre `Pi = 0`: la risorsa avanza, un'unità in
più non vale nulla.

### 5.3 Costi ridotti (`RC`) — "perché questa variabile è a zero?"

Se `x_C.X = 0` e `x_C.RC = -4`, il prodotto C è fuori dal piano ottimo e il suo margine
dovrebbe **migliorare di almeno 4 €** perché entri in soluzione. Variabili in base hanno
`RC = 0`.

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
5. La soluzione è stabile? (rieseguire con dati perturbati del 5%)
6. Tradurre tutto in una **raccomandazione manageriale di tre righe**.

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

Per gli NLP generali (Weber, domanda logistica, M/M/1) si usa `scipy.optimize.minimize`:
stessa logica (dati → funzione obiettivo → risoluzione → lettura), la differenza è che il
risultato è un ottimo **locale** salvo convessità dimostrata.
