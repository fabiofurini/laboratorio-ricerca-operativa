# Piano di lavoro — Dispensa unica del Laboratorio di Ricerca Operativa

**Obiettivo:** trasformare i 4 PDF esistenti in un'unica dispensa LaTeX didattica, completa e
autosufficiente, che sia la base concreta del laboratorio del prossimo anno, con **tutti i modelli
implementati in Python/Gurobi**, dati realistici, esempi numerici svolti, casi di studio, analisi
di sensitività e figure generate dal codice.

**Fonti (4 PDF):**
1. `modelli_laboratorio_ricerca_operativa.pdf` — 8 modelli continui deterministici (LP/QP/NLP)
2. `newsvendor_modello_e_varianti.pdf` — newsvendor e varianti (stocastico)
3. `var_cvar_modelli_lineari_e_applicazioni.pdf` — VaR/CVaR e applicazioni
4. `support_vector_machine_modelli_e_applicazioni.pdf` — SVM, SVR, One-Class

---

## Struttura dei file prodotti

```
LABORATORIO/
├── PIANO_DI_LAVORO.md            ← questo file
├── GUIDA_GUROBI.md               ← guida autonoma al solver: costruire il modello,
│                                    farlo girare, recuperare la soluzione, interpretare l'output
├── dispensa/
│   ├── main.tex                  ← documento principale (book, italiano)
│   ├── preambolo.tex             ← pacchetti, box didattici, stile listing
│   ├── capitoli/
│   │   ├── cap01_introduzione.tex
│   │   ├── cap02_richiami.tex         (LP, QP, NLP, dualità, KKT, sensitività)
│   │   ├── cap03_python_gurobi.tex    (anatomia di un modello, guida pratica)
│   │   ├── cap04_produzione.tex       (Modello 1  — LP/QP)
│   │   ├── cap05_supplychain.tex      (Modello 2  — LP/NLP)
│   │   ├── cap06_markowitz.tex        (Modello 3  — QP)
│   │   ├── cap07_pricing.tex          (Modello 4  — NLP)
│   │   ├── cap08_budget.tex           (Modello 5  — NLP convesso)
│   │   ├── cap09_localizzazione.tex   (Modello 6  — NLP convesso)
│   │   ├── cap10_ricarica_ev.tex      (Modello 7  — LP/QP)
│   │   ├── cap11_code.tex             (Modello 8  — NLP convesso, M/M/1)
│   │   ├── cap12_newsvendor.tex       (PDF 2 completo)
│   │   ├── cap13_var_cvar.tex         (PDF 3 completo)
│   │   ├── cap14_svm.tex              (PDF 4 completo)
│   │   └── cap15_organizzazione.tex   (4 laboratori, valutazione, template report)
│   └── figure/                   ← PDF generati dagli script Python
├── python/
│   ├── stile.py                  ← stile comune dei grafici + utilità
│   ├── lab04_produzione.py
│   ├── lab05_supplychain.py
│   ├── lab06_markowitz.py
│   ├── lab07_pricing.py
│   ├── lab08_budget.py
│   ├── lab09_localizzazione.py
│   ├── lab10_ricarica_ev.py
│   ├── lab11_code.py
│   ├── lab12_newsvendor.py
│   ├── lab13_var_cvar.py
│   ├── lab14_svm.py
│   └── esegui_tutti.py           ← esegue tutti gli script in sequenza
└── dati/                         ← CSV dei casi di studio (generati e riutilizzabili)
```

---

## Impostazione didattica (richiesta esplicita: “versione didattica con esempi e spiegazioni”)

Ogni capitolo applicativo segue **sempre la stessa scaletta in 8 passi**:

1. **Motivazione gestionale** — il problema raccontato come decisione aziendale.
2. **Costruzione guidata del modello** — insiemi, parametri, variabili, vincoli, obiettivo,
   ciascuno spiegato riga per riga (perché il vincolo è scritto così, cosa succede se lo tolgo).
3. **Esempio numerico svolto a mano** — istanza minuscola (2–3 variabili) risolta passo-passo
   con tutti i passaggi algebrici, per capire il meccanismo prima del solver.
4. **Caso di studio** — istanza realistica con dati in CSV, descritta e commentata.
5. **Implementazione Python/Gurobi** — codice completo mostrato e spiegato blocco per blocco.
6. **Risultati e figure** — output del solver interpretato in linguaggio manageriale.
7. **Analisi di sensitività** — prezzi ombra, costi ridotti, scenari, trade-off, con figure.
8. **Esercizi proposti** — 4–6 esercizi graduati (verifica, variante, estensione, discussione).

Box didattici colorati usati ovunque (tcolorbox):
- **Modello** (blu) — formulazione matematica completa
- **Spiegazione** (grigio) — lettura riga per riga
- **Esempio svolto** (verde) — calcoli a mano completi di ogni passaggio
- **Insight manageriale** (azzurro) — cosa dice il modello a un decisore
- **Attenzione** (giallo) — errori tipici e trappole modellistiche
- **Esercizio** (bordo) — attività per lo studente

---

## Passi operativi dettagliati (eseguiti in sequenza)

### FASE 0 — Ambiente  ✅
- [x] Lettura integrale dei 4 PDF
- [x] Installazione `gurobipy` 13.0.3, `matplotlib`, `pandas` (licenza pip fino a 2000 var/vincoli)
- [x] Verifica pdflatex + tcolorbox/listings/booktabs

### FASE 1 — Infrastruttura
- [x] 1.0 `GUIDA_GUROBI.md`: guida autonoma e completa al solver — installazione e licenza;
      come si costruisce un modello (Model, addVars, addConstrs, setObjective, passo per passo
      su un esempio completo); come si fa girare (`optimize`, parametri, log spiegato riga per
      riga); come si recupera la soluzione (`Status`, `ObjVal`, `X`, `Pi`, `RC`, `Slack`,
      `SAObjLow/Up`, `SARHSLow/Up`); come si interpreta l'output (ottimo/inammissibile/illimitato,
      prezzi ombra, costi ridotti, range di validità); errori tipici e come diagnosticarli.
- [x] 1.1 Creare l'albero di cartelle `dispensa/`, `python/`, `dati/`
- [x] 1.2 `python/stile.py`: palette coerente con la dispensa, funzioni di salvataggio figure
- [x] 1.3 `dispensa/preambolo.tex`: pacchetti, definizione dei 6 box, stile codice Python
- [x] 1.4 `dispensa/main.tex`: frontespizio, indice, inclusione capitoli

### FASE 2 — Script Python (un modello alla volta: dati → modello → soluzione → sensitività → figure)
Ogni script: genera/salva i dati in `dati/*.csv`, costruisce il modello Gurobi (o scipy per gli
NLP generali), risolve, stampa un report, esegue la sensitività e salva le figure in
`dispensa/figure/` come PDF vettoriali.

- [x] 2.1 `lab04_produzione.py` — 3 prodotti × 6 mesi; LP costo minimo, duali della capacità,
      variante QP con smoothing (γ), scenario di domanda ±10%, figura: piano di produzione + scorte.
- [x] 2.2 `lab05_supplychain.py` — rete 2 stabilimenti/2 hub/4 mercati; flusso a costo minimo,
      congestione quadratica, prezzo CO₂ crescente; figure: rete e costi vs τ.
- [x] 2.3 `lab06_markowitz.py` — 8 titoli, 60 mesi di rendimenti simulati; minima varianza al
      variare di r̄ → frontiera efficiente; composizione del portafoglio; effetto limiti u_i.
- [x] 2.4 `lab07_pricing.py` — domanda lineare (QP esatto con Gurobi), elasticità costante e
      logistica (scipy); prezzo ottimo vs capacità K; valore marginale di un posto.
- [x] 2.5 `lab08_budget.py` — 4 canali con risposta log/esponenziale satura; KKT verificate
      numericamente (ritorno marginale uguale sui canali attivi); curva valore–budget.
- [x] 2.6 `lab09_localizzazione.py` — 12 quartieri pesati; Weber, minimax, baricentro,
      compromesso α; mappa con punti ottimi; distanza vs α.
- [x] 2.7 `lab10_ricarica_ev.py` — 6 veicoli × 24 ore, prezzi orari reali-stilizzati; costo minimo
      LP, peak shaving minimax, profilo regolare QP; confronto profili orari.
- [x] 2.8 `lab11_code.py` — M/M/1: costo totale convesso, μ* analitico vs numerico; curva
      costo-servizio; prezzo ombra del vincolo di attesa massima.
- [x] 2.9 `lab12_newsvendor.py` — quantile analitico (esempio del PDF: μ=100, σ=20, α*=0,6923),
      LP a scenari (dimostrare che coincide), multiprodotto con budget, service level,
      media-CVaR al variare di λ; valore della soluzione stocastica; figure costo/quantile/frontiera.
- [x] 2.10 `lab13_var_cvar.py` — esempio a 6 scenari del PDF (VaR=12, CVaR=18,67) verificato in
      Gurobi; portafoglio mean-CVaR con 300 scenari e confronto con Markowitz; frontiera
      rendimento-CVaR; supply chain a due stadi con scenari avversi.
- [x] 2.11 `lab14_svm.py` — dataset 2D "rischio di credito" simulato (80 clienti); hard margin QP,
      soft margin al variare di C, duale (support vector evidenziati), kernel RBF, classi
      sbilanciate con costi, SVR su domanda; figure: iperpiano, margine, frontiere non lineari.
- [x] 2.12 `esegui_tutti.py` + esecuzione completa e verifica di tutte le figure.

### FASE 3 — Capitoli LaTeX (scritti dopo i risultati numerici, così testo e numeri coincidono)
- [x] 3.1 cap01 Introduzione: obiettivi del laboratorio, filosofia (nessuna variabile binaria),
      mappa dei modelli, percorso in 4 laboratori, criteri di valutazione (30/25/25/20).
- [x] 3.2 cap02 Richiami: LP e dualità con esempio 2×2 svolto; QP e convessità; KKT con esempio
      svolto; il protocollo di sensitività in 6 passi (dal PDF 1, pagina 11).
- [x] 3.3 cap03 Python/Gurobi: installazione, anatomia di un modello (vars → constrs → obj →
      optimize → query), lettura di `Pi`, `RC`, `SAObjLow/Up`; scipy per NLP generali.
- [x] 3.4–3.11 cap04–cap11: gli 8 modelli del PDF 1 con la scaletta in 8 passi.
- [x] 3.12 cap12 Newsvendor (7 sezioni del PDF 2, tutte, in forma estesa e didattica).
- [x] 3.13 cap13 VaR/CVaR (7 sezioni del PDF 3, con dimostrazione guidata di Rockafellar–Uryasev).
- [x] 3.14 cap14 SVM (7 sezioni del PDF 4, con derivazione guidata del duale e kernel).
- [x] 3.15 cap15 Organizzazione: calendario 4 laboratori, consegne, rubrica di valutazione,
      template del report, domande d'esame tipiche.

### FASE 4bis — Riordino e sito GitHub
- [x] 4b.1 Riordinare la cartella: PDF originali in `pdf_originali/`, struttura pulita.
- [ ] 4b.2 Versione inglese — RINVIATA su richiesta: si traduce dopo la validazione
      del materiale italiano (dispensa, slide e sito).
- [x] 4b.3 Sito GitHub navigabile in ITALIANO: repo git con README, `docs/` in Markdown
      (un file per capitolo, figure PNG generate dagli script), `mkdocs.yml`
      (tema Material) + workflow GitHub Actions per Pages.

### FASE 4ter — Slide per l'insegnamento (richiesta aggiuntiva)
- [x] 4t.1 Slide beamer in italiano (`slides/it/slides_laboratorio.tex`): deck unico
      completo (60 slide) che copre TUTTO il materiale della dispensa, con sezioni
      per capitolo, stessi colori, stessi casi di studio e figure dagli stessi CSV.
- [ ] 4t.2 Slide beamer in inglese — RINVIATE: dopo la validazione dell'italiano.

### FASE 4quater — Soluzioni degli esercizi (richiesta aggiuntiva)
- [x] 4q.1 Fascicolo LaTeX separato `soluzioni/soluzioni.tex` con le soluzioni di tutti
      gli esercizi proposti, capitolo per capitolo; numeri verificati con
      `python/soluzioni_calcoli.py`.

### FASE 4 — Compilazione e controllo qualità
- [x] 4.1 Compilare con `latexmk -pdf` fino a zero errori; risolvere overfull/reference mancanti.
- [x] 4.2 Controllo incrociato: ogni numero citato nel testo = output degli script.
- [x] 4.3 Verifica finale: indice, figure, listings, esercizi numerati.
- [x] 4.4 Riepilogo finale a Fabio: cosa c'è, come ricompilare, come rieseguire gli script,
      come attivare la licenza accademica Gurobi completa.

---

## Scelte tecniche motivate

- **Solver:** Gurobi (`gurobipy` 13) per LP/QP/QP non convessi; `scipy.optimize` per gli NLP
  generali (Weber, logistica, M/M/1) — didatticamente utile mostrare entrambi gli strumenti.
- **Dimensioni istanze:** tutte sotto le 2000 variabili/vincoli → funzionano con la licenza pip;
  con la licenza accademica nulla cambia.
- **Riproducibilità:** seed fissi (`numpy.random.default_rng(42)`), dati salvati in CSV,
  figure rigenerabili con `python3 python/esegui_tutti.py`.
- **Lingua:** italiano (coerente con i PDF), termini tecnici inglesi dove standard.
- **Classe LaTeX:** `book` a capitoli, formato A4, colori sobri coerenti con i PDF originali
  (blu notte `#16324A`, teal `#0E7490`).
