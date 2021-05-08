import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# get_ipython().run_line_magic('matplotlib', 'inline')
import tensorflow as tf
import cufflinks as cf
import pandas as pd  # for handling csv and csv contents
from sklearn.feature_selection import VarianceThreshold

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
from sklearn.feature_extraction.text import CountVectorizer
import io
import time
from io import StringIO
import re
from nltk.corpus import stopwords
from PIL import *
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from ipywidgets import FileUpload
from IPython.display import display
import nltk
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import yake
import csv


def function1(data_file):
  nltk.download('stopwords')
  # upload = FileUpload(accept='.csv', multiple=True)
  # display(upload)
  global df1
  df1 = pd.read_csv(data_file)
  df1.head(10)
  df1.drop(['Date', 'Link'], axis=1, inplace=True)
  df1.info()
  df1['label'] = 'conjunctivitis'
  df1.head()
  df1 = df1.reset_index(drop=True)
  global REPLACE_BY_SPACE_RE
  REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|,;]')
  global BAD_SYMBOLS_RE
  BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
  global STOPWORDS
  STOPWORDS = set(stopwords.words('english'))
  return "function 1"


def clean_text(text):
  """
        text: a string

        return: modified initial string
    """
  text = text.lower()  # lowercase text
  text = REPLACE_BY_SPACE_RE.sub(' ',
                                 text)  # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
  text = BAD_SYMBOLS_RE.sub('',
                            text)  # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
  # text = re.sub(r'\W+', '', text)
  text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # remove stopwors from text
  return text


def function2():
  df1['Country'] = df1['Country'].apply(clean_text)
  df1['Country'] = df1['Country'].str.replace('\d+', ' ', regex=True)

  df1.head(5)
  global nlp
  nlp = en_core_web_sm.load()
  nlp = spacy.load('en_core_web_sm')


class TextRank4Keyword():
  """Extract keywords from text"""

  def __init__(self):
    self.d = 0.85  # damping coefficient, usually is .85
    self.min_diff = 1e-5  # convergence threshold
    self.steps = 10  # iteration steps
    self.node_weight = None  # save keywords and its weight

  def set_stopwords(self, stopwords):
    """Set stop words"""
    for word in STOP_WORDS.union(set(stopwords)):
      lexeme = nlp.vocab[word]
      lexeme.is_stop = True

  def sentence_segment(self, doc, candidate_pos, lower):
    """Store those words only in cadidate_pos"""
    sentences = []
    for sent in doc.sents:
      selected_words = []
      for token in sent:
        # Store words only with cadidate POS tag
        if token.pos_ in candidate_pos and token.is_stop is False:
          if lower is True:
            selected_words.append(token.text.lower())
          else:
            selected_words.append(token.text)
      sentences.append(selected_words)
    return sentences

  def get_vocab(self, sentences):
    """Get all tokens"""
    vocab = OrderedDict()
    i = 0
    for sentence in sentences:
      for word in sentence:
        if word not in vocab:
          vocab[word] = i
          i += 1
    return vocab

  def get_token_pairs(self, window_size, sentences):
    """Build token_pairs from windows in sentences"""
    token_pairs = list()
    for sentence in sentences:
      for i, word in enumerate(sentence):
        for j in range(i + 1, i + window_size):
          if j >= len(sentence):
            break
          pair = (word, sentence[j])
          if pair not in token_pairs:
            token_pairs.append(pair)
    return token_pairs

  def symmetrize(self, a):
    return a + a.T - np.diag(a.diagonal())

  def get_matrix(self, vocab, token_pairs):
    """Get normalized matrix"""
    # Build matrix
    vocab_size = len(vocab)
    g = np.zeros((vocab_size, vocab_size), dtype='float')
    for word1, word2 in token_pairs:
      i, j = vocab[word1], vocab[word2]
      g[i][j] = 1

    # Get Symmeric matrix
    g = self.symmetrize(g)

    # Normalize matrix by column
    norm = np.sum(g, axis=0)
    g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

    return g_norm

  def get_keywords(self, number=10):
    """Print top number keywords"""
    node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
    for i, (key, value) in enumerate(node_weight.items()):
      print(key + ' - ' + str(value))
      if i > number:
        break

  def analyze(self, text,
              candidate_pos=['NOUN', 'PROPN'],
              window_size=4, lower=False, stopwords=list()):
    """Main function to analyze text"""

    # Set stop words
    self.set_stopwords(stopwords)

    # Pare text by spaCy
    doc = nlp(text)

    # Filter sentences
    sentences = self.sentence_segment(doc, candidate_pos, lower)  # list of list of words

    # Build vocabulary
    vocab = self.get_vocab(sentences)

    # Get token_pairs from windows
    token_pairs = self.get_token_pairs(window_size, sentences)

    # Get normalized matrix
    g = self.get_matrix(vocab, token_pairs)

    # Initionlization for weight(pagerank value)
    pr = np.array([1] * len(vocab))

    # Iteration
    previous_pr = 0
    for epoch in range(self.steps):
      pr = (1 - self.d) + self.d * np.dot(g, pr)
      if abs(previous_pr - sum(pr)) < self.min_diff:
        break
      else:
        previous_pr = sum(pr)

    # Get weight for each node
    node_weight = dict()
    for word, index in vocab.items():
      node_weight[word] = pr[index]

    self.node_weight = node_weight


def function3():
  docs = df1.Country.values.tolist()
  str1 = ''.join(docs)

  text = str1
  tr4w = TextRank4Keyword()
  tr4w.analyze(text, window_size=4, lower=False)
  tr4w.get_keywords()
  # get_ipython().system('pip install yake')
  text = str1
  simple_kwextractor = yake.KeywordExtractor()
  keywords = simple_kwextractor.extract_keywords(text)

  # df1 = pd.DataFrame(data=keywords, index=["Country", "poids"]).transpose()

  for kw in keywords:
    print(kw)

  # specifying parameters
  max_ngram_size = 1
  custom_kwextractor = yake.KeywordExtractor(lan="en", n=max_ngram_size, dedupLim=0.9, dedupFunc='seqm', windowsSize=1,
                                             features=None)

  keywords = custom_kwextractor.extract_keywords(text)

  for kw in keywords:
    print(kw)

  with open('C:\dataset\output.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(('Country', 'Poids'))
    for row in keywords:
      csvwriter.writerow(row)
