# ITEC224 — Web Development & Scripting Project

A Flask web application featuring web scraping, automated email delivery, and daily scheduling.

---

## Project Structure

```
itec224_project/
├── app.py              # Flask app (routes + app entry point)
├── scraper.py          # Requests + BeautifulSoup scraping + email
├── scheduler.py        # Runs daily job at 08:00 using schedule library
├── requirements.txt    # Python dependencies
├── scraped_data/       # Auto-created — stores JSON result files
└── templates/
    ├── base.html       # Shared layout + navbar
    ├── home.html       # Landing page
    ├── about.html      # Group members postcards
    └── task.html       # URL input form + live results
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure email credentials
Open `scraper.py` and update these values:

```python
EMAIL_SENDER    = "samuelpwlehjr13@gmail.com"
EMAIL_PASSWORD  = "ovnb piug clbh csjt"    
GROUP_EMAILS   = [
    "kanatnur0501@gmail.com",
    "aiteginshabaeva00@gmail.com",
    "abdullohahmatkulov@gmail.com",
    "Rashedhaylooz6@gmail.com",
    "Kenzaynouri17@gmail.com",
    "abdullohahmatkulov@gmail.com"
    "aiteginshabaeva00@gmail.com"
]
```

### 3. Update group member postcards
Open `app.py` and edit the `members` list in the `/about` route with real names, student IDs, hobbies, and photo URLs.

### 4. Run the app
```bash
python app.py
```

browser at: http://localhost:5000

---

## Pages

| Page   | URL       | Description                                   |
|--------|-----------|-----------------------------------------------|
| Home   | `/`       | Landing page with project overview            |
| About  | `/about`  | Postcard grid for each group member           |
| Task   | `/task`   | URL form → scrape → display results + email   |

---

## Scraping Pipeline

1. User enters a URL on the Task page and clicks Scrape URL
2. Flask calls `scraper.scrape_and_send(url)`
3. `requests.get()` fetches the page
4. `BeautifulSoup` parses: title, meta, headings, paragraphs, links, image count
5. Data saved to `scraped_data/<domain>_<timestamp>.json`
6. Email with JSON attachment sent to all group members via Gmail SMTP
7. Results displayed live in the browser

---

## Scheduler

- Runs automatically at 08:00 AM every day
- Configured in `scheduler.py` → `DEFAULT_URL`
- Starts as a background daemon thread when `app.py` launches
- Uses the `schedule` library: `schedule.every().day.at("08:00")`

---

## Dependencies

| Package        | Purpose                            |
|----------------|------------------------------------|
| Flask          | Web framework                      |
| requests       | HTTP requests to fetch web pages   |
| beautifulsoup4 | HTML parsing and data extraction   |
| lxml           | Fast HTML/XML parser backend       |
| schedule       | Cron-like job scheduler in Python  |
