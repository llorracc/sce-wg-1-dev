# Journal of 2026-11-19

Times are EST, from the clock, the transcript, git or GitHub. The owner typed nothing in this session this day.

- **19:34:40, from the buffer-stock session:** a plan, `schemas/other-models.md` in wg1-buffer-stock (PROPOSED,
  uncommitted then), on whether the scheme for comparing buffer-stock solutions was built with enough attention to the
  working group's other models (Aiyagari, Krusell–Smith, a small New Keynesian model and the rest of the baseline
  library), with proposals to make wg1-buffer-stock and this repository consistent and more extensible. The owner asked
  for it in that session at 19:05:06 and asked that this session be briefed at 19:22:15, as that session reports; his
  words there approve the write-up and the brief, no change. It asked for corrections of fact about the core and a view
  of each proposal's half in the core. Its seven proposals: the solution concept a family states; statements from
  blocks; laws of processes beside the shock laws; a catalog of typed quantities; the bench as a step; one home for each
  shared thing, the tag `v0.1.0` first; and three models before a rule.
- **19:38:45, answered, nothing changed.** Read at the fork's main 4e90bb1 and the records at 72335c3.
  - **All six of its statements about the core are right.** Details added:
    - on the host the runner starts an adapter as `uv run --quiet --project <environment> --frozen python <adapter>`,
      or with the core's own interpreter when an entry has no environment; in a container, `docker run ... python
      <adapter>`;
    - a job succeeds on exit status zero and a results file; the methods and settings files are hashed into the record
      when present, not required;
    - the core parses a whole request file and checks its hash, family and member, but nothing checks its shape;
    - flattening keeps lists in order and mappings by sorted key, and skips booleans, nulls and strings, so a status
      drops out silently; two files are compared by position, nothing checking that their points are the same;
    - jobs take no other job's output;
    - between the model repositories' pin, 9fc7d27, and today's core lie #22, #23 and #25: seven files, so moving the
      pin should be held to the plan's own reproduction rule.
  - **Two additions:** the registry file's model block and toolkit entries accept closed sets of keys, so the core must
    accept a new key before a model repository writes it, and a core pinned earlier refuses a newer registry file; the
    ontology of probability distributions already defines finite Markov kernels.
  - **Rulings and deferrals that bear on it:** no repository split (2026-11-04), so a template for model repositories
    belongs in the core; the pin is a tag, a model repository tagged before it is cataloged (2026-11-11); no default
    metric, an experiment defining its own, and the two points that ruling deferred, companion quantities for a metric
    and "not compared" for a quantity behind a status (2026-11-12); the validators for request files (2026-10-18); the
    split between a toolkit's report and the bench's computation, unread (2026-11-03); the ontology's identifiers on the
    schemas' keys (2026-10-31); the stones' methods addition bound to a family's stage file (2026-11-06, 2026-11-11).
  - **Views:** the solution concept named within #14's merged wording, which already requires a definition to name the
    objects that make up its solution, rather than amending the criterion; processes a module of their own, since every
    law in the core is a positive random variable with mean one; the measure step the largest change, reaching the
    execution-record and registry schemas, REMARK's copy of the record schema and every job's fingerprint, ordered as a
    registry entry's own command, then jobs taking other jobs' output, then the measure step; a model stated in blocks
    needing a rule for which block's methods file binds where, and one hash over all its files; the reproduction of
    both model repositories run outside the public core's CI and reported.
