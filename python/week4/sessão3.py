import requests
import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_path = Path("data") / "olist.db"

# Fetch all repositories for a given GitHub user, handling pagination
def get_repos(username):
    all_repos = []
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"page": page, "per_page": 30},
            timeout=5
        )
        response.raise_for_status()
        repos = response.json()

        # Stop when the API returns an empty page
        if not repos:
            break
        all_repos.extend(repos)
        logger.info(f"Page {page} — {len(repos)} repos fetched")
        page += 1
    return all_repos

# Load repositories into SQLite, skipping duplicates via INSERT OR IGNORE
def load_repos(repos, conn):
    cursor = conn.cursor()

    # Create table if it doesn't exist yet
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS github_repos (
            id INTEGER PRIMARY KEY,
            name TEXT,
            owner TEXT,
            stars INTEGER,
            language TEXT
        )
    """)

    # Extract only the fields we need from each repo dict
    rows = [
        (repo['id'], repo['name'], repo['owner']['login'], repo['stargazers_count'], repo.get('language'))
        for repo in repos
    ]

    # Batch insert — idempotent, safe to re-run
    cursor.executemany("""
        INSERT OR IGNORE INTO github_repos (id, name, owner, stars, language)
        VALUES (?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    logger.info(f"Rows inserted: {cursor.rowcount}")

# Connect to the database, run the pipeline, then close the connection
conn = sqlite3.connect(db_path)
repos = get_repos("torvalds")
load_repos(repos, conn)
conn.close()