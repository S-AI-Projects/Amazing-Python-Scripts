# R29 T013 Car cross check

Car is defined in Drag Racing Game Drag.py at line 4.

## Preconditions and Source Anchors
Car.__init__ starts current_speed at 0 and gear at 1 at line 5.
accelerate increases speed by acceleration times gear at line 16.
race checks while current_speed is less than top_speed at line 28.
race shifts gear when current_speed reaches 80 percent of top_speed at line 31.

## Independent Oracle Reference
An independent simulation loop computes steps, speed, and gear without calling the Car class.
1. Smallest valid input: top_speed 10 and acceleration 10 reaches finish line in 1 step with final gear 2.
2. Ordinary input: top_speed 200 and acceleration 20 reaches finish line in 9 steps with final gear 3.
3. High acceleration boundary: top_speed 100 and acceleration 85 shifts gear on first step and finishes in 2 steps.
