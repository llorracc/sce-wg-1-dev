"""The standing check of the Rosetta Stones in schemas/rosetta/.

    uv run --with jsonschema --with pyyaml --with scipy --with numpy --with pytest pytest -q schemas/checker

Each stone's lexicon has a row for every parameter of the stage file and every key of the parameter file, and its cards
parse, carry the fields of a card, name only the stage's method targets, and give each part a whole-stage handler covers
one of Bellman's verdicts, with a handler of its own exactly where the whole-stage handler cannot take it. A parameter or key enters the family only with
its row in every stone.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

SCHEMAS = Path(__file__).resolve().parent.parent
STONES = ["hark", "quantecon-jax"]

# The stage file's parameters, by the symbol the lexicons write them in, the plain text of model.md's notation. A law's
# spread is found under its shock.
SYMBOLS = {"β": "β", "ℒ": "ℒ", "ϱ": "ϱ", "R": "R", "𝒢": "𝒢", "a_Art": "a_Art", "a_Nat": "a_Nat",
           "σ_ψ": "ψ", "σ_θ": "θ", "p_zero": "℘", "ξ_u": "ξ_u"}
# Keys that identify a file rather than state a number of the model.
NOT_PARAMETERS = {"family", "period"}
# The verdicts of a whole-stage handler on the parts it covers, in Bellman's tokens.
STATUSES = {"honours", "fixed", "requires_own_handler", "absent"}


def stage_parameters() -> set[str]:
    """The names the stage file declares with a domain and a gloss, `name : domain :: [...]`; not its functions."""
    text = (SCHEMAS / "bst-1" / "bellman" / "buffer_stock.bl").read_text(encoding="utf-8")
    return {m.group(1) for m in re.finditer(r"^([^\s(]+)\s+:\s[^=\n][^\n]*::\s*\[", text, re.M)}


def parameter_keys() -> set[str]:
    """The leaves of the parameter validator's properties, with `[]` for the items of a list."""
    schema = json.loads((SCHEMAS / "bst-1" / "parameters.schema.json").read_text(encoding="utf-8"))
    keys = set()

    def walk(node: dict, prefix: str) -> None:
        for name, spec in node.get("properties", {}).items():
            path = prefix + name
            if "properties" in spec:
                walk(spec, path + ".")
            elif "properties" in spec.get("items", {}):
                walk(spec["items"], path + "[].")
            else:
                keys.add(path)

    walk(schema, "")
    return keys - NOT_PARAMETERS


def lexicon_rows(stone: str) -> list[str]:
    """The first column of each row of the stone's lexicon table."""
    text = (SCHEMAS / "rosetta" / f"{stone}.md").read_text(encoding="utf-8")
    section = text.split("## The lexicon", 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| ") and not line.startswith("|---")]
    return [row.split("|")[1] for row in rows[1:]]  # the first row is the header


def method_targets() -> set[str]:
    text = (SCHEMAS / "bst-1" / "model.md").read_text(encoding="utf-8")
    section = text.split("## Method targets", 1)[1].split("\n## ", 1)[0]
    return {m.group(1) for line in section.splitlines() if line.startswith("| `")
            for m in [re.match(r"\| `([^`]+)`", line)] if m}


def test_the_symbols_cover_the_stage_file():
    assert stage_parameters() == set(SYMBOLS), "a stage parameter with no symbol here, or a symbol for none"


@pytest.mark.parametrize("stone", STONES)
def test_every_stage_parameter_has_a_row(stone):
    rows = lexicon_rows(stone)
    missing = [name for name, symbol in SYMBOLS.items() if not any(symbol in row for row in rows)]
    assert not missing, f"stage parameters with no row in {stone}.md: {missing}"


@pytest.mark.parametrize("stone", STONES)
def test_every_parameter_key_has_a_row(stone):
    named = {key for row in lexicon_rows(stone) for key in re.findall(r"`([^`]+)`", row)}
    missing = parameter_keys() - named
    assert not missing, f"parameter-file keys with no row in {stone}.md: {sorted(missing)}"


@pytest.mark.parametrize("stone", STONES)
def test_the_cards_carry_a_card_s_fields_and_the_stage_s_targets(stone):
    cards = yaml.safe_load((SCHEMAS / "rosetta" / f"{stone}.cards.yaml").read_text(encoding="utf-8"))
    assert set(cards) == {"toolkit", "handlers", "methods", "evidence", "examples"}
    assert {"package", "repository", "read_at"} <= set(cards["toolkit"])
    targets = method_targets()
    methods = {entry["on"]: entry for entry in cards["methods"]}
    assert set(methods) <= targets, sorted(set(methods) - targets)
    for handler in cards["handlers"]:
        assert {"id", "target", "scope", "transition_alignment", "single_step", "adapter_contract"} <= set(handler)
        assert {"encode", "decode", "status"} <= set(handler["adapter_contract"]), handler["id"]
        assert handler["target"] in targets, handler["target"]
        policy = handler.get("interior_policy", {})
        assert set(policy) <= targets and handler["target"] not in policy, handler["id"]
        for part, verdict in policy.items():
            assert verdict["status"] in STATUSES, (part, verdict)
            # A part the whole-stage handler runs names no handler of its own; one it cannot take names the adapter's.
            named = methods.get(part, {}).get("handler")
            if verdict["status"] in ("honours", "fixed"):
                assert named is None, (part, named)
            else:
                assert named == "adapter", (part, named)
    assert "correctness" in cards["evidence"]
