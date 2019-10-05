import math
import operator
import typing


class CosineSimilarity:
    """余弦による文字列の類似度を計算する"""
    Vector = typing.List[float]

    @staticmethod
    def dot_product(vec1: Vector, vec2: Vector, sum=sum, map=map, mul=operator.mul) -> float:
        """ベクトルの内積を計算する"""
        return sum(map(operator.mul, vec1, vec2))

    @staticmethod
    def norm(vec: Vector, sum=sum, map=map, mul=operator.mul) -> float:
        """ベクトルのEuclidノルムを計算する"""
        return math.sqrt(sum(map(operator.mul, vec, vec)))

    def cosine(self, vec1: Vector, vec2: Vector) -> float:
        """ベクトルのなす角の余弦を計算する"""
        return self.dot_product(vec1, vec2) / (self.norm(vec1) * self.norm(vec2))

    def __call__(self, a: str, b: str) -> float:
        """文字列の類似度を計算する。類似度は0から1の間で1に近いほど類似度が高い。"""
        a_charset, b_charset = set(a), set(b)
        common_char_list = list(a_charset.union(b_charset))
        a_vector = [1 if c in a_charset else 0 for c in common_char_list]
        b_vector = [1 if c in b_charset else 0 for c in common_char_list]
        return self.cosine(a_vector, b_vector)
