#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 22:32:17 2023

@author: welcome870117
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 17:28:06 2022

@author: welcome870117
"""

import pandas as pd
import re, string
import emoji
import nltk
from sklearn import preprocessing
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import word_tokenize     #以空格形式实现分词
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer , PorterStemmer , LancasterStemmer
from nltk.stem import WordNetLemmatizer

# stop word dictionary
stops = set(stopwords.words("english"))

#＊＊＊＊＊＊＊＊＊data preprocessing function ＊＊＊＊＊＊＊＊＊＊＊ #

# remove same element
def delete_same_element(inputdata):
    '''
    
    Parameters
    ----------
    inputdata : dataframe
        text dataset
    
    Returns
    -------
    inputdata : dataframe
        text dataset without same text
    
    '''
    inputdata.drop_duplicates(subset='new_reply',inplace=True)
    inputdata.reset_index(drop=True,inplace=True)
    return inputdata

# remove emoji
def strip_emoji(text):
    
    '''
    re : 正則表達式的模塊 / re是regular expression的所寫，表示正規表示式
    re.sub : sub是substitute的所寫，表示替換 / re.sub(替換對象,替換目標,string)
    emoji.get_emoji_regexp() : 獲取表情符號？
    '''
    
    return re.sub(emoji.get_emoji_regexp(), r"", text) #remove emoji

#  
def strip_all_entities(text): 
    text = text.replace('\r', '').replace('\n', ' ').replace('\n', ' ').lower() #remove \n and \r and lowercase
    text = re.sub(r"(?:\@|https?\://)\S+", "", text) #remove links and mentions
    text = re.sub(r'\\[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9]',r'', text) #remove non utf8/ascii characters such as '\x9a\x91\x97\x9a\x97'
    banned_list= string.punctuation + 'Ã'+'±'+'ã'+'¼'+'â'+'»'+'§'
    table = str.maketrans('', '', banned_list)
    text = text.translate(table)
    return text

#clean hashtags at the end of the sentence, and keep those in the middle of the sentence by removing just the # symbol
def clean_hashtags(tweet):
    new_tweet = " ".join(word.strip() for word in re.split('#(?!(?:hashtag)\b)[\w-]+(?=(?:\s+#[\w-]+)*\s*$)', tweet)) #remove last hashtags
    new_tweet2 = " ".join(word.strip() for word in re.split('#|_', new_tweet)) #remove hashtags symbol from words in the middle of the sentence
    return new_tweet2

#Filter special characters such as & and $ present in some words
def filter_chars(a):
    sent = []
    for word in a.split(' '):
        if ('$' in word) | ('&' in word):
            sent.append('')
        else:
            sent.append(word)
    return ' '.join(sent)

# remove multiple spaces
def remove_mult_spaces(text): 
    return re.sub("\s\s+" , " ", text)

def tokenize(sentence):
    tokenization = word_tokenize(sentence)
    return tokenization

def remove_stop_word(tokenization):
    return [word for word in tokenization if word not in stops]

def stemming(sentence):
    return [SnowballStemmer(word) for word in sentence]

def stemming_snowball(sentence):
    return [SnowballStemmer('english').stem(word) for word in sentence]

def lemmatizer(sentence):
    #return [ WordNetLemmatizer().lemmatize(cutword2,pos='v') ]
    return [WordNetLemmatizer().lemmatize(word) for word in sentence]

if __name__ == '__main__':
    text = ''
                            
    lemmatizer(remove_stop_word(tokenize(remove_mult_spaces(filter_chars(clean_hashtags(strip_all_entities(strip_emoji(text))))))))

# ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ conclusion ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊ ＊
'''
Compared with stemming, lemmatizer has a better effect, because it reduces some illogical words, and social media 
often has misspellings, causing more stemming to cut out more illogical words, but the effect of lemmatization 
is not very good, because the main method is through table lookup, but there are too many characters out of range.

Experiment: 
    Compare with lemmatization , stemming , none 

'''