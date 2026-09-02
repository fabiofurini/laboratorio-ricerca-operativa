# Stile e formato del materiale didattico — riferimento permanente

Questo file memorizza le convenzioni di stile e di formato scelte da Fabio Furini per
tutto il materiale del Laboratorio di Ricerca Operativa (dispensa, slide, sito,
soluzioni). **Chi estende il materiale — umano o LLM — deve leggerlo prima di
scrivere qualunque cosa e attenersi a queste regole.** Gli esempi di riferimento del
formato dei modelli sono in `ESEMPI_FORMATO_MODELLI/` (EX_1 … EX_5).

---

## 1. Notazione matematica

- **Scalari e indici**: minuscoli in corsivo ($x_{it}$, $b_t$, $\lambda$, $i$, $t$).
- **Insiemi di oggetti numerati**: gli oggetti (prodotti, canali, titoli, veicoli,
  scenari…) si indicano con i **numeri**, mai con lettere (prodotto 1, 2, 3 — NON
  A, B, C), e gli indici corrono su insiemi **enumerati esplicitamente**:
  `i \in \{1, 2, \dots, n\}` — così la notazione del testo è già quella del modello.
  Le sommatorie hanno sempre gli estremi espliciti: `\sum_{i=1}^{n}`.
- **Conteggi**: interi positivi, `n \in \Z_{\ge 1}`.
- **Dati numerici**: razionali, `\Q_{>0}` / `\Q_{\ge 0}` (macro `\Q`, `\Z`, `\R` nel
  preambolo).
- **Vettori**: minuscoli in grassetto (`\vet x`); **matrici**: maiuscole in
  grassetto (`\mat Q`); notazione matriciale **il meno possibile** (preferire le
  componenti e le sommatorie).
- **Grafi**: $G=(N,A)$, unico caso di insiemi non enumerati.
- Eccezioni dichiarate (aderenza alla letteratura): variabili aleatorie maiuscole
  ($D$, $L$) con realizzazioni minuscole ($d_s$, $\ell_s$); $F$ = funzione di
  ripartizione; $C$ della SVM.
- **Ogni coefficiente e ogni insieme è definito PRIMA di essere usato.**

## 2. Formato dei modelli (il "formato LP" degli esempi EX_1–EX_5)

Sequenza obbligatoria:

1. **Problema a parole** (decisione, obiettivo, vincoli in linguaggio naturale).
2. **Dati (input del modello)**: tabella `Simbolo | Tipo | Significato` — tipo
   esplicito per ogni dato ($\in \Q_{\ge 0}$, $\in \{0,1\}$, $\in \Z_{\ge 1}$…).
3. **Introduzione delle variabili**, prima del modello, con il conteggio:
   «Introduciamo le seguenti $3\,n$ variabili non negative:» seguito da un blocco
   `cases` se le variabili sono due o più (per UNA sola variabile: equazione
   semplice senza graffa) e chiuso dal quantificatore:
   ```latex
   $$\begin{cases}
   x_i = \text{litri del prodotto } i \text{ non trattati al giorno}\\[1ex]
   y_i = \dots
   \end{cases} \qquad \forall i \in \{1, 2, \dots, n\}.$$
   ```
4. **Il modello**, in un box tcolorbox **verde**
   (`colback=green!7!white, colframe=green!55!black` — ambiente `modello` del
   preambolo), con `subequations` + `align`:
   - **ogni riga numerata** con `\label{...}`: obiettivo e ciascuna famiglia di
     vincoli, **compresi i vincoli di non negatività** (che chiudono il modello e
     "definiscono le variabili");
   - struttura di riga (SENZA `&&` iniziale, altrimenti il lato sinistro finisce
     in una colonna allineata a sinistra e i versi non si incolonnano):
     `lhs &\le rhs, & \forall i \in \{1,\dots,n\}, \label{...} \\[1ex]`
     — il lato sinistro è right-aligned, quindi i **versi** (`=`, `\le`, `\ge`)
     cadono tutti nella stessa colonna (verificare con
     `pdftotext -bbox`: gli xMin dei simboli devono coincidere);
     obiettivo: `\min ~~ \sum ... & & \label{obj} \\[1ex]`;
     primo vincolo: `\text{soggetto a} \quad lhs &\le rhs, & ...`;
   - la dicitura è sempre **«soggetto a»** (`\text{soggetto a}`), MAI "s.t.";
   - **punteggiatura**: virgola alla fine di ogni riga del modello, punto fermo
     sull'ultima; virgola prima di ogni quantificatore;
   - etichette uniche per capitolo (es. `eq:p-obj`, `eq:p-cap`);
   - ATTENZIONE all'allineamento delle colonne dell'`align`.
5. **Descrizione puntata** subito dopo il modello (ambiente `spiegazione`):
   - «la funzione obiettivo (lineare/quadratica/…)~\eqref{obj} massimizza/minimizza …;»
   - per ogni famiglia: «i vincoli lineari~\eqref{consX} assicurano che …
     (**$n\,m$ vincoli lineari**);» — sempre con il **conteggio dei vincoli**;
   - ultima voce: «i vincoli~\eqref{consN} definiscono le variabili del modello.»

## 3. Struttura di ogni capitolo (8 passi)

1. Motivazione gestionale + introduzione che inquadra il problema + «In questo
   capitolo impareremo a: (1)… (4)»;
2. «Il problema a parole» (decisione/obiettivo/vincoli) e costruzione guidata
   (dati → variabili → modello → descrizione, come in §2);
3. Esempio numerico **svolto a mano** con tutti i passaggi;
4. Caso di studio con dati CSV;
5. Implementazione (codice mostrato e spiegato);
6. Risultati (output trascritto FEDELMENTE dagli script) e figure;
7. Analisi di sensitività (protocollo: base → one-at-a-time → prezzi ombra
   verificati per perturbazione → scenari → trade-off → stabilità);
8. Esercizi (con soluzioni nel fascicolo separato `soluzioni/`).

## 4. Regole ferree sui numeri

- **Nessun numero inventato**: ogni valore citato proviene da uno script eseguito
  (cartella `python/`); i numeri delle soluzioni degli esercizi sono verificati da
  `python/soluzioni_calcoli.py`.
- Se si cambiano dati o modelli: rieseguire `python3 python/esegui_tutti.py`,
  aggiornare i numeri trascritti in .tex/.md, ricompilare.
- Gli acronimi si introducono al primo uso; il documento è self-contained (nessun
  riferimento a materiali esterni o "documenti originali").

## 5. Figure

- Nella dispensa: **pgfplots/TikZ** che leggono i CSV di `dispensa/figure/dat/`
  (generati dagli script) — modificabili in LaTeX; i diagrammi complessi (reti,
  mappe) sono TikZ generati dagli script in `dispensa/figure/*.tex`.
- **Caption numerata sempre presente** che descrive che cosa è raffigurato.
- **Legende FUORI dal grafico** (sotto, centrate — stile `lab` nel preambolo).
- Palette: blunotte `#16324A`, teal `#0E7490`, rossomattone, verde, arancio,
  grigiomedio, viola, ocra (definite in `preambolo.tex` e `python/stile.py`).
- Controllo finale obbligatorio: **zero Overfull** (`grep Overfull *.log`) e
  **ispezione visiva** delle pagine con figure (nessuna sovrapposizione).

## 6. Documenti e dove vivono

| Materiale | Percorso | Pubblico? |
|---|---|---|
| Dispensa LaTeX | `dispensa/main.tex` | no (solo locale) |
| Slide del corso (beamer, 60 slide) | `slides/it/` | no |
| Soluzioni esercizi | `soluzioni/` | no |
| Sito = dispensa online (MkDocs Material) | `docs/` + `mkdocs.yml` | sì |
| Script e dati | `python/`, `dati/` | sì |
| Guida al solver | `GUIDA_GUROBI.md` | sì |
| PDF originali di partenza | `pdf_originali/` | no |

Repo: `github.com/fabiofurini/laboratorio-ricerca-operativa` (Pages attivo).
Il sito deve restare **navigabile** (tab, schede cliccabili in home, indice, una
sottopagina per argomento con il codice completo in blocco espandibile).

## 7. Lingua

Tutto in **italiano** (termini tecnici inglesi dove standard: LP, soft margin,
fill rate…). La traduzione inglese si farà **solo dopo la validazione** del
materiale italiano.
