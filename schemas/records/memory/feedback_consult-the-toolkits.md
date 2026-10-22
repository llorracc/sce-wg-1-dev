---
name: feedback_consult-the-toolkits
description: "What a results file carries, or a toolkit must compute, is put to the toolkits' sessions (HARK, HAFiscal) for their views before a change is drafted; one session's recommendation and the owner's quick yes are not that consultation"
metadata:
  type: feedback
---

On 2026-10-20 the HAFiscal-Latest session found that the quantile at probability 1 in its results files moved with the
Python and numpy versions while the solution did not. It recommended dropping that quantile from the results schema and put
the question to the owner, who agreed. This session drafted the change as a draft pull request the same evening, consulting
no one. The owner then said that the question belonged more properly to HARK and HAFiscal, and asked whether their sessions
had been consulted. They had not, so both were asked, with the alternatives.

**Why:** the schema is the working group's, but whether a quantity can be reported reliably is a fact about the toolkits that
compute it. The toolkits' sessions know their representations; a change drafted on one session's word alone carries that
session's view of every other toolkit.

**How to apply:** before drafting a change to what a results file carries, or to what a toolkit must compute, ask the HARK
session and the HAFiscal session for their views. Give them the finding, the alternatives and specific questions, and
report their answers to the owner. A draft already made stays unmerged until they have answered. Name the sessions not
consulted, such as another toolkit's, when that applies. See [[feedback_iterate-and-propose]].
