import os, base64
filename = input("What is the file path? (ex: C:/users/python/script.py)")
this_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
with open(filename) as file:
    file_contents = file.read()
    print(file_contents)
    file.close()
with open(os.path.join(this_file_path, "one_line_token_logger.py"), 'w') as fp:
    fp.write("import base64\neval(bytes.decode(base64.b64decode(\"" + bytes.decode(base64.b64encode(file_contents.encode('ascii'))) + "\")))")
    fp.close()
