# A redesign of HARK's expectation machinery: the laws first-class, the method chosen at solve time

**Status: PROPOSED, 2026-11-05 in the afternoon, on the owner's request of 13:46:09 EST, with the HARK, HARK-dev and
HAFiscal-Latest sessions consulted the same afternoon and their accounts below.** Nothing here changes HARK or the
schemas: the proposal is for the owner, and what it decides is his. It is written to be public: the sessions'
unposted work is described by what it does, their private records are not cited, and of the owner's review of
2026-10-29 only what HARK-dev said may be cited is used, in substance.

## The request, in substance

The continuous expectation and the solver that uses it have been retrofitted onto a structure in which a solver sees
only the atoms of a discretized distribution. That keeps today's behavior intact but has reached the point where a
thorough redesign may serve better: one in which a solver can be told, when it is called, whether to take its
expectations by a discrete method or a continuous one, so that the two methods' results can be compared directly on
the same laws, and so that an adapter can instruct HARK to solve a model either way.

## What the working group's harness needs of it

These are fixed by the schemas and the rulings, whatever the architecture.

- **The method is the adapter's to name, per precision level.** A method file names, on the stage's expectation
  operator `E_ψ_θ_j`, the method's tag, `!quadrature` for nodes or pieces that approximate the laws and `!sum` only
  where every law is finite, with HARK's routine as the handler and the settings the handler reads: for the discrete
  method the node counts and their placement, for the continuous one the nodes per piece and where the pieces split
  (`schemas/bst/model.md`, "Method targets"; `schemas/numerics.md`). The diagnostics' expectation, which the Euler
  residuals use, must differ from the household's. So the redesign's switch must be settable from outside a solve,
  per run, with its settings recorded.
- **The effective member is what was solved.** A results file reports the expectations under the toolkit's own
  approximation of the laws, the lowest values, the mass at the worst income and the derived parameters
  (`schemas/bst/results.md`, "The effective member"). Under the discrete method these are the atoms'; under the
  continuous method they are the stated laws' own, to the quadrature's error, with the lowest values the infima. The
  redesign must make both reportable from the same object, and the landing mass the laws' in both.
- **The representation is the toolkit's** (the ruling of 2026-11-02): how HARK represents the laws is HARK's choice,
  stated in its stone and its method file, never prescribed by the harness. The redesign therefore decides HARK's
  representations; the harness only asks that each be named and refinable.
- **Two methods in one toolkit are two modes**, keyed with the toolkit in the registry and compared by the comparator
  as two toolkits would be (`schemas/registry.md`, "Modes of solution", the ruling of 2026-11-04): the same laws, the
  same member, two results files, their distances on the experiment's quantities, and the checks between them. That
  is the direct comparison the owner asks for, and it tests HARK's consistency and the definition at once.
- **Both methods must be valid methods** under the exactness criterion (`project-a/exact-definition.md`): every choice
  of theirs refinable without bound, the node count of the discrete method and the pieces and nodes of the continuous
  one, with no default that is not itself refinable. The test is convergence: each method's results fall with its
  level, and the two methods approach each other as both are refined, which the experiment's checks `falls_with_level`
  and `compare: toolkits` can state as written.
- **The reference solution** (the ruling of 2026-11-04 at 06:23:39) is to come from the continuous methods at very
  high precision; under the redesign it is HARK's continuous method at its finest settings, with the point-mass
  landing right, and its certified errors from the convergence in the settings.

## The architecture: the HARK session's account

Received 2026-11-05 in the afternoon. Facts, judgments and what was not checked are kept apart as it marked them; its
unposted prototype is described by what it does.

**Two bounds on the design.** First, the owner's review of the concavity group on 2026-10-29 already chose a shape,
recorded in HARK-dev's private records: a separate solver under an experimental tier, selected through an options
registry with profiles for the classic, the advanced and the future behavior; one private body shared by the separate
solver and the classic one; the classic standard-consumer solver kept as on main, with no continuous option on the
classic agent and the infimum limit only in the separate solver; #1862 closed, its limit opened anew; the registry and
the tier first. None of the registry, the tier or the separate entry exists on any branch. The request of 13:46:09
goes further, the method chosen on the fly per run by a user or an adapter, so the redesign either fits inside that
shape or supersedes it, which is the owner's decision. Second, where the retrofit shows in the prototype: the
continuous solver reads the laws back out of the discretized object's records and raises when they are absent; the
method is a flag that swaps the one-period solver; inside one shared body the worst-income probability, mean income,
the grid's anchor and the limit each switch on that flag; and the simulation still draws atoms after a continuous
solve, in both simulators.

**The interface (its judgment).** One income-process object per period, and per Markov state, that owns the model's
income laws and not their atoms. Its inputs are the permanent-shock law and the employed transitory law, any HARK
distribution, continuous, truncated, a mixture, a point or a discrete law, and the unemployment event as the two
parameters, never a transitory atom, as the owner ruled on 2026-10-20; bounds and end behavior come from the laws. Its
expectation takes the integrand, its arguments and a method chosen at call time, a small settings object: the
discrete method with its counts, placement, tails and the source of the limit, which discretizes the laws exactly as
today's constructors do, caches the result per settings and sums as today; or the continuous method with its nodes
per piece per law and its split rule, the generic quadrature, Gauss–Legendre in pieces in each law's own normal
coordinate, split at points the caller gives as functions of the earlier variables, mixtures component by component
and discrete laws by their atoms, four nodes a piece by default. The model-specific part, the transition of resources
and the mapping of next period's kinks to each law's cut points, belongs to a beginning-of-period function in each
model's module, not to the object. What the solver asks of the object besides expectations is the model's answer, the
same under either method, with the discrete method's own available on request: the natural limit by the sign rule;
whether the limit binds without a kink, which is yes when a mass sits at the landing or when densities sit there on
the laws that set it with risk aversion at least their number; the landing mass, branch by branch, the employed law
weighted 1 − ℘ and the unemployed point weighted ℘, with the permanent shock's end chosen by the same sign; mean
income for human wealth; the worst-income mass for the weak return impatience factor; the bounds; and draws, from the
laws under the continuous method and from the atoms under the discrete one, so that a simulation matches its solve.
The Markov solver takes one object per state, with #1858's function that takes each next state's expectation at the
current state's asset points as the call site and a guard for a zero mass where the combination divides by it; the
labeled solver could be served by a wrapper, anything beyond that unchecked; the simulator takes draws, while the
transition-matrix route needs atoms, so under the continuous method the population step needs a discretization of its
own, recorded and refinable.

**How the solvers change (its judgment, on measured facts).** The prototype's shared body branches on the method at
the worst-income probability, mean income, the limit, whether the rule kinks, the unconstrained bottom slope, the grid
and the three expectations; under the discrete method every result is bit-identical to main, by the suite and by a
test. A solver written against the interface computes the limit from the object, the constraint in force, whether it
kinks, the landing mass and from it the MPC at the limit, one with a kink and 1 − p^(1/ϱ) Þ_R without, the cubic's
slope there the largest of that, the first segment's secant and the MPC at the first knot; takes the grid from a grid
rule; takes the three beginning-of-period expectations from the model's function under the chosen method; proceeds
by the endogenous grid method as today; and records the kinks, the method and its settings on the solution. The
discrete method at today's settings keeps the atoms' limit, the grid anchored there, the landing mass from the atoms'
smallest product, no splits and the cached discretization, so the classic path stays bit-identical. The continuous
method needs from the interface the laws and the event, each law's ends, coordinate and steps, next period's kinks and
knots, a grid anchored at the binding constraint with a knot there, the landing mass, and points placed near a smooth
natural limit, whose constants are tuned rather than derived. The grid rule must be a setting of its own, apart from
the expectation method. The method is both a type parameter, the default, and an argument of the solve that
overrides it for one solve without changing the agent, each solution carrying its method and settings, so that an
adapter sets it per run and a user compares two solves of one agent.

**Compatibility and migration (its judgment).** What survives as the model's statement: the standard deviations of
the logs, the truncation bounds, the unemployment event's probability and income with their retirement versions, and
the retirement date. What becomes method settings: the atom counts, the quadrature nodes, the placement and tail
options. What becomes derived: the three distribution objects, the discrete method's discretization of the laws,
built on demand, cached and readable as today. An income distribution the user assigns is a discrete law in its own
right, both methods then giving the same answer; if it records its laws as HARK's constructors do, the object recovers
them. Of the pull requests: #1861 and #1863 stay the foundation; #1862 is subsumed in substance by the object's limit,
its code moving into the object, the owner's choice of 2026-10-29 to close it and open the limit anew not yet made;
#1858 stays, a correctness fix and the Markov call site; #1859 is needed only for persistence, which is the class
decision; #1860's newborn convention is still needed, whether through it or not; #1855 and #1827 are independent.
Issue #1869 is not the redesign in disguise: it retrofits a flag onto the existing solver with the laws read back
from records, though most of its pieces carry over unchanged, the quadrature, the three continuous expectations, the
shape-preserving cubic, the truncated shocks, the mixture, the natural-limit logic and the placed points; what changes
is who owns the laws.

**Comparison by construction (measured today).** The standard consumer, infinite horizon, laws at three standard
deviations, linear interpolation, the default grid of 48 points, the continuous method at 8 nodes a piece as the
reference, the measure the largest gap in consumption from the limit to m = 20. With the natural limit binding
(℘ = 0.05, no income while unemployed, no artificial constraint): 1.28·10⁻² at 7 atoms per shock, 4.32·10⁻³ at 15,
1.45·10⁻³ at 31, 4.94·10⁻⁴ at 61, about N^(−1.5). With an artificial constraint at zero and no unemployment:
1.40·10⁻², 4.53·10⁻³, 1.45·10⁻³, then 1.61·10⁻³ at 61, the gap stopping, which it attributes, unisolated, to the two
paths' grids: the atoms' anchored at the atoms' natural limit with the kink found by a crossing, the continuous one
anchored at the constraint with a knot there. The continuous method against itself, 4 against 8 nodes a piece,
differs by 5·10⁻⁸ to 7·10⁻⁸ in both cases. What to record (its judgment): the method and every setting, for the
discrete one the counts, placement, tails, endpoints and limit source, for the continuous one the nodes per law, the
split rule with its constants, the corner rule and the placed points' constants; the grid rule and the grid, the
interpolation, the tolerance and HARK's version; the effective member, the atoms and probabilities used and the limit
they imply under the discrete method, the laws with their bounds under the continuous one, and in both the event,
the limit used, whether it bound with or without a kink, and the landing mass. What both report: the rule and its
derivative at the requested points from the interpolant, the value through its inverse, the lower limit, the kinks,
the three limiting values, the landing mass, the condition factors, and Euler residuals at the requested points
computed with one reference expectation, the continuous method at a high node count, never the method's own, so
that they compare across methods. The test: on a common grid rule, refine each method's settings one at a time and
without bound, the discrete method's counts, the continuous method's nodes and the grid, and require the gap to fall
with each refinement, while the limit, the landing mass and the top MPC agree exactly, being the model's and not the
method's.

**Where it lives (its judgment).** A new class on the new machinery with the old types untouched is the safer route
and fits the choices of 2026-10-29: the classic path unchanged, the advanced one in the experimental tier, a shared
body. Its costs are a second entry point, users having to opt in, and tests enforcing that the shared body keeps the
classic path bit-identical. Changing the standard consumer in place breaks more: the kinked-return type hands off to
its solver when its two rates coincide and the New Keynesian type calls it with defaults of its own; nine subclasses'
pre-solve does not call the standard consumer's; the discretized distribution is read directly by the condition
checks, both simulators, the transition-matrix route and the labeled solver; and sixteen files on main sum over their
own distributions, about thirty one-period solvers among them. The operator itself is generic: the quadrature beside
the existing expectation in the distributions module, the income-process object beside the income constructors, the
beginning-of-period function in each model's module, all reached through the experimental tier and the registry until
promoted. HARK-dev may want the operator in the experimental tier from the start, a disagreement to show the owner.

**Size and order (its judgment).** New code with tests: the income-process object and the method settings, 500 to 700
lines plus about 400 of tests; the expectation dispatcher by method, about 100; the solver body against the interface
and the new class, 600 to 800; the Markov route on #1858, 200 to 300; the comparison tests and a notebook, 300 to 500.
About two thirds of the solver-side code carries over from the prototype. The order: #1861 and #1863; the registry and
the experimental tier if the order of 2026-10-29 stands; the generic quadrature with the dispatcher; the income-process
object, with a test that the discrete method at today's settings reproduces today's distribution bit for bit; the
solver body and the new class with the comparison tests; the cubic, independent, at any point; the Markov route, #1858,
then the per-state objects, then persistence if wanted; simulation by method, and later promotion to core and the
default's change. Not checked: the labeled solver beyond its imports, the fast solver that works on arrays of atoms,
the continuous method's cost on fine grids, how the model-file simulator would take a law, and HAFiscal's needs.

## The distribution, the simulation and the model file: the HARK-dev session's account

Received 2026-11-05 in the afternoon, from an export of HARK's main at 4c285e86 unless marked; facts, judgments and
what was not checked kept apart as it marked them, and what it marked private left out.

**A correction to the brief's premise.** Monte Carlo draws do not come from the laws. On main the standard consumer's
draws and the model-file simulator's both draw the discretized object's atoms, so a draw, a transition matrix and a
solver expectation already read one object through its atoms; the unposted continuous path changes only the solver,
reading the laws the discretized object records beside its atoms, while every draw, matrix and Jacobian still reads
the atoms. That split is what a redesign has to close.

**The stationary distribution.** The model-file route quasi-simulates each period from every node of the arrival
grid, a shock event splitting each probability blob over the atoms, the period's dynamics running on the blobs, and
Young's lottery putting each landing on the two neighboring nodes; the transition is conditioned on survival and the
decedents' mass replaced by the newborns' arrival distribution; the income measure is a post-weighting of each blob by
its realized growth, refused when growth outpaces mortality, one of three implementations of the same tilt in HARK;
the steady state is the leading eigenvector of a dense transition. Its judgment: the distribution's method is a
setting of its own, not the solver's, with three values, the solver's own atoms, which is the discretized model end
to end and undefined for a continuous solver; the same laws discretized more finely for the distribution alone, which
fits today's machinery; and transition weights integrated against the laws. For results compared directly, hold the
distribution's method fixed and vary only the solver's, else the comparison mixes two approximations; and when a
simulation is checked against the matrix, both use the same distribution. The laws-based weights can be built
generically, the landing being nondecreasing in the transitory shock for fixed arrival state and permanent shock, so
that each continuation cell's preimage is an interval found from the solution's own endogenous points, the lottery's
weight linear in the shock wherever the rule is, and its expectation needing only the law's distribution function
at the piece ends and its first partial moment on each piece, a point mass evaluated as itself, the permanent shock
by Gauss–Legendre in its normal coordinate; designed, not built or measured. That builder does not fit inside the
event-by-event quasi-simulation, which expands the blobs before the rule runs: it is a second builder for models
whose period map is monotone in a shock, the standard consumer and its Markov kin. The settings enter as an argument
of the matrix construction, are stored on the simulator and recorded with each result; the transitions are stored
sparse; the income measure's tilt is never written back into the object the solver reads; mortality with newborns
needs survival by period and state with its timing stated once, the newborns' arrival distribution, the newborn's
first-period rule and, from the object, the first-period law by branch name.

**The simulator.** Newborns are stated in four places on main, the simulate method, the model files, the legacy
New Keynesian route and two mixins, with different defaults; measured, the distribution function of resources at one
differs by the newborn's flag in simulation and not in the matrix, and a Markov chain's newborns are moved once by
the matrix against the initial state the simulation respects. Its judgment: the simulator needs an object that
carries the laws and serves views, draws from the law by the inverse distribution function on uniforms, which also
serves the dual measure's shared uniforms, draws from a discretization, and the discretization itself cached by its
settings; a simulation method, the law or as the matrix, defaulting to the matrix's distribution when the two are
compared; and the newborn stated once, a first-period statement in the model file read by every route, giving the
arrival states at birth and for each event whether a newborn runs it, takes a stated value or draws from a named
branch; for BST's newborn, no assets, employed with the Markov draw skipped, the transitory shock from the employed
branch, and permanent income one made explicit. The flags become views of that statement; the matrix builds the
newborns' first period as its own block; the solver never reads the statement. The object has named branches,
employed and unemployed, as the schemas state the unemployment event, so that a first draw from the employed branch
is a name and a Markov employment state uses the same branches by state.

**The model file and the Jacobians.** The model file names the income distribution and receives the discretized
object from the agent; its timing is stated by offsets; no method appears in it; only the simulator reads model files,
the solvers taking their inputs from the agent. Its judgment: the laws belong in the model file and the method does
not, the model file stating the model and the method being a run setting given to the solve, the matrices and the
simulation and recorded with each result, which is what lets one model be solved both ways. Two steps: first no
change to the language, the object behind the name becoming the law-carrying income process with the atoms a view;
later the language, shocks declared with their laws and branches and the first-period statement, a change to the
simulator's design agreed with its maintainers first. A discrete component is a law whose every method gives its
sum, so the method applies per continuous component and a passed-in discrete distribution keeps working. The
Jacobians go through one route, the model-file matrices, with the distribution's method held fixed across the
perturbed solves and a law's parameter rebuilding the object and its views; the legacy route stays classic or is
retired by the owner's decision. In the working group's schemas the method already belongs to the method file, the
run's specification, and not to the parameter file, so nothing there changes.

**The moving limit of issue #1868.** The labeled solver's distance is infinite while the natural limit moves between
iterations, because each iterate's lowest point is its own limit where the value is minus infinity; the limit moves
because the recursion starts from the terminal limit of zero and approaches the stationary one geometrically. Its
judgment: a limit from the laws does not stop it moving; starting the infinite-horizon iteration from a terminal
function whose limit is the stationary one does, acceptable in a new class's infinite-horizon solve and not in the
classic solver; with a zero-income event the limit is zero at every iterate and the issue cannot arise; the cure that
holds either way is to compare the inverse value function, finite at the limit, or the marginal value as the
unlabeled solution does.

**Measurements a redesign should fix by construction.** On a uniform arrival grid the first cell inflates the mass at
the constraint, 0.0263 against 0.0180 on a grid with a node at the constraint and geometric spacing above it, and
0.0178 by simulation; the arrival grid silently replaces a continuation variable's output grid; the distribution
function at stated points depends on node placement and on floating point, each error about half a cell's mass; the
lottery puts mass beyond the grid's ends on the end nodes without reporting it; the transitions are dense, so that
the Jacobians at a thousand nodes peaked at 4.9 gibibytes at a hundred periods and 13.8 at three hundred, a Markov
state multiplying the memory by the square of its count. The fixes: the constrained mass as its own atom, with at
least a node at each constraint and geometric spacing above it; outcome grids independent of the state grid; the
distribution function's convention stated; the mass beyond the ends reported; the transitions sparse.

**Where the object lives.** HARK's discretized distributions already record their law, the method, the count and the
bounds, which #1861 keeps true. The atoms are read directly by the solver, the limiting values, the kinked-return
bounds, the draws, the model-file events, the legacy matrix and two mixins; the standard consumer is the base of most
types, one newborn flag alone sitting in seventeen defaults in fourteen modules. Its judgment: the object goes in
core as a description only, laws with their generic interface composed into an income process with named branches, a
discrete view on request, and the checks the owner's rules put on laws and constraints made once for every method,
with no method of its own that takes an expectation or builds a matrix, a leaf that changes no classic behavior and
grows from what the record holds now, the laws primary and the atoms a view. The methods, the continuous expectation
and the laws-based transition builder, go in the experimental tier until promoted; the atoms method stays in core
unchanged. It recommends a new class in the tier, the method a parameter of the agent, recorded in its parameters and
its results, with a registry key supplying the default so that an adapter or a process can set it, the standard
consumer unchanged. The new class costs a second type kept in step by a parity test, the new class under atoms with
classic newborns reproducing the standard consumer's recorded results to 10⁻¹⁰, documentation of which type to use,
and a melding step later; it gives a home now for BST's laws as its own defaults, truncated at three standard
deviations, unemployment as its own event, newborns born employed. The in-place change costs every subclass and
every reader of the atoms touched, classic behavior proven bit for bit across the family, and a reversal of the
review's choice that the classic agent has no continuous option; it gives no second type.

**The owner's review of 2026-10-29, as HARK-dev confirms it may be cited.** Classic tools unchanged, with advanced
versions as separate objects in an experimental tier; an options registry with three profiles and environment-variable
mirrors, and a warning when a classic tool is given an advanced-only argument; a separate standard-consumer solver
sharing the classic solver's body; the classic solver as on main, with no continuous option; the infimum limit in the
separate solver until a default is changed; the registry and the tier first; #1862's replacement, once it happens.
The public anchors are #1845, the owner's proposal of a designated tier, and #1869, whose text on options on the
existing solver that review superseded. HARK-dev's view of whether the request of 13:46:09 fits that shape: it does
both, at different layers. How a method is chosen fits, the registry having been designed for choosing on the fly,
with the method an explicit, recorded parameter of the agent whose default the registry supplies. How the advanced
solver is built is where it goes further: the review's separate solver is a thin entry over the classic body, which is
the retrofit the owner names, and a new class on new machinery would not share that body, so the new class supersedes
the shared-body choice while the single-source principle survives, the new machinery being the one source called by
every solver that needs it. The distribution side extends the shape, which placed nothing in the simulator, the
matrices or the model files. The decision it puts to the owner: keep the separate standard-consumer solver as the
vehicle, or make the new class the vehicle and drop the separate solver, reusing its built parts, the continuous
expectation, the shape-preserving cubic and the infimum limit, as the new machinery's; it would put the new class to
him, with the registry and the tier first as decided, since they serve either path. On the operator's home it differs
from no one yet: the laws and the object in core as leaves, the continuous expectation and the builder in the tier
from the start, the atoms' expectation in core unchanged; HAFiscal's precomputed operator, lognormal-specific and
representing marginal value directly, it would keep off HARK's route for now.

## The user's side: the HAFiscal session's account

Received 2026-11-05 in the afternoon, written to be public; facts, judgments and what was not checked kept apart as it
marked them. One fact it holds on the owner's word in its session is left out here too.

**Its own continuous solver, by what it does.** A copy of HARK's one-period standard solver with one change: the two
expectations, of marginal value and, for the cubic, of its derivative, taken over the continuous laws instead of the
atoms; installed by replacing the agent's one-period solver, its configuration riding on the distribution objects so
that it reaches worker processes. It takes the laws, mean-one lognormals truncated at three standard deviations of the
log with the spread rescaled so that the truncated law keeps the stated variance, the unemployment event as a point
mass inside the transitory law with the employed part scaled; the quadrature's settings, sixteen Gauss–Legendre points
in the permanent shock, sixteen in the constrained piece where the marginal value has a closed form, and a
precomputed sparse operator for the unconstrained piece, next period's marginal value as cubic Hermite pieces on a
fixed log grid each integrated against the lognormal in closed form with only the cell holding the kink rebuilt each
iteration; and from next period's solution the rule with its slopes, the lower limit and the recorded kink. It splits
the transitory integral at the kink's preimage so that no node crosses the kink, integrates the permanent shock by
Gauss–Legendre on its truncated support with a graded rule where a row nears a natural limit, and returns HARK's
solution object with the kink recorded, one entry when the artificial constraint binds. It refuses two rates of
return, a binding natural limit, which was left to HARK so that one copy of that logic exists, a value function, which
it does not build, an end-of-period grid that starts at the natural limit on the continuous path, since a landing
from below the constraint can reach next period's minimum inside the support where the marginal value is not
integrable, and a missing configuration, which halts rather than fall back to the atoms. It is lognormal-specific in
three places, which is why it is not the version for HARK, whose tools are to read only a law's quantile function,
distribution function and bounds; HAFiscal's copy is frozen and will be replaced by HARK's.

**What a redesign must get right, each learned from a defect or a measurement.** Compute the kink rather than search
for it: with a gridpoint at the constraint in force the kink is that point's endogenous point, recorded on the
solution for next period's expectation, where a bisection of the rule moved with its bracket in the last bits. Split
wherever the integrand is not smooth: at the kink's preimage and at next period's knots, a cubic Hermite being only
once differentiable there, since a rule whose nodes cross them converges only algebraically, 1.7·10⁻⁵ in the marginal
value's expectation and 1.1·10⁻³ in its derivative's at thirty-two nodes in one test; at the truncated density's ends,
where a narrow cell holding the support's lower end left a row 1.7·10⁻⁷ off; and graded near a natural limit, where
sixteen fixed nodes left 1.2·10⁻⁵ and the graded rule reached 2·10⁻⁸. Take the worst-income mass from the law's point
masses, the finding released today. Start the end-of-period grid at the constraint in force on the continuous path.
Take the two expectations from one evaluation of next period's rule and split both: four points a piece of the knot
split gave 1.5·10⁻⁸ and 3.0·10⁻⁸ on the estimation's types, the operator 2.2·10⁻⁷ and 1.8·10⁻⁵, a rule split only at
the kink and the corners 4.4·10⁻⁶ and 6.9·10⁻⁴. Never fall back silently: a continuous request once ran on the atoms'
solver without an error, so the solution must record what it integrated and the solve must halt on a mismatch. Mind
that the interpolant and the expectation interact: atoms put image kinks into this period's rule, two to five convex
segments per type on the production grid under a cubic Hermite, every one of which the continuous expectation
removed; a shape-preserving cubic is legal with either. Take the limiting MPC and human wealth from closed forms where
they exist, since the recursion the tolerance stops early put the limiting MPC at 0.04033 against 0.03923 on the
restrained member at HARK's default tolerance. And state both sides, since the estimation integrates the law backward
and runs its transition matrices and lottery on the same law's atoms, a mixture whose size was never measured.

**What the reference solution needs.** On the restrained member, HAFiscal's continuous solver with the cubic rule
against its own finest setting, thirty-two permanent points, a node ratio of 1.005, a thousand grid points to 200 and
a tolerance of 10⁻¹¹: sixteen points, a ratio of 1.02 and the default grid of 48 to 20 give a relative error in
consumption of 2·10⁻⁷ between the kink and m = 3, 10⁻⁴ above it, and a kink 5·10⁻⁸ off; with 400 points to 100 the
three fall to 2·10⁻⁸, 10⁻⁸ and 3·10⁻⁹; with the ratio 1.01, to 10⁻⁸, 2·10⁻⁹ and 2·10⁻¹⁰; with thirty-two points and the
ratio 1.005 at 10⁻¹¹, to 5·10⁻¹⁰, 2·10⁻⁹ and 10⁻¹¹. HARK's defaults on the same member, seven atoms per shock, the
linear rule and the default grid, sit 4·10⁻³ to 6·10⁻³ from that reference, the atoms, the interpolant and the grid
unseparated. The emitter's atoms on the toy give an Euler residual at the kink of 9.8·10⁻³ at seven nodes per shock
falling to 5.3·10⁻⁴ at sixty-three, about n^(−1.4), with the kink moving from 0.8417 to 0.8298, so equiprobable atoms
cannot give a reference good to 10⁻⁸ near the kink, which would take of the order of a hundred thousand nodes per
shock; the continuous path reaches it. Its judgment of "very high precision": the knot split at eight or more points
a piece, where convergence turns geometric past about seven, 4·10⁻⁵ at eight and 10⁻¹² at fifteen in a one-period
test; splits at the kink, the knots and the truncation corners, with the graded rule near a natural limit; a thousand
or more end-of-period points, nested, with a node at the constraint in force; a tolerance of 10⁻¹¹; the value function
on; the limiting MPC and human wealth in closed form. Certified errors come from a ladder refining one knob at a time,
each quantity's error bounded by its largest change at the last step and certified only where each knob's last three
steps converge monotonically, with the Euler residual against the stated law beside it by an independent quadrature
of stated precision, which at 10⁻⁹ must itself split at the knots. The reference must report, near a natural limit,
consumption and the MPC against the distance from the limit, since relative errors in consumption are unbounded as
it goes to zero, the top MPC with the formula used, the request's lower end as the emitter sets it, and no node of the
distribution grid at the limit; and at the kink its location with its certified error, consumption there and the
slopes on each side, one below and the unconstrained MPC above, so that the comparator reports the kinks' distance
directly, compares consumption across the band between two toolkits' kinks and the MPC only outside it; and the
distribution's atoms with their masses, at the constraint and where households from the constraint land exactly on
the income while unemployed, so that the request's points stay off them. Whether the emitter gets a continuous method
for the reference waits on the owner's word in that session; under the single-copy rule it would be HARK's.

**What the estimation needs.** Its first step solves the types many times inside an optimizer with the law, the grid
and the permanent nodes fixed and only next period's marginal value changing, which the sparse operator serves, built
once and shared by every type and evaluation with the same law, grid, return, growth and lower limit: 538 evaluations
of the rule a call against about 300,000 for the knot split. The types share one income process and differ in the
discount factor. The splurge is outside the solve, entering the simulation and the lottery responses through each
agent's drawn transitory income, so the draws must come from the law the solver integrates; the toy-hafiscal
estimation mixes the other way, solving on the emitter's atoms while its panel draws from the laws by the inverse
distribution function with common random numbers; the benchmark's Jacobians are independent of HARK and run on atoms.
Its judgment: a method switch at solve time serves the estimation if it flips without rebuilding the agent, if the
expectation's precomputation can be cached and shared across types and evaluations keyed by the law, the grid, the
return, growth and the lower limit, and if the forward side is told its own representation, atoms of the same law at
a stated count, draws from the law, or an exact landing distribution from the law's distribution function. The
income-process object should carry the law as its quantile function, distribution function, bounds and point masses
with closed forms only as an optional supplied integral; the discretization rule and count; a sampler through the
inverse distribution function for common random numbers; and the affine maps of the transitory shock, the employed
scale and the Jacobians' inputs, since the kink's preimage moves with them.

**What an adapter needs.** The schema as it stands can carry it: both methods are `!quadrature` on the expectation
operator with different handlers; the forward representation goes on the population's transition target, so a
continuous backward with a discrete forward is expressible; and the diagnostics' expectation must already differ.
The registry must add two things, neither a schema change: the continuous handler with its settings, and per handler
which settings are model-changing, nodes per shock under atoms being model-changing since they define the effective
law, points a piece under the knot split being method-only since the effective member is then the stated member and
its expectations equal the closed forms to the quadrature's precision. Per level the adapter sets the expectation's
handler and its settings, the interpolant, the grid with its node at the constraint, the tolerance, the value function
and the forward transition's representation. HARK reports none of the effective member today, the emitter computing
it from the atoms itself; under the redesign HARK reports back, under either method, the constraint in force, the
natural limit with its source, the worst-income mass, the three limiting values as used, the kinks, the final distance
and the iteration count; under atoms, the atoms' named expectations and lowest values; under the law, the law's own
and the quadrature's record, points a piece, which splits it made and whether it graded. The direct comparison is two
method files on one parameter file and one request file, one ladder each, which the experiment file already allows.

**The comparison, as it would set it up.** Everything shared but the expectation: one member, one request, one grid
with a node at the constraint, one tolerance, one interpolant, a shape-preserving cubic being legal with both; each
method on its own ladder, atoms at 7, 15, 31 and 63 nodes per shock, the law at 4, 8, 16 and 32 points a piece, with
the grid refined under each to show the interpolation's error below the expectation's. The test is that both ladders
converge and that the atoms' limit equals the law's solution within the certified errors; two different limits mean
two models, a definitional mismatch in the natural limit, the worst-income mass, the truncation, the mean
normalization, the employed scale or the newborn, or a bug in one method, and the effective members test the
definition directly, the atoms' expectations and lowest values approaching the closed forms and infima along the
ladder, the law's equal to them at once. Run on truncated laws, since under an untruncated law every atoms member has
a finite natural limit and a kink the stated member lacks. The checks: the kink and the kinks' distance with the
slopes on each side; consumption across the kink band and the MPC outside it; the MPC at a natural limit against its
closed form, the limiting MPC and human wealth against theirs; concavity violations on a dense grid; the Euler
residual by an independent split quadrature; the targets; the distribution's moments, Lorenz ordinates, distribution
functions off the atoms and the atoms' masses; welfare; and a few Jacobian columns. What it expects: at the kink the
atoms converge slowly, about n^(−1.4) in the residual and 1.4 percent in the kink between seven and sixty-three nodes
on the toy, the law geometrically, to 10⁻¹¹ in the kink on the restrained member; near a natural limit with a
zero-income event the atoms get the MPC at the limit right, the event being a true atom, while a continuous path says
one until fixed, and fixed permanent nodes' error rises toward the limit unless graded; with no point mass the atoms'
natural limit lies below the law's, −5.54 against −1.73 on the toy, so the atoms solve over resources the stated
member excludes, and the comparison starts at the stated member's infimum.

**A new class or an in-place change, from HAFiscal's side.** Its macro agents descend from the standard consumer
through the Markov and the aggregate-Markov types, built without construction and with a hand-assigned income
process; its estimation's agents are the kinked-return type with a subclass for the splurge, and its reproduction of
the published results stays on that type with atoms bit for bit; its continuous solver replaces the one-period solver
and imports seven of HARK's helpers by name; the emitter and toy-hafiscal assign the income distribution by hand,
construct the marginals and assert that HARK rebuilt nothing; its store of solved policies keys on a content hash of
HARK's interpolation, core and standard-consumer modules, so any edit there recomputes every stored solution even
when results are bit for bit; and its move to HARK's continuous path is built and on hold until HARK settles how that
path is selected. Its judgment: in place, nothing of HAFiscal's breaks provided the default stays today's atoms path
to the last bit, the one-period solver's signature and the helpers' names stay, a hand-built income process still
solves on atoms by default, and the method can be chosen without reconstruction; the costs are one cold rebuild of
the store and a bit-for-bit gate on every path; the gain is that the Markov descendants inherit the method, which is
where atoms matter most to HAFiscal, seven per shock moving its wealth targets by several percent at a fixed
calibration; the risk, a subclass bypassing the switch and running on atoms silently, is closed by the solution's
record of its method and a halt on mismatch. A new class breaks nothing and leaves the store intact if the existing
modules are untouched, but HAFiscal's Markov chain cannot use it without a Markov counterpart and an aggregate type
on top, so the macro steps stay on atoms, and a two-method comparison becomes a two-class comparison, which holds
only while the classes' other code stays identical. Its view: the method belongs to the solve, not the class; keep
the existing classes as the model, make the expectation a setting chosen at solve time defaulting to today's path,
carry the law on the income-process object beside its discretization, and if HARK wants the code to mature off the
stable path first, a new class is fine provided its one-period solver is the same body the Markov solver calls, so
that moving it in place later is a re-export rather than a rewrite. Not checked: whether HARK's Markov solver can
share that body, which helpers a redesign would rename, the Jacobians under a continuous expectation, which were
never built, and the size of the backward-continuous, forward-discrete mixture in HAFiscal's estimate.

## Where the accounts agree, and where they do not

**Agreed by the three sessions, independently.**
- The laws are first-class and the atoms derived: an income-process object carries the laws with their bounds and
  point masses and the unemployment event as parameters, and makes its discretization on demand, recorded and
  cached.
- The method is a setting chosen at solve time, defaulting to today's atoms path bit for bit, settable without
  rebuilding the agent; every solution records the method and its settings, and a solve halts rather than fall back
  silently on a mismatch.
- One body serves the standard and the Markov solvers; the Markov solver takes one object per state.
- The natural limit, the landing mass, the worst-income mass, mean income and the limiting values come from the laws
  under either method, by closed forms where they exist, so that the two methods agree on them exactly.
- On the continuous path the end-of-period grid starts at the binding constraint with a knot at it, so that the kink
  is computed and recorded rather than found by a crossing; the integrals split at the kink's preimage, at next
  period's knots and at the truncated laws' ends, and are graded near a natural limit; the two expectations come from
  one evaluation of next period's rule.
- The forward side, draws and transition matrices, is told its own representation, from the laws under the
  continuous method or from a stated discretization, recorded and refinable; HARK-dev makes it a setting of its
  own with three values, held fixed when the solvers' methods are compared.
- The method is a run setting and not part of the model's statement: in HARK the agent's recorded parameter with
  its default from the registry, in the model file nothing, and in the working group's schemas the method file.
- The newborn is stated once, born employed at permanent income one with no assets and its first draw from the
  employed branch, and read the same way by the solve, the simulation and the matrices.
- The comparison refines one knob at a time on each method's ladder, with the Euler residuals by an independent
  quadratature of stated precision, and requires the model's quantities, the limit, the landing mass and the top MPC,
  to agree exactly while the method's quantities converge.

**Where they differ.**
- **Where it lives.** The HARK session favors a new class on the new machinery with the old types untouched, and
  HARK-dev recommends the same, a new class in the experimental tier with the registry and the tier first, noting
  that it fits the review of 2026-10-29 in how a method is chosen and goes beyond it in how the solver is built,
  since a class on new machinery would not share the classic body. The HAFiscal session holds that the
  method belongs to the solve, not the class: keep the existing classes as the model and make the expectation a
  solve-time setting, so that its Markov descendants inherit it, which is where atoms cost it most; a new class is
  acceptable to it only if its one-period solver is the same body the Markov solver calls, so that moving it in place
  later is a re-export. The HARK session counts what an in-place change touches: the kinked-return hand-off, the New
  Keynesian type's defaults, nine subclasses' pre-solve, the direct readers of the discretized distribution, and some
  thirty one-period solvers that sum over their own atoms. The HAFiscal session's four conditions for in place, the
  default bit-identical, the solver's signature and helpers' names kept, a hand-built process solving on atoms by
  default, the method chosen without reconstruction, are the same conditions the shared body would have to meet in
  either placement.
- **The cost of the continuous expectation.** The HAFiscal session's estimation solves its types many times inside an
  optimizer and relies on a precomputed sparse operator shared across types and evaluations, 538 evaluations of the
  rule a call against about 300,000 for the knot-split quadrature; the HARK session's design caches the discrete
  method's discretization per settings but says nothing of caching on the continuous path, and marks the continuous
  method's cost on fine grids as unchecked. A redesign that serves the estimation needs the object to admit a
  precomputed operator keyed by the law, the grid, the return, growth and the lower limit.
- **The precomputed operator's place.** HARK-dev would keep HAFiscal's operator off HARK's route for now, being
  lognormal-specific and representing marginal value directly, against two of the owner's rules; the HAFiscal
  session itself calls its copy frozen and will adopt HARK's. What stands is the estimation's need, which a generic
  operator could meet: the cells' integrals of the rule's Hermite pieces against the law computed once by
  quadrature from the law's generic interface, which is a design question for the tier, not a disagreement of
  principle.
- **Precision settings.** The HARK session's prototype defaults to four nodes a piece and places seventeen tuned points
  near a smooth natural limit; the HAFiscal session's "very high precision" wants eight or more points a piece, where
  convergence turns geometric, a thousand or more grid points with a node at the constraint, and a tolerance of
  10⁻¹¹. These are settings on one ladder, not a disagreement of design, but the reference solution's are the
  HAFiscal session's.

## The proposal

Drawn from the three accounts; where it chooses, it says so.

- **One income-process object, in core, carrying the laws.** The permanent and the employed transitory laws as HARK
  distributions with a generic interface, the distribution function, the quantile function, the bounds and the point
  masses; the unemployment event as the two parameters, never a transitory atom, as the schemas state it; named
  branches, employed and unemployed, by which a newborn's first draw and a Markov employment state are stated; the
  discretization a view on request, cached by its settings and bit-identical to today's constructors at today's
  settings; a sampler through the inverse distribution function for common random numbers; and the model's
  quantities answered from the laws, the natural limit by the sign rule with the permanent shock's infimum or
  supremum as the sign picks, whether the limit binds without a kink, the landing mass branch by branch, mean income,
  the worst-income mass, the bounds. It takes no expectation and builds no matrix.
- **One solver body against that object, with the method chosen at call time.** The expectation takes the integrand,
  its arguments and a method as a settings object: discrete, with its counts, placement, tails and the source of the
  limit; or continuous, Gauss–Legendre in pieces in each law's own coordinate, split at the kink's preimage, at next
  period's knots and at the truncated laws' ends, graded near a natural limit, the two expectations from one
  evaluation of next period's rule, with a generic precomputed operator admitted where the law, the grid and the
  limit are fixed across many solves. The model-specific part, the transition of resources and the mapping of next
  period's kinks to each law's cut points, is a function in each model's module. The body computes the limit, the
  constraint in force, whether it kinks, the landing mass and the MPC at the limit from the object, takes its grid
  from a grid rule that is a setting of its own, anchored at the atoms' limit under the discrete method at today's
  settings and at the binding constraint with a knot there under the continuous one, and records on the solution the
  kinks, the method and every setting. The discrete method at today's settings reproduces today's results bit for
  bit, which a test enforces.
- **The method is the agent's parameter and the solve's argument, never silent.** A type parameter sets the default,
  supplied by the options registry so that an adapter or a process can set it from outside; the solve's argument
  overrides it for one solve without rebuilding the agent, so that a user compares two solves of one agent; each
  solution carries its method and settings, and a solve halts on a mismatch rather than fall back.
- **The forward side told its representation.** The distribution's method is a setting of its own, the solver's own
  atoms, the same laws discretized more finely for the distribution alone, or weights integrated against the laws by
  the monotone-landing builder, held fixed when the solvers' methods are compared; the simulation draws from the law
  or as the matrix does, defaulting to the matrix's distribution when the two are compared; the constrained mass is
  its own atom with a node at each constraint; the transitions are sparse; the mass beyond the grid's ends is
  reported; the newborn is stated once and read by every route.
- **The vehicle: a new class in the experimental tier, on a body shared with the classic and the Markov solvers.**
  This is the proposal's one choice between the accounts. The new class, in the module the owner has named, is a thin
  entry over the shared body with the method parameter exposed and BST's laws as its defaults; the classic
  standard-consumer solver becomes a thin entry over the same body with the discrete method fixed at today's settings,
  so that the classic agent keeps no continuous option and its results stay bit-identical, proven by the parity test;
  the Markov solver calls the same body per state. That keeps the review's shape in what it fixes, classic tools
  unchanged in behavior, advanced objects in the tier, the registry and the tier first, and meets the HAFiscal
  session's condition that a new class's one-period solver be the body the Markov solver calls, so that its Markov
  descendants inherit the method and a later move in place is a re-export. It costs the classic solver one refactor
  proven bit for bit, which HAFiscal's store of solved policies pays once, and the owner's earlier choice of a
  separate standard-consumer solver as the vehicle gives way to the class.
- **The reference solution** comes from the new class's continuous method at the HAFiscal session's settings, eight
  or more points a piece, the splits and the graded rule, a thousand or more grid points with a node at the
  constraint, a tolerance of 10⁻¹¹, the value function on, the limiting values in closed form, with certified errors
  from a ladder that refines one knob at a time and an independent split quadrature beside it; it reports near a
  natural limit against the distance from the limit and at the kink the location with its error and the slopes on
  each side, and the comparator reports the kinks' distance directly, compares consumption across the band between
  two kinks and the MPC outside it.
- **The comparison** is two method files on one parameter file and one request file, one ladder each, atoms at 7,
  15, 31 and 63 nodes per shock and the law at 4, 8, 16 and 32 points a piece, on one grid rule with a node at the
  constraint, one tolerance and one interpolant, the distribution's method fixed; the test is that both ladders
  converge, that the model's quantities, the limit, the landing mass and the top MPC, agree exactly, and that the
  atoms' limit equals the law's solution within the certified errors, with the effective members testing the
  definition directly; it runs on truncated laws. In the working group's registry of handlers the continuous handler
  is added with its settings, and each handler's settings are marked model-changing or method-only; neither is a
  schema change, and both are proposals under the owner's standing rule on schema changes.

## What it costs, and the order

The HARK session's count, new code with tests: the object and the method settings, 500 to 700 lines plus about 400 of
tests; the dispatcher, about 100; the body and the new class, 600 to 800; the Markov route, 200 to 300; the comparison
tests and a notebook, 300 to 500; about two thirds of the solver-side code carrying over from its prototype, the
quadrature, the three continuous expectations, the natural-limit logic, the placed points, the shape-preserving cubic,
the truncated shocks and the mixture. HARK-dev's side adds the laws-based transition builder, the sparse transitions,
the distribution's method on the simulator, the newborn's first-period statement, and the simulation by method, which
it did not count and which the simulator's maintainers must agree to first. HAFiscal pays one cold rebuild of its store
and rebuilds its move to the continuous path on the new interface.

The order, from the three accounts:

1. #1861 and #1863, posted as drafts: the laws and their bounds.
2. The options registry and the experimental tier, as decided on 2026-10-29, which serve either vehicle.
3. The generic quadrature and the expectation dispatcher by method.
4. The income-process object, with the test that the discrete view at today's settings reproduces today's
   distribution bit for bit, and the checks on laws and constraints made once.
5. The shared body and the new class, the classic solver re-entered over the body with the parity test, the method
   as parameter and argument, the records on the solution, and the comparison tests on the two ladders.
6. The shape-preserving cubic, independent, at any point.
7. The Markov route: #1858 as it stands, then the per-state objects with the zero-mass guard, then persistence if it
   is wanted.
8. The distribution's method on the simulator and the matrices, the constrained atom, the sparse transitions and the
   reported mass; then the laws-based builder; then the newborn's first-period statement in the model file, agreed
   with the simulator's maintainers.
9. Simulation by method; the Jacobians through the one route; later, promotion to core and any change of defaults.

## Decisions for the owner

- **The vehicle.** The new class in the tier on a body shared with the classic and Markov solvers, as proposed; or the
  review's separate standard-consumer solver over the classic body, with the method as its option; or the HAFiscal
  session's in-place change of the existing types. The first changes the classic solver's code once, proven bit for
  bit; the second keeps the retrofit; the third touches every reader of the atoms.
- **The distribution's method** as a setting of its own with HARK-dev's three values, held fixed when the solvers'
  methods are compared; and whether the laws-based builder is written now or after the comparison runs on finer
  atoms.
- **The newborn's first-period statement** in the model file, which changes the simulator's design and is to be agreed
  with its maintainers first, or the flags kept as views for now.
- **The precomputed operator**: a generic one in the tier for the estimation's many solves, or none until the
  comparison shows the knot-split quadrature too slow for it.
- **The reference solution** from the new class's continuous method, with the emitter's switch on his word in the
  HAFiscal session.
- **The working group's registry of handlers**: the continuous handler and the model-changing marking, as proposals.
- **What becomes of #1862, #1859, #1860 and #1869** under the chosen vehicle: #1862 subsumed by the object's limit and
  closed when the set opens, as decided; #1859 needed only for persistence; #1860's newborn convention through the
  first-period statement; #1869's text revised to the vehicle.

