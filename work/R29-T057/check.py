#!/usr/bin/env python3
"""Automated check runner for R29-T057.

Task: Publish a runnable example for FacebookLogin (script.py) [Automate Facebook bot]
Target: Automate Facebook bot/script.py
"""

import io
import json
import os
import platform
import sys
import unittest
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
REPO_ROOT = WORK_DIR.parent.parent
MODULE_DIR = REPO_ROOT / "Automate Facebook bot"

# Add paths for imports
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import module and tests
import script
from tests.test_script import TestFacebookLogin


def run_checks():
    """Run focused unit tests and record evidence."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFacebookLogin)

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    output = stream.getvalue()
    print(output)

    # Prepare evidence dictionary
    evidence = {
        "task": "R29-T057",
        "item": "Automate Facebook bot",
        "target_file": "Automate Facebook bot/script.py",
        "class_documented": "FacebookLogin",
        "source_data_anchors": {
            "source_line_login_url": "Line 10: LOGIN_URL = 'https://www.facebook.com/login.php'",
            "source_line_groupid": "Line 13: groupid = []",
            "source_lines_init": "Lines 22-31: FacebookLogin.__init__ credentials & navigation",
            "source_lines_login": "Lines 34-44: FacebookLogin.login authentication submission",
            "source_lines_loop": "Lines 45-60: Group broadcast loop"
        },
        "fixtures": {
            "smallest_valid_input": {
                "email": "test_user@example.com",
                "password": "password123",
                "groupid": [],
                "expected_displayed_output": "",
                "expected_final_url": "https://www.facebook.com/login.php",
                "expected_visited_urls": ["https://www.facebook.com/login.php"]
            },
            "ordinary_input": {
                "email": "ordinary_user@example.com",
                "password": "secure_password_456",
                "groupid": ["123456789"],
                "expected_displayed_output": "Waiting for few seconds .......\n",
                "expected_final_url": "https://facebook.com/groups/123456789",
                "expected_visited_urls": [
                    "https://www.facebook.com/login.php",
                    "https://facebook.com/groups/123456789"
                ]
            }
        },
        "decisive_state_transitions": [
            "Transition 1: Authentication session transition (login credentials entered and loginbutton clicked)",
            "Transition 2: Group broadcast loop transition (evaluating groupid = [] vs non-empty group URLs and submitting post)"
        ],
        "python_version": sys.version,
        "platform": platform.platform(),
        "tests_run": result.testsRun,
        "errors": len(result.errors),
        "failures": len(result.failures),
        "successful": result.wasSuccessful()
    }

    results_json_path = WORK_DIR / "results.json"
    results_txt_path = WORK_DIR / "results.txt"

    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)

    with open(results_txt_path, "w", encoding="utf-8") as f:
        f.write(f"Task: R29-T057 Check Results\n")
        f.write(f"Target: Automate Facebook bot/script.py\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Tests run: {result.testsRun}\n")
        f.write(f"Failures: {len(result.failures)}\n")
        f.write(f"Errors: {len(result.errors)}\n")
        f.write(f"Status: {'PASSED' if result.wasSuccessful() else 'FAILED'}\n\n")
        f.write("Output:\n")
        f.write(output)

    if not result.wasSuccessful():
        print(f"FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
        sys.exit(1)

    print(f"SUCCESS: All {result.testsRun} checks passed.")
    sys.exit(0)


if __name__ == '__main__':
    run_checks()
