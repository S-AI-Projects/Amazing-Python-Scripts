import os
import shutil

"""
Automated Backup Contract & Mutation-Resistance Specification:
Function: automated_backup(source_dir: str, destination_dir: str) -> list[str]

Contract & Preconditions:
  - Line 24: Verifies source directory existence: if not os.path.exists(source_dir): return None
  - Line 28: Ensures destination exists: os.makedirs(destination_dir, exist_ok=True)
  - Line 34: Preserves directory hierarchy via os.path.relpath(source_file, source_dir)
  - Line 36: Ensures nested destination directory exists before copy
  - Line 37: Copies file and metadata via shutil.copy2(source_file, destination_file)
Outputs:
  - Returns list of relative file paths copied into destination_dir, or None on failure.
Protected Invariant / Mutation Resistance:
  - Protected condition: Preserves subdirectory hierarchy. A plausible mutation replacing
    os.path.relpath(source_file, source_dir) with os.path.basename(source_file) flattens
    the directory tree, failing the hierarchy preservation assertion.
"""


def automated_backup(source_dir, destination_dir):
    try:
        # Check if the source directory exists
        if not os.path.exists(source_dir):
            print(f"Source directory '{source_dir}' does not exist.")
            return None

        # Create the destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        copied_files = []
        # Copy files and folders from source to destination
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                rel_path = os.path.relpath(source_file, source_dir)
                destination_file = os.path.join(destination_dir, rel_path)
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                shutil.copy2(source_file, destination_file)
                copied_files.append(rel_path)

        print("Backup completed successfully!")
        return sorted(copied_files)
    except Exception as e:
        print(f"An error occurred during backup: {e}")
        return None


if __name__ == '__main__':
    source_directory = input("Enter the source directory to be backed up: ")
    destination_directory = input(
        "Enter the destination directory for the backup: ")

    automated_backup(source_directory, destination_directory)
