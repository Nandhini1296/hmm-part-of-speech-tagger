import sys
import json
import io
from collections import defaultdict

START_TAG = "<START_TAG>"
alpha = 0.9


def parse_inputs(input_file):
    global transition_dictionary, tags_count_dictionary
    global tag_to_words_count_dictionary, tag_to_tag_count_dictionary, all_vocabulary

    with open(input_file, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            words_tag_list = []
            for word_tag in line.strip().split():
                words_tag_list.append(word_tag.rsplit('/', 1))

            prev_tag = START_TAG
            for element in words_tag_list:
                word = element[0]
                tag = element[1]
                transition_dictionary[prev_tag] += 1
                tags_count_dictionary[tag] += 1
                tag_to_words_count_dictionary[tag][word] += 1
                tag_to_tag_count_dictionary[prev_tag][tag] += 1
                all_vocabulary[word] += 1
                prev_tag = tag


def calculate_transition_probabilities():
    global transition_dictionary, tags_count_dictionary, tag_to_words_count_dictionary
    global tag_to_tag_count_dictionary, all_vocabulary

    all_tags = list(tags_count_dictionary.keys())
    num_distinct_tags = len(transition_dictionary)

    for tag in all_tags + [START_TAG]:
        for follow_tag in all_tags:
            numerator = 1 + tag_to_tag_count_dictionary[tag][follow_tag]
            # print tag_to_tag_count_dictionary[tag][follow_tag]
            denominator = num_distinct_tags + transition_dictionary[tag]
            # print transition_dictionary[tag]9
            transition_probabilities[tag][follow_tag] = (float(numerator) / float(denominator))


def calculate_emission_probabilities():
    global emission_probabilities

    all_tags = list(tags_count_dictionary.keys())

    for tag in all_tags:
        for word, count in tag_to_words_count_dictionary[tag].items():
            emission_probabilities[tag][word] = float(count)/(tags_count_dictionary[tag] * 1.0)


def write_model_file():
    global transition_dictionary, tags_count_dictionary, tag_to_words_count_dictionary
    global tag_to_tag_count_dictionary, all_vocabulary

    model_file = "hmmmodel.txt"

    with open(model_file, 'w') as m_file:
        m_file.write(json.dumps(all_vocabulary) + "\n")
        m_file.write(json.dumps(transition_probabilities) + "\n")
        m_file.write(json.dumps(emission_probabilities) + "\n")
        m_file.write(json.dumps(tags_count_dictionary) + "\n")


if __name__ == "__main__":
    input_file_path = sys.argv[1]

    all_vocabulary = defaultdict(int)
    tags_count_dictionary = defaultdict(int)
    transition_dictionary = defaultdict(float)
    tag_to_words_count_dictionary = defaultdict(lambda: defaultdict(int))
    tag_to_tag_count_dictionary = defaultdict(lambda: defaultdict(int))

    parse_inputs(input_file_path)

    transition_probabilities = defaultdict(lambda : defaultdict(float))
    emission_probabilities = defaultdict(lambda: defaultdict(float))

    calculate_transition_probabilities()
    calculate_emission_probabilities()

    write_model_file()
