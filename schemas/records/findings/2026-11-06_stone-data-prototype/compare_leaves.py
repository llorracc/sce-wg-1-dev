"""Compare two results files leaf by leaf: how many leaves, how many numbers, and which differ.

    python compare_leaves.py <results.json> <results.json>
"""
import json
import sys


def leaves(x, path=""):
    if isinstance(x, dict):
        for key, value in x.items():
            yield from leaves(value, f"{path}.{key}" if path else key)
    elif isinstance(x, list):
        for i, value in enumerate(x):
            yield from leaves(value, f"{path}[{i}]")
    else:
        yield path, x


a = dict(leaves(json.load(open(sys.argv[1], encoding="utf-8"))))
b = dict(leaves(json.load(open(sys.argv[2], encoding="utf-8"))))
numbers = [k for k in a if isinstance(a[k], (int, float)) and not isinstance(a[k], bool)]
differ = [k for k in a if k not in b or a[k] != b[k]]
print(f"{len(a)} leaves, {len(numbers)} of them numbers; {len(differ)} differ; {len(set(a) ^ set(b))} are in one file only")
for key in differ[:20]:
    print("  ", key, "|", str(a.get(key))[:60], "|", str(b.get(key))[:60])
