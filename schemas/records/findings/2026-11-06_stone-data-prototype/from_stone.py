"""PROTOTYPE, in a scratch folder: a toolkit's arguments assembled from its Rosetta Stone's data file.

`arguments(stone, member, beta, own, built)` returns the keyword arguments for the toolkit's handler: the member's
parameters under the toolkit's names and in its shapes, the adapter's fixed arguments, the placeholders the toolkit
asks for, its own settings at the level, and what the adapter built itself. It is the same for every toolkit whose
handler is called with keyword arguments; a stone's data file says everything toolkit-specific that it needs.

It refuses what would otherwise fail far from its cause: a member key the parameter file does not have, a shape the
stone does not define, a setting the ladder does not state, an argument named twice.
"""
import ast
import importlib

import numpy as np

KINDS = ("arguments", "fixed", "placeholders")


def load(path):
    """The stone's data, read in the schemas' strict YAML subset."""
    from wg1core import canonical
    with open(path, encoding="utf-8") as f:
        return canonical.load_strict(f.read())


def literal(entry):
    """A fixed value: the toolkit's own literal, as an array where the stone says so."""
    value = ast.literal_eval(entry["literal"])
    return np.array(value) if entry.get("as") == "array" else value


def member_value(member, key, beta):
    """The member's value at a parameter-file key, written as the schemas write keys: income.growth, types[].beta."""
    if key == "types[].beta":
        return beta
    at = member.data
    for part in key.split("."):
        if not isinstance(at, dict) or part not in at:
            raise KeyError(f"the member has no parameter-file key {key!r}")
        at = at[part]
    return at


def shaped(value, shape, stone):
    if shape not in stone["shapes"]:
        raise ValueError(f"the stone defines no shape {shape!r}")
    if shape == "scalar":
        return value
    if shape == "per-period-per-state":
        return [np.array([value] * len(stone["states"]))]
    raise ValueError(f"no rule for the shape {shape!r}")


def arguments(stone, member, beta, own, built):
    """The handler's keyword arguments, and the names in each kind, for the adapter's record."""
    out, names = {}, {}

    def put(kind, name, value):
        if name in out:
            raise ValueError(f"{name} is given twice, the second time under {kind}")
        out[name] = value
        names.setdefault(kind, []).append(name)

    for name, entry in stone["arguments"].items():
        natural = entry.get("in_a_natural_family")
        if natural is not None and member.natural:
            put("arguments", name, literal(natural))
        else:
            put("arguments", name, shaped(member_value(member, entry["from"], beta), entry["shape"], stone))
    for kind in ("fixed", "placeholders"):
        for name, entry in stone[kind].items():
            put(kind, name, literal(entry))
    for name in stone["settings"]["passed"]:
        if name not in own:
            raise KeyError(f"the ladder states no setting {name!r} at this level")
        put("settings", name, own[name])
    stated = set(stone["built_by_the_adapter"])
    if set(built) != stated:
        raise ValueError(f"the adapter built {sorted(built)}, the stone says {sorted(stated)}")
    for name, value in built.items():
        put("built_by_the_adapter", name, value)
    for name, entry in stone["handler"].get("extra", {}).items():
        put("extra", name, literal(entry))
    return out, names


def handler(stone):
    """The toolkit's class and the constructors it is given: the defaults', with the stone's switched off."""
    module = importlib.import_module(stone["handler"]["module"])
    constructors = dict(getattr(module, stone["handler"]["defaults"])["constructors"])
    for name in stone["switched_off"]["constructors"]:
        if name not in constructors:
            raise KeyError(f"the toolkit has no constructor {name!r} to switch off")
        constructors[name] = None
    return getattr(module, stone["handler"]["class"]), constructors
