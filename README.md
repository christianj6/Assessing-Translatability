# Assessing-Translatability
Algorithmic procedure for scoring German compounds according to English-Translatability.

---

### Overview

If you have done any translation or are familiar with the vocabulary of a second language, then it is apparent that some words or concepts are easier to translate than others. Many are familiar with the German-English loanwords ‘Schadenfreude’ or ‘Wanderlust,’ which mean, respectively, a perverse pleasure gained at the expense of another’s pain and a desire to leave an area of comfort and see the outside world.

This project aims to develop an algorithmic procedure for quantifying a 'translatability' score using the statistical properties of words and their translations. The procedure only works for German compound nouns.

---

### Setup

Install dependencies.

```
pip install -r requirements.txt
```



Download Corpora.

- http://opus.nlpl.eu/Europarl.php

- http://opus.nlpl.eu/Wikipedia.php

- http://opus.nlpl.eu/OpenSubtitles-v2018.php

Ensure you download the above corpora as aligned MOSES format. You may pass the path to each of the files when running the script, as in the example below.

```
python main.py -w <path to Wikipedia corpus> -e <path to Europarl corpus> -s <path to OpenSubtitles corpus> -f <path to file>
```

---

### Usage

todo

---

### Documentation

For further details on the algorithm, its evaluation, and application in a small study, please consult the ```\docs``` directory.

---

### todo

- [ ] import ngram_probs correctly
- [ ] improve file handling for large corpora
- [ ] improve ux with cli
  - [ ] manager which installs nltk packages
    - [ ] wordnet_ic
    - [ ] brown
    - [ ] punkt
    - [ ] semcor
    - [ ] averaged_perceptron_tagger
    - [ ] wordnet
- [ ] usage instructions
- [ ] remove all 'main' methods from non-main scripts
- [x] section linking to docs
- [ ] test cases and information on running them
- [ ] note that i stole the charplit code
- [ ] lookup tables and maybe pickle files of corpora to speed up corpora processing
