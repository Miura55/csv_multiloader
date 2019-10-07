import gensim
from pathlib import PurePath
import MeCab
from scipy import spatial
import numpy as np

model = gensim.models.KeyedVectors.load_word2vec_format('model/model.vec', binary=False)
mecab = MeCab.Tagger('-Owakati')

def avg_feature_vector(sentence, model, num_features):
    words = mecab.parse(sentence).replace(' \n', '').split() # mecabの分かち書きでは最後に改行(\n)が出力されてしまうため、除去
    feature_vec = np.zeros((num_features,), dtype="float32") # 特徴ベクトルの入れ物を初期化
    for word in words:
        if word in model.wv:
            feature_vec = np.add(feature_vec, model[word])
        else:
            pass
    if len(words) > 0:
        feature_vec = np.divide(feature_vec, len(words))
    return feature_vec

def sentence_similarity(sentence_1, sentence_2):
    num_features=300
    sentence_1_avg_vector = avg_feature_vector(sentence_1, model, num_features)
    sentence_2_avg_vector = avg_feature_vector(sentence_2, model, num_features)
    return 1 - spatial.distance.cosine(sentence_1_avg_vector, sentence_2_avg_vector)

