import os
from scraper import WebScraper
from vector_db import VectorDatabase
from chatbot import ChatBot
import sys

class CLIInterface:
    def __init__(self):
        self.scraper = WebScraper()
        self.vector_db = VectorDatabase()
        self.chatbot = ChatBot()
        self.current_url = None

    def run(self):
        print("=== Web Scraper Chatbot ===")
        self.handle_scraping()
        self.handle_chat()

    def handle_scraping(self):
        url = input("Enter website URL to scrape: ").strip()
        print(f"Scraping {url}...")
        
        result = self.scraper.scrape_url(url)
        if not result or not result['content']:
            print("Failed to scrape website")
            sys.exit(1)
            
        self.current_url = result['url']
        chunks_count = self.vector_db.process_and_store(result)
        print(f"Scraped content processed into {chunks_count} chunks")

    def handle_chat(self):
        print("\nChat with the bot (type 'exit' to quit)")
        while True:
            query = input("\nYou: ").strip()
            if query.lower() == 'exit':
                break
                
            context = self.vector_db.search(query)
            response = self.chatbot.generate_response(query, context, self.current_url)
            print(f"\nBot: {response}")

if __name__ == "__main__":
    CLIInterface().run()