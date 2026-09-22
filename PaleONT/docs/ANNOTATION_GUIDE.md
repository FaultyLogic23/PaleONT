# Annotation guide

How to fill the four tables in `data/csv/`. Read this once, then read twenty existing rows. The rows are a better manual than any explanation.

---

## The rule

> You are transcribing what the source says, not summarising it and not judging it.

If the article writes "indicative of", the hedge wording is "indicative of". If it writes "consistent with", it is a weaker claim and must be recorded as weaker. The difference between those two phrases is the project's main result, and it survives only if nobody smooths it out.

**Never record a fact. Record who said it.** There is no row anywhere that says an individual had a disease. There are rows saying that someone proposed a disease for a specimen, on the basis of an observation, within a framework, with a stated confidence.

---

## The four tables

```
specimens.csv      5 rows    one per skeleton
observations.csv  46 rows    one per act of examining
claims.csv        69 rows    one per assertion
intervals.csv     12 rows    one per dated range
```

### Naming

Every identifier is prefixed with its specimen, so five skeletons never collide:

```
ex:sk90_obs_tibia          ex:rf130_claim_systemic
ex:sk89_claim_date_c14     ex:tp292_reject_leprosy
```

Identifiers are stable and opaque on purpose. If you call a claim `ex:leprosy_claim` and later discover it proposed something else, you are left with a name that lies. Meaning lives in the triples, not in the identifier.

### Multiple values

Cells that can hold more than one value separate them with `|`:

```
lesion_types   ex:clusteredPitting|ex:periostealReaction
grounded_in    ex:sk90_obs_parietal|ex:sk90_obs_femur|ex:sk90_obs_tibia
```

The `relation` column separates groups with `;` and targets within a group with `|`:

```
relation   cito:agreesWith>ex:sk90_claim_harper;cito:disagreesWith>ex:sk90_claim_ortner
```

### Empty cells

An empty cell means "not stated". It never means "no" or "zero". This matters most for `negated`: an empty cell means the claim is affirmative, and `true` means the source denies its content.

---

## observations.csv

One row for one act of examining one specimen with one technique.

| column | contents |
|---|---|
| `id` | `ex:<specimen>_obs_<what>` |
| `specimen` | the skeleton |
| `lesion_types` | one or more `po:LesionType` individuals, `\|` separated |
| `bone` | one `po:Bone` individual |
| `technique` | one `po:Technique` individual |
| `source` | usually `ex:schwarz2013` |
| `label` | the source's own description, quoted closely |

**No observation may mention a disease.** If you find yourself wanting to write one into a label, what you have is a claim, and it belongs in the other table.

Observations with no lesion, such as a mercury measurement or a radiocarbon run, leave `lesion_types` and often `bone` empty. They still exist, because claims are grounded in them.

---

## claims.csv

One row per assertion. Every row carries the same core columns whatever its type.

| column | contents |
|---|---|
| `id` | `ex:<specimen>_claim_<what>` or `ex:<specimen>_reject_<what>` |
| `type` | one of the six subclasses, see below |
| `specimen` | the skeleton, **empty for `MethodologicalClaim`** |
| `proposes` | what the claim puts forward; what goes here depends on `type` |
| `min_age`, `max_age` | integers, `AgeClaim` only |
| `agent` | who says it |
| `standpoint` | where the claimant stands, in this source always `po:ModernBiomedical` |
| `frames_content` | which system of thought the content belongs to |
| `hedge` | `po:Certain`, `po:Probable`, `po:Possible`, `po:Tentative` |
| `hedge_wording` | **the source's exact words**, quoted |
| `negated` | `true` if the source denies the content, otherwise empty |
| `grounded_in` | the observations it rests on, `\|` separated |
| `source` | where it was published |
| `label` | a readable one-line summary |

### What goes in `proposes`

The `type` column decides:

| type | `proposes` holds |
|---|---|
| `DiagnosticClaim` | a `po:Condition`, for example `ex:leprosy` |
| `TreatmentClaim` | a `po:Treatment` |
| `DatingClaim` | one or more interval ids from `intervals.csv` |
| `RejectionClaim` | **the id of the claim being rejected** |
| `MethodologicalClaim` | a `po:Technique` |
| `AgeClaim` | nothing; use `min_age` and `max_age` |

### Choosing the hedge

Map the source's words, do not invent a scale.

| the source writes | hedge |
|---|---|
| "for sure", "with certainty", "completely reliable" | `po:Certain` |
| "indicative of", "regarded as diagnostic", "apparently" | `po:Probable` |
| "consistent with", "possible", "might be", "can also occur" | `po:Possible` |
| "remains contentious", "cannot be excluded" | `po:Tentative` |

Always fill `hedge_wording` with the actual sentence. The level is for querying; the wording is what protects the author from our normalisation. If the two ever come apart, the wording is the truth.

### Rejections

A rejection needs the claim it rejects to exist first. The pattern is always two rows:

```
ex:sk89_claim_alt_leprosy    DiagnosticClaim   proposes ex:leprosy       hedge Possible
ex:sk89_reject_leprosy       RejectionClaim    proposes ex:sk89_claim_alt_leprosy
```

The first records that the diagnosis was entertained. The second records that it was refused, by whom and on what ground.

**A rejection says nothing about the disease.** Rejecting a claim of leprosy does not assert that the individual did not have leprosy. It asserts that a proposal was refused. This is the distinction the whole project is built on, so do not collapse the two rows into one.

### Methodological claims

Leave `specimen` empty. A methodological claim is about a technique, and the model forbids `aboutSpecimen` on it; a value there makes the ontology inconsistent.

If the judgement was reached while examining particular skeletons, and the source says so, list them in `applied_to`.

---

## intervals.csv

| column | contents |
|---|---|
| `id` | `ex:<specimen>_interval_<method>` |
| `start_year`, `end_year` | integers; negative for BCE |
| `confidence_interval` | "1 sigma", "95% CI", "archaeological, no statistical confidence stated" |
| `label` | as the source prints it |

The confidence column is not decoration. CQ4b compares intervals, and comparing a 1 sigma range with an archaeological estimate as if both had hard edges is the error described in D7. One dating claim may carry several intervals; list them all in `proposes`, `|` separated.

---

## Adding a new term

If the article names a bone, a lesion type, a condition or a technique that does not yet exist, add it to `data/vocabulary.ttl`, not to a CSV. Terms are curated; claims are annotated.

```turtle
ex:newLesion a po:LesionType ;
    rdfs:label "the source's own term"@en .
```

For bones and conditions, look the term up at https://www.ebi.ac.uk/ols4 and add an alignment. Read the definition, not only the label. If the external term is broader or narrower than yours, use `skos:closeMatch` rather than `skos:exactMatch` and say so in a comment. An alignment is a claim and takes its own hedge.

---

## After every change

```bash
python3 tools/build.py
python3 run_tests.py
python3 run_probes.py
```

If a test fails, the CSV is usually wrong before the model is. Read the failing query, find which column it reads, and check that column in the rows you just added.

---

## Dividing the work between three people

Split by **row type**, not by specimen. Everyone then does the same job repeatedly and gets fast at it.

| person | table and rows |
|---|---|
| A | `observations.csv`: lesions, bones, techniques |
| B | `claims.csv`: diagnoses, rejections, differential diagnoses |
| C | `claims.csv` and `intervals.csv`: datings, ages, treatments, methodological claims |

B and C share a file but never a row. Agree on identifier prefixes before starting and there will be no collisions.

---

## Common mistakes

**Writing a disease into an observation label.** That is a claim. Move it.

**Filling `hedge` and leaving `hedge_wording` empty.** The level alone is our reading. Without the quotation nobody can check it.

**Merging two rejections into one row.** Each rejected diagnosis needs its own entertained claim, otherwise CQ3 cannot report what was rejected and on what ground.

**Giving a `MethodologicalClaim` a specimen.** The reasoner will catch it, but it is faster to remember the rule.

**Tidying the source.** If the article contradicts itself, record both sides and say so in a comment. Two such contradictions are already in the data, on Refshale 130 and St. Albani 94, and they are left visible on purpose.
