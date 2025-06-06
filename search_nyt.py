import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.environ.get("NYT_API_KEY")
API_BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

def search_articles(search_term):
    if not API_KEY:
        print("Error: NYT_API_KEY not found. Make sure it's set in your .env file.")
        return None
    params = {
        'q': search_term,
        'api-key': API_KEY
    }
    # this is based on the NYT API documentation
    # the format is: /articlesearch.json?q={query}&fq={filter}
    # an example call is: https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=yourkey
    response = requests.get(API_BASE_URL, params)
    response.raise_for_status() # Good practice to check for HTTP errors
    return response.json()

def display_results(search_results):
    #removed so now we are only printing article headlines and URLs
    #print(search_results)
    if not search_results or "response" not in search_results or "docs" not in search_results["response"]:
        print("No results found or error in API response.")
        return
    docs = search_results["response"]["docs"]
    if not docs:
        print("No articles found for your search term.")
        return

    for doc in docs:
            article_web_url = doc.get("web_url", "N/A") # Use .get for safer access
            article_headline = doc.get("headline", {}).get("main", "No Headline") # Safer access for nested dict

        print(f"{article_headline} ({article_web_url})") # Use f-string for cleaner formatting

if __name__ == "__main__":
    while True:
        search_term = input("Your search term (or type 'exit' to quit): ")
        if search_term.lower() == 'exit':
            break
        if search_results := search_articles(search_term): # Walrus operator for conciseness
            display_results(search_results)
        print("")