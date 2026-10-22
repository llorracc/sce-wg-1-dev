"""The standing check of conventions.md: every name the shock-law validator fixes has a row there.

    uv run --with jsonschema --with pyyaml --with scipy --with numpy --with pytest pytest -q schemas/checker

A row names the ontology's chart the spelling writes and the convention it follows, or why it departs; a name enters a
validator only with its row.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parent.parent


def registered() -> set[str]:
    """The names in the first column of the registry's tables."""
    names = set()
    for line in (SCHEMAS / "conventions.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| `"):
            names.update(re.findall(r"`([^`]+)`", line.split("|")[1]))
    return names


def fixed_by_the_shock_law_validator() -> set[str]:
    """Each accepted law's name and the names of its fields, its components' fields included."""
    schema = json.loads((SCHEMAS / "shock-laws.schema.json").read_text(encoding="utf-8"))
    defs = schema["$defs"]
    names = set()
    for ref in defs["ShockLaw"]["oneOf"]:
        law = defs[ref["$ref"].rsplit("/", 1)[1]]
        (name, body), = law["properties"].items()
        names.add(name)
        for field, spec in body.get("properties", {}).items():
            names.add(field)
            names.update(spec.get("items", {}).get("properties", {}))
    return names


def test_every_name_of_the_shock_law_validator_has_a_row():
    missing = fixed_by_the_shock_law_validator() - registered()
    assert not missing, f"names with no row in conventions.md: {sorted(missing)}"


def test_every_row_names_an_ontology_chart_or_says_there_is_none():
    for line in (SCHEMAS / "conventions.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| `"):
            ontology = line.split("|")[3]
            assert "PD_" in ontology or "written form" in ontology, line
