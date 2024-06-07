import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

def read_file(path):
    if os.path.exists(path):
        with open(path, 'r+') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
    return None

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token.isalnum()]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens

def process_articles(json_file_path):
    article_data = read_file(json_file_path)
    if article_data is None:
        print("Failed to read the JSON file.")
        return
    
    modified_data = {}
    for index, article in enumerate(article_data):
        key = f"A{index}"
        modified_data[key] = {
            "title": article["title"],
            "tags": preprocess_text(" ".join(article["tags"])) if article["tags"] else None,
            "description": preprocess_text(article["description"]) if article["description"] else None,
            "url": article["url"]
        }

    output_file_path = 'src/file/modified_mises_articles.json'
    with open(output_file_path, 'w') as json_file:
        json.dump(modified_data, json_file, indent=4)
    
    print("Articles have been saved to", output_file_path)


json_file_path = 'C:\\Users\\shrir\\OneDrive\\Documents\\Repositories\\Plagirirsm_Detection\\server\\mises_articles.json'
process_articles(json_file_path)
