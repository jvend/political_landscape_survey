########################################################################

import numpy as np
import time

from gensim import corpora, models
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore

# Set up log to external log file
import logging
logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

start = time.time()

corpus = corpora.MmCorpus('corpus.mm')

print(corpus)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[list(corpus)]

end = time.time()
print("Time:",end - start)

start = time.time()
dct = Dictionary.load("LDA_dct.dct")
lda_model_tfidf = LdaMulticore(corpus_tfidf, num_topics=50, id2word=dct, passes=8, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

lda_model_tfidf.save("LDA_model")

end = time.time()
print("Time:",end - start)

#lda_model_tfidf = LdaModel.load("LDA_model") ## Load
#for idx, topic in lda_model_tfidf.print_topics(-1):
#    print('Topic: {} Word: {}'.format(idx, topic))
