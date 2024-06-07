import nltk
import os
import json
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pymongo import MongoClient
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from Levenshtein import distance
import spacy
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()

nlp = spacy.load('en_core_web_md')


def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token for token in tokens]
    tokens = [token for token in tokens if token.isalnum()]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


def get_collection():
    connection_string = os.environ.get("MONGO_ENV")
    database_name = os.environ.get("database_name")
    collection_name = os.environ.get("collection_name")
    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db["Mises_Ner"]

    return collection


def load_json_file(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
    return None


def get_descriptions(path):
    articles_data = load_json_file(path)

    descriptions = []
    for article_id, article_data in articles_data.items():
        if 'description' in article_data and article_data['description']:
            descriptions.append(" ".join(article_data['description']))
    return descriptions


def get_top_k_articles_cos_sim(cos_sim, numDocs):
    cos_sim_flat = cos_sim.flatten()
    top_k_indices = np.argpartition(cos_sim_flat, -numDocs)[-numDocs:]
    json_path = 'C:\\Users\\shrir\\OneDrive\\Documents\\Repositories\\Plagirirsm_Detection\\server\\src\\data\\modified_mises_articles.json'
    data = load_json_file(json_path)
    top_k_indices = [f"A{i}" for i in top_k_indices]

    articles = []
    for article_index in data:
        if article_index in top_k_indices:
            articles.append(data[article_index])

    return articles


def get_jaccard_similarity(descriptions, preprocessed_text1, preprocessed_text2):
    jaccard_similarity_text1 = {}
    jaccard_similarity_text2 = {}

    for index, description in enumerate(descriptions):
        intersection_text1 = len(set(description).intersection(set(preprocessed_text1)))
        union_text1 = len(set(description).union(set(preprocessed_text1)))
        jaccard_similarity_text1[index] = intersection_text1 / float(union_text1)

        intersection_text2 = len(set(description).intersection(set(preprocessed_text2)))
        union_text2 = len(set(description).union(set(preprocessed_text2)))
        jaccard_similarity_text2[index] = intersection_text2 / float(union_text2)

    return jaccard_similarity_text1, jaccard_similarity_text2


def get_top_k_articles(similarity_dict, numDocs):
    sorted_keys = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
    sorted_keys = sorted_keys[:numDocs]
    print(sorted_keys)
    json_path = 'C:\\Users\\shrir\\OneDrive\\Documents\\Repositories\\Plagirirsm_Detection\\server\\src\\data\\modified_mises_articles.json'
    data = load_json_file(json_path)
    top_k_indices = [f"A{i}" for i in sorted_keys]
    articles = []
    for article_index in data:
        if article_index in top_k_indices:
            articles.append(data[article_index])
    return articles


def get_fuzzy_match_ratio(descriptions, preprocessed_text1, preprocessed_text2):
    fuzzy_match_text1 = {}
    fuzzy_match_text2 = {}

    for index, description in enumerate(descriptions):
        fuzz_ratio_1 = fuzz.token_sort_ratio(description, preprocessed_text1) / 100
        fuzzy_match_text1[index] = fuzz_ratio_1

        fuzz_ratio_2 = fuzz.token_sort_ratio(description, preprocessed_text2) / 100
        fuzzy_match_text2[index] = fuzz_ratio_2

    return fuzzy_match_text1, fuzzy_match_text2

def get_levenstein_distance(descriptions, preprocessed_text1, preprocessed_text2):

    levenstein_dist_text1 = {}
    levenstein_dist_text2 = {}

    for index, description in enumerate(descriptions):
        leven_dist_1 = distance(description, preprocessed_text1) / 100
        levenstein_dist_text1[index] = leven_dist_1

        leven_dist_2 = distance(description, preprocessed_text2) / 100
        levenstein_dist_text2[index] = leven_dist_2

    return levenstein_dist_text1,levenstein_dist_text2