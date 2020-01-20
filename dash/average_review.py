import pandas as pd
from nltk.tokenize import word_tokenize

#leggo il dataset con pandas
def create_df_year():
    dataframe = pd.DataFrame(columns=['year', 'score', 'mean'])
    i = 0
    df = pd.read_csv('../reviews_final.csv')
    df['len'] = df['text'].apply(len)

    years_mean = {}
    #lunghezza delle review in media anno per anno by score
    for year in range(2000,2013):
      different_year = df[df['year'] == year]
      years_mean[year] = {}
      for score in range(1,6):
        different_score = different_year[different_year['score']==score]
        sumL = 0

        for j in range(0,len(different_score)):
          sumL = sumL + different_year.iloc[j].len
        if(year != 2001 and year != 2002):
          years_mean[year][score] = sumL/len(different_year)
          dataframe.loc[i] = [str(year)] + [str(score)] + [sumL/len(different_year)]
          i = i+1
          #print("anno: ", year," score: ",score, " lunghezza media: ", sumL/len(different_year))

    years_mean_grouped = {}
    for score in range(1,6):
        years_mean_grouped[score] = {}

    for year in range(2000,2013):
        for score in range(1,6):
            if(year != 2001 and year != 2002):
                years_mean_grouped[score][year] = years_mean[year][score]

    return(dataframe)
    #print(years_mean_grouped[1])
