import os

directory = "../data/companies"
print(len(__file__))
path = os.getcwd()
print("Current Directory", path)

# prints parent directory
print(os.path.abspath(os.path.join(path, os.pardir)))
print(os.path.abspath(__file__)[0 : -len(__file__)])
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    file_dir_path = os.path.join(directory, filename)
    print(file_dir_path)
