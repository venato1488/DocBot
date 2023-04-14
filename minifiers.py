
import re
import subprocess
import sys

def minify_java(input_file):
    with open(input_file, 'r', encoding="utf-8") as file:
        java_code = file.read()

    # Remove single-line comments
    java_code = re.sub(r'//.*', '', java_code)

    # Remove multi-line comments
    java_code = re.sub(r'/\*.*?\*/', '', java_code, flags=re.DOTALL)

    # Remove extra whitespace
    java_code = re.sub(r'\s+', ' ', java_code)

    # Remove leading and trailing spaces
    java_code = re.sub(r'^\s|\s$', '', java_code)

    return java_code

def minify_python(input_file):
    process = subprocess.run(["pyminifier", input_file], stdout=subprocess.PIPE)
    mini_python_code = process.stdout.decode('utf-8')
    return mini_python_code
