import pandas as pd


alphabet_data = pd.read_csv("morse_code_alphabet.csv")
alphabet = {row.letter: row.code for index, row in alphabet_data.iterrows()}
alphabet["\n"] = "\n"
reversed_alphabet = {value: key for key, value in alphabet.items()}


def text_to_morse(text: str) -> str:
    text = text.rstrip().upper()
    output = []
    for letter in text:
        if letter not in alphabet:
            raise ValueError("Oops! Only letters or numbers allowed.")
        output.append(alphabet[letter])
    final_output = ""
    for symbol in output:
        if symbol != "\n":
            final_output += " "
        final_output += symbol
    return final_output


def morse_to_text(morse: str) -> str:
    morse_lines = morse.rstrip().split("\n")
    output = []
    for line in morse_lines:
        morse_words = line.split("/")
        for word in morse_words:
            morse_letters = word.split(" ")
            letters = [reversed_alphabet[code] for code in morse_letters if code != ""]
            output.append("".join(letters))
            output.append(" ")
        output.append("\n")
    return "".join(output).rstrip()