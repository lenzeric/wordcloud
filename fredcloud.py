#Wordcloud program with masked images for FRED graph. A comparison of FOMC statements before and after the COVID-related recession.
#Author: Eric Lenz, PhD

#Description
#This program scrapes text from multiple FOMC statements and generates two wordclouds corresponding to time periods before and after the recent COVID recession. The wordcloud jumbles the words in a seemingly random way with different colors to give a visual impression of the texts' focus and tone. This analysis compares the focus and tone of the FOMC before and after the recession. 

#Result/Analysis
#The pre-COVID period (2016-2019) typically mentions the labor market, market conditions, and maximum employment. However, the post-COVID period (2020-2024) is marked by more varied topics like public health, inflation pressure, and household business. Also interesting is the frequent occurence of "treasury security" as interest rates increased dramatically from the near zero environment.

#In the command line, be sure to install wordcloud and other packages.
#pip install wordcloud
#pip install pillow
#pip install nltk
#python -m nltk.downloader all
#pip install numpy

#Code also borrowed from:
#https://medium.com/codex/a-beginners-guide-to-easily-create-a-word-cloud-in-python-7c3078c705b7
#https://www.nltk.org/api/nltk.tokenize.html
#From https://stackoverflow.com/questions/716477/join-list-of-lists-in-python
#https://www.machinelearningplus.com/nlp/lemmatization-examples-python/)
#https://www.geeksforgeeks.org/how-to-iterate-through-a-nested-list-in-python/
#https://www.youtube.com/watch?v=uJbNIWPakj0
#https://www.geeksforgeeks.org/overlay-an-image-on-another-image-in-python/
#https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil#5324782

from wordcloud import WordCloud
from PIL import Image
import requests
from bs4 import BeautifulSoup
import urllib.request
import numpy as np

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

#FOMC statement dates before COVID (January 27th, 2016 - December 11th, 2019): 
meetings_pre = ['20160127', '20160316', '20160427', '20160615', '20160727', '20160921', '20161102', '20161214', '20170201', '20170315', '20170503', '20170614', '20170726', '20170920', '20171101', '20171213', '20180131', '20180321', '20180502', '20180613', '20180801', '20180926', '20181108', '20181219', '20190130', '20190320', '20190501', '20190619', '20190731', '20190918', '20191030', '20191211']

#FOMC statement dates after COVID (March 23rd, 2020 - March 20th, 2024): 
meetings_post = ['20200323', '20200429', '20200610', '20200729', '20200916', '20201105', '20201216', '20210127', '20210317', '20210428', '20210616', '20210728', '20210922', '20211103', '20211215', '20220126', '20220316', '20220504', '20220615', '20220727', '20220921', '20221102', '20221214', '20230201', '20230322', '20230503', '20230614', '20230726', '20230920', '20231101', '20231213', '20240131', '20240320']

#Create a list corresponding to the two date lists. The code below loops through the first element (meetings_pre) and generates the first wordcloud. Then, it loops through the second element (meetings_post) for the second wordcloud. 
meetings_post_pre = [meetings_pre, meetings_post]
for meetings in range(len(meetings_post_pre)) :
    text = " "
    for date in range(len(meetings_post_pre[meetings])) :
        url = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary{}a.htm'.format(meetings_post_pre[meetings][date])
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        text_0 = soup.find(attrs={"class": "col-xs-12 col-sm-8 col-md-8"}).get_text(" ", strip=True)
        text = text + text_0
        #print(text)

    sent = sent_tokenize(text)
    words = [word_tokenize(t) for t in sent]
    list_words = sum(words,[])
    low_words = [w.lower() for w in list_words]
    remove_words = [w for w in low_words if w not in stopwords.words('english')]
    punc_words = [w for w in remove_words if w.isalnum()]

    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    final_words = [WordNetLemmatizer().lemmatize(w, get_wordnet_pos(w)) for w in punc_words]
    delete_lst = ['committee', 'fund', 'rate', 'federal','monetary', 'policy', 'percent', 'target', 'range', 'economic', 'activity']
    words_v2 = [w for w in final_words if w not in delete_lst]

#The masked images are labeled "Fred_0" and "Fred_1" corresponding to FOMC meetings before and after the COVID-related recession. I downloaded the graph from Fred and then opened and edited it in Gimp. You can use the fuzzy select tool and bucket fill tool to select and fill the two masks with black. Be sure to select and fill everything but the mask with white. 

#Change the contour_color to 'white'. The Fred graph will have the funds rate already shown.
    unique_string_v2=(" ").join(words_v2)
    #print(unique_string_v2)
    cloud_mask = np.array(Image.open("Fred_{}.png".format(meetings)))    
    wordcloud = WordCloud(width = 1000, height = 500, background_color="white",
                          mask=cloud_mask, max_words=5000, contour_width=2, contour_color='white')
    wordcloud.generate(unique_string_v2)

#The two generated wordclouds are "word_cloud_masked_0" and "word_cloud_masked_1" corresponding to "Fred_0" and "Fred_1". I cleaned up the edges in Gimp with the feather tool, too. Finally, select and create translucent areas in the original Fred graph by adding an alpha layer in the selection. Save the image as .png or the image type needed.
    wordcloud.to_file("word_cloud_masked_{}.png".format(meetings))

img1 = Image.open(r"Fred.png") 
img2 = Image.open(r"word_cloud_masked_0.png") 
img3 = Image.open(r"word_cloud_masked_1.png")
img4 = Image.open(r"Fredtrans.png")

# No transparency mask specified,  
# simulating an raster overlay 
img3.paste(img2, (0,0)) 

#transparency mask specified as img4.
img3.paste(img4, (0,0), mask = img4) 
  
img3.show()
