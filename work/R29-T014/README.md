# R29 T014 Support Chat Bot invariant checks

Support Chat Bot For Your Website is in app.py.

## Preconditions and Source Anchors
Session state keys initialized at lines 6 to 9.
document_count slider defined at line 43 with range 0 to 5, step 1, default 2.
Search trigger and result fetching at lines 47 to 56.

## Invariant Properties
1. Bounded result count: For any query and any integer slider value k between 0 and 5, the length of the returned document list must be less than or equal to k.
2. Smallest valid input: When k is 0, the returned list must be empty with length 0.
3. Ordinary input: When k is 2, the returned list has at most 2 items.
4. Mutation check: A mutant function that returns 1 item when k is 0 violates the invariant and is caught by the test.
