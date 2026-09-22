# Project status

Reference document for the group. Where the project stands, what has been done, what remains.

---

## Current state

```
T-Box        21 classes, ~30 properties, restrictions and disjointness
A-Box        5 specimens of 5, GENERATED from the CSV
             1632 triples in the merged ontology
Annotation   5 specimens, 46 observations, 69 claims, 12 intervals
Queries      16 competency questions, 5 negative, all executed
Tests        21/21 passing
Probes       12/12, constraints verified rather than declared
Reasoner     HermiT: CONSISTENT
Round trip   CLEAN, the CSV loses no data triple
```

**Open decisions: none.** D1 to D7 are all closed.

---

## The five specimens

| specimen | site | sex | age | treponematosis hedge | mercury |
|---|---|---|---|---|---|
| St. Albani 89 | urban | probably female | adult | Possible | 374 ng/g, treated |
| St. Albani 90 | urban | male | 15 to 22.7 | **Probable** | 388 ng/g, treated |
| St. Albani 94 | urban | male | 35 to 45 | Possible | 390 ng/g, treated |
| Refshale 130 | rural | female | 24.7 to 46.4 | Possible | 22 ng/g, **denied** |
| Tirup 292 | rural | female | 20 to 24 | **Probable** | 25 ng/g, **denied** |

The hedge column is the project's main result. Two specimens reach "indicative of" or "regarded as diagnostic"; three stop at "consistent with". Certainty appears twice in the entire paper, and both times it attaches to a **date**, never to a diagnosis.

---

## Working cycle

```
1. edit a file in data/csv/
2. python3 tools/build.py
3. python3 run_tests.py  &&  python3 run_probes.py
```

Terms are curated by hand in `data/vocabulary.ttl`. Claims are annotated in the CSV. Two different jobs, two different files.

---

## What remains

### Required

**1. The RML mapping.** `data/mapping.rml.ttl`, producing `data/abox_generated.ttl`. This is the extraction half of Knowledge Representation **and** Extraction, and many projects submit only the first half.

It is no longer a risk. The CSV to A-Box pipeline already works in Python, the tests pass and the round trip is clean, so RML is a presentation upgrade rather than a dependency. If it turns out to be painful, submit with the script and say so.

`tools/csv_to_ttl.py` doubles as the **specification and the test oracle**: the RML output must match its output. The mapping is not written blind, and you know immediately when it is right.

**2. Documentation and publication.** README (done), design decisions (done), a Graffoo diagram of the model, LODE-generated documentation, GitHub Pages. Keep the process diagram separate from the model diagram.

**3. Run HermiT yourselves** in Protégé. Do not take the recorded result on trust. See `docs/REASONER.md`.

### Small, worth doing if time allows

- Three `skos:closeMatch` alignments to verify and, if the definitions match, promote to `skos:exactMatch`: venereal syphilis against MONDO's syphilis, Paget's disease of bone against MONDO's Paget's disease, the parietal bone against its NCIT term.
- Three bones still without a UBERON identifier: frontal, nasal aperture, orbit.
- Repository housekeeping: git, licence, folder structure.

---

## Two discrepancies left visible

Neither has been tidied away, and both belong in the report.

**Refshale 130.** The paper states this is the one specimen whose radiocarbon age agrees completely with the archaeological date. Taken literally the intervals conflict, and the strict CQ4b reports a disagreement. Applying the paper's **own** stated precision of +/- 30 years to the paper's **own** 95 per cent range resolves it, and the tolerant query then returns exactly the two specimens the paper treats as discordant. See D7.

**St. Albani 94.** The body text dates the burial to AD 1250 to 1400 by arm position; Table 2 records 1250 to 1350 for the same burial. The body value is modelled and the difference is recorded in the row's label.

The numbers were not adjusted to make the queries agree with the prose. A model that holds the tabulated values and the claims side by side, and lets the discrepancy surface, is doing what the project set out to do.

---

## Standing rules

> **Everything the thesis promises must exist at least once. Nothing needs to exist a hundred times.** Gaps in coverage are expected and defensible. A gap between what is claimed and what the model does is fatal.

> **Every class must earn its place.** If no query binds a variable to a class, that class is not needed.

> **The T-Box must not name the source.** If replacing the article with another palaeopathology paper would require rewriting the T-Box, the result is a structured summary, not an ontology.

> **An explained inconsistency is worth more than a consistency obtained by accident.**
