import json
import argparse
import os

def load_assignments(file_path):
    with open(file_path, 'r') as file:
        assignments = json.load(file)
    return assignments

def replace_definitions(text, assignments):
    text = text.replace(" ", "")
    for key, definitions in assignments.items():
        for definition in definitions:
            text = text.replace(definition, key)
    return text

def process_text_or_file(text_or_file):
    if os.path.isfile(text_or_file):
        with open(text_or_file, 'r') as file:
            return file.read()
    else:
        return text_or_file

def main():
    parser = argparse.ArgumentParser(description='Replace text based on JSON assignments.')
    parser.add_argument('file_path', type=str, help='Path to the JSON assignments file')
    parser.add_argument('text_or_file', type=str, help='Text to process or path to the text file')

    args = parser.parse_args()
    assignments = load_assignments(args.file_path)
    text = process_text_or_file(args.text_or_file)
    updated_text = replace_definitions(text, assignments)
    print(updated_text)

if __name__ == "__main__":
    main()

