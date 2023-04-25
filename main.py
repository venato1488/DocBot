import os
import sys
import argparse
import openai
import time
import file_handler
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

openai.api_key = os.environ.get("OPENAI_API_KEY")

def parse_arguments():
    parser = argparse.ArgumentParser(description='DocBot: Generate documentation from Java or Python source code')
    parser.add_argument('input_directory', help='Path to the directory containing Java or Python source code')
    parser.add_argument('-l', '--level', choices=['high-level', 'intermediate'], default='intermediate', help='Level of detail for the generated documentation')
    #parser.add_argument('-s', '--sections', nargs='+', default=['classes', 'methods'], help='Sections or information to include in the generated documentation')
    parser.add_argument('-f', '--format', choices=['markdown', 'html'], default='markdown', help='Format of the generated documentation')

    return parser.parse_args()


def level_of_detail(level):
    # TODO - add more levels of detail and explanation of what GPT should do
    if level == 'high-level':
        high_level = "write a brief overview of technical documentation for a source code, ensuring that it is easy to read and understand. The documentation should cover essential aspects such as getting started, architectural design, usage guides"
        return 'high-level'
    elif level == 'intermediate':
        intermed = """write detailed technical documentation for a source code based on the following guidelines:Use active voice, simple sentences, and proper formatting for easy reading.Develop a clear, task-oriented Getting Started section.
Provide architectural design details, in-production usage guides, use cases, references, and a roadmap.
In your response, ensure that you include all essential components such as:
Introduction and purpose of the software
Prerequisites and installation instructions
Getting Started section, including a step-by-step guide for using the software
In-depth explanation of the software's architecture, modules, and design patterns
In-production usage guides with best practices and troubleshooting tips
Real-world use cases, illustrating how the software can be applied in various scenarios
References to external resources, libraries, and tools used in the project"""
        return intermed


def message_post(input_directory,level, sections, format):
     # Note: you need to be using OpenAI Python v0.27.0 for the code below to work

    file_contents = file_handler.process_files(input_directory)

    request = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """As an AI Technical Documentation Specialist, your responsibility is to 
        create clear and user-friendly technical documentation from source code using natural language processing skills. 
        You must analyze this code, infer context, and maintain up-to-date documentation to ensure product quality"""},
        {"role": "user", "content": f"{file_contents} you must encode your response in the {format} format."}
    ] 
)

# TODO - total amount of tokens before sending the request to the API
# TODO - to split code into chunks and send them to the API
# TODO - conversation mode, maybe to adjust some parameters or redo documentation


 # Exponential backoff with a maximum of 6 attempts 
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    print("Sending request to OpenAI API...")
    return openai.ChatCompletion.create(**kwargs)





def api_request(**kwargs):
    file_contents = kwargs['file_contents']
    format = kwargs['format']
    level = kwargs['level']
    instructions_for_details = level_of_detail(level)
    request = completion_with_backoff(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions_for_details},
            {"role": "user", "content": f"{file_contents} you must encode your response in the {format} format."}
    ] )
    return request['choices'][0]['message']['content'] # type: ignore



def main():
    args = parse_arguments()
    
    input_directory = args.input_directory
    level = args.level
    #sections = args.sections
    format = args.format

    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        sys.exit(1)
    

    file_contents = file_handler.process_files(input_directory)
    
    print("Files were processed successfully.")
    response_message = api_request(file_contents=file_contents, format=format, level=level)
   
    #message_post(input_directory, level, sections, format)
    
    # Print the response message
    print(f"ChatGPT response: {response_message}")

    file_handler.save_to_file(response_message,"READMEdaddy", format)



if __name__ == '__main__':
    start = time.time()
    main()