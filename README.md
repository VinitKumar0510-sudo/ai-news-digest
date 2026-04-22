# AI Morning News Digest

Automated daily news digest delivered to your inbox every morning, summarised by a local LLM.

## How It Works

```
7am cron job triggers digest.py
        ↓
NewsAPI → fetch latest articles (AI, Tech, Finance, Health)
        ↓
Ollama (llama3.2:3b) → summarise each article locally
        ↓
Gmail SMTP → formatted HTML email to recipients
```

## Stack

| Component | Tool |
|-----------|------|
| News data | NewsAPI |
| Summarisation | Ollama (llama3.2:3b — runs locally, no API cost) |
| Email delivery | Gmail SMTP |
| Scheduling | cron |

## Setup

```bash
# Install Ollama and pull model
brew install ollama
brew services start ollama
ollama pull llama3.2:3b

# Install dependencies
pip install requests ollama python-dotenv

# Configure credentials
cp .env.example .env
# Fill in NEWS_API_KEY, GMAIL_ADDRESS, GMAIL_APP_PASSWORD
```

## Configuration

Add your credentials to `.env`:
```
NEWS_API_KEY=your_newsapi_key
GMAIL_ADDRESS=your@gmail.com
GMAIL_APP_PASSWORD=your_16char_app_password
```

Customise topics in `digest.py`:
```python
TOPICS = {
    "Artificial Intelligence": "artificial intelligence OR machine learning OR LLM",
    "Technology": "Apple OR Google OR Microsoft OR tech startup",
    "Finance": "stock market OR economy OR cryptocurrency",
    "Health": "Fitness OR Medicine",
}
```

## Scheduling (Mac)

```bash
# Run every day at 7am
crontab -e
# Add: 0 7 * * * cd /path/to/ai-news-digest && python3 digest.py
```

## Features

- Fully local LLM — no OpenAI API costs
- Deduplication across topics
- Multi-recipient support
- Customisable topics and schedule
