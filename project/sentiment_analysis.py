import pandas as pd
import re
import os
import nltk
import wordcloud
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
#nltk.download("wordnet")

def read_dataset(file_name):
    path = os.path.join("./..",file_name)
    return pd.read_csv(path, sep=";")

def labmt():
    return pd.read_csv("data/labmt-sentiment-data.txt",sep="\t")

def read_words_to_sentiment_values(labmt_dataframe):
    df = labmt_dataframe
    words = df["word"].values
    sentiment_values = df["happiness_average"].values
    words_to_sentiment_values = {}

    for w, sv in zip(words, sentiment_values):
        words_to_sentiment_values[w] = sv

    return words_to_sentiment_values

def comment_to_sentiment(comment, words_to_sentiment_values):
    tokens = comment_to_tokens(comment)
    sentiment = tokens_to_sentiment(tokens, words_to_sentiment_values)
    return sentiment

def comment_to_tokens(comment):
    tokens = re.findall(r"\w+(?:[-']*\w*)*", comment)
    tokens = [w.lower() for w in tokens]
    return tokens

def lemmatize_tokens(tokens, lemmatizer):
    # a lemmatizer is a WordNetLemmatizer object
    # i.e. lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []
    for token in tokens:
        lemmatized_token = lemmatizer.lemmatize(token)
        lemmatized_tokens.append(lemmatized_token)
    return lemmatized_tokens

def tokens_to_sentiment(tokens, words_to_sentiment_values):
    w_to_sv = words_to_sentiment_values
    fdist = nltk.FreqDist(tokens)
    sentiment = 0
    n_avg = 0
    for word, frequency in fdist.items():
        if word in w_to_sv.keys():
            sentiment += w_to_sv[word] * frequency
            n_avg += 1*frequency

    if sentiment == 0:
        return None
    else:
        sentiment = sentiment / n_avg

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

