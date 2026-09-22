# Design decisions

Seven tracked decisions, plus the choices made before tracking began. Each entry states what was chosen, what was rejected, and why. This is the pattern matching section of the project: the course does not grade reification as such, it grades whether you can say why you reified instead of doing something else.

A thread runs through the tracked decisions and is worth naming at the start. **Three times out of seven the problem was one property trying to say two things, and three times the answer was to split it rather than to choose.** The fourth time, in the annotation tables, the answer was the opposite, and the reason it differs is set out under D4.

---

## Before the tracked decisions

### Framing

| | chosen | rejected |
|---|---|---|
| scope | one article | a theme, or a corpus |
| thesis | disagreement is a symptom | "scientists contradict one another" |
| order | T-Box before the annotation tables | annotate first |
| verification | a vertical slice with a CQ/NCQ gate | annotate everything, then look |
| tools | Turtle by hand, Protégé only for the reasoner | build in Protégé |

**Why a source and not a theme.** A theme has no end. An article does. There is also a less obvious benefit: a story written by someone else stops you from modelling the ontology you already had in mind. Invent the material and the result is circular; a real source pushes back, and the places where it pushes back are where the decisions worth arguing come from.

**Why the T-Box first.** The columns of the annotation tables *are* the properties, so designing the columns is designing the model, only in a format that cannot express domain, range or disjointness and that no reasoner can check. The cost is also asymmetric: the T-Box is one person for an afternoon, the annotation is three people for days, and whichever comes second inherits the constraints of the first. The real danger is psychological. With two hundred rows already filled, discovering that the model needs changing does not lead to changing the model. It leads to bending the model to fit the table.

**The objection, and why it does not apply.** You cannot model what you have not looked at. True in general, and already satisfied here: the article was read, and the competency questions came out of it. **Reading is not annotating.** Reading is discovery and is done; annotation is transcription and is done against a schema. For the residual risk there is the vertical slice, forty triples on one specimen, which is the deliberately small and deliberately early point at which the data gets a vote on the model.

### Classes

**No `Hypothesis` class.** A hypothesis is not a kind of thing. It is a **role** that a `Condition` takes on when competing claims propose it. Leprosy is not both a disease and a hypothesis; it is a disease that plays the role of hypothesis in a context. The course has six Role patterns precisely because this distinction keeps recurring.

**One `Technique` class, with no hierarchy.** Naked-eye examination and radiocarbon dating sit together, as individuals of the same class. Splitting them into "observation" and "scientific method" would write a hierarchy of reliability into the schema, and that hierarchy is exactly what the article **argues about**. CQ7 asks which techniques are presented as able to discriminate; if the answer were built into the class structure, CQ7 would have nothing left to ask, and it would be answering with our lens rather than the source's. Discriminating power lives in `po:MethodologicalClaim`, where the source can state it without our endorsing it.

**`LesionType` is the type, `Observation` is the occurrence.** Periostitis as a universal cannot be located on one tibia; the same type recurs on many bones of many individuals. The concrete occurrence is the observation, which carries the bone and the technique. Without this separation CQ10, recurrence across specimens, has nothing to group on.

*Cost, declared:* if two authors observe the same physical lesion independently, this model gives two observations with no way to state that they concern one lesion. A separate `LesionOccurrence` class would fix it. No competency question needs it, so it was not introduced.

**`ConfidenceLevel` is an individual, not a number and not a string.**

A number invents precision the source never produced. "Probable" is not 0.7, and once 0.7 is in the graph it looks like a measurement: it can be averaged, ranked, plotted. That is the project's own error committed one level up.

A string cannot be counted, ordered, defined or aligned. Thirty claims hedged as "probable" become thirty unrelated pieces of text, `"Probable"` with a capital is a different value again, and nothing can express that one level is weaker than another.

An individual is a single node with thirty arrows pointing at it. Alongside it, `po:hedgeWording` keeps the source's exact phrasing, so our normalisation never silently replaces the author's own way of hedging.

**`ErrorSource` and `Correction` are separate classes.** An error source is a known limitation of a **technique** and holds always. A correction is an intervention applied to **this dating** and holds here. The distinction is not pedantry: without the correction recorded, CQ4b would report as a disagreement between authors what is one measurement in two states, which is a false positive in our own results.

**`CalibratedInterval` is a class, ages are two literals.** CQ4b compares two intervals against each other and needs addressable nodes with comparable bounds. No competency question compares two age estimates. Structure is introduced only where a query demands it.

---

## D1. Range of `po:groundedIn`

**Question.** The range is `po:Observation`. But a `RejectionClaim` is often grounded in a methodological argument rather than in a direct observation. Widen the range to `Observation` or `Claim`, or introduce a second property?

**Resolved by evidence: the range stays `po:Observation`.**

Every rejection in the article turned out to rest on an observation, and CQ3 returns 23 rows. A union range would have kept one property and one query pattern, at the cost of the guarantee that grounding bottoms out in evidence. Since the data never needed it, the guarantee was kept.

---

## D2. Domain of `po:usedTechnique`

**Question.** The domain is `po:Observation`, so a `DatingClaim` reaches its technique through `groundedIn / usedTechnique`. Accept the extra hop, or duplicate the property on `po:Claim`?

**Resolved: the domain stays `po:Observation`.**

The hop enforces that every use of a technique is an observation. A duplicate would be shorter to query but would let a claim cite a technique it never applied. CQ4 and CQ9 answer through the hop without difficulty.

---

## D3. `po:redetermines` withdrawn in favour of `cito:updates`

**Question.** `po:redetermines` was coined for this project, to say that the radiocarbon date supersedes the arm-position date. Does CiTO already carry that sense?

**Resolved: the local term is withdrawn. `cito:updates` is used instead.**

CiTO defines it as "the citing entity provides updated information superseding the cited entity", which is exactly the intended meaning. One fewer invented term, and reuse is a stated value of the course.

Two things were checked before adopting it.

**`cito:corrects` is the near neighbour and was not chosen.** Correcting an *error* is what `po:RejectionClaim` already records. The relation between the two dating claims is supersession, not correction.

**Using CiTO between claims rather than between documents is legitimate.** CiTO declares no domain and no range on its properties, and states the reason: "so that this ontology could be easily integrated with other models". The extension of use is designed. This also settles `cito:agreesWith` and `cito:disagreesWith`, which were already being used the same way.

`po:rejects` stays local. Refusing another agent's claim is a distinct act from citing them, and no CiTO property carries the sense of a claim whose entire content is the refusal of another.

---

## D4. `po:underFramework` and `po:framesContent`

**Question.** A modern study asserts that an individual was treated with mercury. Which framework does that claim belong to, the modern biomedical one or the medieval humoral one?

**Resolved: two properties, not one.**

| property | records | value in this source |
|---|---|---|
| `po:underFramework` | where the **claimant stands** | always `ModernBiomedical` |
| `po:framesContent` | the system of thought the **content** belongs to | `MedievalHumoral` for the mercury claims |

**Why one property could not do both.** Schwarz et al. are modern scientists who measured mercury with a spectrometer. The claim is modern. But mercury counted as a *medicine* because medieval medicine said so, and that is where the content belongs. Collapsing the two forced a choice between a false uniformity (everything modern, CQ8b empty, the two-lens demonstration gone) and an equivocation (the property meaning one thing for the mercury claim and another for the rest).

**The consequence is sharper than the version it replaces.** The two frames do not coexist as equals. One contains the other. The paper does not look at Sk. 90 from inside the medieval frame; it looks from outside and **represents** that frame. There is no standpoint from which both can be seen externally, and that is the perspectival argument in its strongest form.

`po:underFramework` stays functional: a claim is made from one position. `po:framesContent` is deliberately **not** functional, because a claim may frame content belonging to more than one system, and closing that off buys nothing.

**Uniformity as a finding.** Every `po:underFramework` in the A-Box is `ModernBiomedical`. That is not a defect of the data. It records that the source never leaves the modern frame. Add a second source written from another standpoint and the column starts to vary.

### The same question in the annotation tables, answered the other way

`claims.csv` has one polymorphic `proposes` column, holding a condition, a treatment, an interval or a rejected claim depending on the row. That is the opposite of what was done in the T-Box, and the reason is a rule worth stating:

> **Merge when something else in the row disambiguates. Split when nothing does.**

In `claims.csv` the `type` column is the discriminator: a row typed `DiagnosticClaim` has a condition in `proposes`, and the mapping branches on it. In D4 there was no discriminator anywhere in the graph, so the same property genuinely meant two things.

There is also a cost on the human side that does not exist in the T-Box. Separate columns would leave most rows with three empty cells out of four, and a sheet like that is filled in wrongly. Readability in a spreadsheet matters as much as precision in the schema, but it matters for different people.

---

## D5. `aboutSpecimen` forbidden on methodological claims, plus `po:appliedTo`

**Question.** A `MethodologicalClaim` is about a technique, not a skeleton, which is why it has no `aboutSpecimen`. But nothing stopped anyone writing one. Should the model forbid it?

**Resolved: forbid it, and add a different property for the thing that was true.**

```turtle
po:MethodologicalClaim rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty po:aboutSpecimen ;
    owl:maxCardinality "0"^^xsd:nonNegativeInteger ] .

po:appliedTo  MethodologicalClaim -> Specimen
```

This is D4 again in a different costume. One property was being asked to carry two meanings. "This claim is about this skeleton" is false of a methodological claim. "This judgement about a method was reached while examining this skeleton" is true, and the source says so: *"the results of the archaeometric analyses **applied here** cannot elucidate the origin"*.

Forbidding alone would have lost that information. Allowing alone would have left the meta level as a convention rather than a constraint. Splitting gives both.

Verified: `aboutSpecimen` on a methodological claim now makes the ontology inconsistent, and `appliedTo` does not.

---

## D6. `po:isNegated`

**Question.** The source states that the Refshale and Tirup individuals "were not exposed to high amounts of Hg during their life". That is a claim, with an agent, a ground and a hedge. The model could not hold it.

**Resolved: a negation flag on `po:Claim`.**

```turtle
po:isNegated a owl:DatatypeProperty , owl:FunctionalProperty ;
    rdfs:domain po:Claim ; rdfs:range xsd:boolean .
```

**Why it was needed.** Every property in the model was affirmative, so a source could be recorded only when it asserted something. **That asymmetry was itself a position.** It made denial invisible while assertion was fully represented, in a project whose entire subject is how a source's standpoint shapes what gets recorded.

**Precedent.** The course slides use exactly this device in the Ferguson unit tests. "Who is refused to receive what?" is answered with `?e :isNegated "true"`, and the affirmative queries carry `FILTER NOT EXISTS { ?e :isNegated "true" }`. Ours is typed boolean rather than a string, but the pattern is theirs.

**Not the same as `po:rejects`.** A `RejectionClaim` refuses **someone else's claim**, at layer 3. `po:isNegated` is layer 1: the claim's own content is asserted negatively.

> "I reject your diagnosis of syphilis" is not "I claim he was not treated with mercury".

**No tension with NCQ3.** A negated claim is still a claim, carrying an agent, a framework and a hedge. The model still cannot say that an individual **was healthy**. It can say that someone denied a particular condition for them. Denials are perspectival too, which is the thesis applied symmetrically rather than an exception to it.

**Consequence.** Absence of the property means affirmative, so every query reporting what a source asserts carries `FILTER NOT EXISTS { ?claim po:isNegated true }`. Ten queries were updated. A new competency question, CQ11, asks what the source denies.

---

## D7. `po:confidenceInterval`, and two readings of CQ4b

**Question.** CQ4b computed disagreement by comparing the endpoints of two calibrated intervals. Is that right?

**Resolved: no, and the fix is a second query rather than a changed one.**

**Our own query was committing the reduction this project argues against.** A calibrated radiocarbon interval is not a fact with edges. It is a hedged estimate, and the source says so: *"the precision of the radiocarbon dates of medieval samples are often better than +/- 25 to 30 years for the 1 sigma statistical uncertainty of the calibrated age interval"*.

Every `po:CalibratedInterval` now carries its stated confidence: "1 sigma", "95% CI", or "archaeological, no statistical confidence stated". And there are two queries.

| query | result |
|---|---|
| `cq04b.rq`, strict reading | 3 disagreements: Sk. 90, Sk. 94, Refshale 130 |
| `cq04b_tolerant.rq`, with the source's own +/- 30 | 2: Sk. 90 and Sk. 94 |

The arithmetic for Refshale 130: the 95% range corrected for the marine component reaches 1224, plus the 30 years the authors declare gives 1254, against an archaeological date beginning in 1250. They meet. For Sk. 90 the gap survives: 1400 plus 30 is 1430, against 1443.

**The tolerance is the source's figure, not ours.** Inventing one would have been the same error in better disguise: our lens substituted for theirs. Both queries stay in the repository, because **the difference between them is the finding**. One shows what the numbers say taken literally; the other shows what they say once the uncertainty the authors declare is applied. Neither is the correct one. Being able to show that they differ is the point of the project.

This also answers an obvious challenge at the oral. Is the model too sceptical? No. It is sceptical about itself too.

---

## Technical decisions

| | chosen | why |
|---|---|---|
| disjointness | all 15 top-level classes pairwise, plus `owl:AllDifferent` on the value individuals | without it the reasoner finds nothing: `rdfs:range` does not forbid, it **retypes** |
| years | `xsd:integer` | `xsd:gYear` is not in the OWL 2 datatype map and HermiT refuses to load an ontology that uses it |
| `po:declaredIn` | no domain | with domain `Claim`, every observation carrying it was inferred to be a claim, and the two classes are disjoint. HermiT found this |
| superproperties | `po:proposes`, `po:engagesWith` | one query term instead of an enumeration that must be edited whenever a relation is added |
| alignments | UBERON and MONDO, with a declared NCIT fallback, and `closeMatch` where unverified | an alignment is a claim and deserves its hedge |

### Where sub-properties were deliberately not used

The observation and claim boundary is **not** a property hierarchy. `po:groundedIn` is a single property between two disjoint classes. Making evidence and interpretation two sub-properties of one parent would imply they are two flavours of the same relation, which is precisely the conflation the project argues against.

---

## Standing rules

> **Everything the thesis promises must exist at least once. Nothing needs to exist a hundred times.** Gaps in coverage are expected and defensible. A gap between what is claimed and what the model does is fatal.

> **Every class must earn its place.** If no query binds a variable to a class, that class is not needed. It is the harshest criterion and the most useful.

> **The T-Box must not name the source.** If replacing the article with another palaeopathology paper would require rewriting the T-Box, the result is a structured summary, not an ontology.

> **An explained inconsistency is worth more than a consistency obtained by accident.** This is why the probes exist: break the model on purpose and check that the reasoner notices.
