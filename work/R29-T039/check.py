#!/usr/bin/env python3
"""
Test runner for R29-T039: Measure the work done by Text_to_speech (text-to-speech.py) [Text-To-Speech].
Executes scaling measurement checks distinguishing algorithm operations from I/O,
and records inputs, measurements, and tool versions under work/R29-T039/.
"""

import os
import sys
import json
import unittest
from unittest.mock import MagicMock

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T039")
TTS_DIR = os.path.join(ROOT_DIR, "Text-To-Speech")

if TTS_DIR not in sys.path:
    sys.path.insert(0, TTS_DIR)

tts_module = __import__("text-to-speech")
import test_tts


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T039",
        "target": "Text-To-Speech/text-to-speech.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    mock_speech = MagicMock()
    mock_gtts = MagicMock(return_value=mock_speech)
    mock_player = MagicMock()
    mock_cleaner = MagicMock()

    # 1. Smallest input measurement
    min_text = "a"
    res_min = tts_module.Text_to_speech(min_text, mock_gtts, mock_player, mock_cleaner)
    test_1 = {
        "name": "smallest_valid_input_measurement",
        "source_preconditions": "Text-To-Speech/text-to-speech.py lines 36-40",
        "input": min_text,
        "measurements": {
            "text_length": res_min["text_length"],
            "char_operations": res_min["char_operations"],
            "word_count": res_min["word_count"]
        },
        "passed": (res_min["text_length"] == 1 and res_min["char_operations"] == 1)
    }
    evidence["tests"].append(test_1)
    if not test_1["passed"]:
        print(f"FAILED: {test_1['name']}", file=sys.stderr)
        sys.exit(1)

    # 2. Ordinary input measurement
    ord_text = "Convert your Text into Voice"
    res_ord = tts_module.Text_to_speech(ord_text, mock_gtts, mock_player, mock_cleaner)
    test_2 = {
        "name": "ordinary_input_measurement",
        "source_preconditions": "Text-To-Speech/text-to-speech.py lines 36-40",
        "input": ord_text,
        "measurements": {
            "text_length": res_ord["text_length"],
            "char_operations": res_ord["char_operations"],
            "word_count": res_ord["word_count"]
        },
        "passed": (res_ord["text_length"] == len(ord_text) and res_ord["char_operations"] == len(ord_text))
    }
    evidence["tests"].append(test_2)
    if not test_2["passed"]:
        print(f"FAILED: {test_2['name']}", file=sys.stderr)
        sys.exit(1)

    # 3. Scaling across sizes
    scaling_series = []
    sizes = [10, 50, 100, 200, 500]
    all_scaled = True
    for s in sizes:
        txt = "A" * s
        r = tts_module.Text_to_speech(txt, mock_gtts, mock_player, mock_cleaner)
        scaling_series.append({"input_size": s, "operations": r["char_operations"]})
        if r["char_operations"] != s:
            all_scaled = False

    test_3 = {
        "name": "linear_scaling_series",
        "source_preconditions": "Text-To-Speech/text-to-speech.py lines 36-40",
        "complexity": "O(N)",
        "scaling_series": scaling_series,
        "passed": all_scaled
    }
    evidence["tests"].append(test_3)
    if not all_scaled:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_tts)
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
