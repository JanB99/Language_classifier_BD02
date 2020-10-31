import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/dataset"

def load(language):
    path = os.path.join(BASE_DIR, language)
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]

    dataset = []
    for path in files:
        file = open(path, 'r', encoding="utf8")
        filedata = ""
        for line in file.readlines():
           filedata += line.strip() + " "
        filedata = filedata.lower().split(" ")
        # filedata = file.read().lower().strip().split(" ")
        filedata = [value for value in filedata if value != '']
        dataset.extend(filedata)
    
    print("{} dataset loaded with {} words".format(language, len(dataset)))
    return dataset