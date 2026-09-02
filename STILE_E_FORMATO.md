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
  scenari…) si indicano con i **numeri**, mai con lettere — nemmeno come pedici: $x_1, x_2$, MAI $x_A, x_B$ (prodotto 1, 2, 3 — NON
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
- **Indici**: quando possibile $i$ per le righe (vincoli, osservazioni) e $j$ per
  le colonne (variabili, caratteristiche): $a_{ij}$.
- **Notazione allineata alle dispense LP di Fabio (cartella 3_LINEAR_PROGRAMMING)**:
  coppia canonica con PRIMALE = MAX (vincoli ≤, x ≥ 0) e duale = min; forma
  generale con insiemi DESCRITTIVI M_≤, M_=, M_≥ e N_{≥0}, N_{≷0}, N_{≤0};
  variabili duali π_i (mai y); costi ridotti c̄_j (la barra è parte del nome);
  scarti s_i; le variabili INCOGNITE si scrivono lisce (x_j, π_i): BARRA solo sui
  valori di una soluzione ammissibile (x̄_j, s̄_i), TILDE solo su quelli di una
  soluzione ottima (x̃, z̃, π̃), MAI l'asterisco; intervalli di validità formali [b_i^min, b_i^max] (termine
  noto) e [c_j^min, c_j^max] (coefficiente).
- **Struttura dei capitoli 2 e 3**: due sottocapitoli (\section) ciascuno —
  cap. 2: «Teoria della programmazione lineare» e «Teoria dell'ottimizzazione non
  lineare» (+ protocollo di sensitività); cap. 3: «Implementazione dei modelli
  lineari» e «Implementazione dei modelli non lineari». Sul sito le pagine sono
  divise allo stesso modo: teoria-lp, teoria-non-lineare, solver-lp,
  solver-non-lineare (GUIDA_GUROBI.md resta intera come file autonomo).
- **Capitolo 2 (richiami) = solo teoria**: NIENTE notazione del solver (Pi, RC,
  SARHS, SAObj, Gurobi); si scrive «risolvendo si ottiene». Il ponte
  teoria ↔ attributi (π̃ ↔ Pi, c̄ ↔ RC, s̄ ↔ Slack, intervalli ↔ SARHS/SAObj) sta
  nel capitolo 3, in una tabella dedicata.
- **Insiemi per enumerazione**: sempre DUE valori iniziali, i puntini, l'ultimo
  valore: $\{1, 2, \dots, n\}$ — mai $\{1, \dots, n\}$.
- **Trasposto**: con l'apice, $\vet x'$ (macro `\T`), MAI $^T$ o $^\top$.
- **Variabile libera**: si scrive con il simbolo $\gtreqless 0$ (es.
  `y_i &\gtreqless 0,` nel modello), mai la parola "libera" dentro il modello.
- **Coppia primale-duale canonica**: forma generale con TUTTI i versi dei vincoli
  ($\ge$, $=$, $\le$, insiemi $M_1, M_2, M_3$ che ripartiscono $M$) e TUTTI i
  segni delle variabili ($\ge 0$, $\gtreqless 0$, $\le 0$, insiemi $N_1, N_2,
  N_3$ che ripartiscono $N$); le sommatorie usano gli insiemi ($\sum_{j \in N}$),
  e dopo il box la tabella delle regole di conversione primale/duale.
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
3bis. **Colori dei box** (devono restare ben distinti): modello = VERDE
   (green!7/green!55!black); esempio svolto = AZZURRO (teal!6/teal); spiegazione =
   grigio; insight = blu notte chiaro con barra a sinistra; attenzione = giallo;
   esercizio = bianco con cornice blu notte.

4. **Il modello**, in un box tcolorbox **verde**
   (`colback=green!7!white, colframe=green!55!black` — ambiente `modello` del
   preambolo), con `subequations` + `align`:
   - **ogni riga numerata** con `\label{...}`: obiettivo e ciascuna famiglia di
     vincoli, **compresi i vincoli di non negatività** (che chiudono il modello e
     "definiscono le variabili");
   - struttura di riga (SENZA `&&` iniziale, altrimenti il lato sinistro finisce
     in una colonna allineata a sinistra e i versi non si incolonnano):
     `lhs &\le rhs, & \forall i \in \{1, 2, \dots, n\}, \label{...} \\[1ex]`
     — il lato sinistro è right-aligned, quindi i **versi** (`=`, `\le`, `\ge`)
     cadono tutti nella stessa colonna (verificare con
     `pdftotext -bbox`: gli xMin dei simboli devono coincidere);
     obiettivo: `\min ~~ \sum ... & & \label{obj} \\[1ex]`;
     primo vincolo: `\text{soggetto a} \quad lhs &\le rhs, & ...`;
   - la dicitura è sempre **«soggetto a»** (`\text{soggetto a}`), MAI "s.t.";
   - **punteggiatura**: virgola SEMPRE dopo il termine noto (RHS) di ogni
     vincolo, punto fermo sull'ultima riga; virgola prima di ogni quantificatore;
   - etichette uniche per capitolo (es. `eq:p-obj`, `eq:p-cap`);
   - ATTENZIONE all'allineamento delle colonne dell'`align`.
4bis. **Modelli numerici (di istanza)**: layout a coefficienti staccati, una
   colonna per variabile, con verso e termine noto incolonnati (stile EX_1),
   virgola dopo ogni RHS:
   ```latex
   \[
   \begin{array}{r r@{\;}c@{\;}r c r l}
   \max & 30\,x_1 & + & 50\,x_2 & & & \\
   \text{soggetto a} & x_1 & + & 3\,x_2 & \le & 90, & \text{(ore)}\\
    & 2\,x_1 & + & x_2 & \le & 80, & \text{(kg)}\\
    & x_1, & & x_2 & \ge & 0. &
   \end{array}
   \]
   ```

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
3. Esempio numerico **svolto a mano** con tutti i passaggi — i passi («Passo 1»,
   «Passo 2», …) sempre come voci di un `itemize`, MAI come paragrafi sciolti;
4. Caso di studio con dati CSV;
5. Implementazione (codice mostrato e spiegato);
6. Risultati (output trascritto FEDELMENTE dagli script) e figure;
7. Analisi di sensitività (protocollo: base → one-at-a-time → prezzi ombra
   verificati per perturbazione → scenari → trade-off → stabilità);
8. Esercizi (con soluzioni nel fascicolo separato `soluzioni/`).

### Ordine espositivo e analisi

- **Prima le definizioni, poi gli esempi**: un esempio non usa mai un concetto
  (prezzo ombra, costo ridotto, ...) definito solo più avanti.
- **I dati prima del modello, sempre**: anche per la coppia primale-duale il
  paragrafo che definisce dati e variabili PRECEDE il box del modello.
- **Niente riferimenti in avanti** nel corpo del documento (\ref a capitoli o
  sezioni successivi): l'unica mappa in avanti è la tabella-indice del capitolo 1.
- **Eccezioni di notazione dichiarate al primo uso** (es. la variabile aleatoria
  D maiuscola, il parametro C della SVM), mai elencate in blocco all'inizio.
- **Range di validità citati SEMPRE**: `SARHSLow/Up` accanto a ogni prezzo ombra
  e `SAObjLow/Up` accanto a ogni costo ridotto (per una variabile a zero la
  soglia di convenienza è proprio `SAObjLow` nei problemi di minimo, `SAObjUp`
  nei problemi di massimo).
- **Capitoli 2 (richiami) e 3 (solver): esempi GENERICI.** Niente storie o unità
  reali (ore, kg, prodotti, impianti, €): solo variabili, vincoli, "risorsa 1",
  coefficienti e termini noti. Le applicazioni concrete arrivano nei capitoli
  successivi. Gli esempi canonici, che coprono tutti i casi che si rivedranno:
  LP 2×2 (max, dualità, prezzi ombra, costi ridotti con la terza variabile);
  LP "tutti i casi" (min 5x1+8x2−9x3 con vincoli GENERICI a più variabili
  x1+x2 ≥ 30, x1+x2−x3 = 100, x1−2x2 ≤ −20 e variabili ≥0 / libera / ≤0:
  z* = 620, Pi = (0, 6, −1), RC = (0, 0, −3), SAObjUp3 = −6); QP
  (min x1²+2x2², x1+x2 ≥ 6) su cui si calcolano anche le KKT.
- **Niente commenti tra parentesi accanto ai vincoli** nei modelli dei richiami;
  i vincoli su singola variabile che sembrano bound si evitano: meglio vincoli
  generici a più variabili.
- **Nei valori dal solver scrivere `Pi = (...)`, mai `y = Pi = (...)`**: i
  simboli matematici (y, lambda) si usano nelle verifiche a mano, gli attributi
  (`Pi`, `RC`) quando si riporta l'output del solver; e MAI il simbolo
  matematico e l'attributo nella stessa frase — l'attributo si nomina dopo, in
  una frase separata ("In Gurobi si legge dall'attributo Pi") e i valori del solver si
  riportano SENZA calcoli (z* = 1900, non z* = 30·30 + 50·20 = 1900): i conti
  stanno solo nei passi di verifica.
- **I segni dei prezzi ombra si spiegano col ragionamento in due domande**
  (aumentare b allarga/restringe la regione? una regione più ampia non peggiora
  mai l'ottimo) e con la tabella verso × min/max.
- **I calcoli e i valori si mostrano come formule centrate** (\[...\]), mai
  incorporati nel testo; il Passo 1 di ogni esempio elenca TUTTI i valori dati
  dal solver (x, z*, Pi, RC, range), i passi successivi li verificano.
- **Pattern espositivo degli esempi**: "i valori li dà il solver, poi si fanno i
  conti per verificare le proprietà" (A'y = c in base, dualità forte, regole dei
  segni, formula dei costi ridotti, perturbazioni). MAI la soluzione
  grafica/algebrica del primale.
- **Degenerazione**: ricordare sempre che può esistere una variabile in base a
  valore zero (RC = 0 non implica che la variabile sia usata).

### Un solver solo: Gurobi

- TUTTA l'ottimizzazione usa Gurobi, MAI `scipy.optimize` o altri solver locali
  (`scipy.stats` per le funzioni statistiche è ammesso).
- NLP generali: vincoli funzionali `addGenConstrLog/Exp/Pow` con
  `FuncNonlinear = 1`; termini bilineari/rapporti con variabile ausiliaria e
  `NonConvex = 2` (es. `w·(mu - lam) = 1`); distanze euclidee con vincoli conici
  `dx² + dy² ≤ d²` (Weber, minimax).
- Per analisi marginali accurate: `MIPGap`, `FeasibilityTol`, `OptimalityTol`
  a 1e-9; riformulare per la scalatura (es. `q·p^eps ≤ A`, non `q ≤ A·p^-eps`).
- Ogni riscrittura di solver va verificata confrontando l'output col precedente
  (diff dei numeri stampati).
- **Analisi di sensitività degli LP**: oltre ai prezzi ombra (`Pi` + intervallo
  `SARHSLow/Up`), leggere SEMPRE anche i **costi ridotti** (`v.RC`) delle variabili
  a zero, con interpretazione manageriale: la soglia di convenienza oltre la quale
  la variabile entrerebbe in soluzione (es. "la rotta entra solo se il costo scende
  sotto 7 − 2 = 5 €/unità"). Nell'esempio 2×2 dei richiami: prodotto 3 con RC = −2,
  soglia 22 €, controprova con margine 23 → piano (0, 5, 75), valore 1975 €.

## 4. Regole ferree sui numeri

- **Nessun numero inventato**: ogni valore citato proviene da uno script eseguito
  (cartella `python/`); i numeri delle soluzioni degli esercizi sono verificati da
  `python/soluzioni_calcoli.py`.
- Se si cambiano dati o modelli: rieseguire `python3 python/esegui_tutti.py`,
  aggiornare i numeri trascritti in .tex/.md, ricompilare.
- Gli acronimi si introducono al primo uso; il documento è self-contained (nessun
  riferimento a materiali esterni o "documenti originali").

### Slide (beamer)

- Mai comprimere: **dare spazio** a formule e testo, un vincolo per riga anche nei
  modelli delle slide; se un frame è troppo pieno (Overfull \vbox), DIVIDERLO in
  due frame, non rimpicciolire.
- Elenchi puntati al posto dei paragrafi lunghi.
- Controllare `Overfull` (hbox E vbox) nel log a ogni modifica; attenzione ai
  grafici pgfplots dentro le colonne (le etichette dell'asse y sporgono: usare
  width=0.92\textwidth della colonna).

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
