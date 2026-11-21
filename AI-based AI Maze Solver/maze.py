import heapq
import random


class MazeSolver:
    """
    AI-based Maze Solver using A* search.

    Supported Domain Boundary Contract:
    - Precondition Anchors:
      - Line 7: self.maze = maze (reference to 2D grid)
      - Line 8: self.rows = len(maze)
      - Line 9: self.cols = len(maze[0]) (requires len(maze) >= 1)
      - Line 10: self.start = (0, 0)
      - Line 11: self.goal = (self.rows - 1, self.cols - 1)
    - Valid Boundary (Smallest valid input):
      1x1 grid: maze = [[0]] (or [[False]]).
      start = (0, 0), goal = (0, 0). solve() returns [(0, 0)].
    - Valid Interior (Ordinary input):
      R x C grid with R >= 1, C >= 1 (e.g. 2x2, 3x3).
    - Valid Boundaries (Dimensional):
      - 1xN single-row grid (e.g. [[0, 0, 0]], goal = (0, N - 1))
      - Nx1 single-column grid (e.g. [[0], [0], [0]], goal = (N - 1, 0))
    - Valid Boundary (Unsolvable / Blocked):
      When no path exists between start and goal, solve() returns None.
    - Unsupported Boundary:
      Empty list maze = [] raises IndexError at line 9 (len(maze[0])).
    - Immutability:
      Solver does not mutate caller's input maze structure.
    """

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)

    def get_neighbors(self, node):
        row, col = node
        neighbors = []
        if row > 0 and not self.maze[row - 1][col]:
            neighbors.append((row - 1, col))
        if row < self.rows - 1 and not self.maze[row + 1][col]:
            neighbors.append((row + 1, col))
        if col > 0 and not self.maze[row][col - 1]:
            neighbors.append((row, col - 1))
        if col < self.cols - 1 and not self.maze[row][col + 1]:
            neighbors.append((row, col + 1))
        return neighbors

    def heuristic(self, node):
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def solve(self):
        open_set = []
        closed_set = set()
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}
        heapq.heappush(open_set, (f_score[self.start], self.start))

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == self.goal:
                path = []
                while current in g_score:
                    path.append(current)
                    current = g_score[current]
                return path[::-1]

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + \
                        self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None


def generate_random_maze(rows, cols, obstacle_probability):
    return [[random.random() < obstacle_probability for _ in range(cols)] for _ in range(rows)]


def print_maze(maze):
    for row in maze:
        print("".join(["#" if cell else " " for cell in row]))


def main():
    rows = 10
    cols = 10
    obstacle_probability = 0.2

    maze = generate_random_maze(rows, cols, obstacle_probability)
    print("Random Maze:")
    print_maze(maze)

    maze_solver = MazeSolver(maze)
    path = maze_solver.solve()

    if path:
        print("\nSolution Path:")
        for node in path:
            maze[node[0]][node[1]] = True  # Marking the path in the maze
        print_maze(maze)
    else:
        print("\nNo path found!")


if __name__ == "__main__":
    main()
