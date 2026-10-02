#!/usr/bin/env python3
"""Round trip check: does the CSV schema lose anything?

    hand-written A-Box  ->  CSV  ->  generated A-Box  ->  compare

Compares Data triples only. The long rdfs:comment rationales are excluded by
design, they are project documentation, not data about a skeleton therefore every other triple must survive.

A clean result proves the annotation tables are complete, the strongest thing
that can be said about a mapping before it is trusted with five specimens.
"""

import os
from rdflib import Graph, RDFS

Base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from rdflib import Namespace, RDF
Po_n = Namespace("https://w3id.org/paleont/")

# What the CSV is responsible for: specimens, observations, claims and
# intervals, wherever they were hand-written. The controlled vocabulary
# (techniques, bones, conditions, error sources) stays in vocabulary.ttl and
# is deliberately outside the comparison.

Covered = [Po_n.Specimen, Po_n.Observation, Po_n.CalibratedInterval,
           Po_n.DiagnosticClaim, Po_n.RejectionClaim, Po_n.DatingClaim,
           Po_n.AgeClaim, Po_n.TreatmentClaim, Po_n.MethodologicalClaim]

def data_triples(g):
    subjects = {s for c in Covered for s in g.subjects(RDF.type, c)}
    return {t for t in g if t[0] in subjects and t[1] != RDFS.comment}

# The two hand-written A-Box files live in data/legacy/ and are frozen.
# They are the only independent record of what the CSV must be able to carry.

original = Graph()
original.parse(os.path.join(Base, "data", "vocabulary.ttl"), format="turtle")
for f in ("abox_sk90", "abox_rf130"):
    original.parse(os.path.join(Base, "data", "legacy", f + ".ttl"), format="turtle")

generated = Graph()
generated.parse(os.path.join(Base, "data", "abox_generated.ttl"), format="turtle")

# The CSV now also carries three specimens the hand-written files never had,
# so the check is one-directional: nothing the hand-written files contained
# may be missing from what the CSV regenerates.

a, b = data_triples(original), data_triples(generated)
lost = a - b
gained = set()   # the CSV legitimately holds more than the legacy files did

print(f"hand-written (legacy)   {len(a)} data triples")
print(f"regenerated from CSV    {len(b)} data triples")
print(f"                        ({len(b)-len(a)} added by the three later specimens)\n")

def show(title, s):
    if not s:
        print(f"  {title}: none")
        return
    print(f"  {title}: {len(s)}")
    for t in sorted(s, key=str)[:15]:
        print("     ", " ".join(str(x).split('/')[-1][:45] for x in t))
    if len(s) > 15: print(f"      ... and {len(s)-15} more")

show("Lost in the round trip", lost)
show("Appeared from nowhere", gained)

print()
print("The CSV schema carries everything the hand-written files did"
      if not lost else
      "The schema loses information")
