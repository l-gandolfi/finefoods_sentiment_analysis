import pandas as pd
from nltk.tokenize import word_tokenize

#Caffe
#Very Smooth Rich flavor even on the largest setting, dark blend a very satisfying cup of coffee
#A2MP7KWDQ2JVT
#productid: B0089SPDUW
#My husband and I were very disappointed in this coffee, very weak, watery cup of coffee. A definite waste of $13.00.
#A2DYZJ8D7QD1KE
#productid: B004WJAUBE

#Chip
#A1IRN1M05TPOVT
#WOW!  I have eaten quite a few potato chips in my day. Kettle chips are the BEST non-baked chips I have eaten. I decided to try the sweet onion chips, since I've never had them. I now have a FAVORITE!! If you like onions, this is a MUST buy! I will definitely reorder these, as I mentioned above, they are the BEST I have ever eaten! The flavor is GREAT.
#productid: B0058AMY74

#Tea
#A3VEYLW2KPZNGK
#I have been drinking this tea for a long time now.  I used to have to purchase it at a doctor's office because it wasn't available elsewhere.  I'm so glad that I can buy it now from Amazon.com.  I drink this tea throughout the day like other folks drink coffee.  Wonderful taste.
#productid: B0037LW78C

#dogfood
#AC3ZR64550O35
#THESE TREATS ARE THE ONLY ONES MY 14 YEAR OLD DOG WILL EAT. SHE LOVES THEM.
#productid: B002CTJG02


##A2ISKAWUPGGOLZ

#petfood
#A3V0CYPXC5C3KT
#I have 4 dogs and all were sick on this food. One actually almost died. It had to be ressucitated. After I spent $4,000.00 on Vet's bills I decided to call the FDA to analize this food. They found Ethoxyquin on it - a pesticide. [...] I just want to make sure if someone out there has the same problem, that it must be known. I'm still not happy about this incident. I decided not to pursue it any longer, but I still feel people should know. These 'Organic' companies can't get away misleading people. If everyone exposed them, then this would be a better world. Think about it...<br /><br /><a href=""http"
#productid: B00139TT72

#A1NUGHVW06D9AA
#This slop has the color and consistency of baby diarrhea with whole peas in it. Our cat ate less than half a bowl of this slop and immediately puked all over the carpet!<br /><br />She devours the Felidae Platinum, (which we feed as an occasional alternative to Newman's Own Turkey). She was raised on Felidae dry, so I can say that generally the Canidae Company provides quality products... except for this grain-free slop. You can find the good stuff at
#productid: B003R0LKSG

#leggo il dataset con pandas
def create_df_topic():
    dataframe = pd.DataFrame(columns=['topic', 'text', 'score', 'afinn', 'vader compound'])
    df = pd.read_csv('../reviews_final.csv')
    i = 0

    #Topic sul caffè
    #Sentiment Positivo
    df1 = df.loc[df['userid'] == 'A2MP7KWDQ2JVT']
    dataframe.loc[i] = [str('coffee')] + [str(df1.text.values[0])] + [str(df1.score.values[0])] + [str(df1.afinn.values[0])] + [str(df1['vader compound'].values[0])]
    i = i + 1
    #Sentiment Negativo
    df1 = df.loc[df['userid'] == 'A2DYZJ8D7QD1KE']
    dataframe.loc[i] = [str('coffee')] + [str(df1.text.values[0])] + [str(df1.score.values[0])] + [str(df1.afinn.values[0])] + [str(df1['vader compound'].values[0])]
    i = i + 1

    #Topic sulle chip
    df1 = df.loc[df['userid'] == 'A1IRN1M05TPOVT']
    dataframe.loc[i] = [str('chip')] + [str(df1.text.values[1])] + [str(df1.score.values[1])] + [str(df1.afinn.values[1])] + [str(df1['vader compound'].values[1])]
    i = i + 1

    #Topic sul tea
    df1 = df.loc[df['userid'] == 'A3VEYLW2KPZNGK']
    dataframe.loc[i] = [str('tea')] + [str(df1.text.values[0])] + [str(df1.score.values[0])] + [str(df1.afinn.values[0])] + [str(df1['vader compound'].values[0])]
    i = i + 1

    #Topic sul dogFood
    df1 = df.loc[df['userid'] == 'AC3ZR64550O35']
    dataframe.loc[i] = [str('dogFood')] + [str(df1.text.values[0])] + [str(df1.score.values[0])] + [str(df1.afinn.values[0])] + [str(df1['vader compound'].values[0])]
    i = i + 1

    #Topic sul petFood
    df1 = df.loc[df['userid'] == 'A3V0CYPXC5C3KT']
    dataframe.loc[i] = [str('petFood')] + [str(df1.text.values[0])] + [str(df1.score.values[0])] + [str(df1.afinn.values[0])] + [str(df1['vader compound'].values[0])]
    i = i + 1

    #Topic sul petFood
    df1 = df.loc[df['userid'] == 'AS0A4EHP1XRT8']
    dataframe.loc[i] = [str('petFood')] + [str(df1.text.values[0])] + [str(df1.score.values[0])] + [str(df1.afinn.values[0])] + [str(df1['vader compound'].values[0])]

    return(dataframe)

create_df_topic()
