"""The schemas' laws against the ontology of probability distributions.

    uv run --with jsonschema --with pyyaml --with scipy --with numpy --with pytest pytest -q schemas/checker

Each law a parameter file writes is read through the ontology's table alone: the chart whose parameter-file form has the
law's name, its fields, defaults and none token. The law is converted to its family's canonical chart by the ontology's
formulas, and its mean, moments and support are compared with the checker's closed forms. The converter's Bellman-SYM
call is compared with the ontology's coordinates of the same law. Agreement is to the ontology's tolerance for
irrational conversions, 1e-12.

The table and the formula evaluator are copies of a release of ontologies/probability-distributions/, in ontology/;
ONTOLOGY_VERSION and ONTOLOGY_SOURCE pin the release.
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
from pathlib import Path

import numpy as np
import pytest

from bst1 import load_member
from laws import law_from_mapping
from test_checker import LAWS, MEMBERS

HERE = Path(__file__).resolve().parent
ONTOLOGY_VERSION = "0.1.0-draft.1"
ONTOLOGY_SOURCE = "2ef9d5c6d5fd02ee163d05f1a9138d1e3a9560e2a186a0c0e93a8756687d8252"
TOLERANCE = 1e-12

_spec = importlib.util.spec_from_file_location("ontology_formulas", HERE / "ontology" / "formulas.py")
formulas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(formulas)
TABLE = json.loads((HERE / "ontology" / "probability-distributions.json").read_text(encoding="utf-8"))
ROWS = {r["id"]: r for r in TABLE["rows"]}

EXAMPLES = LAWS + [
    {"Degenerate": {}},
    {"Discrete": {"values": [0.5, 1.5], "probs": [0.5, 0.5]}},
    {"Discrete": {"values": [0.6, 1.0, 1.4], "probs": [0.25, 0.5, 0.25]}},
]


def close(a, b) -> bool:
    a, b = float(a), float(b)
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= TOLERANCE * max(1.0, abs(a), abs(b))


def chart_for(name: str) -> dict:
    """The chart the parameter files write the law named `name` in."""
    charts = [r for r in ROWS.values() if r["kind"] == "chart"
              and any(f["head"] == name for f in r.get("written_as", {}).get("parameter-file", []))]
    assert len(charts) == 1, (name, [c["qualified_name"] for c in charts])
    return charts[0]


def root(row: dict) -> dict:
    family = ROWS[row["family"]] if row["kind"] == "chart" else row
    while "subfamily_of" in family:
        family = ROWS[family["subfamily_of"]]
    return family


def read(chart: dict, name: str, params: dict) -> dict:
    """The chart's coordinates of a parameter file's law, from the written form in the table: each field's value, its
    default when left out, and the none token's value where it is written."""
    form = next(f for f in chart["written_as"]["parameter-file"] if f["head"] == name)
    if "arguments" not in form:  # Tabulated: its one field, points, interleaves the two coordinates
        points = np.array(params["points"], dtype=float)
        return {"u": points[:, 0], "q": points[:, 1]}
    defaults = form.get("defaults", {})
    none = form.get("none", {"token": None, "values": {}})

    def value(source: dict, field: str):
        if field not in source:
            return formulas.evaluate(defaults[field], {})
        if source[field] is None:
            return formulas.evaluate(none["values"][field], {})
        return source[field]

    coordinates = {}
    for field, formula in form["arguments"].items():
        assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", formula), "a field must name one coordinate"
        if form.get("per_component"):
            coordinates[formula] = np.array([value(c, field) for c in params["components"]], dtype=float)
        else:
            v = value(params, field)
            coordinates[formula] = np.array(v, dtype=float) if isinstance(v, list) else float(v)
    return coordinates


def canonical(chart: dict, point: dict) -> dict:
    if chart["canonical"]:
        return dict(point)
    env = formulas.evaluate_all(chart.get("to_canonical_where", {}), point)
    return {k: formulas.evaluate(f, env) for k, f in chart["to_canonical"].items()}


def parse_call(text: str):
    """A Bellman-SYM call as (head, arguments), a tuple as a list, a number as a float."""
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|-?inf|-?[0-9.]+(?:e[-+]?[0-9]+)?|[(),]", text)

    def items(i, close_at):
        out = []
        while tokens[i] != close_at:
            v, i = item(i)
            out.append(v)
            if tokens[i] == ",":
                i += 1
        return out, i + 1

    def item(i):
        t = tokens[i]
        if t == "(":
            return items(i + 1, ")")
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", t) and t != "inf":
            args, j = items(i + 2, ")")
            return (t, args), j
        return float(t), i + 1

    value, end = item(0)
    assert end == len(tokens), text
    return value


@pytest.mark.parametrize("mapping", EXAMPLES, ids=[next(iter(m)) + str(i) for i, m in enumerate(EXAMPLES)])
def test_the_ontology_and_the_checker_state_the_same_law(mapping):
    (name, params), = mapping.items()
    law = law_from_mapping(mapping)
    assert law.check() == []
    chart = chart_for(name)
    assert chart["id"] == law.ontology, (name, chart["qualified_name"])
    family = root(chart)
    point = canonical(chart, read(chart, name, params))
    env = formulas.evaluate_all(family.get("where", {}), point)
    props = family["properties"]
    assert close(formulas.evaluate(props["mean"], env), law.moment(1.0)), name
    moments = props.get("moments", {})
    if "formula" in moments:
        orders = (-1.0, 0.5, 2.0, 3.0) if moments["orders"] == "all-real" else (2.0, 3.0)
        for k in orders:
            assert close(formulas.evaluate(moments["formula"], {**env, "k": k}), law.moment(k)), (name, k)
    support = props["support"]
    assert close(formulas.evaluate(support["infimum"], env), law.infimum), name
    assert close(formulas.evaluate(support["supremum"], env), law.supremum), name
    assert close(formulas.evaluate(support["mass_at_infimum"], env), law.mass_at_infimum), name


@pytest.mark.parametrize("mapping", EXAMPLES, ids=[next(iter(m)) + str(i) for i, m in enumerate(EXAMPLES)])
def test_the_converter_writes_the_ontology_coordinates(mapping):
    (name, params), = mapping.items()
    law = law_from_mapping(mapping)
    chart = chart_for(name)
    family = root(chart)
    canonical_chart = ROWS[family["canonical_chart"]]
    call = law.bellman()
    if call is None:
        assert "bellman-sym" not in canonical_chart.get("written_as", {}), name
        return
    head, args = parse_call(call)
    own = read(chart, name, params)
    point = canonical(chart, own)
    forms = chart.get("written_as", {}).get("bellman-sym", [])
    if forms and "arguments" in forms[0]:  # the chart's own spelling: evaluate it at the chart's point
        assert head == forms[0]["head"], (name, call)
        expected = [formulas.evaluate(a, own) for a in forms[0]["arguments"]]
        assert all(close(a, e) for a, e in zip(args, expected)) and len(args) == len(expected), (call, expected)
        return
    canonical_forms = canonical_chart.get("written_as", {}).get("bellman-sym", [])
    if head != "Mixture":  # the canonical chart's spelling, at the canonical point
        assert head == canonical_forms[0]["head"], (name, call)
        expected = [formulas.evaluate(a, point) for a in canonical_forms[0]["arguments"]]
        assert all(close(a, e) for a, e in zip(args, expected)) and len(args) == len(expected), (call, expected)
        return
    # a mixture: each component against the canonical vectors
    weights = point.get("weights", point.get("probs"))
    assert len(args) == len(weights), call
    for j, (weight, component) in enumerate(args):
        assert close(weight, weights[j]), (call, j)
        if isinstance(component, float):  # a number: a point mass of the finite discrete law
            assert close(component, point["values"][j]), (call, j)
            continue
        sub_head, sub_args = component
        assert close(sub_args[0], point["mu"][j]) and close(sub_args[1], point["sigma"][j]), (call, j)
        if sub_head == "TruncatedLogNormal":
            assert close(sub_args[2], point["l"][j]) and close(sub_args[3], point["u"][j]), (call, j)
        else:
            assert sub_head == "LogNormal", call
            assert point.get("l", np.zeros(len(weights)))[j] == 0 and point.get("u", np.full(len(weights), np.inf))[j] == np.inf


def test_the_members_laws_agree_with_the_ontology():
    for path in sorted(MEMBERS.glob("*.yaml")):
        member = load_member(path)
        for shock in ("permanent_shock", "employed_shock"):
            mapping = member.data["income"][shock]
            test_the_ontology_and_the_checker_state_the_same_law(mapping)
            test_the_converter_writes_the_ontology_coordinates(mapping)


def test_the_vendored_table_is_the_pinned_release():
    assert TABLE["ontology"]["version"] == ONTOLOGY_VERSION
    assert TABLE["ontology"]["source_sha256"] == ONTOLOGY_SOURCE
