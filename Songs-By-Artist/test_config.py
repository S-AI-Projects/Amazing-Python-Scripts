import os
import sys
import unittest

# Ensure Songs-By-Artist module directory is importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import config


class TestSongsByArtistConfigContract(unittest.TestCase):
    """
    Focused regression test suite locking down the contract of Songs By Artist (config.py).
    Precondition source lines referenced from Songs-By-Artist/config.py:
      - Line 12: client_id initialized as string literal.
      - Line 13: secret_key initialized as string literal.
      - Line 16: get_config() returns a dictionary copy mapping config fields without mutation.
      - Line 21: validate_config(cid, skey) validates credentials contract.
    """

    def test_default_config_contract(self):
        """
        Smallest valid supported input:
        Preconditions: config.py lines 12-13.
        Assert default client_id and secret_key are strings and get_config() matches expected dictionary.
        """
        # Literal inputs
        expected_cid = ""
        expected_skey = ""
        expected_dict = {"client_id": "", "secret_key": ""}

        # Actual values
        actual_cid = config.client_id
        actual_skey = config.secret_key
        actual_dict = config.get_config()

        # Observable values & mutation check
        self.assertEqual(actual_cid, expected_cid)
        self.assertEqual(actual_skey, expected_skey)
        self.assertEqual(actual_dict, expected_dict)

        # Mutating the returned dictionary must not mutate config module state
        actual_dict["client_id"] = "mutated"
        self.assertEqual(config.client_id, expected_cid)

    def test_ordinary_credentials_input(self):
        """
        Ordinary input:
        Preconditions: config.py line 21 (validate_config).
        Validates ordinary 32-character Spotify API key input.
        """
        ordinary_cid = "1234567890abcdef1234567890abcdef"
        ordinary_skey = "abcdef1234567890abcdef1234567890"

        expected_validity = True
        actual_validity = config.validate_config(ordinary_cid, ordinary_skey)

        self.assertEqual(actual_validity, expected_validity)

    def test_domain_boundaries_and_empty_inputs(self):
        """
        Boundary inputs (smallest supported / empty / whitespace / repeated-value):
        Preconditions: config.py line 21.
        Tests empty strings, whitespace strings, and repeated character boundary keys.
        """
        # Smallest input: empty strings
        self.assertFalse(config.validate_config("", ""))
        self.assertFalse(config.validate_config("   ", "   "))

        # Repeated-value boundary input
        repeated_cid = "a" * 32
        repeated_skey = "b" * 32
        expected_repeated_valid = True
        actual_repeated_valid = config.validate_config(repeated_cid, repeated_skey)
        self.assertEqual(actual_repeated_valid, expected_repeated_valid)

        # Non-string / invalid type boundaries
        self.assertFalse(config.validate_config(12345, "secret"))
        self.assertFalse(config.validate_config("client", None))


if __name__ == "__main__":
    unittest.main()
