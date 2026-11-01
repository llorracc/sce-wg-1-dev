# Buffer-stock models

A semantic ontology of buffer-stock saving models, in the sense of the working group's
[Project A](../../project-a/special-issue-proposal.md). It has three parts: what is assumed to exist (the *ontology*),
what stands for what (the *denotation*), and what is written down (the *syntax*). It also records when the reading holds
and when two statements of a model are the same. Its primary source is Carroll and Shanker's *Theoretical Foundations of
Buffer Stock Saving* (BST), cited by the anchors of [its published page](https://llorracc.github.io/BufferStockTheory/).
Where another paper, a notation or a schema uses BST's terms in another sense, the ontology records the divergence. It
names no toolkit, and nothing peculiar to how a toolkit solves or simulates a model: how each toolkit holds the terms,
and where it departs from them, is in that toolkit's [Rosetta Stone](../../schemas/rosetta/README.md).

**Status: draft, version 0.1.0-draft.2.** Its decisions are proposals until the owner rules on them; the ones still open
are listed [at the end](#open-questions). Its namespace is provisional, as the ontology of probability distributions'
is. Since draft.2 it states its objects in Bellman-SYM's terms, the language of the schemas' stage files
([below](#in-bellman-syms-terms)).

## A semantic ontology and a schema

They are not the same thing, and the working group needs both. A schema fixes the written form of one family's models:
which parameter files, stage files and results files are legal, and what each key means for that family. It is the
*syntax* of a semantic ontology, with parts of its *denotation* and of its *well-posedness*. This ontology states the
model class itself, independently of any written form: what a buffer-stock model is, which objects it has, which
conditions and results relate them, and when two models are one. Each written form then denotes one of its terms.

| part | here | in the schemas |
|---|---|---|
| ontology: what exists, and when two things are the same | the classes, axioms, objects, quantities, conditions, properties, results and identities in [`source.yaml`](source.yaml) | — |
| denotation: what stands for what | each term's `written_as`: its spelling in BST, econ-ark's registry, a bst/1 parameter file and the bst/1 stage file; the divergences | each family's `model.md`, which reads its stage file in BST's notation |
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
- An **object** is an entity of the model, in one of nineteen categories:
  - agents and time: an agent, a population, the time index, a structure (a stage or a trellis);
  - fields: a perch, a state, a control, a shock or a value;
  - inputs: a primitive (a parameter), a bound (a property of a law);
  - maps: a function, a law of motion, a connector, an operator, an operation;
  - the rest: a relation, a constraint or a measure.
- A **moment** is an expectation under the law of one shock.
- A **quantity** is a number the primitives determine, given by a formula: a patience factor, an MPC limit, human wealth.
- A **condition** is an inequality on quantities, which holds or fails.
- A **property** is a statement about a solution or a population, such as the existence of a target.
- A **result** relates conditions and properties. Each records its source: proved in BST, cited there, stated without
  proof, or deduced here.
- An **identity** is a criterion for when two models, or two statements of one model, are the same.
- A **family** is a written family of the schemas, with the classes whose members it writes.
- A **divergence** is a place where another paper, a notation or a schema uses a term in another sense.

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
│   └── liquidity-constrained     a ≥ 0, with a positive lowest income
├── with-types                    permanent types differing in β
├── with-markov-states            Markov employment and an aggregate regime
├── with-kinked-return            a higher rate on borrowing
├── with-risky-asset              a random return; conditions not yet stated
└── life-cycle                    finite horizon, primitives varying with age
perfect-foresight-benchmark       the limit, outside the class
└── perfect-foresight-constrained the benchmark with a ≥ 0, the limit of liquidity-constrained
```

Each extension reduces to `bst-model` under a stated restriction, such as ℒ = 1 or ξ_u = 0. The schemas' family bst/1
writes the members of `with-survival`, `with-positive-benefit`, `with-artificial-constraint` and `with-types`; the
Markov family adds `with-markov-states`.

In the life-cycle class, a primitive binds the stage occurrence of the period whose block reads it. In bst/1's one-stage
period, β and ℒ are read in period t's decision block, and R, 𝒢 and the shocks' laws in period t+1's arrival block.
Both are the move from t to t+1.

## The conditions

Every condition is a factor compared with a bound. The factors carry survival as bst/1 does, through β̊ = βℒ and
Þ̊ = (Rβ̊)^(1/ϱ). They are BST's when ℒ = 1. MST-βR is Ma, Stachurski and Toda's (2020) condition G_βR < 1, read for the
normalized problem, whose discount factor is β̊(𝒢ψ′)^(1−ϱ) and whose return is R/(𝒢ψ′).

| condition | holds when | governs, by the results |
|---|---|---|
| AIC | Þ̊ < 1 | consumption growth below one as m grows |
| RIC | Þ̊_R < 1 | a positive MPC as m grows |
| WRIC | `p_worst`^(1/ϱ) Þ̊_R < 1 | with the FVAC, a non-degenerate solution |
| FHWC | 𝒢/R < 1 | finite human wealth |
| PF-FVAC | β̊𝒢^(1−ϱ) < 1 | perfect foresight's finite value of autarky |
| FVAC | β̊𝒢^(1−ϱ)E[ψ^(1−ϱ)] < 1 | with the WRIC, a non-degenerate solution; with MST-βR, one in the liquidity-constrained model |
| GIC | Þ̊_𝒢 < 1 | the pseudo-target m̌; income-weighted invariance |
| GIC-Mod | Þ̊_𝒢 E[ψ⁻¹] < 1 | the target m̂ |
| GIC-Szeidl | log Þ̊_𝒢 < E[log ψ] | invariance under the population measure; the log target m̃ |
| GIC-Harmenberg | Þ̊_𝒢 < exp(E[ψ log ψ]) | Harmenberg's condition |
| GIC-Liv | ℒ Þ̊_𝒢 < 1 | aggregate balanced growth with estates destroyed |
| MST-βR | β̊R𝒢^(−ϱ)E[ψ^(−ϱ)] < 1, that is E[(Þ̊_𝒢/ψ)^ϱ] < 1 | with the FVAC, a non-degenerate solution in the liquidity-constrained model; with the RIC as well, a stationary distribution |

The implications among the conditions alone are results of the ontology, each tested on sampled models:
- MST-βR ⇒ GIC-Mod ⇒ GIC-Szeidl ⇒ GIC ⇒ GIC-Harmenberg, and GIC ⇒ GIC-Liv;
- RIC ⇒ WRIC, and FVAC ⇒ PF-FVAC;
- with the RIC, the failure of the GIC means finite human wealth;
- under the FHWC, GIC ⇒ PF-FVAC ⇒ RIC;
- if both the RIC and the GIC fail, so does the FVAC;
- if the GIC holds and the RIC fails, the FHWC fails, and so it does whenever the FVAC holds and the RIC fails.

The tests also find models that satisfy each weaker condition and fail the stronger one, so the ladder does not
collapse.

## The natural and the artificial constraint

The two make different models, and the ontology keeps them apart in four ways.

- **Membership.** The atom at the worst transitory shock is required only where the natural constraint is in force, the
  edge `a_Art` = `a_Nat` included. A model whose artificial constraint lies strictly above the natural one needs no
  atom. An artificial constraint at or below the natural one is no constraint.
- **Behavior.** The natural constraint never binds. In BST's class, the zero-income event keeps the consumer from ending
  a period at the limit, and near the lowest resources the MPC approaches κ_max, below one; the paper states this. An
  artificial constraint strictly above the natural one binds on an interval of m just above it, where c = m − `a_Art`
  and the MPC is one. That is deduced here, and not tested.
- **Conditions.** Without an artificial constraint, the WRIC and the FVAC give a non-degenerate solution. BST says the
  WRIC "cannot be relaxed further without an artificial liquidity constraint". The ontology reads that as necessity
  and, by the owner's decision of 2026-11-01, treats it as true until the paper proves it. With the constraint a ≥ 0
  and a positive lowest income, the liquidity-constrained class, the problem is Ma, Stachurski and Toda's (2020):
  - **existence:** their Theorem 2.2 gives a non-degenerate solution under the FVAC and MST-βR. Neither the RIC nor the
    WRIC enters, and MST-βR already implies the GIC-Mod;
  - **a stationary distribution:** their Theorem 3.1 adds the RIC, since their stationarity condition is the RIC with
    the GIC-Mod;
  - **necessity:** MST-βR is sufficient, not necessary. Ma, Stachurski and Toda (2022) need no condition on the return.
    That covers the problem without permanent shocks, where MST-βR is the GIC. With permanent shocks the discount
    factor is random, a case that paper does not treat;
  - **a caveat:** their model gives the discount factor, the return and income separate innovations, while the
    normalized problem's discount factor and return share ψ′. That fits exactly when ψ has finite support. For a
    continuous ψ it has not been checked.

  The artificial constraint also makes the feasible set compact, which BST's proof cannot rely on under the natural
  constraint.
- **Limits.** As ℘ ↓ 0, BST's model converges to the liquidity-constrained problem. As the shocks vanish, that class's
  limit is the constrained perfect-foresight benchmark, with a ≥ 0, where BST's taxonomy holds:
  - with the RIC, a non-degenerate solution. If the GIC fails as well, the constraint never binds and the constrained
    rule is the unconstrained one. If the GIC holds, the constraint binds and the rule approaches the unconstrained one,
    with the MPC tending to 1 − Þ̊_R;
  - without the RIC, a non-degenerate solution exists if and only if the GIC holds. Human wealth is then infinite and
    the MPC tends to zero. Without the GIC as well, the solution is degenerate.

  Under uncertainty, the natural constraint plays the artificial one's part: when the RIC fails and the FVAC holds,
  human wealth is infinite, and the MPC tends to zero.

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

## In Bellman-SYM's terms

The schemas state each family's household problem in a Bellman-SYM stage file, so the ontology states its objects in
that language's terms. Bellman-SYM's documentation is not public. Its rules are therefore stated here as the ontology's
own, and its concepts are named by their slugs, pinned in `bellman-concepts.txt`, never linked.

- **Perches and values.**
  - A stage has three perches: arrival, decision and continuation. They are information contexts, not dates.
  - In bst/1's one-stage period their states are k, m and a. A period of several stages would not keep that
    correspondence.
  - Each perch has a value field: V[<], V and V[>]. Each field is represented by a function of its perch's state.
  - BST's v_t(m) is the decision value. Its arrival value is v≺(k) = E[(𝒢ψ)^(1−ϱ) v(m)]. Its continuation value is a
    function of a, supplied by the next period's arrival value.
  - The derivative of a value is no field. It is read by a derivative term: D_{m}V, D_{k}V[<] and D_{a}V[>].
  - BST's end-of-period value is β̊ V[>](a), and its end-of-period marginal value is β̊ D_{a}V[>](a) =
    β̊ R E[(𝒢ψ′)^(−ϱ) u′(c(m′))].
  - The policy is the consumption function, from the decision state into the feasible set. The control c is its value
    at one m.
- **Laws of motion and the connector.** BST's dynamic budget constraint is a composite of four relations:
  - the decision law of motion, a = m − c;
  - the connector, k′ = a, a renaming with no calculation;
  - the next period's arrival law of motion, m′ = R k′/(𝒢ψ′) + ξ′, on which the shocks are drawn;
  - permanent income's growth, which the normalized problem carries only as factors.

  It is a law of motion, not a constraint. The constraint in force is stated three times in the stage file: in the set
  of a, in the feasible set 𝒞(m), and in the Euler equation's clause.
- **Operators and operations.**
  - The backward stage operator 𝕋 = 𝕋_≺ ∘ 𝕋_≻ runs from continuation value to arrival value. The factor (𝒢ψ)^(1−ϱ) is a
    non-identity arrival aggregator inside its expectation.
  - BST's T runs from decision value to decision value: it is the same operator cut at the decision perch. Their fixed
    points correspond.
  - The forward distribution operator 𝕄_π moves the population's measure. The expectation and BST's cross-sectional mean
    are operations, not operators.
  - The Euler equation is a Kuhn–Tucker relation. Its clause covers the natural constraint as well as the artificial one.
- **Measures.**
  - The population measure is a measure on a perch's states, and its stationary distribution is a fixed point of 𝕄_π
    across the connector.
  - The income measure has no spelling in a stage: it is a second forward problem, with ψ's law weighted by ψ
    (deduced).
  - Death and the inflow of newborns are stated outside bst/1's stage file, which states survivors' problem.
- **Time.** A trellis counts periods back from the terminal one, so t = T − h. A primitive binds the occurrence whose
  block reads it (see the life-cycle class above).
- **Inputs.**
  - The primitives are parameters; none is a setting.
  - The bounds ψ_min, ξ_min and the probabilities at them are properties of the shocks' laws, linked to the ontology of
    probability distributions' support and atoms.
  - The natural limit is a quantity of the laws. A stage file that takes it as a calibrated parameter must agree with the
    laws, which no stage file can check.
  - A shock on a two-point set replaces the category of event.
- **Meaning and representation.** Each format of the denotation has a role:
  - BST's notation, the registry and the stage file are notations, and `written_as` lists the expressions each one's
    meaning map sends to the term;
  - a parameter-file key is where a calibration binds a value.

  The ontology states the target, the schemas' stated member with its true laws. How a toolkit approximates it, and
  the effective member it solves, are the schemas' and each toolkit's Rosetta Stone's to state.
- **Where Bellman-SYM is silent:**
  - the model classes and their axioms;
  - the conditions on more than one parameter;
  - named constants such as the patience factors;
  - the infinite horizon and its limiting solution;
  - permanent income and the normalization by it;
  - the income measure;
  - newborns entering from outside a trellis.

  The ontology states these itself.

## Denotation

Each term names its written forms in four formats:

| format | example: relative risk aversion | example: the target |
|---|---|---|
| BST's notation | `\CRRA` | `\mTrgNrm` |
| econ-ark's notation registry | `crra` | `target` |
| a bst/1 parameter file | `crra` | — |
| the bst/1 stage file | `ϱ` | — |

The parameter file is a calibration, and the others are notations. In the stage file a block's or a line's id, such as
`policy.euler`, is the address of where a relation is written, not a name of an object. The three derivative terms are
written as Bellman-SYM now writes them; bst/1's stage file will carry them once its proposed rewrite is made.

The tests check every parameter-file key against bst/1's validator and every stage-file name against its stage file.
They also check that the ontology's formulas give the checker's verdict and factor for each condition, type and member:
the ontology and the schemas mean the same thing by each condition.

## Divergences

Each divergence is recorded where it is found, with a checkable source. Each has a kind:
- a difference of meaning;
- of notation;
- of convention;
- or an absence.

A toolkit's departures from the terms are not divergences of the ontology: each is recorded in that toolkit's
[Rosetta Stone](../../schemas/rosetta/README.md).

The divergences:
- **BST and Bellman-SYM:** 𝕄 names BST's cross-sectional mean and the forward distribution operator alike.
- **The schemas:** bst/1's stage file and the Markov family's still write the marginal values as fields with a role word
  Bellman-SYM retired on 2026-10-26. The language now refuses both files.
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
  2026-10-22, in econ-ark's notation registry, that the condition is ℒ Þ̊_𝒢, and the ontology follows
  the ruling. The paper's text could say so. The condition also assumes, as BST does, that newborns' permanent income
  grows with aggregate productivity. bst/1's newborn arrives with 𝐩 = 1, and its aggregate conditions are its own.
- **Weak return impatience.** The ontology treats the WRIC as necessary without an artificial constraint, by the
  owner's decision of 2026-11-01, until the paper proves it; the paper's own tracker asks for the proof.
- **Ma, Stachurski and Toda with a continuous permanent shock.** Their statement fits the normalized problem exactly
  when ψ has finite support. Do their proofs need the discount factor and the return to have separate innovations?
- **Existence without MST-βR, with permanent shocks.** Their 2022 paper drops the condition on the return under a
  constant discount factor. Does that extend to the normalized problem's random one, as their footnote expects?
- **An artificial constraint other than zero.** Their results take a ≥ 0. The ontology states nothing for a borrowing
  limit strictly between the natural one and zero.
- **The schemas.** Three schema changes, each to be proposed with its consequences before it is made:
  - **The stage files' rewrite with derivative terms.** Both stage files need it to elaborate under Bellman-SYM's
    current language. The owner approved it on 2026-10-31, and it is in the fork's pull request #15; once that is
    merged, the divergence it resolves is closed and the derivative terms are no longer pending.
  - **Identifiers on the schemas' keys.** Should each key carry its term's identifier, as SBML components carry SBO
    terms?
  - **The atom axiom as a validity condition of bst/1.** That would reject `toy-untruncated`.

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
| `bellman-concepts.txt` | the slugs of Bellman-SYM's concepts, read on 2026-10-31, named and never linked |
| `test_ontology.py` | the tests |
| `CHANGELOG.md` | what each version changed |
| `LICENSE` | Creative Commons Attribution 4.0 International |

Never edit a generated file; edit the source and run the generator. Everything runs with `uv`, from this folder:

```bash
uv run --with pyyaml --with jsonschema python generate.py
uv run --with pyyaml --with jsonschema --with referencing --with scipy --with numpy --with rdflib --with pytest pytest -q
```

The tests import the schemas' checker, so they run in a clone of this repository.
