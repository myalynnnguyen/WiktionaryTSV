import requests
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry

from worddefinition import WordDefinition
from dictionary import standardize_language

def wiktionary_url(word: str) -> str:
    """
    Formats the proper url to access the definitoin of word with Wiktionary API
    """
    word = word.replace(' ', '_')
    return f"https://en.wiktionary.org/api/rest_v1/page/definition/{word}"

def tsv_from_api(word: str, language:str) -> str:
    """
    Retrieves the definition of a word, both lowercase and uppercase forms,
    in the given language using Wiktionary REST API
    Returns a single TSV mapping the word to its definition
    """
    
    lowercase = word.lower()
    capitalize = word.capitalize()
    forms = [lowercase,capitalize]
    invalid_forms = 0

    wdefinition = WordDefinition(word)
    for form in forms:
        try:
            wdefinition = get_definition(form, language, wdefinition)
        except LookupError as e:
            invalid_forms += 1
    
    if invalid_forms == len(forms):
        raise LookupError(f"No definitions found for {word}.")
    
    return wdefinition.format_tsv()

@sleep_and_retry
@limits(calls=200,period=10)
def get_definition(word: str, language:str, wdefinition: WordDefinition = None) -> WordDefinition:
    """
    Retrieves the definition of a word in a given language from Wiktionary API
    if given an existing instance of WordDefinition, data is appended to it
    Note: the lower case and capitalized form of a word have different definitions
    """
    if not wdefinition:
        wdefinition = WordDefinition(word)
    
    language = language.strip().capitalize()
    
    url = wiktionary_url(word)
    headers = {'User-Agent': 'https://github.com/myalynnnguyen/WiktionaryTSV'}
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        raise LookupError(f"{word} could not be found")
    
    entries = []
    for subsection in response.json().values():
        for field in subsection:
            if field["language"] == language:
                entries.append(field)

    if len(entries) == 0:
        raise LookupError(f"No {language} entry for {word}")
    
    for entry in entries:
        pos = BeautifulSoup(entry["partOfSpeech"], "html.parser").text
        for definitions in entry["definitions"]:
            definition = BeautifulSoup(definitions.get("definition", ""), "html.parser").text
            wdefinition.add_sense(pos, definition)
    
    return wdefinition