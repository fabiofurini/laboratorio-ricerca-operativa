# Implementazione: modelli non lineari

**Un solver solo: anche gli NLP generali si risolvono con Gurobi** (dalla
versione 12), con la stessa sintassi e la stessa checklist dei modelli lineari.
Funzioni non lineari come vincoli funzionali su variabili ausiliarie — `addGenConstrLog`,
`addGenConstrExp`, `addGenConstrPow` con `m.Params.FuncNonlinear = 1` — e termini bilineari
con `m.Params.NonConvex = 2`: l'ottimo resta **globale certificato**. Esempi nel laboratorio:
budget pubblicitario (`log`), pricing a elasticità costante (`Pow` + bilineare), code M/M/1
(vincolo bilineare `w·(mu - lam) = 1`), Weber (vincoli conici `dx² + dy² ≤ d²`, un QCP
convesso). Per le analisi marginali stringere `MIPGap`, `FeasibilityTol` e `OptimalityTol`
a `1e-9`; riformulare per evitare quantità minuscole (es. `q·p^eps ≤ A` invece di
`q ≤ A·p^(-eps)`).


## Come si scrivono

```python
m.Params.FuncNonlinear = 1     # funzioni trattate in modo esatto (globale)
z = m.addVar(lb=-GRB.INFINITY)
m.addGenConstrLog(g, z)        # z = log(g);  anche Exp, Pow, Sin, ...
m.addQConstr(w * v == 1)       # termini bilineari: servono NonConvex = 2
```

Due accorgimenti pratici, entrambi usati negli script del laboratorio:

- **tolleranze**: per analisi marginali accurate (differenze tra due ottimi
  vicini) stringere `MIPGap`, `FeasibilityTol` e `OptimalityTol` a `1e-9`;
- **scalatura**: riformulare per evitare quantità minuscole — ad esempio
  `q ≤ A·p^(-eps)` si scrive `q·r ≤ A` con `r = p^eps`, che tiene i numeri in un
  range sano.

## I moltiplicatori nei modelli non lineari

Per QP/NLP convessi i moltiplicatori (`Pi` sui vincoli lineari, condizioni KKT in generale)
hanno la stessa lettura marginale dei prezzi ombra. Verifica numerica consigliata nel
laboratorio: perturbare il termine noto di ε e ricontrollare che
`nuovo_ottimo ≈ vecchio_ottimo + Pi·ε`.


## Perché un solver solo

Stessa sintassi, stessa checklist di interpretazione e — soprattutto — ottimo
**globale certificato** anche nei problemi non convessi: con un solver locale ogni
risultato andrebbe accompagnato dalla domanda «è solo un ottimo locale?». I
problemi convessi con sola struttura quadratica o conica (vincoli come
`dx² + dy² ≤ d²`) non richiedono nulla di speciale.
