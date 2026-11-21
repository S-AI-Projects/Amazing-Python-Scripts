# Task R29-T058: Cover the failure behavior of start_game (Color_guess.py)

## Overview
- **Item**: Color Guess-GUI
- **Target File**: `Color Guess-GUI/Color_guess.py`
- **Target Function**: `start_game` (lines 10–14)
- **Task Type**: Failure-path coverage
- **Source Data Anchor**: `colors_name = ['Red', 'White', 'Yellow', 'Pink', 'Blue', 'Black', 'Brown', 'Purple', 'Green', 'Cyan']` (Lines 4–5)

---

## 1. Failure / Absent-Result Branch Identification

The function `start_game(play)` orchestrates game start and step evaluation:
```python
def start_game(play=None):
    if time_left == 60:
        countdown()
    change_color()
```

### Decisive Absent-Result Branch: Line 19 (`if (time_left > 0):`)
Inside `change_color()` (called by line 13), the core state mutation is guarded by:
```python
if (time_left > 0):
```
When `time_left <= 0` (such as `time_left = 0`, representing an expired timer / game over state):
- Line 11 evaluates `time_left == 60` as `False`, skipping `countdown()`.
- Line 13 invokes `change_color()`.
- Line 19 evaluates `time_left > 0` as `False`.
- The function exits with absent-result (`None`) without mutating caller-owned state:
  - `score` remains unchanged (`0`)
  - `time_left` remains unchanged (`0`)
  - `colors_name` list remains in its current order (unshuffled)
  - `scoreLabel.text` remains unchanged
  - `e.text` is not cleared

### Rejection Branch: Line 21 (`if e.get().lower() == colors_name[1].lower():`)
When an incorrect guess is submitted, `score` is not incremented (remains unchanged), but the entry field is cleared and colors are reshuffled.

---

## 2. Preconditions and Fixtures

### Preconditions Table
| Precondition | Source Line | Description |
|---|---|---|
| `colors_name` | Lines 4–5 | Data anchor: list of 10 color name strings |
| `score = 0` | Line 6 | Initial player score |
| `time_left = 60` | Line 7 | Initial countdown seconds |
| `if time_left == 60:` | Line 11 | Active timer start branch |
| `if (time_left > 0):` | Line 19 | Absent-result fallback branch in `change_color()` |
| `if e.get().lower() == colors_name[1].lower():` | Line 21 | Guess validation branch |
| `if time_left > 0:` | Line 32 | Countdown decrement and repeat branch |

### Fixtures
1. **Smallest Valid Input (Absent-Result / Expired Branch)**:
   - Literal inputs: `play = None`, `time_left = 0`, `score = 0`, `e.text = 'White'`
   - Expected outputs: `return None`, `time_left == 0`, `score == 0`, `colors_name` unshuffled, `e.text == 'White'`.
2. **Ordinary Valid Input (Active Game Branch)**:
   - Literal inputs: `play = None`, `time_left = 60`, `score = 0`, `e.text = 'White'`
   - Expected outputs: `return None`, `time_left == 59`, `score == 1`, `scoreLabel.text == 'Score: 1'`, `e.text == ''`.
3. **Recovery After Failure**:
   - Calling `start_game(None)` in the absent-result case (`time_left = 0`) safely returns `None`.
   - Re-initializing state to `time_left = 60` and calling `start_game(None)` succeeds normally (`score` increments to 1, timer decrements to 59).

---

## 3. Automated Verification

Run checks locally:
```bash
python3 work/R29-T058/check.py
```
Or via unittest:
```bash
python3 -m unittest discover -s "Color Guess-GUI/tests" -p "test_color_guess.py" -v
```
Evidence is stored in `work/R29-T058/results.json` and `work/R29-T058/results.txt`.
