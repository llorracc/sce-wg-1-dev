# The Jacobian interface's consultation

2026-11-01, 16:37–17:23 EST, on the owner's request of 16:37:49 and his decisions of 17:05:24 (`../../jacobians.md`).

## What was read

- **Read-only surveys,** by this session's delegated readers:
  - HARK's main branch at `a0fe5740`: `make_basic_SSJ` and `calc_jacobian`;
  - HAFiscal's published package, HAFiscal-QE at `fa3adfd`: its own fake-news code on HARK, with the sequence_jacobian
    package for the general equilibrium only;
  - EconForge/dolark.py at `b0eef38` and econ-ark/DARKolo at `8e428de`: no sequence-space Jacobians; a backward and a
    forward operator, and the projection of aggregates into the agent's problem.
- **The four sessions' answers:** QuantEcon, HAFiscal-Latest, HARK and HARK-dev. Their private items are not recorded
  here.

## What the HARK sessions measured

Measured on HARK main `4c285e86` at illustrative parameters, not a member of the schemas:
- **The flow budget,** dC + dA − ρ dA₋₁ − dY = cash, closed to:
  - about 10⁻¹² for the income scale and the transfer;
  - between 10⁻¹⁰ and 4 · 10⁻⁸ for R.
  With R's term one row later it failed by 0.53, so the identity settles the dating.
- **The present value** of the transfer columns was 1.0000 at s = 0, 10 and 60.
- **HARK's two routes** date R and income alike and the discount factor one period apart. They agree to within about
  half a percent once newborns start from the same wealth.
- **On the shared grid,** 1000 nodes to 500 with exponent 3:
  - the flow budget closed to 1.5 · 10⁻¹¹;
  - A_ss moved by 2.9 · 10⁻⁴ from a 301-node grid;
  - memory peaked at 4.9 GiB at T = 100 and 13.8 GiB at T = 300, for one input with three outputs.
- **Patient types:** at HARK's default tolerance, open #1823 measures errors of 47–57% for growth-patience factors of
  0.997–0.9997.

## What this session tested

In a scratch run, the draft validator `../../bst/jacobians.schema.json` is a valid JSON Schema of draft 2020-12. A full
example, three inputs, three outputs and three types with the aggregate, 36 matrices, validates. A tolerance looser than
10⁻¹⁰, an unknown input, an absolute path and missing dating are each refused. The shared grid's nodes, computed as
x = j/999 and a_j = 500((x · x) · x), have SHA-256 `e88176020da3a4ad8dc6299b9ee06c719b6c9dea93d321e299112a3976944e06`.

## What it does not establish

- No toolkit has written a Jacobians block.
- The checker's verifications are designed but not written.
- The measured identities are HARK's on its own parameters, not on a member of the toy-hafiscal suite. That member's
  β's are not yet estimated.

## Pending

- The owner's approval of the block.
- HARK's run from a branch carrying #1863.
- HAFiscal's plumbing for the toy member, on the owner's word.
