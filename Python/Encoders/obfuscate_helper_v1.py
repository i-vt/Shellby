"""
Requires generated assignments.json
$ python3 obfuscate_v3.py "hello world" to
touch-up Douglass moth-eaten Goldwater colonel metalworking pralines robberies soluble wouldst adaptiveness particularizing colonel Douglass blasphemies bipolarity

$ python3 obfuscate_v3.py "touch-up Douglass moth-eaten Goldwater colonel metalworking pralines robberies soluble wouldst adaptiveness particularizing colonel Douglass blasphemies bipolarity" from
hello world

"""
import json
import os
import base64
import random
import argparse

strDICTIONARYPATH = "assignments.json"

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

def encode(strFilepath, strTextOrFile):
    assignments = load_assignments(strFilepath)
    text = process_text_or_file(strTextOrFile)
    updated_text = replace_keys_with_random_definitions(text, assignments)
    return updated_text

def decode(strFilepath, strTextOrFile):
    assignments = load_assignments(strFilepath)
    text = process_text_or_file(strTextOrFile)
    updated_text = replace_definitions(text, assignments)
    return updated_text

def file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def base64_to_file(base64_string, output_file):
    with open(output_file, 'wb') as file:
        file.write(base64.b64decode(base64_string))

def base64_to_text(text_passed):
    return base64.b64decode(text_passed).decode("utf-8")

def text_to_base64(text_passed):
    return base64.b64encode(text_passed.encode("utf-8")).decode("utf-8")

def translate(strPassed: str="", strDirection: str="to") -> str:
    strReturn = ""
    if strDirection.lower() == "to":
        strCommand = strPassed
        baseCommand = text_to_base64(strCommand)
        wordCommand = encode(strDICTIONARYPATH, baseCommand)
        strReturn = wordCommand
    elif strDirection.lower() == "from":
        wordCommand = strPassed
        baseCommand = decode(strDICTIONARYPATH, wordCommand)
        strCommand = base64_to_text(baseCommand)
        strReturn = strCommand
    return strReturn

def main():
    parser = argparse.ArgumentParser(description="Translate text using encoded definitions.")
    parser.add_argument("text", help="The text or file path to be translated.")
    parser.add_argument("direction", choices=["to", "from"], help="The direction of translation.")
    
    args = parser.parse_args()
    
    result = translate(args.text, args.direction)
    print(result)

if __name__ == "__main__":
    main()

