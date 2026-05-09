import schedule
import time
import scraper

# ─────────────────────────────────────────
# Put the default URL to scrape daily here
# ─────────────────────────────────────────
DEFAULT_URL = "https://www.bbc.com"


def daily_job():
    print(f"[Scheduler] Running daily scrape for: {DEFAULT_URL}")
    try:
        result = scraper.scrape_and_send(DEFAULT_URL)
        print(f"[Scheduler] Done. File saved: {result.get('saved_file')}")
        if result.get("email_sent"):
            print("[Scheduler] Email sent successfully.")
        else:
            print(f"[Scheduler] Email failed: {result.get('email_error')}")
    except Exception as e:
        print(f"[Scheduler] Error: {e}")


def start_scheduler():
    """Run the scheduler loop — call this in a background thread."""
    schedule.every().day.at("08:00").do(daily_job)
    print("[Scheduler] Started. Daily job scheduled at 08:00.")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    # Run standalone for testing
    start_scheduler()
