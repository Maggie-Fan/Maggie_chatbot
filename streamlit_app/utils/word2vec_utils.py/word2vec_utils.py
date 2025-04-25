# utils/word2vec_utils.py

from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from sklearn.decomposition import PCA
import numpy as np



# 預設句子，可自訂
DEFAULT_SENTENCES = [
    "Fifteen people in South Korea were injured, two of them seriously, after a pair of fighter jets accidentally dropped eight bombs in a civilian district on Thursday during a live-fire military exercise, local media reported",
    "The incident involving the Air Force KF-16 aircraft, in the city of Pocheon near North Korea, was part of routine drills held by the South to maintain combat readiness against potential attacks from the North",
    "South Korea's Air Force said that it was investigating the incident and apologised for the damage, adding it would provide compensation to those affected",
    "While shells from live firing exercises sometimes land near civilian residences, they rarely cause injuries",
    "According to local media reports, two people suffered fractures to their necks and shoulders",
    "The military said the pilot of one of the jets inputted the wrong coordinates by mistake, causing the bombs to drop in the civilian community",
    "Investigators have yet to determine why the second jet dropped its bombs, the military said, adding all live-fire exercises will be suspended",
    "One church building and houses were also damaged as a result of the incident",
    "South Korea and the US are set to run combined drills from March 10 to March 20 - the first since US president Donald Trump's return to the White House",
    "This comes at a time when the two countries are increasingly wary of the growing alliance between North Korea and Russia",
]

def train_word2vec(sentences=None, vector_size=100, window=5, min_count=1):
    if sentences is None:
        sentences = DEFAULT_SENTENCES
    tokenized_sentences = [simple_preprocess(s) for s in sentences]
    model = Word2Vec(tokenized_sentences, vector_size=vector_size, window=window, min_count=min_count)
    return model, tokenized_sentences

def reduce_dimensions(model, n_components=2):
    word_vectors = np.array([model.wv[word] for word in model.wv.index_to_key])
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(word_vectors)
    return reduced
