# -*- coding: utf-8 -*-
from lxml import html
import requests

OUTPUT_FILE_NAME = "words.txt"
BASE_URL = 'https://www.kelimetre.com/'
LETTERS = 'abcçdefghıijklmnoöprsştuüvyz'

def get_urls_by_letter(base_url=BASE_URL, letters=LETTERS):
    letter_url = base_url + "{}-ile-baslayan-kelimeler"
    return [letter_url.format(x) for x in letters]

def get_words_with_x_letters_page(letter_urls):
    print("Fetching word pages for each letter...")
    words_with_x_letters_page_urls = []

    for url in letter_urls:
        try:
            page = requests.get(url)
        except:
            print("Error opening the URL")

        tree = html.fromstring(page.content)
        
        links = reversed(tree.xpath("//html/body/main/div/div/div/section[4]/div/div[*]/div/div/a/@href"))

        words_with_x_letters_page_urls.extend(links)
    
    return words_with_x_letters_page_urls

def get_words(word_paths, base_url=BASE_URL):
    print("Fetching words...")

    all_words = []

    for rel_path in word_paths:
        try:
            page = requests.get(base_url + rel_path)
        except:
            print("Error opening the URL")
        
        tree = html.fromstring(page.content)

        words = tree.xpath("//html/body/main/div/div/div/section[4]/div/ul/a[*]/@title")

        words = [word.split()[0] for word in words]

        all_words.extend(words)

    return all_words

def write_words_to_file(words, file_name=OUTPUT_FILE_NAME):
    print("Writing words to file...")
    with open(file_name, 'w') as f:
        f.write("\n".join(words))

if __name__ == "__main__":
    write_words_to_file(get_words(get_words_with_x_letters_page(get_urls_by_letter())))

    print("DONE")
