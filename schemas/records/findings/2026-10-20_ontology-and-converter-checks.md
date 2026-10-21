# The ontology's tests, and the converter at Bellman's draft

**The ontology.** Draft pull request #1: `ontologies/probability-distributions/`, version 0.1.0-draft.1, rows
`PD_0000001` to `PD_0000063`.
- **The tests check:**
  - that every conversion round-trips;
  - that every stated mean and moment agrees, by quadrature, with the measure the row defines;
  - that every coordinate stated as an expectation equals it, so a spread after truncation cannot pass for one before;
  - that the constraints hold, and the boundaries and reductions meet the families they name;
  - that the generated files are current, and the Turtle parses.
- **Twelve tests pass** at the head, `44d10cc`.
- **Deliberate breaks.** As each family was added, the tests were also run against deliberately broken copies of the
  source, and every break was caught.
- **Bellman's families.** Every family name in Bellman-SYM's table resolves to a row, by the head of its written form.
- **One departure from Matsya's design:** the normal is compared in its mean and standard deviation, not its mean and
  variance. It changes no written form and no hash.

**The schemas on it.** Draft pull request #2, `0583a60`.
- The hash over the filled form leaves the three members' hashes unchanged: library `fee9fcced828…`, toy
  `2fe95c8cf8e5…`, toy-untruncated `32a326c4bfd5…`.
- The cross-test reads every law through the vendored table alone. Its mean, moments and support agree with the checker's
  closed forms to 10⁻¹².
- 123 tests pass.
- The checker caught a mistake in one of this session's own test examples: a `Discrete` law with mean 1.1.

**The converter at Bellman's draft.** The bellman session reported this at 15:07 on 2026-10-20.
- **The calls.** The converter's eleven Bellman-SYM calls were tried at the head of Bellman's draft pull request for the
  truncated lognormal: the members' laws, a law truncated below only and one above only, `Uniform`, `Degenerate`, a
  `Discrete`, and the three kinds of mixture.
- **What happened.** Each elaborated in place of ψ's law in the buffer-stock stage, calibrated, and had its graphs built.
- **The means.** Bellman's closed forms give each call a mean of 1.000000000000, which confirms the converter's locations
  and common shifts.
- **Bellman's comparator,** integrating the retained law, agrees:
  - within 4.2·10⁻⁹ for the toy's two laws, and 2.4·10⁻¹⁰ for the truncated mixture;
  - exactly for the library's lognormal, the point mass, the discrete law and the untruncated mixture;
  - within 2.0·10⁻⁶, 4.3·10⁻⁶ and 1.75·10⁻⁵ for the mixture with one untruncated component, the law truncated above only
    and the law truncated below only. These last three come from its twelve-node quadrature over a one-sided window, not
    from the law.
- **The uniform** elaborates, with mean one by its closed form, but the comparator does not integrate a uniform.
- **The support condition** is established at calibration for the five lone truncated laws: [0.84531, 1.17945] for the
  toy's ψ and [0.328485, 2.70059] for its θ. It stays required for the rest, as the branch's design has it.

**What it establishes.** The ontology's rows, the schemas' closed forms and Bellman's closed forms state the same laws. The
truncated laws work only with Bellman's draft family, and the uniform's numerical cross-check waits for Bellman's
comparator.

**What it does not:** the review of Bellman's draft, which may change its spelling, and with it the ontology's row and
both copies of its table.
