# R29 T016 find_lyrics refactoring checks

find_lyrics is defined in Lyrics_Finder script.py at line 8.

## Refactored Responsibility
The URL formatting operation was extracted into a dedicated helper function build_lyrics_url at line 4.
This isolates URL formatting from network request execution and response parsing.

## Preconditions and Source Anchors
build_lyrics_url defined at line 4.
find_lyrics calls build_lyrics_url and requests.get at lines 8 to 10.
Response JSON extraction and default lyrics message handled at lines 12 to 14.
Error string returned on non 200 HTTP response at line 16.

## Fixtures Tested
1. Smallest valid input: artist a and title b formats URL https://api.lyrics.ovh/v1/a/b and returns lyrics.
2. Ordinary input: artist Coldplay and title Yellow formats URL https://api.lyrics.ovh/v1/Coldplay/Yellow and returns lyrics.
3. Error status: HTTP 404 returns error message.
4. Missing key: empty JSON returns default not found message.
