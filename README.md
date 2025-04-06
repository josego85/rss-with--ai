# 📰 RSS-WITH-AI

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/josego85/rss-with--ai)
[![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11-green.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/josego85/rss-with--ai)
[![Issues](https://img.shields.io/github/issues/josego85/rss-with--ai)](https://github.com/josego85/rss-with--ai/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/josego85/rss-with--ai/pulls)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://img.shields.io/github/downloads/josego85/rss-with--ai/total.svg)](https://github.com/josego85/rss-with--ai/releases)

This Python script processes articles from technology RSS feeds using AI to automatically filter and summarize the most relevant content. The results are saved as `.md` (Markdown) and `.html` files.

## 📑 Table of Contents
- [Features](#-features)
- [Requirements](#️-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Output Structure](#output-structure)
  - [Feedback System](#feedback-system)
- [Models Used](#-models-used)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## ✅ Features

- 🔎 Reads RSS feeds (e.g., OMG! Ubuntu)
- 🌍 Detects the article's language (Spanish, English, German, etc.)
- 🌐 Translates to Spanish if necessary
- 🧠 Uses AI to classify and filter only relevant articles
- ✂️ Automatically summarizes content with a language model
- 📝 Exports results in Markdown and HTML formats
- 📊 Feedback system for continuous learning
- 🎯 Automatic score adjustment based on historical feedback
- ⚡ Concurrent RSS feed processing
- 🎨 Enhanced HTML output with styling
- 📈 Progress indicators with emojis
- ⚠️ Improved error handling and logging

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

The script will:
1. Download articles from configured RSS feeds
2. Process them using AI models
3. Apply feedback-based relevance adjustments
4. Generate summaries
5. Save results in the `output/` folder

### Output Structure

```
output/
├── summary_2025-04-06.md   # Markdown summary
└── summary_2025-04-06.html # HTML summary with styling
```

### Feedback System

The script maintains a feedback database in:

```
data/
└── feedback.json   # Historical feedback data
```

This helps improve article selection over time by:
- Tracking article relevance
- Adjusting scores based on past feedback
- Learning from user preferences

---

## 🧠 Models Used

- `mrm8488/bert-mini-finetuned-age_news-classification` → Relevance classification (AI)
- `sshleifer/distilbart-cnn-12-6` → Automatic summarization

---

## 🔧 Configuration

Key settings in `config.py`:

```python
MAX_ARTICLES = 10              # Maximum articles to show
RELEVANCE_THRESHOLD = 0.85     # Minimum relevance score
MIN_CONTENT_LENGTH = 300       # Minimum article length
```

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, create a branch, and submit a pull request.

---

## 📧 Contact

For questions or suggestions, contact [josego85@gmail.com].