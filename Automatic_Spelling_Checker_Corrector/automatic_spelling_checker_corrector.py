# imports
import sys

try:
    from spellchecker import SpellChecker
    spell = SpellChecker()
except ImportError:
    spell = None

try:
    from nltk import word_tokenize
except ImportError:
    # Fallback tokenizer for testing without NLTK installed
    def word_tokenize(text):
        import re
        return re.findall(r"\w+|[^\w\s]", text)

# tokens --> stores the tokenized words
tokens = []


def readTextFile(textFilename):
    """
    This function is used to read the input file and extract alphabetic words.

    Contract:
      - Reads contents of textFilename.
      - Tokenizes using word_tokenize.
      - Sets global tokens to full tokenized sequence.
      - Returns list of words filtered by `word.isalpha()`.
      - Mutation-protected condition:
          `words = [word for word in tokens if word.isalpha()]`
          A plausible one-line mutation altering this check (e.g., using `isalnum()` or removing the filter)
          would erroneously include numeric or punctuation tokens.
      - Preconditions:
          - Line 35: tokens = word_tokenize(inputFile.read()).
          - Line 38: words = [word for word in tokens if word.isalpha()].
    """
    global tokens
    words = []
    with open(textFilename, "r") as inputFile:
        tokens = word_tokenize(inputFile.read())

    # Create a list of words from these tokens checking if the word is alphabetic
    words = [word for word in tokens if word.isalpha()]
    return words


def findErrors(textWords):
    """This function is used to detect the errors in file if any"""
    misspelledWords = []
    for word in textWords:
        # correction() --> method of spellchecker module to correct the word
        if spell.correction(word) != word:
            misspelledWords.append(word)

    return misspelledWords


def printErrors(errorList):
    """This function is used to print the errors"""
    print("---------------------")
    print("Misspelled words are:")
    print("---------------------")
    for word in errorList:
        # candidates() --> method of spellchecker module to find suitable corrections of the word
        print(f"{word} : {spell.candidates(word)}")


def correctErrors(errorList):
    """This function is used to correct the errors and
    write the corrected text in output.txt file"""
    # open a new file to write the corrected text
    outputFile = open("output.txt", "w")
    for word in tokens:
        if word in errorList:
            # if word is incorrect we replace it with the corrected word
            word = spell.correction(word)

    # this writes text to the new output.txt file
    outputFile.write(" ".join(tokens))

    outputFile.close()


def main():
    """This is the main function"""
    textFile = input("Enter text file: ")

    textList = readTextFile(textFile)
    errorList = findErrors(textList)

    # if there are no errors
    if len(errorList) == 0:
        print("No errors detected")
        return

    # call to printErrors function
    printErrors(errorList)

    # ask if user needs to correct the text
    user_answer = input("Do you want to auto correct the errors, Y/N ? ")

    if user_answer.lower() == "y" or user_answer.lower() == "yes":
        # call to correctErrors function
        correctErrors(errorList)
        print("-------------------------------------------------")
        print("Check the output.txt file for the corrected text.")
        print("-------------------------------------------------")
        print("Thankyou for using spelling checker program.")
    else:
        print("--------------------------------------------")
        print("Thankyou for using spelling checker program.")
        print("--------------------------------------------")


# call to the main function
if __name__ == "__main__":
    main()
