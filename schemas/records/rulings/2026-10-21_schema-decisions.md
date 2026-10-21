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
