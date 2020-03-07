# Import libraries
import nltk
import requests
import urllib.request
import heapq
import time
from googlesearch import search
from bs4 import BeautifulSoup
import re
# to search
# nltk.download('punkt')
# nltk.download('stopwords')
query = input("Search")
for j in search(query, tld="com", num=10, stop=1, pause=2):
    print(j)
# Set the URL you want to webscrape from
    url = j

# Connect to the URLk
    response = requests.get(url)
    print(response)

# Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    for s in soup(['script', 'style']):
        s.decompose()
    final =  ' '.join(soup.stripped_strings)
    print("*****************************",final)
    time.sleep(5) #pause the code for a sec

article_text = re.sub(r'\[[0-9]*\]', ' ', final)
article_text = re.sub(r'\s+', ' ', final)

# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text)

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print("++++++++++++++++++++++++++++++++++++++++++",summary)