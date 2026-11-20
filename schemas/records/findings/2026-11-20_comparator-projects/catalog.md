# Comparator projects: the catalog, by field

The catalog of the survey of 2026-11-20 ([the finding](README.md)): fifty-five open-source projects, in eight fields,
that compare computations made by different codes, each described from its primary sources and checked against them
by a second agent. NIST's reference datasets appear in two fields. Every source is public; the entries name no part of
this project's private repositories.

Each entry gives what the project compares, the engineering decisions that matter to us, its documented lessons, what
verification found, and its sources.

### Computational economics and econometrics

**The JEDC computational suite (Den Haan, Judd, Juillard), 2008 to 2011.** *Compares* solution algorithms, each run by
its own team, on a model the organizers fixed: in round one six algorithms on an incomplete-markets model, in an economy
without aggregate uncertainty (aggregate capital held at 43, a partial-equilibrium individual problem) and in the full
model; in round two six algorithms on 30 multi-country RBC specifications. *Decisions:* a six-page task document with a
notation rule and fixed index letters; shared shock files and an initial distribution; a prescribed non-stochastic
simulation on a 0.1-step capital grid, "to ensure that differences in the simulated output is only due to differences in
the policy functions used"; in round two an organizer-written C++/GSL test bench that rebuilds each team's approximating
function from its submitted coefficients and evaluates every solution with the same random elements (Sobol points on
spheres around the steady state, Mersenne-Twister shocks), the same quadrature and the same precision. No reference
solution: Euler-equation residuals, the Den Haan-Marcet statistic and a test of the aggregate law are the only arbiters;
no pass/fail tolerance. *Lessons:* the Penal team solved a different model and said so in its abstract; Den Haan included
it and also tested it against the stated model, where it was rejected in all 20 samples. Accuracy in the
partial-equilibrium economy did "not carry over" to the full model. An R-squared above 0.9999 coexisted with inaccurate
laws of motion. The bench simulated a second-order perturbation without the pruning its authors used, because it "uses a
generic simulation routine", and participants proposed residual normalizations that lowered every error; the bench kept
the default and offered the rest as named options. The wiki and the paper disagree on the burn-in (500 against 200), and
the bench's URL now returns 404. Den Haan's own conclusion is our premise: it is "even more convincing if the results do
not change if a different algorithm is used." *Verification* corrected the claim that Penal's departure was found by
reading its method (it was declared) and that round one's simulations were organizer-run (they appear to have been run by
participants under the prescribed procedure). *Sources:* https://www.wouterdenhaan.com/datasuite.htm,
https://www.wouterdenhaan.com/suite/ModelB.pdf, https://www.wouterdenhaan.com/papers/comparison.pdf,
https://robertkollmann.com/JUILLARD_VILLEMOT_TESTBENCH_JEDC2011.pdf,
https://robertkollmann.com/KOLLMANN_PUBL_MALIAR_MALIN_PICHLER_JEDC_2011.pdf,
http://web.archive.org/web/20170928081743/http://www.dynare.org:80/JedcTestsuiteWiki/TestBenchProblemA

**Aruoba, Fernandez-Villaverde and Rubio-Ramirez, comparing solution methods (2003 working paper, JEDC 2006).** *Compares*
eight approximations of the stochastic growth model with leisure, by one team. *Decisions:* value-function iteration on a
million-point grid introduced as "a natural benchmark"; one fixed set of shocks for all methods; Euler errors pointwise and
integrated against a simulated distribution; computing time on one machine; equal time budgets rejected as "not very
useful". *Lessons:* the benchmark's own errors (around 1e-5) were worse than the fifth-order perturbation's (below 1e-7),
and the authors warn against treating value-function iteration as the "true" solution. The integrated metric put the
benchmark first while its pointwise errors put it behind, and the weighting distribution was its own (the authors call
that bias slight). *Verification* softened the weighting-bias lesson to what the table shows. *Sources:*
https://economics.sas.upenn.edu/sites/default/files/filevault/working-papers/04-003.pdf,
https://ideas.repec.org/a/eee/dyncon/v30y2006i12p2477-2508.html

**Aruoba and Fernandez-Villaverde, comparing programming languages (2014 onward).** *Compares* one algorithm (grid-search
value-function iteration) in many languages and runtimes. *Decisions:* a closed-form policy (full depreciation, log
utility) checks accuracy; correctness is that every implementation converges in the same 257 iterations to identical
value and policy functions; the paper's table names every compiler and runtime version; improvements are accepted only if
offered for all languages, and the main fork is frozen "to allow researchers to check our basic results." *Lessons:* the
speed ranking drew disputes from 2014 to 2022 over timers, printing inside timed loops, bounds checking and idiom; the
timer is described two ways (elapsed in the paper, CPU time in an issue reply); timings decayed with runtimes (base R
from 345 seconds to about 20); the repository's code moved on after the timed version. *Verification* corrected an
earlier claim that versions were unpinned (the paper pins them; the README does not). *Sources:*
https://github.com/jesusfv/Comparison-Programming-Languages-Economics, https://www.nber.org/papers/w20263.pdf,
https://github.com/jesusfv/Comparison-Programming-Languages-Economics/issues/6

**The Macroeconomic Model Data Base (MMB).** *Compares* more than 160 macro models, all solved by Dynare, on common
variables, common shocks and common policy rules. *Decisions:* each model's equations stay in its authors' notation, with
marked sections defining the common variables in terms of the model's own (the nearest economic precedent for our
lexicon); a JSON file per model declares its capabilities (which of nine rules it supports), coefficients mapping its rule
to the standard form, and a units flag; the desktop application validates every model's JSON against a draft-07 schema
with `additionalProperties: false` at load and collects failures per model; admission requires visual replication of a
figure in the source paper. *Lessons:* models admitted on replication still carry reported, unresolved parameter
questions (issue 169's commented-out posterior mean; issue 168's fiscal shock); the manual's "any Dynare version" broke
when Dynare 6 appeared (issue 170, still open). *Verification* found the load-time schema validation, which corrected the
cross-field claim that no project validated submissions by machine. *Sources:* https://macromodelbase.com/,
https://github.com/IMFS-MMB/mmb-gui-electron/blob/master/src/schemas/model.schema.json,
https://github.com/IMFS-MMB/mmb-gui-electron/issues/170, https://www.econstor.eu/bitstream/10419/97763/1/IMFS_WP_49.pdf

**NIST Statistical Reference Datasets, as McCullough and vendors used them.** *Compares* statistical packages on fixed
problems with certified answers. *Decisions:* one self-describing text file per dataset (model, data, certified values,
difficulty class, two starting points for nonlinear problems); linear values computed carrying 500 digits with the
decimal data "read in exactly"; nonlinear values "confirmed by at least two different algorithms and software packages";
accuracy as digits of agreement (log relative error), capped at the certified digits; McCullough reported every package
twice, at default settings and at others. *Lessons:* several packages scored zero at defaults on problems they solved to 7
to 11 digits with other options; on the Filip data packages silently dropped collinear regressors; on three ANOVA sets
every binary double-precision package scores at most about 4.6 digits because the decimal data cannot be stored exactly,
so Stata built rescaled variants that score 15 ("the problem is with the test, not the packages being tested"); NIST's own
pages disagree on the digit counts and on the nonlinear working precision (128-bit against 64-bit). NIST "does not
endorse", runs no validation service, and leaves vendors to self-report. *Verification* found that the absolute-error
fallback near zero is Stata's definition, not NIST's, and that the rescaled variants are Stata's. *Sources:*
https://www.itl.nist.gov/div898/strd/general/bkground.html, https://www.itl.nist.gov/div898/strd/nls/nls_info.shtml,
https://www.itl.nist.gov/div898/strd/anova/SmLs07_cmd.html, http://qed.econ.queensu.ca/jae/1999-v14.2/mccullough/,
https://www.stata.com/support/cert/nist/

**The AEA Data Editor's reproducibility checks, with TRACE's Transparent Research Objects.** *Compares* authors' replication
packages with their manuscripts before acceptance. *Decisions:* a fixed outcome scale (full; full with minor issues;
partial, where more than 25 percent differ; not able to reproduce) and a fixed list of reasons (software not available to
the replicator, insufficient computing resources, data missing, and others); the authors' stated environment recorded
separately from the replicator's; "DO commit to git before EACH new run with corrected code"; reports from trusted third
parties and from signed TRO declarations accepted. Since November 2026 the template ships AI-agent skills: one runs a
package and drafts findings, a separate one finalizes the report, and the editor decides. *Lessons:* the outcome scale
and reasons list encode operating experience; no published retrospective was found. *Verification* removed an unsourced
count of packages and dated the current policy (February 2026). *Sources:*
https://www.aeaweb.org/journals/data/data-code-policy, https://github.com/AEADataEditor/replication-template,
https://transparency-certified.github.io/trace-specification/docs/tro-declaration-format

**Dynare's test suite, with its cross-validation against the Sequence-Space Jacobian toolkit.** *Compares* Dynare with
results stored from Dynare 4.3.2, and its heterogeneous-agent Jacobians with SSJ's on the same models. *Decisions:*
about 890 registered model files, about 40 expected to fail; fixed absolute thresholds (1e-6 against the old release,
1e-3 against SSJ); SSJ's large reference file downloaded at test time with no checksum in the lines read. *Lessons:*
golden files from an old release test "unchanged", not "right"; a fixed 1e-3 threshold is unrelated to either toolkit's
convergence. *Verification* confirmed the thresholds and removed an unread claim. *Sources:*
https://git.dynare.org/Dynare/dynare/-/blob/master/tests/heterogeneity/test_solve_functionality.m,
https://github.com/shade-econ/sequence-jacobian

### Numerical-methods benchmarking against reference solutions

**The Test Set for IVP Solvers (CWI, then Bari), 1996 to 2008.** *Compares* stiff ODE and DAE solvers on real problems.
*Decisions:* each problem has a four-part description (general information, mathematical description with "all
ingredients that are necessary for implementation", origin and interpretation, numerical solution) and a Fortran file of
six subroutines, one of which holds the reference; one generic driver per solver, inputs at their defaults "unless stated
otherwise", with any per-problem adaptation (DASSL's error control for higher-index problems) in the driver; accuracy as
significant correct digits at the end point (scd, then mescd, "what actually the solvers ... try to control"); solvers
compared by sweeping their own tolerances and plotting achieved digits against time; every published number names its
machine and compiler; a standing caveat that the diagrams "just show the result of runs with the prescribed input on the
specified computer". *Lessons:* reference solutions were recomputed in two later releases; one problem was reformulated;
the drivers were "changed considerably"; intake by email closed and reopened, and no release followed 2008. The problems
outlived the harness: ten of the thirteen stiff-ODE notebooks in SciMLBenchmarks are Bari problems. *Verification*
corrected the problem count (16 in release 2.0), marked the 128-bit Cray precision as an inference and the stall's cause as
an interpretation. *Sources:* https://archimede.uniba.it/~testset/, https://ir.cwi.nl/pub/4619/04619D.pdf,
https://archimede.uniba.it/~testset/report/hires.pdf

**SciMLBenchmarks.jl with DiffEqDevTools.** *Compares* ODE, SDE, DAE and other solvers across Julia and wrapped C and
Fortran codes. *Decisions:* problems are code in Weave notebooks, each folder with its own Manifest; solvers enter through
the common `solve()` interface; references are trusted solvers at 1e-14; work-precision sets sweep tolerances and plot
achieved error against time; benchmarks run on dedicated self-hosted runners, and each page ends with package versions
and the machine; "critique by pull request" because "issues ... are generally vague and not actionable, while pull
requests with code changes are exact". *Lessons:* the "wall": when every method plateaus at a common error, the
reference is the limit ("any walling behavior is an indicator that some method in the benchmark set is more accurate than
the reference"); omitted or failing methods are documented in notebook prose; narrative "fastest" sentences rank in
effect. *Verification* confirmed the wall passage and the archive of DiffEqDevTools (2026-05-12). *Sources:*
https://github.com/SciML/SciMLBenchmarks.jl,
https://raw.githubusercontent.com/SciML/DiffEqDevTools.jl/master/src/test_solution.jl

**COCO: Comparing Continuous Optimizers.** *Compares* black-box optimizers on suites of functions with known optima.
*Decisions:* truth is known by construction and kept from the solver ("not easily accessible in the API"); runtime in
function evaluations to reach a target, not wall time; "the very same parameter setting must be used" on every function,
function-dependent settings prohibited since 2012, and other settings benchmarked as "different algorithms"; never
aggregate over dimension; an archive definition listing each data file's SHA-256 and size; datasets accepted on a
publication, with code optional. *Lessons:* declaring an algorithm better because it reaches 1e-30 instead of 1e-10 "is
more often than not unjustified"; aggregating unbalanced suites "can ... seriously misguide research efforts". *Verification*
replaced "about 100 targets" with the papers' 51 and left unverified whether hashes are checked on download. *Sources:*
https://arxiv.org/pdf/1603.08785v4, https://arxiv.org/pdf/1605.03560,
https://raw.githubusercontent.com/numbbo/data-archive/gh-pages/howtos/publish-a-dataset-howto.md

**Benchopt.** *Compares* optimization solvers across datasets and objectives in benchmark repositories. *Decisions:* one
Python class per solver, R and Julia through wrappers; metrics computed "off-line" by the objective "to ensure fair
evaluation"; JIT warm-up excluded from timing; a `benchopt test` conformance suite (dataset and solver classes,
installation, stopping criterion, a run) before any comparison; results as a long table with system and version columns;
truth is the best iterate among entrants, so "the curves are a lower bound estimate of the sub-optimality". *Lessons:* a
float32 solver shows up as an accuracy floor; one framework was 28 percent slower despite best practices; reporting only
the best test error is a recurrent criticism. *Verification* added a conformance test and noted that the dashboard also
offers bar charts. *Sources:* https://github.com/benchopt/benchopt, https://arxiv.org/pdf/2206.13424,
https://raw.githubusercontent.com/benchopt/benchopt/main/benchopt/tests/test_benchmarks.py

**NIST StRD, the numerical-methods view.** The economics entry above covers it. What this survey added: the linear
certification page says the decimal data were "read in exactly as multiple precision numbers" and that "these multiple
precision results are an idealization", and the Simon-Lesage case shows that a reference computed from exact decimals is a
different problem from the one every binary-double package solves. *Sources:*
https://www.itl.nist.gov/div898/strd/anova/SmLs07_cmd.html, https://www.nist.gov/itl/sed/statistical-reference-datasets-strd

**posteriordb, with a note on the Inference Gym.** *Compares* Bayesian inference algorithms on a library of posteriors.
*Decisions:* model, data and posterior are separate objects; a written definition of a reference posterior with
acceptance checks (R-hat below 1.01, autocorrelation, E-FMI, no divergences) and an info record per reference (method,
arguments, seed "for full reproducibility", diagnostics, checks made, versions); the reference's draw count "imposes an
upper bound on the accuracy of a system being evaluated"; the Inference Gym stores a standard error beside every ground
truth value. *Lessons:* "In hindsight, more difficult posteriors are more relevant"; "separate the model, data, and
posteriors"; the references come from Stan, which also writes most models. *Verification* corrected the author list and
the draw-count wording. *Sources:* https://github.com/stan-dev/posteriordb,
https://raw.githubusercontent.com/stan-dev/posteriordb/master/doc/REFERENCE_POSTERIOR_DEFINITION.md,
https://arxiv.org/abs/2407.04967

**Hans Mittelmann's benchmarks for optimization software.** *Compares* LP, MILP, NLP and other solvers, run by one
organizer on fixed hardware. *Decisions:* shifted geometric means of wall time scaled so the best is 1; failures counted
at the time limit; logs published. *Lessons:* in 2018 a vendor presented a self-selected subset of 99 models, on the
organizer's logs, as if it were his independent analysis; two vendors demanded removal; Gurobi withdrew in August 2024,
saying rigorous validation and over-tuning detection needed more resources than the benchmark had, and MindOpt followed in
December 2024. *Verification* quoted the 2018 retraction verbatim and updated the code list. *Sources:*
https://plato.asu.edu/bench.html, https://plato.asu.edu/ftp/apology.pdf, https://plato.asu.edu/talks/informs2022.pdf

### Simulator standards and cross-simulator testing in systems biology and neuroscience

**The SBML Test Suite, Test Runner and Test Suite Database (2007 onward).** *Compares* SBML simulators against 1,823
semantic cases and 100 stochastic ones. *Decisions:* one directory per case holding the model in each SBML level it
translates to, a settings file with output grid and per-case absolute and relative tolerances (relative 1e-4 by default,
agreed at 2008 hackathons), expected results and tags; the developer writes the wrapper the Runner calls with five
placeholders; cases excluded by tag are "marked as unsupported instead of failed"; the stochastic cases use statistics
scaled by the number of runs, with a stated expected rate of false failures; the Database shows a per-case map per tool
version with no totals. *Lessons:* tolerances were loosened repeatedly "by request" of those tested; expected results were
wrong, including an analytic one (case 00939), and were corrected in place with a line in the changelog; since 3.0.0 the
Runner deletes each output file before invoking the wrapper, because "not all wrappers behave as expected" and a stale file
would be read as a result; a bug in the shared parser surfaced as test failures; the README's "one fifth analytic" has
drifted from the corpus (42 percent by tag). *Verification* tallied all 1,823 cases, found case 01000's reference rests on
one named tool, and removed an unsupported claim about unvetted uploads. *Sources:*
https://github.com/sbmlteam/sbml-test-suite,
https://raw.githubusercontent.com/sbmlteam/sbml-test-suite/develop/NEWS.md,
https://sbml.org/software/sbml-test-suite/docs/test-wrappers, https://sbml.bioquant.uni-heidelberg.de/

**Bergmann and Sauro, comparing SBML simulators (2008).** *Compares* six and later more simulators on 150 curated
models with no reference: "As no authoritative result set exists". *Decisions:* one fixed experiment for every model (0 to
10 seconds, 1,000 points); pairwise errors between simulators, taking "the second highest value" of each error vector so
single-point failures are not penalized; results binned by agreement. *Lessons:* the comparison found flaws later fixed;
the fixed span missed features; the metric "draws no conclusions as to the correctness of the results". *Verification*
corrected two quotations. *Sources:* https://pmc.ncbi.nlm.nih.gov/articles/PMC2732216

**BioSimulators and BioSimulations, with SED-ML, KiSAO and COMBINE archives.** *Compares* simulation tools through a
registry and a validation suite. *Decisions:* each tool is a Docker image with a standard command (`-i` archive, `-o`
output folder, `-v` printing its version "and the versions of any critical dependencies"); a JSON specification per tool
version with the image digest, algorithms named by KiSAO terms and their parameters with recommended ranges; KiSAO names
each algorithm and setting (absolute tolerance KISAO:0000211, seed KISAO:0000488) and publishes a substitutability
matrix; submission by a GitHub issue that triggers an automated validation run, with manual review of a tool's first
version only; `validateImage: false` admits a tool without a compliant image; test cases skip by declared capabilities or
by a `skippedSimulators` entry carrying a reason and an issue link. *Lessons:* the suite mostly checks conformance (in 24
of 27 project files only time values are checked numerically); `runtimeFailureAlertType: warning` turns a crash into a
passing warning; the recommended substitution default lets a tool run an algorithm other than the one requested; SED-ML
renamed `numberOfPoints` because it meant "the number of output points minus one". *Verification* corrected counts and
field names and added the failure-downgrade switch. *Sources:* https://ar5iv.labs.arxiv.org/html/2203.06732,
https://docs.biosimulations.org/concepts/conventions/simulator-interfaces/, https://github.com/SED-ML/KiSAO,
https://raw.githubusercontent.com/biosimulators/Biosimulators_test_suite/dev/biosimulators_test_suite/test_case/published_project.py

**Reproducibility curation in BioModels and the Physiome/CellML repository.** *Compares* published models, re-encoded and
re-simulated by curators, with the papers' figures. *Decisions:* BioModels re-simulates "using a software different from
the one used in the original manuscript"; outcomes are binary, without numeric tolerance; failures sit unlabeled in the
non-curated part. The Physiome repository uses curation stars, with level 3 requiring "a domain expert who is not the author
of the original publication". *Lessons:* 37 percent of 455 models did not reproduce, mainly from missing parameters and
initial conditions ("insufficient and incorrect reporting"); the community asked for "transparent and flexible
labelling"; the Physiome documentation says its levels 1 (faithful to the paper's math) and 2 (reproduces its
results) "may be mutually exclusive" and plans to replace the stars. *Verification* softened a claim that the single scale
"broke down" because of that conflict. *Sources:* https://pmc.ncbi.nlm.nih.gov/articles/PMC7901289,
https://aucklandphysiomerepository.readthedocs.io/en/latest/cellmlcuration.html

**The Cardiac Electrophysiology Web Lab.** *Compares* many cardiac cell models under many virtual protocols (36 by 23 at
publication), by one engine. *Decisions:* protocols are separate from models and bind to them through annotations of
physiological meaning, so a protocol whose quantities a model lacks is computed to be inapplicable (a gray cell); results
are stored and rerun when a model or protocol changes; "a model displaying all green results should not be considered as
the best model". *Lessons:* testing across protocols found an error in a widely used model file that had been public since
2010, because "these differences only become apparent when a model is tested in a range of situations"; transient and
steady-state protocols gave different conclusions for the same model. *Verification* corrected a quotation and the
meaning of the red cell. *Sources:* https://pmc.ncbi.nlm.nih.gov/articles/PMC4724653,
https://github.com/ModellingWebLab/WebLab

**OSB Model Validation (OMV).** *Compares* one neural model on many simulator engines against stored expected properties.
*Decisions:* a shared file of expected emergent properties per model and one test file per engine giving the observables
and the tolerance; `numpy.allclose` with the tolerance as a relative tolerance, 0.1 by default; OMV installs engines at
default versions; tests run in the model's own CI. *Lessons:* the per-engine files' tolerances are 2.2e-16 and 0, which is
consistent with expected values written from a run's output (an inference); after each check the tool prints "A better
tolerance to try is". *Verification* confirmed the counts and the messages. *Sources:*
https://github.com/OpenSourceBrain/osb-model-validation,
https://raw.githubusercontent.com/OpenSourceBrain/osb-model-validation/master/omv/analyzers/utils/timeseries.py

**SciUnit, NeuronUnit and the EBRAINS Model Validation Framework.** *Compares* neuron models with experimental
observations. *Decisions:* a test declares the capabilities it needs; a model lacking one gets NAScore, "not a failure", and
TBDScore marks capable but not yet run; typed scores declare their best and worst values; EBRAINS forbids editing a result,
deleting anything, or editing a model or test once a result cites it. *Lessons:* SciUnit builds ranking into its core
(`stature()`, weighted means, colored tables); models translated to NeuroML still need checking "to ensure that nothing has
been lost in translation". *Verification* replaced two unfound quotations. *Sources:* https://github.com/scidash/sciunit,
https://raw.githubusercontent.com/scidash/sciunit/master/sciunit/scores/incomplete.py,
https://hbp-validation-client.readthedocs.io/en/master/

### Cross-code verification in materials science and quantum chemistry

**The Delta test (Lejaeghere et al., Science 2016).** *Compares* 40 methods (a code with a potential set) across 15 DFT
codes on the equation of state of 71 elemental crystals. *Decisions:* the unit compared is the method, not the code; no
absolute reference ("the definition of D does not favor a particular reference"); the spread among all-electron codes is
taken as "the best attainable precision"; the tolerance is calibrated against that spread and against experimental scatter;
methods listed alphabetically within categories; speed excluded. To isolate method differences, four codes ran osmium with
inputs "as consistently as possible", and a deviation above the noise was "partly" traced to a different scalar-relativistic
scheme, a choice the problem statement had not fixed. *Lessons:* a specification leaving settings to each code "would have to
include code defaults and hard-coded values"; the update page the paper promised is gone after a site redesign.
*Verification* corrected the history of the Delta metric and the osmium attribution. *Sources:*
https://perso.uclouvain.be/gian-marco.rignanese/publications/A061.pdf, https://molmod.ugent.be/deltacodesdft

**ACWF verification of DFT precision (Bosoni et al. 2024).** *Compares* nine pseudopotential approaches with an
all-electron reference on 960 crystals. *Decisions:* the reference is the average of two independent all-electron codes,
whose spread is its error bar, and four systems outside "good" are named; Box 3 lists the choices every approach must share
(smearing type and width, the energy fitted, the k-mesh in scaled units, fixed reference volumes, the fitting protocol);
the reference is for that regularized problem, "not ... the zero-temperature (i.e., no smearing) limit"; thresholds
derived by propagating random noise through the fit, and tied to the volume window; results labeled by approach (code,
method, library); results files flag failed workflows, missing outputs and systems whose minimum lies at the window's edge.
*Lessons:* erbium in the diamond structure has two minima whose order depends on smearing, so smearing had to be fixed;
reusing the minimum energies for formation energies can be off by 1 eV per atom ("Do not transfer the choices ... to a
different context"); verification drove fixes in four pseudopotential libraries; intermediate results moved through a
shared Google Drive; dependency pins disagree across the repository's files; one protocol name covers three
pseudopotential libraries, distinguished only by file name. *Verification* corrected the relation of the new metrics to
Delta and identified the protocol-name lesson. *Sources:* https://arxiv.org/abs/2305.17274,
https://github.com/aiidateam/acwf-verification-scripts

**AiiDA common workflows (Huber et al. 2021).** *Compares* nothing itself: an interface across eleven DFT and
quantum-chemistry engines. *Decisions:* a code-specific input generator behind one call signature; inspection methods
report in machine-readable form what each implementation supports; protocols fast, moderate and precise, mapped to
parameters "up to the respective code experts"; the step that turns common inputs into code inputs is not recorded.
*Lessons:* only 2 of 8 relaxation types are shared by all codes; total energy has no code-independent zero; the
verification study later needed a separate cross-code protocol; the mechanism for making runs comparable needed fixes
before the first stable release. *Verification* marked two claims as inferences. *Sources:* https://arxiv.org/abs/2105.05063,
https://aiida-common-workflows.readthedocs.io/en/latest/workflows/base/relax/index.html

**MolSSI QCSchema, QCEngine, QCDB and QCArchive.** *Compares* nothing itself: one schema and executor across many
quantum-chemistry programs, and an archive. *Decisions:* the executor never homogenizes ("There is no compensation for
program peculiarities", so "b3lyp" differs where programs chose VWN3 or VWN5); a separate layer (QCDB) registers each
program's defaults (frozen core, density fitting, convergence) and can impose shared ones (a "unified" mode) or leave each
program at its own (a "sandwich" mode); algorithm choices kept out of the method name; units fixed by the schema; exact
deduplication of computations, returning the existing record; every attempt kept with its output and error; schema v1
and v2 coexist with conversion functions. *Lessons:* shared names hide divergent definitions; values found wrong were
"reported to the code developers". *Verification* replaced a units quotation that could not be found. *Sources:*
https://pmc.ncbi.nlm.nih.gov/articles/PMC8614229, https://molssi-qc-schema.readthedocs.io/en/latest/,
https://docs.qcarchive.molssi.org/user_guide/record_submission.html

**GW100 (van Setten et al. 2015) and its follow-ups.** *Compares* GW codes on the ionization energies and electron affinities
of 100 molecules. *Decisions:* fixed geometries; a relativistic convention fixed to exclude one source of difference; the
reference an extrapolation to the complete basis, its error the gap between two extrapolation schemes; contributions as JSON
files by pull request. *Lessons:* "Because not all GW codes search for all solutions, different G0W0 implementations may
give different answers for multiple-solution cases": the problem left the root unstated; the extrapolated reference was later
found weak for affinities and above-vacuum resonances; the frequency treatment ended up in an undocumented free-text field
with ten inconsistent values, and root selection in file names. *Verification* corrected what the follow-ups found and
counted the field in 95 of 111 files. *Sources:* https://github.com/setten/GW100, https://arxiv.org/abs/1610.01853,
https://math.berkeley.edu/~linlin/publications/GW100.pdf

**Matbench Discovery.** *Compares* machine-learned interatomic potentials against DFT on a ranked leaderboard.
*Decisions:* a submission schema that "rejects unknown keys"; canonical file names checked by code; prediction files by URL
with optional hashes; one ingestion command that evaluates, renders and archives; an entry lifecycle (pending, active,
superseded, deprecated, aborted); disclosed caveats marked, not excluded; a composite score with adjustable weights.
*Lessons:* a constant in the composite score was wrong by a factor of ten and was fixed a day after the score became the
sort key; the live leaderboard runs ahead of the last tagged release and shows no benchmark version. *Verification*
removed an unsupported claim and found the constant fix. *Sources:* https://matbench-discovery.materialsproject.org/contribute,
https://raw.githubusercontent.com/janosh/matbench-discovery/main/changelog.md, https://arxiv.org/abs/2308.14920

### Model intercomparison and code verification in the earth and physical sciences

**The SCEC/USGS Spontaneous Rupture Code Verification Project, and its successor SEAS.** *Compares* about eighteen
independent earthquake-rupture codes on 45 benchmark problems, with no analytic solutions. *Decisions:* one versioned PDF
per benchmark ("TPV" for "The Problem, Version"), complexity added one step at a time; uploads of ASCII files with a
self-describing header (code, "Code version (if desired)", element size, time step) that the server checks at once,
returning a success page, an error log or a warning log; convergence as its own benchmark at resolutions spanning two
orders of magnitude; results overlaid, never ranked; uploads deletable and results behind a login. *Lessons:* the
fault-branch problems agreed least until the branch's end was defined "so that its location is not dependent on the
discretization size"; a well-posed problem was chosen so that results converge; "The slow but steady approach has worked
best". In SEAS the problem stated a semi-infinite half-space, codes chose their own truncation and boundary conditions, and
"far-field boundary condition type leads to quantitative differences in long-term fault behavior": each converged, but to
different limits. *Verification* corrected the code count and quotations and left the metric formulas unverified.
*Sources:* https://strike.scec.org/cvws/, https://kbolsen.sdsu.edu/PUBL_dir/srl-Harris_2018.pdf,
https://igppweb.ucsd.edu/~fialko/Assets/PDF/Erickson_SRL20.pdf, https://strike.scec.org/cvws/download/uploadTPV67v2.pdf

**The NASA Turbulence Modeling Resource and the AIAA benchmarking working group.** *Compares* implementations of named
turbulence models in independently written CFD codes. *Decisions:* each model's variants are named by a grammar (a base
model plus corrections, some combinations forbidden, some choices that "should always be reported", a non-default constant
written into the name), "to help avoid confusion when comparing results from different codes"; each case ships a nested
grid family; reference values by grid convergence of codes that passed the method of manufactured solutions, each value
printed with apparent order, extrapolated error and grid-convergence index; a Model Readiness Rating that rates evidence
(described, one code, two codes agree, codes from two organizations, manufactured solutions) and "does not judge the
quality". *Lessons:* the site began because "different codes with ostensibly the same turbulence model would produce
inconsistent results"; failing a simple 2D case predicted outlying results on a full aircraft; resolution near a sharp
trailing edge mattered more than the discretization scheme, and asymptotic order was not established even at 15 million
degrees of freedom; "a better procedure for collating results from different codes needs to be found". *Verification*
removed an unsupported claim that the site named the thin-layer variant in response to a finding. *Sources:*
https://tmbwg.github.io/turbmodels/, https://tmbwg.github.io/turbmodels/spalart.html,
https://tmbwg.github.io/turbmodels/modelreadiness.html,
https://ntrs.nasa.gov/api/citations/20160006057/downloads/20160006057.pdf,
https://fun3d.larc.nasa.gov/papers/aiaa-2015-1746.pdf

**The CMIP6 data infrastructure.** *Compares* output of coupled climate models once standardized. *Decisions:*
"machine-readable experiment design", meant "to avoid ... errors ... introduced by the need for humans to transcribe" the
protocols; controlled vocabularies as versioned JSON releases with DOIs, pinned by consumers as a git submodule; a writing
library (CMOR) that checks units and attributes; PIDs per file; a version per "atomic dataset" so one bad variable need
not republish the rest; superseded data kept and marked; errata served by querying a PID. *Lessons:* pushing retraction
notices to users "was found to result in imperfect coverage", so errata became "pull"; third-party snapshot archives missed
corrections; key software is "built and tested by volunteers or short-term project staff"; the validator built into the
writing library was deprecated and removed; the CMIP7 data request moved to a fixed timetable of releases after users
asked to limit "the number of versions and updates". *Verification* replaced an unsourced variable count and attributed the
validator's replacement to a downstream project. *Sources:* https://gmd.copernicus.org/articles/11/3659/2018/gmd-11-3659-2018.pdf,
https://github.com/WCRP-CMIP/CMIP6_CVs, https://github.com/PCMDI/cmip6-cmor-tables,
https://gmd.copernicus.org/articles/19/8053/2026/gmd-19-8053-2026.html

**ISIMIP3: the machine-actionable protocol, isimip-qc and the repository.** *Compares* impact models under common
forcing. *Decisions:* one repository of definitions renders both the human-readable protocol and the checker's inputs,
with schema tests on every edit; the checker stamps a unique ID, its own version, the protocol's git hash and the pass date
into each file; a model whose behavior changes gets a new version name, so that differences "are fully attributable to the
changes in model forcings"; replaced data get a new DOI version, the old one kept online and on tape, with a caveat log.
*Lessons:* the checker reads the live protocol by default (it stamps the hash it used); its fixes are written into the
original files. *Verification* found the version rule's purpose stated in the protocol itself. *Sources:*
https://github.com/ISI-MIP/isimip-protocol-3, https://github.com/ISI-MIP/isimip-qc,
https://www.isimip.org/dashboard/doi-creation-replacement/

**ESMValTool and the PCMDI Metrics Package.** *Compares* climate model output with observational references. *Decisions:*
ESMValTool v2 moved preprocessing (regridding, masking) from each diagnostic into a shared core after v1 showed "lack of
consistency among the different approaches"; non-conforming datasets are handled by named "fixes" per project, dataset,
table and variable, contributed by pull request; the checker's strictness is chosen (ignore, relaxed, default, strict);
W3C-PROV provenance attached to every output. PMP keeps a default and alternative observational references because "we
lack definitive measures as to which is the most accurate", and shows the spread; it leaves ranking to users, yet
normalizes errors by the median model. *Lessons:* a stricter reader exposed more departures, each needing a named fix; the
order of regridding and computing extremes changes the comparison. *Verification* corrected a quotation and attributed one
claim to older documentation. *Sources:* https://gmd.copernicus.org/articles/13/1179/2020/,
https://docs.esmvaltool.org/projects/ESMValCore/en/latest/develop/fixing_data.html,
https://gmd.copernicus.org/articles/17/3919/2024/

**AGORA, the galaxy-simulation comparison.** *Compares* seven to nine galaxy-formation codes. *Decisions:* shared initial
conditions, a shared cooling library used through a common interface, and one analysis platform; calibration in steps,
"adding one physical process at a time"; feedback left to each code's community practice and tuned to a target; "We do
not intend to identify a correct or incorrect code". *Lessons:* the step that introduced the shared cooling library exposed
problems in each group's interface to it; parameters chosen on an isolated disk "cannot be naively used in cosmological
simulations"; participants learned "sometimes surprisingly, about their own" codes. *Verification* softened a claim that
every code had bugs. *Sources:* https://arxiv.org/abs/2106.09738, https://arxiv.org/abs/1308.2669

**The Jablonowski-Williamson baroclinic wave and the DCMIP series.** *Compares* atmospheric dynamical cores. *Decisions:*
a two-part test, first keeping an analytic steady state, then a perturbation with no analytic solution; the reference is a
set of very-high-resolution solutions from several models, and "the maximum spread of all high-resolution reference
simulations defines the uncertainty of the reference state despite the fact that all single-model assessments stay well
below the uncertainty limit"; once a model converges within that band "finer horizontal resolutions do not provide a
better estimate"; diffusion treated as part of each scheme, so the cores "solve different equations", against an
alternative test that prescribed diffusion to obtain exact convergence. DCMIP2016 ships shared Fortran initialization and
physics routines and names non-default settings in a file-name field. *Lessons:* the test exposed a flawed energy fixer in
one core; the paper's verdict that one core is "most cost-effective" is a judgment from cost. *Verification* replaced "no
ranking" with that verdict. *Sources:*
https://www.gfdl.noaa.gov/wp-content/uploads/files/user_files/pjp/qj_jablonowski_williamson_2006.pdf,
https://gmd.copernicus.org/articles/10/4477/2017/, https://github.com/ClimateGlobalChange/DCMIP2016

### Benchmarks and comparison platforms in machine learning and forecasting

**MLPerf Training and Inference.** *Compares* whole systems on fixed workloads. *Decisions:* a reference implementation
defines each workload and is "not optimized for performance"; a Closed division requiring equivalence to the reference and
an Open division listed and labeled; Reference Convergence Points, a band from repeated reference runs applied by a stated
one-sided t-test, with a recorded group vote to accept a failure; inference accuracy targets defined as 99 or 99.9 percent
of the reference's; a load generator "compiled from a tagged approved revision ... without alteration", with a test that
outputs logged in the performance run match the accuracy run; rules against cherry-picking runs; every submitter reviews
another's submission; a random audit with hardware access; no official summary score, because "no weighting scheme is
universally representative" and because coverage differs; Messaging Guidelines that bind anyone quoting results (result
IDs, "unverified" beside unreviewed scores, no comparison with non-MLPerf results). *Lessons:* run counts were calibrated
on the references' own variance; mature rule sets still carry sections marked "TODO". *Verification* corrected round dates
and several rule details. *Sources:* https://github.com/mlcommons/training_policies/blob/master/training_rules.adoc,
https://github.com/mlcommons/policies/blob/master/submission_rules.adoc,
https://www.github.com/mlcommons/policies/blob/master/MLPerf_Results_Messaging_Guidelines.adoc,
https://github.com/mlcommons/inference/blob/master/compliance/TEST01/README.md, https://arxiv.org/pdf/1910.01500

**OpenML.** *Compares* algorithms through a public registry of tasks, flows, setups and runs. *Decisions:* evaluation is
server-side, and a new metric can be computed for every stored run because runs keep their predictions; a flow is name plus
software version with exact dependency versions and parameter metadata (type and description); a client checks for an
existing run of the same task and setup. *Lessons:* the benchmark suite's successor fixed errors found after release
(duplicate datasets, a time-dependent one); "exactly reproducing all results may not always be possible" without
environment capture; suite versioning is informal. *Verification* removed a claimed inconsistency and marked setup sharing
as an inference. *Sources:* https://docs.openml.org/concepts/runs/, https://ar5iv.arxiv.org/html/1708.03731

**AMLB, the AutoML Benchmark.** *Compares* AutoML frameworks on OpenML tasks under fixed budgets. *Decisions:* resource
constraints kept apart from tasks; each framework integrated in "less than 250 lines of code across at most four files",
written with its authors so it runs "as intended by their authors"; a failure taxonomy (memory, time, data,
implementation); frozen framework versions. *Lessons:* failures "correlate with data set properties", so averaging over
solved tasks inflates results; an earlier study compared a framework set to the wrong metric with another's optimization
disabled; the aim to freeze versions "ideally, every quarter" produced three frozen sets in six years. *Verification*
settled the frozen sets and removed a version number. *Sources:* https://arxiv.org/pdf/2207.12560,
https://openml.github.io/automlbenchmark/docs/extending/framework/

**HELM (Stanford CRFM).** *Compares* language models across scenarios and metrics. *Decisions:* "The object of evaluation
is the language model"; one standardized adaptation for all; all raw prompts and completions released; results tied to
query timestamps. *Lessons:* one model scored 79.1 percent with one prompt layout and 30.2 with another, so the authors
recommend that "model developers explicitly declare how their models should be evaluated"; reproduction documents drifted
(a stale-page warning, two spellings of one variable). *Verification* confirmed the release and removed one claim.
*Sources:* https://arxiv.org/pdf/2211.09110, https://crfm-helm.readthedocs.io/en/latest/reproducing_leaderboards/

**The EleutherAI evaluation harness and the Open LLM Leaderboard.** *Compares* language models on task configurations.
*Decisions:* each task a YAML file with a version bumped on breaking changes and a dated changelog line naming the pull
request and reason; a checklist item "have you checked against the reference implementation"; bootstrapped standard
errors by default. *Lessons:* three implementations of one benchmark disagreed by up to 15 points and reordered models
because of an unstated scoring convention, fixed by aligning with the original; a written priority list for resolving
such questions; models were fine-tuned to the leaderboard's separator tokens; the leaderboard's first version was archived
in 2024 and its second retired in 2025. *Verification* corrected the size of the prompt effect and the leaderboard's
history. *Sources:* https://huggingface.co/blog/open-llm-leaderboard-mmlu, https://arxiv.org/pdf/2405.14782,
https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md

**The US COVID-19 Forecast Hub and the hubverse.** *Compares* teams' real-time probabilistic forecasts. *Decisions:*
versioned JSON task configuration; submissions as files by pull request, validated in CI by named check classes, with a
check flagging changes to earlier submissions; a team's "primary" model designated in advance; truth versions recovered
from commit history; an "auditable trail". *Lessons:* truth data were revised; teams covered different subsets, so
aggregates needed inclusion rules; the hub "could likely have been set up even earlier" with shared infrastructure.
*Verification* corrected which check classes fail CI and removed an unfound lesson. *Sources:*
https://par.nsf.gov/servlets/purl/10338216, https://hubverse-org.github.io/hubValidations/articles/validate-pr.html,
https://pmc.ncbi.nlm.nih.gov/articles/PMC12632657/

**Codabench and CodaLab Worksheets.** *Compares* submissions to organizer-defined benchmarks. *Decisions:* an ingestion
module and a scoring module whose reference data are "invisible to the participant's submission"; result submissions and
code submissions run in organizer images named by tag; Worksheets' run options cap time, memory, disk and processors and
switch the network, and `mimic` reruns everything downstream of one bundle with another substituted. *Lessons:* the
platform itself notes that other registries do not guarantee reproduction. *Verification* corrected a quotation.
*Sources:* https://arxiv.org/pdf/2110.05802, https://codalab-worksheets.readthedocs.io/en/latest/CLI-Reference/

### Conformance suites run across many implementations of one specification

**Bowtie, with the JSON Schema Test Suite.** *Compares* about 69 JSON Schema validators on the official suite.
*Decisions:* each implementation is wrapped in a small harness, usually a container, speaking JSON over stdin and stdout:
`start` carries the protocol version (a harness "should bail out" on one it does not know) and returns the implementation's
name, language and source; `dialect` must not be used "to mutate incoming schemas"; `run` returns valid, errored with
context, or skipped with a message or issue URL; `bowtie smoke` tests a harness against the protocol; harnesses now
publish their own reports, combined centrally only because the suite is pinned to "the newest commit ... at or before the
start of the current hour"; reports record the suite commit and Bowtie's version. *Lessons:* `site combine` still drops
reports whose test cases differ, warning only on stderr; the compliance badge counts declared skips as failures, and the
failure summary sorts worst to best; skip support is "still somewhat crude" without persistent test IDs; the suite "cannot
express indeterminate or error states". *Verification* corrected the restructure's dates, the harness count and the badge
formula. *Sources:* https://github.com/bowtie-json-schema/bowtie,
https://raw.githubusercontent.com/bowtie-json-schema/bowtie/main/docs/implementers.rst,
https://raw.githubusercontent.com/bowtie-json-schema/bowtie/main/bowtie/schemas/io/commands/run.json,
https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md

**web-platform-tests, wpt.fyi and the Interop project.** *Compares* browser engines on a shared suite. *Decisions:* a run
is identified by suite revision, product, browser version and OS; an `aligned` view shows only revisions every product
ran; expected and intermittent outcomes kept per test outside the tests, conditional on version and OS; failures linked to
bugs in a separate metadata repository; Interop chooses focus areas by champions, rankings and veto, and requires "a
mature-enough web standard" and existing tests. *Lessons:* an open request records the concern that per-browser scores
pull test design toward the score; an open issue records a score silently wrong because its denominator counted a test
that no longer existed; the metadata field meant to flag stale triage is "currently unused by tooling". *Verification*
softened the score-pressure claim to a documented concern. *Sources:* https://raw.githubusercontent.com/web-platform-tests/wpt.fyi/main/api/README.md,
https://raw.githubusercontent.com/web-platform-tests/interop/main/charter.md,
https://github.com/web-platform-tests/rfcs/issues/167, https://github.com/web-platform-tests/results-analysis/issues/149

**test262 (ECMAScript).** *Compares* JavaScript engines daily through community dashboards. *Decisions:* one test per file
with front matter citing the specification by named anchor (`esid`) after section numbers proved unstable; feature tags;
a `non-deterministic` flag for tests whose outcome "is neither reliable nor an indication of conformance"; the
interpretation rules versioned so consumers "can more easily determine the cause of new test failures"; tests must rest on
"citable, normative text" and may not forbid permitted extensions; a lighter staging lane for tests converted from
implementations' own suites; a proposal reaches the standard only with "Two compatible implementations which pass".
*Lessons:* a results site whose orchestration and data were "internal to Bocoup" now redirects to an expired-domains page.
*Verification* corrected a quotation and cited the internal-infrastructure claim. *Sources:*
https://raw.githubusercontent.com/tc39/test262/main/INTERPRETING.md, https://raw.githubusercontent.com/tc39/test262/main/CONTRIBUTING.md,
https://tc39.es/process-document/

**toml-test.** *Compares* TOML parsers. *Decisions:* a decoder reads stdin and prints tagged JSON in which every value is a
string with its type, so no number passes through a float parser; comparison is exact but semantic; the comparator
separates a defect of the suite (`bug`) from one of the implementation (`failf`); declared departures are switches
(`-int-as-float`), and `-skip-must-error` turns a declared skip that now passes into a failure; the README lists what the
specification leaves to implementations and tests the recommended choice. *Lessons:* a subcommand removed in 2.0 was
restored nine days later, "as it turns out people were using them". *Verification* corrected what the suite tests about
integer width. *Sources:* https://raw.githubusercontent.com/toml-lang/toml-test/main/README.md,
https://raw.githubusercontent.com/toml-lang/toml-test/main/json.go

**sqllogictest (SQLite).** *Compares* SQL engines, 7.2 million queries against four other databases. *Decisions:* truth by
agreement of independent engines, "to sidestep this tedium"; seeded generation of scripts; labels that require logically
equivalent queries to give identical results; scripts that repeat statements with and without indices to show the results
do not depend on them; per-engine branches where engines legitimately differ (NULL handling). *Lessons:* floats rendered
with three decimals are a tolerance hidden in formatting; a later fork's `--override` makes blessing an engine's output
trivial. *Verification* read the text through a mirror; the canonical page showed a robot check. *Sources:*
https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki, https://www.sqlite.org/testing.html

**Berkeley TestFloat.** *Compares* one floating-point implementation with SoftFloat. *Decisions:* hexadecimal text pipes;
bitwise equality of results and exception flags, with two documented relaxations each of which can be made strict; the
variations the standard permits are switches set to the implementation's declared choice; coverage levels owned by the
test, not the implementation; the trusted emulation is itself tested against an independent one. *Lessons:* a reported
error has four possible causes (permitted variation, a faulty reference, a faulty test program, a faulty implementation),
and "It is the responsibility of the user to determine the causes". *Verification* changed a claimed word-for-word match
with our reading of discrepancies into a five-way vocabulary. *Sources:*
http://www.jhauser.us/arithmetic/TestFloat-3/doc/TestFloat-general.html,
http://www.jhauser.us/arithmetic/TestFloat-3/doc/testfloat_ver.html

**Accuracy of libm implementations (Gladman, Innocente, Mather, Zimmermann).** *Compares* 13 math libraries' elementary
functions with MPFR. *Decisions:* error in ulps with rules for NaN and infinity; every number labeled an upper bound
(exhaustive search) or a lower bound (sampled search); the worst input published in hexadecimal "which enables the reader
to reproduce our results"; worst cases found for one library tried on all; hardware, compiler and flags per library.
*Lessons:* the same binary gives different results on different hardware; documented error bounds are "not always
accurate"; a bold best entry per row is a mild ranking. *Verification* confirmed every claim checked. *Sources:*
https://homepages.loria.fr/PZimmermann/papers/glibc242.pdf, https://hal.univ-lorraine.fr/hal-03141101v1

### Provenance and reproducibility infrastructure for results of record

**CODECHECK.** *Compares* an article's claimed outputs with an independent checker's single run of the authors'
workflow; 141 certificates. *Decisions:* a YAML manifest of required outputs; certificates on Zenodo cited by version DOI,
"not the concept DOI", and published only after an editor's review; validation rules with permanent IDs (`CC-CFG-016`)
and RFC 2119 severities, deprecated rules keeping their IDs, two independent implementations tagged by rule ID; changes
after version 2.0 "only allow what was not allowed before". *Lessons:* "We do not yet have a process for denoting if a
reproduction fails"; failed attempts shared "only with the authors"; matching is human judgment. *Verification* corrected
how proprietary software was handled and left unconfirmed whether the parity check runs. *Sources:*
https://codecheck.org.uk/spec/config/2.0/, https://github.com/codecheckers/register/blob/master/RULES.md,
https://f1000research.com/articles/10-253/v2

**ReScience C.** *Compares* independent reimplementations (replications) and reruns (reproductions) of published
computational work with the originals. *Decisions:* replication "based exclusively on the originally published paper";
outcomes marked in the title (Re, Rp, and ¬Re, ¬Rp for failures); open review on GitHub; a failure to replicate needs the
editors to contact the original authors and "issue a challenge to the community to spot and report errors in the new
implementation", after which the work is "declared non-replicable". *Lessons:* "There is a strong bias towards successful
replication (100%)"; reviewers with the community's libraries installed "may not notice that these libraries are actually
dependencies"; "The main obstacle to replicability is an incomplete or imprecise description of the models and methods";
in the Ten Years challenge undocumented parameter values and normalization were the common failures. *Verification*
settled the submission route. *Sources:* https://arxiv.org/abs/1707.04393, https://rescience.github.io/faq/,
https://media.nature.com/original/magazine-assets/d41586-020-02462-7/d41586-020-02462-7.pdf

**The Common Workflow Language conformance tests.** *Compares* workflow engines against 378 tests. *Decisions:* tests
tagged `required` or by optional feature; 41 tests that must fail; `Any` as a declared wildcard; implementation-specific
fields named once; every document declares its version, with an upgrader; a new feature needs "a formal proposal with a
prototype implementation". *Lessons:* the tests "were critical to the CWL project's success", but "the CWL community does
not yet test or certify implementations"; compliance on the website is self-reported and its badges are hosted by the
implementers; the central results repository has been dormant since 2020. *Verification* recounted the suite. *Sources:*
https://github.com/common-workflow-language/cwl-v1.2/blob/main/CONFORMANCE_TESTS.md, https://www.commonwl.org/implementations/,
https://ir.cwi.nl/pub/33643/33643.pdf

**Workflow Run RO-Crate, on W3C PROV.** *Compares* nothing itself: a record format for executions in six workflow systems.
*Decisions:* three nested profiles so systems can adopt partially; one execution as a `CreateAction` with its instrument,
inputs, results, container image with its sha256, environment variables and status, failures included; each crate declares
its profile by versioned permalink; a validator grades findings required, recommended or optional with a check ID.
*Lessons:* "one single profile would not have been sufficient"; reproducibility "can only be supported, but not ensured".
*Verification* corrected the system count and the environment rule. *Sources:*
https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/, https://arxiv.org/abs/2312.07852v2

**SLSA build provenance.** *Compares* nothing itself: a graded scheme for trusting a record of how an artifact was made.
*Decisions:* external parameters "MUST be complete" and verified downstream, internal ones kept for diagnosis though they
"MAY be necessary for reproducing the build"; the builder's identity is "intended to be the sole determiner" of the level;
level 1 records are "trivial to bypass or forge", level 2 records are signed by a hosted platform. GitHub documents its
artifact attestations as level 2. *Lessons:* version 1.0 removed self-asserted `completeness` and `reproducible` fields
because trust is "implied by builder.id". *Verification* corrected the builder quotation. *Sources:*
https://slsa.dev/spec/v1.0/provenance, https://slsa.dev/spec/v1.0/levels,
https://docs.github.com/en/actions/concepts/security/artifact-attestations

**airspeed velocity (asv).** *Compares* one project's benchmarks across its own commits, per machine. *Decisions:* a named
machine profile; results stored by machine and environment; a benchmark's version defaults to the hash of its code, and
"results whose version is not equal to the current version of the benchmark are ignored"; repeats and samples stored;
regressions flagged only within one machine's history. *Lessons:* noise from frequency scaling and OS upgrades; a
dedicated machine recommended. *Verification* narrowed a truncation claim. *Sources:*
https://asv.readthedocs.io/en/latest/dev.html, https://asv.readthedocs.io/en/latest/tuning.html

**GNU Guix time-machine with Software Heritage.** *Compares* nothing itself: re-deploys an exact environment "bit for
bit". *Decisions:* the whole source graph with content hashes as the identity; a fallback to Software Heritage by content
hash; SWHIDs as intrinsic identifiers (equal to Git's object IDs for SHA-1 repositories, by a compatibility the standard
does not guarantee). *Lessons:* 91.5 percent of sources were unaltered at their upstream address after five years; the
oldest commit lacked 21.3 percent of its sources; travelling back in time runs old recovery code with old bugs; coverage
jumped only once the archive began loading sources ahead of need; containers lose "the source/binary correspondence".
*Verification* restated which bugs were current. *Sources:* https://arxiv.org/abs/2405.15516v1,
https://www.swhid.org/specification/v1.1/5.Core_identifiers/

