import ast
import tokenize
import io
from google import genai
from google.genai import types
import argparse

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def is_function_exist(source_code):
    if source_code is None:
        return False
    try:
        tree = ast.parse(source_code)
        return any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
    except SyntaxError as e:
        return False

def remove_comments(file):
    try:
        result = []
        for toktype, token, start, end, line in tokenize.generate_tokens(file.readline):
            if toktype != tokenize.COMMENT:
                if toktype == tokenize.STRING and token.startswith(('"""', "'''")):
                    if len(result) > 0:
                        if result[-1][0] == tokenize.OP:
                            result.append((toktype, token))    
                    continue
                result.append((toktype, token))
        return tokenize.untokenize(result)
    except:
        print(f"Error: This tool only generates unit tests for functions.")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path to your function file")
    args = parser.parse_args()
    file_path = args.file_path
    file = read_file(file_path)
    if not is_function_exist(file):
        print("Error: This tool only generates unit tests for functions.")
        return

    cleaned_code = remove_comments(io.StringIO(file))
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=cleaned_code,
        config=types.GenerateContentConfig(
            system_instruction="""
            Role: You are a CLI tool to generate Python unittest code. You are not a chat assistant
            Input: You will get a snippet of python code containing a function
            Output Rules:
            Output ONLY VALID and Executable Python code for unittests and nothing else.
            Generate high-quality unittests for the given function
            NO markdown: do NOT wrap output in markdown blocks
            NO Commentary: do NOT add any comments just the unittests.
            NO Explanation: do NOT provide Explanations just give the plain unittest for the python function.
            NO extra text: do NOT include any converstaional or any extra text.
            """,
            temperature=0
        )
    )
    print(response.text)
if __name__ == "__main__":
    main()
