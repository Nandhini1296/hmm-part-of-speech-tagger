import sys
import json
import io
from collections import defaultdict

START_TAG = "<START_TAG>"
alpha = 0.9
MIN_VALUE = float("-inf")


def read_from_model_file():
    global all_vocabulary, tags_count_dictionary
    global transition_probabilities, emission_probabilities

    with open('hmmmodel.txt', 'r') as model_file:
        all_vocabulary = json.loads(model_file.readline())
        transition_probabilities = json.loads(model_file.readline())
        emission_probabilities = json.loads(model_file.readline())
        tags_count_dictionary = json.loads(model_file.readline())


def viterbi_decoding(words):
    global transition_probabilities, emission_probabilities
    global all_tags, all_vocabulary

    if words == []:
        return []

    most_likely_tag = []
    num_tags = len(all_tags)
    num_words = len(words)

    each_prob = [[0.0] * num_words for i in range(num_tags)]
    backtracking = [[0] * num_words for j in range(num_tags)]

    for tag_index, tag in enumerate(all_tags):
        # print tag
        if words[0] in all_vocabulary:
            if tag not in emission_probabilities:
                emission_prob = 0.0
            else:
                if emission_probabilities[tag].get(words[0]):
                    emission_prob = emission_probabilities[tag][words[0]]
                else:
                    emission_prob = 0.0
            each_prob[tag_index][0] = transition_probabilities[START_TAG][tag] * emission_prob
        else:
            # print "tag", tag
            # print "words", words[0]
            each_prob[tag_index][0] = transition_probabilities[START_TAG][tag]
        backtracking[tag_index][0] = 0

    for count in range(1, num_words):
        for tag_index, tag in enumerate(all_tags):
            max_val = MIN_VALUE
            max_tag_index = 1
            for prev_index, prev_tag in enumerate(all_tags):
                if words[count] in all_vocabulary:
                    if tag not in emission_probabilities:
                        emission_prob = 0
                    else:
                        if emission_probabilities[tag].get(words[count]):
                            emission_prob = emission_probabilities[tag][words[count]]
                        else:
                            emission_prob = 0.0
                    calc_value = transition_probabilities[prev_tag][tag] * each_prob[prev_index][
                        count - 1] * emission_prob
                    # calc_value = math.log(transition_prob[prev][tag] + emission_prob + each_prob[prev][count-1]
                else:
                    calc_value = transition_probabilities[prev_tag][tag] * each_prob[prev_index][count - 1]
                # print "calc_value", calc_value
                if max_val < calc_value:
                    max_val = calc_value
                    max_tag_index = prev_index

            each_prob[tag_index][count] = max_val
            backtracking[tag_index][count] = max_tag_index

    required_index = get_tag_value_number(each_prob, num_tags, num_words - 1)
    most_likely_tag.append(all_tags[required_index])

    for count in range(num_words - 1, 0, -1):
        required_index = backtracking[required_index][count]
        most_likely_tag.append(all_tags[required_index])

    return list(most_likely_tag[::-1])


def decode_input_file(input_file):
    answer = []
    with open(input_file, 'r', encoding='utf-8') as i_file:
        for line in i_file:
            words = line.strip().split()
            ans_tags = viterbi_decoding(words)
            answer.append(list(zip(words, ans_tags)))
    return answer


def get_tag_value_number(matrix, nums, index):
    max_val = MIN_VALUE
    max_index = 0
    for i in range(0, nums):
        if max_val < matrix[i][index]:
            max_val = matrix[i][index]
            max_index = i
    return max_index


def write_output(data):
    with open('hmmoutput.txt', 'w') as outfile:
        # print (data)
        for line in data:
            sentence = ''
            for word in line:
                sentence += ''.join([word[0], '/', word[1]]) + " "
            outfile.write(sentence + "\n")


if __name__ == "__main__":
    input_file_path = sys.argv[1]

    transition_probabilities = defaultdict(lambda: defaultdict(float))
    emission_probabilities = defaultdict(lambda: defaultdict(float))

    all_vocabulary = defaultdict(int)
    tags_count_dictionary = defaultdict(int)

    read_from_model_file()

    all_tags = list(tags_count_dictionary.keys())
    # print all_tags

    output_data = decode_input_file(input_file_path)

    # output_data
    write_output(output_data)
