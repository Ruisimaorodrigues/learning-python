import requests
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_repos(username, per_page=30):
    all_repos = []
    page = 1
    
    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"page": page, "per_page": per_page}
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        repos = response.json()
        
        if not repos:
            break
            
        all_repos.extend(repos)
        logger.info(f"Página {page} — {len(repos)} repos encontrados")
        page += 1
        time.sleep(0.5)
    
    return all_repos

repos = get_all_repos("sindresorhus", per_page=30)
logger.info(f"Total de repos: {len(repos)}")