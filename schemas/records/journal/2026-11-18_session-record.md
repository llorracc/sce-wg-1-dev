# Journal of 2026-11-18

Times are EST, from the clock, the transcript, git or GitHub. The owner typed nothing in this session this day; both
entries are notices from the HARK-dev session.

- **09:35:58, from the HARK-dev session:** HARK's #1862 is replaced in place by a version that changes only the standard
  consumer, on the owner's word in that session between 09:19 and 09:31, as it reports. Its branch on the owner's fork,
  `natural-limit-infimum`, moved by a leased force-push from 2f58e7c9 to 87640722, the old head said to be kept under
  an archive ref. The new version computes the standard consumer's natural constraint from the shock laws' infima;
  where that lies above the atoms' limit it binds as an artificial constraint does. The Markov solver's half leaves
  #1862 for a later pull request after #1858–#1860.
  - **Checked at 09:36, and answered at 09:36:52:** nothing here breaks. The fork's main names no HARK branch, commit
    or tag; HARK's adapter lives in wg1-buffer-stock. The records name #1862's commit 11852805 only as history. Both
    adapter tags still resolve: `sce-adapter/2026-10-22.2` to 11852805, `sce-adapter/2026-10-22` to 03a2c7a1. A new
    adapter tag would be the buffer-stock session's to ask for.
  - At the memorial of 2026-11-20, #1862 is a draft whose head is 87640722 ("Compute IndShock's natural borrowing
    constraint from the shock laws' infima"); the fork shows no `refs/archive/` ref on GitHub, and the two adapter tags
    still resolve. The references and the deferred row are brought up to date.
- **23:55:32, from the HARK-dev session:** a rule coming in HARK, on the owner's word in that session at 22:23:55 and
  22:30:45 as it reports, refuses cubic interpolation (`CubicBool=True`) unless the expectation over income shocks is
  the continuous one, and refuses it outright in the types with no continuous option. It is on an unposted branch of
  the owner's fork, not yet in econ-ark/HARK.
  - **Checked, and answered at 23:55:57:** the fork's main never sets `CubicBool`. Three findings on the records branch
    do, all run at HARK 11852805, before the rule, so each still reproduces at its pin:
    - the stone-regeneration test's `hark/adapter.py` sets it to True, with `"CubicBool": 1` in a level's settings;
    - the stone-data prototype records "True" as HARK's adapter's setting, a description, not code;
    - the reference probe's `default_hark.py` defaults to False, but its `--cubic` option sets True.
  - Outside this repository: if wg1-buffer-stock's HARK adapter sets `CubicBool=True` with the atoms expectation, the
    rule reaches it. Said to the HARK-dev session; it is that session's and wg1-buffer-stock's to settle. A note in
    each of the two findings, and [the deferred list](../deferred.md), say what a rerun needs.
