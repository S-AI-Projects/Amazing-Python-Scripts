# R29 T011 welcomeScreen contract checks

welcomeScreen is defined in Flappy Bird Game main.py at line 21.

## Preconditions and Source Anchors
SCREENWIDTH is 289 defined at line 8
SCREENHEIGHT is 511 defined at line 9
GAME_SPRITES is defined at line 13
GAME_SOUNDS is defined at line 14

## Inputs and Outputs
The function reads events from pygame.
When the space key or up arrow key is pressed, the function returns None.
It does not change GAME_SPRITES or GAME_SOUNDS.

## Fixtures tested
1. Smallest valid input: sprite dimensions with width 1 and height 1. Space key pressed. Return value is None.
2. Ordinary input: sprite dimensions with width 184 and height 24. Up arrow key pressed. Return value is None.
3. Domain boundary: sprite dimensions equal to screen width and height. Harmless event followed by space key. Return value is None.
