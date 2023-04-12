import os
import tiktoken

def read_files(input_directory):
    global file_contents
    # Define a generator function to read the file contents in fixed-size chunks
    def read_file_in_chunks(file_path, chunk_size=1024):
        with open(file_path, "r") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # Initialize an empty string to hold the file contents
    global file_contents, read_time
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
    
def save_to_file(document):
    with open("C:\\Users\\Janea\\Desktop\\README1.md", "w") as f:
        f.write(document)
    f.close()
    print("File saved to C:\\Users\\Janea\\Desktop\\README1.md")


encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
result = encoding.encode(read_files("C:\\Users\\Janea\\Desktop\\SSL"))
print(len(result))