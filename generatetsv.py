from typing import Iterable

from dictionary import load_dictionary
from apiscrape import tsv_from_api

def file_to_tsv(input: str, output: str, language: str):
    """
    Takes a path to an input file containing words separted by newline characters
    Generates TSV file at output path with each word mapped to its language definition
    """
    tsv = ""
    with open(input, "r") as input_file:
        tsv = list_to_tsv(input_file, language)
    with open(output, "w") as output_file:
        output_file.write(tsv)
            
def list_to_tsv(wordlist: Iterable[str], language: str) -> str:
    """
    For every str in wordlist, retrieves a TSV containing the
    word and its definition for a certain language in English
    Returns a string containing all TSVs separated by newline character
    """
    tsvdict = None
    try:
        tsvdict = load_dictionary(language)
    except LookupError as e:
        print(e)
        print("Attempting to retrieve definitions from Wiktionary API instead. This may take a while.")

    wordlist_tsv = ""
    for word in wordlist:
        word = word.strip().lower()

        if tsvdict:
            if word in tsvdict.keys():
                wordlist_tsv += f"{tsvdict[word]}\n"
            else:
                print(f"No definitions found for {word}")
        else:
            try:
                wordlist_tsv += f"{tsv_from_api(word, language)}\n"
            except LookupError as e:
                print(e)

    return wordlist_tsv
