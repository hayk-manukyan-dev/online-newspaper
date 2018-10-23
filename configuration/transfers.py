import json


def readJson(document):
    with open(document, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data


def writeJson(document, data):
    with open(document, 'w') as jsonfile:
        json.dump(data, jsonfile)
    return True


def getMemoryJsonData(file):
    file = file.read()
    file = file.decode()
    return json.loads(file)


def mixedArticlesSave(mixed_articles):
    file = 'configuration/json/webconfig.json'
    data = readJson(file)
    data['mixed_articles'] = mixed_articles
    write_data = writeJson(file, data)
    return write_data


