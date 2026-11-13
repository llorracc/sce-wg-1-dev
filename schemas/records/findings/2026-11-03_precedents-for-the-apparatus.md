# Precedents for the apparatus: six families of model and software intercomparison

Researched on 2026-11-03 at the owner's request, as the ground for [`schemas/participation.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/participation.md),
and proposed with it. Each family is described by what it is, how it is organized, what it establishes
for this project and what it does not. Sources are addresses that were fetched during the research; addresses that could
not be fetched are left out, and a claim that rested only on an unfetched page is dropped or marked.

## Climate model intercomparison

What it is: CMIP, from a single archive in CMIP3 to a federated one in CMIP5, a mandatory entry card plus endorsed
projects in CMIP6, and a continuous entry card with community projects on their own timelines in CMIP7; with CMOR as the
reference writer, PrePARE and the CF checker as validators, the CF conventions and JSON vocabularies as the format,
input4MIPs forcings and obs4MIPs references in the output's own format, ES-DOC for documentation, and ESMValTool and PMP
for evaluation. How it is organized: a panel designs and endorses experiments, an infrastructure panel owns the technical
specifications (created in 2014 after a position paper argued volunteer-kept standards would not scale), and an
international project office opened in 2022; a joint decision log of the panel and the infrastructure panel is public,
listing proposals, the meeting that discussed them and whether they were accepted (who maintains the log was not
confirmed; the project office's site could not be fetched during the research); CF changes by moderated issue with a comment
window, named supporters and one release a year; vocabularies promise never to impair access to published data; datasets
are versioned and retracted, never edited.

Documentation has been required since before CMIP7: CMIP5 required the Metafor documentation system; Eyring et al. 2016
say CMIP6 modeling groups are required to provide documentation following a common template, and Pascoe et al. 2020 say
ES-DOC use is required for CMIP6 models and ensembles. What CMIP7 adds, per Dunne et al. 2025, is a short essential
model documentation, a high-level description required of every participating model. Pascoe et al. record that CMIP5's
documentation arrived too late to be of use and that the tools were difficult to use.

What it establishes for us: a small mandatory entry card plus optional tiers lets groups join at the level their
resources allow and keeps the archive comparable across phases; standards backed by software and enforced at the gate
are checked by a tool, not by reviewers; verification at entry is structural and comparison happens downstream, by the
organizer's packages, because the models are the objects of study; references and inputs in the output's format let one
evaluation path consume everything; documentation is required on a common template with the submission, and the lesson
of CMIP5 is that documentation collected late through hard tools is documentation that arrives too late. What it does
not: it certifies no number, has no closed forms and no reference solution, screened no model at entry (which produced
the hot-model problem), and its one unreadable normative artifact, the attributes document behind a sign-in wall, is the
nearest analogue to a stage file in a language with no public documentation and is recorded as a failure. Reruns are
infeasible there; here a solve takes minutes.

## Systems biology model and simulation exchange

What it is: SBML as the public model format with reference libraries; SED-ML for the experiment; KiSAO, an OWL ontology
of algorithms, and SBO for annotation; the SBML Test Suite with, per case, the model, a script-generated settings file,
expected results, a plot and tags, and a database where tool authors upload results; OMEX archives; BioSimulators, which
put 21 tools behind one command line and one container with a capabilities file. How it is organized: elected editors
per standard, package proposals needing two independent implementations, term requests by issue, a coordination board
with no legal form.

What it establishes: a conformance suite whose expected results depend on no single tool (closed forms for about a fifth
of cases, otherwise agreement of two tools), with one tolerance formula per case and a public ledger, turned support into
a testable claim; a reference library made parsing free for participants; a thin convention (one command, one archive in,
one report out, one capabilities file) brought many tools in and surfaced hundreds of bugs; and a discipline of outcomes
in BioSimulators' test suite: a case whose formats or algorithms the capabilities file does not claim is skipped, a value
outside the tolerance (a relative tolerance of 1e-4) fails, and a runtime failure is raised as an error by default, with
a warning only where a case's own settings choose it. What it does not: its self-reported ledger shows passes and not
discrepancies and a third of its entries are unreleased; curated experiment files carried mistakes nobody caught until a
validator read them: Smith et al. 2025 found that only about half of BioModels' entries had SED-ML files and that almost
all of those had at least one mistake, however minor, that made them impossible to run, and the SED-ML validator's
authors used it to correct the official example files; and reproducibility was poor regardless of the standards, 49% of
455 published models not reproducible from the manuscript, a further 12% only with effort, and 37% never. Whether
anything required the standards' use is not stated in the sources read and is not claimed here.

## Co-simulation and tool interoperability

What it is: FMI, a free standard with public schemas and headers, 290 or so tools, hand-coded Reference FMUs with a
reference simulator and several validators; the Cross-Check, in which vendors uploaded models with their own reference
results and importers filed pass or fail markers; SSP for system structure. How it is organized: a Modelica Association
project with a steering committee of vendors and users, rules fixed in advance and revised at most yearly, trademark
guidelines in place of certification, semantic versioning in which minor versions add only ignorable content.

What it establishes: a small public container and interface with reference implementations lets a vendor self-test
before any other artifact exists; evaluation burden on participants with the organizer limited to rules, publication and
arbitration is what made vendors take part; layered standards kept the core small; a vendor could remove its own entries.
What it does not: the vendor-run central cross-check became unmanageable and was archived in 2022, its importer proof
reduced to self-assessed markers; the oracle was the exporter's own result, never an independent truth; vendor-chosen
test models left coverage incomplete; no accuracy ranking was ever published and certification was rejected for want of
resources and objectivity. The lesson is the one our ledger must heed: a results store filled by participants hollows
out.

## Benchmark libraries and solver competitions

What it is: SMT-LIB with its library of problems carrying a status, source, license and category, on which SMT-COMP is
based and run on a published container with a published selection script; the MiniZinc Challenge, entered as a
container, scored by Borda count; CUTEst and SIF, COPS with its analyzer, Mittelmann's rerun sets; the Bari test set of
initial value problems with reference end-point solutions and work-precision diagrams, in the format of Hairer and
Wanner's test set; MLPerf with reference implementations, a mandatory load generator, divisions, peer review and audits.
How it is organized: steering committees and yearly organizers who publish rule changes with rationale and a comment
date, and may remove faulty benchmarks; an organizer's own entry cannot win: SMT-COMP's rules let the organizers enter
other solvers for comparison but make only submitted solvers eligible to be designated winners, and the MiniZinc
Challenge's rules make the organizers' own systems ineligible for prizes while their results still enter the scoring. No
recusal clause was found.

What it establishes: a public format read directly by solvers lets a library grow without coordination; expected answers
stored with each problem make correctness a pass or fail check separate from any ranking, with wrong answers penalized
heavily; low entry cost (one JSON file, one container, one driver) widens the field; each summary's limits are stated
(profiles identify only the best solver; adding a solver reorders the rest; some competitions refuse a summary score);
execution limits are published with the results. What it does not: selection sensitivity changed winning orders;
libraries decay without volunteers; commercial vendors withdrew from Mittelmann's benchmarks (results for CPLEX, Gurobi
and XPRESS removed after a 2018 action by INFORMS and demands by IBM and FICO; Gurobi withdrew in August 2024; MindOpt in
December 2024), Gurobi stating as its reasons test-set sizes out of line with best practice, a validation and
over-tuning detection burden beyond the administrators' resources, machine-learning tuning and diminished utility. A
ranking as such is not named among them; this record reads the episode as the cost of a contest that the organizer could
not police, and as support for the no-timings rule here.

## Computational-economics model comparison

What it is: Taylor and Uhlig's 1990 exercise on a stochastic growth problem in ten parameter cases; Judd's unit-free
Euler residual in base-10 logarithm, later integrated against the computed ergodic distribution; the JEDC suite of 2010
(a Krusell-Smith economy with organizer-supplied shocks, initial distribution and simulation procedure) and of 2011 (a
multi-country model in thirty specifications with a standalone test bench fed only each team's policy function); the
Macroeconomic Model Data Base of over 150 models as Dynare mod files behind a four-variable interface; Econ-ARK's REMARK
standard of a reproduction script in a pinned, tagged environment. How it is organized: working groups and special
issues with one paper per algorithm; the 2011 suite's comparison paper co-authored by participants (Kollmann, Maliar,
Malin and Pichler), the 2010 suite's comparison paper (Den Haan, JEDC 34(1)) single-authored by its organizer; a funded
group for the database; pull-request review for REMARK.

What it establishes: a small model with fixed parameter cases keeps entry cheap; one bench with identical points, shocks,
integration rule and precision, fed only a policy function, makes every difference attributable to the policy function;
the unit-free Euler residual is the shared currency of accuracy; where the information lies depends on the suite: in the
2011 suite all methods delivered similar unconditional moments and the differences were in the tails, bad states and
higher cross-sectional moments, while in the 2010 suite the unconditional means and standard deviations of individual
variables were themselves among the larger differences (individual consumption differed by up to 11.4% between the two
most distant algorithms) and only the correlations were similar; one reproduction command a reviewer can run is a
requirement that holds. Whether co-authorship was what secured participation is not stated by either comparison paper
and is not claimed here. What it does not: self-drawn shocks and self-reported timings made the 1990 paths incomparable
and the organizers could not say who won; reference solutions were themselves uncertain; the bench held one hand-written
module per solution, which does not scale; and the test bench's published address is dead (the Dynare wiki page the
paper cites now returns a 404), which argues for a deposit under a DOI. The JEDC papers themselves were read from a
participant's own site, where the 2010 comparison's link was dead on 2026-11-03; its DOI is in the sources.

## Software architecture for multi-implementation interchange

What it is: LLVM's one intermediate representation between many front and back ends; Pandoc's reader, AST, filter and
writer pipeline, a filter being any program on stdin and stdout; the Language Server Protocol's capabilities exchange
over JSON-RPC; the web-platform-tests suite with results archived on a public dashboard and a yearly scored program;
the JSON Schema Test Suite with Bowtie, a meta-validator that drives each implementation in a container through a
four-command protocol and publishes a report; the SBML suite again; Unicode's normalization test file reissued per
version; NIST's statistical reference datasets with values certified at 128-bit precision by two algorithms and a
four-digit criterion; the retired Acid tests; the W3C's and IETF's requirement of independent interoperable
implementations.

What it establishes: a small, public, language-neutral spoke interface means a newcomer writes a wrapper, not a port;
expected results owned by the organizer and runnable by anyone; one explicit pass formula, with leave to report a skip or
a different minimum without being failed; the organizer runs the comparison and publishes the dashboard, so participants
receive a bug list rather than homework; versions are directories and files, never edits, and old versions freeze in
place; tests laid out to mirror the specification so a failure names the clause; independence from incumbents, since a
test suite built to break particular implementations (Acid3) was disowned. What it does not: hub churn (LLVM admits
invasive changes force updating every pass); optional buckets that mix reasons for being optional; registries where one
faulty plugin breaks the host.

## What the six have in common

Every normative format is public and versioned; every organizer ships a writer or a reference library and a validator;
every participant supplies one artifact they already have plus a short self-description; verification at entry is
structural or against values the organizer owns; comparison is downstream, by the organizer's code, published with its
limits stated and its execution limits named; documentation is required on a template with the submission; an
organizer's own entry is marked and wins nothing; a participant can withdraw; and the schemes that let participants run
or report the comparison themselves were the ones that collapsed. Nothing in the six reports the model actually solved in
representation-free numbers, which is this project's own contribution and the thing a newcomer most needs explained.

## Sources

Fetched during the research of 2026-11-03. Pages that could not be fetched (the COPS site, Hairer's test-set page, the
MiniZinc Challenge's philosophy paper, the CMIP project office's site, ACM Queue) are not listed, and nothing above rests
on them alone.

- Eyring et al. 2016: https://gmd.copernicus.org/articles/9/1937/2016/gmd-9-1937-2016.xml
- CMIP6 participation guide: https://pcmdi.llnl.gov/CMIP6/Guide/modelers.html
- CMOR: https://cmor.llnl.gov/ and PrePARE: https://cmor.llnl.gov/mydoc_cmip6_validator/
- CF conventions: https://cfconventions.org/ and contributing rules: https://github.com/cf-convention/cf-conventions/blob/main/CONTRIBUTING.md
- CMIP6 vocabularies: https://github.com/WCRP-CMIP/CMIP6_CVs
- Juckes et al. 2020, the data request: https://gmd.copernicus.org/articles/13/201/2020/
- Pascoe et al. 2020, ES-DOC: https://gmd.copernicus.org/articles/13/2149/2020/
- Balaji et al. 2018: https://gmd.copernicus.org/articles/11/3659/2018/gmd-11-3659-2018.xml
- Dunne et al. 2025, CMIP7: https://gmd.copernicus.org/articles/18/6671/2025/
- Righi et al. 2020, ESMValTool: https://gmd.copernicus.org/articles/13/1179/2020/
- Lee et al. 2024, PMP: https://gmd.copernicus.org/articles/17/3919/2024/
- Hausfather et al. 2022: https://media.nature.com/original/magazine-assets/d41586-022-01192-2/d41586-022-01192-2.pdf
- WIP governance proposal 2014: https://wcrp-cmip.github.io/WGCM_Infrastructure_Panel/Papers/standards-governance.pdf
- obs4MIPs: https://pcmdi.github.io/obs4MIPs/ and input4MIPs: https://pcmdi.llnl.gov/mips/input4MIPs/
- SBML Test Suite case organization: https://sbml.org/software/sbml-test-suite/docs/test-case-details
- SBML Test Suite evaluating outputs: https://sbml.org/software/sbml-test-suite/docs/evaluating-outputs
- SBML results database: https://sbml.bioquant.uni-heidelberg.de/Simulator
- SBML editor elections: https://sbml.org/documents/process/editor-elections and package process: https://sbml.org/documents/process/level-3-process
- Keating et al. 2020, SBML Level 3: https://pmc.ncbi.nlm.nih.gov/articles/PMC8411907/
- SED-ML: https://sed-ml.org/ and KiSAO: https://github.com/SED-ML/KiSAO/
- SED-ML validator, Shaikh et al.: https://arxiv.org/abs/2106.00844
- OMEX specification: https://github.com/combine-org/combine-specifications/blob/main/specifications/omex.md
- BioSimulators interfaces: https://docs.biosimulations.org/concepts/conventions/simulator-interfaces/
- BioSimulators capabilities: https://docs.biosimulations.org/concepts/conventions/simulator-capabilities/
- BioSimulators test suite: https://github.com/biosimulators/Biosimulators_test_suite
- Shaikh et al. 2022: https://academic.oup.com/nar/article/50/W1/W108/6595873
- BioModels verification, Smith et al. 2025: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013239
- Tiwari et al. 2021, reproducibility of models: https://www.biorxiv.org/content/10.1101/2020.08.07.239855
- Waltemath et al. 2020, COMBINE: https://pmc.ncbi.nlm.nih.gov/articles/PMC7756615/
- FMI: https://fmi-standard.org/ and the 3.0 specification: https://fmi-standard.org/docs/3.0/
- FMI Cross-Check rules: https://raw.githubusercontent.com/modelica/fmi-cross-check/master/FMI-CROSS-CHECK-RULES.md
- FMI Cross-Check repository: https://github.com/modelica/fmi-cross-check
- Cross-Check rules 2014: https://wiki.eecs.berkeley.edu/ptexternal/uploads/Main/FMI_Cross_Check_Rules_v3_2014_07_31.pdf
- Updated Cross-Check rules 2020: https://fmi-standard.org/news/2020-10-27-updated-cross-check-rules/
- FMI Implementers' Guide: https://modelica.github.io/fmi-guides/main/fmi-guide/
- FMI status 2024: https://fmi-standard.org/assets/literature/2024-05-28_FMI_Status_Outlook_Colloquium_Martin_Otter.pdf
- Reference FMUs: https://github.com/modelica/Reference-FMUs and FMPy's validation: https://raw.githubusercontent.com/CATIA-Systems/FMPy/main/src/fmpy/util.py
- Gomes et al. 2020: https://2020.american.conference.modelica.org/proceedings/papers/Modelica2020US_paper_1.pdf
- SSP: https://ssp-standard.org/docs/main/
- SMT-LIB: https://smt-lib.org/ and benchmark submission: https://github.com/SMT-LIB/benchmark-submission
- SMT-COMP 2026 rules: https://smt-comp.github.io/2026/rules.pdf and solver submission: https://smt-comp.github.io/2026/solver_submission/
- The 2014 SMT Competition report: https://user.it.uu.se/~tjawe125/publications/cok16the.pdf
- MiniZinc Challenge 2025 rules: https://www.minizinc.org/challenge/2025/rules/ and FlatZinc: https://docs.minizinc.org/en/stable/fzn-spec.html
- CUTEst: https://github.com/ralna/CUTEst
- Dolan and Moré: https://arxiv.org/pdf/cs/0102001 and Gould and Scott: https://numerical.rl.ac.uk/media/people/nick-gould/GoulScot16_toms.pdf
- COPS 3.0 report: https://optimization-online.org/wp-content/uploads/2004/05/871.pdf
- Mittelmann: https://plato.asu.edu/bench.html and Gurobi's statement: https://www.gurobi.com/resources/blog/an-update-on-gurobi-s-participation-in-the-mittelmann-benchmarks
- Bari test set: https://archimede.uniba.it/~testset/ and prologue: https://archimede.uniba.it/~testset/report/prologue.pdf
- MLPerf inference rules: https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc
- MLCommons submission rules: https://github.com/mlcommons/policies/blob/master/submission_rules.adoc
- MLPerf Training paper: https://arxiv.org/pdf/1910.01500
- Taylor and Uhlig 1990: https://www.nber.org/system/files/working_papers/w3117/w3117.pdf
- Den Haan's suite page: http://www.wouterdenhaan.com/datasuite.htm and tasks document: http://www.wouterdenhaan.com/suite/ModelB.pdf
- Den Haan, Judd and Juillard 2011: https://www.robertkollmann.com/DEN_HAAN_JUDD_JUILLARD_INTRO_JEDC2011.pdf
- Juillard and Villemot 2011: https://www.robertkollmann.com/JUILLARD_VILLEMOT_TESTBENCH_JEDC2011.pdf
- Kollmann, Maliar, Malin and Pichler 2011: https://www.robertkollmann.com/KOLLMANN_PUBL_MALIAR_MALIN_PICHLER_JEDC_2011.pdf
- Den Haan 2010, JEDC 34(1) 4-27, the Krusell-Smith comparison: https://doi.org/10.1016/j.jedc.2008.12.010 (Kollmann's site links a copy, `DEN_HAAN_MODEL_COMPARISON_JEDC_2010.pdf`, which returned 404 on 2026-11-03)
- Aruoba, Fernández-Villaverde and Rubio-Ramírez: https://economics.sas.upenn.edu/sites/default/files/filevault/working-papers/04-003.pdf
- Macroeconomic Model Data Base: https://www.macromodelbase.com/ and user guide: https://www.macromodelbase.com/files/userguide.pdf
- Dynare, the model file: https://www.dynare.org/manual/the-model-file.html
- REMARK: https://econ-ark.github.io/REMARK and its standard: https://raw.githubusercontent.com/econ-ark/REMARK/master/STANDARD.md
- LLVM in AOSA: https://aosabook.org/en/v1/llvm.html and developer policy: https://llvm.org/docs/DeveloperPolicy.html
- Pandoc filters: https://pandoc.org/filters.html
- Language Server Protocol: https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/
- web-platform-tests: https://web-platform-tests.org/ and Interop: https://github.com/web-platform-tests/interop
- JSON Schema Test Suite: https://github.com/json-schema-org/JSON-Schema-Test-Suite and Bowtie: https://docs.bowtie.report/en/stable/implementers/
- UAX 15: https://www.unicode.org/reports/tr15/
- NIST StRD: https://www.itl.nist.gov/div898/strd/nls/nls_info.shtml and background: https://www.itl.nist.gov/div898/strd/general/bkground.html
- acidtests.org: https://acidtests.org/
- W3C Process: https://www.w3.org/policies/process/ and the Tao of IETF: https://www.ietf.org/about/participate/tao/
