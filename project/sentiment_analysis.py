#%%
import pandas as pd
import re
import os
import nltk
import wordcloud
import matplotlib.pyplot as plt

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

def get_TFTR(trump_tokens, biden_tokens, c):
    t_tf = nltk.FreqDist(trump_tokens)
    b_tf = nltk.FreqDist(biden_tokens)
    t_tftr = []
    b_tftr = []
    for (token, t_freq) in t_tf.items():
        b_freq = b_tf[token]

        t_wt = t_freq / (t_freq + c)
        b_wt = b_freq / (b_freq + c)

        t_tftr.append((token,t_wt))
        b_tftr.append((token,b_wt))

    return t_tftr, b_tftr

def get_freq_string(tftr):
  freq_string = ""
  for (token, score) in tftr:
    token = token.replace("-", "")
    score = round(score)
    freq_string += score * (token + " ")
  return freq_string

def dataframe_comments_to_tokens(dataframe):
    df = dataframe
    dataframe_comments_tokens = []
    for comment in df["comment"]:
        tokens = comment_to_tokens(comment)
        dataframe_comments_tokens += tokens
    return dataframe_comments_tokens




if __name__ == "__main__":
    df = pd.read_csv("data/csv_files/data_all_merged.csv", sep=";")

    trump_df = df[df["from_subreddit"]=="trump"]
    biden_df = df[df["from_subreddit"]=="biden"]

    trump_tokens = dataframe_comments_to_tokens(trump_df)
    biden_tokens = dataframe_comments_to_tokens(biden_df)

    trump_tftr, biden_tftr = get_TFTR(trump_tokens, biden_tokens, c=1)
    trump_tftr.sort(reverse=True, key=lambda t: t[1])
    biden_tftr.sort(reverse=True, key=lambda t: t[1])

    trump_freqstring = get_freq_string(trump_tftr)
    biden_freqstring = get_freq_string(biden_tftr)

    trumpcloud = wordcloud.WordCloud(background_color="white", collocations=False, colormap="ocean")
    bidencloud = wordcloud.WordCloud(background_color="white", collocations=False, colormap="ocean")

    trumpcloud = trumpcloud.generate(trump_freqstring)
    bidencloud = bidencloud.generate(biden_freqstring)
    plt.subplots(figsize=(10,8))
    plt.title("TrumpCloud")
    plt.imshow(trumpcloud)
    plt.axis("off")
    plt.show()
    plt.subplots(figsize=(10,8))
    plt.title("BidenCloud")
    plt.imshow(bidencloud)
    plt.axis("off")
    plt.show()
#%%


# %%
