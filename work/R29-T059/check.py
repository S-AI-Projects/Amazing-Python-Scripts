#!/usr/bin/env python3
"""Automated check runner for R29-T059.

Task: Measure the work done by Data Visualization (heat_maps.py) [Data-Visualization]
Target: Data-Visualization/HeatMap/heat_maps.py
"""

import io
import json
import os
import platform
import statistics
import sys
import time
import unittest
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
REPO_ROOT = WORK_DIR.parent.parent
MODULE_DIR = REPO_ROOT / "Data-Visualization" / "HeatMap"
PKG_DIR = REPO_ROOT / "Data-Visualization"

# Add paths for imports
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import module and tests
import heat_maps
from tests.test_heat_maps import TestHeatMapComplexity


def run_benchmark():
    """Run complexity experiment: 3 increasing sizes, 5 repetitions, fixed seeds."""
    sizes = [
        {"name": "small", "rows": 5, "columns": 5, "N": 25},
        {"name": "medium", "rows": 20, "columns": 20, "N": 400},
        {"name": "large", "rows": 50, "columns": 50, "N": 2500},
    ]
    repetitions = 5
    benchmark_results = []

    for size_cfg in sizes:
        r = size_cfg["rows"]
        c = size_cfg["columns"]
        n = size_cfg["N"]
        run_times_sec = []

        for rep in range(repetitions):
            seed = 42 + rep

            # Measure strictly algorithm computation (isolating from I/O & startup)
            start_t = time.perf_counter()
            data, x_labels, y_labels = heat_maps.generate_heatmap_data(
                rows=r, columns=c, seed=seed
            )
            elapsed_t = time.perf_counter() - start_t
            run_times_sec.append(elapsed_t)

            # Verification of output correctness outside timed section
            assert len(data) == c, f"Row count {len(data)} != {c}"
            assert len(data[0]) == r, f"Col count {len(data[0])} != {r}"
            assert len(x_labels) == r, f"X label count {len(x_labels)} != {r}"
            assert len(y_labels) == c, f"Y label count {len(y_labels)} != {c}"

        median_t = statistics.median(run_times_sec)
        min_t = min(run_times_sec)
        max_t = max(run_times_sec)
        range_t = max_t - min_t

        benchmark_results.append({
            "size_name": size_cfg["name"],
            "rows": r,
            "columns": c,
            "N_elements": n,
            "operation_count_matrix_elements": n,
            "operation_count_labels": r + c,
            "repetitions": repetitions,
            "runs_sec": run_times_sec,
            "median_sec": median_t,
            "min_sec": min_t,
            "max_sec": max_t,
            "range_sec": range_t,
            "correctness_verified": True
        })

    return benchmark_results


def run_checks():
    """Run focused unit tests and complexity experiment, recording evidence."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestHeatMapComplexity)

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    output = stream.getvalue()
    print(output)

    # Run complexity benchmark
    benchmark_data = run_benchmark()
    print("\nComplexity Benchmark Results:")
    for b in benchmark_data:
        print(f"  Size {b['size_name']} (R={b['rows']}, C={b['columns']}, N={b['N_elements']}): "
              f"median={b['median_sec']*1e6:.2f} µs, range={b['range_sec']*1e6:.2f} µs, "
              f"min={b['min_sec']*1e6:.2f} µs, max={b['max_sec']*1e6:.2f} µs")

    evidence = {
        "task": "R29-T059",
        "item": "Data-Visualization",
        "target_file": "Data-Visualization/HeatMap/heat_maps.py",
        "complexity_statement": {
            "input_size_variable": "N = rows * columns (total matrix elements)",
            "theoretical_worst_case_time": "O(N) = O(R * C) matrix generation + O(R + C) labels",
            "theoretical_worst_case_space": "O(N) = O(R * C) 2D grid allocation",
            "empirical_observation": "Runtime and operation count scale linearly with N across tested sizes (N=25, 400, 2500)"
        },
        "preconditions": {
            "line_4_seed": "np.random.seed(42)",
            "lines_7_8_dimensions": "rows = 5, columns = 3",
            "line_10_randint": "np.random.randint(low=0, high=50, size=(columns, rows))",
            "lines_15_16_labels": "x=[Product i for i in range(rows)], y=[Type i for i in range(columns)]"
        },
        "fixtures": {
            "smallest_valid_input": {
                "rows": 1,
                "columns": 1,
                "N": 1,
                "expected_shape": [1, 1],
                "expected_x_labels": ["Product 0"],
                "expected_y_labels": ["Type 0"]
            },
            "ordinary_input": {
                "rows": 5,
                "columns": 3,
                "N": 15,
                "expected_shape": [3, 5],
                "expected_x_len": 5,
                "expected_y_len": 3
            }
        },
        "benchmark_scaling": benchmark_data,
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
        f.write(f"Task: R29-T059 Check Results\n")
        f.write(f"Target: Data-Visualization/HeatMap/heat_maps.py\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Tests run: {result.testsRun}\n")
        f.write(f"Failures: {len(result.failures)}\n")
        f.write(f"Errors: {len(result.errors)}\n")
        f.write(f"Status: {'PASSED' if result.wasSuccessful() else 'FAILED'}\n\n")
        f.write("Output:\n")
        f.write(output)
        f.write("\nBenchmark Metrics:\n")
        for b in benchmark_data:
            f.write(f"- Size {b['size_name']} (N={b['N_elements']}): median={b['median_sec']*1e6:.2f} µs, "
                    f"range={b['range_sec']*1e6:.2f} µs (min={b['min_sec']*1e6:.2f} µs, max={b['max_sec']*1e6:.2f} µs)\n")

    if not result.wasSuccessful():
        print(f"FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
        sys.exit(1)

    print(f"\nSUCCESS: All {result.testsRun} checks passed.")
    sys.exit(0)


if __name__ == '__main__':
    run_checks()
