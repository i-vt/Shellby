import argparse
import base64
import os

def file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def base64_to_file(base64_string, output_file):
    with open(output_file, 'wb') as file:
        file.write(base64.b64decode(base64_string))

def main():
    parser = argparse.ArgumentParser(description='Convert a file to Base64 string and vice versa.')
    parser.add_argument('operation', choices=['encode', 'decode'], help='Operation to perform: encode or decode')
    parser.add_argument('input', help='Input file for encoding or Base64 string file for decoding')
    parser.add_argument('output', help='Output file path')
    
    args = parser.parse_args()
    
    if args.operation == 'encode':
        if not os.path.isfile(args.input):
            print(f"Error: The input file '{args.input}' does not exist.")
            return
        
        base64_string = file_to_base64(args.input)
        with open(args.output, 'w') as output_file:
            output_file.write(base64_string)
        print(f"File '{args.input}' has been encoded to Base64 and saved to '{args.output}'.")
    
    elif args.operation == 'decode':
        with open(args.input, 'r') as input_file:
            base64_string = input_file.read()
        
        base64_to_file(base64_string, args.output)
        print(f"Base64 string from '{args.input}' has been decoded and saved to '{args.output}'.")

if __name__ == '__main__':
    main()

