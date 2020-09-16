#!/usr/bin/env python
# coding: utf-8
from afinn import Afinn
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter
import itertools

from nltk.corpus import stopwords
import string
from nltk import wordpunct_tokenize
from nltk.tag import *

from nltk.stem.lancaster import LancasterStemmer
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import re
import nltk

contractions = {
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}

pattern = re.compile(r'[\W_]+')
def strip_token(token):
    token = pattern.sub('', token).strip()
    if len(token): return token
    return None

#Remove None tokens in a list
def remove_none(lista):
    lista = list(filter(None, lista))
    return lista

wl = []
with open('WordList.txt', 'r') as wordlist:
    for row in wordlist:
        wl.append(row)

print(wl)

#leggo il dataset con pandas
#df = pd.read_csv('reviews_small_afinn.csv')

#Importing Amazon reviews Dataset
h = ['productid', 'userid', 'score', 'text']
df = pd.read_csv('food.tsv', sep = '\t', skiprows = 1, header = None, encoding = 'latin-1', names = h)

#Convert all reviews in lower case
text = df['text']
df['text'] = list(map(lambda x: x.lower(), text))

#de-contract words
def clean(text):
  text = text.split()
  new_text = []
  for word in text:
    if word in contractions:
      new_text.append(contractions[word])
    else:
      new_text.append(word)
  text = " ".join(new_text)
  return text

clean_text = []
for text in df.text:
   clean_text.append(clean(text))
df['clean_text'] = clean_text


#Let's tokenize the reviews using word_tokenize from nltk
df['tokenized_clean'] = df.apply(lambda row: sent_tokenize(row['clean_text']), axis=1)

clean_tokenized = df['tokenized_clean']

df['word_tokenize'] = clean_tokenized.apply(lambda x: [wordpunct_tokenize(item) for item in x])

text_tokenized_word = df['word_tokenize']

#remove stopwords
stop = stopwords.words('english')
stop = set(stop)
stop.remove('not')
stop.add("''")
stop.add('``')
stop.add("br")
stop.add("em")
stop.add("...")

text_tokenized_stop = []
for sentence in text_tokenized_word:
    sublist = []
    for subsent in sentence:
        el = []
        for element in subsent:
            if(element not in stop):
                el.append(element)
        if('ecofriendly' in el):
            print(el)
        sublist.append(el)
    text_tokenized_stop.append(sublist)

#remove puntaction
punctuation = string.punctuation

l = []
for sentence in text_tokenized_stop:
    sub = []
    for sublist in sentence:
        el = []
        for element in sublist:
            element = strip_token(element)
            '''
            if(element not in punctuation):
            '''
            el.append(element)
        if('ecofriendly' in el):
            print("questa è ecofriendfly",el)
        el = list(filter(None, el))
        el = list(filter(lambda x: not x.isdigit(), el))
        sub.append(el)
    l.append(sub)



l2 = []
for lists in l:
    new_row = []
    for row in lists:
        sublist = []
        b = False
        for word in row:
            if(b):
                if(str(word)=='ecofriendly'):
                    print("boolean",b)
                    print("parola",word)
                sublist.append(str('not' + word))
                b = False
            elif(str(word) == 'not'):
                b = True
            else:
                sublist.append(word)
        new_row.append(sublist)
    l2.append(new_row)


'''
l2 = []
for lists in l:
	new_row = []
	for row in lists:
		sublist = []
		b = False
		for word in row:
			if(b):
    			sublist.append(str('not' + word))
    			b = False
			if(word == 'not'):
			    b = True
			else:
			    sublist.append(word)
		new_row.append(sublist)
	l2.append(new_row)
'''

lancaster_stemmer = LancasterStemmer()
l3 = []
print("token stemmed")
for sentence in l2:
	sublist = []
	for subsent in sentence:
		el = []
		for element in subsent:
			el.append(lancaster_stemmer.stem(element))
		sublist.append(el)
	l3.append(sublist)

'''
for e in l3:
    print("------------------TEST-------------------------------")
    print(e)
'''

count = 0
with open('BagOfSentences.txt', 'w') as outfile:
    for sentence in l3:
        outfile.write(str(len(sentence)))
        outfile.write('\n')
        for subsentence in sentence:
            stringa = ''
            for element in subsentence:
                index = wl.index(str(element+'\n'))
                stringa = stringa+ str(index)
                stringa = stringa + ' '
            print(stringa)
            outfile.write(stringa)
            outfile.write('\n')
        count = count + 1
        print(count)
