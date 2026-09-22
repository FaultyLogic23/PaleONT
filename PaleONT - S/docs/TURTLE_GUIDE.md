# Reading and writing the Turtle

Practical guide to `ontology/paleont.ttl` and `data/vocabulary.ttl`, the two files still written by hand. The A-Box is generated from the CSV and is never edited.

---

## The one fact that makes everything simple

Turtle has exactly one kind of sentence:

```
subject   predicate   object .
```

Three things and a full stop. Classes, axioms, ten-thousand-line ontologies: all of it is that sentence repeated. There is no second syntax to learn, only abbreviations that save retyping the subject.

Three abbreviations cover almost everything:

| sign | meaning | example |
|---|---|---|
| `;` | same subject, new predicate | `ex:sk90 a po:Specimen ; po:specimenID "St. Albani-90" .` |
| `,` | same subject and predicate, new object | `po:discriminatesBetween ex:leprosy , ex:yaws .` |
| `a` | short for `rdf:type` | `ex:obs_01 a po:Observation .` |

The `.` closes the block. Ninety per cent of syntax errors are a missing full stop, or a `;` where a `.` was needed.

---

## Prefixes

```turtle
@prefix po: <https://w3id.org/paleont/> .
@prefix ex: <https://w3id.org/paleont/data/> .
```

A prefix is an abbreviation for a long address. `po:Specimen` is exactly `<https://w3id.org/paleont/Specimen>`, written short.

One convention to hold to:

- `po:` is **the model**: classes, properties, vocabulary. It lives in `paleont.ttl`.
- `ex:` is **the data**: Sk. 90, obs_01, claim_03.

Looking at an identifier tells you which file it belongs in. If `ex:` appears in `paleont.ttl`, data has leaked into the T-Box. If a `po:` term is defined in a data file, part of the model has leaked out.

---

## Declaring a class

```turtle
po:Observation a owl:Class ;
    rdfs:label   "Observation"@en ;
    rdfs:comment "One act of examining a specimen with a technique."@en .
```

- `a owl:Class` says it is a class. That is all that is required.
- `rdfs:label` is the readable name. `@en` is the language.
- `rdfs:comment` is the prose definition.

**Do not skip the comments.** Three concrete reasons: LODE generates the project documentation by reading exactly those fields; a reader will read them instead of guessing from the name; and in two weeks nobody will remember why `Correction` is separate from `ErrorSource`.

A subclass adds one line:

```turtle
po:DiagnosticClaim a owl:Class ;
    rdfs:subClassOf po:Claim ;
    rdfs:label "Diagnostic claim"@en .
```

`rdfs:subClassOf` means every diagnostic claim is also a claim. The practical consequence is the one that saves work: every property declared on `po:Claim` applies to all six subclasses automatically. You write them once.

---

## Declaring a property

```turtle
po:observedOn a owl:ObjectProperty , owl:FunctionalProperty ;
    rdfs:label  "observed on"@en ;
    rdfs:domain po:Observation ;
    rdfs:range  po:Specimen .
```

- `owl:ObjectProperty` points at another thing.
- `owl:DatatypeProperty` points at a value: a number, a string, a date.
- `rdfs:domain` is the type of the **subject**, whatever stands on the left.
- `rdfs:range` is the type of the **object**, whatever stands on the right.

Read the two together as a sentence: *observedOn runs from an Observation to a Specimen*.

The comma in `owl:ObjectProperty , owl:FunctionalProperty` says it is both: an object property, and functional, meaning one observation concerns exactly one specimen.

### What domain and range actually do

Not what you would expect. In RDFS they **forbid nothing**. Put the wrong kind of object on the right and RDFS does not object: it *infers* that the object has the declared type. This is the liberality of RDF, and it is an exam question.

They become checks only under OWL with a reasoner, and only when the two types **cannot coexist**. That is what the `owl:AllDisjointClasses` blocks are for. Without disjointness the reasoner has no way to notice anything, and this ontology learned that the hard way: see D7 in the design decisions, where a wrong domain on `po:declaredIn` silently retyped thirteen observations as claims until disjointness was added and HermiT caught it.

---

## How the pieces connect

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

The specimen is reached twice and no arrow leaves it.

```turtle
ex:sk90_obs_parietal a po:Observation ;
    po:observedOn         ex:sk90 ;
    po:observesLesionType ex:focalSuperficialCavitation .

ex:sk90_claim_treponematosis a po:DiagnosticClaim ;
    po:groundedIn        ex:sk90_obs_parietal ;     <-- the bridge
    po:proposesCondition ex:treponematosis .
```

`po:groundedIn` is the only crossing between evidence and interpretation. To get from `ex:sk90` to `ex:treponematosis` you have to climb back up through a claim, and climbing through it means carrying the agent, the framework and the hedge. You cannot pretend they are not there.

That is why NCQ1 returns nothing. It is not a filter in the query. The road does not exist.

---

## Naming conventions

Hold to these from the first day. Renaming later costs more than deciding now.

| thing | form | example |
|---|---|---|
| class | `PascalCase`, a noun | `po:DiagnosticClaim` |
| property | `camelCase`, a verb phrase | `po:proposesCondition` |
| model individual | `PascalCase` | `po:ModernBiomedical` |
| data individual | `snake_case`, prefixed by specimen | `ex:sk90_claim_01` |

If you cannot phrase something as a verb, it is not a property.

---

## Running the queries

From a terminal, without installing a triple store:

```bash
pip install rdflib owlrl
```

```python
from rdflib import Graph

g = Graph()
g.parse("ontology/paleont.ttl", format="turtle")
g.parse("data/vocabulary.ttl",  format="turtle")
g.parse("data/abox_generated.ttl", format="turtle")

for row in g.query(open("queries/cq02.rq").read()):
    print(row)
```

The files load into **one graph**. They are separate on disk for convenience, not because they are separate worlds.

Three queries return nothing this way and it is not a bug. `cq06.rq`, `cq11.rq` and `thesis.rq` use the superproperties `po:proposes` and `po:engagesWith`, which nobody ever asserts: they have to be inferred. Close the graph under RDFS first:

```python
import owlrl
owlrl.RDFSClosure.RDFS_Semantics(g, False, False, False).closure()
```

`run_tests.py` runs everything both ways, so the queries needing a reasoner are visible as the difference between the two columns.

---

## Mistakes you will make

In order of frequency.

**A `.` where a `;` belonged.** You close the block halfway and the next line becomes a triple with no subject. The parser reports an error on a line that looks fine: look **above** it, not at it.

**An undeclared prefix.** You use `skos:` and forgot the header. Obvious message, two second fix.

**The wrong literal type.** `"1270"` is a string; `1270` is an integer. CQ4b compares years arithmetically, and on strings the comparison does something absurd in silence. No error, just a wrong answer, which is the worst category.

**Data in the T-Box.** If `Sk. 90` appears in `paleont.ttl`, a level has been crossed. The test: replacing the article with another palaeopathology paper, what would you have to rewrite? Whatever stays identical is T-Box.
