from collections import defaultdict
import re

from dictionary import load_dictionary
from apiscrape import tsv_from_api

class TextAnalyzer():
    """
    Class that analyzes texts for word frequency and generates a TSV file
    containing the valid words that appear alongside their wikitionary definitions

    Attributes:
        language (str): the language of the texts
        frequency (dict[str, int]): maps word to number of occurences across all parsed texts
        validwords (set[str]): all words that have dictionary entries in a language
        tsv (dict[str,str]): maps all valid words to a TSV containing the word and its definition
        scrape (bool): if true, attempts to search for words not in dictionary with Wiktionary API
    """

    def __init__(self, language: str, scrape: bool = False):
        self.language = language.strip().capitalize()
        self.frequency = defaultdict(int)
        self.scrape = scrape
        self.invalidwords = set()
        try:
            self.tsv: dict[str, str] = load_dictionary(language)
            self.validwords = self.tsv.keys()
        except LookupError as e:
            print(e)
            print("Will attempt to retrieve definitions from Wiktionary API instead. This may take a while.")
            self.scrape = True
            self.tsv = {}
            self.validwords = set()

    def parse_text(self, text: str, ngram: int = 1):
        """
        Records the frequencies of valid words or ngrams with wiktionary entries.
        For each word, the next (ngram - 1) words are used to create an ngram.
        If invalid ngram, attempts to record increasingly shorter ngram.
        Words captured in phrases are not used to start new ngrams.
        """
        if ngram < 1:
            raise ValueError("ngram cannot be less than 1")
        
        #splitting into sentences based on conventional punctuation
        sentences = re.split(r"[!\?\.;]+", text)
        for sentence in sentences:

            #removing common punctuation
            sentence = re.sub(r"[/!\"#$%&()*+,\-\./:;<=>?@[\]^_`{|}~'…“”‘’」「—0-9]", " ", sentence)
            words = sentence.lower().split()

            index = 0
            while index < len(words):
                for splice in range(ngram, 0, -1):
                    if index + splice <= len(words):
                        phrase = " ".join(words[index:index + splice])

                        if phrase in self.validwords:
                            self.frequency[phrase] +=1
                            index += splice
                            break

                        elif self.scrape and phrase not in self.invalidwords:
                            try:
                                tsv = tsv_from_api(phrase, self.language)
                                self.tsv[phrase] = tsv
                                self.validwords.add(phrase)
                                self.frequency[phrase] +=1
                                
                                index += splice
                                break

                            except LookupError as e:
                                print(e)
                                self.invalidwords.add(phrase)
              
                else:
                    index +=1

    def print_frequency(self, file_name: str = "frequency.txt"):
        """
        Prints every word found alongside the number times it appeared
        in the order of highest frequency to lowest frequency
        """
        with open(file_name, "w") as output_file:
            sorted_frequency = sorted(self.frequency.items(),key=lambda x: x[1],reverse=True)
            for phrase, freq in sorted_frequency:
                print(phrase, freq, file=output_file)
    
    def print_tsv(self, file_name: str = "definitions.tsv"):
        """
        Prints the word and definiton of every word found as a TSV
        in the order of highest frequency to lowest frequency
        """
        with open(file_name, "w") as output_file:
            sorted_frequency = sorted(self.frequency,key=self.frequency.get,reverse=True)
            for phrase in sorted_frequency:
                print(self.tsv[phrase], file=output_file)
    
    def print_all(self):
        self.print_frequency()
        self.print_tsv()