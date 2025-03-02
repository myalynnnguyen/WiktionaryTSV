import json
import requests
import os

from worddefinition import WordDefinition

def dictionary_path(language:str) -> str:
    language = standardize_language(language)
    return f"dictionaries/{language}.tsv"

def standardize_language(language:str) -> str:
    return language.strip().capitalize()

def make_dictionary(language: str) -> str:
    """
    Retrieves the en.wiktionary dump of a language from kaikki.org and
    creates a TSV file storing every word and its definition
    """
    language = standardize_language(language)
    url = f"https://kaikki.org/dictionary/{language}/kaikki.org-dictionary-{language}.jsonl"
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise LookupError(f"Could not find wiktionary dump for {language} at {url}")
    
    definitions: dict[str, WordDefinition] = {}
    for line in response.iter_lines():
        j = json.loads(line)
        word = j["word"].lower()
        if word not in definitions.keys():
            definitions[word] = WordDefinition(word)

        pos = j["pos"]
        for sense in j["senses"]:
            if "glosses" in sense.keys():       
                gloss = sense["glosses"][0]
                definitions[word].add_sense(pos, gloss)
    

    with open(f"dictionaries/{language}.tsv", "w") as file:
        for definition in definitions.values():
            file.write(f"{definition.format_tsv()}\n")


def load_dictionary(language: str) -> dict[str, str]:
    """
    Loads the dictionary file for the language into memory
    as a dict mapping the word to the tsv
    Creates the dictionary if it does not exist
    """
    dictionary = {}
    if not os.path.exists(dictionary_path(language)):
        print(f"Creating {language} dictionary from wiktionary dump. "
                "This is a one time process that may take a few minutes.")
        make_dictionary(language)
        
    with open(dictionary_path(language), "r") as file:
        for line in file:
            line = line.strip()
            word = line.split('\t')[0]
            dictionary[word] = line
    return dictionary