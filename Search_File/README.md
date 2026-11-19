# Searching Specific files

Using the os.walk() module function and match filenames with the fnmatch module.
It walks the tree top-down or bottom-up to create file names in a directory tree. It returns a 3-tuple for each directory in the tree rooted at directory top, including top itself, i.e., dirpath, dirnames, filenames.

## Prerequisites

- Python 3.x

## Usage

1. Clone the repository or download the `searching_specific_files.py` file.
2. Open a terminal or command prompt and navigate to the directory where the file is located.
3. Run the following command to start the program:

   ```shell
   python searching_specific_files.py
   ```

## Search behavior and scaling

`searching_specific_files.py` exposes `search_files(root_path, pattern='*.mp4')` for callers and retains the command-line behavior shown above. It walks the tree top-down and yields each matching path. The program examines each directory entry at most once, so for `N` filesystem entries across the visited tree its worst-case traversal work is O(N). Filtering costs O(F) for the `F` filenames passed to `fnmatch.filter`; this is included in that bound. The iterator streams results rather than collecting the entire tree.

Run correctness checks and local scaling observations with:

```shell
python3 work/R29-T049/check.py
```

The report uses fresh temporary trees at three sizes, five fixed-seed repetitions per size, and checks matched paths outside the timed interval. Timings are observations on the current machine, not performance guarantees.
