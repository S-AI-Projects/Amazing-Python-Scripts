import random

# Constants
ZOOMBINIS_COUNT = 16
ZOOMBINIS_PER_TEAM = 8

# Functions

"""
Contract for setup_teams:
Function: setup_teams(num_teams: int = 2, team_size: int = ZOOMBINIS_PER_TEAM, rng=None) -> list[list[int]]
Inputs:
  - num_teams (int): Number of teams to generate (default: 2).
  - team_size (int): Number of Zoombinis per team (default: 8).
  - rng (optional): Random number generator or callable; defaults to random.randint.
Preconditions:
  - Line 25: teams = [] initialized as an empty list.
  - Line 27: team = [] initialized for each team index.
  - Line 29: Each zoombini feature integer must be in range [1, 4].
Outputs:
  - Returns a list of `num_teams` lists, each containing `team_size` integers in range [1, 4].
Invariants:
  - Preserves output structure list[list[int]], shape (num_teams, team_size), and range 1 <= val <= 4.
"""


def setup_teams(num_teams=2, team_size=ZOOMBINIS_PER_TEAM, rng=None):
    if rng is None:
        rand_func = random.randint
    else:
        rand_func = getattr(rng, 'randint', rng)

    teams = []
    for i in range(num_teams):
        team = []
        for _ in range(team_size):
            team.append(rand_func(1, 4))
        teams.append(team)
    return teams


def display_teams(teams):
    for i, team in enumerate(teams, start=1):
        print(f"Team {i}: {team}")


def main():
    print("Welcome to Zoombinis!")
    teams = setup_teams()

    while True:
        display_teams(teams)
        team_choice = int(input("Select a team (1 or 2): "))

        if team_choice < 1 or team_choice > 2:
            print("Invalid team choice. Please select 1 or 2.")
            continue

        selected_team = teams[team_choice - 1]
        zoombini_choice = int(input("Select a Zoombini (1-8): "))

        if zoombini_choice < 1 or zoombini_choice > 8:
            print("Invalid Zoombini choice. Please select a number between 1 and 8.")
            continue

        zoombini = selected_team[zoombini_choice - 1]
        print(f"Selected Zoombini: {zoombini}")

        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != "y":
            print("Thanks for playing Zoombinis!")
            break


if __name__ == "__main__":
    main()
