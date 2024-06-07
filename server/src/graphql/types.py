import strawberry
from typing import List

@strawberry.type
class SimilarityMetrics:
    cosine_similarity_tfidf: float
    fuzzy_match_ratio: float
    jaccard_similarity: float
    levenshtein_distance: float
    word2vec_similarity: float
    cbow_similarity: float
    doc2vec_similarity: float
    common_words: List[str]

@strawberry.type
class ArticleSimilarity:
    cos_sim: float
    common_words: List[str]
    jaccard_sim: float
    levenshtein_distance: float


@strawberry.type
class ArticlesResult:
    articles1: List[str]
    articles2: List[str]