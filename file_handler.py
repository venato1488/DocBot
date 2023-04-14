import os
import tiktoken
import minifiers

def read_files(input_directory):
    # Define a generator function to read the file contents in fixed-size chunks
    def read_file_in_chunks(file_path, chunk_size=1024):
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # Initialize an empty string to hold the file contents
    file_contents = ""

    # Loop through each file in the directory
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        if os.path.isfile(filepath):
            print(f"Reading file: {filename}")
            # Use the generator function to read the file contents in fixed-size chunks
            for chunk in read_file_in_chunks(filepath):
                #print("Current chunk is: " + chunk)
                file_contents += chunk
    return file_contents
    

def process_files(input_directory):
    # Initialize an empty string to hold the file contents
    file_contents = ""

    # Loop through each file in the directory
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        if os.path.isfile(filepath):
            print(f"Reading file: {filename}")
            # 
            if filename.endswith(".py"):
                file_contents += minifiers.minify_python(filepath)
            elif filename.endswith(".java"):
                file_contents += minifiers.minify_java(filepath)
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    result = encoding.encode(process_files(file_contents))
    another_result = encoding.encode(read_files(input_directory))
    print("minified " + str(len(result)) + " tokens")
    print("unminified " + str(len(another_result)) + " tokens")
    return file_contents
            

def save_to_file(document, file_name, document_type):
    if document_type == "html": format = "html"
    else : format = "md"
    name_format = file_name + "." + format
    with open(f"C:\\Users\\Janea\\Desktop\\{name_format}", "w") as f:
        f.write(document)
    f.close()
    print(f"File saved to C:\\Users\\Janea\\Desktop\\{name_format}")


