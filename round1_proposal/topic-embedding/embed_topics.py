########################################################################
# Topic Embedding

import pickle
import numpy as np
import gensim
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True,limit=500000)

title_word_dict = pickle.load( open( "./title_word_freq.p", "rb" ))

title_word_dict_sorted = sorted(title_word_dict.items(), key=lambda kv: kv[1])
title_word_dict_sorted = title_word_dict_sorted[-500:]

words     = [ el[0] for el in title_word_dict_sorted if el[0] in model.vocab ]
word_vecs = [ model[el[0]] for el in title_word_dict_sorted if el[0] in model.vocab ]
word_vecs = np.array(word_vecs)

from sklearn.manifold import TSNE
tsne = TSNE(n_components = 2, init = 'random', perplexity = 30)
tsne_fit = tsne.fit_transform(word_vecs)

import matplotlib.pyplot as plt
#plt.figure()
#plt.scatter(tsne_fit[:,0],tsne_fit[:,1])
#plt.show()

#from sklearn.cluster import KMeans
#random_state = 17
#y_pred = KMeans(n_clusters=2, random_state=random_state).fit_predict(tsne_fit)

from sklearn import mixture
gmm = mixture.GaussianMixture(n_components=2, covariance_type='full').fit(tsne_fit)
gmm_pred = gmm.predict(tsne_fit)
wordsnp = np.array(words)
words_labels = np.transpose(np.vstack((wordsnp,gmm_pred)))
#print(words_labels[words_labels[:,1].argsort()])

interesting_labels0 = ['border','ban','security','immigration','military','water','legal','marijuana','budget','tax', 'white', 'black', 'shutdown', 'gun', 'trade', 'shooting', 'protest', 'sanctions', 'energy', 'gay', 'killing', 'shot', 'scandal', 'spending', 'trump', 'abortion', 'murder', 'twitter', 'prison', 'facebook', 'jobs', 'oil', 'bank']

interesting_labels1 = ['elections','gop','lawmakers','democrats','secretary','russia','obama','clinton','eu','senators', 'presidential','washington','korea','israel','iran','china']

interesting_labels = interesting_labels0 + interesting_labels1
label_locations = [words.index(label) for label in interesting_labels]
   

#plt.scatter(tsne_fit[:,0],tsne_fit[:,1], c=gmm_pred)
#plt.show()

fig, ax = plt.subplots()
ax.scatter(tsne_fit[:,0],tsne_fit[:,1],c=gmm_pred)
for i, txt in enumerate(interesting_labels):
    pos = label_locations[i]
    ax.annotate(txt, (tsne_fit[pos,0],tsne_fit[pos,1]))
#plt.show()

DIR = '/Users/jvenderley/Documents/coding/muckrack/analyze_titles/'
plt.savefig(DIR + 'topic_embedding.svg')
plt.savefig(DIR + 'topic_embedding.pdf')
