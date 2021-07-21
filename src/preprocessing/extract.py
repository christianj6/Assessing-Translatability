"""An algorithm to extract English German multi-noun compounds which are difficult to translate and score them according to 'translatability.'"""

import re
import os
import nltk
import heapq
import char_split
import collections
import duden_search
import google_search
import prepare_results
from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn
from spellchecker import SpellChecker
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from calculate_translatability import (
    lemmatize_translations,
    lemmatize_TECs,
    normalize_dictionary,
    score_translatability,
    normalize_TECs,
    generate_test_dictionary,
)

# CORPORA - Sentence aligned .txt files

EUROPARL_DE = "europarl_de.txt"
EUROPARL_EN = "europarl_en.txt"

WIKIPEDIA_DE = "wikipedia_de.txt"
WIKIPEDIA_EN = "wikipedia_en.txt"

SUBTITLES_DE = "subtitles_de.de"
SUBTITLES_EN = "subtitles_en.en"

brown_ic = wordnet_ic.ic("ic-brown.dat")
semcor_ic = wordnet_ic.ic("ic-semcor.dat")


def extract_nouns(text):
    """Extracts nouns from input German text."""
    capitalized = re.findall(r"[A-Z,Ä,Ö,Ü][a-z,ä,ö,ü,ß]+", text, flags=re.UNICODE)
    return capitalized


def clean_nouns(noun_list):
    """Cleans noun list for duplicates and removes other unwanted candidates."""
    nouns_cleaned = set()
    for noun in noun_list:
        if len(noun) > 5:
            nouns_cleaned.add(noun)

    return nouns_cleaned


def split_compounds(candidates):
    """Splits a compound candidate into noun segments, filtering out candidates which do not yield multiple noun segments."""
    compounds = []
    for noun in candidates:
        segments = char_split.split_compound(noun)
        compounds.append(segments)

    flat_list = [
        [item[0], item[1], item[2]]
        for sublist in compounds
        for item in sublist
        if item[0] > 0.2
    ]

    return flat_list


def extract_compounds(candidates):
    """Iterative extraction of valid compounds from list of split compound candidates."""
    spell = SpellChecker(language="de")
    compounds_preliminary = []
    compounds_final = []
    compounds_final_translations = []
    for compound in candidates:
        if (
            spell[compound[1]]
            and spell[compound[2]]
            or duden_search.search(compound[1])
            and duden_search.search(compound[2])
        ):
            print(
                "Assessing '{compound1}' - '{compound2}'...".format(
                    compound1=compound[1], compound2=compound[2]
                )
            )
            compounds_preliminary.append([compound[1], compound[2]])

    print("\n\n\nTranslating compound segments...")
    for compound in compounds_preliminary:
        print("Translating '{word}'...".format(word="".join(compound).title()))
        compound_translations = []
        for word in compound:
            compound_translations.append(google_search.search(word))
        if compound_translations[0] and compound_translations[1]:
            compounds_final.append(compound)
            compounds_final_translations.append(compound_translations)

    compounds_dictionary = dict(
        zip(
            [
                "".join([segments[0], segments[1].lower()])
                for segments in compounds_final
            ],
            compounds_final_translations,
        )
    )
    print("\n\n\nExtracted compounds:")
    for i in compounds_dictionary.items():
        print(i)

    return compounds_dictionary


def prepare_segment_file(word, directory):
    """Accepts a dictionary entry, creating an accompanying file where the extracted corpus segments will be stored. File paths are linked in dictionary."""
    file_path = directory + "\\" + word + ".txt"
    segments_entry = {"segments": file_path}
    with open(file_path, "w") as f:
        pass

    return segments_entry


def write_segments(segments, file_path):
    """Writes extracted corpus segments to the relevant files for each word."""
    for segment in segments:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(segment)
            f.write("\n")

    print("Segments extracted to {filepath}\n\n".format(filepath=file_path))


def prepare_corpus(source, target):
    """Zips source and target corpus files into iterable to be used during querying."""
    with open(source, "rb") as f:
        print("Reading source file...")
        source_read = f.read().splitlines()

    with open(target, "rb") as f:
        print("Reading target file...")
        target_read = f.read().splitlines()

    print("Zipping source and target file...")
    corpus = zip(source_read, target_read)
    return corpus


def query_corpus(corpus, word):
    """Checks word against corpus iterable, generating dictionary of the target segments containing this word ."""
    segments = []
    for item in corpus:
        if str(word) in str(item[0]):
            segments.append(item[1].decode("utf-8"))

    return segments


def extract_translation_candidates(dictionary):
    """For each item in dictionary, extracts likely translation equivalents from segments based on POS and frequency. Updates the item with list of TECs."""

    for word in dictionary:
        nouns_in_segments = []
        with open(dictionary[word]["segments"], "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) == 0:
                dictionary[word].update({"TECs": "n/a", "score": "n/a"})
                print(
                    "No segments found for '{word}.' This word has been removed from the candidate list.".format(
                        word=word
                    )
                )

            elif len(lines) == 1:
                for line in lines:
                    nouns = []
                    text = nltk.word_tokenize(line)
                    text_tagged = nltk.pos_tag(text)
                    for tpl in text_tagged:
                        if tpl[1] == "NN" or tpl[1] == "NNS":
                            nouns.append(tpl[0])

                TEC_list = []
                for item in nouns:
                    tpl = (item, 0, 0, 0)
                    TEC_list.append(tpl)

                dictionary[word].update({"TECs": TEC_list, "score": 0})
                print(
                    "Possible TECs for '{word}'. Only one segment found.".format(
                        word=word
                    )
                )
                print(TEC_list)
                print("\n\n")

            elif len(lines) > 1:
                for line in lines:
                    nouns = set()
                    text = nltk.word_tokenize(line)
                    text_tagged = nltk.pos_tag(text)
                    for tpl in text_tagged:
                        if tpl[1] == "NN" or tpl[1] == "NNS":
                            nouns.add(tpl[0])

                    nouns_in_segments.append(nouns)

                frequency_evaluation = []
                for segment_x in nouns_in_segments:
                    for segment_y in nouns_in_segments:
                        intersection = segment_x.intersection(segment_y)
                        if len(intersection) > 0:
                            for item in list(intersection):
                                frequency_evaluation.append(item)

                counter = collections.Counter(frequency_evaluation)
                most_common = counter.most_common(2)
                most_frequent = []
                for item in most_common:
                    tpl = (
                        item[0],
                        item[1] / len(frequency_evaluation),
                        item[1],
                        len(frequency_evaluation),
                    )
                    most_frequent.append(tpl)

                dictionary[word].update({"TECs": most_frequent, "score": 0})
                print("\n\nMost frequent nouns for '{word}':".format(word=word))
                print(most_frequent)
                print("\n\n")


def main():
    text = input("Input a text from which the untranslatable words will be extracted: ")

    cwd = os.getcwd()
    segments_directory = cwd + "\\segments"
    lemmatizer = WordNetLemmatizer()

    print("\n\n\nExtracting nouns...")
    noun_candidates = extract_nouns(text)
    noun_candidates = clean_nouns(noun_candidates)

    print("\n\n\nExtracting compounds...")
    compound_candidates = split_compounds(noun_candidates)

    print("\n\n\nAssessing compound segments...")
    compound_translations = extract_compounds(compound_candidates)
    dictionary_final = collections.defaultdict(dict)
    for word in compound_translations:
        dictionary_final.update({word: dict(translations=compound_translations[word])})

    print("\n\n\nSegment filepaths:")
    os.makedirs(segments_directory, exist_ok=True)
    for word in dictionary_final:
        dictionary_final[word].update(prepare_segment_file(word, segments_directory))

    for i in dictionary_final.items():
        print(i)

    print("\n\n\nCrossreferencing corpus: EuroParl...")
    for word in dictionary_final:
        file_path = dictionary_final[word]["segments"]
        EuroParl = prepare_corpus(EUROPARL_DE, EUROPARL_EN)
        print("Searching for segments containing '{word}'...".format(word=word))
        write_segments(query_corpus(EuroParl, word), file_path)

    print("\n\n\nCrossreferencing corpus: Wikipedia...")
    for word in dictionary_final:
        file_path = dictionary_final[word]["segments"]
        Wikipedia = prepare_corpus(WIKIPEDIA_DE, WIKIPEDIA_EN)
        print("Searching for segments containing '{word}'...".format(word=word))
        write_segments(query_corpus(Wikipedia, word), file_path)

    print("\n\n\nCrossreferencing corpus: OpenSubtitles2018...")
    for word in dictionary_final:
        file_path = dictionary_final[word]["segments"]
        Subtitles = prepare_corpus(SUBTITLES_DE, SUBTITLES_EN)
        print("Searching for segments containing '{word}'...".format(word=word))
        write_segments(query_corpus(Subtitles, word), file_path)

    extract_translation_candidates(dictionary_final)
    results = prepare_results.create_directory()
    dictionary_final = prepare_results.export_unscored(dictionary_final, results)
    lemmatize_translations(dictionary_final)
    lemmatize_TECs(dictionary_final)
    normalize_dictionary(dictionary_final)
    score_translatability(dictionary_final)
    text = sent_tokenize(text)
    neat_list = prepare_results.print_neat_list(dictionary_final)
    prepare_results.export_data_full(dictionary_final, results)
    prepare_results.export_original_text(text, results)


if __name__ == "__main__":
    main()
