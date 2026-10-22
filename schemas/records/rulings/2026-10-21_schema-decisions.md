# Rulings of 2026-10-21

The owner's decisions, in substance and by time (EDT). His words are kept outside this public repository.

- **07:26:34** (question tool), on four questions put to him at 05:00:33:
  - The coverage check's two wording changes, from the toolkits' final looks, are committed and pushed to its draft pull
    request (#4), with the description updated to match. The descriptions of #3 and #4 now say that merging does not wait
    for the emitter's rerun, which reads its own copy of the schemas.
  - The records since the memorial of 09:37 on 2026-10-19 are memorialized and pushed, with the plan
    `existing-syntax.md`, to which the conventions registry of #2 links.
  - Nothing replaces Q(1) above 0.999. The quantile maps keep the fourteen probabilities 0.01 to 0.999, as #3 has them.
    This answers his question of 22:38 on 2026-10-20.
  - The coverage points stay each toolkit's choice, as #4 has them. A statistic comparable across toolkits, which the HARK
    session suggested as one point shared by all of them, is deferred as a separate question.
- **07:39:20.** He asks whether this session or Matsya understands what he means by a Rosetta Stone. He wants to begin
  building Rosetta Stones for HARK and for QuantEcon's toolkits, so that one stage file and one set of parameter values can
  be solved by both and their results compared.
- **07:53:22** (question tool).
  - On QuantEcon's side, the stone is for QuantEcon's own JAX code: the lectures' income-fluctuation solver, with the
    recasting or small extension that the buffer-stock model needs.
  - The Rosetta Stones live in this repository's schemas, with fields shaped like Bellman's Rosetta cards, so that the
    bellman session can turn them into cards later.
  - Matsya takes part, questions only, through the bellman session and on his word there.
- **08:20:49** (question tool). Matsya's brief carries QuantEcon's lecture as plain material, fetched here since Matsya
  reads no web page. It leaves out this session's own recasting of the model, so that Matsya's reading is independent.

After the memorial:

- **08:27:33** (question tool). The run times leave the records, with a defect and a standing rule against publishing
  timings, and this morning's Rosetta Stone rulings are added; the commit is pushed to the schemas' branch.
- **08:32:15** (question tool). The run time leaves `bst/1`'s results files, by a new draft pull request; both toolkit
  sessions had preferred dropping the field to keeping it or making it optional. **08:39:39:** the branch is pushed and
  opened as draft #5. **08:50:30:** its description is corrected to say that the HAFiscal-Latest session's emitter writes
  the field only where the schema has it, so nothing waits on the emitter.
- **08:50:30** (question tool). The Rosetta Stones stay local until Matsya's answers are weighed. `model.md`'s sentence on
  Bellman-SYM's families is corrected in the Rosetta pull request, as a commit of its own.
- **In the bellman session**, as that session reported, not verified here: his go-ahead for a second Matsya session on
  HARK alone, at about 09:22; and by 10:00 his choice to give Matsya HARK's source, excerpts prepared here.
- **11:47:32** (question tool). The Rosetta Stones are committed, pushed and opened as draft #6, then sent to the HARK,
  HAFiscal-Latest and bellman sessions for review. He also declined an older question about a second Matsya session on
  HARK; that session had already run on his word in the bellman session, so the answer is recorded as overtaken.
- **11:59:20** (question tool).
  - The HARK-source session goes ahead.
  - The HARK stone's pointer to the community library's HARK solution is corrected and pushed.
  - QuantEcon's adapter lives in this repository's schemas and imports the community library's solver at a pinned
    commit; the library holds the solver and its results.
- **12:14:52** (question tool). The reviewed revision of #6 is pushed with its description updated. The stones cite what a
  reader can check: HARK at `4c285e86`, the lecture's source at `96ede2993`, HARK's drafts by number, and the
  buffer-stock benchmark's emitter as not yet public. Who read what stays in the records.
- **12:20:54** (question tool). The HARK session's last two corrections to #6 are pushed: HARK stores no natural limit,
  and the laws' own limit is tighter than the nodes' whenever the income while unemployed is positive.
- **12:36:06.** The BST paper is the authority on notation. ξ is the full transitory shock, the unemployment event
  included, and θ the transitory shock of the employed.
- **12:45:30.** He observes that in BST the income while unemployed is the lowest transitory income. Put to him in reply:
  the toy's lowest employed income, 0.333, is below its income while unemployed, 0.7, so the two differ there; the family
  could allow that, as now, or require the lowest employed income to be at least the income while unemployed. **Open:**
  he has not chosen.
- **13:03:35.** The notation proposal is approved as put, to be drafted as its own pull request:
  - Typeset notation follows BST: an underline marks a minimum, so `\underline{\xi}` is the minimum of ξ, and a subscript
    that is a word is set upright, as in `\underline{a}_{\mathrm{Art}}`.
  - Plain text uses names in code font, never pasted into LaTeX as they stand: `ξ_min`, `ψ_min`, `θ_min`, `a_Art`,
    `a_Nat`, `a_min`, `m_min` and `p_worst`.
  - The income while unemployed is μ, as econ-ark's notation file names it.
  - Each family's `model.md` carries a notation table: the typeset form, the plain-text name and the meaning in words.
  - A standing check refuses the combining underline in the schemas and bare multi-letter subscripts in their LaTeX,
    and wants a row in the notation tables for every parameter a stage file declares. The documents' other combining
    marks, a bar, a tilde, a hat and a caron, were not part of the proposal.
  - Bellman, when it typesets a stage file, maps the identifiers the same way; the bellman session is to be told.
- **13:06:11.** This memorial.
- **13:27:28.** μ is withdrawn for the income while unemployed: it has other common uses likely to be wanted here,
  marginal utility and a measure, and econ-ark's notation registry already gives it to log excess resources. Proposed in
  reply: ξ_U, as the Markov family writes it. **Open:** he has not chosen.
- **17:06:40** (typed in the econ-ark-tools session, relayed, and checked as typed by him). The schemas follow econ-ark's
  notation registry on the two targets: the buffer stock target is `\hat{m}` (`\mTrgNrm`) and the pseudo-target `\check{m}`
  (`\mBalLvl`). The schemas had them the other way round, as BufferStockTheory's slides do. Made on the notation branch.
- **Reported from the econ-ark-tools session, about 17:07.** The registry's patience factors take a bold capital thorn,
  `\textbf{Þ}`, the rule these schemas already follow. The same session reported registry v1.0.0 on its master: the growth
  factor is 𝒢, and ξ is the transitory shock with the zero-income event included.
- **17:16:40.** Three answers:
  - the underlined ξ now draws acceptably in his terminal, which he gave as a reason to keep it for the income while
    unemployed (superseded at 17:23:10);
  - the Markov family's growth factor in a quarter is 𝒢_t, not Γ_t, since the registry keeps Γ as a dialect for the
    growth factor itself;
  - the notation pull request is to be committed and pushed, as a draft like the others.
- **17:23:10.** The income while unemployed needs a symbol of its own, since it need not lie below the worst transitory
  shock. That settles the question left open at 12:45:30: `bst/1` allows the lowest employed income below the income while
  unemployed, as the toy has it. μ stays declined for its competing uses, and he asks which letters are free.
- **19:25:18.** **The income while unemployed is ξ_U** (typeset `\xi_{\mathrm{U}}`), the Markov family's spelling. A census
  of the letters econ-ark's notation sources leave free was put to him first: ι, ϖ and ℵ are the least claimed, η is next,
  and every Roman letter is assigned or prohibited by econ-ark's naming conventions. He chose ξ_U over them. This
  supersedes the 13:03:35 item's μ and settles the 13:27:28 open question.
- **19:48:17.** #6 is to be rebased onto the notation pull request, #7, and moved to its notation.
- **19:55:00.** He would rather not force-push, and asks for another way; he approves editing #6, its base and its
  description. Put to him in reply: merge #7's branch into #6's history instead, which needs only an ordinary push.
- **19:58:06.** That is done: the ordinary push of #6, and the edit.
- **19:58:47.** This memorial.
- **19:59:01.** `\IncUnemp`'s expansion in econ-ark's shortcuts is to be fixed, from μ to ξ_U. The file is econ-ark-tools',
  so the request went to that repository's session, which made the change locally; its push waits for his word there.
- **20:33:50.** He confirms that he pushed the schemas' branch at 16:58 himself.
- **20:35:09.** The bellman session is to be told how stage-file names are typeset (sent), and a batch of notation
  proposals is to be drafted for his decision.
- **20:36:49.** No module of QuantEcon's code is to be published; the focus moves to a dolo module.
- **20:37:57.** The first module is HARK's, before dolo's.
- **20:39:38.** HARK's module is to use HARK's Markov consumer, not the standard one, with `bst/1` as the nonpersistent
  chain of the Markov family's nesting: employed and unemployed states with identical rows, unemployment with
  probability ℘ whatever the previous state. The HARK session is consulted first.
- **20:41:10.** The modules are **adapters**, and they live in this repository's schemas (`schemas/adapters/`): an adapter
  reads a parameter file, solves with its toolkit and writes a results file. HARK's starts from the benchmark's emitter,
  scanned before anything is made public.
- **20:41:46.** The nonpersistent chain is as read: the Markov family's nesting of `bst/1`.
- **20:43:30.** The notation batch is approved as proposed:
  - the natural limit written −`ξ_min` `ψ_min`/(ℛ − `ψ_min`), with ℛ = R/𝒢, without κ, which is econ-ark's MPC;
  - the barred thorn replaced by R(1 − `κ_min`), with `κ_min` = max(0, 1 − Þ/R) the limiting MPC;
  - in the Markov family `sep`, `find`, `p_exit`, `reg` and ℷ, and Ω in the HAFiscal design note; z kept for the
    employment state;
  - the plain-text rule narrowed to minima and word subscripts, marks above a letter kept;
  - a request to econ-ark-tools' session for registry rows for the schemas' symbols, `\MPCmin` as max(0, 1 − Þ_R), and a
    plain-text field.
- **22:40:21** (typed in the econ-ark-tools session, relayed, and checked as typed by him). Every branch reconciling
  notation is to be merged, and then the remaining differences reconciled.
- **23:03:44** (question tool, in this session):
  - #7 is pushed, taken out of draft and merged into the schemas' branch with a merge commit (`5b4207f1`, 23:04);
    `notation-bst` is kept. #6's two commits are pushed and its base set back to the schemas' branch.
  - The HARK adapter pins HARK pull request #1858's commit, the Markov solver's fix, until a release includes it.
  - A public results file's provenance carries only what the results schema asks for, with package versions: no
    operating-system or kernel string.
  - The community-library session stops the QuantEcon module and keeps its commits local.
- **23:04:15.** He asks for the remaining questions.
- **23:06:16** (question tool):
  - The fork's pull requests are merged in the planned order: #1 into `main` (23:07), the schemas' branch takes `main`,
    then #2 (23:08), #3, #4, #5 and #6 (23:09–23:10), each with a merge commit. #2's one conflicting README sentence keeps
    #2's wording with `a_Nat`.
  - HARK's #1858 stays a draft; the adapter pins its commit.
  - The ontology's namespace is `sce`, at w3id.org. Its registration, and the change of the namespace with a new version
    of the ontology and of #2's copy of its table, are to follow; the source keeps its provisional namespace until then.
  - The records are brought up to date, committed and pushed.
