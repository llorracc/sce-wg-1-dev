"""HARK's adapter for the buffer-stock families: HARK's part, written from HARK's Rosetta Stone (rosetta/hark.md and
rosetta/hark.cards.yaml), the ladder file beside this file, the schemas and the Toolkit protocol of ../common.py.

    <python of HARK's environment> harness/adapters/hark/adapter.py <parameter file> --out <dir> --level <n> \
        --request <request file>

The toolkit is HARK's MarkovConsumerType on the nonpersistent chain, which writes the families' unemployment event as a
state: two states, employed and unemployed, both rows of the chain (1 - p_zero, p_zero).
  Encode: the stone's lexicon. The chain and the income process are built here, with HARK's constructors for both
    switched off; HARK's own income inputs are placeholders. The grid's four settings and the tolerance are the level's
    element of ladder.yaml, in HARK's names, and HARK builds its grid from them itself.
  Call: solve(), the infinite horizon (cycles = 0, T_cycle = 1).
  Decode: the checks the stone lists, then the employed state's cFunc and vFunc and its mNrmMin.
Everything between that solution and the results file is ../common.py's, the same for every toolkit.
"""

import importlib.metadata
import json
import pathlib
import sys
from types import SimpleNamespace

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import common  # noqa: E402
import HARK  # noqa: E402
from HARK.ConsumptionSaving.ConsMarkovModel import MarkovConsumerType, init_indshk_markov  # noqa: E402
from HARK.distributions import DiscreteDistributionLabeled  # noqa: E402

HANDLER = "HARK.ConsumptionSaving.ConsMarkovModel.MarkovConsumerType"
STATES_AGREE = 1e-12        # the two states' rules and values, relative (the stone, "Decode")
LIMIT_AGREES = 1e-9         # both states' mNrmMin against the effective member's constraint in force (the stone)
CHECK_POINTS = 400          # points of m, inside the solution grid, at which the two states are held to each other
SEED = 0                    # of the two distributions; nothing here draws from them


def _lowest(member, psi, th):
    """The lowest nodes of psi and of xi: the worst income is the lower of xi_u and the lowest scaled employed node."""
    xi_low = float(common.employed_scale(member) * np.min(th))
    if member.wp > 0:
        xi_low = min(xi_low, float(member.xi_u))
    return float(np.min(psi)), xi_low


def constraint_in_force(member, psi, th):
    """The effective member's constraint in force: the larger of the member's constraint (a_Art, or under natural the
    stated laws' limit) and the natural limit of the nodes' lowest values, -xi_min psi_min / (R/G - psi_min)."""
    psi_low, xi_low = _lowest(member, psi, th)
    a_member = float(member.a_art)
    if psi_low * member.G >= member.R:          # no finite natural limit
        return a_member
    natural = -xi_low * psi_low / (member.R / member.G - psi_low) + 0.0
    return max(a_member, natural)


def income_process(member, nodes):
    """IncShkDstn for one period: one labeled distribution over PermShk and TranShk per state. Employed: the product of
    psi's nodes and the employed nodes scaled by (1 - p_zero xi_u)/(1 - p_zero). Unemployed: psi's nodes with TranShk =
    xi_u at each. Each carries the stated laws' infima and suprema as its limit, from which HARK takes the natural
    borrowing limit (BoroCnstInfimum)."""
    p_psi, psi, p_th, th = nodes
    scale = common.employed_scale(member)
    xi_u = float(member.xi_u)
    psi_bounds = (float(member.psi.infimum), float(member.psi.supremum))
    bounds = ((scale * float(member.theta.infimum), scale * float(member.theta.supremum)), (xi_u, xi_u))
    names = ("employed", "unemployed")
    dstns = []
    for (p, perm, tran), (low, high), name in zip(common.state_shocks(member, p_psi, psi, p_th, th), bounds, names):
        dstns.append(DiscreteDistributionLabeled(
            pmv=np.asarray(p, float), atoms=np.vstack([perm, tran]), seed=SEED,
            limit={"infimum": np.array([psi_bounds[0], low]), "supremum": np.array([psi_bounds[1], high])},
            name=f"the buffer-stock families' income shocks, {name}", var_names=["PermShk", "TranShk"]))
    return [dstns]


def chain(member):
    """MrkvArray for one period: the nonpersistent chain, both rows (1 - p_zero, p_zero)."""
    row = [1.0 - float(member.wp), float(member.wp)]
    return [np.array([row, row])]


def encode(member, beta, nodes, own):
    """The member, one type's beta, the nodes and the level's settings as MarkovConsumerType's arguments."""
    both = lambda x: [np.array([float(x), float(x)])]       # a list per period of one value per state, the same in both
    return dict(
        cycles=0, T_cycle=1,                                  # the infinite horizon
        CRRA=float(member.rho), DiscFac=float(beta),
        LivPrb=both(member.L), Rfree=both(member.R), PermGroFac=both(member.G),
        BoroCnstArt=None if member.natural else float(member.a_art),
        MrkvArray=chain(member), IncShkDstn=income_process(member, nodes),
        constructors=dict(init_indshk_markov["constructors"], MrkvArray=None, IncShkDstn=None),
        UnempPrb=np.zeros(2), IncUnemp=np.zeros(2),           # the standard consumer's way, left at zero, one per state
        MrkvPrbsInit=np.array([1.0, 0.0]), NewbornTransShk=True,   # the newborn: employed, with an employed draw
        CubicBool=True, vFuncBool=True,
        aXtraMin=float(own["aXtraMin"]), aXtraMax=float(own["aXtraMax"]), aXtraCount=int(own["aXtraCount"]),
        aXtraNestFac=int(own["aXtraNestFac"]), tolerance=float(own["tolerance"]))


def _same(x, y, tolerance):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return bool(np.all(np.abs(x - y) <= tolerance * np.maximum(np.abs(x), np.abs(y))))


def decode(agent, member, nodes, own):
    """The stone's checks on what HARK solved, then the employed state's rule, value and lower limit."""
    solution = agent.solution[0]
    # HARK solved with the adapter's chain and income process
    assert len(agent.MrkvArray) == 1 and np.array_equal(agent.MrkvArray[0], chain(member)[0]), agent.MrkvArray
    for mine, harks in zip(income_process(member, nodes)[0], agent.IncShkDstn[0]):
        assert np.array_equal(mine.pmv, harks.pmv) and np.array_equal(mine.atoms, harks.atoms), "IncShkDstn was rebuilt"
        assert all(np.array_equal(mine.limit[k], harks.limit[k]) for k in ("infimum", "supremum")), "limits were rebuilt"
    # both states' lower limits are the effective member's constraint in force
    a_lo = constraint_in_force(member, nodes[1], nodes[3])
    floors = np.asarray(solution.mNrmMin, float)
    assert floors.shape == (2,) and np.all(np.abs(floors - a_lo) <= LIMIT_AGREES), (floors, a_lo)
    # the two states' rules and values agree, as they must when every row of the chain is the same
    m = float(floors.max()) + np.geomspace(float(own["aXtraMin"]), float(own["aXtraMax"]), CHECK_POINTS)
    for part in ("cFunc", "vFunc"):
        employed, unemployed = getattr(solution, part)
        assert _same(employed(m), unemployed(m), STATES_AGREE), f"the two states' {part} differ"
    assert _same(solution.cFunc[0].derivative(m), solution.cFunc[1].derivative(m), STATES_AGREE), "the MPCs differ"
    # the top of the solution grid in m: the last knot of the relaxed rule, the first function of HARK's lower envelope
    top = float(solution.cFunc[0].functions[0].x_list[-1])
    return SimpleNamespace(cFunc=solution.cFunc[0], vFunc=solution.vFunc[0], mNrmMin=float(floors[0]), top=top)


class HarkToolkit:
    """HARK, as ../common.py's Toolkit protocol asks for it."""

    name = "HARK"
    driver = "harness/adapters/hark/adapter.py, with harness/adapters/common.py"
    description = ("HARK's adapter for the buffer-stock families: solves a member with MarkovConsumerType on the "
                   "nonpersistent chain and writes its results, method and settings files")
    representation = ("the unemployment event a state of HARK's MarkovConsumerType on the nonpersistent chain, both rows "
                      "(1 - p_zero, p_zero): employed, the product of psi's nodes and the employed nodes scaled by "
                      "(1 - p_zero xi_u)/(1 - p_zero); unemployed, psi's nodes with xi = xi_u; each state's distribution "
                      "carries the stated laws' infima and suprema, from which HARK takes the natural limit")
    diagnostics_method = (f"Gauss-Legendre in logs of the stated laws, {common.DIAG_NODES} nodes per piece per shock, "
                          "the employed draw's support split at the rule's kink; the unemployment event exact")
    # The stone's methods, on the stage's targets: the tag where the cards give one that names what runs, words otherwise;
    # a handler where the cards name one. No values.
    methods = [
        {"on": "policy.euler.solve", "method": "!time-iteration", "handler": HANDLER},
        {"on": "policy", "method": "a cubic Hermite whose slopes are the solution's own MPCs"},
        {"on": "E_ψ_θ_j", "method": "!quadrature"},
        {"on": "cntn_to_dcsn.value", "method": "value-function"},
        {"on": "arvl_to_dcsn", "method": "!histogram", "handler": "adapter"},
        {"on": "population.distribution", "method": "the adapter's own fixed point", "handler": "adapter"},
        {"on": "diagnostics.expectation", "method": "Gauss-Legendre in logs of the stated laws, split at the rule's kink",
         "handler": "adapter"},
    ]

    def __init__(self):
        self.solver = {"handler": HANDLER, "types": []}      # how each solve ended, filled by solve()
        self._ladder = common.ladder(HERE / "ladder.yaml")

    def version(self):
        return str(HARK.__version__)

    def commit(self):
        """The commit HARK was installed from, as the environment records it; None when it records none."""
        try:
            url = json.loads(importlib.metadata.distribution("econ-ark").read_text("direct_url.json"))
            return str(url["vcs_info"]["commit_id"])
        except Exception:
            return None

    def level_settings(self, level):
        """HARK's own settings at a level, in HARK's names: the level's element of the ladder file."""
        return dict(self._ladder[level])

    def settings(self, level, lev):
        """The settings file's mapping: the level, HARK's settings in HARK's names, and those of the code the adapters
        share. Plain numbers only: the strict subset has no booleans, so the two switches are written as 1."""
        return {"level": level, **self.level_settings(level), "CubicBool": 1, "vFuncBool": 1,
                "nodes_per_shock": lev["nodes"], "transition_nodes_per_shock": lev["transition_nodes"],
                "histogram_points": lev["dist_points"], "histogram_top": lev["dist_top"],
                "target_search_top": lev["solve_top"], "diagnostics_nodes": common.DIAG_NODES}

    def solve(self, member, beta, nodes, own):
        agent = MarkovConsumerType(**encode(member, beta, nodes, own))
        agent.solve()
        distance, cycles = float(agent.solution_distance), int(agent.completed_cycles)
        # HARK stops without a word after 5000 cycles: a solve that ends there is not the method the stone states
        assert distance <= agent.tolerance, f"HARK stopped at {cycles} cycles, distance {distance} above {agent.tolerance}"
        solution = decode(agent, member, nodes, own)
        self.solver["types"] = [t for t in self.solver["types"] if t["beta"] != float(beta)] + [
            {"beta": float(beta), "completed_cycles": cycles, "solution_distance": distance,
             "tolerance": float(agent.tolerance), "gridpoints": int(agent.aXtraGrid.size),
             "top_gridpoint_m": solution.top}]
        return solution


TOOLKIT = HarkToolkit()

if __name__ == "__main__":
    common.run(sys.argv[1:], TOOLKIT)
