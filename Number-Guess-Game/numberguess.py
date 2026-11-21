"""
Number Guess Game module.

Contract and Invariants:
Precondition Anchors:
- Line 3 (original) / 38: top_of_range = input("Type a number: ")
- Lines 5-10 (original) / 40-45: top_of_range must be a positive integer (> 0).
- Line 15 (original) / 50: random_number = random.randint(0, top_of_range) establishes target in [0, top_of_range].
- Lines 18-35 (original) / 53-70: Guessing loop increments guesses, compares guess with target, and outputs:
  - guess == random_number: "You got it! "
  - guess > random_number: "You were above the number!"
  - guess < random_number: "You were below the number!"
- Line 36 (original) / 71: Final summary: "You got it in {guesses} guesses"

Invariants:
1. Target Boundedness Invariant:
   For any valid top_of_range >= 1, the secret random_number satisfies:
   0 <= random_number <= top_of_range.
2. Comparison Monotonicity Invariant:
   - For all user_guess > random_number: feedback is strictly "You were above the number!".
   - For all user_guess < random_number: feedback is strictly "You were below the number!".
   - When user_guess == random_number: feedback is "You got it! " and the loop terminates.
3. Guess Count Invariant:
   Total reported guesses strictly equals the total number of guess iterations taken (>= 1).
"""

import random


def validate_range(top_of_range_str):
    """Validate top_of_range input string; return integer or error message."""
    if top_of_range_str.isdigit():
        val = int(top_of_range_str)
        if val <= 0:
            return None, 'Please type a number larger than 0 next time. '
        return val, None
    return None, 'Please type a number next time. '


def evaluate_guess(user_guess, random_number):
    """
    Compare guess with secret target and return feedback string and termination flag.

    Precondition anchors:
    - Lines 28-34: equality and inequality checks against random_number
    """
    if user_guess == random_number:
        return "You got it! ", True
    elif user_guess > random_number:
        return "You were above the number!", False
    else:
        return "You were below the number!", False


def run_game(top_of_range, guesses_input_iter, random_number=None):
    """
    Simulate or execute the guessing loop under given inputs.

    Precondition anchors:
    - Line 15: random_number initialization
    - Line 16: guesses counter initialized to 0
    - Lines 18-36: loop and feedback generation
    """
    if random_number is None:
        random_number = random.randint(0, top_of_range)

    guesses = 0
    feedback_history = []
    for raw_guess in guesses_input_iter:
        guesses += 1
        if isinstance(raw_guess, int):
            user_guess = raw_guess
        elif str(raw_guess).isdigit():
            user_guess = int(raw_guess)
        else:
            feedback_history.append('Please type a number')
            continue

        msg, is_correct = evaluate_guess(user_guess, random_number)
        feedback_history.append(msg)
        if is_correct:
            break

    summary = f"You got it in {guesses} guesses"
    return {
        "random_number": random_number,
        "guesses": guesses,
        "feedback": feedback_history,
        "summary": summary
    }


def main():
    top_of_range = input("Type a number: ")

    if top_of_range.isdigit():
        top_of_range = int(top_of_range)

        if top_of_range <= 0:
            print('Please type a number larger than 0 next time. ')
            quit()
    else:
        print('Please type a number next time. ')
        quit()

    random_number = random.randint(0, top_of_range)
    guesses = 0

    while True:
        guesses += 1
        user_guess = input('Make a guess: ')
        if user_guess.isdigit():
            user_guess = int(user_guess)

        else:
            print('Please type a number')
            continue

        if user_guess == random_number:
            print("You got it! ")
            break
        elif user_guess > random_number:
            print("You were above the number!")
        else:
            print("You were below the number!")

    print("You got it in", guesses, "guesses")


if __name__ == '__main__':
    main()
