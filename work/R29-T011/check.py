"""
Focused contract checks for Flappy Bird Game welcomeScreen function
"""
import sys
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Flappy-Bird-Game" / "main.py"

# Mock pygame before importing source
mock_pygame = MagicMock()
mock_locals = MagicMock()

QUIT_VAL = 1
KEYDOWN_VAL = 2
K_ESCAPE_VAL = 3
K_SPACE_VAL = 4
K_UP_VAL = 5

mock_locals.QUIT = QUIT_VAL
mock_locals.KEYDOWN = KEYDOWN_VAL
mock_locals.K_ESCAPE = K_ESCAPE_VAL
mock_locals.K_SPACE = K_SPACE_VAL
mock_locals.K_UP = K_UP_VAL

mock_pygame.locals = mock_locals
mock_pygame.QUIT = QUIT_VAL
mock_pygame.KEYDOWN = KEYDOWN_VAL
mock_pygame.K_ESCAPE = K_ESCAPE_VAL
mock_pygame.K_SPACE = K_SPACE_VAL
mock_pygame.K_UP = K_UP_VAL

sys.modules["pygame"] = mock_pygame
sys.modules["pygame.locals"] = mock_locals

import importlib.util
spec = importlib.util.spec_from_file_location("flappy_main", str(SOURCE_PATH))
flappy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flappy)


class WelcomeScreenContractTests(unittest.TestCase):

    def setUp(self):
        # Reset mocks and sprites before each test
        mock_pygame.reset_mock()
        mock_pygame.event.get.side_effect = None
        self.mock_screen = MagicMock()
        flappy.SCREEN = self.mock_screen
        flappy.FPSCLOCK = MagicMock()

    def test_smallest_valid_input(self):
        # Preconditions established at source lines:
        # SCREENWIDTH = 289 (line 8)
        # SCREENHEIGHT = 511 (line 9)
        # GAME_SPRITES = {} (line 13)
        # GAME_SOUNDS = {} (line 14)
        player_mock = MagicMock()
        player_mock.get_height.return_value = 1
        message_mock = MagicMock()
        message_mock.get_width.return_value = 1

        initial_sprites = {
            "player": player_mock,
            "message": message_mock,
            "background": MagicMock(),
            "base": MagicMock()
        }
        flappy.GAME_SPRITES = dict(initial_sprites)
        flappy.GAME_SOUNDS = {}

        event_space = MagicMock()
        event_space.type = KEYDOWN_VAL
        event_space.key = K_SPACE_VAL
        mock_pygame.event.get.return_value = [event_space]

        # Call welcomeScreen with smallest valid sprite dimensions
        result = flappy.welcomeScreen()

        # Expected output is None
        expected_result = None
        self.assertEqual(result, expected_result, f"Expected {expected_result} but got {result}")

        # Observable mutation check
        self.assertEqual(list(flappy.GAME_SPRITES.keys()), list(initial_sprites.keys()))
        self.assertEqual(flappy.GAME_SOUNDS, {})

    def test_ordinary_input(self):
        # Preconditions:
        # SCREENWIDTH = 289 (line 8)
        # SCREENHEIGHT = 511 (line 9)
        player_mock = MagicMock()
        player_mock.get_height.return_value = 24
        message_mock = MagicMock()
        message_mock.get_width.return_value = 184

        initial_sprites = {
            "player": player_mock,
            "message": message_mock,
            "background": MagicMock(),
            "base": MagicMock()
        }
        flappy.GAME_SPRITES = dict(initial_sprites)
        flappy.GAME_SOUNDS = {}

        event_up = MagicMock()
        event_up.type = KEYDOWN_VAL
        event_up.key = K_UP_VAL
        mock_pygame.event.get.return_value = [event_up]

        result = flappy.welcomeScreen()

        expected_result = None
        self.assertEqual(result, expected_result, f"Expected {expected_result} but got {result}")
        self.assertEqual(list(flappy.GAME_SPRITES.keys()), list(initial_sprites.keys()))
        self.assertEqual(flappy.GAME_SOUNDS, {})

    def test_boundary_repeated_event(self):
        # Preconditions:
        # SCREENWIDTH = 289 (line 8)
        # SCREENHEIGHT = 511 (line 9)
        player_mock = MagicMock()
        player_mock.get_height.return_value = 511
        message_mock = MagicMock()
        message_mock.get_width.return_value = 289

        initial_sprites = {
            "player": player_mock,
            "message": message_mock,
            "background": MagicMock(),
            "base": MagicMock()
        }
        flappy.GAME_SPRITES = dict(initial_sprites)
        flappy.GAME_SOUNDS = {}

        # Non terminating event followed by key down space
        dummy_event = MagicMock()
        dummy_event.type = 999
        dummy_event.key = 999

        event_space = MagicMock()
        event_space.type = KEYDOWN_VAL
        event_space.key = K_SPACE_VAL

        mock_pygame.event.get.side_effect = [
            [dummy_event],
            [event_space]
        ]

        result = flappy.welcomeScreen()

        expected_result = None
        self.assertEqual(result, expected_result, f"Expected {expected_result} but got {result}")
        self.assertEqual(flappy.GAME_SOUNDS, {})


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(WelcomeScreenContractTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T011/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
