import pandas as pd
import os
from datetime import datetime

class DataAnalyzer:
    def __init__(self, csv_file=None):
        self.df = None
        self.csv_file = csv_file
        
    def load_data(self):
        """Load the latest CSV file if not specified"""
        if not self.csv_file:
            # Find the latest data file
            data_dir = 'data'
            if os.path.exists(data_dir):
                files = [f for f in os.listdir(data_dir) if f.startswith('books_')]
                if files:
                    files.sort(reverse=True)
                    self.csv_file = os.path.join(data_dir, files[0])
        
        if self.csv_file and os.path.exists(self.csv_file):
            self.df = pd.read_csv(self.csv_file)
            print(f"✓ Loaded data from {self.csv_file}")
            print(f"  Total records: {len(self.df)}")
        else:
            print("✗ No data file found. Run scraper first!")
            return False
        return True
    
    def analyze_prices(self):
        """Analyze book prices"""
        if self.df is None:
            return None
        
        # Clean price column (remove £ and convert to float)
        self.df['Price_Numeric'] = self.df['Price'].str.replace('£', '').astype(float)
        
        analysis = {
            'Average Price': f"£{self.df['Price_Numeric'].mean():.2f}",
            'Min Price': f"£{self.df['Price_Numeric'].min():.2f}",
            'Max Price': f"£{self.df['Price_Numeric'].max():.2f}",
            'Median Price': f"£{self.df['Price_Numeric'].median():.2f}",
        }
        return analysis
    
    def analyze_ratings(self):
        """Analyze book ratings"""
        if self.df is None:
            return None
        
        rating_counts = self.df['Rating'].value_counts().to_dict()
        return rating_counts
    
    def analyze_availability(self):
        """Analyze availability"""
        if self.df is None:
            return None
        
        in_stock = len(self.df[self.df['Availability'].str.contains('In stock')])
        total = len(self.df)
        
        return {
            'In Stock': in_stock,
            'Out of Stock': total - in_stock,
            'In Stock %': f"{(in_stock/total)*100:.1f}%"
        }
    
    def generate_report(self):
        """Generate a complete analysis report"""
        if not self.load_data():
            return
        
        print("\n" + "="*50)
        print("BOOK DATA ANALYSIS REPORT")
        print("="*50 + "\n")
        
        # Price Analysis
        print("📊 PRICE ANALYSIS")
        print("-" * 50)
        prices = self.analyze_prices()
        for key, value in prices.items():
            print(f"  {key}: {value}")
        
        # Rating Analysis
        print("\n⭐ RATING ANALYSIS")
        print("-" * 50)
        ratings = self.analyze_ratings()
        for rating, count in sorted(ratings.items(), reverse=True):
            print(f"  {rating} stars: {count} books")
        
        # Availability Analysis
        print("\n📦 AVAILABILITY ANALYSIS")
        print("-" * 50)
        availability = self.analyze_availability()
        for key, value in availability.items():
            print(f"  {key}: {value}")
        
        # Summary Statistics
        print("\n📈 SUMMARY STATISTICS")
        print("-" * 50)
        print(f"  Total Books: {len(self.df)}")
        print(f"  Unique Titles: {self.df['Title'].nunique()}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.generate_report()
