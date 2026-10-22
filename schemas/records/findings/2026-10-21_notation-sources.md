# Econ-ark's notation sources and the schemas

Found on 2026-10-21, while harmonizing the schemas' notation with econ-ark's.

**The three sources.**
- **The registry**, `@resources/notation/notation.yml` in econ-ark-tools. Each entry is named for its object, not its letter,
  and records its ruling, declared dialects and the clashes checked; generated outputs, a sync test and a lint follow
  from it, and a ruling is a pull request. Its master was at version 0.2.0 until 14:52 that day, when pull requests #39
  to #44 merged; #38 followed at 16:42, making it version 1.0.0, with 68 rows.
- **`econark-shortcuts.sty`**, in the same repository: 395 macro definitions, the ones most papers load. Where both
  are loaded, the registry's macros give way, since they are `\providecommand`.
- **NARK**, econ-ark's naming conventions: a document, with tables of Roman letters, factors and rates, and parameters.
  Its `econark.sty` only loads the shortcuts.

**The schemas against registry 1.0.0.**
- **Agreeing already:** 𝒢 for the growth factor; ξ the transitory shock with the zero-income event included; θ the
  employed shock; ℘ the probability of that event, which the schemas generalize to an income ξ_U ≥ 0 while unemployed; a
  bold capital thorn for the patience factors.
- **Fixed in #7:** the two targets, which the schemas had the other way round; Γ_t for the Markov family's growth factor
  in a quarter, since Γ is the registry's dialect for the factor itself; μ for the income while unemployed, which the
  registry gives to log excess resources.
- **Not yet decided:**
  - κ in the schemas' natural limit, κ = `ψ_min` 𝒢/R, where the registry's κ is the MPC;
  - Þ̄ = min(Þ, R), a coinage of the schemas, where the registry's bar marks an upper bound;
  - registry rows for the schemas' own symbols: θ, ξ_U, the minima, the two limits, ℒ and `p_worst`;
  - a plain-text field beside the registry's `unicode`, which writes κ's and h's minima with the combining underline.

**Free letters for the income while unemployed.** Every lowercase Greek letter and variant was checked against the
shortcuts' macros, the registry's rows, the papers' sources and the schemas:
- **Least claimed:** ι, ϖ and ℵ, each free of the shared macros and the registry, with at most a local use in a paper's
  proof or appendix. ι has a mnemonic, Greek *i* for income, but is easily misread; ℵ follows NARK's use of Hebrew
  letters (ℶ, ℷ, ℸ).
- **Next:** η, which the registry uses subscripted for two remainders, and economics for elasticities.
- **Ruled out:** the letters the shortcuts or the registry claim; ε and λ, heavily used in proofs, and λ the schemas'
  dominant eigenvalue; υ, ϱ, ο and ϑ, which read as v, ρ, o and θ; uppercase Greek, which NARK keeps for aggregates;
  and every Roman letter, which NARK assigns or prohibits.

The owner chose ξ_U, which takes no letter (see the rulings).

**`\IncUnemp`.** The shortcuts defined it as μ. Its expansion is now `\xi_{\mathrm{U}}`, committed locally in
econ-ark-tools on the owner's word, and drawn correctly by pdflatex and KaTeX. HARK's parameter `IncUnemp` keeps its name.
No SolvingMicroDSOPs document writes the macro, so nothing there changes.
