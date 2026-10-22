---
name: feedback_no-timings
description: "Public material carries no run times or speed figures of a toolkit: not in records, findings, pull requests or documents"
metadata:
  type: feedback
---

No wall time, speed or other timing of a toolkit's run goes into this repository or a pull request's description. The
community library of baseline models publishes no timings and no ranking of toolkits, and the HAFiscal-Latest session
publishes none of its runs'. The memorial of 2026-10-21 broke the rule before it was known here; see the defects.

**Why:** timings set beside each other read as a ranking of toolkits, which the working group declines to publish; they
measure the machine and the moment as much as the method; and a toolkit's session owns its runs' data.

**How to apply:** report a run by what it produced and how it ended (verified; out of memory; no file), never by how long
it took. Scan for timings, as for private markers, before a commit or a description goes out. Whether a results file
should carry its wall time at all is a question for the toolkits and the owner, since `results.schema.json` requires it.
