import json

#prediction function
def predict(sentence, n, grams):
    sentence = sentence.lower().split(" ")

    probs = [1 for lang in languages]

    for word in sentence:
        for i in range(0, len(word)-n+1, 1):
            s = ""
            for j in range(0, n):
                s += word[i+j]
            probs = [p * grams[index][s] for (index, p) in enumerate(probs)]

    sum_probs = sum(probs)

    print("\nprobabilities for {}-gram".format(n))
    for (index, prob) in enumerate(probs):
        print("({}, {})".format(languages[index], prob/sum_probs))


#languages 
languages = ["NL", "EN", "FR", "DE", "ES", "RU"]

#load models
with open("trigrams.json", "r") as json_file:
    print("loading trigrams...")
    trigrams = json.load(json_file)

with open("bigrams.json", "r") as json_file:
    print("loading bigrams...")
    bigrams = json.load(json_file)

print("bigrams and trigrams have been loaded\n")

# test with user input
test = input("provide a sentence to be recognised: ")

while True:
    predict(test, 3, trigrams)
    predict(test, 2, bigrams)
    test = input("\nprovide a sentence to be recognised: ")
