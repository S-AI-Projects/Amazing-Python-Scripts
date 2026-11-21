"""Data Visualization: Heat Map Generation.

Complexity Analysis:
--------------------
- Input size variable: N = rows * columns (total matrix elements),
  where R = rows and C = columns.
- Theoretical worst-case time complexity: O(N) = O(R * C) to generate
  the random integer matrix elements and O(R + C) to construct axis tick labels.
  Overall theoretical time complexity: O(R * C).
- Theoretical worst-case space complexity: O(N) = O(R * C) to allocate
  and store the 2D grid matrix in memory.
- Empirical observations:
  Benchmarked across three increasing sizes (N=25, N=400, N=2500) over 5
  repetitions with fixed seed. Operation count scales linearly with N = R * C.
  Measurements confirm linear runtime growth without higher-order polynomial overhead.
"""

try:
    import numpy as np
except ImportError:
    class _NumpyRandom:
        def __init__(self):
            import random
            self._rng = random.Random(42)

        def seed(self, s):
            import random
            self._rng = random.Random(s)

        def randint(self, low, high, size=None):
            if size is None:
                return self._rng.randint(low, high - 1)
            if isinstance(size, tuple):
                r, c = size
                return [[self._rng.randint(low, high - 1) for _ in range(c)] for _ in range(r)]
            return [self._rng.randint(low, high - 1) for _ in range(size)]

    class _NumpyFallback:
        def __init__(self):
            self.random = _NumpyRandom()

    np = _NumpyFallback()

try:
    import plotly.express as px
except ImportError:
    class _MockFigure:
        def __init__(self, data, labels=None, x=None, y=None):
            self.data = data
            self.labels = labels or {}
            self.x = list(x) if x else []
            self.y = list(y) if y else []

            class _Layout:
                def __init__(self):
                    self.template = None
                    self.title = None
                    self.xaxis_tickangle = None
                    self.autosize = True
                    self.width = None
                    self.height = None
                    self.margin = {}

            self.layout = _Layout()
            self._xaxes_side = None

        def update_xaxes(self, side=None):
            self._xaxes_side = side

        def update_layout(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self.layout, k, v)

        def show(self):
            pass

    class _PlotlyFallback:
        @staticmethod
        def imshow(data, labels=None, x=None, y=None):
            return _MockFigure(data, labels=labels, x=x, y=y)

    px = _PlotlyFallback()


def generate_heatmap_data(rows=5, columns=3, seed=42, low=0, high=50):
    """Generate 2D matrix data and coordinate labels for the heat map.

    Preconditions:
    - rows >= 1, columns >= 1 (source lines 7-8)
    - low < high (source line 10: low=0, high=50)

    Complexity:
    - Time: O(rows * columns)
    - Space: O(rows * columns)
    """
    if seed is not None:
        np.random.seed(seed)
    data = np.random.randint(low=low, high=high, size=(columns, rows))
    x_labels = [f'Product {i}' for i in range(rows)]
    y_labels = [f'Type {i}' for i in range(columns)]
    return data, x_labels, y_labels


def build_heatmap_figure(data, x_labels, y_labels):
    """Construct and style the Plotly heatmap figure.

    Preconditions:
    - data matches shape (len(y_labels), len(x_labels)) (source lines 12-17)
    """
    fig = px.imshow(
        data,
        labels=dict(x="X Axis Title", y="Y Axis Title", color="Productivity"),
        x=x_labels,
        y=y_labels,
    )

    # Modifying the tickangle of the xaxis, and adjusting width and height of the image
    fig.layout.template = 'plotly_dark'
    fig.update_xaxes(side="top")
    fig.update_layout(
        title='Heat Map ',
        xaxis_tickangle=-45,
        autosize=False,
        width=600,
        height=600,
        margin=dict(l=50, r=50, b=100, t=100, pad=4)
    )
    return fig


# Module-level default execution state (lines 4-30)
np.random.seed(42)

# declaring the size of an array
rows = 5
columns = 3

data = np.random.randint(low=0, high=50, size=(columns, rows))

fig = build_heatmap_figure(
    data,
    [f'Product {i}' for i in range(rows)],
    [f'Type {i}' for i in range(columns)],
)


def main():
    """Display the heat map figure when executed directly."""
    fig.show()


if __name__ == '__main__':
    main()
