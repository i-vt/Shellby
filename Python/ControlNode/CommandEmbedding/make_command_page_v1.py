
import json
import os
import base64
import random
import argparse
import random

strDICTIONARYPATH = "assignments.json"
strJUNKHTML = "junk.txt"

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

def embed_in_junk(strPassed: str="", strOutputFilename: str="", 
                strJunkHtmlFilepath: str=strJUNKHTML):
    strJunk = ""
    with open(strJunkHtmlFilepath, "r") as objFile: strJunk = objFile.read()
    listJunkInserts = []
    for strLine in strJunk.split("<p>"):
        bolPresent = False
        if "</p>" in strLine: listJunkInserts.append(strLine.split("</p>")[0])
    random.shuffle(listJunkInserts)
    strOutputText = strJunk.replace(listJunkInserts[0], strPassed)
    with open(strOutputFilename, "w") as objFile: objFile.write(strOutputText)



def main():
    parser = argparse.ArgumentParser(description="Embed text into a junk web page.")
    parser.add_argument("text", help="The text or file path to be translated.")
    parser.add_argument("output_file", help="Where to output the generated text.")
    
    args = parser.parse_args()
    
    result = translate(args.text, "to")
    embed_in_junk(result, args.output_file)

if __name__ == "__main__":
    main()

