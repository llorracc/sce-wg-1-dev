---
name: feedback_no-timings
description: "SUPERSEDED 2026-11-04: the owner ruled against the no-timings rule; a run's time may be recorded, with the machine, the threads and the environment beside it. The rule of 2026-10-21 is kept below for the record"
metadata:
  type: feedback
---

**Superseded.** Between 13:37:35 and 14:06:58 on 2026-11-04 the owner ruled against this rule, among the container
architecture's decisions ([the rulings](../rulings/2026-11-04_architecture.md)). A run's time may now be recorded: in
the run registry he asked for that morning, with the machine, the thread count and the environment's image digest
beside it, without which a time means nothing, and in the harness's manifest. The results schema dropped its wall time
in the fork's pull request #5; whether it returns there is a schema question, proposed before changed. The community
library's practice and the HAFiscal-Latest session's are their own.

**How to apply now:** record times where the registry and the manifest provide for them, each with its machine, threads
and environment. A document that still states the old rule is stale; correct it when met. A time set beside another
toolkit's still reads as a ranking, so a published comparison says what machine and settings each time came from.

**The rule as it stood, from 2026-10-21 to 2026-11-04, kept for the record.** No wall time, speed or other timing of a
toolkit's run went into this repository or a pull request's description. The community library of baseline models
publishes no timings and no ranking of toolkits, and the HAFiscal-Latest session publishes none of its runs'. The
memorial of 2026-10-21 broke the rule before it was known here; see the defects. Its reasons: timings set beside each
other read as a ranking of toolkits, which the working group declines to publish; they measure the machine and the
moment as much as the method; and a toolkit's session owns its runs' data. Under it a run was reported by what it
produced and how it ended, never by how long it took, and timings were scanned for before a commit went out.
