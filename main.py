import feedparser
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from transformers import pipeline
from datetime import datetime
import os
import time
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

from config import (
    CLASSIFICATION_MODEL,
    SUMMARY_MODEL,
    RSS_FEEDS,
    MIN_CONTENT_LENGTH,
    MAX_CLASSIFICATION_LENGTH,
    RELEVANCE_THRESHOLD,
    MAX_SUMMARY_LENGTH,
    SUMMARY_MAX_LENGTH,
    SUMMARY_MIN_LENGTH,
    OUTPUT_DIR,
    MAX_ARTICLES,
)
from feedback import FeedbackSystem


class RSSProcessor:
    def __init__(self):
        """Initialize RSS processor with feedback system and AI models"""
        self.feedback_system = FeedbackSystem()
        self._load_ai_models()

    def _load_ai_models(self):
        """Load classification and summarization models"""
        try:
            self.classifier = pipeline(
                "text-classification", model=CLASSIFICATION_MODEL
            )
            self.summarizer = pipeline("summarization", model=SUMMARY_MODEL)
            print("✅ AI models loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading AI models: {e}")
            self.classifier = None
            self.summarizer = None

    def fetch_feed(self, url):
        """Fetch RSS feed entries from a URL"""
        try:
            return feedparser.parse(url).entries
        except Exception as e:
            print(f"⚠️ Error fetching feed {url}: {e}")
            return []

    def download_articles(self):
        """Download articles from all RSS feeds concurrently"""
        entries = []
        print(f"📥 Downloading articles from {len(RSS_FEEDS)} feeds...")
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.fetch_feed, RSS_FEEDS)
            for r in results:
                entries.extend(r)
        return entries

    def process_entry(self, entry):
        """Process a single RSS entry"""
        try:
            # Fetch and parse content
            response = requests.get(entry.link, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            content = " ".join([para.get_text() for para in paragraphs])

            if not content.strip() or len(content) < MIN_CONTENT_LENGTH:
                return None

            print(f"📝 Processing: {entry.title}")
            print(f"🔗 URL: {entry.link}")

            # Detect language and translate if needed
            try:
                original_language = detect(content)
                if original_language != "es":
                    content = GoogleTranslator(source="auto", target="es").translate(
                        text=content
                    )
                    print(f"🌐 Translated from {original_language} to Spanish")
            except Exception as e:
                print(f"⚠️ Translation error: {e}")
                return None

            # Classify content
            classification_text = content.strip().replace("\n", " ")[:MAX_CLASSIFICATION_LENGTH]
            if self.classifier:
                result = self.classifier(classification_text)[0]
                base_score = result["score"]

                # Adjust score based on feedback
                adjustment = self.feedback_system.get_relevance_adjustment(entry.link)
                final_score = min(1.0, max(0.0, base_score + adjustment))

                if final_score < RELEVANCE_THRESHOLD:
                    return None

                print(f"🤖 Classification: {result['label']} (score: {final_score:.2f})")

                # Add automatic feedback
                self.feedback_system.add_feedback(
                    url=entry.link,
                    is_relevant=True,
                    category=result['label']
                )

            # Generate summary
            summary_text = content.strip().replace("\n", " ")[:MAX_SUMMARY_LENGTH]
            if self.summarizer:
                summary = self.summarizer(
                    summary_text,
                    max_length=SUMMARY_MAX_LENGTH,
                    min_length=SUMMARY_MIN_LENGTH,
                    do_sample=False,
                )[0]["summary_text"]
                print("✂️ Summary generated")
            else:
                summary = summary_text[:700] + "..."

            return {
                "title": entry.title,
                "link": entry.link,
                "summary": summary,
                "score": final_score,
                "date": entry.get("published_parsed", None),
                "category": result.get('label', 'general')
            }

        except Exception as e:
            print(f"⚠️ Error processing entry: {e}")
            return None

    def save_markdown(self, articles, filename):
        """Save articles as Markdown file"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 📰 Daily Summary - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            for article in articles:
                f.write(f"## [{article['title']}]({article['link']})\n")
                f.write(f"{article['summary']}\n\n")
                f.write(f"_Category: {article['category']} | Score: {article['score']:.2f}_\n\n")

        print(f"✅ Summary saved as Markdown in: {output_path}")

    def save_html(self, articles, filename):
        """Save articles as HTML file"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"""
            <html>
                <head>
                    <meta charset='utf-8'>
                    <title>Daily Summary {datetime.now().strftime("%Y-%m-%d")}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; }}
                        h1 {{ color: #2c3e50; }}
                        h2 {{ color: #34495e; }}
                        a {{ color: #3498db; text-decoration: none; }}
                        a:hover {{ text-decoration: underline; }}
                        .metadata {{ color: #7f8c8d; font-style: italic; }}
                    </style>
                </head>
                <body>
            """)
            f.write(f"<h1>📰 Daily Summary - {datetime.now().strftime('%Y-%m-%d')}</h1>")
            for article in articles:
                f.write(f"<h2><a href='{article['link']}'>{article['title']}</a></h2>")
                f.write(f"<p>{article['summary']}</p>")
                f.write(f"<p class='metadata'>Category: {article['category']} | Score: {article['score']:.2f}</p>")
            f.write("</body></html>")

        print(f"✅ Summary saved as HTML in: {output_path}")

    def process_feeds(self):
        """Process all RSS feeds and return relevant articles"""
        start_time = time.time()
        entries = self.download_articles()

        relevant_articles = []
        for entry in entries:
            result = self.process_entry(entry)
            if result:
                relevant_articles.append(result)

        # Sort by score and date
        relevant_articles.sort(
            key=lambda x: (x["score"], x.get("date", 0)), reverse=True
        )
        relevant_articles = relevant_articles[:MAX_ARTICLES]

        end_time = time.time()
        print(f"⏱️ Total processing time: {end_time - start_time:.2f} seconds")
        print(f"📊 Found {len(relevant_articles)} relevant articles out of {len(entries)}")

        return relevant_articles


def main():
    """Main execution function"""
    print("🚀 Starting RSS processor...")
    processor = RSSProcessor()
    articles = processor.process_feeds()

    if articles:
        date_str = datetime.now().strftime("%Y-%m-%d")
        processor.save_markdown(articles, f"summary_{date_str}.md")
        processor.save_html(articles, f"summary_{date_str}.html")
        print("✨ Processing completed successfully!")
    else:
        print("❌ No relevant articles found.")


if __name__ == "__main__":
    main()