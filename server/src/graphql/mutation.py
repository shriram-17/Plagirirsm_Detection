import strawberry
from strawberry.file_uploads import Upload
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from Levenshtein import distance
import spacy
from bs4 import BeautifulSoup
import requests
from src.utils import preprocess_text, get_descriptions, get_top_k_articles_cos_sim, get_top_k_articles, \
                      get_jaccard_similarity, get_fuzzy_match_ratio, get_levenstein_distance
from .types import SimilarityMetrics, ArticleSimilarity, ArticlesResult

nlp = spacy.load('en_core_web_md')

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def process_file(info, file1: Upload, file2: Upload) -> SimilarityMetrics:
        try:
            text1 = (await file1.read()).decode('utf-8')
            text2 = (await file2.read()).decode('utf-8')

            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix1 = tfidf_vectorizer.fit_transform([text1])
            tfidf_matrix2 = tfidf_vectorizer.transform([text2])
            cos_sim = cosine_similarity(tfidf_matrix1, tfidf_matrix2)[0][0]

            fuzz_ratio = fuzz.token_sort_ratio(text1, text2) / 100

            set1 = set(text1.split())
            set2 = set(text2.split())
            common_words = list(set1 & set2)
            jaccard_sim = len(common_words) / len(set1 | set2)

            levenshtein_distance = distance(text1, text2) / 100

            doc1 = nlp(text1)
            doc2 = nlp(text2)
            word2vec_sim = doc1.similarity(doc2)

            cbow_sim = sum(token.similarity(doc2) for token in doc1 if token.has_vector) / len(doc1)

            doc1_vec = doc1.vector
            doc2_vec = doc2.vector
            doc2vec_sim = cosine_similarity([doc1_vec], [doc2_vec])[0][0]

            return SimilarityMetrics(
                cosine_similarity_tfidf=round(float(cos_sim), 2),
                fuzzy_match_ratio=fuzz_ratio,
                jaccard_similarity=round(float(jaccard_sim), 2),
                levenshtein_distance=levenshtein_distance,
                word2vec_similarity=round(float(word2vec_sim), 2),
                cbow_similarity=round(float(cbow_sim), 2),
                doc2vec_similarity=round(float(doc2vec_sim), 2),
                common_words=common_words
            )

        except Exception as e:
            raise Exception(f"An exception occurred: {str(e)}")

    @strawberry.mutation
    async def get_vsm_model(self, file1: Upload, file2: Upload, num_docs: int, metric: str) -> ArticlesResult:
        try:
            text1 = (await file1.read()).decode('utf-8')
            text2 = (await file2.read()).decode('utf-8')

            preprocessed_text1 = " ".join(preprocess_text(text1))
            preprocessed_text2 = " ".join(preprocess_text(text2))
            json_path = 'src/data/modified_mises_articles.json'
            descriptions = get_descriptions(json_path)

            if metric == "cosine":
                texts = descriptions + [preprocessed_text1, preprocessed_text2]
                vectorizer = TfidfVectorizer()
                tf_idf_matrix = vectorizer.fit_transform(texts[:-2])
                tfidf_vector1 = vectorizer.transform([preprocessed_text1])
                tfidf_vector2 = vectorizer.transform([preprocessed_text2])
                cos_sim_1 = cosine_similarity(tf_idf_matrix, tfidf_vector1)
                cos_sim_2 = cosine_similarity(tf_idf_matrix, tfidf_vector2)
                articles1 = get_top_k_articles_cos_sim(cos_sim_1, num_docs)
                articles2 = get_top_k_articles_cos_sim(cos_sim_2, num_docs)

            elif metric == "jaccard":
                descriptions_split = [description.split() for description in descriptions]
                jaccard_similarity_text1, jaccard_similarity_text2 = get_jaccard_similarity(
                    descriptions_split, preprocessed_text1, preprocessed_text2)
                articles1 = get_top_k_articles(jaccard_similarity_text1, num_docs)
                articles2 = get_top_k_articles(jaccard_similarity_text2, num_docs)

            elif metric == "fuzzy":
                fuzzy_match_1, fuzzy_match_2 = get_fuzzy_match_ratio(descriptions, preprocessed_text1, preprocessed_text2)
                articles1 = get_top_k_articles(fuzzy_match_1, num_docs)
                articles2 = get_top_k_articles(fuzzy_match_2, num_docs)

            elif metric == "leven":
                leven_dist_1, leven_dist_2 = get_levenstein_distance(descriptions, preprocessed_text1, preprocessed_text2)
                articles1 = get_top_k_articles(leven_dist_1, num_docs)
                articles2 = get_top_k_articles(leven_dist_2, num_docs)

            else:
                raise ValueError("Unsupported metric")

            return ArticlesResult(articles1=articles1, articles2=articles2)

        except Exception as e:
            raise Exception(f"An exception occurred: {str(e)}")

    @strawberry.mutation
    async def get_article_url(self, file1: Upload, url: str) -> ArticleSimilarity:
        try:
            text1 = (await file1.read()).decode('utf-8')
            preprocessed_text1 = " ".join(preprocess_text(text1))

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            extracted_text_list = [
                paragraph.text.strip()
                for paragraph in soup.find_all("p")
                for tag in paragraph.find_all(['a', 'em'])
                if tag.decompose()
            ]
            texts = " ".join(preprocess_text(" ".join(extracted_text_list)))

            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix1 = tfidf_vectorizer.fit_transform([preprocessed_text1])
            tfidf_matrix2 = tfidf_vectorizer.transform([texts])
            cos_sim = cosine_similarity(tfidf_matrix1, tfidf_matrix2)[0][0]

            set1 = set(preprocessed_text1.split())
            set2 = set(texts.split())
            common_words = list(set1 & set2)
            jaccard_sim = len(common_words) / len(set1 | set2)

            levenshtein_distance = distance(text1, preprocessed_text1) / 100

            return ArticleSimilarity(
                cos_sim=cos_sim,
                common_words=common_words,
                jaccard_sim=jaccard_sim,
                levenshtein_distance=levenshtein_distance
            )

        except Exception as e:
            raise Exception(f"An exception occurred: {str(e)}")
