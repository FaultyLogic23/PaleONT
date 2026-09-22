#!/usr/bin/env python3
"""Rebuild everything from source.  python3 tools/build.py

    data/csv/*.csv  →  data/abox_generated.ttl  →  ontology/paleont_merged.{ttl,owl}
"""
import os, subprocess, sys
from rdflib import Graph
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

subprocess.run([sys.executable, os.path.join(BASE, "tools", "csv_to_ttl.py")], check=True)

g = Graph()
g.parse(os.path.join(BASE, "ontology", "paleont.ttl"), format="turtle")
for f in ("vocabulary", "abox_generated"):
    g.parse(os.path.join(BASE, "data", f + ".ttl"), format="turtle")
g.serialize(os.path.join(BASE, "ontology", "paleont_merged.ttl"), format="turtle")
g.serialize(os.path.join(BASE, "ontology", "paleont_merged.owl"), format="xml")
print(f"{len(g)} triple → ontology/paleont_merged.{{ttl,owl}}")
print("\nOra:  python3 run_tests.py   e   python3 run_probes.py")
