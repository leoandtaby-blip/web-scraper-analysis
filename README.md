# Web Scraper + Data Analysis Project

A practical web scraping and data analysis project that demonstrates full-stack data engineering skills.

## Overview

This project scrapes book data from [books.toscrape.com](http://books.toscrape.com), cleans it, and performs comprehensive analysis. It's designed to showcase:
- Web scraping with BeautifulSoup
- Data processing with Pandas
- Data pipeline automation
- CSV data handling

## Features

✓ Scrapes multiple pages of book data
✓ Extracts title, price, availability, and rating
✓ Saves data to timestamped CSV files
✓ Analyzes price distribution, ratings, and availability
✓ Generates detailed analysis reports

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd web-scraper-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the scraper:
```bash
python scraper.py
```

### Run the analysis:
```bash
python analysis.py
```

## Project Structure

```
web-scraper-analysis/
├── scraper.py
├── analysis.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
```

## Technologies Used

- BeautifulSoup4
- Requests
- Pandas
- NumPy
