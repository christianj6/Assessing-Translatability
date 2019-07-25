# Assessing-Translatability
Algorithmic procedure for scoring German compounds according to English-Translatability.



Dependencies

CharSplit (please use the modified script included above. The ngram probability file must be downloaded from https://github.com/dtuggener/CharSplit)

nltk (stem, corpus, tokenize)

heapq

bs4

Spellchecker




Three corpora must also be downloaded from the http://opus.nlpl.eu/ website. They should be downloaded as aligned MOSES format and the respective files named according to the variables in extractor_3.py and placed in the same directory.


http://opus.nlpl.eu/Europarl.php

http://opus.nlpl.eu/Wikipedia.php

http://opus.nlpl.eu/OpenSubtitles-v2018.php
