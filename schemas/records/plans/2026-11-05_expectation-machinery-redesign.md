# A redesign of HARK's expectation machinery: the laws first-class, the method chosen at solve time

**Status: HANDED OFF to the HARK-dev session on 2026-11-05, sent at 15:38:43 EST and confirmed filed at 15:54:22,
on the owner's ruling of 15:09:32 that the redesign should have been formulated there and his choices of 15:32:48.**
Proposed here at about 14:10 on his request of 13:46:09, with the HARK, HARK-dev and HAFiscal-Latest sessions consulted
that afternoon. The design is now a plan of econ-ark/HARK-dev, where its decisions are put to the owner:

- the plan: `plans/20261105-1411h_expectation-machinery-redesign_plan.md`
- the handoff record it was made from: `records/handoffs/2026-11-05_expectation-redesign-from-sce-wg-1-dev/`

That repository is private to econ-ark's admins, so these names serve those who can open it. The full text as proposed
here is in this branch's history at af8e609. This file keeps the two parts that are the working group's own: the
request in substance and what the harness needs of any such redesign. How the handoff was made is in
[the handoff plan](2026-11-05_handoff-to-hark-dev.md).

## The request, in substance

The continuous expectation and the solver that uses it have been retrofitted onto a structure in which a solver sees
only the atoms of a discretized distribution. That keeps today's behavior intact but has reached the point where a
thorough redesign may serve better: one in which a solver can be told, when it is called, whether to take its
expectations by a discrete method or a continuous one, so that the two methods' results can be compared directly on
the same laws, and so that an adapter can instruct HARK to solve a model either way.

## What the working group's harness needs of it

These are fixed by the schemas and the rulings, whatever the architecture.

- **The method is the adapter's to name, per precision level.** A method file names, on the stage's expectation
  operator `E_ψ_θ_j`, the method's tag, `!quadrature` for nodes or pieces that approximate the laws and `!sum` only
  where every law is finite, with HARK's routine as the handler and the settings the handler reads: for the discrete
  method the node counts and their placement, for the continuous one the nodes per piece and where the pieces split
  (`schemas/bst/model.md`, "Method targets"; `schemas/numerics.md`). The diagnostics' expectation, which the Euler
  residuals use, must differ from the household's. So the redesign's switch must be settable from outside a solve,
  per run, with its settings recorded.
- **The effective member is what was solved.** A results file reports the expectations under the toolkit's own
  approximation of the laws, the lowest values, the mass at the worst income and the derived parameters
  (`schemas/bst/results.md`, "The effective member"). Under the discrete method these are the atoms'; under the
  continuous method they are the stated laws' own, to the quadrature's error, with the lowest values the infima. The
  redesign must make both reportable from the same object, and the landing mass the laws' in both.
- **The representation is the toolkit's** (the ruling of 2026-11-02): how HARK represents the laws is HARK's choice,
  stated in its stone and its method file, never prescribed by the harness. The redesign therefore decides HARK's
  representations; the harness only asks that each be named and refinable.
- **Two methods in one toolkit are two modes**, keyed with the toolkit in the registry and compared by the comparator
  as two toolkits would be (`schemas/registry.md`, "Modes of solution", the ruling of 2026-11-04): the same laws, the
  same member, two results files, their distances on the experiment's quantities, and the checks between them. That
  is the direct comparison the owner asks for, and it tests HARK's consistency and the definition at once.
- **Both methods must be valid methods** under the exactness criterion (`project-a/exact-definition.md`): every choice
  of theirs refinable without bound, the node count of the discrete method and the pieces and nodes of the continuous
  one, with no default that is not itself refinable. The test is convergence: each method's results fall with its
  level, and the two methods approach each other as both are refined, which the experiment's checks `falls_with_level`
  and `compare: toolkits` can state as written.
- **The reference solution** (the ruling of 2026-11-04 at 06:23:39) is to come from the continuous methods at very
  high precision; under the redesign it is HARK's continuous method at its finest settings, with the point-mass
  landing right, and its certified errors from the convergence in the settings.

## The rest of the proposal

The three sessions' accounts, where they agree and differ, the proposal itself, its cost and order, and the seven
decisions for the owner are HARK-dev's from the handoff on, in the plan and the handoff record named above. What this
repository asks of the result is the section above; the adapter's and the comparator's parts of it are in
`schemas/bst/model.md`, `schemas/numerics.md`, `schemas/registry.md` and `project-a/exact-definition.md`, as the
section cites them.
