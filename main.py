import requests
import json
from bs4 import BeautifulSoup
import re
import csv

url = "https://www.shell.com/news-and-insights/newsroom/news-and-media-releases.model.json"

payload = ""
headers = {
    "cookie": "ApplicationGatewayAffinityCORS=6599aae92075c8e9c9b9e476d724b646; ApplicationGatewayAffinity=6599aae92075c8e9c9b9e476d724b646",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "Referer": "https://www.shell.com/news-and-insights/newsroom/news-and-media-releases.html",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"'
}

response = requests.request("GET", url, data=payload, headers=headers)

# Print response in JSON format
response_json = response.json()



# Open CSV file for writing (overwrite mode)
with open("shell-news-scraper1.csv", mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header
    csv_writer.writerow(['date', 'header', 'link'])

    # Function to recursively extract data with a limit
    def extract_data(item, limit, skip_count=0):
        if 'children' in item:
            for child in item['children']:
                limit, skip_count = extract_data(child, limit, skip_count)
        elif 'model' in item:
            if skip_count < 11:
                skip_count += 1
            else:
                if limit > 0:
                    model = item['model']
                    title = model.get('title', 'N/A')
                    text_html = model.get('text', 'N/A')
                    link = model.get('links', [{}])[0].get('value', 'N/A')

                    # Convert HTML to text
                    text = BeautifulSoup(text_html, 'html.parser').get_text(strip=True)

                    # Use regular expression to extract date from text
                    date_match = re.match(r'(\w+ \d{1,2}, \d{4})', text)
                    if date_match:
                        date = date_match.group(1)
                    else:
                        date = 'Date not found'
                    # date = f'"{date}"'

                    # Skip if any value is 'N/A'
                    if title != 'N/A' and text != 'N/A' and link != 'N/A':
                        # Write row to CSV
                        csv_writer.writerow([date, title, link])
                        limit -= 1
                else:
                    return limit, skip_count
        return limit, skip_count

    # Extract data, processing only the first 20 valid entries
    remaining_limit, _ = extract_data(response_json, 20)

print("successfully data saved to csv file")




