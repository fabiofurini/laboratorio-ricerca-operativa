# Organizzazione del laboratorio

## Percorso essenziale in quattro laboratori

| | Contenuto | Obiettivi di apprendimento |
|---|---|---|
| **Lab 1** | Produzione e scorte | formulare un LP multiperiodale; leggere duali, slack e range; verificare un prezzo ombra per perturbazione |
| **Lab 2** | Markowitz | costruire un QP convesso; tracciare una frontiera; discutere la fragilità delle stime |
| **Lab 3** | Pricing *oppure* budget | modellare funzioni non lineari; studiare la concavità; verificare le KKT numericamente |
| **Lab 4** | Progetto a scelta | supply chain, ricarica EV, localizzazione, code, Newsvendor, CVaR o SVM; presentazione manageriale |

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
python3 -m pip install gurobipy matplotlib pandas scipy   # scipy: solo funzioni statistiche
python3 python/esegui_tutti.py       # rigenera dati, risultati e figure
```

Le slide del corso e le soluzioni degli esercizi vengono distribuite a lezione.
