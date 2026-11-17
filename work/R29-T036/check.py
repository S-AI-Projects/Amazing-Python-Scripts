#!/usr/bin/env python3
"""
Test runner for R29-T036: Simplify one responsibility in start (script.py) [Telegram Bot code].
Executes refactored checks, verifies response calculation isolation,
and records inputs, outputs, and tool versions under work/R29-T036/.
"""

import os
import sys
import json
import unittest
from unittest.mock import MagicMock

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T036")
BOT_DIR = os.path.join(ROOT_DIR, "Telegram Bot code")

if BOT_DIR not in sys.path:
    sys.path.insert(0, BOT_DIR)

import script
import test_script


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T036",
        "target": "Telegram Bot code/script.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Smallest input (no user details)
    mock_up = MagicMock()
    mock_up.effective_user = None
    mock_up.message.reply_text = MagicMock(return_value="replied")
    script.start(mock_up)
    expected_msg = "Hello! I'm your Telegram bot. How can I assist you?"
    test_1 = {
        "name": "smallest_valid_input_start",
        "source_preconditions": "Telegram Bot code/script.py lines 11, 25-27",
        "input": {"user_name": None},
        "expected": expected_msg,
        "actual": mock_up.message.reply_text.call_args[0][0],
        "passed": mock_up.message.reply_text.call_args[0][0] == expected_msg
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary input (user with first_name)
    mock_up2 = MagicMock()
    mock_up2.effective_user.first_name = "Alice"
    mock_up2.message.reply_text = MagicMock(return_value="replied_alice")
    script.start(mock_up2)
    expected_msg_ord = "Hello Alice! I'm your Telegram bot. How can I assist you?"
    test_2 = {
        "name": "ordinary_input_start",
        "source_preconditions": "Telegram Bot code/script.py lines 11, 25-27",
        "input": {"user_name": "Alice"},
        "expected": expected_msg_ord,
        "actual": mock_up2.message.reply_text.call_args[0][0],
        "passed": mock_up2.message.reply_text.call_args[0][0] == expected_msg_ord
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # 3. Direct helper test
    test_3 = {
        "name": "build_welcome_message_helper",
        "source_preconditions": "Telegram Bot code/script.py lines 11-18",
        "passed": (script.build_welcome_message(None) == expected_msg and
                   script.build_welcome_message("Bob") == "Hello Bob! I'm your Telegram bot. How can I assist you?")
    }
    evidence["tests"].append(test_3)
    if not test_3["passed"]:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_script)
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
