from bs4 import BeautifulSoup

html_content = """
<div class="content-col">
        <!-- Your HTML content here -->
</div>
"""

soup = BeautifulSoup(html_content, 'html.parser')

# Extracting prices and dates
prices = soup.find_all('div', class_='price')
dates = soup.find_all('div', class_='date')

for price, date in zip(prices, dates):
        print(f"Price: {price.text.strip()}, Date: {date.text.strip()}")
        # Extracting prices and dates from specific wrapper
        station_details = soup.find_all('div', class_='station-detail-wrapper pb text-center')

        for detail in station_details:
                price = detail.find('div', class_='price')
                date = detail.find('div', class_='date')
                if price and date:
                        print(f"Price: {price.text.strip()}, Date: {date.text.strip()}")