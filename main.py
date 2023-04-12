import os
import sys
import argparse
import openai
import time
import file_handler
#import tiktoken

openai.api_key = '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'

def parse_arguments():
    parser = argparse.ArgumentParser(description='DocBot: Generate documentation from Java or Python source code')
    parser.add_argument('input_directory', help='Path to the directory containing Java or Python source code')
    parser.add_argument('-l', '--level', choices=['high-level', 'intermediate', 'detailed'], default='high-level', help='Level of detail for the generated documentation')
    parser.add_argument('-s', '--sections', nargs='+', default=['classes', 'methods'], help='Sections or information to include in the generated documentation')
    parser.add_argument('-f', '--format', choices=['markdown', 'html'], default='markdown', help='Format of the generated documentation')

    return parser.parse_args()


def message_post(input_directory,level, sections, format):
     # Note: you need to be using OpenAI Python v0.27.0 for the code below to work

    file_contents = file_handler.read_files(input_directory)

    request = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """As an AI Technical Documentation Specialist, your responsibility is to 
        create clear and user-friendly technical documentation from source code using natural language processing skills. 
        You must analyze code, infer context, and maintain up-to-date documentation to ensure product quality"""},
        {"role": "user", "content": f"{file_contents} you must encode your response in the {format} format."}
    ] 
)
    ##response_message = request['choices'][0]['message']['content'] # type: ignore
    # Print the response message
    #print(f"ChatGPT response: {response_message}")

    #file_handler.save_to_file(response_message)


# TODO - total amount of tokens before sending the request to the API
# TODO - minify the code before spliting it into chunks
# TODO - to split code into chunks and send them to the API
# TODO - use pyminifier for making python code smaller prior to sending it to the API
# TODO - conversation mode, maybe to adjust some parameters or redo documentation


def main():
    args = parse_arguments()
    
    input_directory = args.input_directory
    level = args.level
    sections = args.sections
    format = args.format

    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        sys.exit(1)
    
    message_post(input_directory, level, sections, format)


if __name__ == '__main__':
    start = time.time()
    main()