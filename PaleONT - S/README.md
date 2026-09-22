# PaleONT

An ontology of palaeopathological claims.

PaleONT does not model the diseases of the people buried in medieval Danish cemeteries. It models what someone **said** about them: who said it, on the basis of which observation, with which instrument, within which framework of thought, and with how much stated confidence.

**Source.** Schwarz S., Skytte L., Rasmussen K.L., *Pre-Columbian treponemal infection in Denmark? A paleopathological and archaeometric approach*, Heritage Science 2013, 1:19. doi:10.1186/2050-7445-1-19, CC BY 2.0.

Course project for Knowledge Representation and Extraction (KRKE), DHDK, University of Bologna.

---

## The thesis

> **There is no view from nowhere.** Every assertion carries with it who made it, with which instrument, and under which assumptions. Disagreement is not the finding. It is the symptom that makes the standpoint visible.

### What this project does not claim

It does not set out to show that palaeopathologists contradict one another. That would be debunking, and a weaker result. Where two claims diverge, the divergence is not the conclusion: it is the evidence that a standpoint was there all along.

The difference is practical, not rhetorical. It is why the model records the correction applied to a dating (without it, an explained difference looks like a contradiction), and why `po:rejects` has range `po:Claim` and not `po:Condition` (you refuse an assertion, not a disease).

### The result, in one table

The same condition, the same study, the same techniques, five skeletons:

| specimen | hedge | the source's own words |
|---|---|---|
| Refshale 130 | Possible | "lesions consistent with treponemal disease are found on several long bones" |
| St. Albani 89 | Possible | as above |
| St. Albani 94 | Possible | "only meet the descriptions of Hackett's on-trial criteria" |
| St. Albani 90 | Probable | "only those in skeleton 90 are **indicative of** treponemal infection" |
| Tirup 292 | Probable | "regarded as **diagnostic** for treponemal disease" |

Certainty appears twice in the whole paper, and both times it is granted to a **date**, never to a diagnosis. That is a query result, not an opinion, and anyone can re-run it.

---

## Quick start

```bash
pip install rdflib owlrl
python3 tools/build.py        # CSV  ->  A-Box  ->  merged ontology
python3 run_tests.py          # 21 unit tests
python3 run_probes.py         # 12 deliberate errors
```

To inspect the ontology in Protégé, open `ontology/paleont_merged.owl`. See `docs/REASONER.md`.

---

## What is in the repository

```
SOURCE FILES, edited by hand
  ontology/paleont.ttl         the T-Box
  data/vocabulary.ttl          controlled terms with their alignments
  data/csv/specimens.csv       \
  data/csv/observations.csv     |  the annotation tables
  data/csv/claims.csv           |  this is where daily work happens
  data/csv/intervals.csv       /
  queries/*.rq                 the competency questions
  queries/negative/*.rq        the negative competency questions

GENERATED, never edited
  data/abox_generated.ttl      the A-Box
  ontology/paleont_merged.ttl  T-Box plus A-Box
  ontology/paleont_merged.owl  the same, for Protégé

TOOLS
  tools/build.py               the single command
  tools/csv_to_ttl.py          the mapping, in Python
  tools/roundtrip_check.py     proof that the CSV schema loses nothing
  tools/ttl_to_csv.py          the initial export, run once
  run_tests.py                 competency question suite
  run_probes.py                constraint verification

DOCUMENTATION
  docs/DESIGN_DECISIONS.md     the seven decisions and why
  docs/PROPERTIES.md           full property specification
  docs/ANNOTATION_GUIDE.md     how to fill the tables
  docs/TURTLE_GUIDE.md         how to read and write the Turtle
  docs/REASONER.md             running HermiT, and what it caught
  docs/PROJECT_STATUS.md       current state and what remains
```

**Working cycle.** Edit a CSV, run `tools/build.py`, run the two test scripts. Terms are curated by hand in `vocabulary.ttl`; claims are annotated in the CSV. Two different jobs, two different files.

---

## The model in one picture

```
   LAYER 0                              LAYER 1
 +--------------+                    +--------------+
 | Observation  | <--- groundedIn ---|    Claim     |
 +------+-------+                    +------+-------+
        | observedOn                        | aboutSpecimen
        v                                   v
   +----------+                        +----------+
   | Specimen |                        | Specimen |
   +----------+                        +----------+
```

The specimen is reached twice and no arrow ever leaves it. A specimen says nothing. It is spoken about.

`po:groundedIn` is the only bridge between evidence and interpretation. To get from a set of remains to a disease you must climb through a claim, and climbing through it means carrying the agent, the framework and the hedge with you.

There are four layers:

| layer | class | holds |
|---|---|---|
| 0, evidence | `po:Observation` | what was seen or measured, with which technique, on which bone |
| 1, interpretation | `po:DiagnosticClaim` and its siblings | what someone inferred from layer 0 |
| 2, meta | `po:MethodologicalClaim` | what a technique can or cannot establish |
| 3, adjudication | `po:RejectionClaim`, `cito:*` | a claim about another claim |

Layer 2 is recognised by an absence: a methodological claim **cannot** carry `po:aboutSpecimen`, and a cardinality restriction enforces it. That absence is how the model distinguishes "this individual had leprosy" from "this method cannot tell leprosy from syphilis".

---

## Competency questions

Sixteen questions, all executed against the full A-Box.

| | question | rows |
|---|---|---|
| CQ1 | Which lesions were observed on each specimen? | 32 |
| CQ2 | Which conditions were proposed for each specimen? | 25 |
| CQ3 | Which diagnoses were explicitly rejected? | 23 |
| CQ4 | Which datings were produced for each specimen? | 18 |
| CQ4b | For which specimens do two datings disagree? (strict) | 3 |
| CQ4b-t | The same, applying the precision the source states | 2 |
| CQ5 | Which error sources does the source declare per technique? | 5 |
| CQ6 | Which prior claims does the source engage with? | 21 |
| CQ7 | Which techniques are said to discriminate between hypotheses? | 9 |
| CQ8 | Which claims concern a treatment received in life? | 3 |
| CQ8b | For which specimens does medieval framed content sit beside a modern diagnosis? | 17 |
| CQ9 | How was the age of each individual estimated? | 6 |
| CQ10 | Which lesion types recur across more than one specimen? | 7 |
| CQ11 | Which claims does the source explicitly deny? | 2 |
| thesis | Everything ever asserted about one specimen | 12 |

CQ6, CQ11 and the thesis query need RDFS entailment: they use the superproperties `po:proposes` and `po:engagesWith`, which nobody ever asserts. On a store without reasoning they return nothing. `cq06_noentail.rq` is the same question written with a property path, kept beside the other to show what the superproperty buys.

### Negative competency questions

A competency question passes when it returns rows. A negative one passes when it returns none. The value is in the contrast on the same data: an empty result on an empty graph proves nothing.

| | question | why it is empty |
|---|---|---|
| NCQ1 | What disease did this individual have? | no property runs from `Specimen` to `Condition` |
| NCQ2 | In what year did this individual die? | years live only inside a `CalibratedInterval`, reachable only through a `DatingClaim` |
| NCQ3 | Which of the screened individuals were healthy? | the model has no vocabulary for asserting health |
| NCQ4 | Which technique proves the diagnosis? | for a different reason: the model would allow it, the source never claims it |
| NCQ5 | Does the mercury prove a disease? | no observation reaches a condition |

NCQ1 is no longer only an empty query. Writing `ex:sk90 po:proposesCondition ex:leprosy` makes the ontology **inconsistent**, and `run_probes.py` verifies it.

---

## Verification

Two suites, both runnable in one command each.

**`run_tests.py`** executes every competency question and every negative one, twice: on the raw graph and on the graph closed under RDFS entailment. Queries that need a reasoner are visible as the difference between the two columns.

**`run_probes.py`** breaks the model on purpose and records whether the reasoner notices. A consistent ontology proves nothing on its own, since an empty one is consistent too.

| probe | expected |
|---|---|
| reject a `Condition` instead of a `Claim` | inconsistent |
| two different hedges on one claim | inconsistent |
| two standpoints on one claim | inconsistent |
| one observation on two specimens | inconsistent |
| a `Claim` where a `Specimen` belongs | inconsistent |
| a `Specimen` given a `Condition` directly | inconsistent |
| `aboutSpecimen` on a methodological claim | inconsistent |
| a claim both negated and affirmed | inconsistent |
| `declaredIn` on an observation | consistent, allowed |
| two framed contents on one claim | consistent, allowed by design |
| `appliedTo` on a methodological claim | consistent, the sanctioned form |

**`tools/roundtrip_check.py`** takes the two hand-written A-Box files kept in `data/legacy/`, compares them against what the CSV regenerates, and reports any triple lost or invented. The result is clean, which is what proves the annotation tables are complete.

---

## Reuse and alignment

| our class | aligned to | how |
|---|---|---|
| `po:Bone` | UBERON | `skos:exactMatch` for femur, tibia, humerus, radius, fibula |
| `po:Condition` | MONDO | `skos:exactMatch` for leprosy, tuberculosis, treponemal infection |
| agents | FOAF | `foaf:Person`, `foaf:Organization` used directly |
| claim relations | CiTO | `cito:agreesWith`, `cito:disagreesWith`, `cito:updates` |

Three alignments are recorded as `skos:closeMatch` rather than `skos:exactMatch`, and the difference is deliberate. `exactMatch` says the two terms are the same thing, which lets a reasoner substitute one for the other; a wrong one propagates errors through the graph. Where a definition has not been checked, or where our term is narrower than theirs (our *venereal syphilis* against MONDO's *syphilis*), `closeMatch` is the honest statement. **An alignment is itself a claim**, and it deserves its hedge like any other.

One term, the parietal bone, is aligned to NCIT rather than UBERON, because neither UBERON nor MONDO carried a term at the required level of generality. Mixing alignment targets is acceptable when it is declared, and this is the declaration.

On using CiTO between claims rather than between documents: CiTO declares no domain and no range on its properties, and says why, so that the ontology "could be easily integrated with other models". The extension of use is designed, not improvised.

---

## Two things left visible on purpose

**Refshale 130.** The paper states that this is the one specimen whose radiocarbon age is in complete accordance with the archaeological date. Read literally the two intervals conflict, and the strict CQ4b reports a disagreement. The numbers have not been adjusted to make the query agree with the prose. See D7 in `docs/DESIGN_DECISIONS.md`, where applying the paper's own stated precision resolves it.

**St. Albani 94.** The body text dates the burial to AD 1250 to 1400 by arm position; Table 2 records 1250 to 1350 for the same burial. The body value is modelled and the difference is noted. The discrepancy is in the source.

---

## Precedent

**CONTRO** (KRKE 2023/24), on dialectical perspectives in argumentative discourse, is the precedent for treating perspective as the subject of an ontology rather than as noise to be removed.

---

## Licence

The ontology and the code are released under CC BY 4.0. The source article is CC BY 2.0 and is cited throughout; every `po:hedgeWording` value is a direct quotation from it.
