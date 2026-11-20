import unittest
import tempfile
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from Script import automated_backup


def mutant_backup_flattened_paths(source_dir, destination_dir):
    """
    Deliberate mutant simulating a plausible one-line mistake in automated_backup:
    Flattens subdirectories by using os.path.basename(source_file) instead of
    os.path.relpath(source_file, source_dir).
    """
    try:
        if not os.path.exists(source_dir):
            return None
        os.makedirs(destination_dir, exist_ok=True)
        copied_files = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                # MUTATION: Flattens path instead of preserving subdirectories
                destination_file = os.path.join(destination_dir, file)
                shutil.copy2(source_file, destination_file)
                copied_files.append(file)
        return sorted(copied_files)
    except Exception:
        return None


class TestAutomatedBackupMutation(unittest.TestCase):
    """
    Mutation-resistant regression tests for automated_backup in Automated Script/Script.py.
    Preconditions cited:
      - Line 24: if not os.path.exists(source_dir): return None
      - Line 28: os.makedirs(destination_dir, exist_ok=True)
      - Line 34: rel_path = os.path.relpath(source_file, source_dir)
      - Line 37: shutil.copy2(source_file, destination_file)
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.src = os.path.join(self.temp_dir.name, 'src')
        self.dest = os.path.join(self.temp_dir.name, 'dest')
        os.makedirs(self.src, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_smallest_valid_input(self):
        """
        Smallest valid input: Single file in root of source directory.
        Precondition: Line 24, Line 28, Line 34, Line 37.
        """
        file_path = os.path.join(self.src, 'single.txt')
        with open(file_path, 'w') as f:
            f.write("content 123")

        copied = automated_backup(self.src, self.dest)

        expected = ["single.txt"]
        self.assertEqual(copied, expected)

        dest_file = os.path.join(self.dest, 'single.txt')
        self.assertTrue(os.path.exists(dest_file))
        with open(dest_file) as f:
            self.assertEqual(f.read(), "content 123")

    def test_ordinary_input_nested_hierarchy(self):
        """
        Ordinary input: Multiple files across root and nested subdirectories.
        Precondition: Line 34 (relpath preservation).
        """
        # Create root file
        with open(os.path.join(self.src, 'root.txt'), 'w') as f:
            f.write("root file")

        # Create nested file
        nested_dir = os.path.join(self.src, 'subdir')
        os.makedirs(nested_dir, exist_ok=True)
        with open(os.path.join(nested_dir, 'nested.txt'), 'w') as f:
            f.write("nested file")

        copied = automated_backup(self.src, self.dest)

        expected_copied = ["nested.txt", "root.txt"]
        # Normalize relative path comparison
        normalized_copied = [p.replace(os.sep, '/') for p in copied]
        self.assertIn("root.txt", normalized_copied)
        self.assertIn("subdir/nested.txt", normalized_copied)

        # Assert hierarchy in destination
        self.assertTrue(os.path.exists(os.path.join(self.dest, 'root.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.dest, 'subdir', 'nested.txt')))

    def test_mutant_fails_nested_hierarchy_check(self):
        """
        Proves mutation resistance:
        The original automated_backup passes the nested hierarchy check,
        while the mutant fails the exact same semantic assertion.
        """
        # Setup nested structure
        nested_dir = os.path.join(self.src, 'docs')
        os.makedirs(nested_dir, exist_ok=True)
        with open(os.path.join(nested_dir, 'manual.pdf'), 'w') as f:
            f.write("dummy pdf")

        # 1. Original execution
        dest_original = os.path.join(self.temp_dir.name, 'dest_orig')
        automated_backup(self.src, dest_original)
        orig_nested_exists = os.path.exists(os.path.join(dest_original, 'docs', 'manual.pdf'))
        self.assertTrue(orig_nested_exists, "Original must preserve docs/manual.pdf")

        # 2. Mutant execution
        dest_mutant = os.path.join(self.temp_dir.name, 'dest_mutant')
        mutant_backup_flattened_paths(self.src, dest_mutant)
        mutant_nested_exists = os.path.exists(os.path.join(dest_mutant, 'docs', 'manual.pdf'))
        self.assertFalse(mutant_nested_exists, "Mutant flattens structure and fails docs/manual.pdf existence")

    def test_nonexistent_source_directory_returns_none(self):
        """
        Precondition: Line 24 (if not os.path.exists(source_dir): return None).
        """
        result = automated_backup("/nonexistent/path/dir_123", self.dest)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
