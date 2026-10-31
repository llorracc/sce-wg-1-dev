# Buffer-stock models

A semantic ontology of buffer-stock saving models, in the sense of the working group's
[Project A](../../project-a/special-issue-proposal.md). It has three parts: what is assumed to exist (the *ontology*),
what stands for what (the *denotation*), and what is written down (the *syntax*). It also records when the reading holds
and when two statements of a model are the same. Its primary source is Carroll and Shanker's *Theoretical Foundations of
Buffer Stock Saving* (BST), cited by the anchors of [its published page](https://llorracc.github.io/BufferStockTheory/).
Where a toolkit or another paper uses BST's terms in another sense, the ontology records the divergence.

**Status: draft, version 0.1.0-draft.1.** Its decisions are proposals until the owner rules on them; the ones still open
are listed [at the end](#open-questions). Its namespace is provisional, as the ontology of probability distributions'
is.

## A semantic ontology and a schema

They are not the same thing, and the working group needs both. A schema fixes the written form of one family's models:
which parameter files, stage files and results files are legal, and what each key means for that family. It is the
*syntax* of a semantic ontology, with parts of its *denotation* and of its *well-posedness*. This ontology states the
model class itself, independently of any written form: what a buffer-stock model is, which objects it has, which
conditions and results relate them, and when two models are one. Each written form then denotes one of its terms.

| part | here | in the schemas |
|---|---|---|
| ontology: what exists, and when two things are the same | the classes, axioms, objects, quantities, conditions, properties, results and identities in [`source.yaml`](source.yaml) | — |
| denotation: what stands for what | each term's `written_as`: its spelling in BST, econ-ark's registry, a bst/1 parameter file, the bst/1 stage file and HARK; the divergences | each family's `model.md`, which reads its stage file in BST's notation |
| syntax: what is written | — | the parameter, stage, results, method and settings files, and their validators |
| well-posedness | the membership axioms, the paper's hypotheses, the conditions and the results | each family's `conditions.md`, which the checker enforces |
| equivalence, adequacy, convergence | the identities | the hash, the effective member, the results files, the precision levels |

Systems biology keeps the same split, and keeps it on purpose: SBML fixes the written form of a model, the Systems
Biology Ontology states what its components mean, and each SBML component carries an SBO term. The two are maintained
separately, so meaning can change without breaking files. The same holds here. bst/1 and the Markov family are two
schemas, with two parameter files and two stage files, and their models belong to one class with one set of
conditions. A schema is written per family; the ontology is written per model class. In the proposal's terms, a paper on
buffer-stock models is a *model-class* paper, and this is its ontology.

## The kinds

Every row of the source is one of these, and the generator writes each as an OWL class.

- A **model class** is a class of models, defined by axioms. A model is a member when it satisfies every membership
  axiom.
- An **axiom** is a statement a member must satisfy (*membership*), or one the class's results assume (*hypothesis*).
- An **object** is an entity of the model: an agent, a population, a state, a control, a shock, an event, a primitive, a
  bound, a function, an operator, a constraint or a measure.
- A **moment** is an expectation under the law of one shock.
- A **quantity** is a number the primitives determine, given by a formula: a patience factor, an MPC limit, human wealth.
- A **condition** is an inequality on quantities, which holds or fails.
- A **property** is a statement about a solution or a population, such as the existence of a target.
- A **result** relates conditions and properties. Each records its source: proved in BST, cited there, stated without
  proof, or deduced here.
- An **identity** is a criterion for when two models, or two statements of one model, are the same.
- A **family** is a written family of the schemas, with the classes whose members it writes.
- A **divergence** is a place where a toolkit, a paper or a schema uses a term in another sense.

Formulas use the ontology of probability distributions' formula syntax. The shocks' laws are rows of
[that ontology](../probability-distributions/), which this one imports.

## What makes a model a buffer-stock model

The **membership axioms** of the class `buffer-stock-model`:
- **one agent's consumption-saving problem**: each period, market resources m are split between consumption c and
  end-of-period assets a = m − c;
- **CRRA utility with ϱ > 1**, so u(0⁺) = −∞;
- **the Friedman–Muth income process**: noncapital income 𝐩ξ, with 𝐩′ = 𝒢ψ′𝐩, E[ψ] = 1 and ξ ≥ 0;
- **income risk**: at least one of the shocks is not degenerate;
- **assets earn a return**, R > 0;
- **the constraint in force** is `a_min` = max(`a_Art`, `a_Nat`): the natural constraint, or a tighter artificial one;
- **an atom at the worst transitory shock where the natural constraint is in force** (the owner's ruling of
  2026-10-31). If `a_min` = `a_Nat`, the edge `a_Art` = `a_Nat` included, then P(ξ = inf supp ξ) > 0 under the true law.
  The condition is on the transitory shock alone, not on income ψξ. BST calls such an atom inessential to its proofs;
  the ruling makes it part of the class's definition.

The **hypotheses** of BST's own class, `bst-model`, which its theorems assume beyond membership: iid shocks, bounded
support, the zero-income event (ξ = 0 with probability ℘ > 0), a riskless and constant return, no artificial constraint,
infinite lives and one type. A model with untruncated lognormal shocks can therefore be a buffer-stock model and still
lie outside the reach of BST's theorems. Keeping the two tiers apart is one of the draft's proposals.

**Buffer-stock saving** is a property of a member's solution, not a condition of membership. This draft says a member
exhibits it when it has a non-degenerate limiting solution and an individual target m̂, as BST's introduction does. The
perfect-foresight model fails the axiom of income risk: it is the class's benchmark, the limit as the shocks vanish, and
not a member.

Applied to bst/1's members, the axioms classify them as follows (the tests check this):
- `library` is a member and satisfies every hypothesis of BST's class;
- `toy` is a member: its artificial constraint lies above the natural one, so the atom axiom does not apply;
- `toy-untruncated` is **not** a member. Its untruncated laws put `a_Nat` at 0, equal to `a_Art` (the edge), and the
  lowest transitory shock comes from the employed lognormal's tail, which has no atom.

## The classes

```
buffer-stock-model
├── bst-model                     BST's model, as the paper states it
├── with-survival                 perpetual youth, no annuity: BST's Modigliani scheme
├── with-blanchard-annuities      survivors earn R/ℒ
├── with-positive-benefit         ξ_u > 0
├── with-artificial-constraint    a_Art above the natural constraint
├── with-types                    permanent types differing in β
├── with-markov-states            Markov employment and an aggregate regime
├── with-kinked-return            a higher rate on borrowing
├── with-risky-asset              a random return; conditions not yet stated
└── life-cycle                    finite horizon, primitives varying with age
perfect-foresight-benchmark       the limit, outside the class
```

Each extension reduces to `bst-model` under a stated restriction, such as ℒ = 1 or ξ_u = 0. The schemas' family bst/1
writes the members of `with-survival`, `with-positive-benefit`, `with-artificial-constraint` and `with-types`; the
Markov family adds `with-markov-states`.

In the life-cycle class, a primitive indexed by period t governs the move from t to t+1: the income laws, the survival
probability, the return on end-of-period assets and the growth factor of permanent income. That is how HARK's solvers
read them.

## The conditions

Every condition is a factor compared with a bound. The factors carry survival as bst/1 does, through β̊ = βℒ and
Þ̊ = (Rβ̊)^(1/ϱ). They are BST's when ℒ = 1.

| condition | holds when | governs, by the results | HARK |
|---|---|---|---|
| AIC | Þ̊ < 1 | consumption growth below one as m grows | `check_AIC` |
| RIC | Þ̊_R < 1 | a positive MPC as m grows | `check_RIC` |
| WRIC | `p_worst`^(1/ϱ) Þ̊_R < 1 | with the FVAC, a non-degenerate solution | `check_WRIC` |
| FHWC | 𝒢/R < 1 | finite human wealth | `check_FHWC` |
| PF-FVAC | β̊𝒢^(1−ϱ) < 1 | perfect foresight's finite value of autarky | `check_FVAC`, perfect foresight |
| FVAC | β̊𝒢^(1−ϱ)E[ψ^(1−ϱ)] < 1 | with the WRIC, a non-degenerate solution | `check_FVAC` |
| GIC | Þ̊_𝒢 < 1 | the pseudo-target m̌; income-weighted invariance | `check_GICRaw` |
| GIC-Mod | Þ̊_𝒢 E[ψ⁻¹] < 1 | the target m̂ | `check_GICMod` |
| GIC-Szeidl | log Þ̊_𝒢 < E[log ψ] | invariance under the population measure; the log target m̃ | `check_GICSdl` |
| GIC-Harmenberg | Þ̊_𝒢 < exp(E[ψ log ψ]) | Harmenberg's condition | `check_GICHrm` |
| GIC-Liv | ℒ Þ̊_𝒢 < 1 | aggregate balanced growth with estates destroyed | `check_GICLiv` |

The implications among the conditions alone are results of the ontology, each tested on sampled models:
- GIC-Mod ⇒ GIC-Szeidl ⇒ GIC ⇒ GIC-Harmenberg, and GIC ⇒ GIC-Liv;
- RIC ⇒ WRIC, and FVAC ⇒ PF-FVAC;
- under the FHWC, GIC ⇒ PF-FVAC ⇒ RIC;
- if both the RIC and the GIC fail, so does the FVAC;
- if the GIC holds and the RIC fails, the FHWC fails, and so it does whenever the FVAC holds and the RIC fails.

The tests also find models that satisfy each weaker condition and fail the stronger one, so the ladder does not
collapse.

## Identity

- The problem in levels and the problem in ratios to permanent income are one model.
- The limiting solution is the stationary fixed point.
- Without an annuity, the household's rule depends on β and ℒ only through β̊. With survival by Markov state it depends
  on β ℒ(s), state by state. The population depends on ℒ apart from β, since ℒ sets the rate of death and replacement.
  With Blanchard's annuity, ℒ also enters the return, and the identity fails.
- An artificial constraint at or below the natural one is no constraint.
- With ℘ = 0, ξ_u never pays.
- Two written laws are one law when the ontology of probability distributions says so.
- Blanchard's annuity leaves the absolute patience factor unchanged.

The schemas' hash is a finer identity, of written forms; these are identities of models.

## Denotation

Each term names its written forms in five formats:

| format | example: relative risk aversion | example: the target |
|---|---|---|
| BST's notation | `\CRRA` | `\mTrgNrm` |
| econ-ark's notation registry | `crra` | `target` |
| a bst/1 parameter file | `crra` | — |
| the bst/1 stage file | `ϱ` | — |
| HARK | `CRRA` | `mNrmTrg` |

The tests check every parameter-file key against bst/1's validator and every stage-file name against its stage file.
They also check that the ontology's formulas give the checker's verdict and factor for each condition, type and member:
the ontology and the schemas mean the same thing by each condition.

## Divergences

Each divergence is recorded where it is found, with a checkable source.
- **HARK, main at `4c285e86`:**
  - VAFac leaves out survival, while PFVAFac includes it, though its message does not;
  - the WRIC message drops the power 1/ϱ;
  - two objects are named hNrm, one including this period's income and one not;
  - WorstPrb and the natural limit are taken from the discretized atoms, not the true law's infima;
  - the RIC-failure message claims the FHWC fails without the FVAC that makes it true;
  - in a cyclical model, the simulation reads each period's parameters one period after the solver did;
  - the log target m̃ that BST says Econ-ARK computes is not computed;
  - GPFacLivMod carries ℒ once more than the GIC-Liv as ruled, which is GPFacLiv.
- **The published HAFiscal paper and code:**
  - ξ names the employed draw, BST's θ;
  - "target" names a data moment;
  - "MPC" names the share of a windfall spent within a year;
  - the cap on β places survival outside the patience factor.

These divergences are what the proposal's closing comparison is meant to collect: places where the profession's
conventions silently differ.

## Open questions

- **The two tiers.** Are bounded support, iid shocks and the zero-income event hypotheses of BST's theorems, as drafted,
  or conditions of membership?
- **Buffer-stock saving.** Is it the individual target, as drafted, or does the pseudo-target suffice?
- **The perfect-foresight model and the risky asset.** Is the first outside the class, as drafted? Is the second inside,
  as drafted from the owner's ruling of 2026-10-27 that a target exists?
- **GIC-Liv in BST's text.** BST writes ℒ Þ_𝒢 < 1 without saying whether Þ carries survival. The owner ruled on
  2026-10-22, in econ-ark's notation registry, that the condition is ℒ Þ̊_𝒢, HARK's GPFacLiv, and the ontology follows
  the ruling. The paper's text could say so. The condition also assumes, as BST does, that newborns' permanent income
  grows with aggregate productivity. bst/1's newborn arrives with 𝐩 = 1, and its aggregate conditions are its own.
- **The schemas.** Should each schema key carry its term's identifier, as SBML components carry SBO terms? Should the
  atom axiom become a validity condition of bst/1, which would reject `toy-untruncated`? Both are schema changes, to be
  proposed with their consequences before either is made.

## The files

| file | what it is |
|---|---|
| `source.yaml` | the one source: every row, by kind |
| `source.schema.json` | the JSON Schema the source must satisfy |
| `generate.py` | writes the two files below from the source, or checks that they are current |
| `buffer-stock-models.ttl` | the ontology in OWL 2, Turtle syntax (generated) |
| `buffer-stock-models.json` | a flat table, one row per term, references resolved (generated) |
| `bst-anchors.txt` | the anchors of BST's published page, read on 2026-10-31, which every bst citation must be among |
| `registry-keys.txt` | the keys of econ-ark's notation registry, version 8.0.0 |
| `test_ontology.py` | the tests |
| `CHANGELOG.md` | what each version changed |
| `LICENSE` | Creative Commons Attribution 4.0 International |

Never edit a generated file; edit the source and run the generator. Everything runs with `uv`, from this folder:

```bash
uv run --with pyyaml --with jsonschema python generate.py
uv run --with pyyaml --with jsonschema --with referencing --with scipy --with numpy --with rdflib --with pytest pytest -q
```

The tests import the schemas' checker, so they run in a clone of this repository.
