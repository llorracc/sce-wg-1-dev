---
name: feedback_notation-and-foundation
description: "The schemas use Buffer Stock Theory's notation with econ-ark's notation registry as the authority beside the BST paper; two spellings of each symbol; the symbols in force (Þ̊, β̊, ϱ, ε, ξ_u, ξ_x, j); the Bellman-SYM stage file is the foundation (rulings of 2026-10-18, 2026-10-21 and 2026-10-22)"
metadata:
  type: feedback
---

On 2026-10-18 the owner ruled that the schemas use the notation of *Theoretical Foundations of Buffer Stock Saving*, and
SolvingMicroDSOPs' notation where BST has none, and that the `.bl` machinery of Bellman-SYM is the foundation of a family's
description of its true model. The baseline model is BST's version, not the Tractable model's or a benchmark's.

**Why:** the schemas are read beside those two documents, and the working group's formal language is Bellman-SYM; private
names and a prose-first design cut both links.

On 2026-10-21 he ruled that the BST paper is the authority on notation, and approved two spellings of every symbol:
- **Typeset** (LaTeX, MathJax, MyST, the paper), BST's own: an underline marks a minimum, as in `\underline{\xi}`; a
  subscript that is a word is set upright, `\underline{a}_{\mathrm{Art}}`, never `a_{Art}`.
- **Plain text** (Markdown prose, the terminal, stage-file identifiers, code): a minimum, and a symbol whose subscript is a
  word, are names in code font (`ξ_min`, `ψ_min`, `θ_min`, `a_Art`, `a_Nat`, `a_min`, `m_min`, `p_worst`), never pasted into
  LaTeX as they stand. Marks above a letter (a hat, a check, a tilde, the ring) stay, since terminals draw them on their
  letters; the combining underline does not, and a standing check refuses it.

Econ-ark's notation registry (`@resources/notation/notation.yml` in econ-ark-tools) is in force beside BST, and the owner
rules on it there; the schemas take each version by pull request (#7 for 1.0.0, #9 for 5.0.0 and 6.0.0). In force:
- the targets: `\hat{m}` the buffer stock target, `\check{m}` the pseudo-target;
- 𝒢 the growth factor, 𝒢_t and 𝒢(z) the Markov family's in a quarter; R typeset `\mathsf{R}`, levels bold italic
  (`\pLvl`), k "kapital";
- ξ the transitory shock including the unemployment event, θ the employed draw;
- **survival-inclusive symbols take the ring:** β̊ = β ℒ and Þ̊ = (R β̊)^(1/ϱ), with Þ̊_R and Þ̊_𝒢 (`\DiscFacEff`,
  `\APFacEff`, `\RPFacEff`, `\GPFacEff`); the GIC-Liv is ℒ Þ̊_𝒢 < 1, HARK's and the registry's `GPFacLiv`;
- **ϱ** is relative risk aversion (`\CRRA`, since 6.0.0); **ε** the tail (Pareto) exponent, ζ being the leisure share;
- `κ_min` (`\underline{\kappa}`) the limiting MPC, max(0, 1 − Þ̊_R); ℛ = R/𝒢;
- ℘ the probability of unemployment whatever the income then; `p_worst` the probability of the worst income;
- **the incomes while unemployed are ξ_u, with benefits, and ξ_x, after they expire** (ruled 2026-10-22, registry 8.0.0,
  `\IncUnemp` and `\IncUnempNoBen`), superseding the ξ_U and ξ_X of 2026-10-21; neither is underlined, since neither need
  be ξ's lowest value;
- **j is the employment state** (ruled 2026-10-22), `bst/1`'s unemployment-event label included; z is the registry's
  matching elasticity only;
- in the Markov family `sep`, `find`, `p_exit`, `reg` and ℷ.

The ξ_u, ξ_x and j of 2026-10-22 were merged with #10 at 16:02:08 that day. A method's target names the operator in
Bellman's spelling, `E_ψ_θ_j` ([[feedback_method-attachment]]).

**How to apply:** look a symbol up in the registry, then BST's macros or SolvingMicroDSOPs' `Notation.md`, before writing it;
write a minimum with BST's underline when typeset and with `_min` in plain text; never use a combining underline; propose a
symbol only where all are silent, and say so. Python normalizes identifiers (NFKC), under which ϱ becomes ρ and ℒ becomes L:
keep such names as strings. Start a family from its stage file; the prose states what the language cannot, and names a
method's target by the stage file's own ids. See [[feedback_iterate-and-propose]].
