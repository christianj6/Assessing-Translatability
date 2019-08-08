# Assessing-Translatability
Algorithmic procedure for scoring German compounds according to English-Translatability.



Dependencies

CharSplit (please use the modified script included above. The ngram probability file must be downloaded from https://github.com/dtuggener/CharSplit)

nltk (stem, corpus, tokenize)

heapq

bs4

pyspellchecker

googletrans

requests 




Three corpora must also be downloaded from the http://opus.nlpl.eu/ website. They should be downloaded as aligned MOSES format and the respective files named according to the variables in extractor_3.py and placed in the same directory. Please pay attention to the naming conventions of these corpora files in the main script 'extractor_3.py.'


http://opus.nlpl.eu/Europarl.php

http://opus.nlpl.eu/Wikipedia.php

http://opus.nlpl.eu/OpenSubtitles-v2018.php

The nltk packages "wordnet_ic", "brown", "semcor", "punkt",
"averaged_perceptron_tagger" and "wordnet" must also be downloaded with nltk before usage.


Usage

Download all the scripts and dependencies listed above.

Run 'extractor_3.py' as the main script

Results will be extracted to the main directory after each iteration of the main script, but these directories should be emptied manually after each iteration.


