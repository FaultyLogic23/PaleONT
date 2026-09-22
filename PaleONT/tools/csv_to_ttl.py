#!/usr/bin/env python3
"""Generate the A-Box from the annotation tables.

    python3 tools/csv_to_ttl.py

Reads  : data/csv/*.csv
Writes : data/abox_generated.ttl

This is the Python reference implementation of what the RML mapping must do.
Keep it: when the RML mapping is written, its output must match this file, so
this script doubles as the specification and the test oracle for the mapping.
"""
import csv, os
from rdflib import Graph, Namespace, RDF, RDFS, Literal, XSD

PO = Namespace("https://w3id.org/paleont/")
EX = Namespace("https://w3id.org/paleont/data/")
CITO = Namespace("http://purl.org/spar/cito/")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "data", "csv")

# The polymorphic column resolved by the type column, the discriminator that
# makes one column legitimate here where it was not in the T-Box.
PROPOSES_BY_TYPE = {
    "DiagnosticClaim":     PO.proposesCondition,
    "TreatmentClaim":      PO.proposesTreatment,
    "DatingClaim":         PO.hasResult,
    "RejectionClaim":      PO.rejects,
    "MethodologicalClaim": PO.aboutTechnique,
    "AgeClaim":            None,
}

def iri(token):
    token = token.strip()
    if not token: return None
    if token.startswith("ex:"):   return EX[token[3:]]
    if token.startswith("po:"):   return PO[token[3:]]
    if token.startswith("cito:"): return CITO[token[5:]]
    return EX[token]

def each(cell):
    return [t for t in (cell or "").split("|") if t.strip()]

def rows(name):
    with open(os.path.join(CSV, name), encoding="utf-8") as fh:
        yield from csv.DictReader(fh)

def add(g, s, p, o):
    if o is not None and o != "":
        g.add((s, p, o))

def main():
    g = Graph()
    g.bind("po", PO); g.bind("ex", EX); g.bind("cito", CITO)

    for r in rows("specimens.csv"):
        s = iri(r["id"])
        g.add((s, RDF.type, PO.Specimen))
        add(g, s, PO.specimenID, Literal(r["specimen_id"]) if r["specimen_id"] else None)
        add(g, s, RDFS.label, Literal(r["label"], lang="en") if r["label"] else None)
        add(g, s, RDFS.comment, Literal(r["note"], lang="en") if r["note"] else None)

    for r in rows("observations.csv"):
        s = iri(r["id"])
        g.add((s, RDF.type, PO.Observation))
        add(g, s, PO.observedOn, iri(r["specimen"]))
        for lt in each(r["lesion_types"]):
            g.add((s, PO.observesLesionType, iri(lt)))
        add(g, s, PO.onBone, iri(r["bone"]))
        add(g, s, PO.usedTechnique, iri(r["technique"]))
        add(g, s, PO.declaredIn, iri(r["source"]))
        add(g, s, RDFS.label, Literal(r["label"], lang="en") if r["label"] else None)

    for r in rows("intervals.csv"):
        s = iri(r["id"])
        g.add((s, RDF.type, PO.CalibratedInterval))
        add(g, s, PO.startYear, Literal(int(r["start_year"]), datatype=XSD.integer) if r["start_year"] else None)
        add(g, s, PO.endYear,   Literal(int(r["end_year"]),   datatype=XSD.integer) if r["end_year"] else None)
        add(g, s, PO.confidenceInterval, Literal(r["confidence_interval"]) if r["confidence_interval"] else None)
        add(g, s, RDFS.label, Literal(r["label"], lang="en") if r["label"] else None)

    for r in rows("claims.csv"):
        s = iri(r["id"])
        g.add((s, RDF.type, PO[r["type"]]))
        prop = PROPOSES_BY_TYPE[r["type"]]
        if prop is not None:
            for t in each(r["proposes"]):
                g.add((s, prop, iri(t)))
        add(g, s, PO.aboutSpecimen, iri(r["specimen"]))
        add(g, s, PO.minAge, Literal(int(r["min_age"]), datatype=XSD.integer) if r["min_age"] else None)
        add(g, s, PO.maxAge, Literal(int(r["max_age"]), datatype=XSD.integer) if r["max_age"] else None)
        add(g, s, PO.heldBy, iri(r["agent"]))
        add(g, s, PO.underFramework, iri(r["standpoint"]))
        add(g, s, PO.framesContent, iri(r["frames_content"]))
        add(g, s, PO.hedge, iri(r["hedge"]))
        add(g, s, PO.hedgeWording, Literal(r["hedge_wording"]) if r["hedge_wording"] else None)
        if r["negated"].strip().lower() == "true":
            g.add((s, PO.isNegated, Literal(True)))
        for o in each(r["grounded_in"]):
            g.add((s, PO.groundedIn, iri(o)))
        add(g, s, PO.appliedCorrection, iri(r["correction"]))
        for o in each(r["applied_to"]):
            g.add((s, PO.appliedTo, iri(o)))
        for c in each(r["discriminates_between"]):
            g.add((s, PO.discriminatesBetween, iri(c)))
        add(g, s, PO.hasDiscriminatingPower, iri(r["discriminating_power"]))
        for group in (r["relation"] or "").split(";"):
            if not group.strip(): continue
            pred, _, targets = group.partition(">")
            for t in each(targets):
                g.add((s, iri(pred), iri(t)))
        add(g, s, PO.declaredIn, iri(r["source"]))
        add(g, s, RDFS.label, Literal(r["label"], lang="en") if r["label"] else None)

    out = os.path.join(BASE, "data", "abox_generated.ttl")
    header = ("# PaleONT, A-Box, GENERATED from data/csv/*.csv\n"
              "# Do not edit. Change the CSV and regenerate.\n"
              "#   python3 tools/csv_to_ttl.py\n\n")
    body = g.serialize(format="turtle")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(header + body)
    print(f"{len(g)} triple → data/abox_generated.ttl")

if __name__ == "__main__":
    main()
