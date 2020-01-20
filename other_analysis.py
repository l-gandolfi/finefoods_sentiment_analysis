import pandas as pd
import matplotlib
import numpy
from collections import Counter

df = pd.read_csv('reviews_small_timed.csv')

def most_criticato():
	df1 = df.groupby('productid')['score'].agg(['count','mean']).reset_index()
	filtered= df1[df1['mean']==1]
	sort = filtered.sort_values('count', ascending=False)
	print(sort)

def most_valutato():
	df1 = df.groupby('productid')['score'].agg(['count','mean']).reset_index()
	filtered= df1[df1['mean']==5]
	sort = filtered.sort_values('count', ascending=False)
	print(sort)

def most_count_valutato():
	df1 = df.groupby('productid')['score'].agg(['count','mean']).reset_index()
	filtered= df1[df1['count']>100]
	sort = filtered.sort_values('mean', ascending=False)
	print(sort)

def most_count_criticato():
	df1 = df.groupby('productid')['score'].agg(['count','mean']).reset_index()
	filtered= df1[df1['count']>20]
	sort = filtered.sort_values('mean', ascending=True)
	print(sort)
most_count_criticato()
