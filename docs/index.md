# Laboratorio di Ricerca Operativa

**Modelli continui di ottimizzazione per l'Ingegneria Gestionale** — dispensa,
codice Python/Gurobi, dati e casi di studio, tutto riproducibile.

Questo laboratorio insegna a usare la programmazione matematica come strumento di
**decisione**, non solo di calcolo. Ogni capitolo parte da un problema gestionale
concreto — quanto produrre, dove localizzare un servizio, quale prezzo fissare, quanto
rischio accettare — lo trasforma in un modello di ottimizzazione, lo risolve in Python
e, soprattutto, lo *interroga*: quanto vale un'ora di capacità in più? La soluzione
resiste se i dati cambiano del 5%? Quale compromesso consiglieremmo a un decisore?

!!! tip "La domanda giusta"
    Alla fine di ogni esercitazione la domanda non è soltanto *«qual è l'ottimo?»*,
    ma *«quale decisione suggeriamo e quanto è robusta?»*.

## Una scelta di campo: solo variabili continue

Tutti i modelli usano **esclusivamente variabili continue**: niente variabili binarie
o intere. Con variabili continue valgono la dualità, i prezzi ombra e le condizioni
KKT — gli strumenti che trasformano una soluzione numerica in una spiegazione
economica. E una quantità sorprendente di decisioni reali è naturalmente continua:
quantità, flussi, quote, prezzi, potenze, coordinate.

## Mappa dei modelli

| Capitolo | Applicazione | Classe | Concetto centrale |
|---|---|---|---|
| [Produzione e scorte](produzione.md) | pianificazione multiperiodale | LP / QP | dualità, capacità, smoothing |
| [Supply chain](supplychain.md) | flussi su rete e CO₂ | LP / NLP | congestione, frontiera costo-emissioni |
| [Markowitz](markowitz.md) | portafoglio finanziario | QP | rischio-rendimento |
| [Pricing](pricing.md) | revenue management | NLP | elasticità e capacità |
| [Budget pubblicitario](budget.md) | allocazione con saturazione | NLP convesso | rendimenti decrescenti, KKT |
| [Localizzazione](localizzazione.md) | dove aprire una struttura | NLP convesso | efficienza vs equità |
| [Ricarica EV](ricarica-ev.md) | smart charging | LP / QP | prezzi orari, peak shaving |
| [Code](code.md) | capacità di servizio | NLP convesso | il muro dell'utilizzazione |
| [Newsvendor](newsvendor.md) | decidere prima di sapere | LP stocastico | regola del quantile, scenari |
| [VaR e CVaR](var-cvar.md) | rischio di coda | LP | Rockafellar–Uryasev |
| [SVM](svm.md) | classificazione | QP | margine, duale, kernel |

## Come usare il materiale

```bash
python3 -m pip install gurobipy matplotlib pandas scipy
python3 python/esegui_tutti.py        # rigenera dati, risultati e figure
latexmk -pdf dispensa/main.tex        # compila la dispensa (81+ pagine)
```

- **`dispensa/`** — la dispensa LaTeX completa (teoria, esempi svolti a mano, casi di
  studio, codice commentato, esercizi); le figure sono pgfplots/TikZ che leggono i CSV
  generati dagli script, quindi sono modificabili in LaTeX e si aggiornano da sole.
- **`python/`** — uno script per capitolo, ognuno autonomo: dati → modello →
  soluzione → sensitività → figure.
- **`dati/`** — tutti i dati dei casi di studio in CSV (seed fissi, riproducibili).
- **`slides/`** — le slide beamer dei quattro laboratori.
- **`soluzioni/`** — le soluzioni degli esercizi (per i docenti).

## Percorso in quattro laboratori

1. **Produzione e scorte** — formulazione LP, duali, prezzi ombra e scenari.
2. **Markowitz** — QP convesso, frontiera efficiente, fragilità delle stime.
3. **Pricing oppure budget** — modellazione non lineare e verifica delle KKT.
4. **Progetto a scelta** — supply chain, ricarica EV, localizzazione, code,
   Newsvendor, CVaR o SVM, con presentazione manageriale dei risultati.

*Valutazione suggerita: formulazione 30%, implementazione e verifica 25%,
analisi di sensitività 25%, interpretazione manageriale 20%.*
