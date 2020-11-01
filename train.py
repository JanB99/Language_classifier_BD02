from fetch import load
import math, json, datetime

#languages 
languages = ["NL", "EN", "FR", "DE", "ES", "RU"]

#load datasets
datasets = [load(lan) for lan in languages]

#characterset (roman alphabet, punctuation marks, accents, numbers and cyrillic alphabet)
characterset = [chr(i) for i in range(97, 123)]
characterset.extend([",", ".", ";", '"', '“', '”', "'", "’", "!", "?", "(", ")", "[", "]", ":", "-", "—"])
characterset.extend(["é", "ç", "û", "è", "ê", "â", "á", "ü", "ë", "î", "ï", "ô", "ò", "ó", "ù", "ñ"])
characterset.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
characterset.extend(["а", "б", "в",	"г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"])
print("characterset: " + str(len(characterset)))

#creates n-gram
def ngram(characters, n, char, gram):
    if n == 0:
        gram[char] = 0
        return gram

    for i in characters:
        gram = ngram(characters, n-1, char+i, gram)
    return gram

#training function
def train(n, data, gram):
    numGrams = 0
    for word in data:
        for i in range(0, len(word)-n+1, 1):
            s = ""
            for j in range(0, n):
                s += word[i+j]
            if s in gram:
                gram[s] += 1
                numGrams += 1

    gram = {key: value / numGrams for (key, value) in gram.items()}

    gram = smoothing(1/numGrams/2, gram)

    return gram

#smoothing function
def smoothing(smoothing_value, gram): 
    for (key, value) in gram.items():
        if value == 0:
            gram[key] += smoothing_value
            
    sum_values = sum(gram.values())

    for (key, value) in gram.items():
        gram[key] = value/sum_values

    return gram

#make bigrams and trigrams
trigrams = [ngram(characterset, 3, "", {}) for lan in languages]
bigrams = [ngram(characterset, 2, "", {}) for lan in languages]

#train on datasets
print("training started...")
start = datetime.datetime.now()
trigrams = [train(3, datasets[index], trigram) for (index, trigram) in enumerate(trigrams)]
end = datetime.datetime.now()
time = end - start
print("trigrams training done, elapsed time: {}.{} sec".format(time.seconds, time.microseconds))

start = datetime.datetime.now()
bigrams = [train(2, datasets[index], bigram) for (index, bigram) in enumerate(bigrams)]
end = datetime.datetime.now()
time = end - start
print("bigrams training done, elapsed time: {}.{} sec".format(time.seconds, time.microseconds))

#saving models to json
print("saving models...")
with open("trigrams.json", "w") as json_file:
    json.dump(trigrams, json_file)

with open("bigrams.json", "w") as json_file:
    json.dump(bigrams, json_file)

print('models saved in "bigrams.json" and "trigrams.json", run test.py to load the models and test them against user input. ')
