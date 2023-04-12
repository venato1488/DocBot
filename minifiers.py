import re
import sys

def minify_java(input_file, output_file):
    with open(input_file, 'r') as file:
        java_code = file.read()

    # Remove single-line comments
    java_code = re.sub(r'//.*', '', java_code)

    # Remove multi-line comments
    java_code = re.sub(r'/\*.*?\*/', '', java_code, flags=re.DOTALL)

    # Remove extra whitespace
    java_code = re.sub(r'\s+', ' ', java_code)

    # Remove leading and trailing spaces
    java_code = re.sub(r'^\s|\s$', '', java_code)

    with open(output_file, 'w') as file:
        file.write(java_code)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python minify_java.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    minify_java(input_file, output_file)
