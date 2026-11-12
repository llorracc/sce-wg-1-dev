---
name: feedback_stamps-from-the-clock
description: "Every time label, in the records and in messages to other sessions, comes from the clock or the transcript's own stamp; a time is never inferred"
metadata:
  type: feedback
---

Take every time label from the clock (`date`) or from the transcript's own stamp of the event: the owner's messages by
their entries' timestamps, an event by the moment it was seen. This holds in messages to other sessions as much as in the
journal, since they record what they are told.

**Why:** on 2026-11-01 this session wrote "16:41" for a request typed at 16:37:49 into four sessions' briefs, and three
journal stamps ahead of the clock; HARK-dev caught the first, and both HARK sessions had to correct their records. The
same lapse was corrected earlier that day. On 2026-11-05 it happened twice more, both in messages to other sessions:
"about 13:20" for a request typed at 13:46:09, and "15:4x" for a message's own send time, written before the message
was sent; the HARK session caught the second.

**How to apply:** before writing a time, read it: the transcript's stamp for the owner's words, `date` for the present.
Write "by HH:MM" with a time already read when an event's own time is not known. A message's own send time is not
known while it is being written: say "now" or "in this message", and read the stamp afterwards for the records.
On 2026-11-11 and 2026-11-12 it happened five more times, each in the journal and each corrected by amending an
unpushed commit: a "by HH:MM" written a minute or more ahead of the clock, or behind it, because the entry was composed
before the clock was read. So read the clock in the same command that writes the entry, before the text is fixed, and
take the stamp from that reading; a stamp remembered from an earlier command is an inference.
Related: [[project_state]].
