# **Data Analytics**

## Sentiment analysis on Amazon FineFoods Reviews

* Luca Gandolfi 807485
* Stefano Sacco 807532

### Introduction
The aim of this project is to analyze the sentiment of users and use Natural Language Process tecniques.
The dataset chosen for this work is the Amazon FineFoods Reviews, but the analysis are performed on a portion of the original dataset. About 100.000 reviews has been used, instead of 500.000 of the original dataset.

### Libraries
Full analysis is written in Python 3, but the ASUM approach we have used is the Yohan Jo's code written in Java.
The must-have libraries to run this project are:

* pandas for manipuating data
* nltk for text processing
* afinn and vaderSentiment for sentiment analysis
* gensim and spacy for LDA
* matplotlib for plotting
* dash for the demo


### File and folders
In this repository you can find 3 Python-notebook, about the analysis and the simple Machine Learning model we have trained. You can also find some Python scripts in different files, for plotting, testing LDA and manipulating data for ASUM's requirements. Of course you can find the datasets used in this project, which for semplicity are 3: the original food.tsv, used in ASUM and LDA, reviews_small_timed.csv which has been used for the analysis and reviews_final.csv which has been used in dash.
Finally, you can find the documentation about this project.

### Tasks performed and their order
Here are the tasks performed in this project:
1. General analysis of data
2. Text processing
3. Analysys about bot presence viewing worst users
4. Afinn and vaderSentiment
5. Topic modelling with LDA
6. Aspect and sentiment -based approch using Yohan Jo's ASUM
