import json
from pathlib import Path

alphabet_file = Path(__file__).parent / "morse_code_alphabet.json"
with open(alphabet_file, "r", encoding="utf-8") as file:
    alphabet = json.load(file)

reversed_alphabet = {value: key for key, value in alphabet.items()}


def text_to_morse(text: str) -> str:
    text_lines = text.upper().split("\n")
    output = []

    for line in text_lines:
        line = " ".join(line.split())
        for letter in line:
            if letter not in alphabet:
                raise ValueError("Oops! Only letters or numbers allowed.")
            output.append(alphabet[letter])
        output.append("\n")

    final_output = ""
    for symbol in output:
        if symbol != "\n":
            final_output += " "
        final_output += symbol
    return final_output


def morse_to_text(morse: str) -> str:
    morse_lines = morse.split("\n")
    output = []
    for line in morse_lines:
        line = " ".join(line.split())
        morse_words = line.split("/")
        for i, word in enumerate(morse_words):
            morse_letters = word.split(" ")
            letters = [reversed_alphabet[code] for code in morse_letters if code != ""]
            output.append("".join(letters))
            if i < len(morse_words) - 1:
                output.append(" ")
        output.append("\n")
    return "".join(output).rstrip()