import requests
import os
import logging
import time
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ✅ Load environment variables
load_dotenv()
FLIC_TOKEN = os.getenv("FLIC_TOKEN")

# ✅ Validate environment variable
if not FLIC_TOKEN:
    raise ValueError("❌ Missing FLIC_TOKEN in environment variables")

# ✅ API Configuration
HEADERS = {"Flic-Token": FLIC_TOKEN}
BASE_URL = "https://api.socialverseapp.com"

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Set up retry mechanism for API requests
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

def fetch_data(endpoint):
    """
    Fetch data from the given API endpoint with proper error handling and retries.
    """
    url = f"{BASE_URL}{endpoint}"
    
    try:
        start_time = time.time()  # Track response time
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an error for HTTP failure codes (4xx, 5xx)
        elapsed_time = time.time() - start_time

        # ✅ Log response time
        logging.info(f"✅ API Call: {url} | Status: {response.status_code} | Time: {elapsed_time:.2f}s")

        # ✅ Validate response structure
        data = response.json()
        if not isinstance(data, dict) or 'posts' not in data:
            logging.warning(f"⚠️ Unexpected API response format for {endpoint}")
            return []

        return data.get('posts', [])

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Failed to fetch data from {endpoint}: {e}")
        return []  # Return an empty list in case of failure

from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

def get_ai_recommendations():
    return ["AI Video 1", "AI Video 2", "AI Video 3"]  # Placeholder


def get_viewed_posts():
    return fetch_data("/posts/view?page=1&page_size=1000")

def get_liked_posts():
    return fetch_data("/posts/like?page=1&page_size=1000")

def get_inspired_posts():
    return fetch_data("/posts/inspire?page=1&page_size=1000")

def get_rated_posts():
    return fetch_data("/posts/rating?page=1&page_size=1000")

# ✅ Test API Calls (Optional)
if __name__ == "__main__":
    print("\n🚀 Testing API calls...")
    print("\n🔹 Viewed Posts:", get_viewed_posts()[:2])  # Display first 2 posts
    print("\n🔹 Liked Posts:", get_liked_posts()[:2])
    print("\n🔹 Inspired Posts:", get_inspired_posts()[:2])
    print("\n🔹 Rated Posts:", get_rated_posts()[:2])

def get_ai_recommendations():
    return [
        {"id": 1, "title": "AI-Recommended Video 1", "video_url": "https://example.com/video1.mp4"},
        {"id": 2, "title": "AI-Recommended Video 2", "video_url": "https://example.com/video2.mp4"},
        {"id": 3, "title": "AI-Recommended Video 3", "video_url": "https://example.com/video3.mp4"},
    ]
