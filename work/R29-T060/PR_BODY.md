## Description
This pull request strengthens test coverage for `Video To Audio(CLI Ver)` in `Video-To-Audio(CLI-Ver)/video_to_audio.py` with mutation-resistant contract and regression tests. It proves that regression tests detect plausible one-line mistakes (such as destination path swap and error suppression), locks down behavior on the smallest valid input (`v.mp4` -> `a.mp3`) and ordinary input, preserves input immutability, and keeps the production implementation free of test-only branches or mutations.

## Related Issue
Fixes: S-AI-Projects/Amazing-Python-Scripts#60

## Type of Change
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance

## Changes Made
- Extracted conversion logic into `convert_video_to_audio(video_file, audio_path, clip_loader=None)` while preserving 100% backward-compatibility for CLI invocations (`-v/--videoFile` and `-p/--path`).
- Added lightweight `MockVideoClip` and `MockAudioClip` test fixtures to allow fast, offline, deterministic testing without requiring heavy ffmpeg/moviepy binaries.
- Protected two core conditions:
  1. Destination parameter binding (line 15: audio is written strictly to `audio_path`).
  2. Failure sentinel handling (lines 16–17: returns `False` on corrupt or missing audio).
- Demonstrated mutation resistance against two plausible one-line mistakes:
  - Destination swap mutant (`write_audiofile(video_file)` instead of `audio_path`): original passes, mutant fails named assertion `self.assertEqual(clip.audio.written_path, target_audio)`.
  - Error suppression mutant (`return True` on exception): original passes, mutant fails named assertion `self.assertFalse(result)`.
- Kept all deliberate mutants out of the production source.
- Created standalone automated runner `work/R29-T060/check.py` saving evidence in `work/R29-T060/results.txt` and `work/R29-T060/results.json`.
- Added detailed task documentation in `work/R29-T060/README.md`.

## Screenshots / Recordings
Not applicable (automated unit tests / CLI utility).

## Testing
Tested locally using:
```bash
python3 work/R29-T060/check.py
```
And via unittest discovery:
```bash
python3 -m unittest discover -s "Video-To-Audio(CLI-Ver)/tests" -p "test_video_to_audio.py" -v
```
All 7 tests passed successfully with 0 errors and 0 failures.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
All checks run cleanly and offline using the Python standard library without requiring external media codecs or network access.
