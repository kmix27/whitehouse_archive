import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim import corpora, models, similarities, matutils
import nltk


stopwords = nltk.corpus.stopwords.words('english')
for i in ['Mr', 'mr','Gibbs','gibbs', 'robert gibbs','applause','america','president']:
    stopwords.extend(i)


with open("extraction_warc1/extraction_warc1_corpusf.json") as docs:
    crp = json.load(docs)


files = []
    for k in crp.keys():
        files.append(crp['{}'.format(k)]['text'])

files = files[:500]


titles = []
for k in crp.keys():
    titles.append(crp['{}'.format(k)]['title'])

titles = titles[:500]


count_vectorizer  = CountVectorizer(ngram_range=(1,2), stop_words=stopwords,token_pattern='\\b[a-z][a-z]+\\b',max_features=10000)
count_vectorizer.fit(content)
counts = count_vectorizer.transform(content).transpose()


tfidf = TfidfVectorizer(ngram_range=(1,2),stop_words=stopwords,token_pattern='\\b[a-z][a-z]+\\b',max_features=10000)
tfidf.fit(content)
tcounts = tfidf.transform(content).transpose()


corpus = matutils.Sparse2Corpus(counts)
id2word = dict((v,k) for k,v in count_vectorizer.vocabulary_.items())
lda = models.LdaModel(corpus=corpus,num_topics=10, id2word=id2word,passes=10)
lda_corpus = lda[corpus]


lda_docs = [doc for doc in lda_corpus]
topics = lda.show_topics(formatted=False)


word_list = []
proba_list = []
for i in topics:
    for tup in i[1]:
        proba = tup[1]
        word = tup[0]
        word_list.append(word)
        proba_list.append(proba)
