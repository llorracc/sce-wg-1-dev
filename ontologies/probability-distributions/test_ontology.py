"""Tests of the ontology of probability distributions.

    uv run --with pyyaml --with jsonschema --with numpy --with rdflib --with pytest pytest -q

The generator already refuses a source that fails its checks; these tests run it, and then check the math: every
conversion round-trips, every mean and moment the rows state agrees with the measure the row defines, every constraint
holds on its subfamily's charts, every boundary and reduction meets the family it names, the generated files are
current, and the Turtle file parses as RDF. Points are drawn from each coordinate's domain and kept where the chart's
joint conditions hold; agreement is to the relative tolerance of irrational conversions, 1e-12. A point at which a
truncation keeps less than MIN_MASS of the base measure is skipped: there a difference of two values of Φ loses the
precision that tolerance asks for, though the formulas remain right.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

import formulas
import generate

TOLERANCE = 1e-12
INF = math.inf
SAMPLES = {
    "real": (-1.3, 0.0, 0.45),
    "positive": (0.05, 0.3, 0.9),
    "extended-real": (-INF, -2.0, 0.5, INF),
    "extended-nonnegative": (0.0, 0.6, 1.4, INF),
}
MIN_MASS = 1e-3  # the least mass a truncation may keep at a tested point
CUTOFF = 40.0  # the standard normal's mass beyond this many standard deviations is negligible
PANEL, NODES = 0.5, 16  # composite Gauss-Legendre: panel width and nodes per panel


@pytest.fixture(scope="module")
def table():
    source, digest = generate.load()
    return generate.build(source, digest)


@pytest.fixture(scope="module")
def rows(table):
    return {r["id"]: r for r in table["rows"]}


def close(a: float, b: float) -> bool:
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= TOLERANCE * max(1.0, abs(a), abs(b))


def points(chart: dict, coordinates: list[dict] | None = None):
    """Every combination of each coordinate's sample values at which the chart's joint conditions hold."""
    coordinates = chart["coordinates"] if coordinates is None else coordinates
    names = [c["name"] for c in coordinates]
    for values in itertools.product(*(SAMPLES[c["domain"]] for c in coordinates)):
        p = dict(zip(names, values))
        if all(formulas.evaluate(c, p) for c in chart.get("domain_conditions", [])):
            yield p


def root(rows: dict, family: dict) -> dict:
    while "subfamily_of" in family:
        family = rows[family["subfamily_of"]]
    return family


def charts_of(rows: dict, family: dict) -> list[dict]:
    return [rows[c] for c in family["charts"]]


def to_canonical(chart: dict, point: dict) -> dict:
    if chart["canonical"]:
        return dict(point)
    env = formulas.evaluate_all(chart.get("to_canonical_where", {}), point)
    return {k: formulas.evaluate(f, env) for k, f in chart["to_canonical"].items()}


def from_canonical(chart: dict, point: dict) -> dict:
    if chart["canonical"]:
        return dict(point)
    env = formulas.evaluate_all(chart.get("from_canonical_where", {}), point)
    return {k: formulas.evaluate(f, env) for k, f in chart["from_canonical"].items()}


def family_env(family: dict, point: dict) -> dict:
    """A point of the canonical chart, with the family's auxiliary quantities."""
    return formulas.evaluate_all(family.get("where", {}), point)


def Phi(z: float) -> float:
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


class Degenerate(Exception):
    """A point whose truncation keeps too little mass to test at the tolerance."""


def standard_normal_rule(lower: float, upper: float) -> tuple[np.ndarray, np.ndarray]:
    """Nodes and weights for the standard normal conditioned on [lower, upper], by composite Gauss-Legendre."""
    if Phi(upper) - Phi(lower) < MIN_MASS:
        raise Degenerate
    a, b = max(lower, -CUTOFF), min(upper, CUTOFF)
    panels = max(1, math.ceil((b - a) / PANEL))
    edges = np.linspace(a, b, panels + 1)
    x, w = np.polynomial.legendre.leggauss(NODES)
    mid, half = (edges[:-1] + edges[1:]) / 2, (edges[1:] - edges[:-1]) / 2
    z = (mid[:, None] + half[:, None] * x[None, :]).ravel()
    weights = (half[:, None] * w[None, :]).ravel() * np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
    return z, weights / (Phi(upper) - Phi(lower))


def quadrature(rows: dict, family: dict, point: dict) -> tuple[np.ndarray, np.ndarray]:
    """Nodes and weights integrating against the family's measure at a point of its canonical chart, built from the
    row's own definition: its atoms, or its base measure carried through its operators. Conditioning on an interval
    after increasing maps is conditioning the base on the interval's preimage, since f⁻¹(f(A)) = A."""
    props = family["properties"]
    if "atoms" in props:
        env = family_env(family, point)
        at = np.array([formulas.evaluate(a["at"], env) for a in props["atoms"]], dtype=float)
        mass = np.array([formulas.evaluate(a["mass"], env) for a in props["atoms"]], dtype=float)
        return at, mass
    built = family["built_from"]
    assert rows[built["base"]]["name"] == "standard-normal", "no quadrature for this base measure"
    env = family_env(family, point)
    forward, inverse = [], []  # the increasing maps applied so far, and their inverses
    lower, upper = -INF, INF  # the base's conditioning interval
    for step in built["operators"]:
        op = rows[step["operator"]]["name"]
        args = {k: formulas.evaluate(f, env) for k, f in step["arguments"].items()}
        if op == "affine-pushforward":
            a, b = args["location"], args["scale"]
            assert b > 0
            forward.append(lambda z, a=a, b=b: a + b * z)
            inverse.append(lambda y, a=a, b=b: (y - a) / b)
        elif op == "exponential-pushforward":
            forward.append(np.exp)
            inverse.append(lambda y: formulas.FUNCTIONS["log"](y))
        elif op == "interval-conditioning":
            lo, hi = args["lower"], args["upper"]
            for g in reversed(inverse):
                lo, hi = g(lo), g(hi)
            lower, upper = max(lower, lo), min(upper, hi)
        else:
            raise AssertionError(f"no quadrature rule for the operator {op}")
    z, w = standard_normal_rule(lower, upper)
    for f in forward:
        z = f(z)
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
    checked = 0
    for fam in rows.values():
        if fam["kind"] != "family":
            continue
        top = root(rows, fam)
        canonical = rows[top["canonical_chart"]]
        for chart in charts_of(rows, fam):
            if chart["canonical"]:
                continue
            for p in points(chart):
                back = from_canonical(chart, to_canonical(chart, p))
                assert all(close(back[k], p[k]) for k in p), (chart["qualified_name"], p, back)
                checked += 1
            if "subfamily_of" in fam:
                continue  # a reduced chart reaches only its subfamily
            for c in points(canonical):
                if "covers" in chart and not formulas.evaluate(chart["covers"], c):
                    continue
                again = to_canonical(chart, from_canonical(chart, c))
                assert all(close(again[k], c[k]) for k in c), (chart["qualified_name"], c, again)
    assert checked > 0


def test_means_and_moments_agree_with_the_measures(rows):
    checked = 0
    for fam in root_families(rows):
        props = fam["properties"]
        canonical = rows[fam["canonical_chart"]]
        for p in points(canonical):
            try:
                x, w = quadrature(rows, fam, p)
            except Degenerate:
                continue
            env = family_env(fam, p)
            assert close(float(w.sum()), 1.0), (fam["name"], p)
            if "mean" in props:
                assert close(float(w @ x), formulas.evaluate(props["mean"], env)), (fam["name"], p)
                checked += 1
            moments = props.get("moments", {})
            if "formula" in moments:
                orders = (1, 2, 3) if moments["orders"] == "nonnegative-integers" else (-1.0, 0.5, 1, 2, 3)
                for k in orders:
                    expected = formulas.evaluate(moments["formula"], {**env, "k": k})
                    assert close(float(w @ x**k), expected), (fam["name"], p, k)
                    checked += 1
            support = props.get("support")
            if support:
                lo = formulas.evaluate(support["infimum"], env)
                hi = formulas.evaluate(support["supremum"], env)
                assert np.all((x >= lo) & (x <= hi)), (fam["name"], p)
                at_lo = float(w[x == lo].sum())
                assert close(at_lo, formulas.evaluate(support["mass_at_infimum"], env)), (fam["name"], p)
    assert checked > 0


def test_coordinates_mean_what_they_say(rows):
    """A coordinate stated as an expectation equals that expectation under the law at the point, by quadrature."""
    checked = 0
    for fam in rows.values():
        if fam["kind"] != "family":
            continue
        top = root(rows, fam)
        for chart in charts_of(rows, fam):
            stated = [c for c in chart["coordinates"] if "as_expectation" in c]
            if not stated:
                continue
            for p in points(chart):
                try:
                    x, w = quadrature(rows, top, to_canonical(chart, p))
                except Degenerate:
                    continue
                expect = {"E": lambda g: float(w @ g(x))}
                for c in stated:
                    value = formulas.evaluate(c["as_expectation"], expect)
                    assert close(value, p[c["name"]]), (chart["qualified_name"], c["name"], p, value)
                    checked += 1
    assert checked > 0


def test_constraints_hold_on_their_subfamilies(rows):
    for fam in rows.values():
        if fam["kind"] != "family" or "subfamily_of" not in fam:
            continue
        top = root(rows, fam)
        for constraint in (rows[c] for c in fam["constraints"]):
            prop = rows[constraint["property"]]["name"]
            target = formulas.evaluate(constraint["value"], {})
            for chart in charts_of(rows, fam):
                for p in points(chart):
                    value = formulas.evaluate(top["properties"][prop], family_env(top, to_canonical(chart, p)))
                    assert constraint["relation"] == "=" and close(value, target), (chart["qualified_name"], p)


def _same_law(rows, fam: dict, here: dict, other: dict, there: dict, label) -> None:
    """The family at a canonical point and another family at one of its own agree in mean and moments."""
    mine, theirs = family_env(fam, here), family_env(other, there)
    assert close(formulas.evaluate(fam["properties"]["mean"], mine),
                 formulas.evaluate(other["properties"]["mean"], theirs)), label
    f = fam["properties"].get("moments", {}).get("formula")
    g = other["properties"].get("moments", {}).get("formula")
    if f and g:
        for k in (1, 2, 3):
            assert close(formulas.evaluate(f, {**mine, "k": k}), formulas.evaluate(g, {**theirs, "k": k})), (label, k)


def test_boundaries_meet_the_family_they_name(rows):
    for fam in root_families(rows):
        canonical = rows[fam["canonical_chart"]]
        for b in fam.get("boundaries", []):
            coordinate, _, value = b["where"].partition(" = ")
            chart = rows[b["chart"]]
            free = [c for c in canonical["coordinates"] if c["name"] != coordinate]
            for p in points({"coordinates": free}, free):
                here = {**p, coordinate: formulas.evaluate(value, p)}
                there = to_canonical(chart, {c["name"]: p[c["name"]] for c in chart["coordinates"]})
                _same_law(rows, fam, here, rows[b["family"]], there, (fam["name"], b, p))


def test_reductions_meet_the_family_they_name(rows):
    checked = 0
    for fam in root_families(rows):
        canonical = rows[fam["canonical_chart"]]
        for r in fam.get("reductions", []):
            chart = rows[r["chart"]]
            for p in points(canonical):
                if not formulas.evaluate(r["when"], family_env(fam, p)):
                    continue
                there = to_canonical(chart, {c["name"]: p[c["name"]] for c in chart["coordinates"]})
                _same_law(rows, fam, p, rows[r["family"]], there, (fam["name"], r, p))
                x, w = quadrature(rows, fam, p)  # a vacuous truncation keeps all the mass
                assert close(float(w @ x), formulas.evaluate(rows[r["family"]]["properties"]["mean"],
                                                             family_env(rows[r["family"]], there)))
                checked += 1
    assert checked > 0 or not any(f.get("reductions") for f in root_families(rows))


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
