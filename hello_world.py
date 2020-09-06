
from bs4 import BeautifulSoup
import requests
import string
import itertools

from nltk.corpus import wordnet



def get_phrase(url):
    #
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser').prettify().split(' ')

    comp_flag = False
    print_flag = False
    for w, word in enumerate(soup):

        if 'rube-codeberg-competition' in word:
            comp_flag = True

        if comp_flag:
            if 'Print' in word:
                print_flag = True

        if comp_flag and print_flag:
            if '"' in word:
                # Find the end of the word
                for m, more_word in enumerate(soup[w + 1:]):
                    if '"' in more_word:
                        start_word_index = w
                        end_word_index = w + m + 2
                        break
                break

    to_print = soup[start_word_index:end_word_index]
    to_print = [word.strip('\n').strip('"') for word in to_print]

    return to_print


to_print = get_phrase('https://2020.pycon.org.au/program/sun/')

# Find alternative words
alt_words = {}
grammar = {}
for word in to_print:
    exclude = set(string.punctuation)
    word_no_grammar = ''.join(ch for ch in word if ch not in exclude)

    # Save the garmmar for later
    grammar[word] = {c:ch for c, ch in enumerate(word) if ch in exclude}
    try:
        syns = wordnet.synsets(word_no_grammar)
    except LookupError:
        import nltk
        nltk.download('wordnet')

        syns = wordnet.synsets(word_no_grammar)

    alt_words[word] = [l.name() for s in syns for l in s.lemmas()]

# Add grammar back in
for word in alt_words:
    if len(grammar[word]) > 0:
        for g, gram in grammar[word].items():
            # Too hard to add in grammar otherwise
            if not(g == 0 or g == len(word) - len(grammar[word])):
                break
            for w, word_alt in enumerate(alt_words[word]):
                if g == 0:
                    alt_words[word][w] = gram + alt_words[word][w]
                else:
                    alt_words[word][w] =  alt_words[word][w] + gram


# Find all permutations
alt_phrases_no_grammar = list(itertools.product(*alt_words.values()))


actual_print = [' '.join(phrase).capitalize() for phrase in alt_phrases_no_grammar]


for phrase in actual_print:
    if phrase == ' '.join(to_print):
        print(phrase)
        break
