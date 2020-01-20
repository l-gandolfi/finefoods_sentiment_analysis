#!/usr/bin/env python
# coding: utf-8

# In[3]:

'''
get_ipython().system('pip install afinn')
get_ipython().system('pip install vaderSentiment')
get_ipython().system('pip install sklearn')
'''

# In[4]:


import nltk
nltk.download('punkt')
nltk.download('stopwords')
from afinn import Afinn
import numpy as np
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from collections import Counter
import itertools

from nltk.corpus import stopwords
import string
from nltk import wordpunct_tokenize

from nltk.stem.lancaster import LancasterStemmer
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
from PIL import Image
import numpy as np

from wordcloud import WordCloud

from sklearn.preprocessing import MinMaxScaler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# In[ ]:


#leggo il dataset con pandas
df = pd.read_csv('reviews_small_timed.csv')


# In[ ]:


#applichiamo Afinn alle review e aggiungiamo lo score in una nuova colonna
afinn = Afinn()
df['afinn'] = df['text'].apply(afinn.score)
df[['afinn', 'text']].head()
values = df.afinn.value_counts()


# In[7]:

'''
df[['score','afinn']].head(10)
'''

# In[8]:

'''
pd.crosstab(df.score, df.afinn)
'''

# In[9]:


#vogliamo ora portare i risultati in 3 classi: -1 , 0, +1
'''
confusion = pd.crosstab(np.sign(df.score -3), np.sign(df.afinn))
confusion
'''

# In[10]:


'''non più utilizzato ma potrebbe tornare utile
scaler = MinMaxScaler()
df['afinn normalized'] = scaler.fit_transform(df['afinn'].values.reshape(-1,1))
df[['score','afinn', 'afinn normalized']].head(10)
'''


# In[ ]:


#applichiamo ora il vader score sentiment
analyzer = SentimentIntensityAnalyzer()
df['vader'] = df['text'].apply(analyzer.polarity_scores)


# In[12]:

'''
df[['score','afinn', 'vader']].head(10)
'''

# In[ ]:


#accediamo come un dict all'oggetto compound che ci restituisce un valore tra -1 e 1
temp = []
for i in range(0,100000):
   temp.append(dict(df.iloc[i].vader)['compound'])
df['vader compound'] = temp

# In[14]:


#Per andare a confrontare le due valutazioni diverse, andiamo a considerare le 3 classi: -1, 0, 1
#Per Afinn guarderemo il segno
#Per vader assegneremo lo 0 per valori compound t.c. -0.05 < compound < 0.05
'''
temp = []
for i in range(0,100000):
  t = float(df.iloc[i]['vader compound'])
  if(t >= 0.05):
    temp.append('1')
  elif(t <= -0.05):
    temp.append('-1')
  else:
    temp.append('0')
df['vader polar'] = temp

df[['vader polar','vader compound']].head(20)
'''

# In[15]:
'''

temp = []
for i in range(0,100000):
  t = float(df.iloc[i]['afinn'])
  if(t > 0):
    temp.append('1')
  elif(t < 0):
    temp.append('-1')
  else:
    temp.append('0')
df['afinn polar'] = temp

df[['afinn polar','afinn']].head(20)
'''

# In[16]:
'''

df.drop(['vader','vader compound'], axis=1)

'''
# In[17]:

#Save new DF
df.to_csv('reviews_final.csv', index=False)

#Andiamo quindi a plottare i confronti degli score e traiamo delle conclusioni
c1 = Counter(df['vader polar'])
c2 = Counter(df['afinn polar'])
print(c1)
print(c2)

'''come è possibile osservare dalle print, gli score positivi sono numericamente simili.
le due tecniche hanno trovato differenze un po più significative per gli score 
negativi e neutri.
'''

#plt.bar(c1.keys(), c1.values())
#plt.bar(c2.keys(), c2.values())

'''
#verifichiamo dove gli score non combaciano
vader_positive = df[(df['vader polar']=='1')]
#vader_positive.head(10)
t = vader_positive[(vader_positive['afinn polar'] != '1')]
print(len(t)) #ben 4622 review sono classificate diversamente da afinn


# In[38]:


#volte in cui afinn sbaglia in negativo
subset_df = df[df['afinn polar'] == "-1"]
subsubset_df = subset_df[subset_df['score'] == 5]
print(subsubset_df.head(10))
print(len(subsubset_df))


# In[30]:


df.iloc[292].text


# In[39]:


#volte in cui vader sbaglia in negativo
subset_df = df[df['vader polar'] == "-1"]
subsubset_df = subset_df[subset_df['score'] == 5]
print(len(subsubset_df))


# In[40]:


subset_df = df[df['vader polar'] == "1"]
subsubset_df = subset_df[subset_df['score'] == 1]
print(subsubset_df.head(10))
print(len(subsubset_df))


# In[44]:


df.iloc[229].text


# In[41]:


subset_df = df[df['afinn polar'] == "1"]
subsubset_df = subset_df[subset_df['score'] == 1]
print(len(subsubset_df))


# In[63]:


#lunghezza delle review in media anno per anno
import statistics

df['len'] = df['text'].apply(len)

for i in range(2000,2013):
  different_year = df[df['year'] == i]
  sumL = 0
  for j in range(0,len(different_year)):
    sumL = sumL + different_year.iloc[j].len
  if(i != 2001 and i != 2002):
    print(sumL/len(different_year))


# In[68]:


#lunghezza delle review in media anno per anno by score
for i in range(2000,2013):
  different_year = df[df['year'] == i]
  for score in range(1,6):
    different_score = different_year[different_year['score']==score]
    sumL = 0

    for j in range(0,len(different_score)):
      sumL = sumL + different_year.iloc[j].len
    if(i != 2001 and i != 2002):
      print("anno: ", i," score: ",score, " lunghezza media: ", sumL/len(different_year))


# In[ ]:
'''



