#!/usr/bin/env python3
import sys
import re

keys = ["SFE_SC", "SE_LJ", "SE_ES"]

coeff_sets = {
#    "Full": {
#        "xmu":  [-0.34694766, 0.55289482, 0.6106927],
#        "xmu0": [0.66651081, 0.0, 0.0],
#    },
    "Standard": {
        "xmu":  [0.0, 0.53900435, 0.44943914],
        "xmu0": [0.31305262, 0.0, 0.0],
    },
}

def parse_xmu(filename):
    values = {}
    pattern = re.compile(r"^\s*(\w+)\s*=\s*([-\d\.Ee+]+)")
    with open(filename, "r") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                key, val = m.group(1), float(m.group(2))
                if key in keys:
                    values[key] = val
    return values

def weighted_sum(values, coeffs):
    total = 0.0
    for k, c in zip(keys, coeffs):
        if k not in values:
            raise RuntimeError(f"{k} not found")
        total += c * values[k]
    return total

def main():
    if len(sys.argv) != 2:
        print("Usage: python milc.py [basename]")
        sys.exit(1)

    base = sys.argv[1]

    vals_xmu  = parse_xmu(f"{base}.xmu")
    vals_xmu0 = parse_xmu(f"{base}.xmu0")

    for set_name, coeff in coeff_sets.items():
        sum_xmu  = weighted_sum(vals_xmu,  coeff["xmu"])
        sum_xmu0 = weighted_sum(vals_xmu0, coeff["xmu0"])
        total    = sum_xmu + sum_xmu0

        print(f"== {set_name} ==")
#        print("xmu  contribution =", sum_xmu)
#        print("xmu0 contribution =", sum_xmu0)
        print("SFE(MILC)=", total, "(J/mol)")
        print("         =", total/4184, "(Kcal/mol)")
        print()

if __name__ == "__main__":
    main()
