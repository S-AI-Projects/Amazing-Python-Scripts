# R29-T051: Codechef Scrapper `get_problems` Contract Checks

## Overview
This task locks down the contract and provides focused regression tests for `get_problems` in `Codechef Scrapper/codechef.py`.

## Preconditions and Source Anchors
Preconditions identified from `Codechef Scrapper/codechef.py`:
- **Line 18**: `baseurl = "https://www.codechef.com/problems"` establishes target base endpoint.
- **Line 19**: `wait = WebDriverWait(driver, 15)` establishes web wait handler.
- **Lines 22-23**: `problem_difficulty = {"Beginner": "school", "Easy": "easy", "Medium": "medium", "Hard": "hard", "Challenge": "challenge"}` maps user category labels to URL slugs.
- **Line 31 (original) / Line 53**: `problem_info = {}` initializes the local dictionary for storing problem names and URLs.
- **Lines 63-71 (original 41-48)**: Iterates over problem rows, queries element text and href attribute, and maps `problem_info[problem_name] = problem_url`.

## Contract Specification
- **Inputs**:
  - `category` (`str`): Difficulty slug from `problem_difficulty` mapping (`school`, `easy`, `medium`, `hard`, `challenge`).
  - `no_of_problems` (`int`): Count of problems to scrape (non-negative integer).
- **Outputs**:
  - `problem_info` (`dict[str, str]`): Dictionary mapping problem names to problem URLs.
- **Observable Mutations**:
  - Does not mutate global `problem_difficulty`.
  - Returns a newly created dictionary; mutations on the returned dictionary do not affect module state.

## Fixtures Tested
1. **Smallest Valid Input**:
   - `category = "school"` (`problem_difficulty["Beginner"]`), `no_of_problems = 1`
   - Row 1: name = `"ATM"`, url = `"https://www.codechef.com/problems/HS08TEST"`
   - Expected return: `{"ATM": "https://www.codechef.com/problems/HS08TEST"}`
   - Driver navigates to: `"https://www.codechef.com/problems/school"`

2. **Ordinary Input**:
   - `category = "easy"` (`problem_difficulty["Easy"]`), `no_of_problems = 2`
   - Row 1: name = `"CIELAB"`, url = `"https://www.codechef.com/problems/CIELAB"`
   - Row 2: name = `"HORSES"`, url = `"https://www.codechef.com/problems/HORSES"`
   - Expected return: `{"CIELAB": "https://www.codechef.com/problems/CIELAB", "HORSES": "https://www.codechef.com/problems/HORSES"}`
   - Driver navigates to: `"https://www.codechef.com/problems/easy"`

3. **Repeated-Value Domain Boundary**:
   - `category = "medium"` (`problem_difficulty["Medium"]`), `no_of_problems = 2`
   - Row 1: name = `"DUPLICATE_NAME"`, url = `"https://www.codechef.com/problems/VER1"`
   - Row 2: name = `"DUPLICATE_NAME"`, url = `"https://www.codechef.com/problems/VER2"`
   - Expected return: `{"DUPLICATE_NAME": "https://www.codechef.com/problems/VER2"}` (deduplicated key, len = 1)

4. **Zero Problems Boundary**:
   - `category = "school"`, `no_of_problems = 0`
   - Expected return: `{}` (empty dict matching initial state `problem_info = {}` at anchor line 31)

5. **Observable Mutation and State Isolation**:
   - Verifies `problem_difficulty` is unmutated before and after function invocation.
   - Mutating returned dictionary does not mutate module state or affect subsequent calls.

## Running the Checks
```bash
python3 work/R29-T051/check.py
```
Or directly via unittest:
```bash
python3 -m unittest discover -s "Codechef Scrapper/tests" -p "test_codechef.py" -v
```
