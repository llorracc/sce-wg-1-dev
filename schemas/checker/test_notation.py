"""The standing check of the families' notation.

    uv run --with jsonschema --with pyyaml --with scipy --with numpy --with pytest pytest -q schemas/checker

Each symbol has two spellings, the notation section of bst-1/model.md says: typeset, as BST writes it, and in plain text,
as a name in code font. Three things are checked:
- no combining underline (U+0332) appears in the schemas outside the records, since terminals do not draw it reliably; a
  minimum is a name in plain text and `\\underline` when typeset;
- every parameter a family's stage file declares has a row in that family's notation tables;
- no typeset symbol, and no LaTeX in the documents, has a bare subscript of two or more letters, which LaTeX sets in italic
  as a product; a word in a subscript is set upright, as `\\mathrm{Art}`, or is an operator such as `\\min`.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SCHEMAS = Path(__file__).resolve().parent.parent
FAMILIES = {  # each family's stage file, and the model documents whose notation tables it may draw on
    "bst-1": ("bst-1/bellman/buffer_stock.bl", ["bst-1/model.md"]),
    "bst-markov_ui-and-agg": ("bst-markov_ui-and-agg/bellman/bst_markov_ui.bl",
                              ["bst-1/model.md", "bst-markov_ui-and-agg/model.md"]),
}


def documents():
    for path in sorted(SCHEMAS.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".bl", ".json", ".yaml", ".yml", ".py"} \
                and "records" not in path.relative_to(SCHEMAS).parts:
            yield path


def notation_rows(doc: str) -> list[list[str]]:
    """The cells of each row of the document's notation table."""
    text = (SCHEMAS / doc).read_text(encoding="utf-8")
    section = text.split("## Notation", 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| ") and not line.startswith("|---")]
    return [[cell.strip() for cell in row.split("|")[1:-1]] for row in rows[1:]]  # the first row is the header


def plain_names(cell: str) -> set[str]:
    """The names a plain-text cell gives: those in code font, and the bare one-word entries of its list."""
    names = set(re.findall(r"`([^`]+)`", cell))
    for item in re.split(r"[,;]", re.sub(r"`[^`]*`", "", cell)):
        if item.strip() and " " not in item.strip():
            names.add(item.strip())
    return names


def stage_parameters(stage: str) -> set[str]:
    """The names the stage file declares with a domain and a gloss, `name : domain :: [...]`; not its functions."""
    text = (SCHEMAS / stage).read_text(encoding="utf-8")
    return {m.group(1) for m in re.finditer(r"^([^\s(]+)\s+:\s[^=\n][^\n]*::\s*\[", text, re.M)}


def bare_word_subscripts(latex: str) -> list[str]:
    """The subscripts of a LaTeX string that hold two or more letters not inside an upright command or an operator."""
    found = []
    for m in re.finditer(r"_(\{(?:[^{}]|\{[^{}]*\})*\}|\\[A-Za-z]+|.)", latex):
        content = m.group(1)
        content = re.sub(r"\\(mathrm|text|textrm|operatorname)\{[^{}]*\}", "", content)
        content = re.sub(r"\\[A-Za-z]+", "", content)  # \min, \max, \psi and the other commands
        if re.search(r"[A-Za-z]{2,}", content):
            found.append(m.group(0))
    return found


def test_no_combining_underline_outside_the_records():
    marked = []
    for path in documents():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "\u0332" in line:
                marked.append(f"{path.relative_to(SCHEMAS)}:{number}")
    assert not marked, f"combining underlines, which terminals do not draw reliably: {marked}"


@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_every_stage_parameter_has_a_row(family):
    stage, docs = FAMILIES[family]
    named = {name for doc in docs for row in notation_rows(doc) for name in plain_names(row[1])}
    missing = stage_parameters(stage) - named
    assert not missing, f"parameters of {stage} with no row in the notation tables: {sorted(missing)}"


@pytest.mark.parametrize("doc", sorted({d for _, docs in FAMILIES.values() for d in docs}))
def test_typeset_symbols_set_words_upright(doc):
    bad = [(cell, sub) for row in notation_rows(doc) for cell in re.findall(r"`([^`]+)`", row[0])
           for sub in bare_word_subscripts(cell)]
    assert not bad, f"bare word subscripts in {doc}'s typeset column: {bad}"


def test_latex_in_the_documents_sets_words_upright():
    bad = []
    for path in documents():
        if path.suffix != ".md":
            continue
        for math in re.findall(r"\$\$(.+?)\$\$|\$([^$\n]+)\$", path.read_text(encoding="utf-8"), re.S):
            for latex in filter(None, math):
                bad += [(str(path.relative_to(SCHEMAS)), sub) for sub in bare_word_subscripts(latex)]
    assert not bad, f"bare word subscripts in LaTeX: {bad}"


def test_the_subscript_rule_itself():
    assert bare_word_subscripts(r"a_{Art}") == ["_{Art}"]
    assert bare_word_subscripts(r"\xi_min") == []  # one letter: LaTeX takes only the m, a separate defect
    assert bare_word_subscripts(r"\xi_{min}") == ["_{min}"]
    assert not bare_word_subscripts(r"\underline{a}_{\mathrm{Art}}")
    assert not bare_word_subscripts(r"\xi_{\min}")
    assert not bare_word_subscripts(r"\sigma_{\psi}")
    assert not bare_word_subscripts(r"p_{\mathrm{worst}}(z)")
