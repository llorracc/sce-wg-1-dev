# The household block's Jacobians: a proposed interface

**Status: APPROVED, 2026-11-01:** the design at 17:05:24 EST, with the owner's decisions below, and the results-schema
block at 17:26:21. The block is the key `jacobians` of `bst/results.schema.json` (its `$defs/Jacobians`), and the checker's
`checker/jacobians.py` verifies it. The owner asked at 16:37:49 for the interface to be
drafted with the toolkits, looking at DolARK, HARK and HAFiscal. The QuantEcon, HAFiscal-Latest, HARK and HARK-dev
sessions answered, the last two with the identities below measured on HARK's main branch at `4c285e86`.

## What it is for

The [toy-hafiscal suite](bst/model.md) gives every toolkit one `bst-artificial/1` member whose three discount-factor types
HARK's and HAFiscal's tools have estimated. Each toolkit solves and simulates that member's steady state. It must also
expose whatever is needed to compute its sequence-space Jacobians (Auclert, Bardóczy, Rognlie and Straub), so that the
sequence-space exercise can be run on every toolkit's steady state and the answers compared. No toolkit but HARK and
HAFiscal estimates anything.

## What the toolkits do now

- **HARK** (econ-ark/HARK main):
  - **Two routines.** `AgentType.make_basic_SSJ(shock, outcomes, grids, …)` runs the fake-news algorithm on any scalar
    parameter (`HARK/core.py`, `HARK/SSJutils.py`). It returns T × T arrays indexed `J[t, s]`, the response at t to news at
    date 0 of a change at s, with T = 300 and a one-sided difference of 10⁻⁴ by default. The older
    `NewKeynesianConsumerType.calc_jacobian` covers consumption and assets only.
  - **Dating.** In the model file R_t is earned on the assets chosen at t − 1. The older routine dates R and income as
    the newer one does, and the discount factor one period later: its column s is the newer routine's column s − 1.
    Once newborns start from the same wealth, the two agree to within about half a percent (measured on HARK main
    `4c285e86` by the HARK and HARK-dev sessions).
  - **Normalization.** Outcomes are per unit of permanent income. An option weights by permanent income, Harmenberg's
    neutral measure, which gives exact aggregates with one state variable.
  - **Dating is a flag the caller sets.** An input the solver reads one period ahead (R, the income process) needs
    `offset=True`. A wrong flag moves a column by one with no warning; the budget identity below catches it.
  - **Its limits.**
    - There are no multiple types: each type gets its own Jacobian. Open pull request #1835 adds an aggregator and a
      check of the flow budget.
    - There is no test against the sequence_jacobian package.
    - Inputs that move the mass of income, survival and growth, are not carried on main (open #1828).
    - Patient households need a tight steady state: at the default tolerance, open #1823 measures errors of 47–57% for
      growth-patience factors of 0.997–0.9997, a range estimated quarterly discount factors can reach.
    - The truncated lognormal is not on main (open draft #1863).
- **HAFiscal**, in its published package llorracc/HAFiscal-QE (`Code/HA-Models/FromPandemicCode/HA-Fiscal-HANK-SAM.py`
  and `…-to-python.py`):
  - **Its own fake-news code.** Built on a copy of HARK's Markov consumer, it computes the household's Jacobians for 3
    education groups × 7 discount factors and 8 inputs: `transfers`, `r`, `w`, `tau`, `eta` (job finding), `DiscFac`,
    `UI_extend` and `UI_rr`.
  - **How it computes them.** It works under the neutral measure on HARK's grid of m, with T = 300 and a step of 10⁻⁴,
    and weights the types into aggregate C and A.
  - **The general-equilibrium side.** The sequence_jacobian package (1.0.0) takes the Jacobians as a precomputed
    `JacobianDict`; no household block is written in that package's form.
  - **Units.** The inputs are changes in levels: a transfer adds to every state's income, in units of permanent income;
    the wage and the tax move employed income only; the two UI inputs add to the benefit and post-exhaustion states'
    income. The outputs are per-capita aggregates under the neutral measure.
  - **The splurge** is not in the household's Jacobians; the general-equilibrium layer adds it to them afterwards.
  - **The iMPC.** It comes from a simulated lottery, not from a Jacobian column.
  - **What its general-equilibrium layer takes:** only the full T × T matrices, as the HAFiscal-Latest session advises
    the interface should require. It keeps no steady-state policy, distribution or transition for a second tier.
- **DolARK** (EconForge/dolark.py):
  - **No sequence-space Jacobians.** It perturbs the whole state, Reiter-style, by finite differences.
  - **Its split.** An agent's model and the aggregate model are separate documents. Aggregates enter the agent's problem
    as exogenous variables through a "projection".
  - **The agent's two operators.** The aggregate solver uses a backward operator, one step of time iteration given
    today's and tomorrow's prices, and a forward operator, the distribution's transition given the policy and prices.
  - **What the proposal takes from it.** That split, and prices entering the household only as its inputs, are what the
    second tier below asks for.
- **QuantEcon:**
  - **None yet.** Neither the lecture's code nor the community library has sequence-space machinery.
  - **Its probe.** In a scratch probe, JAX's forward-mode derivative of one step of the lecture's endogenous-grid method,
    with respect to R and to the income scale, matched central differences to about 10⁻¹⁰. JAX could therefore give exact
    derivatives of its own discretized step.

## The proposal

### The required output: the Jacobians and their metadata

A results file of the suite carries, for each requested output o and input i:
- **the matrix:** `J[o][i]`, T × T. Column s is the date at which the perturbed value applies and row t the date of the
  outcome; the news arrives at date 0, with the steady state before it, so column 0 has no anticipation;
- **by type and in aggregate,** with the weights: each type's share of aggregate permanent income, which for the toy,
  whose types share their income and survival, is its share of the population;
- **the metadata,** which matters as much as the matrices, since every pitfall below is a convention no matrix shows:
  - each input's dating in words, its units and the measure (income-weighted or per capita);
  - T, and the finite difference's step and scheme, or the method (the fake-news algorithm, a direct finite-horizon
    perturbation, automatic differentiation);
  - the steady state the Jacobians linearize around, per type and in aggregate: C, A, Y_hh, R, ℒ, ρ, the mass at the
    constraint and the mean MPC under both measures;
  - the steady-state solve's tolerance, the residual of one backward step at the steady state, and whether the baseline
    was the steady state or an unperturbed finite-horizon run;
  - the newborns' assets and first-period draws, and what becomes of the assets of the dead;
  - the representation: grid, nodes, how the distribution is pushed forward; the mass put at the top node of the
    distribution's grid, and any mass clipped at the ends of an output's grid.

The file is the canonical interface, as all four sessions advise: any language can write it, the comparison is of each
toolkit's own results, and the sequence_jacobian package's `JacobianDict`, which HAFiscal's general-equilibrium layer
uses, takes exactly these arrays.

**The format.** Each matrix is a file of its own beside the results file, in NumPy's `.npy` format, version 1.0:
little-endian 64-bit floats in C order, shape (T, T). The format is a short text header followed by the raw numbers, so
any language reads it without NumPy, and it keeps every double exactly. CSV or JSON would be about three times larger:
nine output-input pairs for three types and the aggregate make 36 matrices, at T = 300 about 26 MB in `.npy`. The results
file lists each matrix by output, input and type, with its path, shape and SHA-256. The details, from the HARK-dev
session:
- the array is written explicitly in C order. NumPy's `np.save` writes a transposed view with `fortran_order: True`, so
  the writer is `np.lib.format.write_array(f, np.ascontiguousarray(J, dtype='<f8'), version=(1, 0))` or its equivalent;
- the SHA-256 is over the file's bytes;
- a sparse array of the optional tier is three `.npy` files, its rows, columns and values. The indices are `<i8` and
  0-based, the entries in row-major order, sorted, with no (i, j) pair repeated and explicit zeros dropped, so that two
  files of one matrix are identical byte for byte; the results file states the shape. A transition's row i is the node the mass
  leaves, rows sum to one, and next period's distribution is D Λ.

### The optional output: the fake-news ingredients, as data

A toolkit may also export, on its own grid of K nodes:
- the steady-state transition Λ (K × K, sparse), the distribution D (K), and each output's values at the nodes;
- for each input, the news terms of the fake-news algorithm: each output's first-period responses dY₀ˢ for s < T, and
  the distribution's dD₁ˢ (T × K).

From these a harness rebuilds the expectation vectors, the fake-news matrix and J without knowing what the nodes mean,
and compares J with the toolkit's own. It also checks the discretization: D Λ = D, rows summing to one, a single closed
class, the mass at the grid's top node. And when two toolkits disagree it shows whether the difference is in the
backward pass or in the forward propagation. The ingredients are data, not a callable backward step: a callable would tie
the harness to each toolkit's grid, state space and language, and would still run the toolkit's own code (the HARK and
HARK-dev sessions). HARK computes them inside `make_basic_SSJ` and does not yet return them; HAFiscal's code keeps none.

The method itself is checked by a few columns computed directly, s = 0, 1 and T/4, from the toolkit's own finite-horizon
perturbation (for HARK, `calc_impulse_response_manually`, whose dating under `offset=True` open #1826 fixes).

### The conventions every toolkit must follow

- **Dating.** R dated s is the gross return paid at the start of s on the assets carried from s − 1. Income and transfers
  dated s are received in s. The household learns the whole path at date 0 and foresees it.
- **The inputs of a first version:**
  - `return`: the gross return R; a step in the factor is the same step in the rate;
  - `income_scale`: a proportional change in all non-capital income received in s, the unemployment benefit included, as
    the `wage` of HARK's HANK income constructor scales every transitory atom. HAFiscal's own `w` moves employed income
    only, which is the decision below;
  - `transfer`: a transfer proportional to permanent income, x·p to each household alive in s, newborns included, added
    to its income in every state. Every toolkit normalized by permanent income represents it exactly. A transfer equal in
    levels needs permanent income as a state and gives a different iMPC; it can be added for the toolkits that carry it.

  The three differ in incidence, labor income, permanent income and assets, so none is redundant. Later inputs:
  - the benefit ξ_u and the probability ℘, once the schema says whether employed income is renormalized when they move.
    HARK's constructors keep the mean at one, rescaling employed income by (1 − ℘ξ_u)/(1 − ℘), so a higher benefit
    lowers it; HAFiscal's benefit input holds employed income fixed;
  - the discount factor, dated as the factor the date-s decision applies to s + 1;
  - survival and growth, which move the mass of income, once every toolkit carries it.
- **The outputs:**
  - C, consumption;
  - A, the end-of-period assets of everyone alive in s, before that period's deaths;
  - Y_hh, the households' non-capital income received in s, transfers included, which lets the budget identity close
    with nothing taken from outside the file. It is named Y_hh, not Y, so as not to collide with the output Y of a
    general-equilibrium layer the Jacobians are handed to (the HAFiscal-Latest session).

  All are per capita, per unit of the steady state's aggregate permanent income, which the three inputs leave unchanged.
  Mean non-capital income in those units is not quite one: newborns draw the employed branch, whose mean is the employed
  scale κ = (1 − ℘ξ_u)/(1 − ℘), and they hold a share 1 − ℒ𝒢 of aggregate permanent income, so Ȳ = ℒ𝒢 + (1 − ℒ𝒢)κ,
  1.000115 for `iid-ui-artificial`. It does not include capital income.
- **The population:**
  - the family's newborn: born employed, at permanent income 1 with no assets, so a change in R pays it nothing;
  - the dead's assets vanish, so the factor that turns this period's A into next period's resources is ρ = R ℒ. (In an
    economy whose newborns inherited a trend it would be divided by that trend. The family's newborns inherit none; the
    member's own growth 𝒢 does not enter ρ.)
  - the types weighted as above.
- **The horizon:** T = 300 quarters, the default of HARK and HAFiscal, stated in the request.
- **The steady state's precision:** a tolerance of 10⁻¹⁰ or tighter on the steady-state solve, so that the most patient
  type's far anticipation entries are not the steady state's residual.
- **The distribution's grid, the same for every toolkit,** so that the Jacobians differ by the solution and not by the
  representation of the population:
  - **the state:** end-of-period assets a, equivalently the next period's arrival capital, under the income-weighted
    (neutral) measure, in which ψ is drawn from its tilted law ψ f(ψ) and newborns enter with the mass of income the
    survivors leave;
  - **the nodes:** a_j = a_max (j/(N − 1))³ for j = 0, …, N − 1, with N = 1000 and a_max = 500. The node at 0 holds the
    mass at the constraint exactly; near the toy's mean the spacing is under a tenth of quarterly income. So that every
    toolkit passes the same 1000 doubles, bit for bit, each is computed in IEEE-754 double precision as x = j / 999.0,
    then a_j = 500.0 × ((x × x) × x): each operation is correctly rounded, where a power function need not be. HARK's
    own polynomial grid differs by up to four units in the last place, so HARK is given the nodes (the HARK session).
    The checker computes them and states their SHA-256;
  - **the push forward:** Young's lottery. A household's a falls between two neighbouring nodes and is split between
    them in proportion to its distance from each. Mass above a_max is put at a_max and reported, as the results
    schema's coverage asks;
  - **in the request,** N, a_max and the exponent are stated, so that the suite can change them. The solution's own
    grid, and the shocks' quadrature, stay each toolkit's own;
  - **the outputs' means are exact:** C and Y_hh are the means of the policy's values under the distribution. A toolkit
    that bins an output on a grid of its own, as HARK's lottery does for cNrm and yNrm, reports any mass clipped at that
    grid's ends.

### What the checker can verify without solving

Measured on HARK's main branch at `4c285e86` by the HARK and HARK-dev sessions, at illustrative parameters:
1. **The flow budget, column by column:** dC[t,s] + dA[t,s] − ρ dA[t−1,s] − dY_hh[t,s] = cash[t,s], with dA[−1,s] = 0.
   The cash term is ℒ A_ss on row s for `return`, and zero for `income_scale` and `transfer`, whose J^{Y_hh} are known
   exactly: Ȳ times the identity matrix for the income scale, the identity matrix for the transfer.
   - It closed to about 10⁻¹² for the income scale and the transfer, and to between 10⁻¹⁰ and 4·10⁻⁸ for R, the
     residual being the grid's.
   - With the R term one row later it fails by 0.53, so it settles the dating.
   - It also settles the units, the treatment of the dead's assets, and the newborns: a transfer that missed them would
     deliver ℒ of each unit.
   - It cannot catch an error that keeps the budget balanced, such as a wrong level of the MPC. It is linear, so it holds
     for the aggregate over types with the aggregate A_ss. A tolerance of about 10⁻⁶ suits a grid.
2. **The steady state's own budget:** C + A − ρA − Y_hh = 0.
3. **The present value of the transfer columns:** Σ_t ρ^−(t−s) J^{C,transfer}[t,s] = 1, measured 1.0000 at s = 0, 10 and
   60. It follows from the flow budget once A's response has died out, so it is a check that T is long enough.
4. **The first-period entries from the steady state alone:**
   - J^{C,transfer}[0,0] = E[∂c/∂m], the mean MPC under the income measure;
   - J^{C,return}[0,0] = E[(∂c/∂m) b/R];
   - J^{C,income_scale}[0,0] = E[(∂c/∂m) y].

   Agreement to about 10⁻³ is to be expected, given the step, the kink at the constraint and the grid.
5. **Homogeneity for the income scale:** in mid-horizon the row sums Σ_s J[t,s] approach C_ss and A_ss. That holds when
   newborns start with no assets, the constraint is a ≥ 0, and the input scales all non-capital income.
6. **Structure:** J[t,s] → 0 as t − s grows; J[0,s] → 0 as s grows, where an unconverged steady state shows; and
   J[t+1,s+1] − J[t,s], the fake-news matrix, → 0 away from the edges.

Before Jacobians are compared, the steady states are: A_ss, C_ss and the mean MPC. The R columns carry ℒ A_ss, so a
difference in A_ss runs through all of them. Across toolkits, agreement to about 10⁻³ is to be expected, not 10⁻¹⁰.

**The iMPC profile.** The column J^{C,transfer}[·, 0] is the profile of the intertemporal MPC for an infinitesimal
transfer. It is the suite's iMPC. The estimation's finite-prize profile is not reported by the toolkits (the owner's
decision).

### What HARK would need

From the HARK and HARK-dev sessions:
- the HANK income constructor for `income_scale`, and a short constructor adding x to every transitory atom for
  `transfer`, both with `offset=True`, as is R;
- the truncated lognormal, which is not on main: HARK would run the suite from a branch carrying open draft #1863, with
  a constructor of about thirty lines combining the truncated laws with the income scale and the transfer. That is the
  one blocker; the rest is adapter code (the HARK session);
- the types aggregated, by hand or with open #1835;
- the steady state's tolerance set to 10⁻¹⁰. HARK stops when successive solutions move less than its tolerance, which is
  not the error, so for the most patient type open #1823's unperturbed baseline removes what is left;
- the mass above a_max, which HARK puts at the top node but does not report: a few lines of the adapter compute it from
  the steady state;
- the direct columns once open #1826 merges;
- for the optional tier, a small addition that returns the fake-news ingredients, which `make_basic_SSJ` computes but
  does not return; on main an adapter would call SSJutils' private helpers;
- memory. On the shared grid HARK's per-period transitions are dense, K × K, so one input with three outputs peaked at
  4.9 GiB at T = 100 and 13.8 GiB at T = 300 (the HARK-dev session, measured on HARK main `4c285e86`). That needs a large
  machine at the suite's T, and sparse arrays in HARK for a model with a discrete state. The toy's i.i.d. unemployment has
  none.

On the shared grid, with HARK's defaults and the HANK income process, the flow budget closed to 1.5 × 10⁻¹¹, and A_ss
differed from its value on a 301-node grid by 2.9 × 10⁻⁴, the measure of what the grid changes. The shared grid removes
the difference between toolkits' representations, not the grid's own error, which falls at about first order as the
grid is refined (the HAFiscal-Latest session).

On the SSJ route HARK's newborns draw a first permanent shock, which the model-file simulator does not let #1860's switch
turn off. The family's newborn does not, so the remaining difference is stated in the results file until it does.

## The owner's decisions (2026-11-01, 17:05:24)

1. **The tiers:** the Jacobians with their metadata required, and the fake-news ingredients optional, as data.
2. **The inputs:** all as proposed: `return`; `income_scale` moving all non-capital income, the benefit included;
   `transfer` proportional to permanent income, reaching newborns.
3. **The outputs:** left to this session: C, A and Y_hh, per unit of aggregate permanent income, since Y_hh lets the flow
   budget close from the file alone and A is the asset the identity's ρ assumes.
4. **The format:** left to this session: `.npy`, as above.
5. **The representation:** one distribution grid for every toolkit, as above.
6. **The finite-prize iMPC:** omitted; the Jacobian's transfer column is the suite's iMPC.
7. **The steady state's precision:** 10⁻¹⁰.
8. **The QuantEcon module:** not restarted. It was listed because the QuantEcon session said implementing the interface
   there would need it; the owner ruled on 2026-10-21 that no QuantEcon module is published and that dolo's is next. So
   the toolkits that implement the interface are HARK, HAFiscal's code and, once its adapter exists, dolo.

## The results-schema block

Drafted after the toolkits confirmed the grid and the format, and approved by the owner.

- **Where it is.** An optional top-level key `jacobians` of a buffer-stock results file, required in the toy-hafiscal
  suite, validated by [`bst/results.schema.json`](bst/results.schema.json)'s `$defs/Jacobians`. The draft validator it
  was drafted as, `bst/jacobians.schema.json`, is folded in, so that one file validates a results file and readers that
  load it alone need no registry.
- **What it holds:**
  - T, the inputs and the outputs;
  - the conventions in words: each input's dating, the units, the measure, the newborns' assets, first-period draws and
    transfer, and what becomes of the dead's assets;
  - the grid: N, a_max, the exponent, the nodes' SHA-256, and the mass above a_max per type and in aggregate, with any
    output's clipped mass;
  - the method: its name, step, scheme and baseline;
  - the steady state: the tolerance, at most 10⁻¹⁰, the residual of one backward step, and per type and in aggregate
    C, A, Y_hh, R, ℒ, ρ, the mass at the constraint and the mean MPC under both measures;
  - the types' weights;
  - one entry per matrix (output, input and type, or the aggregate), with its relative path to a `.npy` file and its
    SHA-256;
  - optionally, the fake-news ingredients: K, the transition as sparse triplets, the distribution, each output's values
    at the nodes, and for each input and type the news terms dY₀ and dD₁.
- **The shared grid's hash.** The 1000 nodes, as little-endian doubles in order, have SHA-256
  `e88176020da3a4ad8dc6299b9ee06c719b6c9dea93d321e299112a3976944e06`.
- **The request file's keys:** `jacobians: {T, inputs, outputs, grid: {N, a_max, exponent}}`, so that asking for
  Jacobians never changes the model's hash.
- **What the validator checks, and what it leaves to the checker:**
  - the validator: the shapes of the block, the inputs' and outputs' names, the units, a tolerance no looser than 10⁻¹⁰,
    relative paths and hashes;
  - the checker: the matrices' shapes, the files' hashes, the grid's hash, the flow budget, the steady state's budget,
    the present value, the first-period entries, homogeneity, and the structure.
- **Tested:** the results schema with the block is a valid JSON Schema of draft 2020-12. `checker/test_jacobians.py` writes
  synthetic matrices that satisfy every identity, checks that they pass and that a results file holding them validates,
  and checks that each break is caught: the return's term one row late, a transfer that misses newborns, a wrong hash, a
  wrong grid, weights that do not sum to one, a wrong first-period MPC, a missing matrix, a matrix saved transposed, and
  a looser tolerance.

## What follows

- Done on 2026-11-01: the block in the results schema; the checker's verification of the files, the grid, the
  households' income responses, the flow budget, the steady state's budget, the present value and the first-period
  entries, run by `check.py --verify-results` when a results file holds the block.
- The request's keys, `jacobians: {T, inputs, outputs, grid}`, written into the request file's validator when that is
  written.
- HARK's adapter writing the Jacobians through `make_basic_SSJ`, per type and in aggregate, with the neutral measure; and,
  if the optional tier is adopted, the shared harness.
