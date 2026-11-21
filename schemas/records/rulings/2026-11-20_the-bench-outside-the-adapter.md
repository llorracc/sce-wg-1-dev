# Rulings of the evening of 2026-11-20: the bench outside the adapter, and settings as suggestions

The owner's decisions in this session on the evening of 2026-11-20, in substance; his words are kept on the machine,
outside this repository. What they led to is in [the journal](../journal/2026-11-20_session-record.md), and the work
in [the plan](../plans/2026-11-20_bench-outside-the-adapter.md).

- **18:11:45, the tag v0.1.0: typed, then interrupted.** He interrupted at 18:11:50, before anything was run; the tag
  was not made. The recommendation of 2026-11-17 stands, waiting on his word ([the defects](../defects.md)).
- **18:19:48, the bench outside the adapter: adopted.** Of the comparator survey's suggestions
  ([the finding](../findings/2026-11-20_comparator-projects/README.md), "The bench as a step"), the one that moves the
  organizer's measuring code out of the adapter, to a step that measures each toolkit's exported solution outside the
  toolkit's container. He had taken it to be the practice already. He asked for a concrete plan to bring the fork and
  both model repositories to it, and proposed that the harness may make suggestions to a toolkit about its grid, its
  number of points, spacing and bounds, without requiring the toolkit to take them, since the outcome is what is
  judged.
- **18:31:06, what the solve is.** He asked whether the solve is the toolkit's alone. Answered toolkit by toolkit from
  the model repositories' adapters: in every case the iteration is the toolkit's own code, but in the buffer-stock
  model the shock nodes, and in effect the grid, are the harness's, and for two toolkits part of what is reported as
  the toolkit's rule is the adapter's reading of the toolkit's internals.
- **18:36:08, the line between the toolkit's solve and the adapter's part: agreed.** An adapter translates the member
  into the toolkit's terms, calls the toolkit, and translates the answer back. It supplies none of the toolkit's
  numerical choices: nodes and grids reach a toolkit as suggestions it may take, adapt or decline, and only the
  outcome is judged. Where an adapter reads the toolkit's internals rather than the object the toolkit returns, the
  solution file declares it and the stone says why. The model's statement in the toolkit's language stays the
  adapter's job. He asked for a plan to implement it at once. Read here as settling:
  - **suggestions in place of inputs**, a level with no suggestions being the toolkit's own defaults;
  - **each toolkit's own representation of the laws,** the agreement check on effective members retired once the move
    has reproduced today's numbers;
  - **quantecon-egm taking the suggested grid,** no longer running HARK's adapter inside its own job. This changes the
    mechanism of his ruling of 2026-11-06 in the buffer-stock repository's records; it was put to him as a reading he
    may withdraw.
- **18:45:18, start the core.** Build the core's packages, and when that is done send the two model repositories'
  sessions their parts.
- **19:10:39, the perfect-foresight reference's driver string: kept.** The exact reference that repository's
  experiment pins by hash records the shared module that made it, which its cut renames. The string is kept, as the
  reference's provenance at its making, so that the file regenerates byte for byte and neither its hash nor the
  experiment's version changes. In the same message: commit and open the core's pull requests.
- **19:40:00, merge** the fork's #31 and #32.
- **19:42:12, yes to all four suggestions then put:**
  - the perfect-foresight session to commit its cut, repin to the merged core, and run the pilot;
  - the buffer-stock session's cut to go on;
  - the two pull requests to the working group's repository, one at a time;
  - the defect closed, and the evening recorded, at the next memorial.
- **19:44:45, memorialize.**

**What it supersedes.** The ruling of [2026-11-02](2026-11-02_harness-decisions.md) at 18:28:43, that the harness
gives a toolkit parameters and not methods or settings, is read through his proposal of 18:19:48. The harness gives
parameters, and suggests settings it never imposes. The shared nodes and grid that ruling called a departure to be
undone are undone in the plan's last package.

**What stays open:**
- the reading on quantecon-egm's grid, his to withdraw;
- whether a toolkit's own numbers (its kink, its targets, its stationary distribution) are reported beside the
  bench's: the drafts allow it, for every toolkit optionally;
- where the plans live: the core's part here, the model repositories' details kept on the machine, as practiced;
- merging the working group's #24 and taking the fork's #32 there after it;
- for the pilot: its push and whether its run becomes the run of record.
