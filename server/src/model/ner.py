import spacy
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")

load_dotenv()

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
    for index,articles in enumerate(articles_data):
        if 'description' in articles and articles['description']:
                descriptions.append((index, articles['description']))
    return descriptions

json_path = 'C:\\Users\\shrir\\OneDrive\\Documents\\Repositories\\Plagirirsm_Detection\\server\\src\\data\\mises_articles.json'

X = get_descriptions(json_path)

collection = get_collection()
for article_id, description in X:
    doc = nlp(description)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    for entity, label in entities:
        collection.insert_one({
            'article_id': article_id,
            'entity': entity,
            'label': label
        })

