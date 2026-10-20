"""Tests of the ontology of probability distributions.

    uv run --with pyyaml --with jsonschema --with numpy --with rdflib --with pytest pytest -q

The generator already refuses a source that fails its checks; these tests run it, and then check the math: every
conversion round-trips, every mean and moment the rows state agrees with the measure the row defines, every constraint
holds on its subfamily's charts, every boundary meets the family it names, the generated files are current, and the
Turtle file parses as RDF. Points are drawn from each coordinate's domain; agreement is to the relative tolerance of
irrational conversions, 1e-12.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

import formulas
import generate

TOLERANCE = 1e-12
SAMPLES = {"real": (-1.3, 0.0, 0.45), "positive": (0.05, 0.3, 0.9)}
NODES = 160  # Gauss-Hermite nodes for the standard normal


@pytest.fixture(scope="module")
def table():
    source, digest = generate.load()
    return generate.build(source, digest)


@pytest.fixture(scope="module")
def rows(table):
    return {r["id"]: r for r in table["rows"]}


def close(a: float, b: float) -> bool:
    return abs(a - b) <= TOLERANCE * max(1.0, abs(a), abs(b))


def points(coordinates: list[dict]):
    """Every combination of each coordinate's sample values."""
    names = [c["name"] for c in coordinates]
    for values in itertools.product(*(SAMPLES[c["domain"]] for c in coordinates)):
        yield dict(zip(names, values))


def root(rows: dict, family: dict) -> dict:
    while "subfamily_of" in family:
        family = rows[family["subfamily_of"]]
    return family


def charts_of(rows: dict, family: dict) -> list[dict]:
    return [rows[c] for c in family["charts"]]


def to_canonical(chart: dict, point: dict) -> dict:
    if chart["canonical"]:
        return dict(point)
    return {k: formulas.evaluate(f, point) for k, f in chart["to_canonical"].items()}


def from_canonical(chart: dict, point: dict) -> dict:
    if chart["canonical"]:
        return dict(point)
    return {k: formulas.evaluate(f, point) for k, f in chart["from_canonical"].items()}


def quadrature(rows: dict, family: dict, point: dict) -> tuple[np.ndarray, np.ndarray]:
    """Nodes and weights integrating against the family's measure at a point of its canonical chart, built from its
    definition: its atoms, or its base measure carried through its operators."""
    props = family["properties"]
    if "atoms" in props:
        at = np.array([formulas.evaluate(a["at"], point) for a in props["atoms"]], dtype=float)
        mass = np.array([formulas.evaluate(a["mass"], point) for a in props["atoms"]], dtype=float)
        return at, mass
    built = family["built_from"]
    base = rows[built["base"]]
    assert base["name"] == "standard-normal", f"no quadrature for the base measure {base['name']}"
    z, w = np.polynomial.hermite_e.hermegauss(NODES)
    w = w / math.sqrt(2.0 * math.pi)
    for step in built["operators"]:
        op = rows[step["operator"]]
        args = {k: formulas.evaluate(f, point) for k, f in step["arguments"].items()}
        if op["name"] == "affine-pushforward":
            z = args["location"] + args["scale"] * z
        elif op["name"] == "exponential-pushforward":
            z = np.exp(z)
        else:
            raise AssertionError(f"no quadrature rule for the operator {op['name']}")
    return z, w


def root_families(rows):
    return [r for r in rows.values() if r["kind"] == "family" and "subfamily_of" not in r]


def test_generated_files_are_current():
    assert generate.main(["--check"]) == 0


def test_identifiers_are_well_formed_and_unique(table):
    ids = [r["id"] for r in table["rows"]]
    assert len(ids) == len(set(ids))
    assert all(len(i) == 10 and i.startswith("PD_") and i[3:].isdigit() for i in ids)
    assert not set(ids) & set(table["retired"])


def test_every_family_has_its_charts_and_a_canonical_one(rows):
    for fam in rows.values():
        if fam["kind"] != "family":
            continue
        for c in fam["charts"]:
            assert rows[c]["family"] == fam["id"]
        if "subfamily_of" not in fam:
            canonical = [rows[c] for c in fam["charts"] if rows[c]["canonical"]]
            assert [c["id"] for c in canonical] == [fam["canonical_chart"]]


def test_conversions_round_trip(rows):
    for fam in rows.values():
        if fam["kind"] != "family":
            continue
        top = root(rows, fam)
        canonical = rows[top["canonical_chart"]]
        for chart in charts_of(rows, fam):
            if chart["canonical"]:
                continue
            for p in points(chart["coordinates"]):
                back = from_canonical(chart, to_canonical(chart, p))
                assert all(close(back[k], p[k]) for k in p), (chart["qualified_name"], p, back)
            if "subfamily_of" in fam:
                continue  # a reduced chart reaches only its subfamily
            for c in points(canonical["coordinates"]):
                if "covers" in chart and not formulas.evaluate(chart["covers"], c):
                    continue
                again = to_canonical(chart, from_canonical(chart, c))
                assert all(close(again[k], c[k]) for k in c), (chart["qualified_name"], c, again)


def test_means_and_moments_agree_with_the_measures(rows):
    checked = 0
    for fam in root_families(rows):
        props = fam["properties"]
        canonical = rows[fam["canonical_chart"]]
        for p in points(canonical["coordinates"]):
            x, w = quadrature(rows, fam, p)
            assert close(float(w.sum()), 1.0), fam["name"]
            if "mean" in props:
                assert close(float(w @ x), formulas.evaluate(props["mean"], p)), (fam["name"], p)
                checked += 1
            moments = props.get("moments", {})
            if "formula" in moments:
                orders = (1, 2, 3) if moments["orders"] == "nonnegative-integers" else (-1.0, 0.5, 1, 2, 3)
                for k in orders:
                    expected = formulas.evaluate(moments["formula"], {**p, "k": k})
                    assert close(float(w @ x**k), expected), (fam["name"], p, k)
                    checked += 1
            support = props.get("support")
            if support:
                lo = formulas.evaluate(support["infimum"], p)
                hi = formulas.evaluate(support["supremum"], p)
                assert np.all((x >= lo) & (x <= hi)), fam["name"]
                at_lo = float(w[x == lo].sum())
                assert close(at_lo, formulas.evaluate(support["mass_at_infimum"], p)), fam["name"]
                assert (at_lo > 0) == support["infimum_attained"], fam["name"]
    assert checked > 0


def test_constraints_hold_on_their_subfamilies(rows):
    for fam in rows.values():
        if fam["kind"] != "family" or "subfamily_of" not in fam:
            continue
        top = root(rows, fam)
        for constraint in (rows[c] for c in fam["constraints"]):
            prop = rows[constraint["property"]]["name"]
            formula = top["properties"][prop]
            target = formulas.evaluate(constraint["value"], {})
            for chart in charts_of(rows, fam):
                for p in points(chart["coordinates"]):
                    value = formulas.evaluate(formula, to_canonical(chart, p))
                    assert constraint["relation"] == "=" and close(value, target), (chart["qualified_name"], p)


def test_boundaries_meet_the_family_they_name(rows):
    for fam in root_families(rows):
        canonical = rows[fam["canonical_chart"]]
        for b in fam.get("boundaries", []):
            coordinate, _, value = b["where"].partition(" = ")
            other = rows[b["family"]]
            chart = rows[b["chart"]]
            free = [c for c in canonical["coordinates"] if c["name"] != coordinate]
            for p in points(free):
                here = {**p, coordinate: formulas.evaluate(value, p)}
                there = to_canonical(chart, {c["name"]: p[c["name"]] for c in chart["coordinates"]})
                for prop in ("mean",):
                    assert close(formulas.evaluate(fam["properties"][prop], here),
                                 formulas.evaluate(other["properties"][prop], there)), (fam["name"], b, p)
                mine = fam["properties"].get("moments", {}).get("formula")
                theirs = other["properties"].get("moments", {}).get("formula")
                if mine and theirs:
                    for k in (1, 2, 3):
                        assert close(formulas.evaluate(mine, {**here, "k": k}),
                                     formulas.evaluate(theirs, {**there, "k": k})), (fam["name"], b, p, k)


def test_written_forms_and_cross_references(table, rows):
    formats = set(table["ontology"]["formats"])
    for chart in (r for r in rows.values() if r["kind"] == "chart"):
        assert set(chart.get("written_as", {})) <= formats
        for x in chart.get("cross_references", []):
            assert x["iri"].startswith(tuple(table["ontology"]["prefixes"].values()))


def test_the_turtle_file_parses():
    rdflib = pytest.importorskip("rdflib")
    graph = rdflib.Graph()
    graph.parse(generate.TURTLE, format="turtle")
    table = generate.build(*generate.load())
    ns = table["ontology"]["namespace"]
    owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
    for row in table["rows"]:
        subject = rdflib.URIRef(ns + row["id"])
        assert (subject, rdflib.RDF.type, owl.NamedIndividual) in graph, row["id"]
        assert (subject, rdflib.RDFS.label, None) in graph, row["id"]
    ontologies = list(graph.subjects(rdflib.RDF.type, owl.Ontology))
    assert ontologies == [rdflib.URIRef(ns.rstrip("/"))]
