# R29-T044: Rock-paper-scissors winner invariant

`game.py` accepts choices 1–3 at line 11, rerolls equal computer choices at lines 32–37, and resolves the winner at lines 57–72. This means completed rounds cannot be draws: each valid round has exactly one winner.

## Expected mapping

For `(user, computer)`, the independently enumerated user-winning pairs are `(1, 3)`, `(2, 1)`, and `(3, 2)`, matching the README's rules. Every other distinct pair is a computer win. When the initial computer draw equals the user's choice, the fixture supplies the next numbered choice, as the source does by redrawing.

The runner mocks console input, randomness, and output. It checks all nine initial pairs and 100 additional bounded valid pairs generated with seed `29044`. A temporary mutation of the first computer-win comparison failed the same winner invariant test; evidence is in `mutation-result.txt`.

Command: `python3 work/R29-T044/check.py` (Python 3.9.6; 2 test methods covering 109 rounds).
