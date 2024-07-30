import json
import random
import argparse
import os

def load_assignments(file_path):
    with open(file_path, 'r') as file:
        assignments = json.load(file)
    return assignments

def replace_keys_with_random_definitions(text, assignments):
    if " " not in text:
        words = [text[i] for i in range(len(text))]
    else:
        words = text.split()

    for i, word in enumerate(words):
        if word in assignments:
            words[i] = random.choice(assignments[word])
    return ' '.join(words)

def process_text_or_file(text_or_file):
    if os.path.isfile(text_or_file):
        with open(text_or_file, 'r') as file:
            return file.read()
    else:
        return text_or_file

def main(file_path, text_or_file):
    assignments = load_assignments(file_path)
    text = process_text_or_file(text_or_file)
    updated_text = replace_keys_with_random_definitions(text, assignments)
    print(updated_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace keys in text with random definitions from a JSON file")
    parser.add_argument('file_path', type=str, help="Path to the JSON file with assignments")
    parser.add_argument('text_or_file', type=str, help="Text to process or path to the text file")

    args = parser.parse_args()
    main(args.file_path, args.text_or_file)
