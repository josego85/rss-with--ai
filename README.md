# 📰 RSS-WITH-AI

This Python script processes articles from technology RSS feeds using AI to automatically filter and summarize the most relevant content. The results are saved as `.md` (Markdown) and `.html` files.

---

## ✅ Features

- 🔎 Reads RSS feeds (e.g., OMG! Ubuntu)
- 🌍 Detects the article's language (Spanish, English, German, etc.)
- 🌐 Translates to Spanish if necessary
- 🧠 Uses AI to classify and filter only relevant articles
- ✂️ Automatically summarizes content with a language model
- 📝 Exports results in Markdown and HTML files

---

## ⚙️ Requirements

- Python 3.11 
- Internet connection (to access models and feeds)

---

## 📦 Installation

Clone the repository and navigate to the directory:

```bash
git clone git@github.com:josego85/rss-with--ai.git
cd rss-with--ai
```

Set up the environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Usage

Simply run:

```bash
python main.py
```

The output files will be located in the `output/` folder.

---

## 🧠 Models Used

- `mrm8488/bert-mini-finetuned-age_news-classification` → Relevance classification (AI)
- `sshleifer/distilbart-cnn-12-6` → Automatic summarization

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, create a branch, and submit a pull request.

---

## 📧 Contact

For questions or suggestions, contact [josego85@gmail.com].