import random
import string


def speak_like_yoda(sentence):
    """
    Translate the input sentence into Yoda-speak and print the result.

    :param sentence: input string
    :return: None

    For n input characters, string processing and the shuffle loop take O(n)
    work and O(n) auxiliary space: punctuation is a fixed set of 31 characters.
    Counting each random index selection as constant-time gives a worst-case
    O(n) bound; Python's rejection-based random selection makes total runtime
    expected O(n), not a strict worst-case claim. Timings are observations only.
    """
    sentence = sentence.lower()
    for p in string.punctuation.replace("'", ''):
        sentence = sentence.replace(p, '')
    words = sentence.split()
    random.shuffle(words)
    new_sent = ' '.join(words)
    print('\nYour Yodenglish sentence: ')
    print(new_sent.capitalize())


if __name__ == '__main__':
    print('Your English sentence: ')
    sentence = str(input())
    speak_like_yoda(sentence)
