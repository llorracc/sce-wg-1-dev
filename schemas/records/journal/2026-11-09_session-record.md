# Journal of 2026-11-09

Times are EST, from the clock, the transcript or git.

- **10:33:44, in the econ-ark-tools session; received here at 10:34.** The owner has the sessions that used Bellman
  use `bellman-dev`, the development repository, in its place, and examine its changes since they last used Bellman,
  for anything that requires revision. His words, typed there, checked against that session's transcript. From here on
  Bellman is read in the clone of `bellman-dev` on this machine and consulted through the bellman-dev session; the
  clone of `bellman` is gone from this machine.
- **10:34 to 10:45, the review.** What this fork takes from Bellman: the concept slugs pinned in the ontology on
  2026-10-31; its two stage files, last checked against Bellman's main that evening; the distribution grammar that
  [the shock laws](../../shock-laws.md), the ontology of probability distributions and the core's converter write;
  the account of Bellman's method types and registry in the stone convention and in [the accepted
  plan](../plans/2026-11-06_stones-as-data.md); and the public pages read for that plan on 2026-11-06. Bellman-dev's
  main as posted this morning, 195 commits after the evening of 2026-10-31 and 92 after the pages were read, checked
  against each, read-only:
  - **The stage files need no change.** Bellman's package at both ends (version 0.1.6 at both, so the number says
    nothing) was built into scratch environments from the package's own tree and run on `natural.bl` and
    `artificial.bl`: the views and the dossiers are identical, and the encodings differ only in the hashes of the three
    grammar files, which the language's specification 0.7 rewrote between 2026-11-04 and 2026-11-08.
  - **The distribution grammar is unchanged.** The families and their argument forms are the same at both ends:
    `N(μ, v)`, `LogNormal(μ, σ)`, `TruncatedNormal(μ, σ, l, u)`, `TruncatedLogNormal(μ, σ, l, u)`, `Uniform(a, b)`,
    `TypeIExtremeValue(μ, s)`, `Mixture`, `Categorical`, `Bernoulli(p)`, `DiscreteMarkov` and `MarkovChain`. The
    families module changed only the wording of its refusals. The ontology of distributions, the converter and the
    shock-laws document stand; the mixture family in logs with a common shift, deferred since 2026-10-20, has not come.
  - **The concept slugs stand.** None of the 61 pinned is gone; three pages were added, `addition`, `grid` and
    `methods`; of the ten pages the ontology maps its categories and objects to, eight are untouched and two changed
    by one sentence each, neither in substance.
  - **The methods side is what changed**, and it reaches this fork's documents. Specification 0.7 merged into
    Bellman's main on the evening of 2026-11-08 ([the public changelog](https://bellman.io/changelog/), entries of
    2026-11-05 to 11-09). A stage's methods now stand in a methods file beside the stage file, a `.bl` file read by the
    stage grammar whose first line is `@methods: <stage>` and which is unioned with the stage before elaboration
    ([Addition](https://bellman.io/wiki/addition/)); its entries type an operator's method, grid and handler at a
    place named by its path, `policy.method : !egm`, `policy.grid : !Cartesian(a=(a_min, a_max, n_a))`,
    `policy.handler : "cons-port:egm"` ([Methodization](https://bellman.io/Bellman-Sym/04-methodization/)); a method
    takes keyword arguments only, each a declared setting, a number, a string or a word, and a grid names settings and
    holds no number ([Grid](https://bellman.io/wiki/grid/)); the settings are declared in the methods file with their
    domains and valued in a settings file; the catalogue of [method types](https://bellman.io/Bellman-Sym/reference/methods/)
    lists each word with the kinds of place it admits and the keywords the package reads. The method words themselves
    are the ones the stone convention relies on, unchanged. Bellman's own workflow page replaced its "Methods YAML" of
    targets with this file. The stone convention's second desideratum and vocabulary, and the plan's method file,
    describe Bellman's old form: a target, a tag, a handler as a package and a callable. Asked of the fork's two stage
    files under the new package, `stage.places()` lists their places: the policy's solution method is typed at the
    builder, `policy.method`; the place the schemas name for it, `policy.euler.solve`, exists in neither file, the
    Euler line's places being the statement `policy.euler` and its derivative `policy.euler.D`, which settles in
    Bellman's terms the question the plan left to the model repository's session; the expectation is the place
    `dcsn_to_arvl.E_ψ_θ_j`, the interpolants the `evaluate` places of the three builders, the population's transition
    the forward builder `dcsn_to_cntn`. The listing is sent to the model repository's session, whose stones hold the
    method files.
  - **The documentation is public.** Since the evening of 2026-11-08 the site answers at bellman.io, by its own
    record of that evening; the address this fork's plan cites, under econ-ark's GitHub pages, redirects there, and the
    pages the plan names answer. The three repositories, `bellman`, `bellman-dev` and `bellman-ark`, still answer an
    unauthenticated request with 404 at 10:3x and are treated as private. The ontology's statement that Bellman-SYM's
    documentation is not public, written on 2026-10-31, is therefore stale as a statement of fact, in its README, in
    the header of `bellman-concepts.txt`, in the generator's property description and in the generated files; its
    rule that a concept is named and never linked was that statement's consequence, and is the owner's to keep or
    lift.
  - **Still pending in Bellman:** the three changes asked on 2026-10-31 appear in none of the commits; the comparator
    is unchanged; nothing new on the condition form of a declared set's limits.
- **Put to the owner, not done:** a revision of the stone convention's second desideratum and vocabulary from
  targets and tags to Bellman's places, method words with keyword arguments, grids and handlers, with the question
  whether a stone's method file is to be a Bellman methods file, one per toolkit, which Bellman would then check; the
  ontology's statement of fact corrected, with or without the rule; the plan's addresses brought to bellman.io. Nothing
  changed on the fork's main. The records: [the pointers](../memory/reference_pointers.md), [the routing
  memory](../memory/feedback_route-matsya-work-to-matsya.md), [the deferred items](../deferred.md) and [the
  state](../memory/project_state.md) say bellman-dev where they said bellman.

**State at the end of the entry.** The fork's main at 7a4889f, pushed; this records branch not pushed, held on the
HAFiscal session's open question; the three proposals above with the owner; the model repository's session told of the
places; the second model repository's design and name his to settle in that session.
