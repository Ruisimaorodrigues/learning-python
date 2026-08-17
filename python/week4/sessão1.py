import requests
import logging
import time
print("script iniciado")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_with_retry(url, max_retries=3, timeout=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout na tentativa {attempt + 1}")
            time.sleep(2 ** attempt)
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP: {e}")
            raise
        except requests.exceptions.ConnectionError:
            logger.warning(f"Erro de ligação na tentativa {attempt + 1}")
            time.sleep(2 ** attempt)
    raise Exception(f"Falhou após {max_retries} tentativas")

url = "https://api.github.com/users/torvalds/repos"
repos = get_with_retry(url)
logger.info(f"Total de repos encontrados: {len(repos)}")
for repo in repos:
    logger.info(f"Repo: {repo['name']} | Stars: {repo['stargazers_count']}")