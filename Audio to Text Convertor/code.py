import speech_recognition as sr


def convert_audio_to_text(recognizer=None, microphone=None):
    # Initialize the recognizer or use injected one
    if recognizer is None:
        r = sr.Recognizer()
    else:
        r = recognizer

    # Open the microphone or use injected one
    mic = sr.Microphone() if microphone is None else microphone
    with mic as source:
        print("Speak something...")
        audio = r.listen(source)  # Record audio from the microphone

    try:
        # Use the recognizer to convert audio to text
        # Convert audio to text using Google Speech Recognition service
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        # Handle the case when speech cannot be recognized
        print("Unable to recognize speech.")
    except sr.RequestError as e:
        # Handle any errors that occur during speech recognition
        print("Error: {0}".format(e))


if __name__ == "__main__":
    # Example usage
    # Call the function to convert audio to text
    audio_text = convert_audio_to_text()
    if audio_text:
        print("You said:", audio_text)  # Print the converted text

    # Manipulate the text for further operations
    if audio_text:
        # Convert the text to lowercase
        lowercase_text = audio_text.lower()
        print("Lowercase text:", lowercase_text)

        # Split the text into words
        words = lowercase_text.split()
        print("Words:", words)

        # Perform other operations on the text as needed
