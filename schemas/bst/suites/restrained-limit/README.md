# The restrained-limit suite

BST's experiment "The Liquidity Constrained Solution as a Limit", for every toolkit's solution of the buffer-stock
families ([`../../model.md`](../../model.md), "The restrained-limit suite").

- **The members:**
  - [`bst-p-zero-0.005`](../../natural/members/bst-p-zero-0.005.yaml),
    [`bst-p-zero-0.0005`](../../natural/members/bst-p-zero-0.0005.yaml) and
    [`bst-p-zero-0.00005`](../../natural/members/bst-p-zero-0.00005.yaml), in `bst-natural/1`;
  - [`bst-restrained`](../../artificial/members/bst-restrained.yaml), in `bst-artificial/1`.
- **The request files,** `<member>.request.yaml`: one per member, with the same comparison points in m, so that the four
  rules can be read side by side. [`make_requests.py`](make_requests.py) writes them.
- **The comparison,** [`compare.py`](compare.py): from a toolkit's results files, laid out as
  `<member>/level-<n>/results.json`, it writes the tables and the figure. It needs no solution of its own.

A toolkit runs its adapter on each member with the member's request file, at each precision level it offers, checks
each results file with `checker/check.py --verify-results`, and runs `compare.py` on the folder.

HARK's run of 2026-11-01 is in
[`../../../records/findings/2026-11-01_restrained-limit-suite-hark/`](../../../records/findings/2026-11-01_restrained-limit-suite-hark/README.md).
