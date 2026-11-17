import os
import sys
import unittest

# Add Blackjack module directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import blackjack


class TestCardBoundaries(unittest.TestCase):
    """
    Focused boundary regression test suite for Card in Blackjack/blackjack.py.

    Precondition anchors referenced:
      - Line 10: Card class definition.
      - Line 25: Card.__init__ sets self.suit and self.rank without mutating inputs.
      - Line 29: Card.__str__ returns self.rank + ' of ' + self.suit.
      - Line 35: Deck.suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs').
      - Line 36: Deck.ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                               'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace').
    """

    def test_smallest_valid_boundary_input(self):
        """
        Smallest valid input boundary:
        First suit in Deck.suits ('Hearts') and first rank in Deck.ranks ('Two').
        Precondition: blackjack.py lines 35, 36, 25, 29.
        """
        suit = "Hearts"
        rank = "Two"
        expected_str = "Two of Hearts"

        card = blackjack.Card(suit, rank)

        self.assertEqual(card.suit, suit)
        self.assertEqual(card.rank, rank)
        self.assertEqual(str(card), expected_str)

    def test_ordinary_interior_input(self):
        """
        Ordinary input interior to the domain:
        Middle suit ('Spades') and middle rank ('Seven').
        Precondition: blackjack.py lines 35, 36, 25, 29.
        """
        suit = "Spades"
        rank = "Seven"
        expected_str = "Seven of Spades"

        card = blackjack.Card(suit, rank)

        self.assertEqual(card.suit, suit)
        self.assertEqual(card.rank, rank)
        self.assertEqual(str(card), expected_str)

    def test_upper_supported_boundary_input(self):
        """
        Upper supported boundary input:
        Last suit in Deck.suits ('Clubs') and last rank in Deck.ranks ('Ace').
        Precondition: blackjack.py lines 35, 36, 25, 29.
        """
        suit = "Clubs"
        rank = "Ace"
        expected_str = "Ace of Clubs"

        card = blackjack.Card(suit, rank)

        self.assertEqual(card.suit, suit)
        self.assertEqual(card.rank, rank)
        self.assertEqual(str(card), expected_str)

    def test_card_state_immutability_on_str(self):
        """
        Verifies that evaluating __str__ observable values does not mutate Card instance state.
        Precondition: blackjack.py line 29.
        """
        card = blackjack.Card("Diamonds", "King")
        _ = str(card)

        self.assertEqual(card.suit, "Diamonds")
        self.assertEqual(card.rank, "King")


if __name__ == "__main__":
    unittest.main()
