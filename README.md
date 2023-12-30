# Stock Market Index Data Web Scraper

This Python application uses Selenium and FastAPI to scrape stock market data from the web and serve it through a REST API.

## Features

- Retrieves Sensex and Nifty values from the web.
- Serves the scraped data through a FastAPI server.

## Requirements

- Python 3.6 or higher
- Docker
- Firefox ESR browser

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Build the Docker image using the provided Dockerfile.


## Usage

Once the server is running, you can access the following endpoints:

- `GET /`: Returns a base address message.
- `GET /sensex-value`: Returns the current Sensex value.
- `GET /nifty-value`: Returns the current Nifty value.

## Note

This application is designed to be run in a Docker container. The Dockerfile sets up a Python environment, installs Firefox ESR and geckodriver for Selenium, and starts the FastAPI server.

The application uses Selenium to interact with the web pages and scrape the data. The scraped data is then served through a FastAPI server. The server has endpoints for getting the current Sensex and Nifty values.

Please note that this application is intended for educational purposes and should not be used for commercial purposes without permission from the data providers. Always respect the terms of service of the website you are scraping. 
