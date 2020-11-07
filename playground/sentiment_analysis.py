#%%
import pandas as pd
import re
import os
import nltk

def read_dataset(file_name):
    path = os.path.join("./..",file_name)
    return pd.read_csv(path, sep=";")

def labmt():
    return pd.read_csv("./../labmt-sentiment-data.txt",sep="\t")

def read_words_to_sentiment_values(labmt_dataframe):
    df = labmt_dataframe
    words = df["word"].values
    sentiment_values = df["happiness_average"].values
    words_to_sentiment_values = {}

    for w, sv in zip(words, sentiment_values):
        words_to_sentiment_values[w] = sv

    return words_to_sentiment_values

def comment_to_tokens(comment):
    tokens = re.findall(r"\w+(?:[-']*\w*)*", comment)
    tokens = [w.lower() for w in tokens]
    return tokens

def tokens_to_sentiment(tokens, words_to_sentiment_values,mean=True):
    w_to_sv = words_to_sentiment_values
    fdist = nltk.FreqDist(tokens)
    sentiment=[]
    for word, frequency in fdist.items():
        if word in w_to_sv.keys():
            sentiment_score = w_to_sv[word] * frequency
            sentiment.append(sentiment_score)

    if len(sentiment) == 0:
        return None

    if not mean:
        sentiment = sum(sentiment)
    else:
        sentiment = sum(sentiment) / len(sentiment)

    return sentiment



#%%
test = read_dataset("testdata.csv")
comments = test["comment"].values

# %%

tc = comments[1]
print(tc)

# %%
ttoken = comment_to_tokens(tc)
print(ttoken)
# %%

w2sv = read_words_to_sentiment_values(labmt())

# %%

sscore = tokens_to_sentiment(ttoken, w2sv)

# %%
print(sscore)
# %%
