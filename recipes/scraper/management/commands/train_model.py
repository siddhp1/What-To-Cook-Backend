from django.core.management.base import BaseCommand
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize

from scraper.models import Recipe


VECTOR_SIZE = 100
WINDOW = 5
MIN_COUNT = 1
WORKERS = 4
MODEL_PATH = "word2vec_recipe_names.model"


nltk.download("punkt_tab")


def generate_corpus():
    recipes = Recipe.objects.all().values_list("name", flat=True)

    corpus = list(recipes)

    return corpus


def train_word2vec(corpus):
    tokenized_corpus = [word_tokenize(name.lower()) for name in corpus]

    model = Word2Vec(
        sentences=tokenized_corpus,
        vector_size=VECTOR_SIZE,
        window=WINDOW,
        min_count=MIN_COUNT,
        workers=WORKERS,
    )

    return model


class Command(BaseCommand):
    help = "Train NLP model"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Starting training...")

            corpus = generate_corpus()

            model = train_word2vec(corpus)
            model.save(MODEL_PATH)

            self.stdout.write("Successfully trained model")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
