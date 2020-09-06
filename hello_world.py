
from bs4 import BeautifulSoup
import requests

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
print(' '.join(to_print))

# Check that the grammar is valid
