#!/usr/bin/env python3
"""
Probe SATD rules from a copied CA_Rule_Search table for small-board periods.

Usage:
  python rule_period_probe.py pasted_table.txt
  python rule_period_probe.py pasted_table.txt --samples 5000 --threshold 8 --out results.csv

The parser expects copied text from CA_Rule_Search.html. It ignores "... omitted ..."
gap rows and reads visible table rows with columns like:

  Rank  Number  Genome  Info  Samples  Score  ...

For each visible rule it probes wrapped Moore-neighborhood boards from 4x4
through 8x8. 4x4 is exhaustive over canonical balanced patterns by default.
Larger boards use balanced random patterns by default.
"""

from __future__ import annotations

import argparse
import csv
import random
import re
import sys
import time
from dataclasses import dataclass
from typing import Iterable


ACTIONS = "SATD"
GENOME_LENGTH = 9
REFERENCE_NAMES = {
    "Life",
    "HighLife",
    "Day & Night",
    "Seeds",
    "Maze",
    "Diamoeba",
    "Replicator",
    "Morley",
    "2x2",
    "EightLife",
    "Pedestrian",
    "Long Life",
    "34 Life",
    "Mazectric",
    "Amoeba",
    "Pseudo Life",
    "Coral",
    "Coagulations",
    "Stains",
    "Serviettes",
    "Life without Death",
    "Gnarl",
    "Live Free or Die",
}


@dataclass
class Rule:
    rank: int
    number: int
    compact: str
    info: str
    samples: int
    score: float
    nearest: str
    genome: str


def genome_from_number(number: int) -> str:
    n = number
    out = []
    for _ in range(GENOME_LENGTH):
        out.append(ACTIONS[n & 3])
        n //= 4
    return "".join(out)


def compact_gene(genome: str) -> str:
    highest = GENOME_LENGTH - 1
    while highest > 0 and genome[highest] == "S":
        highest -= 1
    return "".join(genome[i] for i in range(highest, -1, -1))


def parse_rules(text: str) -> list[Rule]:
    rules: list[Rule] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("...") or line.startswith("Rank\t"):
            continue
        parts = line.split("\t")
        if len(parts) < 7:
            continue
        if not parts[0].isdigit() or not parts[1].isdigit():
            continue
        try:
            rank = int(parts[0])
            number = int(parts[1])
            compact = parts[2].replace("*", "").strip()
            info = parts[3].strip()
            samples = int(float(parts[4]))
            score = float(parts[5])
            nearest = parts[6].strip()
        except ValueError:
            continue
        genome = genome_from_number(number)
        rules.append(Rule(rank, number, compact, info, samples, score, nearest, genome))
    return rules


def wrap(v: int, n: int) -> int:
    return v % n


def step_state(n: int, state: int, genome: str) -> int:
    out = 0
    for r in range(n):
        row_base = r * n
        for c in range(n):
            count = 0
            for dr in (-1, 0, 1):
                rr = wrap(r + dr, n)
                rr_base = rr * n
                for dc in (-1, 0, 1):
                    if dr or dc:
                        cc = wrap(c + dc, n)
                        count += (state >> (rr_base + cc)) & 1
            was = (state >> (row_base + c)) & 1
            action = genome[count]
            if action == "S":
                alive = was
            elif action == "A":
                alive = 1
            elif action == "T":
                alive = 1 - was
            else:
                alive = 0
            if alive:
                out |= 1 << (row_base + c)
    return out


def period(n: int, state: int, genome: str, max_steps: int) -> tuple[int, int, int]:
    seen = {state: 0}
    current = state
    for t in range(1, max_steps + 1):
        current = step_state(n, current, genome)
        old = seen.get(current)
        if old is not None:
            return t - old, old, current
        seen[current] = t
    return 0, max_steps, current


def transform_state(n: int, state: int, kind: int) -> int:
    out = 0
    for r in range(n):
        for c in range(n):
            if kind == 0:
                rr, cc = r, c
            elif kind == 1:
                rr, cc = c, n - 1 - r
            elif kind == 2:
                rr, cc = n - 1 - r, n - 1 - c
            elif kind == 3:
                rr, cc = n - 1 - c, r
            elif kind == 4:
                rr, cc = r, n - 1 - c
            elif kind == 5:
                rr, cc = n - 1 - r, c
            elif kind == 6:
                rr, cc = c, r
            else:
                rr, cc = n - 1 - c, n - 1 - r
            if (state >> (rr * n + cc)) & 1:
                out |= 1 << (r * n + c)
    return out


def canonical_state(n: int, state: int) -> int:
    return min(transform_state(n, state, kind) for kind in range(8))


def balanced(state: int, cells: int, min_each: int) -> bool:
    ones = state.bit_count()
    return ones >= min_each and cells - ones >= min_each


def exhaustive_canonical_states(n: int, min_each: int) -> Iterable[int]:
    total = 1 << (n * n)
    for state in range(total):
        if not balanced(state, n * n, min_each):
            continue
        if canonical_state(n, state) == state:
            yield state


def random_balanced_state(n: int, min_each: int, rng: random.Random) -> int:
    cells = n * n
    while True:
        state = rng.getrandbits(cells)
        if balanced(state, cells, min_each):
            return state


def probe_rule(
    rule: Rule,
    n: int,
    threshold: int,
    max_steps: int,
    samples: int,
    time_limit: float,
    exhaustive: bool,
    rng: random.Random,
) -> dict[str, object]:
    start = time.perf_counter()
    tested = 0
    max_period = 0
    witness = ""
    passed = False
    exhausted = False

    if exhaustive:
      states: Iterable[int] = exhaustive_canonical_states(n, n)
    else:
      states = (random_balanced_state(n, n, rng) for _ in range(samples))

    for state in states:
        if time.perf_counter() - start > time_limit:
            break
        tested += 1
        p, transient, repeat_state = period(n, state, rule.genome, max_steps)
        if p > max_period:
            max_period = p
            witness = hex(state)
        if p >= threshold:
            passed = True
            break
    else:
        exhausted = exhaustive

    return {
        "n": n,
        "tested": tested,
        "max_period": max_period,
        "passed": int(passed),
        "witness": witness,
        "exhausted": int(exhausted),
        "seconds": round(time.perf_counter() - start, 4),
    }


def reference_status(info: str) -> str:
    if info == "Unknown":
        return "feedback_unknown"
    if info in REFERENCE_NAMES:
        return "named_reference"
    if info:
        return "other_named"
    return "unlisted"


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe listed SATD rules for small-board periods.")
    parser.add_argument("input", help="Text file copied from CA_Rule_Search.html")
    parser.add_argument("--out", default="rule_period_probe_results.csv", help="CSV output path")
    parser.add_argument("--threshold", type=int, default=8, help="Pass when period is at least this value")
    parser.add_argument("--max-steps", type=int, default=10000, help="Maximum steps per pattern")
    parser.add_argument("--samples", type=int, default=2000, help="Random samples per board size for n >= 5")
    parser.add_argument("--time-per-rule-size", type=float, default=2.0, help="Seconds per rule per board size")
    parser.add_argument("--full-5", action="store_true", help="Also exhaustively scan canonical balanced 5x5 states")
    parser.add_argument("--seed", type=int, default=12345)
    args = parser.parse_args()

    text = open(args.input, "r", encoding="utf-8").read()
    rules = parse_rules(text)
    if not rules:
        print("No visible rules parsed. Copy the table as tab-separated text into a file.", file=sys.stderr)
        return 2

    rng = random.Random(args.seed)
    rows: list[dict[str, object]] = []
    print(f"Parsed {len(rules)} visible rules.")
    for index, rule in enumerate(rules, 1):
        status = reference_status(rule.info)
        print(f"[{index}/{len(rules)}] {rule.number} {rule.compact} {rule.info or '-'}")
        for n in range(4, 9):
            exhaustive = n == 4 or (n == 5 and args.full_5)
            result = probe_rule(
                rule,
                n=n,
                threshold=args.threshold,
                max_steps=args.max_steps,
                samples=args.samples,
                time_limit=args.time_per_rule_size,
                exhaustive=exhaustive,
                rng=rng,
            )
            rows.append({
                "rank": rule.rank,
                "number": rule.number,
                "compact": rule.compact,
                "full_satd": rule.genome,
                "info": rule.info,
                "reference_status": status,
                "current_samples": rule.samples,
                "current_score": rule.score,
                "current_nearest": rule.nearest,
                **result,
            })
            print(
                f"  {n}x{n}: max_period={result['max_period']} "
                f"tested={result['tested']} passed={result['passed']} seconds={result['seconds']}"
            )

    fieldnames = [
        "rank", "number", "compact", "full_satd", "info", "reference_status",
        "current_samples", "current_score", "current_nearest",
        "n", "tested", "max_period", "passed", "witness", "exhausted", "seconds",
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
