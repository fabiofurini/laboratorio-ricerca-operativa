# Organizzazione del laboratorio

## Percorso essenziale in quattro laboratori

| | Contenuto | Obiettivi di apprendimento |
|---|---|---|
| **Lab 1** | Produzione e scorte | formulare un LP multiperiodale; leggere duali, slack e range; verificare un prezzo ombra per perturbazione |
| **Lab 2** | Markowitz | costruire un QP convesso; tracciare una frontiera; discutere la fragilità delle stime |
| **Lab 3** | Pricing *oppure* budget | modellare funzioni non lineari; studiare la concavità; verificare le KKT numericamente |
| **Lab 4** | Progetto a scelta | supply chain, ricarica EV, localizzazione, code, Newsvendor, CVaR o SVM; presentazione manageriale |

## Struttura della consegna (report, max 8 pagine)

1. **Problema e ipotesi** — contesto e semplificazioni dichiarate;
2. **Modello** — dati, variabili, vincoli e obiettivo, ciascuno spiegato;
3. **Dati** — origine, unità di misura, generazione;
4. **Risultati** — valore ottimo, decisioni, vincoli attivi;
5. **Sensitività** — il protocollo completo in sei passi;
6. **Raccomandazione manageriale** — massimo dieci righe, senza formule.

## Criteri di valutazione

| Dimensione | Peso |
|---|---|
| Correttezza della formulazione | 30% |
| Implementazione e verifica numerica | 25% |
| Analisi di sensitività | 25% |
| Interpretazione e comunicazione | 20% |

## Domande tipiche di discussione

- Quale risorsa conviene aumentare per prima, e quanto si può pagare per essa?
- Qual è il costo di una promessa di servizio più ambiziosa?
- La soluzione resta credibile se i dati cambiano del 5%?
- Quale punto della frontiera consigliereste a un decisore, e perché?
- Che cosa NON dice il modello?

## Gli errori più comuni

1. Leggere `.X` o `.Pi` senza controllare `m.Status`.
2. Dimenticare `lb=-GRB.INFINITY` sulle variabili libere ($b$ della SVM, $\eta$ del CVaR).
3. Usare un prezzo ombra fuori dal suo intervallo di validità.
4. Sbagliare il segno dei duali nei problemi di minimo.
5. Aggiornare il RHS di un vincolo con costanti a sinistra.
6. Ottimizzare un solo obiettivo quando ce ne sono due (minimax puro).
7. Scegliere gli iperparametri guardando il test set.
8. Riportare sei cifre decimali da stime che ballano alla seconda.

## Riproducibilità

```bash
python3 -m pip install gurobipy matplotlib pandas scipy
python3 python/esegui_tutti.py
latexmk -pdf dispensa/main.tex
latexmk -pdf soluzioni/soluzioni.tex      # per i docenti
latexmk -pdf slides/it/slides_laboratorio.tex
```
