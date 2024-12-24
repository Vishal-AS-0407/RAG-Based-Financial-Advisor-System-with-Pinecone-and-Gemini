import os
import requests
from bs4 import BeautifulSoup
import PyPDF2


def download_pdf(url, filename):
    """Download a PDF from the given URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading PDF from {url}: {e}")
        return None
    return filename


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return None
    return text


def scrape_text_from_url(url):
    """Scrape all text from a webpage."""
    text = ""
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
    except requests.RequestException as e:
        print(f"Error scraping website {url}: {e}")
        return None
    return text


def save_to_txt_file(text, folder_name, filename):
    """Save text to a .txt file in a specified folder."""
    if text:
        # Ensure the folder exists
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save the text file in the folder
        file_path = os.path.join(folder_name, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"File saved to: {file_path}")
    else:
        print(f"Skipping saving {filename} as no text was extracted.")


def process_websites(input_file, folder_name="ambi"):
    """Process each URL in the input file and save the scraped content."""
    try:
        with open(input_file, 'r') as file:
            urls = file.readlines()
        
        for idx, url in enumerate(urls, 1):
            url = url.strip()
            if url:
                print(f"Processing: {url}")
                text = ""
                # Handle PDF or Website
                if url.endswith('.pdf'):
                    # Handle PDF link
                    pdf_path = "temp.pdf"
                    downloaded_pdf = download_pdf(url, pdf_path)
                    if downloaded_pdf:
                        text = extract_text_from_pdf(pdf_path)
                        os.remove(pdf_path)  # Clean up temp file
                else:
                    # Handle website link
                    text = scrape_text_from_url(url)

                # Only save if text was successfully extracted
                if text:
                    txt_file_name = f"websites{idx}.txt"
                    save_to_txt_file(text, folder_name, txt_file_name)
                else:
                    print(f"Skipping URL {url} due to extraction failure.")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    input_file = "websites2.txt"  # File containing the list of URLs
    process_websites(input_file)
