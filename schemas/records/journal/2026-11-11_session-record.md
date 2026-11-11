# Journal of 2026-11-11

Times are EST, from the clock, the transcript or git.

- **11:50:45, in the model repository's session; reported here before 12:00.** On the owner's word there that the
  repository work with the updated bellman-dev, its QuantEcon environment pins bellman-dev's `930199a`, in its working
  tree and not yet committed. As that session reports it: the package at that commit is the same tree as at
  bellman-dev's main of today; the adapter's fallback to the arrival line's full address is deleted, bellman-dev
  having corrected its record on the evening of 2026-11-09; the adapter's 42 tests pass with none expected to fail; a
  run through the harness reproduces the results files of 2026-11-06 in every number; the stage files and the two
  methods additions are unchanged. Nothing asked of this session.
- **12:00, checked here, read-only.** The commits are as reported, and the package's tree at `930199a` is that of
  bellman-dev's main, 175 commits after the morning of 2026-11-09. Built from that tree into a scratch environment, the
  package elaborates the fork's two stage files with views, dossiers and places identical to those of
  [the review of 2026-11-09](2026-11-09_session-record.md); the distribution families' module is unchanged and no
  concept page was added or removed. Nothing in the fork needs revision beyond what is already with the owner: the
  stone convention's method file, one question with the model repository's plan, and the ontology's statement that
  Bellman's documentation is not public.
- **13:02, a consultation from the owner's bellman-dev session on another of his machines; answered by 13:04.** At
  his request there, that session asks how the working group should keep track of which toolkit replicates which
  model, having proposed three designs for a registry of its own repositories: a catalog of pointers with one
  command that reads every unit and writes a status table, one working repository that exports its units, or a
  template with a pinned package and a query by topic; and whether REMARK, with changes to its standard, is the
  better base. It comes over Remote Control, so it cannot be checked as his words; it asks for no change, and none
  was made. Answered from the fork's documents and the two model repositories' files, read-only:
  - **What there is.** Each model repository keeps its toolkit registry file, its experiments and its run registry
    of execution and build records in the core's format, which already hold the model's commit, the toolkit with
    its mode, version and commit, the adapter's and environment's hashes, the verdict and the comparison's largest
    distance with the reference's error. Two models, both private. Missing: a list of models as data, a list of
    toolkits across models, a designation of the run of record for a model and toolkit, the core upstream (the
    working group's pull requests #14 to #20 open that hour), and a template for a new model repository.
  - **The unit** is the model repository, one row each; a replication, by model, toolkit and mode, is a cell
    derived from that repository's two files and never kept by hand.
  - **The catalog of pointers fits**, as [the architecture rulings](../rulings/2026-11-04_architecture.md) and
    [the registry design](../../registry.md) already assume, with a pinned commit or tag that the reader honors,
    a command that reads both levels and validates the records without running anything, and entries that may be
    private. One working repository contradicts the ruling of one repository per model. The template and pinned
    package of the third are right, the core being that package, but a query by topic pins nothing.
  - **REMARK is the adopted base for the standard** and need not understand a comparison, since a model's
    reproduction script exits on the verdicts; what it lacks is what the registry design listed on 2026-11-04,
    with a site that honors a tag and a state before publication.
  - **To avoid:** a status table edited by hand, floating branches, any score, rank or bare timing, silent skips,
    a second record format, a copy of the core, and a model's numbers in a public catalog before he publishes them.
- **A second round from that session, answered by 13:05.** It reports that the three sessions it asked, this one, the
  model repository's and the REMARK session, converge: the catalog of pointers, built with REMARK's standard and
  tools; the model repository as the unit; a replication a cell derived from the registry file and the committed
  records, nothing kept by hand and nothing run again; the catalog a separate private root, a model entering
  REMARK's public catalog when the owner publishes it. Three points put for objection, answered so:
  - **The pointer** holds the remote, the title and a pin and nothing else: agreed, the pin resolving to a commit,
    never a branch, and the table printing the commit read.
  - **The reader** of a comparison supplied by the core, found by a kind the unit declares in its REMARK metadata
    file: agreed, with two notes. REMARK's standard requires that file only from its second tier, so the kind needs
    a home at the first. And a reader in the core is a change to the core, to be proposed to the owner before it is
    made ([the deferred items](../deferred.md)); it must read records written under earlier commits of the core.
  - **The run of record**, named by the model repository in one committed file: amended. A run is a folder for one
    experiment holding one record for each toolkit, member and level, so the file maps an experiment, a toolkit and
    a mode to a run folder, not a cell to one entry; the run is of a clean tree and reproduced, as [the execution
    records' document](https://github.com/llorracc/sce-wg-1-dev/blob/7a4889f6fc69f266b5892f9de59cf3ad13aa30a1/schemas/execution-record.md)
    requires of a finding; and the reader says when a run's experiment hash is no longer the current one, not
    only when a newer run exists.
  Nothing changed here. The design is that session's to put to the owner.
- **That session's closing note, read at 13:07.** What it reports to the owner, nothing decided until he rules and
  nothing asked: the catalog design as agreed, with this session's amendment taken, one committed file in the model
  repository mapping an experiment, a toolkit and a mode to the run folder that is its run of record. From the
  other two sessions it took that the execution record's schema is REMARK's once REMARK's third update ships it, the
  core keeping the working group's extensions, which is what [the registry design](../../registry.md) adopted and
  not yet the state: the schema's file is in the core's package today; that REMARK's tool pins by tag alone while
  the buffer-stock repository can be pinned only by commit; and that a toolkit which cannot be built publicly needs
  a stated status. His decisions, as it lists them: pushing REMARK's two committed branches; a sixth update to
  REMARK, the status table with a reader chosen by the unit's kind; commits or tags as pins; where the private
  catalog is kept; whether and where a unit declares its kind; and the runs of record, once the toolkits have run
  again at their present pins.
- **13:23 to 13:26, the REMARK session's report and this session's check of it.** That session reports REMARK's
  build and execute functions settled, each writing an execution record, on a local branch of its clone, unpushed and
  untagged, with the functions' signatures; its schema is the core's fourth draft under REMARK's own identifier; three
  findings that touch the core's runner; and one proposed change of rule, that a record need not name an image when
  the build failed. Checked against the core on the fork's main, read-only:
  - **The schemas agree.** REMARK's file and the core's differ in six places, the identifier, the title and four
    descriptions; no field or rule differs. The fork's registry schema refers to the core's by its identifier, so it
    will refer to REMARK's once that is merged and tagged, a schema change to put to the owner then.
  - **The rule on the image, amended.** The schema states it twice, for a build and for an execution. A failed build
    has no image; an execution always has the one it ran in. So the change belongs to the build alone: an image
    required when the runtime is a container's and the build's exit code is zero. Every record valid today stays
    valid. The core writes no record for a failed build today, stopping with the log's path, so nothing depends on
    the rule. Told to that session; the core's copy changes on the owner's word only.
  - **The memory kill the runtime does not report.** That session measured the runtime's flag false after one of
    forty kills at a memory cap. The core's runner reads the same flag once, as the container exits, and on a miss
    records a kill by signal with the exit code, never an exit of the run's own: the record is true and less
    specific. The records' document says the runtime reports the memory cap; it should say that a kill under a
    memory cap may be an unreported one.
  - **The stale image** that REMARK's builder would reuse does not reach the core, whose runner builds from the
    environment's directory alone, names the image for that directory's hash, records its identifier and runs each
    job by it.
  - **A latent fault in the core's hash of an environment**, found by comparing with REMARK's: [the
    defects](../defects.md). No recorded hash is affected.
  - **Two smaller differences:** REMARK records a signal by its name and the core by its number, where one format
    should have one spelling, the name; and REMARK's execution mounts the checkout writable, where the container
    contract here mounts the source read-only and the job's folder apart with no network, so the core keeps its own
    run until REMARK's function can do the same.
  Nothing changed on the fork's main. The changes to the core and to the rule are [deferred](../deferred.md) to the
  owner's word.
- **13:28, the model repository merged to its main; reported here and checked by 13:31.** On the owner's word typed
  there at 13:26:15, that repository's working branch is merged into its main and pushed; the pin at bellman-dev's
  newer commit and a change to the artificial stage file, which now states the artificial limit above a derived
  natural one, are on it. This fork's records name that branch nowhere. The fork's own copies of the two stage
  files, on this records branch, are the earlier ones and now differ from the model repository's, by two lines and
  by twelve: the checks made here on 2026-11-09 and this noon hold for the copies, and the model repository's own
  checks for the hub.
- **The owner's rulings of 12:13:41 in that session, which settle this session's open question.** Found by the
  relay check where he gave them, by menu, one of them in his own words: the schema's method targets are renamed
  to Bellman's places; a stone's method file is to be a Bellman methods file, with the additions for HARK and dolo
  written and bound first and what does not bind reported before anything is committed, the convention's text
  amended after; and every toolkit's record of its methods in a run becomes a methods file in Bellman's form in
  place of the YAML one. So the first of [the proposals of 2026-11-09](2026-11-09_session-record.md) is answered and
  is not put to him again. Two consequences here, told to that session:
  - **Two texts of the convention.** The model repository's main still holds the draft of October; the adopted
    text is the fork's main, revised on 2026-11-07. The amendment belongs in the fork's, drafted from that
    session's report of what binds, and committed and pushed on the owner's word here, the fork being public and a
    menu answer not a typed word.
  - **The core records a run's methods file by one name.** The runner lists a job's outputs as the results file,
    `methods.yaml` and the settings file, and writes the methods hash into the record only when that file is there;
    the registry schema does not require the hash. A job that writes only a methods file in the new form therefore
    yields a valid record with no methods hash and no methods file among its outputs, and nothing fails. The change
    to the core, the runner taking the new file as it takes the YAML one, is proposed and not made
    ([the deferred items](../deferred.md)).
- **13:29, the REMARK session's answer.** It takes the amendment, the rule on the image relaxed for a build alone,
  and leaves REMARK's copy unchanged until the owner rules, recommending the change to him. On a further local
  branch, unpushed, REMARK's execution now takes a read-only mount of the source, further mounts, a scratch
  directory, variables and the invoking user, with a test in the shape of this project's container contract, and
  builds an environment kept in a subdirectory, naming the image for that directory's hash. What still keeps the
  core's jobs from REMARK's execution is that it runs a shell script where the contract runs an adapter, the fifth of
  the updates. It reports that the thirty records committed in the model repository validate against REMARK's
  schema as they are.
- **13:56, REMARK's four branches posted; reported here and checked on GitHub at 13:59.** On the owner's word typed
  in the REMARK session, the four branches are stacked pull requests on econ-ark/REMARK, all open:
  [#196](https://github.com/econ-ark/REMARK/pull/196), execution in a container without a terminal;
  [#197](https://github.com/econ-ark/REMARK/pull/197), the tool as an importable package with tests;
  [#198](https://github.com/econ-ark/REMARK/pull/198), an execution record for every build and execution, with the
  schema that is the core's fourth draft; and [#199](https://github.com/econ-ark/REMARK/pull/199), environments kept
  in subdirectories and the options a runner needs. The checks pass on the last three. Nothing is merged or tagged,
  so the core has no tag to pin and keeps its own records and run. The rule on a failed build's image is unchanged
  in both copies, waiting on his word.
- **About 14:21, the owner's decisions on the registry, as his bellman-dev session on another machine reports them.**
  Given there between 14:08 and 14:19, some typed and some by menu; relayed over Remote Control, so they could not be
  checked from this machine when they came and approve nothing here, as that session says itself; he confirmed them
  at 14:22:34 in the REMARK session on this machine (below). In substance: one catalog,
  REMARK's public one, an entry carrying a mark that its repository is private, the existence of a private REMARK
  being no secret, which replaces the separate private catalog the three sessions had converged on at 13:05; the
  website shows nothing of an entry marked private until it is public; the pin stays a tag, a model repository
  being tagged before it is listed; a sixth update to REMARK is approved, the status table whose reader is chosen
  by the unit's kind; and a paper's repository may begin under his account and pass to one of its authors, entering
  the catalog once the authors agree. Read against the fork's main: nothing there contradicts them, the apparatus
  document already saying that REMARK's tool pulls a cataloged repository at its tag and that the catalog is
  REMARK's. What they would change here, on his word in this session: the reader in the core for that status table,
  to be written against REMARK's interface for readers once there is one ([the deferred items](../deferred.md)); and
  one step of [the upstreaming plan](../../upstreaming.md), where a model's being public and its being cataloged
  become two events. Nothing changed.
- **14:30 to 14:33, the status table's frame and the reader it expects.** The REMARK session reports the sixth
  update built on two local branches, unpushed: a command that pulls every entry of the catalog at its pin, runs
  nothing, and writes a table with the commit read, the newest commit and a reader's result; a unit declaring its
  kind in the front matter of its REMARK metadata file; a reader found by the kind's name among the entry points
  installed packages offer, a function of the checkout and the entry that returns a one-line summary and, if it
  likes, a table of its own and data; a private entry left out unless asked for, its row then saying only that it
  exists. It says the owner confirmed the decisions relayed at 14:21 in its window; found there, typed at 14:22:34,
  so they are his. Read on that branch and against the two model repositories:
  - **The interface fits the core.** The core's model loader already reads a checkout's registry file and finds its
    run registry, and a reader needs nothing of REMARK's package. Both model repositories already hold the metadata
    file, so the kind has a home; neither has a tag yet, which the pin now requires before listing.
  - **The records name two drafts of the registry schema** in the buffer-stock repository, ten under the fourth and
    twenty under the sixth, and its build records carry no version of the core: a reader says which schema each run
    was checked against and reports what it cannot check as unchecked.
  - **One note sent back:** a run that reads private entries writes their own tables, verdicts and distances
    included, into the same two files as the public rows; a line saying so would keep such a file from being
    published by habit, as his ruling that the site show nothing of a private entry requires.
  The reader in the core is proposed to the owner in this session, with the kind's name his to choose, and not
  written ([the deferred items](../deferred.md)).
- **Reported at 14:35 and checked on GitHub then.** On the owner's word typed in the REMARK session, its two further
  branches are pull requests on econ-ark/REMARK, stacked on the four: [#200](https://github.com/econ-ark/REMARK/pull/200),
  catalog entries marked private, and [#201](https://github.com/econ-ark/REMARK/pull/201), the status table. Their
  checks pass; #196 to #199 are approved and unmerged, these two not yet approved. This session's note is adopted in
  #201: a run that read a private entry says so at the top of the table, in the data and on the terminal.
- **15:03:31, the owner's ruling on the method files revised, in the model repository's session; reported here and
  checked by 15:20.** Typed there, and found by the relay check: what a Bellman methods file cannot hold stays in
  the YAML file, and whatever it can hold leaves the YAML file. This replaces his answer of 12:13:41 that the one
  replaces the other: each toolkit has both, and each part is stated in exactly one. As that session reports, and
  as its working tree shows, uncommitted: a methods addition for each toolkit and family, six files beside the
  adapters, each binding under Bellman's package at its pin; the solution method at the policy builder, the rule's
  representation at its evaluate place, the expectation, the histogram at the arrival builder, where the entry of
  2026-11-09 named another builder by inference; a place whose method Bellman has no word for, HARK's cubic rule for
  one, carrying its handler alone; no grid typed and no setting declared, the settings staying the toolkit's own in
  its ladder. A run's YAML record keeps the rows an addition cannot hold, the population's distribution, the
  diagnostics' expectation and a value a toolkit does not compute, with a pointer to the addition and its hash.
  Two consequences here:
  - **The core need not change for the methods file.** The YAML record is still written, listed among a job's
    outputs and hashed, and its hash now moves with the addition's. The proposal of 13:31 to the owner is
    withdrawn; listing the addition among the outputs would be a refinement.
  - **The convention's amendment has what it waited for.** On the fork's main it touches the second desideratum of
    the stone convention and its workflow line, one word of the apparatus document, and three entries of the
    vocabulary: places for targets, Bellman's method words for tags, and a stone's method file as the pair, the
    addition for what Bellman's language states and the YAML rows for the rest. Proposed to the owner, to be drafted
    on a branch and merged and pushed on his word here.
- **16:05, REMARK's six pull requests merged; reported here and checked on GitHub at 16:07.** On the owner's word in
  the REMARK session, #196 to #201 are merged into econ-ark/REMARK's main, whose tree is the tested one. Main now
  holds the execution-record schema, with no rule different from the core's fourth draft, compared again here; the
  build and the execution that write records; environments in subdirectories; the mark for a private entry; and the
  status table that finds a reader by a unit's kind. Its package is at version 0.2.0 and no release is tagged, so
  there is still nothing for the core to pin: the registry schema's reference to REMARK's schema and the core's use
  of REMARK's records functions wait on a tag and on the owner's word here. Open with him as before: the rule on a
  failed build's image, in both copies or neither, and the name of the working group's kind.

**State at the end of the entry.** As at the end of the journal of 2026-11-09: the fork's main at 7a4889f, pushed; this
records branch not pushed, held on the HAFiscal session's open question; of the two questions above, the stone convention's answered by the owner in the model repository's session, revised by him at 15:03:31, its amendment on the fork's main waiting on his word here, the ontology's statement still with him; the registry for replications in design in his bellman-dev session on another machine, with this session's answer; REMARK's six updates merged into its main and not yet tagged, the reader for its status table proposed to the owner here; four changes to the core and one to the record schema's rule on the image proposed, none made.
