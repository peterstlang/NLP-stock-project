import sys    
import csv

sys.path.append("C:/Users/peter/Documents/NLP-stock-project")

from keys import APIkey

# some more imports

import pprint
import requests 

# importing datetime
from datetime import datetime, timedelta, date
import time

from langdetect import detect
# bool
flag = True

# api endpoint
url = 'https://newsapi.org/v2/everything?'

# query params
query = 'microsoft'
start_date = date.today() -timedelta(days=1)
end_date = date.today()
sortBy = 'publishedAt'
api = APIkey
pagesize = 100

ms_titles = []

parameters = {
        'q': query, # query phrase
        'from': start_date,  # Start date (YYYY-MM-DD) - specify your desired date here
        'to': start_date,    # End date (YYYY-MM-DD) - specify your desired end date
        'sortBy': sortBy, # sort by publishingdate # number of articles (100 max)
        'pageSize': pagesize,
        'apiKey': api, # your own API key
    }
    
    # calling the api and getting json
response = requests.get(url, params=parameters)
response_json = response.json()
    # get articles
articles = response_json["articles"]

articles = [art for art in articles if detect(art["content"]) == "en"]
    
    # getting titles
titles_per_page = list(map(lambda x: x["title"], articles))
desc_per_page = list(map(lambda x: x["description"], articles))
source_per_page = list(map(lambda x: x["source"]["name"], articles))
published_at_per_page = list(map(lambda x: x["publishedAt"], articles))
    # extending list

# ['Title', 'Description', 'Source', 'Published At']
if __name__ == "__main__":

    data = []
    #print(len(titles_per_page))
    for title, desc, source, pub in zip(titles_per_page, desc_per_page, source_per_page, published_at_per_page):
        empty_dict = {
            "Title": title,
            "Description": desc,
            "Source": source,
            "Published At": pub
        }
        
        # Encode strings to the console's encoding before printing
        encoded_dict = {k: v.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding) 
                        if isinstance(v, str) else v for k, v in empty_dict.items()}
        
        data.append(encoded_dict)

    # Write dictionaries to the CSV file
    csv_file_path = 'data/news_headlines.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Define the header fields for the CSV file
        fieldnames = ["Title", "Description", "Source", "Published At"]
        
        # Create a CSV DictWriter object
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        csv_writer.writeheader()
        
        # Write each dictionary to the CSV file
        for row in data:
            # Encode strings to the console's encoding before writing to CSV
            encoded_row = {k: v.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding) 
                            if isinstance(v, str) else v for k, v in row.items()}
            csv_writer.writerow(encoded_row)
