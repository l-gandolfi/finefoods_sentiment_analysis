import gensim
import spacy
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
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
from nltk.tokenize import wordpunct_tokenize
import re
import csv

#df = pd.read_csv('reviews_small_timed.csv')
h = ['productid', 'userid', 'score', 'text']
df = pd.read_csv('food.tsv', sep = '\t', skiprows = 1, header = None, encoding = 'latin-1', names = h)

#Dicts of contractions
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

#Remove punctuation in a list
pattern = re.compile(r'[\W_]+')
def strip_token(token):
    token = pattern.sub('', token).strip()
    if len(token): return token
    return None

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

#Remove None tokens in a list
def remove_none(lista):
    lista = list(filter(None, lista))
    return lista

#Convert all reviews in lower case
text = df['text']
df['text'] = list(map(lambda x: x.lower(), text))

#Cleaning text using function to remove contractions
clean_text = []
for text in df.text:
   clean_text.append(clean(text))
df['clean_text'] = clean_text

#Let's tokenize the reviews using word_tokenize from nltk
df['tokenized'] = df.apply(lambda row: wordpunct_tokenize(row['clean_text']), axis=1)
text_tokenized = df['tokenized']

#remove stopwords
stop = stopwords.words('english')
stop = set(stop)
stop.remove('not')
stop.add("''")
stop.add("'s'")
stop.add("p.s")
stop.add("...")
stop.add('``')
stop.add("br")
tokenized_stop = text_tokenized.apply(lambda x: [item for item in x if item not in stop])

#remove punctuation
punctuation = string.punctuation
tokenized_stop_punct = []
for sentence in tokenized_stop:
    el = []
    for element in sentence:
        element = strip_token(element)
        el.append(element)
    el = list(filter(None, el))
    el = list(filter(lambda x: not x.isdigit(), el))
    tokenized_stop_punct.append(el)

#Concatenating token["not"] and token[generic word] if token["not"] comes before a token[generic word]
#Every token["not"] at the and of a sentece will be removed later
count = 0
for row in tokenized_stop_punct:
  new_row = []
  b = False
  for word in row:
    if(b):
      new_row.append(str('not'+word))
      b = False
    elif(word == 'not'):
      b = True
    else:
      new_row.append(word)
  tokenized_stop_punct[count] = new_row
  count = count + 1

#Adding the "not" word to stopwords again
#This is why we have to delete the last token["not"] left at the end of sentences
stop.add('not')
final_tokenized = list(map(lambda x: list(filter(lambda x: x not in stop, x)), tokenized_stop_punct))

print('\n\n')
print(final_tokenized[:1])

#Create object stemmer
lancaster_stemmer = LancasterStemmer()
final_tokenized_stem = []
for sentence in final_tokenized:
	sublist = []
	for subsent in sentence:
		sublist.append(lancaster_stemmer.stem(subsent))
	final_tokenized_stem.append(sublist)
#final_tokenized_stem = list([lancaster_stemmer.stem(item) for sentence in final_tokenized for item in sentence])

print('\n\n')
print(final_tokenized_stem[:1])
sentences = final_tokenized_stem
sentence_list = [sublist for sublist in sentences]

#DA QUA INIZIA LDA

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

bigram = gensim.models.Phrases(sentences, min_count=5, threshold=100)
bigram_mod = gensim.models.phrases.Phraser(bigram)
#trigram_mod = gensim.models.phrases.Phraser(trigram)
#print("Provo a vedere un trigram",trigram_mod[bigram_mod[sentence_list[0]]])



# Form Bigrams
data_words_bigrams = make_bigrams(sentences)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

print("Frase after lemmatize",data_lemmatized[:1])


# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Human readable format of corpus (term-frequency)
[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]


#Creating LDA model
print('\nBuilding the model\n')
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=100,
                                           alpha='auto',
                                           per_word_topics=True)
topics = lda_model.print_topics()

print(topics)
#topics = zip(*topics)

# Visualize the topics
p = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.save_html(p, 'lda.html')
