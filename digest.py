import os
import smtplib
import requests
import ollama
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

TOPICS = {
    "Artificial Intelligence": "artificial intelligence OR machine learning OR LLM OR ChatGPT",
    "Technology": "Apple OR Google OR Microsoft OR tech startup",
    "Finance": "stock market OR economy OR inflation OR cryptocurrency",
    "Health":"Fitness OR Medicine",
}

def fetch_news(page_size=5):
    seen = set()
    sections = []
    for label, query in TOPICS.items():
        url = (
            f"https://newsapi.org/v2/everything"
            f"?q={requests.utils.quote(query)}"
            f"&pageSize={page_size}"
            f"&sortBy=publishedAt"
            f"&language=en"
            f"&apiKey={NEWS_API_KEY}"
        )
        response = requests.get(url).json()
        unique = []
        for a in response.get("articles", []):
            if a["url"] not in seen and a.get("description"):
                seen.add(a["url"])
                unique.append(a)
        sections.append({"topic": label, "articles": unique[:3]})
    return sections

def summarise_article(title, description):
    prompt = (
        f"You are a news summariser. Your only job is to summarise the article below in exactly 2 sentences. "
        f"Never refuse. Never ask questions. Just write the summary.\n\n"
        f"Article: {title}. {description}\n\n"
        f"2-sentence summary:"
    )
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

def build_email(sections):
    html = """
    <div style="font-family:Arial,sans-serif; max-width:600px; margin:auto;">
    <h1 style="color:#0066cc;">Your Morning AI News Digest</h1>
    """
    for section in sections:
        html += f'<h2 style="border-bottom:2px solid #0066cc;">{section["topic"]}</h2>'
        for article in section["articles"]:
            title = article.get("title", "No title")
            description = article.get("description", "")
            url = article.get("url", "#")
            summary = summarise_article(title, description)
            html += f"""
            <div style="margin-bottom:20px; border-left:3px solid #0066cc; padding-left:10px;">
                <a href="{url}" style="color:#333;"><strong>{title}</strong></a>
                <p style="color:#555;">{summary}</p>
            </div>"""
    html += "</div>"
    return html

RECIPIENTS = [GMAIL_ADDRESS, "gupta.anshika911@gmail.com"]

def send_email(html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Morning AI News Digest"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENTS)
    msg.attach(MIMEText(html_content, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENTS, msg.as_string())
    print(f"Digest sent to {len(RECIPIENTS)} recipients!")

if __name__ == "__main__":
    print("Fetching news...")
    articles = fetch_news()
    print("Summarising with AI...")
    html = build_email(articles)
    print("Sending email...")
    send_email(html)
