"""Contract, regression, and complexity tests for heat_maps.py in Data-Visualization.

Issue: R29-T059
Target: Data-Visualization/HeatMap/heat_maps.py
Preconditions:
- Precondition 1: np.random.seed(42) established at line 4
- Precondition 2: Grid dimensions rows = 5, columns = 3 established at lines 7-8
- Precondition 3: Random integer range low = 0, high = 50 established at line 10
- Precondition 4: Axis label format established at lines 15-16
- Precondition 5: Figure layout configuration established at lines 20-29
"""

import sys
import unittest
from pathlib import Path

# Add project root and module directory to path for clean import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_DIR = REPO_ROOT / "Data-Visualization" / "HeatMap"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import heat_maps


class TestHeatMapComplexity(unittest.TestCase):
    """Correctness and scaling tests for HeatMap generation."""

    def test_smallest_valid_input(self):
        """Precondition: Line 7-8 define rows and columns as positive integers.
        Smallest valid input: 1x1 matrix (rows = 1, columns = 1, N = 1).
        Precondition: Line 10 specifies low = 0, high = 50.
        Precondition: Line 15-16 specifies x=['Product 0'], y=['Type 0'].

        Literal inputs:
        - rows = 1, columns = 1, seed = 42

        Independently calculated expected outputs:
        - data has length 1 (columns = 1)
        - data[0] has length 1 (rows = 1)
        - 0 <= data[0][0] < 50
        - x_labels == ['Product 0']
        - y_labels == ['Type 0']
        - Figure title == 'Heat Map '
        - Figure width == 600, height == 600
        """
        data, x_labels, y_labels = heat_maps.generate_heatmap_data(rows=1, columns=1, seed=42)

        # Dimension assertions
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data[0]), 1)
        val = int(data[0][0])
        self.assertGreaterEqual(val, 0)
        self.assertLess(val, 50)

        # Label assertions
        self.assertEqual(x_labels, ['Product 0'])
        self.assertEqual(y_labels, ['Type 0'])

        # Figure construction assertions
        fig = heat_maps.build_heatmap_figure(data, x_labels, y_labels)
        self.assertEqual(fig.layout.title, 'Heat Map ')
        self.assertEqual(fig.layout.width, 600)
        self.assertEqual(fig.layout.height, 600)
        self.assertEqual(fig.layout.xaxis_tickangle, -45)

    def test_ordinary_input(self):
        """Precondition: Lines 7-8 establish default rows = 5, columns = 3.
        Precondition: Line 10 establishes low = 0, high = 50.
        Precondition: Line 15 establishes x = ['Product 0' ... 'Product 4'].
        Precondition: Line 16 establishes y = ['Type 0' ... 'Type 2'].

        Literal inputs:
        - rows = 5, columns = 3, seed = 42

        Independently calculated expected outputs:
        - data has 3 rows (columns = 3), each of length 5 (rows = 5)
        - Total elements: 15
        - All elements in range [0, 50)
        - x_labels == ['Product 0', 'Product 1', 'Product 2', 'Product 3', 'Product 4']
        - y_labels == ['Type 0', 'Type 1', 'Type 2']
        """
        data, x_labels, y_labels = heat_maps.generate_heatmap_data(rows=5, columns=3, seed=42)

        self.assertEqual(len(data), 3)
        for row in data:
            self.assertEqual(len(row), 5)
            for val in row:
                int_val = int(val)
                self.assertGreaterEqual(int_val, 0)
                self.assertLess(int_val, 50)

        expected_x = ['Product 0', 'Product 1', 'Product 2', 'Product 3', 'Product 4']
        expected_y = ['Type 0', 'Type 1', 'Type 2']
        self.assertEqual(x_labels, expected_x)
        self.assertEqual(y_labels, expected_y)

    def test_module_level_attributes_preserved(self):
        """Verify that default module-level attributes match original script."""
        self.assertEqual(heat_maps.rows, 5)
        self.assertEqual(heat_maps.columns, 3)
        self.assertEqual(len(heat_maps.data), 3)
        self.assertEqual(len(heat_maps.data[0]), 5)
        self.assertEqual(heat_maps.fig.layout.title, 'Heat Map ')
        self.assertEqual(heat_maps.fig.layout.width, 600)
        self.assertEqual(heat_maps.fig.layout.height, 600)

    def test_seed_reproducibility(self):
        """Verify that identical seeds produce identical matrix outputs."""
        data1, x1, y1 = heat_maps.generate_heatmap_data(rows=4, columns=4, seed=123)
        data2, x2, y2 = heat_maps.generate_heatmap_data(rows=4, columns=4, seed=123)

        self.assertEqual(x1, x2)
        self.assertEqual(y1, y2)
        for r1, r2 in zip(data1, data2):
            self.assertEqual(list(r1), list(r2))

    def test_scaling_correctness_across_increasing_sizes(self):
        """Verify correctness across 3 increasing benchmark sizes (N = 25, 400, 2500)."""
        sizes = [(5, 5), (20, 20), (50, 50)]
        for r, c in sizes:
            data, x_labels, y_labels = heat_maps.generate_heatmap_data(rows=r, columns=c, seed=42)
            self.assertEqual(len(data), c)
            self.assertEqual(len(data[0]), r)
            self.assertEqual(len(x_labels), r)
            self.assertEqual(len(y_labels), c)


if __name__ == '__main__':
    unittest.main()
