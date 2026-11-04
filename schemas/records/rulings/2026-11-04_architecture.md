# Rulings of 2026-11-04 on the architecture

The owner's decisions, in substance and by time (EST). His words are kept outside this public repository. The
purpose rulings of the same day are in [their own file](2026-11-04_purpose.md).

- **Before 13:37:35, the architecture put forward.** The owner's sense: one repository per canonical model, holding the
  true model's definitions and, for each toolkit it tests, performing the test by spinning up a Docker container built
  from a Dockerfile the repository holds for that toolkit. He asks for help thinking it through. The reply (recorded in
  the journal) agrees with the core and separates the model, the toolkit's image and the adapter with its stone, adds
  a shared core and a container contract, names the limits, and puts seven decisions.
- **Between 13:37:35 and 14:06:58, the seven decisions answered.**
  1. **The unit.** The buffer-stock model is the canonical model, with its scenarios as its families. All toy-hafiscal
     work moves back to the HAFiscal-Latest repository until it is ready, with the session there consulted on how to
     do it. Separately, the regular default ConsIndShock solution and the Markov version with nonpersistent
     unemployment are to be tested as separate standalone modes of solution; he asks whether infrastructure is needed
     to keep track of solution modes. The reply proposes one, small: a mode as its own registry entry and in the
     results file's identity, a schema change put before it is made.
  2. **The adapters' home.** The model repository, as recommended, with the adapters responsible for defining and
     pinning the environments: the Dockerfile and the lock files live with the adapter.
  3. **The images' home.** As proposed: in the model repository while there is one model, a working-group images
     repository when the second appears, digests pinned throughout.
  4. **No repository split yet.**
  5. **Levels.** He asks whether "the toy levels" meant a fourth level beyond the three. The reply: no; the coarse end
     of the three, run in continuous integration.
  6. **The no-timings rule revoked.** He rules against the no-timings rule of 2026-10-21 (08:27 and 08:32). Run times
     may be recorded. Consequences: the run registry and the harness's manifest record durations, each with the
     machine, the thread count and the environment's image digest beside it; the memory
     [`feedback_no-timings`](../memory/feedback_no-timings.md) marked superseded with the reversal; the documents that
     stated the rule revised. Whether a results file carries its wall time again, dropped in the fork's pull request
     #5, is a schema question, proposed before changed.
  7. **Docker installed on jhu-dell**, on his word.
- **Between 14:21:36 and 14:24:51, the toy-hafiscal boundary.** Taking the recommendations on all five decisions put to
  him after the HAFiscal-Latest session's answer: (1) the Jacobian interface stays in the fork as buffer-stock
  infrastructure, its document, schema key and checker module, with the three toy-hafiscal passages edited, the
  schema description among them; (2) the member `iid-ui-artificial` moves, with its two tests, the toy member staying
  for the two-modes test; (3) the model document's toy-hafiscal section moves; (4) the results document's
  permanent-income section stays, its Lorenz-targets sentence and the links to the finding edited; (5) a plain
  removal commit, the unpushed history not rewritten. What stays open: "ready" on the HAFiscal side waits on three
  decisions he types there (the estimation's go, the emitter's move to the new schema, the continuous method for the
  reference), and the member alone may come back first on his word.
- **Before 15:12:59, the REMARK plan adopted.** The owner adopts the idea of adapting the REMARK framework to these
  purposes ([`schemas/registry.md`](../../registry.md), now ADOPTED) and has opened a session in the local clone of
  econ-ark/REMARK, `jd_REMARK_integrate-with-WG1`, for the REMARK side of the work; he asks whether this session can
  see it. It can: one session there, in `/home/shared/github/econ-ark/REMARK`, idle. The five decisions the proposal
  lists stay open; the REMARK session is briefed with the proposal's REMARK-side items as information, its work on
  the owner's word in its own session.
- **Between 15:30:24 and 15:36:21, the organizer's image and the REMARK pull requests.** Taking the recommendations on
  both: the organizer's image is defined in `binder/`, the root `Dockerfile` the standard requires kept identical to
  it by a test; and the pull requests to econ-ark/REMARK start now, in the REMARK session's order (non-interactive
  execution first, as a bug fix; the tool packaged; the execution records in the drafted format; subdirectory builds;
  the entry point with arguments last). The REMARK session is told with his words and their time; since
  econ-ark/REMARK is public, a relay lets it commit but not push or open the pull requests, which need his word in
  that session. The fork's side begins: the environments moved beside their adapters, the Dockerfiles, the container
  executor, the records.
- **Between 16:17:05 and 16:24:22, the license, the session and the push.** Three answers: wg1-buffer-stock takes the
  same license as HARK, which is Apache License 2.0 (econ-ark/HARK's license as GitHub reports it); the owner has
  opened a session of its own in that repository, `jd_wg1-buffer-stock`, so this session writes there no more and
  hands the work over; and the fork's branch `buffer-stock-ontology` is pushed, which it was at 16:24:22, the branch
  now public with the day's commit 5c6961b.
- **Between 16:37:15 and 16:57:06, the series to upstream.** Taking the recommendations of [`upstreaming.md`](../../upstreaming.md),
  now ADOPTED: the framework goes to econ-ark/sce-wg-1 in ordered pull requests and the buffer-stock model stays in
  wg1-buffer-stock, which vendors the core until the core is a package; the records stay with the model and the
  fork; the apparatus document goes at upstream's root; the order as proposed, with the apparatus and the ontology of
  probability distributions cut now, each from upstream's main on its own branch of the fork.
