#Wordcloud program for a Federal Open Market Committee (FOMC) statement.
#Author: Eric Lenz, PhD

#Description
#This program scrapes text from a web-based FOMC statement and generates a wordcloud. The wordcloud shows words of varying sizes according to their frequency in the text (the FOMC statement). Words that occur more frequently are larger in size than words that occur less frequently. The wordcloud jumbles the words in a seemingly random way with different colors to give a visual impression of the text's focus and tone. This analysis gives a fun and informative view of "forward guidance" in monetary policy.

#Code also borrowed from:
#https://medium.com/codex/a-beginners-guide-to-easily-create-a-word-cloud-in-python-7c3078c705b7
#https://www.nltk.org/api/nltk.tokenize.html
#From https://stackoverflow.com/questions/716477/join-list-of-lists-in-python
#https://www.machinelearningplus.com/nlp/lemmatization-examples-python/)

#In the command line, be sure to install wordcloud and other packages.
#pip install wordcloud
#pip install pillow
#pip install nltk
#python -m nltk.downloader all

#Also, be sure to set your working directory for the generated image (word_cloud.png).
#os.chdir(path)

from wordcloud import WordCloud
from PIL import Image
import requests
from bs4 import BeautifulSoup
import urllib.request

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

#A few FOMC Meeting URLs:
#March 20, 2024
#https://www.federalreserve.gov/newsevents/pressreleases/monetary20240320a.htm
#March 20, 2019
#https://www.federalreserve.gov/newsevents/pressreleases/monetary20190320a.htm
#Choose a URL and copy/paste when asked for input.

url = input('Enter - ')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

#Get all the text from a document.
#print(soup.get_text())

#Find all the 'p' tags.
#print(soup.find_all('p'))

#Search for 'div' tag and class with FOMC statement.
#print(soup.find_all("div", "col-xs-12 col-sm-8 col-md-8"))

#Alternatively, use attrs={} in the find_all.
#print(soup.find_all(attrs={"class": "col-xs-12 col-sm-8 col-md-8"}))

#before_text = soup.find_all(attrs={"class": "col-xs-12 col-sm-8 col-md-8"})
#print(before_text)
#range(before_text)

#Get just the text. However, still have extra info from last few p tags.
#text = soup.find(attrs={"class": "col-xs-12 col-sm-8 col-md-8"}).get_text()
#print(text)

#Specify a string to be used to join the bits of text together:
#text = soup.find(attrs={"class": "col-xs-12 col-sm-8 col-md-8"}).get_text("|")
#text = soup.find(attrs={"class": "col-xs-12 col-sm-8 col-md-8"}).get_text("", strip=True)
#print(text)

#Tell Beautiful Soup to strip whitespace from the beginning and end of each bit of text:
text = soup.find(attrs={"class": "col-xs-12 col-sm-8 col-md-8"}).get_text(" ", strip=True)
#print(text)

#Get just the first four p tags. Last three p tags are not needed. Now a list...not a string to be tokenized.
#before_text = soup.find('div', 'col-xs-12 col-sm-8 col-md-8').find_all('p')[0:4]
#print(before_text)

#Tokenize the text.
#https://www.nltk.org/api/nltk.tokenize.html
#words = word_tokenize(text)
#print(words)

#Prep the tokenized text for the word soup.
#Following steps from: https://medium.com/codex/a-beginners-guide-to-easily-create-a-word-cloud-in-python-7c3078c705b7

#Only include sentences without voting members' names and contact information. View URLs to determine range.
#sent = sent_tokenize(text)[0:14]

#Tokenize all the sentences and then the words.
sent = sent_tokenize(text)
print(sent)
words = [word_tokenize(t) for t in sent]
#print(words)
#sent is a list of sentences and words is a list of a list (a list of words within each sentence list).

#nltk has trouble with lists of lists and we want a word soup rather than a sentence soup. 
#From https://stackoverflow.com/questions/716477/join-list-of-lists-in-python.
list_words = sum(words,[])

#Make the words lowercase. Why? It looks simple and is more uniform.
low_words = [w.lower() for w in list_words]
#print(low_words)

#Remove stop words like "is", "are", and "the".
remove_words = [w for w in low_words if w not in stopwords.words('english')]
#print(remove_words)

#Remove punctuation from words.
punc_words = [w for w in remove_words if w.isalnum()]
#print(punc_words)

#Lemmatize the words, i.e. reduce the words down to their stem. It's going to remove the "s" and "ing" at the end of words.
#The following code will lemmatize based on the part of speech (POS) tag determined through NLTK's pos_tag.
#Create a function to derive given words POS.
#Fcn source: https://www.machinelearningplus.com/nlp/lemmatization-examples-python/)
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

#Now use NLTK's lemmatizer to update our list of words
final_words = [WordNetLemmatizer().lemmatize(w, get_wordnet_pos(w)) for w in punc_words]
#print(final_words)
#Compare the final_words and punc_words printouts to understand lemmatization.

#Create a single string of space separated words
#unique_string=(" ").join(final_words)
#print(unique_string)

#Wordcloud.
#wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
#wordcloud.to_file("word_cloud.png")

# Delete words that aren't useful w/out context or are unrelated to content of paper
delete_lst = ['committee','percent','inflation','federal','rate','economic','labor','remain','range']
words_v2 = [w for w in final_words if w not in delete_lst]

#Wordcloud with deleted words.
unique_string=(" ").join(words_v2)
print(unique_string)
wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
wordcloud.to_file("word_cloud.png")