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

**State at the end of the entry.** As at the end of the journal of 2026-11-09: the fork's main at 7a4889f, pushed; this
records branch not pushed, held on the HAFiscal session's open question; the two questions above with the owner; the registry for replications in design in his bellman-dev session on another machine, with this session's answer.
