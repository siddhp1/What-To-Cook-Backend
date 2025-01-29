import pathlib

import numpy as np
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk


MODEL_PATH = "../recipes/word2vec_recipe_names.model"


nltk.download('punkt_tab')
nltk.download('stopwords')

def run_model(dish_name):
    model = Word2Vec.load(MODEL_PATH)

    words = word_tokenize(dish_name.lower())

    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    word_vectors = [(word, model.wv[word]) for word in filtered_words if word in model.wv]
    sorted_words = sorted(word_vectors, key=lambda x: np.linalg.norm(x[1]), reverse=True)
    
    return [word for word, vector in sorted_words] 

# Testing
dish_name = "Peperroni Pizza"
main_words = run_model(dish_name)
print(main_words)