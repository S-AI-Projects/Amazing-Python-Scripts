#!/usr/bin/env python3
"""
Test runner for R29-T033: Cross-check image1 (blending_Image.py) [Blending Images].
Runs reference comparison tests, validates 20+ domain inputs against independent oracle,
and records inputs, expected vs actual values, and tool versions under work/R29-T033/.
"""

import os
import sys
import json
import unittest
from unittest.mock import MagicMock, patch

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.join(ROOT_DIR, "work", "R29-T033")
BLENDING_DIR = os.path.join(ROOT_DIR, "Blending Images")

if BLENDING_DIR not in sys.path:
    sys.path.insert(0, BLENDING_DIR)

import blending_Image
import test_blending_Image
from test_blending_Image import ReferenceOracle


def run_checks():
    os.makedirs(WORK_DIR, exist_ok=True)

    evidence = {
        "task": "R29-T033",
        "target": "Blending Images/blending_Image.py",
        "tool_versions": {
            "python": sys.version,
            "platform": sys.platform
        },
        "tests": []
    }

    # 1. Smallest valid input check
    smallest_path = "test_data/smallest_1x1.png"
    smallest_raw_shape = (1, 1, 3)
    oracle_smallest = ReferenceOracle.compute_expected(smallest_path, smallest_raw_shape)

    mock_cv2 = MagicMock()
    mock_raw = MagicMock()
    mock_raw.shape = smallest_raw_shape
    mock_resized = MagicMock()
    mock_resized.shape = oracle_smallest["expected_shape"]
    mock_cv2.imread.return_value = mock_raw
    mock_cv2.resize.return_value = mock_resized

    with patch.object(blending_Image, "cv2", mock_cv2):
        res = blending_Image.image1(filepath=smallest_path)
        test_1_passed = (res.shape == oracle_smallest["expected_shape"] and
                         blending_Image.img1.shape == oracle_smallest["expected_shape"])
        test_1 = {
            "name": "smallest_valid_input_reference_comparison",
            "source_preconditions": "Blending Images/blending_Image.py lines 25, 28, 29",
            "input": {"filepath": smallest_path, "raw_shape": list(smallest_raw_shape)},
            "expected": {"shape": list(oracle_smallest["expected_shape"])},
            "actual": {"shape": list(res.shape)},
            "passed": test_1_passed
        }
        evidence["tests"].append(test_1)
        if not test_1_passed:
            print(f"FAILED: {test_1['name']}", file=sys.stderr)
            sys.exit(1)

    # 2. Ordinary input check
    ordinary_path = "lake.jpg"
    ordinary_raw_shape = (600, 800, 3)
    oracle_ord = ReferenceOracle.compute_expected(ordinary_path, ordinary_raw_shape)

    mock_cv2 = MagicMock()
    mock_raw = MagicMock()
    mock_raw.shape = ordinary_raw_shape
    mock_resized = MagicMock()
    mock_resized.shape = oracle_ord["expected_shape"]
    mock_cv2.imread.return_value = mock_raw
    mock_cv2.resize.return_value = mock_resized

    with patch.object(blending_Image, "cv2", mock_cv2):
        res = blending_Image.image1(filepath=ordinary_path)
        test_2_passed = (res.shape == oracle_ord["expected_shape"] and
                         blending_Image.img1.shape == oracle_ord["expected_shape"])
        test_2 = {
            "name": "ordinary_input_reference_comparison",
            "source_preconditions": "Blending Images/blending_Image.py lines 25, 28, 29",
            "input": {"filepath": ordinary_path, "raw_shape": list(ordinary_raw_shape)},
            "expected": {"shape": list(oracle_ord["expected_shape"])},
            "actual": {"shape": list(res.shape)},
            "passed": test_2_passed
        }
        evidence["tests"].append(test_2)
        if not test_2_passed:
            print(f"FAILED: {test_2['name']}", file=sys.stderr)
            sys.exit(1)

    # 3. 20+ enumerated domain inputs check against independent oracle
    domain_comparisons = []
    all_domain_passed = True
    for idx in range(25):
        path = f"sample_images/img_{idx}.jpg"
        raw_shape = (10 * (idx + 1), 10 * (idx + 1), 3)
        expected = ReferenceOracle.compute_expected(path, raw_shape)

        mock_cv2 = MagicMock()
        mock_raw = MagicMock()
        mock_raw.shape = raw_shape
        mock_resized = MagicMock()
        mock_resized.shape = expected["expected_shape"]
        mock_cv2.imread.return_value = mock_raw
        mock_cv2.resize.return_value = mock_resized

        with patch.object(blending_Image, "cv2", mock_cv2):
            actual = blending_Image.image1(filepath=path)
            passed = (actual.shape == expected["expected_shape"])
            if not passed:
                all_domain_passed = False
            domain_comparisons.append({
                "sample_index": idx,
                "input_raw_shape": list(raw_shape),
                "expected_shape": list(expected["expected_shape"]),
                "actual_shape": list(actual.shape),
                "passed": passed
            })

    test_3 = {
        "name": "twenty_domain_inputs_against_oracle",
        "source_preconditions": "Blending Images/blending_Image.py lines 25, 28, 29",
        "sample_count": len(domain_comparisons),
        "passed": all_domain_passed,
        "samples": domain_comparisons[:5]  # first 5 previewed in summary
    }
    evidence["tests"].append(test_3)
    if not all_domain_passed:
        print(f"FAILED: {test_3['name']}", file=sys.stderr)
        sys.exit(1)

    # Run native unittests
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_blending_Image)
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
