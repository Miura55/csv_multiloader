import gensim
from pathlib import PurePath

model = gensim.models.KeyedVectors.load_word2vec_format('model/model.vec', binary=False)
print(model.wv.similarity('タイヤ', 'タイヤ 修復'))
