import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def score_by_year():
	df = pd.read_csv('reviews_small_timed.csv')
	years = df.year
	seen = set()
	for e in years:
		if(e in seen):
			print(e)
		else:
			seen.add(e)
	print('\n\n\n\n')
	
	names = []
	for e in seen:
		names.append(e)
	print(names)
	
	products_score = []
	groups = df.sort_values('year', ascending=False).groupby('year')['score'].mean()
	temp = groups.to_frame()
	print(temp)
	for row in groups:
		products_score.append(row)

	plt.figure(figsize=(20, 15))
	plt.bar(names, products_score)
	plt.xticks(names)
	#plt.yticks(products_score)
	plt.show()
	#this plot shows the distribution of the score by year
	
	#the next plot will show grouped per productid by year
	'''	
	for e in years:
	'''	
	
#score_by_year()

def quantity_by_year():
	df = pd.read_csv('reviews_small_timed.csv')
	years = df.year
	seen = set()
	for e in years:
		if(e in seen):
			print(e)
		else:
			seen.add(e)
	print('\n\n\n\n')
	
	names = []
	for e in seen:
		names.append(e)
	#print(names)
	
	products_score1 = [0,0]
	products_score5 = []
	
	for year in names:
		group = df[df['year']==year]
		#temp1 = group[df['score']=='5']
		c = Counter(group['score'])
		print(c)
		for key,value in c.items():
			#if(year == 2000 or year == 2003):
			#	products_score1.append(0)
			if(key==1):
				products_score1.append(value)
			if(key==5):
				products_score5.append(value)
		#products_score5.append(c.5)
	print(products_score5)
	print(names)

	ind = np.arange(len(products_score5))  # the x locations for the groups
	width = 0.5  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind - width/2, products_score1, width, yerr=names,
		            label='Score=1')
	rects2 = ax.bar(ind + width/2, products_score5, width, yerr=names,
		            label='Score=5')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Scores')
	ax.set_title('Scores by year')
	ax.set_xticks(ind)
	ax.set_xticklabels(names)
	ax.legend()
	fig.tight_layout()

	plt.show()

score_by_year()	
#quantity_by_year()
