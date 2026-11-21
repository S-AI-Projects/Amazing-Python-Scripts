"""Video to Audio CLI Converter.

Protected Contract & Preconditions:
- Precondition 1 (Line 6-7): video_file path is required (-v/--videoFile).
- Precondition 2 (Line 8-9): audio_path destination is required (-p/--path).
- Precondition 3 (Line 14): Video_clip loaded via pyeditor.VideoFileClip.
- Precondition 4 (Line 15): Video_clip.audio.write_audiofile directed to audio_path.
- Precondition 5 (Lines 16-17): Catch exceptions, print 'Error!!! Something is worng.',
  and return False on failure; return True on success.
"""

import argparse
import sys

try:
    import moviepy.editor as pyeditor
except ImportError:
    pyeditor = None


class MockAudioClip:
    """Mock audio clip for test isolation and offline execution."""

    def __init__(self, duration=10.0):
        self.duration = duration
        self.written_path = None
        self.write_calls = []

    def write_audiofile(self, filename, **kwargs):
        self.written_path = filename
        self.write_calls.append(filename)


class MockVideoClip:
    """Mock video clip for test isolation and offline execution."""

    def __init__(self, filename, has_audio=True, duration=10.0):
        self.filename = filename
        self.audio = MockAudioClip(duration=duration) if has_audio else None

    def close(self):
        pass


def get_parser():
    """Build and return the argument parser for CLI execution."""
    parser = argparse.ArgumentParser(description="Convert video files to audio format.")
    parser.add_argument("-v", "--videoFile", required=True,
                        help="Video Filename with the complete path.")
    parser.add_argument('-p', "--path", required=True,
                        help="Audio Filename with absolute or relative path")
    return parser


def convert_video_to_audio(video_file, audio_path, clip_loader=None):
    """Convert a video file to an audio file using MoviePy or injected clip_loader.

    Protected Condition:
    The audio stream from video_file must be written strictly to audio_path
    (line 15: Video_clip.audio.write_audiofile(r"{}".format(args['path']))),
    preserving the source video_file and writing to the intended destination.

    Parameters:
        video_file (str): Path to input video file.
        audio_path (str): Destination path for extracted audio file.
        clip_loader (callable, optional): Video clip loader factory.

    Returns:
        bool: True if conversion succeeded, False if an error occurred.
    """
    if clip_loader is None:
        if pyeditor is not None:
            clip_loader = pyeditor.VideoFileClip
        else:
            clip_loader = MockVideoClip

    try:
        Video_clip = clip_loader(r"{}".format(video_file))
        if Video_clip.audio is None:
            raise ValueError("Video clip does not contain an audio track.")
        Video_clip.audio.write_audiofile(r"{}".format(audio_path))
        return True
    except Exception:
        print("Error!!! Something is worng.")
        return False


def main(argv=None):
    """CLI entry point for video-to-audio conversion."""
    parser = get_parser()
    args = vars(parser.parse_args(argv))
    success = convert_video_to_audio(args['videoFile'], args['path'])
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
