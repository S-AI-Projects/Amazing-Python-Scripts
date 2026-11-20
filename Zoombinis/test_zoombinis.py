import unittest
import random
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from Zoombinis import setup_teams, ZOOMBINIS_PER_TEAM


def reference_setup_teams(num_teams=2, team_size=8, rand_fn=None):
    """
    Independent reference implementation for Zoombinis team generation.
    Generates a list of lists of length team_size with values in [1, 4].
    """
    if rand_fn is None:
        rand_fn = random.randint
    result = []
    for _ in range(num_teams):
        members = [rand_fn(1, 4) for _ in range(team_size)]
        result.append(members)
    return result


class TestZoombinisDifferential(unittest.TestCase):
    """
    Differential cross-check tests comparing setup_teams against reference_setup_teams.
    Anchors cited:
      - Line 25: teams = []
      - Line 27: team = []
      - Line 29: integer values in range [1, 4]
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: num_teams=1, team_size=1.
        Precondition: Line 25 (teams = []), Line 27 (team = []).
        """
        rng_seed = 101

        # Predictable mock generator
        def make_rng(seed):
            r = random.Random(seed)
            return lambda a, b: r.randint(a, b)

        actual = setup_teams(num_teams=1, team_size=1, rng=make_rng(rng_seed))
        expected = reference_setup_teams(num_teams=1, team_size=1, rand_fn=make_rng(rng_seed))

        # Explicit expected literal calculated independently for seed 101
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 1)
        self.assertEqual(len(actual[0]), 1)
        self.assertTrue(1 <= actual[0][0] <= 4)

    def test_ordinary_input_cross_check(self):
        """
        Ordinary input: 2 teams of 8 members (standard 16 Zoombinis).
        Preconditions: Line 25, Line 27.
        """
        rng_seed = 42

        def make_rng(seed):
            r = random.Random(seed)
            return lambda a, b: r.randint(a, b)

        actual = setup_teams(num_teams=2, team_size=8, rng=make_rng(rng_seed))
        expected = reference_setup_teams(num_teams=2, team_size=8, rand_fn=make_rng(rng_seed))

        # Check structured equivalence
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 2)
        self.assertTrue(all(len(t) == 8 for t in actual))
        self.assertTrue(all(1 <= val <= 4 for t in actual for val in t))

    def test_default_behavior_shape_and_range(self):
        """
        Tests default invocation setup_teams() without explicit arguments.
        Preserves original signature and public contract.
        """
        teams = setup_teams()
        self.assertIsInstance(teams, list)
        self.assertEqual(len(teams), 2)
        for team in teams:
            self.assertIsInstance(team, list)
            self.assertEqual(len(team), ZOOMBINIS_PER_TEAM)
            for member in team:
                self.assertIsInstance(member, int)
                self.assertIn(member, [1, 2, 3, 4])

    def test_independent_rng_streams_equivalence(self):
        """
        Cross-checks across multiple distinct random seeds.
        """
        for seed in [1, 7, 99, 12345]:
            def make_rng(s):
                r = random.Random(s)
                return lambda a, b: r.randint(a, b)

            actual = setup_teams(num_teams=2, team_size=8, rng=make_rng(seed))
            reference = reference_setup_teams(num_teams=2, team_size=8, rand_fn=make_rng(seed))
            self.assertEqual(actual, reference, f"Mismatch at seed {seed}")


if __name__ == '__main__':
    unittest.main()
