# WiktionaryTSV

A program to generate TSV files containing word definitions using data from English Wiktionary, made with the purpose of automating flashcards for language learning and creating a file that can easily be imported into Anki.

By default, the definition is obtained from a downloaded [Wiktionary data dump](https://kaikki.org). However, not every language is available in this format. In that case, the definition will be scraped directly using Wiktionary REST API.

## TSV Format

The TSV files contain 2 fields, the word on the left and the definition of the word pertaining to a given language on the right, written in English and formatted in HTML. The definiton contains the parts of speech and the meanings associated with them. For example, here is the definition for the word "amigas" in Spanish:

Raw output:

> amigas\t    Noun\<br>plural of amiga\<br>\<br>Verb\<br>second-person singular present indicative of amigar\<br>

Once formatted:

> amigas<br>
> Noun<br>plural of amiga<br><br>Verb<br>second-person singular present indicative of amigar<br>

## TSV from list of words:

To generate a TSV file from an input file containing a list of words separated by newline characters from a certain language (French, for example):

```
from generatetsv import file_to_tsv

file_to_tsv("input.txt", "output.tsv", "Vietnamese")
```
Input in input.txt:
>trắng<br>
>nhanh<br>
>sinh viên<br>

Raw output in output.tsv:
>trắng\t	adj\<br>white\<br>light or pale\<br><br>
>nhanh\t	adj\<br>fast; quick\<br>\<br>adv\<br>fast; quickly\<br><br>
>sinh viên\t	noun\<br>a postsecondary/undergraduate student\<br><br>

## Frequency list:
You can analyze pieces of text to form a frequency list (from which a TSV file can also be generated). This program utilizes its access to Wiktionary definitions for a few unique features.

Invalid words without definitions on Wiktionary are excluded from the frequency list to create a list without pseudo words that better represents its use of language.

Multi-word compounds can be recorded by setting the <i>ngram</i> keyword arguments of <i>parse_text</i> as shown below. The program will recrod longest valid phrase of length <i>n ≤ ngram</i> that each word can form with its following neighbors. This allows for relatively accurate parsing of text into correct semantic units.
```
from textanalyzer import TextAnalyzer

ta = TextAnalyzer("English")
ta.parse_text("The bus driver drove the school bus to school.", ngram=2)
ta.print_frequency("frequency.txt")
ta.print_tsv("words.tsv")
```

Output in frequency.txt:
> the 2<br>
> bus driver 1<br>
> drove 1<br>
> school bus 1<br>
> to 1<br>
> school 1<br>

Raw output in words.tsv:
> the\t    Article\<br>Used before a noun phrase...<br>
> bus driver\t     Noun\<br>A person employed to drive buses....<br>
> drove\t      Noun\<br>A cattle drive or the herd...<br>
> (continued...)

