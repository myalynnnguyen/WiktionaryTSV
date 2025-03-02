from collections import defaultdict

class WordDefinition():
    """
    Class for storing a definition of a word

    Attributes:
        word (str): the word whose definition is being stored
        senses (dict[str, list[str]]): maps a part of speech to a list of corresponding meanings
    """
    def __init__(self, word:str):
        self.word: str = word
        self.senses: dict[str, list[str]] = defaultdict(list)
    
    def add_sense(self, pos:str, sense:str) -> None:
        """
        Stores one sense of a word alongside its part of speech
        """
        self.senses[pos].append(sense)
    
    def format_tsv(self) -> str:
        """
        Returns an HTML-formatted TSV with the word on the left and the definition on the right
        """
        tsv = ""
        for pos, glosses in self.senses.items():
            if tsv == "":
                tsv = f"{self.word}\t"
            else:
                tsv += "<br>"
            tsv += f"{pos}<br>"
            for gloss in glosses:
                tsv += f"{gloss}<br>"
        return tsv