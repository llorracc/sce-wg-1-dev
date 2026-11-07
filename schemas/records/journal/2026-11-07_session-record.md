# Journal of 2026-11-07

Times are EST, from the clock, the transcript or git.

- **08:49:35.** The owner says to push main. The fork's main, two commits ahead of its remote since the evening's
  merge, holds only the stone convention's revision in `rosetta/README.md` (89 lines added, 33 removed), nothing of
  the held fact, checked against the diff before the push. Pushed before 08:50:00: the fork's main stands at 7a4889f
  on the remote, even with the local branch. The convention's revision is now public on the fork; it reaches the
  working group's repository through the open upstream pull request #18, which carries the stone convention, as a
  further commit on that pull request's branch or a pull request after it, on his word.

- **09:22:03.** The owner questions the held fact's description, that HARK's grid has no point at a binding
  artificial constraint: several grids are in play, and his understanding was that the cusp at a = 0 is put into the
  grids of the consumption, value and marginal-value functions by hand. Read in HARK at the adapter's pin
  (llorracc/HARK 11852805, econ-ark 0.17.2) and measured on the restrained member at the low level: the asset grid is
  shifted by the natural limit, not the artificial one; the point inserted by hand is the domain's bottom, where
  consumption is zero, prepended to the rule's nodes and to the value function's; the rule is a lower envelope of the
  unconstrained interpolant and the 45-degree line, evaluated pointwise, so the cusp is a node of nothing. For the
  restrained member at 300 gridpoints the natural limit is m = −0.7159, 108 endogenous points lie below a = 0, the
  nearest at a = −3.3 × 10⁻⁴, and the envelope's kink at m = 0.976857 falls between the nodes at 0.976281 and
  0.998280, the unconstrained cubic's slope 0.4211 on both sides of it; the crossing and the Euler-equation root agree
  to 4 × 10⁻⁹. HARK does insert a = 0 by hand in its kinked-return solver, where the kink in the return must be on the
  grid, with two points and the chord between them, and in the preference-shock and medical-shock models. Answered so;
  the description stands with that precision.
- **09:38:05.** The owner gives the reason for the design: with a node at the kink and the Hermite method, the
  left and right derivatives at the node differ and that is not easy to work around; solving under the natural
  constraint alone, no node is a kink. He places it among the problems behind HARK's pull request that prohibits the
  Hermite method with the discrete representation of the distribution, and asks that HARK's code carry an in-place
  explanation. Relayed to the HARK session, which owns the clone, with his words and their stamp, the locations at
  the pin in both buffer-stock solvers and the kinked-return contrast, and the measurement; its reply is awaited
  ([the deferred items](../deferred.md)). Nothing changed here; this fork holds no HARK code.

**State at the end of the entry.** The fork's main pushed, 7a4889f, with the stone convention's revision; [the
proposals](../plans/2026-11-06_stones-as-data.md) ACCEPTED, their execution in the stones and adapters the model
repository's session's on his word there; this records branch not pushed, held on the HAFiscal session's open
question, on which six places of the handoff bundle also wait. Open as before: his decisions on both plans in the
HARK-dev session; the convention's revision upstream through #18 or a follow-up.
