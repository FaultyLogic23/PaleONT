# Error provocation

Each file asserts ONE deliberate error. Load it together with
`ontology/paleopath.ttl` in Protégé and run HermiT. Each must make the
ontology **inconsistent**, and the explanation must name the axiom given below.

If a provocation does NOT fire, the ontology is missing a constraint.

| File | Error | Axiom that must catch it |
|------|-------|--------------------------|
| p01-individual-is-claim.ttl | a skeleton typed as a claim | AllDisjointClasses (top level) |
| p02-two-hedges.ttl | one claim, two different hedges | hasHedge exactly 1 |
| p03-claim-and-exclude.ttl | claims and excludes the same disease | claimsDisease propertyDisjointWith excludesDisease |
| p04-observation-is-claim.ttl | an observation typed as a claim | AllDisjointClasses (top level) |

## Why some errors CANNOT be provoked

Under the open world assumption, a **missing** value is not an error.

- A `Claim` with no `hasHedge` does **not** fire, because OWL assumes the hedge
  exists and was simply not written down. Only *two different* hedges violate
  `exactly 1`.
- A `DatingClaim` with no interval does **not** fire, for the same reason.

This is not a gap in the model — it is what open-world reasoning means, and it
is why **SHACL** would be the right tool if we needed to reject incomplete input.
Worth one line in the presentation.
