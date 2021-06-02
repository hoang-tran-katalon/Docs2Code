# Input: URL
# Output: list of tutorials
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

import re
import pickle
import requests
from scrapy import Selector

import constants

model_loaded = tf.keras.models.load_model('./models/classifier.h5')
with open('./models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def remove_tags(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_html)
    clean_text.replace('\n', '')
    return clean_text


def get_sentences_from_url(url):
  html = requests.get(url).content
  sel = Selector(text=html)

  css_path = 'div#article-contents'
  sentences = []
  for sentence in sel.css(css_path).extract():
    sentence = remove_tags(sentence)
    sentence = sentence.replace('\n', '').strip().split('.')
    sentence = [string for string in sentence if string != ""]
    sentences.append(sentence)

  return [item.strip() for sublist in sentences for item in sublist]


def get_tutorials_from_url(url):
  html = requests.get(url).content
  sel = Selector(text=html)

  css_path = 'div#article-contents > ol > li'
  sentences = []
  for sentence in sel.css(css_path).extract():
    sentence = remove_tags(sentence)
    sentence = sentence.replace('\n', '').strip().split('.')
    sentence = [string for string in sentence if string != ""]
    sentences.append(sentence)

  return [item.strip() for sublist in sentences for item in sublist]


def predict_tutorials_from_url(url):
  sentences = get_sentences_from_url(url)
  sequences_predict = tokenizer.texts_to_sequences(sentences)
  padded = pad_sequences(sequences_predict, maxlen=constants.MAX_LENGTH, padding=constants.PADDING_TYPE, truncating=constants.TRUNC_TYPE)

  predicted = model_loaded.predict(padded)

  result = pd.DataFrame()
  result['sentences'] = sentences
  result['predicted'] = predicted

  return result[result['predicted'] > 0.5]['sentences'].to_list()

print(predict_tutorials_from_url(constants.URL_TEST))