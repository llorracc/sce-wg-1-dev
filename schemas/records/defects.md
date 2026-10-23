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
- **Matsya's assignment done here.** On 2026-10-19 the owner asked for Matsya to find or develop an ontology of probability
  distributions. This session gathered and digested the candidates itself and mentioned it in one line, where the
  substitution should have been put to him first, Matsya reading no web page. Found on his question at 11:43.
  **Status:** closed 2026-10-19 12:01. The material went to Matsya through the bellman session as digests carrying no
  recommendation, and the memory on routing Matsya's work holds the rule.
- **Time labels by inference, and a misattribution, in messages to other sessions and to the owner.**
  - On 2026-10-19 the owner's ontology direction was reported to the bellman session as made at about 10:35; its stamp
    is 10:54:20.
  - On 2026-10-20 his approval of the coverage check's revision was reported to the two toolkit sessions as made at
    about 22:55; its stamp is 22:57:38.
  - The question put to him at 22:52 called HARK's shortfall formula his.

  **Status:** each corrected within minutes: at 12:02 on 2026-10-19, and at 22:58 on 2026-10-20.
- **The ontology's catalog lines pushed late.** On 2026-10-20 the commit of the finite laws, `76304ab`, was pushed to the
  ontology's draft without its README and changelog lines, an edit of those having failed. **Status:** fixed a minute
  later in `96a8dac`.
- **The quantile at probability 1, required in every quantile map.** `bst-1/results.schema.json` required Q(1), the top of
  the support, which is infinite for every type of the three members, each having a finite tail exponent in the
  checker's report. A computed Q(1) is the largest point with any mass. It grew with the grid's top across the emitter's
  levels and turned on round-off in the reading. Found 2026-10-20 by the HAFiscal-Latest session, when an upgrade of
  Python and numpy moved it alone. **Status:** fixed on the draft pull request #3 (`456994d`, `141d17e`), not merged.
  Files written before keep Q(1), as files of record under `4f99d01`.
- **The first reason given for leaving Q(1) out.** The draft's first commit blamed the far tail's underflow. The
  HAFiscal-Latest session measured the cause as the reading rule: a running total of mass ending within 5·10⁻¹³ of one,
  with either sign. **Status:** corrected 2026-10-20 22:44 in `141d17e`, on the owner's word, with the description to
  match.
- **A results-file change drafted without the toolkits.** The Q(1) change was drafted and opened as a draft pull request
  on one session's recommendation and the owner's quick approval, before HARK's session or HAFiscal-Latest's had been
  asked. Found on his question at 22:26 on 2026-10-20. **Status:** closed by 22:40, both sessions consulted and agreeing.
  The memory on consulting the toolkits holds the rule.
- **The coverage check's first formula.** The draft's first commit, `033908d`, said the tail beyond the top contributes
  about α/(α − 1)·top·top_mass to the mean. That is the true tail's contribution; the computed mean already counts the
  clipped mass at the top, so what the representation misses is about top·top_mass/(α − 1). Found by HARK's review at
  22:47 on 2026-10-20. **Status:** corrected in `967b174` at 22:57, on the owner's word.
- **A question of the owner's left unanswered.** On 2026-10-20 at 09:28 he asked, mid-turn, whether this session and
  Matsya were discussing whether the ontology should live in Bellman's repository or in this one. The question was
  absorbed into the running turn and not answered then; his own choice at 07:16 had already put it here. Found by this
  session's review of its records on 2026-10-21. **Status:** answered in substance by the explanation at 21:52 of how
  the ontology's pull requests relate to the Bellman repository, and reported to him on 2026-10-21.
- **Run times published.** The memorial of 2026-10-21, `5dbfd8e`, carried the emitter's run times: in the ladder
  finding's table, and in the deferred list, the journal of 2026-10-20 and the project state. The community library of
  baseline models publishes no timings and no ranking of toolkits, and the HAFiscal-Latest session publishes none of its
  runs'. Found on that session's message of 08:02 on 2026-10-21. **Status:** removed from the records in the next commit;
  the branch's history keeps them. The memory on timings holds the rule.
- **The natural limit written with the income while unemployed.** The HARK stone of draft #6 wrote the effective member's
  natural limit with the income while unemployed where the worst income belongs: the lowest value of ξ, the lower of the
  income while unemployed and the lowest employed node. On the toy's seven equiprobable nodes the lowest employed node is
  0.558, below the income while unemployed of 0.7. The checker and `model.md`'s formulas were right. Found by the
  community-library session's module at 12:33 on 2026-10-21. **Status:** fixed in `329d78c`, pushed with #6 at 19:58 on
  2026-10-21, in the new notation, where the worst income is `ξ_min` and the income while unemployed ξ_U.
- **The income while unemployed glossed as the minimum of ξ.** `bst/1`'s notation table and the stage file's gloss on its
  unemployment income call that income the minimum of ξ. That is true only when no employed value is lower, as in BST,
  where the income is 0; the toy's lowest employed income is 0.333, below its 0.7. Found on 2026-10-21. **Status:** fixed
  in #7, opened at 19:46 on 2026-10-21: the income while unemployed is ξ_U, glossed as the minimum of ξ only in BST's case.
- **Questions written with a mark the owner's terminal does not draw.** On 2026-10-21 notation questions put to the owner
  used a combining underline, which his terminal shows as a bare letter; the questions read ambiguously, and he had to
  ask what was meant. **Status:** closed: in the terminal, symbols with marks are written in LaTeX, beside their names in
  words.
- **The two targets the other way round.** The schemas wrote the buffer stock target `\check{m}` and the pseudo-target
  `\hat{m}`, as BufferStockTheory's slides do; the paper and econ-ark's notation registry write the target `\hat{m}`
  (`\mTrgNrm`) and the pseudo-target `\check{m}` (`\mBalLvl`). Found on 2026-10-21 while comparing the schemas with the
  registry. **Status:** fixed in #7 (`96898b4`), on the owner's word of 17:06; the slides are the BufferStockTheory
  session's.
- **A push of unknown origin.** The schemas' branch was pushed to GitHub at 16:58:37 on 2026-10-21, carrying `12ff230`, the
  memorial of that afternoon; no command of this session made it, and that memorial had not been approved for pushing.
  **Status:** closed 20:33 on 2026-10-21, the owner confirming that he pushed it himself.
- **Method targets that Bellman's methods files cannot use.** `bst/1`'s and the Markov family's tables, `numerics.md`,
  both Rosetta cards and HARK's adapter attached the expectation's method to the block `dcsn_to_arvl` or its lines,
  named an `evaluate` target that the stage does not have (calling it Bellman's name), put `!egm` on a policy block that
  writes no endogenous grid, and tagged a quadrature of continuous laws `!sum`. Found on 2026-10-22 from the bellman
  session's run of Bellman's check on the stage files. **Status:** fixed in #11 (`ab187c7`), merged at 16:02:43 on
  2026-10-22, on the owner's ruling of 15:11:02 that `bst/1` stays free of any method's lines.
- **A `natural` constraint passed as an artificial one.** HARK's adapter gives HARK `BoroCnstArt` = `a_Art`, and the
  checker resolves a member's `natural` to the stated laws' natural limit. The adapter's effective member then has that
  limit as an artificial constraint, above its nodes' own natural limit, where HARK's Rosetta Stone said that no adapter
  does this. Found on 2026-10-22 while revising the stone. **Status:** the stone corrected in #11 to say what the
  adapter does. Ruled at 18:06:54 on 2026-10-22, and clarified at 18:18:56: HARK computes the natural borrowing
  constraint itself, from the laws' infima, which gives the stated `a_Nat`; a change to HARK's solvers, asked of the
  HARK session. Until it lands the adapter keeps passing the stated limit. No member states `natural` yet. HARK's draft
  #1862 makes the change, and the adapter uses it since #12, merged at 21:32:14 on 2026-10-22.
