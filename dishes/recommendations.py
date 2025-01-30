import collections
import json
import random
import pathlib

from django.db.models import Q, F
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from backend.settings import BASE_DIR
from .models import Recipe, Ingredient

NUM_INGREDIENTS = 5
MODEL_PATH = pathlib.Path(BASE_DIR, "word2vec_recipe_names.model")


nltk.download("punkt_tab")
nltk.download("stopwords")


def get_keywords(dish_name):
    model = Word2Vec.load(str(MODEL_PATH))

    words = word_tokenize(dish_name.lower())

    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    word_vectors = [(word, model.wv[word]) for word in filtered_words if word in model.wv]
    sorted_words = sorted(word_vectors, key=lambda x: np.linalg.norm(x[1]), reverse=True)

    return [word for word, _ in sorted_words]


def update_ingredient_counts(user, words):
    if not words:
        return

    query = Q()
    for word in words:
        query &= Q(name__icontains=word)
    recipes = Recipe.objects.filter(query)

    ingredient_counts = collections.Counter()
    for recipe in recipes:
        ingredients = json.loads(recipe.ingredients)
        for ingredient in ingredients:
            ingredient_counts[ingredient.lower()] += 1

    for ingredient, count in ingredient_counts.items():
        ingredient_obj, created = Ingredient.objects.get_or_create(
            user=user, name=ingredient, defaults={"count": count}
        )
        if not created:
            ingredient_obj.count = F("count") + count
        ingredient_obj.save()

    return recipes


def add_ingredients(user, dish_name):
    words = get_keywords(dish_name)
    update_ingredient_counts(user, words)


def generate_recipe_recommendations(num_recommendations, num_ingredients=NUM_INGREDIENTS):
    top_ingredients = list(Ingredient.objects.order_by("-count")[:20])
    selected_ingredients = random.sample(
        top_ingredients, min(num_ingredients, len(top_ingredients))
    )
    user_doc = " ".join(ing.name.lower() for ing in selected_ingredients)

    recipes = Recipe.objects.all()
    recipe_docs = []

    for recipe in recipes:
        try:
            ingredients = json.loads(recipe.ingredients)
            recipe_docs.append(" ".join(ingredient.lower() for ingredient in ingredients))
        except json.JSONDecodeError:
            continue

    tfidf = TfidfVectorizer().fit_transform([user_doc] + recipe_docs)
    cos_sim = linear_kernel(tfidf[0:1], tfidf[1:]).flatten()

    scored_recipes = list(zip(recipes, cos_sim))
    scored_recipes.sort(key=lambda x: x[1], reverse=True)
    recommendations = [r[0] for r in scored_recipes[:num_recommendations]]

    return recommendations
