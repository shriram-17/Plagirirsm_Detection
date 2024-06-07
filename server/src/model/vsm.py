import os
import json
import numpy as np
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient

load_dotenv()

def load_json_file(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
    return None

def calculate_tf_idf_matrix(articles_data):
    descriptions = []
    article_ids = []
    for article_id, article_data in articles_data.items():
        if 'description' in article_data and article_data['description']:
            descriptions.append(' '.join(article_data['description']))
            article_ids.append(article_id)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)
    
    return tfidf_matrix, tfidf_vectorizer, article_ids

def store_matrix_in_mongodb(json_path, connection_string, database_name, collection_name):
    articles_data = load_json_file(json_path)

    if articles_data:
        tfidf_matrix, tfidf_vectorizer, article_ids = calculate_tf_idf_matrix(articles_data)

        data_to_insert = []
        terms = tfidf_vectorizer.get_feature_names_out()
        for i, term in enumerate(terms):
            non_zero_indices = tfidf_matrix[:, i].nonzero()[1]
            non_zero_values = tfidf_matrix[:, i].data.tolist()

            term_data = {
                'term': term,
                'tf_idf_indices': non_zero_indices.tolist(),
                'tf_idf_values': non_zero_values
            }
            data_to_insert.append(term_data)

        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]

        result = collection.insert_many(data_to_insert)
        print("Data inserted successfully.")
    else:
        print("Failed to read JSON file or JSON file is empty.")


json_path = 'C:\\Users\\shrir\\OneDrive\\Documents\\Repositories\\Plagirirsm_Detection\\server\\src\\data\\modified_mises_articles.json'
connection_string = os.environ.get("MONGO_ENV")
database_name = os.environ.get("database_name")
collection_name = os.environ.get("collection_name")

store_matrix_in_mongodb(json_path, connection_string, database_name, collection_name)
