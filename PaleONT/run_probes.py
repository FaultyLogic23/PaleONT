#!/usr/bin/env python3
"""Deliberate-error probes.

An ontology that reports "consistent" proves nothing on its own — an empty one
does too. These probes break the model on purpose and record whether the
reasoner notices. Each row is a constraint we claim to enforce, verified.
"""
import os, owlready2
from rdflib import Graph
from owlready2 import sync_reasoner_hermit, OwlReadyInconsistentOntologyError

BASE = os.path.dirname(os.path.abspath(__file__))
g = Graph()
g.parse(f"{BASE}/ontology/paleont.ttl", format="turtle")
for d in ("vocabulary","abox_generated"):
    g.parse(f"{BASE}/data/{d}.ttl", format="turtle")
BASE_TTL = g.serialize(format="turtle")

P = "<https://w3id.org/paleont/"; D = "<https://w3id.org/paleont/data/"

def consistent(extra=""):
    open("/tmp/p.ttl", "w").write(BASE_TTL + "\n" + extra)
    Graph().parse("/tmp/p.ttl", format="turtle").serialize("/tmp/p.owl", format="xml")
    w = owlready2.World(); o = w.get_ontology("file:///tmp/p.owl").load()
    try:
        with o: sync_reasoner_hermit(w, infer_property_values=False, debug=0)
        return True
    except OwlReadyInconsistentOntologyError:
        return False

PROBES = [
 ("baseline — untouched", "", True),
 ("reject a Condition instead of a Claim",
  f"{D}sk90_reject_leprosy> {P}rejects> {D}leprosy> .", False),
 ("two different hedges on one claim",
  f"{D}sk90_claim_age> {P}hedge> {P}Certain> .", False),
 ("two standpoints on one claim",
  f"{D}sk90_claim_age> {P}underFramework> {P}MedievalHumoral> .", False),
 ("one observation on two specimens",
  f"{D}sk90_obs_mercury> {P}observedOn> {D}sk99> . {D}sk99> a {P}Specimen> . "
  f"[] a <http://www.w3.org/2002/07/owl#AllDifferent> ; "
  f"<http://www.w3.org/2002/07/owl#distinctMembers> ({D}sk90> {D}sk99>) .", False),
 ("a Claim used where a Specimen belongs",
  f"{D}sk90_claim_age> {P}aboutSpecimen> {D}sk90_claim_treponematosis> .", False),
 ("a Specimen given a Condition directly (the thing NCQ1 forbids)",
  f"{D}sk90> {P}proposesCondition> {D}leprosy> .", False),
 ("declaredIn on an Observation — WAS a bug, now allowed",
  f"{D}sk90_obs_tibia> {P}declaredIn> {D}schwarz2013> .", True),
 ("two framed contents on one claim — allowed by design",
  f"{D}sk90_claim_mercuryTreatment> {P}framesContent> {P}ModernBiomedical> .", True),
 ("aboutSpecimen on a MethodologicalClaim — D5, now forbidden",
  f"{D}meth_ct> {P}aboutSpecimen> {D}sk90> .", False),
 ("appliedTo on a MethodologicalClaim — the sanctioned way to say it",
  f"{D}meth_ct> {P}appliedTo> {D}sk90> .", True),
 ("a claim both negated and affirmed — D6, isNegated is functional",
  f"{D}rf130_claim_noMercuryTreatment> {P}isNegated> \"false\"^^<http://www.w3.org/2001/XMLSchema#boolean> .", False),
]

print(f"{'probe':62s} {'expected':10s} {'actual':10s}")
print("-" * 86)
ok_all = True
for label, extra, expect_consistent in PROBES:
    actual = consistent(extra)
    ok = actual == expect_consistent
    ok_all &= ok
    e = "consistent" if expect_consistent else "INCONSISTENT"
    a = "consistent" if actual else "INCONSISTENT"
    print(f"{'✓' if ok else '✗'} {label:60s} {e:10s} {a:10s}")
print("-" * 86)
print("all probes behaved as expected" if ok_all else "MISMATCH")
