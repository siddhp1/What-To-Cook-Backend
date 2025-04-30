# What To Cook Backend

Backend for What To Cook.

Built with Django and Python, the backend is hosted on Azure App Service with CI/CD powered by GitHub Actions. It uses Azure Blob Storage for static/media files, Azure PostgreSQL for the database, and includes a Dockerized Selenium web scraping microservice. Recipe recommendations are generated using NLTK and Scikit-Learn's linear kernel.

## About

The backend handles user authentication, stores user dish data (including images), and generates recipe recommendations. It identifies ingredients from user dishes by comparing them to similar dishes in the database, which is populated daily by a web scraper service from Recipes.com. Based on these ingredients, it recommends new recipes from the database.

## Usage

To use What To Cook, follow the instructions in the main repository [here](https://github.com/siddhp1/What-To-Cook).

## License

This project is licensed under the MIT License.
