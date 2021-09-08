import prepare_results
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


def run(args):

    text = input(
        "\nInput a text from which the untranslatable words will be extracted: "
    )

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
