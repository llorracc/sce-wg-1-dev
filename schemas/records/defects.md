# Defects

Faults found in this project's own work, with their status.

- **A commit of unknown origin.** `1ca65f0`, "Add draft schemas for the buffer-stock family bst/1", at 11:37:20 EDT on
  2026-10-18, author `llorracc`, carrying this session's attribution trailer, with the seven first-version files. No command
  of this session made it; the owner was asked whether he did. **Status:** closed 2026-10-18 18:28, the owner confirming that
  he made it himself.
- **Moments cancelling to zero.** The truncated lognormal's moment of large order was computed as an exponential times a
  difference of two normal CDFs that both round to one, so it came out as zero and the tail-exponent search ran to overflow.
  **Status:** fixed 2026-10-18 17:21, every law's moments computed in log space with the complementary tails; the tail
  exponents of the members were unchanged by the fix.
- **A floor claimed to bound consumption.** `conditions.md` said that a positive unemployment income bounds consumption below
  and makes the welfare means finite; only a binding artificial constraint does. **Status:** corrected 2026-10-18 on the
  BufferStockTheory session's reading of the paper's remark.
- **Time labels by inference.** Notes after 14:21 on 2026-10-18 carried inferred times, about two and a half hours fast, until
  the bellman session could not match one. **Status:** corrected at 17:40 from file stamps and marked approximate.
- **The first convention of the HAFiscal family's worst income.** The draft stated it as the exhaustion income, which holds only
  when the employed income cannot fall below it. **Status:** corrected 2026-10-18 on the bellman session's finding.
