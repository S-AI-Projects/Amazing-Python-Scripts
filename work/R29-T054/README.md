# R29-T054: Number Guess Game Invariant Checks

## Overview
This task establishes property-based invariant tests for `Number-Guess-Game/numberguess.py`, verifying algebraic and state invariants across deterministic seeded inputs and validating mutation sensitivity.

## Preconditions and Source Anchors
Preconditions established in `Number-Guess-Game/numberguess.py`:
- **Line 3 (original) / 38**: `top_of_range = input("Type a number: ")` reads range boundary.
- **Lines 5-10 (original) / 40-45**: Validates positive integer `top_of_range > 0`.
- **Line 15 (original) / 50**: `random_number = random.randint(0, top_of_range)` sets secret target.
- **Lines 18-35 (original) / 53-70**: Guessing loop increments `guesses`, compares input with target, and provides directional feedback.
- **Line 36 (original) / 71**: Final summary reports total `guesses`.

## Invariant Definitions
1. **Target Boundedness**:
   For any valid `top_of_range >= 1`, the generated `random_number` satisfies:
   $$0 \le \text{random\_number} \le \text{top\_of\_range}$$
2. **Comparison Monotonicity**:
   - For all $\text{guess} > \text{target}$, feedback is strictly `"You were above the number!"`.
   - For all $\text{guess} < \text{target}$, feedback is strictly `"You were below the number!"`.
   - When $\text{guess} == \text{target}$, feedback is `"You got it! "` and the loop terminates.
3. **Guess Count Invariant**:
   The final reported `guesses` count strictly equals the total number of guess iterations taken ($\text{guesses} \ge 1$).

## Property Test Specifications
- **Smallest Valid Input**: `top_of_range = 1`, `target = 1`, guess `["1"]`. Result: `"You got it in 1 guesses"`.
- **Ordinary Input**: `top_of_range = 10`, `target = 7`, guesses `["3", "8", "7"]`. Feedbacks: `below`, `above`, `correct`, total 3 guesses.
- **100 Seeded Random Cases**: Generated using `random.Random(42)` covering `top_of_range` in $[1, 1000]$ and random targets. All 100 cases assert the 3 core invariants.
- **Mutation Sensitivity**: Deliberate mutant inverting feedback or corrupting guess counter is caught by assertion failure.

## Running the Checks
```bash
python3 work/R29-T054/check.py
```
Or via native unittest discovery:
```bash
python3 -m unittest discover -s "Number-Guess-Game/tests" -p "test_number_guess.py" -v
```
