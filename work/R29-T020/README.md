# R29 T020 generate_doors mutation checks

generate_doors is defined in Door Puzzle AI Puzzle.py at line 9.

## Preconditions and Source Anchors
List creation: doors = [False] * num_doors at line 9.
Prize selection: prize_door = random.randint(0, num_doors - 1) at line 10.
Prize assignment: doors[prize_door] = True at line 11.
Default door count: num_doors = 3 at line 27.

## Protected Condition and Mutants Tested
The protected condition requires that generate_doors produces a list of exactly num_doors elements, with exactly one element equal to True and all remaining elements equal to False.
A plausible mistake altering list allocation to num_doors - 1 fails the assert_valid_door_contract check.
Original implementation passes all assertions cleanly.

## Tested Fixtures
1. Smallest valid input: num_doors = 1 returns [True] with length 1.
2. Ordinary input: num_doors = 3 returns [False, True, False] with length 3 and single prize door.
3. Mutation verification: Plausible mutant fails the named contract assertion.
