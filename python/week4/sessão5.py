import requests
import sqlite3
import logging
import time
from pathlib import Path
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_path = Path("data") / "olist.db"

# --- EXTRACT ---
# Fetch all public repos for a list of users with pagination and retry
def fetch_repos(username, max_retries=3):
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
                logger.warning(f"Attempt {attempt + 1} failed for {username}: {e}")
                time.sleep(2 ** attempt)
        else:
            logger.error(f"Failed to fetch page {page} for {username}")
            break

        repos = response.json()
        if not repos:
            break

        all_repos.extend(repos)
        page += 1

    logger.info(f"Fetched {len(all_repos)} repos for {username}")
    return all_repos

# --- TRANSFORM ---
# Extract only the fields we need and add a pipeline timestamp
def transform_repos(repos, username):
    return [
        {
            "id": repo["id"],
            "name": repo["name"],
            "owner": username,
            "stars": repo["stargazers_count"],
            "language": repo.get("language"),
            "created_at": repo["created_at"],
            "extracted_at": datetime.now(timezone.utc).isoformat()
        }
        for repo in repos
    ]

# --- LOAD ---
# Idempotent upsert into SQLite
def load_repos(records, conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_repos (
            id INTEGER PRIMARY KEY,
            name TEXT,
            owner TEXT,
            stars INTEGER,
            language TEXT,
            created_at TEXT,
            extracted_at TEXT
        )
    """)

    rows = [
        (r["id"], r["name"], r["owner"], r["stars"],
         r["language"], r["created_at"], r["extracted_at"])
        for r in records
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO pipeline_repos
        (id, name, owner, stars, language, created_at, extracted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    logger.info(f"Loaded {len(rows)} records into pipeline_repos")

# --- VERIFY ---
# Confirm row count and show top 5 by stars
def verify(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pipeline_repos")
    count = cursor.fetchone()[0]
    logger.info(f"Total rows: {count}")

    cursor.execute("""
        SELECT owner, name, stars
        FROM pipeline_repos
        ORDER BY stars DESC
        LIMIT 5
    """)
    logger.info("Top 5 repos by stars:")
    for row in cursor.fetchall():
        logger.info(f"  {row[0]}/{row[1]} — {row[2]} stars")

# --- PIPELINE ---
users = ["torvalds", "gvanrossum", "antirez"]

conn = sqlite3.connect(db_path)

for user in users:
    raw = fetch_repos(user)
    transformed = transform_repos(raw, user)
    load_repos(transformed, conn)

verify(conn)
conn.close()