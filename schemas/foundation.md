# The stage file as the foundation of a family's statement

Draft design note, 2026-10-18; see the [README](README.md). Approved by Chris the same day; of the six steps below, the first
five were done that evening (the fifth, the Markov family's stage file, was delivered by the bellman session at 17:40 EDT and
gained its three-valued switch by 18:37), and the sixth waits for the model document to settle and for Chris's word.

## The ruling

A family's true model is to be stated on the `.bl` machinery of Bellman-SYM, the project's language for staged Bellman
problems. The stage file is the normative statement of the household's problem; prose covers what the language cannot yet
state. The schema directory was built the other way around, with prose normative and the stage file a check, and this note
says what changes.

## What a stage file states today, and what it cannot

For `bst/1`, [`bst-1/bellman/buffer_stock.bl`](bst-1/bellman/buffer_stock.bl) states, with its domains, conditions and blocks: the
state and its set; every parameter with its domain, in BST's notation where the language admits the symbol; the shocks and
their laws; the law of motion; the budget; the value and marginal-value recursions with their discounting; the policy
condition as the Euler equation with its complementarity clause; and the borrowing constraint in force, `max(a_Art, a_Nat)`.
The file elaborates and calibrates under Bellman, and a Matsya reading of it found it to state the survivor's problem of the
prose exactly.

What a stage file cannot carry, found by the bellman session and by Matsya's reading on 2026-10-18:
- a population of types with shares, so one stage serves one type, and a member of K types is K calibrations;
- survival as an event, death and replacement, and the newborn's placement; mortality enters only as discounting;
- the stationary population and its two measures, and the infinite-horizon stationarity itself, since a trellis is finitely
  many periods;
- the shock laws outside Bellman's seven families: the truncated lognormal, the uniform and the tabulated law have no
  counterpart, and no family's mean is checked;
- a parameter the laws determine, such as a̲_Nat, which Bellman takes as a calibration entry;
- a piecewise utility, which `bst/1` sidesteps by requiring ρ > 1, as BST does;
- the conditions and implications, beyond conditions attached to a parameter's declaration, which the language records and
  calibration may or may not decide.

## The layered statement of a family

A family is stated in layers, the first normative where it speaks:

1. **The stage files**, the household's one-period problem: states, domains, parameters, laws of the shocks the language
   knows, law of motion, budget, recursion, policy condition.
2. **The population layer**, in prose and in the parameter schema: the types and shares, survival with replacement, the
   newborn's placement, the stationary population and its measures, and what the family fixes.
3. **The shock laws**, the shared [vocabulary](shock-laws.md), with each law's mapping to a Bellman family where one exists
   and the mean-one convention the stage file assumes.
4. **The conditions and implications**: validity, domain rules, testable implications, the simulation phase.
5. **The results schema.**

The prose of the model document becomes, for layer 1, a reading of the stage file block by block, in BST's notation, which
adds nothing the file does not say; layers 2 to 5 stay as they are.

## How the files map

| the schema's file | Bellman's | what the converter does | what is lost |
|---|---|---|---|
| parameter file | the calibration mapping | writes each parameter under the stage's name; computes a̲_Nat from the laws and writes it; writes one calibration per type | the types' shares, the laws' families, the population layer |
| method file | the stage's methods file | maps each address to an `on:` target | parts with no target: the population's distribution, the diagnostics' expectation |
| settings file | the settings file | copies | nothing; Bellman keeps settings no method reads |
| suite file | fill slots and variants | expands into one fill per element | the named levels, the element hashes |
| results file | nothing | | everything |

The addressable parts of the model document become the stage file's own ids where the stage has them: the policy block,
the expectation in the decision-to-arrival block, the forward blocks for the population's transition; the population's
distribution and the diagnostics' expectation keep names of the schema's own, since the stage has no target for them. A
method on a kind, such as every expectation, maps to Bellman's operator-name target.

## The restructuring, in order

1. Reorganize `bst-1/model.md` around the stage files: the household's problem section becomes the reading of the file;
   the population layer, the parameter file and the member examples stay.
2. Replace the addressable parts' names with the stage files' ids, in the model document and in `numerics.md`, keeping
   `population.distribution` and `diagnostics.expectation`.
3. State in `shock-laws.md`, for each law, its Bellman family or its absence.
4. Write the converter from a parameter file to Bellman's calibration, in the checker, with a̲_Nat computed.
5. For `bst-markov_ui-and-agg/1`, write the stage file first, with its chain as named states, and the prose from it.
6. Run one Matsya job on the finished `bst/1` model document as the completeness test, once, as decided.

Nothing downstream of the schema directory exists yet, so the restructuring breaks nothing; the checker's names change
with the addresses.

## Requests to Bellman

What the families need the language to gain, for its maintainers to weigh, in the order the schemas need them:
1. The missing law families, with a stated mean-one convention: the truncated lognormal with the stated standard
   deviation after truncation, the uniform in levels, the tabulated quantile law, and a check that a declared law has mean
   one.
2. A population construct: types with shares, survival as an event with replacement, and the newborn's placement.
3. A statement of infinite-horizon stationarity, the fixed point the stage file does not impose.
4. A derived parameter in the calibration, so that a̲_Nat is computed from the laws rather than written by hand.
5. A results or solution format, so that a solver bound to a stage can return what the results schema asks.
6. The documentation defect the bellman session found: the constraints page's example of a clause on the candidate line,
   which the elaborator now refuses.
7. Later, should a family need log utility: a piecewise utility or a conditional line.

## Decisions

Taken by Chris on 2026-10-18:
- The restructuring is approved in the order above.
- The addresses become the stage file's own targets, each with a comment that explains it.
- The requests go to Bellman's maintainer through the bellman session, under Chris's name.
- ρ = 1 is dropped from `bst/1` for now, for simplicity: the family requires ρ > 1, as BST does, so there is no second stage
  file.
