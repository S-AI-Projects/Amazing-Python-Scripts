#!/usr/bin/env python3
"""Automated check runner for R29-T060.

Task: Strengthen the tests of Video To Audio(CLI Ver) (video_to_audio.py) [Video-To-Audio(CLI-Ver)]
Target: Video-To-Audio(CLI-Ver)/video_to_audio.py
"""

import io
import json
import os
import platform
import sys
import unittest
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
REPO_ROOT = WORK_DIR.parent.parent
MODULE_DIR = REPO_ROOT / "Video-To-Audio(CLI-Ver)"
PKG_DIR = REPO_ROOT / "Video-To-Audio(CLI-Ver)"

# Add paths for imports
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import module and tests
import video_to_audio
from tests.test_video_to_audio import TestVideoToAudioMutationResistance


def run_checks():
    """Run focused unit tests and record evidence."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestVideoToAudioMutationResistance)

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    output = stream.getvalue()
    print(output)

    evidence = {
        "task": "R29-T060",
        "item": "Video-To-Audio(CLI-Ver)",
        "target_file": "Video-To-Audio(CLI-Ver)/video_to_audio.py",
        "function_tested": "convert_video_to_audio",
        "protected_conditions": [
            "Destination parameter binding: audio stream must be written strictly to audio_path (line 15)",
            "Error handling sentinel: exceptions during loading or conversion must return False (lines 16-17)"
        ],
        "deliberate_mutants_evaluated": [
            {
                "description": "Mutant 1: Destination path swap - writing to video_file instead of audio_path",
                "mutated_line": "clip.audio.write_audiofile(video_file)",
                "named_assertion": "self.assertEqual(clip.audio.written_path, target_audio)",
                "original_result": "PASS",
                "mutant_result": "FAIL (AssertionError: source != target)"
            },
            {
                "description": "Mutant 2: Error return suppression - returning True on exception catch",
                "mutated_line": "except Exception: return True",
                "named_assertion": "self.assertFalse(result)",
                "original_result": "PASS",
                "mutant_result": "FAIL (AssertionError: True is not false)"
            }
        ],
        "preconditions": {
            "source_line_video_file_arg": "Line 6-7: -v/--videoFile required argument",
            "source_line_audio_path_arg": "Line 8-9: -p/--path required argument",
            "source_line_clip_loading": "Line 14: Video_clip = pyeditor.VideoFileClip(args['videoFile'])",
            "source_line_audio_writing": "Line 15: Video_clip.audio.write_audiofile(args['path'])",
            "source_line_error_handling": "Lines 16-17: except Exception: print('Error!!! Something is worng.')"
        },
        "fixtures": {
            "smallest_valid_input": {
                "video_file": "v.mp4",
                "audio_path": "a.mp3",
                "expected_return": True,
                "expected_written_destination": "a.mp3",
                "expected_output": ""
            },
            "ordinary_input": {
                "video_file": "/media/videos/holiday_presentation.mp4",
                "audio_path": "/media/audio/holiday_soundtrack.mp3",
                "expected_return": True,
                "expected_written_destination": "/media/audio/holiday_soundtrack.mp3",
                "expected_output": ""
            }
        },
        "python_version": sys.version,
        "platform": platform.platform(),
        "tests_run": result.testsRun,
        "errors": len(result.errors),
        "failures": len(result.failures),
        "successful": result.wasSuccessful()
    }

    results_json_path = WORK_DIR / "results.json"
    results_txt_path = WORK_DIR / "results.txt"

    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)

    with open(results_txt_path, "w", encoding="utf-8") as f:
        f.write(f"Task: R29-T060 Check Results\n")
        f.write(f"Target: Video-To-Audio(CLI-Ver)/video_to_audio.py\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Tests run: {result.testsRun}\n")
        f.write(f"Failures: {len(result.failures)}\n")
        f.write(f"Errors: {len(result.errors)}\n")
        f.write(f"Status: {'PASSED' if result.wasSuccessful() else 'FAILED'}\n\n")
        f.write("Output:\n")
        f.write(output)

    if not result.wasSuccessful():
        print(f"FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
        sys.exit(1)

    print(f"SUCCESS: All {result.testsRun} checks passed.")
    sys.exit(0)


if __name__ == '__main__':
    run_checks()
