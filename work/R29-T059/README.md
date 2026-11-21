# Task R29-T059: Measure the work done by Data Visualization (heat_maps.py)

## Overview
- **Item**: Data-Visualization
- **Target File**: `Data-Visualization/HeatMap/heat_maps.py`
- **Task Type**: Complexity experiment
- **Target Function**: `generate_heatmap_data` / `build_heatmap_figure`

---

## 1. Complexity Statement

### Input Size Variable
- Let $R = \text{rows}$ (number of products on the X axis).
- Let $C = \text{columns}$ (number of types on the Y axis).
- Total input size variable: $N = R \times C$ (total matrix elements generated).

### Theoretical Worst-Case Complexity
- **Time Complexity**: $\mathcal{O}(N) = \mathcal{O}(R \cdot C)$.
  - Generating $R \times C$ pseudo-random integer elements requires $\mathcal{O}(R \cdot C)$ operations.
  - Constructing string axis tick labels requires $\mathcal{O}(R + C)$ operations.
  - Total theoretical time complexity: $\mathcal{O}(R \cdot C)$.
- **Space Complexity**: $\mathcal{O}(N) = \mathcal{O}(R \cdot C)$ to allocate and store the 2D grid matrix in memory.

### Empirical Observations
- Benchmarked across 3 increasing input sizes over 5 repetitions with fixed seeds:
  - **Small** ($R=5, C=5, N=25$)
  - **Medium** ($R=20, C=20, N=400$)
  - **Large** ($R=50, C=50, N=2500$)
- Operation count scales strictly with $N = R \cdot C$.
- Algorithm execution time scales linearly with $N$, demonstrating $\mathcal{O}(N)$ empirical performance without higher-order polynomial overhead.
- Output correctness is verified outside the timed interval across all repetitions.

---

## 2. Preconditions and Fixtures

### Preconditions Table
| Precondition | Source Line | Description |
|---|---|---|
| Random Seed | Line 4 | `np.random.seed(42)` sets initial PRNG state |
| Matrix Dimensions | Lines 7–8 | `rows = 5`, `columns = 3` default dimensions |
| Integer Range | Line 10 | `np.random.randint(low=0, high=50, size=(columns, rows))` |
| Axis Labels | Lines 15–16 | `x=['Product i' for i in range(rows)]`, `y=['Type i' for i in range(columns)]` |
| Figure Layout | Lines 20–29 | `template='plotly_dark'`, `title='Heat Map '`, `width=600`, `height=600` |

### Fixtures
1. **Smallest Valid Input**:
   - `rows = 1, columns = 1, seed = 42` ($N = 1$).
   - Expected shape: $(1, 1)$, values in $[0, 50)$, $x=[\text{'Product 0'}]$, $y=[\text{'Type 0'}]$.
2. **Ordinary Input**:
   - `rows = 5, columns = 3, seed = 42` ($N = 15$).
   - Expected shape: $(3, 5)$, 15 values in $[0, 50)$, 5 $X$ labels, 3 $Y$ labels.

---

## 3. Automated Verification

Run checks locally:
```bash
python3 work/R29-T059/check.py
```
Or via unittest:
```bash
python3 -m unittest discover -s "Data-Visualization/tests" -p "test_heat_maps.py" -v
```
Evidence is stored in `work/R29-T059/results.json` and `work/R29-T059/results.txt`.
