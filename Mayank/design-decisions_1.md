# Design decisions

One block per modelling decision. Every block names the **alternative rejected**
and **which competency question it would have failed**.

This file is the source for presentation slides 4 and 5, and it is what a
reviewer will read to judge whether the ontology was designed or guessed.

Format:

```
## DD-nn — <short name>
CQ:        which competency question forces this
Source:    §, "the sentence that created the problem"
Problem:   what cannot be represented naively
Logic:     why the naive form fails
Solution:  the pattern
Rejected:  the cheaper alternative, and the CQ it cannot answer
```

---

## DD-01 — Nothing connects an individual to a disease

**CQ:** CQ20 (negative), CQ03
**Source:** Methods — *"The bone lesions of the three treponematoses affecting the skeleton are not distinguishable from each other."*

**Problem.** Every osteological recording standard has a `diagnosis` field. One
field holds one value, so a record with three equally supported diagnoses must
pick one — manufacturing a certainty the specialist never had.

**Logic.** A diagnosis is not a property of a skeleton. It is a claim made by a
person about a skeleton. Different things, with different authors, dates and
degrees of confidence.

**Solution.** Reify the claim. `pp:DiagnosticClaim` carries `pp:groundedIn`,
`pp:hasAuthor`, `pp:hasHedge`, `pp:appliesFramework`, and
`pp:claimsDisease` / `pp:excludesDisease`.

**Critically:** no object property in this ontology has domain
`pp:SkeletalIndividual` and range `pp:DiseaseConcept`. CQ20's refusal is
structural, not an omission.

**Rejected.** `pp:hasDiagnosis` from individual to disease. Simpler and easier to
query, but fails CQ03 (what grounds it?), CQ07 (what hedge?), CQ08 (competing
claims), CQ13 (exclusions) — and makes CQ20 return an answer it must not return.

---

## DD-02 — A claim may be grounded in another claim

**CQ:** CQ17, CQ03
**Source:** Discussion — *"**Since tuberculosis can be excluded** the focal superficial cavitations can be regarded as a diagnostic criterion for treponemal infection."*

**Problem.** The obvious range for `pp:groundedIn` is `pp:Observation` — a claim
rests on something someone saw. But here a diagnosis rests on an *exclusion*,
which is itself a claim.

**Logic.** Scientific reasoning chains. If grounding can only reach observations,
every chain is flattened to its leaves and the intermediate reasoning is lost.

**Solution.** `pp:groundedIn` has range `pp:Observation or pp:Claim`. Two
sub-properties keep the distinction queryable:
`pp:groundedInObservation` and `pp:groundedInClaim`.

**Rejected.** Range `pp:Observation` only, with the TB exclusion re-pointed at
the underlying spinal observations. Loses the fact that the authors reasoned
*through* the exclusion, and fails CQ17 entirely.

---

## DD-03 — Adjudication is a claim, with a property-chain shortcut

**CQ:** CQ14, CQ04
**Source:** Discussion — *"This fact points to an **error in the archaeological date** by arm position … as compared to reliable radiocarbon date."*
Also Introduction — *"Harper and colleagues **disproved** most of the alleged pre-Columbian dates."*

**Problem.** The authors do not merely record that two dates disagree. They rule
one of them wrong. That judgement has an author, a hedge, and grounds of its own.

**Logic.** A bare `pp:supersedes` property between two DatingClaims has only two
slots. It cannot say who decided, how confidently, or on what basis.

**Solution.** `pp:AdjudicationClaim` — a Claim with `pp:adjudicates` (the claim
judged) and `pp:inFavourOf` (the claim preferred). Then a property chain restores
the convenient binary form:

```
inverse(pp:inFavourOf) ∘ pp:adjudicates  ⊑  pp:supersedes
```

So a query can use `pp:supersedes` when it doesn't care who decided, and walk
into the `AdjudicationClaim` when it does. *(Patterns part 4: reify for
expressiveness, chain for convenience.)*

**Rejected.** `pp:supersedes` as a plain asserted property. Cheap, but cannot say
that it was *these* authors who judged, with the hedge *"points to an error in"*,
on the grounds of the δ¹⁵N result. Fails CQ14.

---

## DD-04 — Rival claims are linked explicitly

**CQ:** CQ18, CQ08
**Source:** Discussion — *"The individuals **could also have been otherwise in contact with Hg**, but … Hg-containing medicine **seems to be the most likely factor**."*
Conclusions — *"had been treated (**or otherwise in contact**) with Hg."*

**Problem.** A third status is needed, beyond claimed and excluded: a rival
explanation that is neither accepted nor ruled out, and that survives into the
authors' own conclusion in brackets.

**Logic.** The ranking is already carried by the hedges —
`hedge:most-likely-factor` versus `hedge:could-otherwise`. What is missing is the
*link* saying these two claims are competing readings of the same evidence.

In principle rivalry is derivable (two claims sharing grounds but claiming
different things), but that derivation needs negation, which OWL cannot express.

**Solution.** `pp:rivalOf`, symmetric, asserted between claims that explain the
same evidence differently. Ranking is read off the hedges, not off a number.

**Rejected.** (a) A numeric `pp:confidence`. Asserts something the authors never
said — the rule from Phase 1. (b) Leaving rivalry implicit. Fails CQ18.

---

## DD-05 — A dating claim carries many intervals, each tied to its corrections

**CQ:** CQ05, CQ06, CQ21 (negative)
**Source:** Results, sk. 94 — *"calAD 1453–1494 (1 sigma), but could also be as late as calAD 1602–1614."* Table 2 gives sk. 94 three intervals once corrected for marine signature.

**Problem.** A calibrated radiocarbon date is not a number and often not even a
single range. Skeleton 94 has two intervals at 1σ uncorrected and three at 95% CI
corrected. `from`/`to` cannot hold this, and a midpoint is a fiction.

**Logic.** A calibrated date is the end of a chain: a raw determination, a
calibration curve, a marine reservoir correction, and a possible freshwater
correction whose applicability rests on a *dietary inference* from δ¹⁵N. Each
link has its own author and its own hedge.

**Solution.**
`pp:RadiocarbonDetermination` (a Measurement) → `pp:DatingClaim` with
`pp:hasCalibratedInterval` (1..n `pp:TimeInterval`), `pp:appliesCorrection`
(0..n `pp:Correction`), `pp:atSigmaLevel`, and `pp:usesCalibrationCurve`.
Each `pp:Correction` is itself `pp:groundedIn` the isotope measurement that
licensed it.

Because both Table 1 and Table 2 values are modelled, CQ06 correctly answers
*"depends which correction you accept"* for skeleton 94.

**Rejected.** A single `pp:datedTo` with two xsd:gYear values. Fails CQ05
(no corrections), CQ06 (no assumptions to state), and makes CQ21 answerable.

---

## DD-06 — Diseases are SKOS concepts, not OWL classes

**CQ:** CQ03, CQ08, CQ23 (negative)
**Source:** Methods — the three treponematoses; Discussion — the differential diagnosis list.

**Problem.** Should `VenerealSyphilis` be an OWL class with instances, or a term
in a vocabulary?

**Logic.** No competency question asks *"which individuals had disease X"* — that
question is precisely the one the project refuses. Every CQ asks which disease
was **claimed**. So a disease appears only as the *value* of a claim, never as a
category with members.

There is also a practical reason. Our terms must link to MONDO, whose terms are
OWL classes. `owl:equivalentClass` between our term and a MONDO class would be a
much stronger assertion than we can support, and mixing SKOS concepts with OWL
classes in one hierarchy is a known anti-pattern.

**Solution.** `pp:DiseaseConcept ⊑ skos:Concept`, organised with `skos:broader`,
linked outward with `skos:closeMatch` / `skos:exactMatch` to MONDO.

**Critically:** `VenerealSyphilis` and `NonVenerealTreponematosis` stand in **no**
`skos:broader` relation to each other. The article is explicit that they are
different diseases, not a genus and a species.

**Rejected.** OWL classes with `rdfs:subClassOf`. Would let a reasoner infer
subsumptions the article denies, and invites exactly the CQ23 assertion the model
must refuse.

---

## DD-07 — A negative observation is not the absence of an observation

**CQ:** CQ13, CQ22 (negative)
**Source:** Discussion — *"**None** of the five skeletons described in this paper **shows any lesions diagnostic of leprosy**."* Results, sk. 89 — *"**No** concomitant pathology **was observed** on the remaining skeletal elements."*

**Problem.** Three states are being conflated by any single `diagnosis` field:
something was seen · something was looked for and not seen · nothing was looked at.

**Logic.** The leprosy exclusion is grounded in an act of looking that found
nothing. That is evidence. The 1,013 unexamined individuals are not evidence of
anything at all. Under the open world assumption both come out as silence unless
the first is recorded positively.

**Solution.** `pp:NegativeObservation ⊑ pp:Observation`, with
`pp:soughtFeature` naming what was looked for. `pp:ScreeningObservation`
records examination with no candidate lesion found.
A `pp:DiagnosticClaim` with `pp:excludesDisease` may be
`pp:groundedIn` a NegativeObservation.

**Rejected.** Recording only positive findings and treating absence as absence.
Fails CQ13 (the leprosy exclusion has no grounds) and makes CQ22 indistinguishable
from a data gap.

---

## DD-08 — A contrast between claims is itself an entity

**CQ:** CQ09
**Source:** Methods — the indistinguishability statement; Introduction — Rothschild re-reading Stirland's material as yaws.

**Problem.** CQ09 asks not *that* two claims differ but *what the difference
consists in*: same lesions, different criteria, different disease.

**Logic.** That is a three-way statement about a pair of claims. No binary
property holds it.

**Solution.** `pp:Contrast` with `pp:contrastsClaim` (exactly 2),
`pp:sharedEvidence`, `pp:differingFramework`, `pp:differingDisease`.
*(The Situation pattern: reify, project, key.)*

**Rejected.** `pp:differsFrom` between claims. Says that they differ, never how.
Fails CQ09, which is the project's most distinctive query.

---

## DD-09 — Hackett's two tiers of criterion are distinguished

**CQ:** CQ03, CQ09
**Source:** Results — *"superficial cavitation (**diagnostic criterion**, Hackett)"* versus *"fit Hackett's **on-trial criteria**"*. Conclusions — *"three of them only meet the descriptions of Hackett's on-trial criteria, but two are also displaying diagnostic criteria."*

**Problem.** The article uses two named strengths of criterion within one
framework, and the Conclusions turn on the difference.

**Logic.** This is not a hedge — it is a property of the *framework*, not of the
author's confidence. Collapsing it into the hedge vocabulary would misattribute
Hackett's distinction to Schwarz et al.

**Solution.** `pp:CriterionTier` with individuals `ppd:diagnostic-criterion` and
`ppd:on-trial-criterion`, reached by `pp:atCriterionTier` on the claim.

**Rejected.** Folding both into `hedge:fits`. Loses the Conclusions' central
distinction between the three weaker and two stronger cases.

---

## DD-10 — The source's self-contradiction is recorded, not resolved

**CQ:** CQ16
**Source:** Methods p.2 — *"out of **327** that were examined"*; Results p.4 — *"examination of **375** skeletons"*.

**Problem.** Both numbers are printed in the same paper. 114 + 134 + 79 = 327.

**Logic.** Silently picking 327 would be *editing the source*. The project's whole
claim is that it records what was said, including where what was said is
inconsistent.

**Solution.** Two `pp:ScreeningObservation` individuals, each with its own
`pp:statedCount` and `pp:reportedOnPage`. No `owl:sameAs`, no reconciliation.
CQ16 finds them by looking for two observations of the same scope with different
counts.

**Rejected.** Recording 327 with a comment. Fails CQ16, and quietly asserts an
editorial judgement the model has no authority to make.

---

## Summary of what the ontology must forbid

| Must not exist | Why |
|---|---|
| a property from `SkeletalIndividual` to `DiseaseConcept` | DD-01, CQ20 |
| `subClassOf` / `skos:broader` between venereal and non-venereal treponematosis | DD-06, CQ23 |
| a single `deathYear` datatype property | DD-05, CQ21 |
| a numeric confidence on any claim | Phase 1 rule, DD-04 |
| a `Claim` without author, grounds and hedge | DD-01, enforced by axiom |
