# R29 T015 Audio to Text Convertor repeatability checks

convert_audio_to_text is defined in Audio to Text Convertor code.py at line 4.

## Preconditions and Source Anchors
Recognizer and Microphone are initialized at lines 5 to 11.
Speech recognition via Google API is invoked at line 16.
A small dependency seam allows passing recognizer and microphone as optional arguments with default None.

## Repeatability Verification
1. Smallest valid input: Single word audio transcription hi tested across 5 consecutive runs with identical return values.
2. Ordinary input: Multi word phrase python script audio test tested across 5 consecutive runs with identical return values.
3. Unknown speech error: Exception handling returns None as expected.
