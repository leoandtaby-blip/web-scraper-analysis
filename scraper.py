import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

class BookScraper:
    def __init__(self, base_url="http://books.toscrape.com"):
        self.base_url = base_url
        self.books = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self, page_num=1):
        """Fetch a single page of books"""
        url = f"{self.base_url}/catalogue/page-{page_num}.html"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page {page_num}: {e}")
            return None
    
    def parse_books(self, html):
        """Parse book data from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            try:
                title = book.h2.a.get('title', 'N/A')
                price = book.find('p', class_='price_color').text.strip()
                availability = book.find('p', class_='instock availability').text.strip()
                rating_class = book.find('p', class_='star-rating').get('class')[1]
                rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                rating = rating_map.get(rating_class, 0)
                
                self.books.append({
                    'Title': title,
                    'Price': price,
                    'Availability': availability,
                    'Rating': rating
                })
            except (AttributeError, KeyError) as e:
                print(f"Error parsing book: {e}")
                continue
    
    def scrape_pages(self, num_pages=3):
        """Scrape multiple pages of books"""
        print(f"Starting to scrape {num_pages} pages...")
        for page in range(1, num_pages + 1):
            print(f"Scraping page {page}...")
            html = self.fetch_page(page)
            if html:
                self.parse_books(html)
        
        print(f"Scraped {len(self.books)} books total")
        return self.books
    
    def save_to_csv(self, directory='data'):
        """Save scraped books to timestamped CSV file"""
        if not self.books:
            print("No books to save!")
            return None
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"books_{timestamp}.csv"
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Title', 'Price', 'Availability', 'Rating']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.books)
            
            print(f"Data saved to {filepath}")
            return filepath
        except IOError as e:
            print(f"Error saving to CSV: {e}")
            return None

if __name__ == "__main__":
    scraper = BookScraper()
    scraper.scrape_pages(num_pages=3)
    scraper.save_to_csv()
