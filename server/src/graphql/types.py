import strawberry
from strawberry.file_uploads import Upload
from typing import List

@strawberry.type
class Article:
    title: str
    tags: List[str]
    description: List[str]
    url: str
    
@strawberry.type
class File:
    file_name: str
    file_data: str
    
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
    articles1: List[Article]
    articles2: List[Article]
    file1 : File
    file2 : File
