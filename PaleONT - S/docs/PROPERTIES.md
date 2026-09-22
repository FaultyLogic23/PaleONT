# PaleONT, Property specification

Prefix: `po:` → `https://w3id.org/paleont/`
Reused: `rdfs:` `owl:` `xsd:` `foaf:` `cito:` `uberon:` `mondo:`

This document specifies the properties of the PaleONT T-Box. Every property listed here is required by at least one competency question; nothing is included that no query reaches.

---

## 0 · The four layers

The model separates four levels of assertion. Reading them in order is the fastest way to understand the ontology.

| layer | class | what it holds | example |
|---|---|---|---|
| **0, evidence** | `po:Observation` | what was seen or measured, with which technique, on which bone | periostitis observed on the tibia of Sk. 90 by naked-eye examination |
| **1, interpretation** | `po:DiagnosticClaim`, `po:DatingClaim`, `po:AgeClaim`, `po:TreatmentClaim` | what someone proposed on the basis of layer 0 | *leprosy*, proposed by Author A, under the modern biomedical framework, hedged as *probable* |
| **2, meta** | `po:MethodologicalClaim` | what a technique can or cannot establish | radiocarbon dating *can* discriminate between these two intervals; macroscopic palaeopathology *cannot* discriminate leprosy from treponematosis |
| **3, adjudication** | `po:RejectionClaim`, `cito:agreesWith`, `cito:disagreesWith`, `cito:updates` | a claim about another claim | Author B rejects Author A's diagnosis, on the basis of a layer-2 argument |

The boundary between layer 0 and layer 1 is a single property: **`po:groundedIn`**. Everything to the left of it is evidence; everything to the right is interpretation. That property *is* the epistemic argument of the project, expressed in one arc.

Layer 2 is a genuine meta level: a `po:MethodologicalClaim` has **no `po:aboutSpecimen`**, because its subject matter is a technique, not a skeleton. That absence is how the model distinguishes "this individual had leprosy" from "this method cannot tell leprosy from syphilis".

Layer 3 never asserts truth. `po:rejects` has range `po:Claim`, not `po:Condition`, you reject an assertion, not a disease.

---

## 1 · Object properties

### 1.1 On `po:Observation`, layer 0

| domain | property | range | CQ |
|---|---|---|---|
| `po:Observation` | `po:observedOn` | `po:Specimen` | 1, 10 |
| `po:Observation` | `po:observesLesionType` | `po:LesionType` | 1, 10 |
| `po:Observation` | `po:onBone` | `po:Bone` | 1 |
| `po:Observation` | `po:usedTechnique` | `po:Technique` | 1, 4, 9 |

`po:onBone` ranges over UBERON terms. `po:observesLesionType` points at the **type**, shared across specimens, the concrete occurrence is the observation itself, which is why CQ10 can group on the type while CQ1 still distinguishes each sighting.

### 1.2 On `po:Claim`, inherited by all six subclasses

| domain | property | range | CQ |
|---|---|---|---|
| `po:Claim` | `po:aboutSpecimen` | `po:Specimen` | 2, 3, 8, 9 |
| `po:Claim` | `po:groundedIn` | `po:Observation` | all |
| `po:Claim` | `po:heldBy` | `po:Agent` | 2, 3, 6, 8, 9 |
| `po:Claim` | `po:underFramework` | `po:DiagnosticFramework` | 2 |
| `po:Claim` | `po:framesContent` | `po:DiagnosticFramework` | 8b |
| `po:Claim` | `po:hedge` | `po:ConfidenceLevel` | 2, 8, 9 |
| `po:Claim` | `po:declaredIn` | `po:Source` | 5, 6 |

Declared once on the superclass, inherited six times. This is the return on making `po:Claim` a superclass rather than writing six unrelated classes.

`po:aboutSpecimen` is **not** inherited in practice by `po:MethodologicalClaim`, see §0, layer 2.

### 1.3 Specific to subclasses, layer 1

| domain | property | range | CQ |
|---|---|---|---|
| `po:DiagnosticClaim` | `po:proposesCondition` | `po:Condition` | 2 |
| `po:DatingClaim` | `po:hasResult` | `po:CalibratedInterval` | 4, 4b |
| `po:DatingClaim` | `po:appliedCorrection` | `po:Correction` | 4 |
| `po:TreatmentClaim` | `po:proposesTreatment` | `po:Treatment` | 8, 8b |

### 1.4 Specific to subclasses, layer 2

| domain | property | range | CQ |
|---|---|---|---|
| `po:MethodologicalClaim` | `po:aboutTechnique` | `po:Technique` | 5, 7 |
| `po:MethodologicalClaim` | `po:discriminatesBetween` | `po:Condition` | 7 |
| `po:MethodologicalClaim` | `po:hasDiscriminatingPower` | `po:DiscriminatingPower` | 7 |

### 1.5 Specific to subclasses, layer 3

| domain | property | range | CQ |
|---|---|---|---|
| `po:RejectionClaim` | `po:rejects` | `po:Claim` | 3 |
| `po:Claim` | `cito:agreesWith` | `po:Claim` | 6 |
| `po:Claim` | `cito:disagreesWith` | `po:Claim` | 6 |
| `po:Claim` | `cito:updates` | `po:Claim` | 6 |

### 1.6 On value classes

| domain | property | range | CQ |
|---|---|---|---|
| `po:Technique` | `po:hasErrorSource` | `po:ErrorSource` | 5 |

---

## 2 · Datatype properties

| domain | property | range | CQ |
|---|---|---|---|
| `po:CalibratedInterval` | `po:startYear` | `xsd:integer` | 4, 4b |
| `po:CalibratedInterval` | `po:endYear` | `xsd:integer` | 4, 4b |
| `po:CalibratedInterval` | `po:confidenceInterval` | `xsd:string` | 4b |
| `po:Claim` | `po:isNegated` | `xsd:boolean` | 11 |
| `po:AgeClaim` | `po:minAge` | `xsd:integer` | 9 |
| `po:AgeClaim` | `po:maxAge` | `xsd:integer` | 9 |
| `po:ErrorSource` | `po:hasEffect` | `xsd:string` | 5 |
| `po:Specimen` | `po:specimenID` | `xsd:string` | all |

**Why dates are a class and ages are literals.** CQ4b must compare two intervals against each other to detect disagreement, which requires the interval to be an addressable node with comparable bounds. No competency question compares two age estimates, so two literals suffice. Structure is introduced only where a query demands it.

---

## 3 · Property hierarchy

Two superproperties are declared. Both exist to let a single query pattern reach across several subclasses.

### 3.1 `po:proposes`

```turtle
po:proposesCondition  rdfs:subPropertyOf  po:proposes .
po:proposesTreatment  rdfs:subPropertyOf  po:proposes .
po:hasResult          rdfs:subPropertyOf  po:proposes .
```

Lets one query ask *what does this claim put forward?* without knowing which kind of claim it is:

```sparql
SELECT ?claim ?agent ?proposed ?hedge WHERE {
  ?claim a po:Claim ;
         po:aboutSpecimen :sk90 ;
         po:proposes ?proposed ;
         po:heldBy ?agent ;
         po:hedge ?hedge . }
```

One row per assertion made about Sk. 90, across diagnosis, treatment and dating. This query is the clearest single demonstration of the project's thesis, and it exists only because of the superproperty.

### 3.2 `po:engagesWith`

```turtle
cito:agreesWith     rdfs:subPropertyOf  po:engagesWith .
cito:disagreesWith  rdfs:subPropertyOf  po:engagesWith .
cito:updates        rdfs:subPropertyOf  po:engagesWith .
po:rejects          rdfs:subPropertyOf  po:engagesWith .
```

Simplifies CQ6, which otherwise needs a `FILTER(?rel IN (…))` enumeration:

```sparql
SELECT ?claim ?rel ?prior ?agent WHERE {
  ?claim po:engagesWith ?prior .
  ?claim ?rel ?prior .
  ?prior po:declaredIn ?otherSource ; po:heldBy ?agent .
  FILTER(?rel != po:engagesWith) }
```

`po:engagesWith` is the layer-3 marker: any claim that reaches it is a claim about a claim.

### 3.3 Where sub-properties are deliberately **not** used

The observation/claim boundary is **not** a property hierarchy. `po:groundedIn` is a single property between two disjoint classes. Making observation and interpretation two sub-properties of one parent would imply they are two flavours of the same relation, which is precisely the conflation the project argues against.

---

## 4 · Property characteristics

```turtle
po:rejects         a  owl:IrreflexiveProperty .   # no claim rejects itself
po:hedge           a  owl:FunctionalProperty .    # one confidence level per claim
po:underFramework  a  owl:FunctionalProperty .    # one lens per claim
po:observedOn      a  owl:FunctionalProperty .    # an observation is of one specimen
```

`po:underFramework` being functional is a modelling commitment worth defending at the exam: a claim is made *from* one standpoint. Two standpoints on the same content are two claims, which is exactly what CQ8b retrieves.

Note that `po:groundedIn` is **not** functional, one claim may rest on several observations.

---

## 5 · Key axioms

```turtle
po:rejects            rdfs:range   po:Claim .
po:proposesCondition  rdfs:domain  po:DiagnosticClaim .
po:groundedIn         rdfs:domain  po:Claim ;
                      rdfs:range   po:Observation .

po:Specimen     owl:disjointWith  po:Claim .
po:Observation  owl:disjointWith  po:Claim .
```

### What is deliberately absent

There is **no property with `rdfs:domain po:Specimen` and `rdfs:range po:Condition`.**

No path runs from a set of remains to a disease without passing through a `po:DiagnosticClaim` that carries an agent, a framework and a hedge. NCQ1, *what disease did this individual have?*, returns empty because of this absence, not because of a filter.

Reminder for the exam: in **RDFS**, `rdfs:domain` and `rdfs:range` do not constrain, they license entailments, the liberality of RDF. It is only under **OWL 2 with a reasoner** that a misplaced object produces an inconsistency. The axioms above are written to be checked, not merely declared.

---

## 6 · Open design decisions

These are not gaps. They are the material of the pattern-matching section, where alternatives must be presented with their trade-offs.

**D1, range of `po:groundedIn`.**
Currently `po:Observation`. But a `po:RejectionClaim` is often grounded in a methodological argument rather than a direct observation. Widen the range to `po:Observation ⊔ po:Claim`, or introduce a second property `po:groundedInArgument`?
*Trade-off:* a union range keeps one property and one query pattern, but loses the guarantee that grounding bottoms out in evidence.

**D2, domain of `po:usedTechnique`.**
Currently `po:Observation`. A `po:DatingClaim` therefore reaches its technique through `po:groundedIn / po:usedTechnique`. Accept the extra hop, or duplicate the property on `po:Claim`?
*Trade-off:* the hop enforces that every technique use is an observation; the duplicate is shorter to query but lets a claim cite a technique it never applied.

**D3, RESOLVED.** `po:redetermines` (a term coined for this project) and has been withdrawn in favour of **`cito:updates`**, defined as *"The citing entity provides updated information superseding the cited entity"*, exactly the intended sense.

CiTO declares **no domain or range** on its properties, and states why: *"so that this ontology could be easily integrated with other models"*. Using CiTO between **claims** rather than between documents is therefore a designed extension of use, not a stretch, which also settles `cito:agreesWith` and `cito:disagreesWith`, already used the same way.

`cito:corrects` was the near neighbour and was not chosen: correcting an *error* is what `po:RejectionClaim` records; the relation between the two dating claims is supersession. `po:rejects` stays local, because refusing another agent's claim is a distinct act from citing them.


---

## 7 · Decision D4, resolved

`po:underFramework` and `po:framesContent` are now **two properties**, not one.

| property | records | value in this source |
|---|---|---|
| `po:underFramework` | where the **claimant stands** | always `ModernBiomedical` |
| `po:framesContent` | the system of thought the **content** belongs to | `MedievalHumoral` for the mercury claim, `ModernBiomedical` for the rest |

**Why one property could not do both.** A modern study asserting that an individual was treated with an Hg-containing medicine makes a *modern* claim whose *content* belongs to the medieval humoral frame: mercury counted as a medicine because medieval medicine said so. Collapsing the two forced a choice between a false uniformity, everything modern, and CQ8b returning nothing, and an equivocation, the property meaning one thing for the mercury claim and another for the rest.

`po:underFramework` stays functional: a claim is made from one position. `po:framesContent` is deliberately **not** functional, because a claim may frame content belonging to more than one system, and closing that off buys nothing.

**The consequence is sharper than the version it replaces.** The two frames do not coexist as equals; one contains the other. The paper does not look at Sk. 90 from inside the medieval frame, it looks from outside and *represents* that frame. There is no standpoint from which both can be seen externally, and that is the perspectival argument in its strongest form.

**Uniformity as a finding.** Every `po:underFramework` in the A-Box is `ModernBiomedical`. That is not a defect of the data: it records that the source never leaves the modern frame. With a second source written from another standpoint, the column would vary.
