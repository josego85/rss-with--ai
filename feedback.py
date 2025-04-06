import json
import os
from datetime import datetime
from config import DATA_DIR, FEEDBACK_FILE

class FeedbackSystem:
    def __init__(self):
        """Initialize the feedback system"""
        self.feedback_file = os.path.join(DATA_DIR, FEEDBACK_FILE)
        self._initialize_feedback()

    def _initialize_feedback(self):
        """Create necessary directories and initialize feedback data"""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            if os.path.exists(self.feedback_file):
                self._load_feedback()
            else:
                self.feedback_data = {}
                self._save_feedback()
            print(f"✅ Feedback system initialized: {self.feedback_file}")
        except Exception as e:
            print(f"⚠️ Error initializing feedback system: {e}")
            self.feedback_data = {}

    def _load_feedback(self):
        """Load existing feedback data"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                self.feedback_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading feedback data: {e}")
            self.feedback_data = {}

    def _save_feedback(self):
        """Save feedback data to file"""
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving feedback data: {e}")

    def get_relevance_adjustment(self, url):
        """Get score adjustment based on previous feedback"""
        if url in self.feedback_data:
            return 0.1 if self.feedback_data[url]['relevant'] else -0.1
        return 0

    def add_feedback(self, url, is_relevant, category='general'):
        """Add new feedback for an article"""
        self.feedback_data[url] = {
            'relevant': is_relevant,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        self._save_feedback()
        print(f"✅ Feedback saved for: {url}")