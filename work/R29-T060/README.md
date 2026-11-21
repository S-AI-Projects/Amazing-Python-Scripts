# Task R29-T060: Strengthen the tests of Video To Audio(CLI Ver) (video_to_audio.py)

## Overview
- **Item**: Video-To-Audio(CLI-Ver)
- **Target File**: `Video-To-Audio(CLI-Ver)/video_to_audio.py`
- **Target Function**: `convert_video_to_audio`
- **Task Type**: Mutation-resistant tests

---

## 1. Protected Conditions & Plausible Mistakes

### Protected Condition 1: Target Destination Binding (Line 15)
In line 15:
```python
Video_clip.audio.write_audiofile(r"{}".format(args['path']))
```
The audio track extracted from `video_file` must be written strictly to `audio_path`, preserving `video_file` immutability and directing audio output to the intended destination path.

**Plausible One-Line Mistake (Mutant 1)**:
A developer confuses source and target paths and writes to `video_file`:
```python
Video_clip.audio.write_audiofile(r"{}".format(video_file))
```
- **Named Assertion**: `self.assertEqual(clip.audio.written_path, target_audio)`
- **Original Code**: PASSES (`written_path == target_audio`).
- **Mutant Code**: FAILS (`AssertionError: '/data/input.mp4' != '/data/output.mp3'`).

### Protected Condition 2: Error Return Sentinel (Lines 16–17)
In lines 16–17:
```python
except Exception:
    print("Error!!! Something is worng.")
    return False
```
When an unreadable or corrupt file is processed, the error handler must catch the exception, output the error message, and return `False`.

**Plausible One-Line Mistake (Mutant 2)**:
A developer accidentally suppresses the error status by returning `True`:
```python
except Exception:
    print("Error!!! Something is worng.")
    return True  # MUTANT
```
- **Named Assertion**: `self.assertFalse(result)`
- **Original Code**: PASSES (`result is False`).
- **Mutant Code**: FAILS (`AssertionError: True is not false`).

---

## 2. Preconditions and Fixtures

### Preconditions Table
| Precondition | Source Line | Description |
|---|---|---|
| Video Argument | Lines 6–7 | `-v / --videoFile` required CLI parameter |
| Audio Argument | Lines 8–9 | `-p / --path` required CLI parameter |
| Clip Loading | Line 14 | `Video_clip = pyeditor.VideoFileClip(video_file)` |
| Audio Writing | Line 15 | `Video_clip.audio.write_audiofile(audio_path)` |
| Error Catch | Lines 16–17 | `except Exception: print("Error!!! Something is worng.")` |

### Fixtures
1. **Smallest Valid Input**:
   - `video_file = "v.mp4"`, `audio_path = "a.mp3"`
   - Expected Output: `True`, audio written to `"a.mp3"`, no error stdout.
2. **Ordinary Input**:
   - `video_file = "/media/videos/holiday_presentation.mp4"`, `audio_path = "/media/audio/holiday_soundtrack.mp3"`
   - Expected Output: `True`, audio written to `"/media/audio/holiday_soundtrack.mp3"`.

---

## 3. Automated Verification

Run checks locally:
```bash
python3 work/R29-T060/check.py
```
Or via unittest:
```bash
python3 -m unittest discover -s "Video-To-Audio(CLI-Ver)/tests" -p "test_video_to_audio.py" -v
```
Evidence is stored in `work/R29-T060/results.json` and `work/R29-T060/results.txt`.
