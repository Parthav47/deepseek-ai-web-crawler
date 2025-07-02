import csv
from urllib.parse import urlparse

from models.venue import Venue


def is_duplicate_venue(venue_name: str, seen_names: set) -> bool:
    return venue_name in seen_names


def is_complete_venue(venue: dict, required_keys: list) -> bool:
    return all(key in venue for key in required_keys)


def save_venues_to_csv(venues: list, filename: str):
    if not venues:
        print("No venues to save.")
        return

    # Use field names from the Venue model
    fieldnames = Venue.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    print(f"Saved {len(venues)} venues to '{filename}'.")


def extract_website_name(url: str) -> str:
    """
    Extract website name from URL.
    Examples:
    - "https://www.flipkart.com/search" -> "flipkart"
    - "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets" -> "webscraper"
    - "https://www.theknot.com/marketplace/wedding-reception-venues-atlanta-ga" -> "theknot"
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove common prefixes
    domain = domain.replace('www.', '')
    
    # Extract the main domain name (before the first dot)
    website_name = domain.split('.')[0]
    
    return website_name


def generate_csv_filename(base_url: str, prefix: str = "") -> str:
    """
    Generate a CSV filename based on the website name.
    
    Args:
        base_url: The URL being scraped
        prefix: Optional prefix for the filename
    
    Returns:
        A filename like "flipkart_scraped.csv" or "webscraper_scraped.csv"
    """
    website_name = extract_website_name(base_url)
    filename = f"{website_name}_scraped.csv"
    
    if prefix:
        filename = f"{prefix}_{filename}"
    
    return filename
