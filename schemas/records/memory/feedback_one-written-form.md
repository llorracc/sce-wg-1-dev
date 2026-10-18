---
name: feedback_one-written-form
description: "A model has one spelling in a parameter file, since the file's hash is the model's identity; the rules that enforce it"
metadata:
  type: feedback
---

A parameter file's hash identifies its model, so two files that describe one model must hash alike. The rules that follow,
adopted 2026-10-17 and 2026-10-18: each shock law has one written form (no infinities, no silent normalization, a tabulated
law with no exactly collinear point); the hash is taken over the parsed numbers, so `0.10` and `0.1` agree; the types are
listed in increasing β with no repeat; with an unemployment probability of zero the unemployment income is zero; the
artificial borrowing constraint is written no lower than the natural one, since a looser one never binds.

**How to apply:** when a new parameter is added, ask whether two values of it can describe one model; if so, fix one spelling.
