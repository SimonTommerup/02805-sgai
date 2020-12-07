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

def comment_to_sentiment(comment, words_to_sentiment_values, lemmatizer):
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

def tokens_to_sentiment_alt(tokens, words_to_sentiment_values,mean=True):
    w_to_sv = words_to_sentiment_values
    sentiment_of_text = 0
    n_avg = 0
    # Create the frequency distribution and loop through it
    fdist = nltk.FreqDist(tokens)
    for w, f in fdist.items():
        # Check if the token is a part of the LabMT list
        if w in w_to_sv.keys():
            # Compute the weighted sentiment of this token (according to how many times the word occurs)
            sentiment_of_text += words_to_sentiment_values[w]*f
            # Only compute the average with respect to the words which are in the LabMT list
            n_avg+=1*f

    # return error (-1) if none of the words in 'tokens' exist in the LabMT list
    return sentiment_of_text/n_avg if n_avg>0 else -1


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
    df = pd.read_csv("data/csv_files/data_all_merged_with_sentiment.csv", sep=";")
    dfcop = df.copy()
    print(dfcop.head(1))
    w2sv = read_words_to_sentiment_values(labmt())
    lem = WordNetLemmatizer()
    comments = [c for c in df["comment"]]

    sentiments = []
    for comment in comments:
        sentiment = comment_to_sentiment(comment, w2sv, lem)
        sentiments.append(sentiment)


    #print(sum(sentiments)/len(sentiments))

    dfcop["comment_sentiment"] = sentiments
    print(dfcop.head(1))

    columns=["user","from_subreddit","comment","used_subreddits" ,"comment_sentiment"]
    dfcop.to_csv("data/csv_files/data_all_merged_with_sentiment.csv",sep=";",columns=columns,index=False)
"""
    df_nona = df.copy()


    df_nona = df_nona[df_nona["comment_sentiment"].isna()==False]

    print("avg: ", sum(df_nona["comment_sentiment"])/len(df_nona))

    lem = WordNetLemmatizer()
    w2sv = read_words_to_sentiment_values(labmt())

    print((sum(df_nona["comment_sentiment"])-43) / (len(df_nona)+43))
    #s = comment_to_sentiment(com, w2sv, lem)
    #print(s)
"""