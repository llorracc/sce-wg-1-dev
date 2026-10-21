---
name: feedback_notation-and-foundation
description: "The schemas use Buffer Stock Theory's notation, SolvingMicroDSOPs' where BST is silent, with the BST paper the authority; symbols have a typeset and a plain-text spelling; the Bellman-SYM stage file is the foundation (rulings of 2026-10-18 and 2026-10-21)"
metadata:
  type: feedback
---

On 2026-10-18 the owner ruled that the schemas use the notation of *Theoretical Foundations of Buffer Stock Saving*, and
SolvingMicroDSOPs' notation where BST has none, and that the `.bl` machinery of Bellman-SYM is the foundation of a family's
description of its true model. The baseline model is BST's version, not the Tractable model's or a benchmark's.

**Why:** the schemas are read beside those two documents, and the working group's formal language is Bellman-SYM; private
names and a prose-first design cut both links.

On 2026-10-21 he ruled that the BST paper is the authority on notation: ξ is the full transitory shock, the unemployment
event included, and θ the transitory shock of the employed. He then approved two spellings of every symbol:
- **Typeset** (LaTeX, MathJax, MyST, the paper), BST's own: an underline marks a minimum, as in `\underline{\xi}`, the minimum
  of ξ; and a subscript that is a word is set upright, `\underline{a}_{\mathrm{Art}}`, never `a_{Art}`.
- **Plain text** (Markdown prose, the terminal, stage-file identifiers, code), names in code font: `ξ_min`, `ψ_min`,
  `θ_min`, `a_Art`, `a_Nat`, `a_min`, `m_min` and `p_worst`. They are never pasted into LaTeX as they stand, where `min`
  would read as a product.
- **μ** is the income while unemployed, as econ-ark's notation file names it. In BST that income is 0, the minimum of ξ.

Each family's `model.md` carries a table of the two spellings with the meaning in words. A standing check refuses the
combining underline and bare multi-letter LaTeX subscripts, and wants a row for every parameter of a stage file. The
documents' other combining marks, a bar, a tilde, a hat and a caron, await the owner's decision. Until the notation pull
request merges, the documents still carry the underlines.

**How to apply:** look a symbol up in BST's macros or SolvingMicroDSOPs' `Notation.md` before writing it (ψ, ξ, θ, ℘, μ, ℒ,
𝒢, R, β, ρ, m, c, a, k, b); write a minimum with BST's underline when typeset and with `_min` in plain text; never use a
combining underline, which terminals draw unreliably, and add no other combining mark; propose a symbol only where both are silent and say so.
Start a family from its stage file; the prose states what the language cannot, and names a method's target by the stage
file's own ids. See [[feedback_iterate-and-propose]].
