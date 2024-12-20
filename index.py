import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
from collections import deque
import time

class WebCrawler:
    def __init__(self, start_url, output_file):
        self.start_url = start_url if start_url.endswith('/') else f"{start_url}/"
        self.output_file = output_file
        self.domain = urlparse(self.start_url).netloc
        self.visited = set()
        self.queue = deque([self.start_url])
        
        # Create/open CSV file with status_code column
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Status_Code'])
    
    def is_valid_url(self, url):
        """Check if URL belongs to the same domain and is a web URL"""
        web_schemes = {'http', 'https'}
        
        parsed = urlparse(url)
        
        if parsed.scheme not in web_schemes:
            return False
            
        return parsed.netloc == self.domain or not parsed.netloc
    
    def get_links(self, url, response):
        """Extract all links from a webpage"""
        try:
            if response.status_code < 300:  # Only parse content for successful responses
                soup = BeautifulSoup(response.text, 'html.parser')
                links = set()
                
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        absolute_url = urljoin(url, href)
                        
                        if self.is_valid_url(absolute_url):
                            cleaned_url = absolute_url.split('#')[0].split('?')[0]
                            links.add(cleaned_url)
                
                return links
            return set()
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return set()
    
    def save_url(self, url, status_code=None):
        """Save URL and status code to CSV file"""
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if status_code and status_code >= 300:
                writer.writerow([url, status_code])
            else:
                writer.writerow([url, ''])
    
    def crawl(self):
        """Main crawling method"""
        print(f"Starting crawl of {self.start_url}")
        
        while self.queue:
            current_url = self.queue.popleft()
            
            if current_url in self.visited:
                continue
                
            print(f"Processing: {current_url}")
            self.visited.add(current_url)
            
            try:
                # Get the response and status code
                response = requests.get(current_url, timeout=10)
                status_code = response.status_code
                
                # Save URL with status code only if >= 300
                self.save_url(current_url, status_code)
                
                # Only process links if it's a successful response
                new_links = self.get_links(current_url, response)
                
                # Add new links to queue
                for link in new_links:
                    if link not in self.visited:
                        self.queue.append(link)
                
            except requests.RequestException as e:
                print(f"Error accessing {current_url}: {str(e)}")
                # Save failed requests with status code 0
                self.save_url(current_url, 0)
            
            # Be nice to the server
            time.sleep(1)
        
        print(f"Crawl complete! Found {len(self.visited)} URLs")

def main():
    # Get input from user
    start_url = input("Enter the website URL to crawl: ")
    output_file = input("Enter the output CSV filename (e.g., links.csv): ")
    
    # Create and run crawler
    crawler = WebCrawler(start_url, output_file)
    crawler.crawl()

if __name__ == "__main__":
    main()