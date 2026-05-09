import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
# Email-CONFIG 
# ─────────────────────────────────────────────
EMAIL_SENDER    = "samuelpwlehjr13@gmail.com"
EMAIL_PASSWORD  = "ovnb piug clbh csjt"      
GROUP_EMAILS    = [
    "kanatnur0501@gmail.com",
    "aiteginshabaeva00@gmail.com",
    "abdullohahmatkulov@gmail.com",
    "Rashedhaylooz6@gmail.com",
    "Kenzaynouri17@gmail.com",
    "abdullohahmatkulov@gmail.com"
    "aiteginshabaeva00@gmail.com"
]
SAVED_DATA_DIR  = "scraped_data"
# ─────────────────────────────────────────────

os.makedirs(SAVED_DATA_DIR, exist_ok=True)


def scrape_url(url: str) -> dict:
    """Fetch and parse a URL, returning structured data."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ITEC224Bot/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    title = soup.title.string.strip() if soup.title else "No title found"

    # Meta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")

    # All headings
    headings = []
    for tag in ["h1", "h2", "h3"]:
        for el in soup.find_all(tag):
            text = el.get_text(strip=True)
            if text:
                headings.append({"tag": tag.upper(), "text": text})

    # All paragraph texts (first 20)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)][:20]

    # All links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if href.startswith("http") and text:
            links.append({"text": text, "href": href})

    # Images count
    images = [img.get("src", "") for img in soup.find_all("img") if img.get("src")]

    data = {
        "url": url,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "meta_description": meta_desc,
        "headings": headings[:30],
        "paragraphs": paragraphs,
        "links": links[:30],
        "image_count": len(images),
    }
    return data


def save_data(data: dict) -> str:
    """Save scraped data to a JSON file and return the file path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = data["url"].replace("https://", "").replace("http://", "").split("/")[0]
    filename = f"{SAVED_DATA_DIR}/{domain}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename


def send_email(data: dict, filepath: str):
    """Send the scraped data via email to all group members."""
    subject = f"[ITEC224] Scraped Data: {data['title']} — {data['scraped_at']}"

    body = f"""
Hello Team,

Here is the automated scrape report for: {data['url']}
Scraped at: {data['scraped_at']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 PAGE TITLE
{data['title']}

📝 META DESCRIPTION
{data['meta_description'] or 'N/A'}

📋 HEADINGS ({len(data['headings'])} found)
""" + "\n".join(f"  [{h['tag']}] {h['text']}" for h in data['headings'][:10]) + f"""

📄 PARAGRAPHS (first 5)
""" + "\n\n".join(f"  • {p[:200]}" for p in data['paragraphs'][:5]) + f"""

🔗 LINKS ({len(data['links'])} found)
""" + "\n".join(f"  • {l['text']}: {l['href']}" for l in data['links'][:10]) + f"""

🖼️ Images found: {data['image_count']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full data attached as JSON.

Best regards,
ITEC224 Auto-Scraper Bot
"""

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = ", ".join(GROUP_EMAILS)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach the JSON file
    with open(filepath, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filepath)}")
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, GROUP_EMAILS, msg.as_string())


def scrape_and_send(url: str) -> dict:
    """Full pipeline: scrape → save → email → return summary."""
    data     = scrape_url(url)
    filepath = save_data(data)

    try:
        send_email(data, filepath)
        data["email_sent"] = True
    except Exception as e:
        data["email_sent"] = False
        data["email_error"] = str(e)

    data["saved_file"] = filepath
    return data
