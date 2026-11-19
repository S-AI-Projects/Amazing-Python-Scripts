# R29 T012 InstaBot boundary checks

InstaBot is defined in Unfollowers Insta insta_bot_bb8.py at line 7.

## Preconditions and Source Anchors
Precondition anchor at line 83: last_ht, ht = 0, 1 in scroll_list.
Unfollowers logic at lines 102 to 105:
self.unfollowers = [x for x in self.following if x not in self.followers]

## Supported Boundaries
1. Smallest valid scroll input: initial last_ht = 0 and ht = 1. The script returns height 1 on first iteration so the loop stops immediately because last_ht equals ht. Expected return is an empty list of names.
2. Ordinary input: height expands to 200 and then repeats 200 so the loop runs and stops. Expected names list matches found accounts. Following list has 3 users and followers has 1 user, giving 2 unfollowers.
3. Domain boundaries: completely disjoint lists where nobody follows back, and full overlap where all followed users follow back.
