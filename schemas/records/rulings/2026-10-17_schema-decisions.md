# Rulings of 2026-10-17

The owner's decisions on the handoff day, in substance and by time (EDT); his words are kept outside this public repository.

- **About 13:08.** The schema project is handed from the HAFiscal-Latest session to this repository's session; the work branch
  is `buffer-stock-schema-work_CDC`.
- **About 13:15.** The word is "schema". Comparison points cannot be one fixed list, since the right points depend on the
  parameterization. A precision ladder is not required but is to be available as named levels low, medium and high. The
  export of the consumption rule is required. The schemas' final home is `econ-ark/sce-wg-1`, reached by pull request from
  this fork.
- **About 13:50.** The schema must not impose lognormality, which is only convenient; the default is a truncated lognormal.
  This revises the earlier reading that the shocks are continuous lognormals: the law is a parameter, and a quadrature is a
  toolkit's choice.
- **About 14:00.** A truncated lognormal keeps mean one by shifting the log mean, with the bounds in standard deviations of the
  log. The laws offered include the truncated and the untruncated lognormal and the uniform; two more were asked for.
- **About 14:05.** The two suggested laws are added: a finite discrete law whose points are the model, not a quadrature, and a
  mixture of normals in logs with optionally truncated components. The uniform is in levels, parameterized by its half-width.
  The owner raised Lorenz curves for the distribution statistics and asked for proposals on regularity and on quantities a
  member does not define.
- **Afternoon.** A user's own law may be given as a table (adopted at once) and, later, as a formula or as code; the two
  reserved forms are mocked up with their candidate choices noted. The guard hook is turned on. HARK pull request #1855 is
  opened and marked draft.
