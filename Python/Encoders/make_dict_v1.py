import random
import json
import argparse

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
WORD_COUNT = 2

def load_words(file_path):
    with open(file_path, "r") as file:
        return file.read().split()

def create_base64_list():
    return [char for char in BASE64_CHARS]

def shuffle_words(words):
    random.shuffle(words)
    return words

def assign_words_to_base64(base64_list, words, word_count):
    assignments = {}
    index = 0
    for var in base64_list:
        assignments[var] = words[index:index + word_count]
        index += word_count
    return assignments

def save_assignments(assignments, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(assignments, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Assign words to base64 characters.")
    parser.add_argument("words_file", help="Path to the file containing words.")
    parser.add_argument("output_file", help="Path to the output JSON file.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for shuffling.")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    words = load_words(args.words_file)
    base64_list = create_base64_list()
    words = shuffle_words(words)
    assignments = assign_words_to_base64(base64_list, words, WORD_COUNT)
    save_assignments(assignments, args.output_file)

if __name__ == "__main__":
    main()
