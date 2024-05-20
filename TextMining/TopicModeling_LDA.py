import os, re, io
from nltk.tokenize import RegexpTokenizer
#from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import gensim
from gensim import corpora, models
import itertools
tokenizer = RegexpTokenizer(r'\w+')
from nltk.tokenize import word_tokenize
from gensim.corpora import Dictionary

docs=[]
# Folder containing all papers.
cwd = os.getcwd()
dataset_dir = cwd + "/LDADataset"
docs = []

docindex_author_dict={}

files=os.listdir(dataset_dir)#List of filenames.
for file in files:
    with io.open(dataset_dir + '/' + file, errors='ignore', encoding='utf-8') as fid:
        doc=fid.read()
        doc=doc.strip()
        if doc!="":
            index=len(docs)
            docs.append(doc)
            author=str(file).replace(".txt", "")
            docindex_author_dict.update({index:author})

print(docindex_author_dict)
#tokenize doc
tokenize_docs = []
for doc in docs:
    # tokenize document string
    tokens = tokenizer.tokenize(doc)
    tokens_list = [i for i in tokens]
    tokenize_docs.append(tokens_list)

docs = tokenize_docs
del tokenize_docs

dictionary = Dictionary(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]

Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(corpus, num_topics=59, id2word = dictionary, passes=50, minimum_probability=0.0)

author_topics_dict={}
for index, doc in enumerate(corpus):
    author_id=str(docindex_author_dict[index])
    doc_td=ldamodel.get_document_topics(doc)
    temp=[]
    for t in doc_td:
        temp.append(float(t[1]))
    author_topics_dict.update({author_id:temp})

import json
with open('Author_Topics_Distribution_LDA.json', 'w', encoding='utf8') as fout:
    json.dump(author_topics_dict, fout)

