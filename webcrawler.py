import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

# Function to scrape text content from a webpage
def scrape_text_from_url(url):
    """Scrape all text from a webpage."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text(), soup.title.string if soup.title else "no_title"

# Function to save the scraped text to a .txt file
def save_to_txt_file(text, folder_name, filename):
    """Save text to a .txt file in a specified folder."""
    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Save the text file in the folder
    file_path = os.path.join(folder_name, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"File saved to: {file_path}")

# Function to crawl a webpage and follow all links
def crawl_and_scrape(url, folder_name, visited_urls, max_depth=3, current_depth=0):
    """Crawl a webpage, extract text, follow links, and save the content."""
    if url in visited_urls or current_depth > max_depth:
        return  # Skip already visited URLs or exceed max depth

    visited_urls.add(url)  # Mark this URL as visited

    print(f"Crawling: {url}")
    
    try:
        # Scrape the current page
        text, title = scrape_text_from_url(url)
        
        # Use the title of the webpage as the filename
        txt_file_name = f"{title.strip().replace(' ', '_')}.txt"  # Remove spaces and replace with underscores
        save_to_txt_file(text, folder_name, txt_file_name)

        # Extract links and recursively crawl them
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            next_url = link['href']
            next_url = urljoin(url, next_url)  # Resolve relative URLs
            parsed_url = urlparse(next_url)

            # Avoid non-HTTP URLs like mailto: or javascript: or the same domain
            if parsed_url.scheme in ["http", "https"]:
                time.sleep(1)  # Add delay to avoid overwhelming the server
                crawl_and_scrape(next_url, folder_name, visited_urls, max_depth, current_depth + 1)
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error accessing {url}: {e}")

# Main function to start the crawling process
def main(start_url):
    folder_name = "ambi"  # Folder to save the files
    visited_urls = set()  # Track visited URLs to avoid re-crawling

    # Start crawling from the given URL
    crawl_and_scrape(start_url, folder_name, visited_urls)

# Example usage
if __name__ == "__main__":
    start_url = input("Enter the starting URL: ").strip()
    main(start_url)
