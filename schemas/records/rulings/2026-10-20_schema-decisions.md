# Rulings of 2026-10-20

The owner's decisions, in substance and by time (EDT). His words are kept outside this public repository. A decision made
in another session is recorded here only as this session verified it there.

- **07:04 to 07:36, in the bellman session's question tool.** The decisions on the ontology put to him the evening before.
  This session read his answers in that session's transcript by 08:09 and found they matched its report; he confirmed
  them here at 09:24:44. All were as recommended, except where noted:
  - **07:04:56.** Bellman decides the support of its other families in a separate small amendment after the merge, and a
    provider named in a methods file stays unbuilt until a methods target names a law.
  - **07:07:46.**
    - In a parameter file, no bound on a side is written `null`, and an omitted bound means three standard deviations.
    - An untruncated component of the truncated mixture law writes `null` on both sides.
    - Matsya's three settlements are adopted: a pinned mean is a constraint defining a subfamily whose reduced
      parameterization is its chart; a mixture's relative means restrict the chart's domain; the point mass is a family of
      its own, with `N(μ, 0)`, `LogNormal(μ, 0)` and `Degenerate` among its charts.
    - The first release's catalog is what the schemas and Bellman need, with rows added as they are needed.
  - **07:16:06,** after his own proposal, typed there at 07:12:14, of a top-level folder for the project's ontologies,
    since there are likely to be several.
    - The home is `ontologies/probability-distributions/` in this repository.
    - The machine-readable form is as proposed: one YAML source generating OWL 2 in Turtle and a flat JSON table, opaque
      permanent identifiers, a w3id.org namespace, CC BY 4.0, and versioned releases.
    - Rows cross-reference ProbOnto by `skos:exactMatch` and `skos:closeMatch`.
    - The parameter file's hash binds the schema's version alone.
  - **07:20:41.**
    - A relative tolerance of 10⁻¹² applies where a conversion is irrational, and never to the hash.
    - The truncated mixture laws reach a stage file both ways: through the converter's numbers now, and through a Bellman
      family for a mixture in logs by a later amendment.
    - The ontology's release stays out of a stage's encoding. Bellman's family table carries the release it was checked
      against, and a test checks it against a copy of the ontology's table.
  - **07:32:33 and 07:36:16.** Bellman's main had gained `TruncatedNormal(μ, σ, l, u)` that morning, written in levels
    with the location first, and Bellman-SYM's truncated lognormal is aligned with it.
    - It is `TruncatedLogNormal(μ, σ, l, u)`: it takes the mean and standard deviation of the logarithm, as
      `LogNormal(μ, σ)` does, with bounds on the draw itself, and requires σ > 0, as the truncated normal does.
    - This supersedes two of his choices there at 07:04:56: to keep the family as its branch built it,
      `TruncatedLogNormal(σ, bot, top, m)`, and to admit σ = 0.
    - The schemas' convention, bounds in standard deviations and a mean of one, becomes the converter's arithmetic.
    - Bellman's draft pull request opens once Bellman's main is merged into its branch.
- **09:24:44** (question tool).
  - The ontology and the schemas' changes are built on those answers.
  - The parameter file's `NormalMixture` splits into `LogNormalMixture` and `TruncatedLogNormalMixture`.
  - The name of the w3id.org namespace is decided later.
- **09:41:22** (question tool). The ontology's first piece is committed, pushed to the fork and opened as a draft pull
  request into the fork's `main`. Each further family is pushed to that branch when ready, without asking each time.
- **15:04:05 to 15:04:31.** The schemas' change, asked about at 10:18.
  - At 15:04:05, by the question tool, he chose to commit it only.
  - Once the commit was made, he typed at 15:04:25 and 15:04:31 to go ahead with all of it: the schemas' branch pushed
    with its two memorial commits of 2026-10-19, the new branch pushed, and a draft pull request opened into the schemas'
    branch.
- **15:16:26 and 15:18:42.** Bellman's comparator is to integrate the uniform, by a pull request. On the rule of one session
  per repository, the work goes to the bellman session, whose push and pull request wait for his word there.
- **20:43:29, typed in the HAFiscal-Latest session** (verified here at 21:05 in that session's transcript). The emitter
  program resumes, and its ladder starts over from the first level.
- **21:49:24, typed in the HAFiscal-Latest session** (verified here at 21:53 in that session's transcript, as his answer to
  that session's question on it). The quantile at probability 1 is dropped from `bst/1`'s results schema.
- **21:57:30** (question tool). That change is pushed and opened as a draft pull request into the schemas' branch.
- **22:26:33.** What a results file carries is more properly the toolkits' question, HARK's and HAFiscal-Latest's; he asked
  whether their sessions had been consulted. They had not; the standing rule is the memory on consulting the toolkits.
- **22:38:13.** The toolkits' consensus to drop Q(1) persuades him, and he asks what should replace it. He has not ruled on
  the answer given: Q(0.999) is already the quantile maps' top entry, and nothing above it is recommended.
- **22:42:20** (question tool).
  - The corrected reason for dropping Q(1) is committed and pushed to its pull request, and the description is updated to
    match.
  - The coverage check both sessions suggested is drafted as a separate draft pull request and sent to both for review
    before any decision on merging.
- **22:57:38** (question tool). The coverage check's revision, folding in both reviews, is pushed with its description
  updated, and sent to both sessions for a final look.

**Open with him:**
- whether anything replaces Q(1) above 0.999;
- HARK's suggestion of one coverage point shared by every toolkit, against each toolkit's own points, which the draft keeps;
- the name of the w3id.org namespace;
- the uniform's pull request in the bellman session;
- the coverage check's two wording changes from the toolkits' final looks, which are uncommitted;
- every merge, in the order the project state gives.

The first, second and fifth were settled on 2026-10-21; see that day's rulings.

The rerun of the toy's fourth level, which the HAFiscal-Latest session announced at 04:45 on 2026-10-21, comes under the
emitter program he resumed at 20:43:29.
