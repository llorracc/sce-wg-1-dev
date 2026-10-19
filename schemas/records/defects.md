# Defects

Faults found in this project's own work, with their status.

- **A commit of unknown origin.** `1ca65f0`, "Add draft schemas for the buffer-stock family bst/1", at 11:37:20 EDT on
  2026-10-18, author `llorracc`, carrying this session's attribution trailer, with the seven first-version files. No command
  of this session made it; the owner was asked whether he did. **Status:** closed 2026-10-18 18:28, the owner confirming that
  he made it himself.
- **Moments cancelling to zero.** The truncated lognormal's moment of large order was computed as an exponential times a
  difference of two normal CDFs that both round to one, so it came out as zero and the tail-exponent search ran to overflow.
  **Status:** fixed 2026-10-18 17:21, every law's moments computed in log space with the complementary tails; the tail
  exponents of the members were unchanged by the fix.
- **A floor claimed to bound consumption.** `conditions.md` said that a positive unemployment income bounds consumption below
  and makes the welfare means finite; only a binding artificial constraint does. **Status:** corrected 2026-10-18 on the
  BufferStockTheory session's reading of the paper's remark.
- **Time labels by inference.** Notes after 14:21 on 2026-10-18 carried inferred times, about two and a half hours fast, until
  the bellman session could not match one. **Status:** corrected at 17:40 from file stamps and marked approximate.
- **The first convention of the HAFiscal family's worst income.** The draft stated it as the exhaustion income, which holds only
  when the employed income cannot fall below it. **Status:** corrected 2026-10-18 on the bellman session's finding.
- **The natural constraint claimed to differ by state under truncated laws.** The Markov family's conditions document
  said so of every truncated member; it differs by state only when an unemployed branch's term is the larger, and at the
  paper's calibration under `continues` it is the same in every state. **Status:** corrected 2026-10-18 21:10, on the
  owner's question.
- **Two of the owner's words quoted in the journal.** The entry for the restructuring's approval quoted them; the records
  keep his decisions in substance only. **Status:** removed 2026-10-18 22:5x, caught by the scan before the commit.
- **The community library's names, described as colliding where they agree.** `bst-1/model.md` says two names collide and
  then lists agreements: the library follows BST in bold ξ and θ, in b for the bank balance relative to next period's
  permanent income, in 𝒢, in ℘ and in bold letters for levels. Its one real departure of name is γ for relative risk
  aversion, where BST and these schemas write ρ; it also sets the return factor in sans-serif. Found 2026-10-19 on the
  owner's question. **Status:** fixed 2026-10-19 09:29, on the owner's word: the paragraph now says the library follows
  BST's notation and departs only in γ.
- **Levels written as capitals.** The schemas write levels as P, M, A and C, where BST writes them bold, 𝐩, 𝐦, 𝐚 and 𝐜, as
  the community library does; a departure from the notation ruling. Found 2026-10-19 while checking the library's names.
  **Status:** fixed 2026-10-19 09:29, on the owner's word: levels are bold in both families' documents and the HAFiscal
  design note, and bst/1's notation table lists them.
- **The Markov family's constraint in force, stated as a `max`.** `bst-markov_ui-and-agg/conditions.md` states the
  constraint in force in state z as max(a̲_Art, a̲_Nat(z)), with a̲_Nat(z) the natural limits' own fixed point. The artificial
  limit belongs inside the recursion: a state's limit must keep feasible the constraint in force, artificial or natural,
  in every state that can follow, so the constraint in force is the fixed point of a̲(z) = max(a̲_Art, max over the
  successors z′ of (Γ(z′) ψ̲(z′)/R)(a̲(z′) − ξ̲(z′))), which is what HARK's Markov solver computes. The two agree in `bst/1`,
  at the paper's zero artificial limit, whenever no state without a self-transition has a low income, and under
  untruncated laws, where the employed state, which can follow every state, has a lowest income of zero and so every
  state's limit is zero; with bounded laws and benefits far below the employed floor they differ by a tenth of permanent
  income in some states. The stage file, which can state only untruncated laws today, is therefore exact for every member
  it states; the error is the conditions document's, and it matters for the members with bounded laws and for every
  toolkit's effective member, whose laws are discrete. The same section's rule for one
  written form, the artificial limit at or above every state's natural one, is too strict: an artificial limit binds
  somewhere, and so changes the model, whenever it lies above the lowest natural limit. And its remark that `frozen`
  makes the limits differ by state through a larger multiplier is backwards: a larger multiplier loosens the unemployed
  branch's term. Found 2026-10-19 while weighing the bellman session's advice on the stage files' `max`; checked
  numerically. **Status:** fixed 2026-10-19 09:29, on the owner's word: the Markov conditions document states the
  constraint in force as the fixed point with the artificial limit inside, the rule for one written form as an artificial
  limit above the lowest natural limit, and the multiplier's effect the right way round; the model document follows.
- **"Until the language gains the family" said of every law but the lognormal.** `bst-1/model.md` says a member with a law
  other than the lognormal has no stage file until Bellman-SYM gains its family, and the evening's records spoke of the
  language "gaining bounded laws". Bellman-SYM already states finite point masses, as a mixture, which are bounded; what it
  lacks are the continuous bounded laws, the truncated lognormal, the uniform and the tabulated law. A member with
  discrete laws needs only a stage file written with the mixture. Found 2026-10-19 on the owner's question. **Status:**
  fixed 2026-10-19 09:29, on the owner's word, in both families' model documents and the shock-law document.
