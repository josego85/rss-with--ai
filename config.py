# RSS Feed Configuration
RSS_FEEDS = [
    "https://www.omgubuntu.co.uk/feed"
]

# AI Model Configuration
CLASSIFICATION_MODEL = "mrm8488/bert-mini-finetuned-age_news-classification"
SUMMARY_MODEL = "sshleifer/distilbart-cnn-12-6"

# Processing Parameters
MAX_ARTICLES = 10
RELEVANCE_THRESHOLD = 0.85
MIN_CONTENT_LENGTH = 300
MAX_CLASSIFICATION_LENGTH = 1000
MAX_SUMMARY_LENGTH = 2000
SUMMARY_MIN_LENGTH = 200
SUMMARY_MAX_LENGTH = 350

# Output Configuration
OUTPUT_DIR = "output"
DATA_DIR = "data"
FEEDBACK_FILE = "feedback.json"