import time

from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.models import Recipe


BASE_URL = "https://www.food.com/recipe/all/newest"
MAX_PAGES = 10


# Create logging worker
# Add warning suppresion


def setup_driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    return driver


def click_load_more(driver):
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "gk-aa-load-more"))
        )
        load_more_button.click()
        return True
    except Exception as e:
        print(f"Error clicking LOAD MORE button: {e}")
        return False


def collect_recipe_urls(driver):
    recipe_urls = set()
    try:
        for _ in range(MAX_PAGES):
            tile_stream = driver.find_element(By.CLASS_NAME, "fdStream")
            tiles = tile_stream.find_elements(By.CLASS_NAME, "fd-tile")

            for tile in tiles:
                url = tile.get_attribute("data-url")
                if url not in recipe_urls and url is not None:
                    recipe_urls.add(url)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            new_tiles = tile_stream.find_elements(By.CLASS_NAME, "fd-tile")
            if len(new_tiles) == len(tiles):
                break
    except Exception as e:
        print(f"Error finding tile stream or tiles: {e}")
    return recipe_urls


def scrape_recipe_details(driver, url):
    try:
        driver.get(url)
        recipe_id = url.split("-")[-1]

        recipe_name = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
            .text
        )

        recipe_ingredients = []
        ingredient_list = driver.find_element(By.CLASS_NAME, "ingredient-list")
        ingredients = ingredient_list.find_elements(By.XPATH, ".//li")

        for ingredient in ingredients:
            try:
                ingredient_text = ingredient.find_element(By.XPATH, ".//a").text
            except:
                continue
            if ingredient_list:
                recipe_ingredients.append(ingredient_text)
        return {
            "id": recipe_id,
            "name": recipe_name,
            "ingredients": recipe_ingredients,
            "tags": [],  # Add tags later with NLP
        }
    except Exception as e:
        print(f"Error scraping recipe at {url}: {e}")
        return None


def add_to_database(recipe_data):
    if recipe_data is None:
        return False

    try:
        Recipe.objects.get_or_create(
            id=recipe_data["id"],
            defaults={
                "name": recipe_data["name"],
                "ingredients": recipe_data["ingredients"],
                "tags": recipe_data["tags"],
            },
        )
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False


def scrape_recipes():
    driver = setup_driver()
    try:
        if not click_load_more(driver):
            return False

        recipe_urls = collect_recipe_urls(driver)

        for url in recipe_urls:
            recipe_data = scrape_recipe_details(driver, url)
            if recipe_data:
                add_to_database(recipe_data)

        return True
    finally:
        driver.quit()


class Command(BaseCommand):
    help = "Runs the website scraping script and updates the database"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Starting scraping...")
            success = scrape_recipes()
            if success:
                self.stdout.write(
                    self.style.SUCCESS("Successfully scraped data and wrote to database")
                )
            else:
                self.stdout.write(self.style.WARNING("Scraping completed with some errors"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
