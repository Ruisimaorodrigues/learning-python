import requests
import sqlite3
import logging
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_path = Path("data") / "olist.db"

# Fetch all repos for a user with retry logic and pagination
def get_repos(username, max_retries=3):
    all_repos = []
    page = 1

    while True:
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"https://api.github.com/users/{username}/repos",
                    params={"page": page, "per_page": 30},
                    timeout=5
                )
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2 ** attempt)
        else:
            raise Exception(f"Failed to fetch page {page} after {max_retries} attempts")

        repos = response.json()
        if not repos:
            break

        all_repos.extend(repos)
        logger.info(f"Page {page} — {len(repos)} repos fetched")
        page += 1

    return all_repos

# Idempotent load — safe to run multiple times without duplicating data
def load_repos(repos, conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS github_repos_v2 (
            id INTEGER PRIMARY KEY,
            name TEXT,
            owner TEXT,
            stars INTEGER,
            language TEXT,
            loaded_at TEXT DEFAULT (datetime('now'))
        )
    """)

    rows = [
        (repo['id'], repo['name'], repo['owner']['login'],
         repo['stargazers_count'], repo.get('language'))
        for repo in repos
    ]

    # Use INSERT OR REPLACE to update existing records if stars changed
    cursor.executemany("""
        INSERT OR REPLACE INTO github_repos_v2 (id, name, owner, stars, language)
        VALUES (?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    logger.info(f"Rows upserted: {len(rows)}")

# Verify idempotency — row count should be stable across runs
def verify_load(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM github_repos_v2")
    count = cursor.fetchone()[0]
    logger.info(f"Total rows in table: {count}")

conn = sqlite3.connect(db_path)
repos = get_repos("torvalds")
load_repos(repos, conn)
verify_load(conn)
conn.close()