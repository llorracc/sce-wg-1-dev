# Exact definitions of canonical models

A proposed amendment to the documents that state the working group's purpose: the repository's README, the website's
landing page, the special-issue proposal, and, in this fork, the schemas' README and the ontology's.

**Status: APPLIED, 2026-11-04.** The owner asked for the proposal in the fork's session on the afternoon of 2026-11-04
and approved it the same afternoon, with the change to his formulation noted below. The three working-group documents
are amended on the fork's branch `exact-definition`, taken from upstream's main, and proposed to the group as
[econ-ark/sce-wg-1 pull request #14](https://github.com/econ-ark/sce-wg-1/pull/14), where the special-issue proposal's
wording awaits the co-author's reading. The fork's own documents, the schemas' README with its vocabulary,
`for-toolkit-authors.md` and the ontology's README, are aligned in the fork. Project B's optional sentence is offered to
the co-chairs in the pull request. The fork's copy of the landing page is behind upstream's by the primer commits of
2026-11-03 and is brought current when the pull request merges.

## The idea

For the models the project encompasses, the working group canonicalizes an exact definition of each. Exact means this:
a solution method is valid for the definition when, given unbounded computation, it converges to the same solution as
every other valid solution method given unbounded computation. Stated as definitions, the idea has three parts.

- A **solution method** for a model's definition is a procedure that approximates the problem the definition states,
  together with the way its approximation is refined: its grids, nodes, tolerances, interpolants and sample sizes.
- The method is **valid** for the definition when it approximates the stated problem and nothing else, and when
  everything it adds of its own can be refined without bound. A choice that survives the refinement, such as a fixed set
  of nodes standing for a continuous shock, changes the problem; the method is then valid for another definition, not
  this one.
- The definition is **exact** when every valid solution method, given unbounded computation, converges to the same
  solution as every other. That common limit is the model's solution. Equivalently, the definition leaves nothing to
  convention that the solution depends on.

The statement has an object form and a pairwise form. In the object form the definition determines one solution and
every valid method converges to it. In the pairwise form any two valid methods agree in the limit. The two are
equivalent, and each is useful: the object form says what the definition means, and the pairwise form is what can be
tested with two toolkits and no knowledge of the solution.

A **canonical** definition is the exact definition the group fixes for a model among the equivalent ones: the statement
to which every toolkit's files and calls are mapped, and against which every solution is judged. Two exact definitions
are equivalent when the valid methods of one converge to the solution of the other, which is the research themes'
denotational equivalence applied to a model.

For a definition to be exact it has to name three things: the objects that make up the solution (for a buffer-stock
model, the consumption rule, the stationary distribution and the value); the conditions under which those objects
exist and are unique; and the sense in which an approximation approaches them (uniform convergence of the rule on
bounded sets, weak convergence of the distribution, or convergence of named functionals). Without the third the
criterion has no meaning. Without the second it can fail for a reason that is not the definition's.

## Why it belongs in the purpose

1. **It makes the independent standard concrete.** The proposal's abstract says that without a statement of a model's
   meaning there is no independent standard against which to judge code an AI writes. An exact definition is such a
   standard: an implementation, whoever or whatever wrote it, either converges to the canonical solution or does not,
   and computation can tell which.
2. **It joins two research themes into one criterion for a model.** Well-posedness supplies the existence and
   uniqueness conditions; adequacy and convergence are what validity and exactness say about a method. The criterion is
   the model-class form of "equivalence, adequacy, convergence".
3. **It is testable, and the test locates gaps.** Two valid methods that converge to different solutions have found a
   convention the definition left unstated. That is the kind of result the closing comparison paper is to report.
4. **The project is its own test of the thesis.** The fork's adapters for HARK and dolo were written from the definition
   alone, the schemas and the stage files with the toolkits' documentation, by an AI, and the harness checks whether
   what they compute converges to the stated model's solution. If the definition suffices for that, it suffices for the
   group's purpose. The owner confirmed this reading on 2026-11-04
   ([the ruling](../schemas/records/rulings/2026-11-04_purpose.md)). The purpose documents should say that this is the
   test.

## The proposed wording

For each document, the current text and then the proposed text.

### The repository's README, first paragraph

Current:

> Working Group 1 of the Society for Computational Economics develops formal specifications of dynamic economic models
> and their solution and estimation methods. The group was formed at CEF 2026 in Venice and works with Econ-ARK and
> QuantEcon.

Proposed:

> Working Group 1 of the Society for Computational Economics develops formal specifications of dynamic economic models
> and their solution and estimation methods. For the models it takes up, the group fixes a canonical definition of each
> that is exact in this sense: every valid solution method, given unbounded computation, converges to the same solution
> as every other. The group was formed at CEF 2026 in Venice and works with Econ-ARK and QuantEcon.

### The landing page, against upstream's current version

The tagline under the title keeps its sentence, "Working Group 1 develops formal specifications of dynamic economic
models and their solution and estimation methods." The Vision paragraph gains a second paragraph after "While we do not
prescribe a single formalization or language, we aim for interoperability across different approaches.":

> For the models the group takes up, interoperability has an exact meaning. Each such model gets one canonical
> definition, complete enough that every valid solution method, given unbounded computation, converges to the same
> solution as every other: a method's own grids, quadratures and tolerances must vanish in the limit, and a choice that
> survives it changes the model. An implementation in any toolkit, written by a person or by a machine, is judged by
> whether it converges to that solution. Two implementations that converge to different solutions have located a
> convention the definition left unstated.

Optional, and the co-chairs' to decide since Project B is theirs: the Baseline Model Library's blurb, "The baselines
provide shared reference models for comparing implementations, numerical methods, and results across toolkits," becomes
"The baselines provide shared reference models, each with a canonical, exact definition, for comparing implementations,
numerical methods, and results across toolkits."

### The special-issue proposal

Four places. The document is co-authored and circulates, so these go to the co-author through the owner.

**The abstract,** after the sentence that defines a semantic ontology ("We call such a statement a 'semantic
ontology': ... the conditions under which that interpretation holds."), one sentence:

> For a model, such a statement is exact when it fixes the solution: every valid solution method, given unbounded
> computation, converges to the same solution as every other.

**The Proposed Special Issue,** the sentence "In addition to the semantic ontologies, the working group will write a
paper and assemble a community resource of canonical models and their ontologies" becomes "... a community resource of
canonical models, each with an exact definition, and their ontologies", and a paragraph follows it:

> A definition of a model is exact when it leaves nothing to convention that the solution depends on. We make this
> precise through solution methods. A solution method is valid for a definition when it approximates the problem as
> stated and nothing else, and when whatever it adds of its own, grids, quadratures, tolerances and interpolants, can be
> refined without bound; a choice that survives the refinement, such as a fixed set of nodes standing for a continuous
> shock, changes the problem. A definition is exact when every valid solution method, given unbounded computation,
> converges to the same solution as every other, and that common limit is the model's solution. The definition must
> therefore name the objects that make up the solution, the conditions under which they exist and are unique, and the
> sense in which an approximation approaches them. Exactness can be tested: an implementation, whoever or whatever wrote
> it, either converges to the solution or does not, and two valid methods that converge to different solutions have
> located a convention the definition left unstated. For each model it takes up, the working group fixes one exact
> definition as canonical, the statement to which every toolkit's files and calls are mapped and against which every
> solution is judged.

**The closing comparison,** the sentence "Each team will therefore state the conventions its own domain assumes, and
where two teams' ontologies disagree they will have located a point where the profession's conventions silently diverge
— the substance of the closing comparison paper" becomes:

> Each team will therefore state the conventions its own domain assumes. Where two teams' ontologies disagree, or two
> valid solution methods for one canonical model converge to different solutions, they will have located a point where
> the profession's conventions silently diverge, the substance of the closing comparison paper.

**The fifth research theme,** "Equivalence, adequacy, convergence: what preserves it", gains a fourth sentence after
"Convergence: a numerical approximation approaches it as grids and tolerances are refined.":

> Exactness: for a model, every valid solution method converges, given unbounded computation, to the same solution as
> every other, so that adequacy and convergence are judged against one object.

### The schemas' README, this fork's

The aim paragraph, now "The aim is to state a model so completely that any bug-free toolkit, given enough computation,
converges to the same solution as every other. The schemas say what the model is. They prescribe no numerical method:
grids, quadrature, tolerances and simulation sizes stay each toolkit's own choice.", becomes:

> The aim is a canonical, exact definition of each model: a statement so complete that every valid solution method,
> given unbounded computation, converges to the same solution as every other. The schemas say what the model is. They
> prescribe no numerical method: grids, quadrature, tolerances and simulation sizes stay each toolkit's own choice, on
> one condition, that the choice vanishes in the limit. A choice that survives it, such as a fixed set of nodes standing
> for a continuous shock, changes the model; the schemas read it as a model-changing setting, and the results file
> reports the effective member it produces. The schemas are tested by use: the adapters for HARK and dolo were written
> from the schemas and the toolkits' documentation alone, and the harness checks whether what they compute converges to
> the stated member's solution.

Three entries join the vocabulary:

- **Valid solution method:** a procedure that approximates a member's problem as stated and nothing else, every choice
  of its own refinable without bound. A toolkit at fixed settings is an approximation, not a method in this sense; its
  ladder, with its model-changing settings refined as well, is.
- **Exact definition:** a definition under which every valid solution method, given unbounded computation, converges to
  the same solution as every other. The families aim to be exact definitions of their members. A disagreement between
  two toolkits in the limit is a gap in the definition or a departure in one toolkit, and the toolkit's stone, read
  against the definition, says which.
- **Canonical definition:** the exact definition the working group fixes for a model: the hub to which every stone maps
  its toolkit.

### The ontology's README, optional

In "A semantic ontology and a schema", one sentence: "Each family of the schemas is meant as a canonical, exact
definition of the members it writes, a statement under which every valid solution method converges to one solution;
the conditions this ontology states are what make such a definition well-posed."

## Consequences

1. **Uniqueness is presumed, so the conditions are the price of admission.** The criterion speaks of the solution. A
   model with several solutions has no exact definition until the definition selects one. For the buffer-stock families
   the conditions are stated in the ontology and enforced by the checker as validity conditions. The criterion is
   therefore scoped to the models the project takes up, each with its class's well-posedness conditions; a modeling
   language, a toolkit or an empirical method is covered by the other research themes, and by this one only through
   the canonical models it carries.
2. **The sense of convergence has to be named.** For the buffer-stock families the results schema names the objects
   and the points, probabilities and functionals at which they are compared, and the reference-solution proposal names
   the distances. The purpose documents say only that a definition must name them.
3. **A toolkit at its defaults is not a valid method for the stated model.** Its fixed nodes or truncation survive the
   limit, so it is a valid method for its effective member. This is already how the schemas read a toolkit, through its
   effective-member block, and it is why the reference solution is compared to defaults rather than defaults to one
   another: the reference is a valid method taken far along its ladder, provisional because its remaining distance to
   the limit is estimated by refinement rather than proven.
4. **A disagreement needs a diagnosis, and the stone supplies it.** When two methods disagree in the limit, either the
   definition is inexact or one method is not valid, by a bug or by a convention it settled silently. The toolkit's
   stone, which says how the toolkit honors the definition, is what makes the disagreement attributable. Under this
   criterion the stones are not an accessory to the adapters; they are what turns a measured gap into a finding.
5. **The criterion extends to estimation.** For an estimation exercise the object is the estimator, and a valid
   estimation method is one that, with the data fixed and unbounded computation, converges to the same estimate as every
   other. The loose inner-loop tolerance of the proposal's example is a method that stopped being valid. The
   estimation of a published paper's model, with the HAFiscal-Latest repository since 2026-11-04, is the case of this.
6. **Vocabulary in the fork aligns.** "Bug-free toolkit, given enough computation" becomes "valid solution method, given
   unbounded computation" in the two documents that say it, the schemas' README and
   [`for-toolkit-authors.md`](https://github.com/llorracc/sce-wg-1-dev/blob/b42e4b5a85e19fa7bbb4cf0ebc50aeb083f99d60/schemas/for-toolkit-authors.md), since a bug and a silently settled convention are the
   same thing to the criterion, a departure from the definition, and the method, not the toolkit, is what converges.
   "True model", the fork's name for the stated model as against a toolkit's effective member, stays: it names the
   thing the canonical definition defines.
7. **What it does not change.** No numerical method is prescribed: the criterion is about limits, not routes. The stones
   stay hub and spoke. Project B's library is untouched unless the co-chairs take the optional sentence.
8. **How it reaches the group.** The README and the landing page by a pull request from this fork, after the fork's
   landing page is brought current with upstream; the special-issue proposal by the co-authors' agreement; the fork's own
   documents in the commit that applies the proposal, with the records.
