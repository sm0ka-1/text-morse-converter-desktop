import json
from pathlib import Path

alphabet_file = Path(__file__).parent / "morse_code_alphabet.json"
with open(alphabet_file, "r", encoding="utf-8") as file:
    alphabet = json.load(file)

reversed_alphabet = {value: key for key, value in alphabet.items()}

class InvalidMorseCharacter(ValueError):
    pass

class InvalidMorseSequence(ValueError):
    pass


def text_to_morse(text: str) -> str:
    text_lines = text.upper().split("\n")
    output = []

    for i, line in enumerate(text_lines):
        line = " ".join(line.split())
        for letter in line:
            if letter not in alphabet:
                raise ValueError("Oops! Only letters or numbers allowed.")
            output.append(alphabet[letter])
        if i < len(text_lines) - 1:
            output.append("\n")

    final_output = ""
    for i, symbol in enumerate(output):
        if symbol != "\n" and i != 0 and output[i - 1] != "\n":
            final_output += " "
        final_output += symbol
    return final_output


def morse_to_text(morse: str) -> str:
    allowed = {'.', '-', ' ', '/', '\n'}
    if any(ch not in allowed for ch in morse):
        raise InvalidMorseCharacter("Oops! Invalid morse code.\nAllowed characters: dots (.), dashes (-) and slashes (/).")

    morse_lines = morse.split("\n")
    output = []

    try:
        for i, line in enumerate(morse_lines):
            line = " ".join(line.split())
            morse_words = line.split("/")
            word_output = []
            for word in morse_words:
                morse_letters = word.split(" ")
                letter_output = [reversed_alphabet[code] for code in morse_letters if code != ""]
                word_output.append("".join(letter_output))
            output.append(" ".join(word_output))
            if i < len(morse_lines) - 1:
               output.append("\n")

    except KeyError:
        raise InvalidMorseSequence("Oops! All symbols are valid, but this sequence doesn't match any letter or number.\nMake sure to separate letters with spaces and words with /.")

    return "".join(output).rstrip()