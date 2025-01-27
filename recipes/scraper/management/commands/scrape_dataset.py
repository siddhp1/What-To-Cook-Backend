import json

import pandas as pd
from django.core.management.base import BaseCommand

from scraper.models import Recipe


DATA_CSV = "recipes_ingredients.csv"
DROP_COLUMNS = ["description", "ingredients_raw", "steps", "servings", "serving_size"]


def replace_invalid_json(value):
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return []


def extract_data(data_csv=DATA_CSV, drop_columns=DROP_COLUMNS):
    raw_df = pd.read_csv(data_csv)
    # raw_df.head()

    clean_df = raw_df.drop(columns=drop_columns)
    # clean_df.head()

    clean_df.drop_duplicates(subset="id", keep="first", inplace=True)

    clean_df["tags"] = clean_df["tags"].apply(replace_invalid_json)

    return clean_df


def add_to_database(df):
    records = df.to_dict("records")
    instances = [Recipe(**record) for record in records]
    Recipe.objects.bulk_create(instances)


def scrape_recipes():
    df = extract_data()
    add_to_database(df)


class Command(BaseCommand):
    help = "Runs the dataset scraping script and updates the database"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Starting scraping...")
            scrape_recipes()
            self.stdout.write(self.style.SUCCESS("Successfully scraped data and wrote to database"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
