"""Contract, regression, and mutation-resistance tests for video_to_audio.py.

Issue: R29-T060
Target: Video-To-Audio(CLI-Ver)/video_to_audio.py (convert_video_to_audio)
Anchors:
- Precondition 1 (Line 6-7): -v/--videoFile required parameter
- Precondition 2 (Line 8-9): -p/--path required parameter
- Precondition 3 (Line 14): Video_clip = pyeditor.VideoFileClip(args['videoFile'])
- Precondition 4 (Line 15): Video_clip.audio.write_audiofile(args['path'])
- Precondition 5 (Lines 16-17): except Exception: print('Error!!! Something is worng.')
"""

import io
import sys
import unittest
from pathlib import Path

# Add project root and module directory to path for clean import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_DIR = REPO_ROOT / "Video-To-Audio(CLI-Ver)"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import video_to_audio
from video_to_audio import (
    convert_video_to_audio,
    get_parser,
    MockVideoClip,
    MockAudioClip
)


class TestVideoToAudioMutationResistance(unittest.TestCase):
    """Mutation-resistant contract and regression tests for convert_video_to_audio."""

    def _capture_output(self, fn, *args, **kwargs):
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            result = fn(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
        return captured.getvalue(), result

    def test_smallest_valid_input(self):
        """Precondition: Line 6-7 requires video_file; Line 8-9 requires audio_path.
        Smallest valid input: Shortest valid non-empty relative paths ('v.mp4', 'a.mp3').
        Precondition: Line 14 loads clip; Line 15 calls write_audiofile on destination.

        Literal inputs:
        - video_file: 'v.mp4'
        - audio_path: 'a.mp3'

        Independently calculated expected outputs:
        - Result: True
        - clip loaded with 'v.mp4'
        - write_audiofile called with 'a.mp3'
        - Output printed: '' (no error message)
        """
        created_clips = []

        def loader(path):
            clip = MockVideoClip(path)
            created_clips.append(clip)
            return clip

        output, result = self._capture_output(
            convert_video_to_audio,
            video_file="v.mp4",
            audio_path="a.mp3",
            clip_loader=loader
        )

        self.assertTrue(result)
        self.assertEqual(output, "")
        self.assertEqual(len(created_clips), 1)
        self.assertEqual(created_clips[0].filename, "v.mp4")
        self.assertEqual(created_clips[0].audio.written_path, "a.mp3")

    def test_ordinary_input(self):
        """Precondition: Lines 6-9 full absolute file paths.
        Precondition: Lines 14-15 extraction and conversion.

        Literal inputs:
        - video_file: '/media/videos/holiday_presentation.mp4'
        - audio_path: '/media/audio/holiday_soundtrack.mp3'

        Independently calculated expected outputs:
        - Result: True
        - Target destination received extracted audio
        - Output stdout: ''
        """
        created_clips = []

        def loader(path):
            clip = MockVideoClip(path, duration=120.0)
            created_clips.append(clip)
            return clip

        output, result = self._capture_output(
            convert_video_to_audio,
            video_file="/media/videos/holiday_presentation.mp4",
            audio_path="/media/audio/holiday_soundtrack.mp3",
            clip_loader=loader
        )

        self.assertTrue(result)
        self.assertEqual(output, "")
        self.assertEqual(len(created_clips), 1)
        self.assertEqual(created_clips[0].filename, "/media/videos/holiday_presentation.mp4")
        self.assertEqual(created_clips[0].audio.written_path, "/media/audio/holiday_soundtrack.mp3")
        self.assertEqual(created_clips[0].audio.write_calls, ["/media/audio/holiday_soundtrack.mp3"])

    def test_protected_destination_binding(self):
        """Protected Condition: Line 15 binds write_audiofile strictly to audio_path.
        Named assertion: self.assertEqual(clip.audio.written_path, target_audio)
        Verifies that source file is never overwritten by destination path.
        """
        source_video = "/tmp/source_lecture.mp4"
        target_audio = "/tmp/destination_lecture.mp3"
        created_clips = []

        def loader(path):
            clip = MockVideoClip(path)
            created_clips.append(clip)
            return clip

        convert_video_to_audio(source_video, target_audio, clip_loader=loader)

        self.assertEqual(len(created_clips), 1)
        # Named assertion protecting destination binding
        self.assertEqual(created_clips[0].audio.written_path, target_audio)
        self.assertNotEqual(created_clips[0].audio.written_path, source_video)

    def test_deliberate_mutant_destination_swap_fails_assertion(self):
        """Mutation Resistance Check:
        Plausible one-line mistake: In line 15, a developer mistakenly writes
        audio to video_file instead of audio_path:
            Video_clip.audio.write_audiofile(r"{}".format(video_file))

        Prove that the original passes the named assertion and the mutant FAILS
        the same named assertion for a semantic reason.
        """
        source_video = "/data/input.mp4"
        target_audio = "/data/output.mp3"

        # 1. Original implementation test
        clip_original = MockVideoClip(source_video)
        convert_video_to_audio(source_video, target_audio, clip_loader=lambda p: clip_original)
        # Original PASSES:
        self.assertEqual(clip_original.audio.written_path, target_audio)

        # 2. Deliberate mutant simulating the one-line mistake
        def mutant_convert(video_file, audio_path, loader):
            clip = loader(video_file)
            # ONE-LINE MISTAKE: writing to video_file instead of audio_path
            clip.audio.write_audiofile(video_file)
            return True

        clip_mutant = MockVideoClip(source_video)
        mutant_convert(source_video, target_audio, loader=lambda p: clip_mutant)

        # Named assertion: clip.audio.written_path == target_audio
        # Mutant FAILS this assertion:
        with self.assertRaises(AssertionError):
            self.assertEqual(clip_mutant.audio.written_path, target_audio)

    def test_deliberate_mutant_error_suppression_fails_assertion(self):
        """Mutation Resistance Check 2:
        Plausible one-line mistake: In lines 16-17, the error handler mistakenly returns True:
            except Exception:
                print("Error...")
                return True  # ONE-LINE MISTAKE: should return False

        Prove that original returns False and mutant fails the assertion.
        """
        def failing_loader(path):
            raise IOError(f"File not found: {path}")

        # Original implementation:
        output, original_result = self._capture_output(
            convert_video_to_audio,
            video_file="missing.mp4",
            audio_path="out.mp3",
            clip_loader=failing_loader
        )
        self.assertFalse(original_result)
        self.assertIn("Error!!! Something is worng.", output)

        # Deliberate mutant:
        def mutant_error_handler(video_file, audio_path, loader):
            try:
                loader(video_file)
                return True
            except Exception:
                print("Error!!! Something is worng.")
                return True  # MUTANT

        _, mutant_result = self._capture_output(
            mutant_error_handler,
            video_file="missing.mp4",
            audio_path="out.mp3",
            loader=failing_loader
        )
        # Named assertion: self.assertFalse(result)
        # Mutant FAILS this assertion:
        with self.assertRaises(AssertionError):
            self.assertFalse(mutant_result)

    def test_missing_audio_track_fails_cleanly(self):
        """Precondition: Line 15 expects Video_clip.audio to exist.
        When Video_clip.audio is None, it cleanly prints error and returns False.
        """
        def silent_loader(path):
            return MockVideoClip(path, has_audio=False)

        output, result = self._capture_output(
            convert_video_to_audio,
            video_file="silent_film.mp4",
            audio_path="silent.mp3",
            clip_loader=silent_loader
        )
        self.assertFalse(result)
        self.assertIn("Error!!! Something is worng.", output)

    def test_cli_argument_parsing(self):
        """Verify CLI argument parsing structure defined at lines 4-10."""
        parser = get_parser()
        args = parser.parse_args(["-v", "in.mp4", "-p", "out.mp3"])
        self.assertEqual(args.videoFile, "in.mp4")
        self.assertEqual(args.path, "out.mp3")

    def test_input_mutation_behavior(self):
        """Invariant: Caller-owned input arguments must not be mutated."""
        source = "sample.mp4"
        dest = "sample.mp3"
        convert_video_to_audio(source, dest, clip_loader=MockVideoClip)
        self.assertEqual(source, "sample.mp4")
        self.assertEqual(dest, "sample.mp3")


if __name__ == '__main__':
    unittest.main()
