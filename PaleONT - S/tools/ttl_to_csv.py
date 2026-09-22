#!/usr/bin/env python3
"""Export the hand-written A-Box files into the four annotation tables.

This runs ONCE, as a handover. After it, the CSVs are the source of truth for
the A-Box and data/abox_*.ttl stop being edited.

    python3 tools/ttl_to_csv.py

Reads  : data/vocabulary.ttl  data/abox_sk90.ttl  data/abox_rf130.ttl
Writes : data/csv/specimens.csv  observations.csv  claims.csv  intervals.csv

Multi-valued cells are pipe-separated (grounded_in, lesion_types). The long
rdfs:comment rationales are NOT exported: they are project documentation, not
data about a skeleton, and belong in STATO_PROGETTO.md. rdfs:label IS kept.
"""
import csv, os
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef

PO = Namespace("https://w3id.org/paleont/")
EX = Namespace("https://w3id.org/paleont/data/")
CITO = Namespace("http://purl.org/spar/cito/")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "data", "csv")

CLAIM_TYPES = ["DiagnosticClaim", "RejectionClaim", "DatingClaim",
               "AgeClaim", "TreatmentClaim", "MethodologicalClaim"]

# The one polymorphic column: which property carries "what this claim puts
# forward" depends on the claim's type, and the type column disambiguates it.
PROPOSES_BY_TYPE = {
    "DiagnosticClaim":     PO.proposesCondition,
    "TreatmentClaim":      PO.proposesTreatment,
    "DatingClaim":         PO.hasResult,
    "RejectionClaim":      PO.rejects,
    "MethodologicalClaim": PO.aboutTechnique,
    "AgeClaim":            None,          # carries min/max instead
}

def short(term):
    if term is None: return ""
    s = str(term)
    for ns, pre in ((str(EX), "ex:"), (str(PO), "po:"), (str(CITO), "cito:")):
        if s.startswith(ns): return pre + s[len(ns):]
    return s

def joined(g, s, p):
    return "|".join(sorted(short(o) for o in g.objects(s, p)))

def one(g, s, p):
    for o in g.objects(s, p):
        return o.toPython() if isinstance(o, Literal) else short(o)
    return ""

def label(g, s):
    for o in g.objects(s, RDFS.label):
        return str(o)
    return ""

def load():
    g = Graph()
    for f in ("vocabulary", "abox_sk90", "abox_rf130"):
        g.parse(os.path.join(BASE, "data", f + ".ttl"), format="turtle")
    return g

def write(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name:20s} {len(rows):>3} righe")

def main():
    g = load()

    # ---- specimens -----------------------------------------------------
    rows = []
    for s in sorted(g.subjects(RDF.type, PO.Specimen), key=str):
        rows.append([short(s), one(g, s, PO.specimenID), label(g, s),
                     one(g, s, RDFS.comment)])
    write("specimens.csv",
          ["id", "specimen_id", "label", "note"], rows)

    # ---- observations --------------------------------------------------
    rows = []
    for s in sorted(g.subjects(RDF.type, PO.Observation), key=str):
        rows.append([short(s), short(one(g, s, PO.observedOn) or ""),
                     joined(g, s, PO.observesLesionType),
                     one(g, s, PO.onBone), one(g, s, PO.usedTechnique),
                     one(g, s, PO.declaredIn), label(g, s)])
    write("observations.csv",
          ["id", "specimen", "lesion_types", "bone", "technique",
           "source", "label"], rows)

    # ---- intervals -----------------------------------------------------
    rows = []
    for s in sorted(g.subjects(RDF.type, PO.CalibratedInterval), key=str):
        rows.append([short(s), one(g, s, PO.startYear), one(g, s, PO.endYear),
                     one(g, s, PO.confidenceInterval), label(g, s)])
    write("intervals.csv",
          ["id", "start_year", "end_year", "confidence_interval", "label"], rows)

    # ---- claims --------------------------------------------------------
    rows = []
    seen = set()
    for t in CLAIM_TYPES:
        prop = PROPOSES_BY_TYPE[t]
        for s in sorted(g.subjects(RDF.type, PO[t]), key=str):
            if s in seen: continue
            seen.add(s)
            proposes = joined(g, s, prop) if prop is not None else ""
            # several relations per claim: groups separated by ";",
            # targets within a group by "|"
            rels = []
            for p in (CITO.agreesWith, CITO.disagreesWith, CITO.updates):
                tgt = joined(g, s, p)
                if tgt: rels.append(f"{short(p)}>{tgt}")
            rel = ";".join(rels)
            rows.append([
                short(s), t,
                one(g, s, PO.aboutSpecimen),
                proposes,
                one(g, s, PO.minAge), one(g, s, PO.maxAge),
                one(g, s, PO.heldBy),
                one(g, s, PO.underFramework), one(g, s, PO.framesContent),
                one(g, s, PO.hedge), one(g, s, PO.hedgeWording),
                "true" if one(g, s, PO.isNegated) is True else "",
                joined(g, s, PO.groundedIn),
                one(g, s, PO.appliedCorrection),
                joined(g, s, PO.appliedTo),
                joined(g, s, PO.discriminatesBetween),
                one(g, s, PO.hasDiscriminatingPower),
                rel,
                one(g, s, PO.declaredIn), label(g, s)])
    write("claims.csv",
          ["id", "type", "specimen", "proposes", "min_age", "max_age",
           "agent", "standpoint", "frames_content", "hedge", "hedge_wording",
           "negated", "grounded_in", "correction", "applied_to",
           "discriminates_between", "discriminating_power", "relation",
           "source", "label"], rows)

    print(f"\nScritti in {OUT}")

if __name__ == "__main__":
    main()
