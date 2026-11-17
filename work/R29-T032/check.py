#!/usr/bin/env python3
"""
Test runner for R29-T032: Define the supported boundaries of Card (blackjack.py).
Executes boundary checks for Card, verifies outputs and non-mutation, and records
evidence under work/R29-T032/.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T032")
BLACKJACK_DIR = os.path.join(ROOT_DIR, "Blackjack")

if BLACKJACK_DIR not in sys.path:
    sys.path.insert(0, BLACKJACK_DIR)

import blackjack
import test_blackjack


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T032",
        "target": "Blackjack/blackjack.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "boundary_table": {
            "suits_contract": list(blackjack.Deck.suits),
            "ranks_contract": list(blackjack.Deck.ranks),
            "smallest_supported": {
                "suit": blackjack.Deck.suits[0],
                "rank": blackjack.Deck.ranks[0]
            },
            "upper_supported": {
                "suit": blackjack.Deck.suits[-1],
                "rank": blackjack.Deck.ranks[-1]
            }
        },
        "tests": []
    }

    # 1. Smallest valid boundary input ('Hearts', 'Two')
    card_min = blackjack.Card("Hearts", "Two")
    actual_min = {
        "suit": card_min.suit,
        "rank": card_min.rank,
        "str": str(card_min)
    }
    expected_min = {
        "suit": "Hearts",
        "rank": "Two",
        "str": "Two of Hearts"
    }
    test_1 = {
        "name": "smallest_valid_boundary_input",
        "source_preconditions": "Blackjack/blackjack.py lines 25, 29, 35, 36",
        "input": {"suit": "Hearts", "rank": "Two"},
        "expected": expected_min,
        "actual": actual_min,
        "passed": actual_min == expected_min
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary interior input ('Spades', 'Seven')
    card_ord = blackjack.Card("Spades", "Seven")
    actual_ord = {
        "suit": card_ord.suit,
        "rank": card_ord.rank,
        "str": str(card_ord)
    }
    expected_ord = {
        "suit": "Spades",
        "rank": "Seven",
        "str": "Seven of Spades"
    }
    test_2 = {
        "name": "ordinary_interior_input",
        "source_preconditions": "Blackjack/blackjack.py lines 25, 29, 35, 36",
        "input": {"suit": "Spades", "rank": "Seven"},
        "expected": expected_ord,
        "actual": actual_ord,
        "passed": actual_ord == expected_ord
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # 3. Upper boundary input ('Clubs', 'Ace')
    card_max = blackjack.Card("Clubs", "Ace")
    actual_max = {
        "suit": card_max.suit,
        "rank": card_max.rank,
        "str": str(card_max)
    }
    expected_max = {
        "suit": "Clubs",
        "rank": "Ace",
        "str": "Ace of Clubs"
    }
    test_3 = {
        "name": "upper_supported_boundary_input",
        "source_preconditions": "Blackjack/blackjack.py lines 25, 29, 35, 36",
        "input": {"suit": "Clubs", "rank": "Ace"},
        "expected": expected_max,
        "actual": actual_max,
        "passed": actual_max == expected_max
    }
    evidence["tests"].append(test_3)
    if not test_3["passed"]:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_blackjack)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    evidence["unittest_run"] = {
        "tests_run": result.testsRun,
        "was_successful": result.wasSuccessful(),
        "errors_count": len(result.errors),
        "failures_count": len(result.failures)
    }

    # Save evidence file
    evidence_file = os.path.join(WORK_DIR, "results.json")
    with open(evidence_file, "w") as f:
        json.dump(evidence, f, indent=2)

    print(f"\nAll checks passed successfully. Nonzero test count: {result.testsRun}")
    print(f"Evidence saved to {evidence_file}")

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    run_checks()
