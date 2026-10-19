# The Matsya completeness job on bst/1

**What ran.** On 2026-10-18, on the owner's word typed in the bellman session, that session submitted one Matsya job with a
stage file as its target, on the model document and the shock-law document of `bst/1` as pushed at `b218377`, unedited,
three cycles, no formulation given, under the service's default configuration. Submitted at 20:32:56 EDT, ended at 20:53:38,
twenty minutes and forty-two seconds; eighteen model calls, about 759 thousand input tokens and 112 thousand output tokens,
the client reporting no money figure. It asked no question and ended converged, with the reason "semantic fixed point", the
objects of its second and third cycles being equivalent. Its inputs, output and full record are kept outside this
repository.

**What the inputs were.** Since the restructuring, the model document restates the stage file block by block, so the job
tested how faithfully the prose and its restatement carry the stage file, not whether the prose alone yields it. The bellman
session had prepared prose-only copies, with the restatement and the Bellman counterparts removed; the owner chose the files
as pushed.

**The differences from [`bst-1/bellman/buffer_stock.bl`](../../bst-1/bellman/buffer_stock.bl)**, up to renaming:

1. **The unemployment law came out flipped.** The final file draws the employed label with the unemployment probability,
   while its income map keeps the prose's scaling of the employed draw, so E[ξ] is not one and, at the library's
   calibration, the household would be unemployed almost always. Attributed to Matsya, with Bellman's printing contributing.
   The first declaration, read from the prose, was right, a Bernoulli drawing the unemployed label with probability ℘. In the
   first cycle the prose written back from the elaborated object read the dossier's Bernoulli over two labels as drawing the
   first, the writer followed it, and since convergence compares adjacent cycles only, the second and third cycles converged
   on the flipped law. The round-trip judge recorded the contradiction. Not the prose's fault: the model document says which
   label ℘ draws.
2. **One borrowing limit in place of two.** The writer collapsed a̲ = max(a̲_Art, a̲_Nat) into one parameter on (−∞, 0].
   Matsya's. One point in its favor: that domain matches the model document's a̲_Nat ≤ a̲_Art ≤ 0, which our stage file does
   not state, declaring both limits on ℝ. Tightening ours, with a condition on one parameter naming the other, is a decision
   for the owner; the bellman session can test the syntax.
3. **The standard deviations of the logs on ℝ₊**, zero admitted, where ours has ℝ₊₊: the prose's, and minor. The shock-law
   document admits a zero spread only through the degenerate law, which a lognormal stage file cannot tie to it, so ours
   takes the stricter reading; the model document now says so.
4. **Everything else agrees in substance:** the arrival state on [a̲, ∞), m ∈ ℝ, a = m − c; the lognormal laws of ψ and θ
   with mean one; the law of motion with the two branches of ξ; the value and marginal-value lines with β ℒ; the two
   expectations; the feasible set; the Euler line with its complementarity clause; ρ ∈ (1, ∞). Its argmax is operative where
   ours is documentation.
5. **Beyond the prose** it supplied the sets of ψ and θ as ℝ₊₊ and a stage name. **It left open** what the language cannot
   state: the identification of V[>] with the next period, terminal data, the attainment of the maximum, a = m − c staying in
   its set, and integrability. It asked nothing about the types, the restatement saying "one type's problem".

**What it establishes, and what it does not.** The prose and the stage file contradict each other nowhere; a toolkit author
reading both gets one model. Whether the prose alone determines the file was not tested, since the files restate it. That
test remains possible with the prose-only copies, at the cost of a second job, and its premise has weakened: since the
restructuring the prose is a reading of the file by design. Two points for Bellman's maintainer came out of the job, to be
filed on the owner's word: the dossier should name which label a Bernoulli over labels draws with probability p; and a job
whose fixed point differs from its initial declaration should say so in its status.
