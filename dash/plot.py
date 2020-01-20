import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def score_by_year():
	df = pd.read_csv('../reviews_final.csv')
	years = df.year
	seen = set()
	for e in years:
		if(e not in seen):
			seen.add(e)

	names = []
	for e in seen:
		names.append(e)

	products_score = []
	groups = df.sort_values('year', ascending=False).groupby('year')['score'].mean()
	temp = groups.to_frame()
	for row in groups:
		products_score.append(row)

	return(products_score)
	'''
	plt.figure(figsize=(20, 15))
	plt.bar(names, products_score)
	plt.xticks(names)
	#plt.yticks(products_score)
	plt.show()
	#this plot shows the distribution of the score by year

	#the next plot will show grouped per productid by year

	for e in years:
	'''
