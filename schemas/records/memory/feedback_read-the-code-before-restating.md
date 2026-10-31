---
name: feedback_read-the-code-before-restating
description: "Read the code a peer session's claim rests on before restating the claim, and say which object a word like 'index' names; a loose restatement reads as a claim about the mathematics"
metadata:
  type: feedback
---

On 2026-10-31 this session reported, from the HARK-dev session's reading, that in a cyclical model HARK's solver "builds
each period's solution from the next index". It had not read the function. The owner asked what that meant, and whether
the solver computes v′_t(a_t) = E_t[u′(c_{t+1}(m_{t+1}))]. Reading `solve_one_cycle` showed that it does, in every
model. The claim was about which entry of HARK's time-varying lists holds the laws of the move from t to t+1, not about
the Bellman step.

**Why:** the owner reads a statement about a solver as a statement about the model it solves. A peer's reading, restated
in looser words before the code is read, carries the peer's shorthand into a claim neither session made.

**How to apply:** before restating a peer session's account of code, read the lines it cites. Name the object a word
stands for: a list entry, a date, a period of the cycle. Record the restated claim only once it is checked. See
[[feedback_matsya-answers-are-weighed]] and [[feedback_consult-the-toolkits]].
