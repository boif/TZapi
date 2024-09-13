import os
import requests
from dotenv import load_dotenv

#load ENV items
load_dotenv()
GITHUB_USER = os.getenv('GITHUB_USER')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')

if not GITHUB_USER or not GITHUB_TOKEN or not REPO_NAME:
    raise EnvironmentError(
        "Не все необходимые переменные окружения заданы. Проверьте GITHUB_USER, GITHUB_TOKEN и REPO_NAME.")

BASE_URL = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }


def check_repo_exists():
    url = f"{BASE_URL}/repos/{GITHUB_USER}/{REPO_NAME}"
    response = requests.get(url, headers = get_headers())
    return response.status_code == 200


def create_repo():
    if check_repo_exists():
        print(f"Repo '{REPO_NAME}' already exist")
        return

    url = f"{BASE_URL}/user/repos"
    data = {"name": REPO_NAME, "private": False}

    try:
        response = requests.post(url, json = data, headers = get_headers())
        response.raise_for_status()
        print(f"Repo '{REPO_NAME}' has been created.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when creating repo: {e}")
        raise


def delete_repo():
    if not check_repo_exists():
        print(f"Repo '{REPO_NAME}' does not exist.")
        return

    url = f"{BASE_URL}/repos/{GITHUB_USER}/{REPO_NAME}"
    try:
        response = requests.delete(url, headers = get_headers())
        response.raise_for_status()
        print(f"Repo '{REPO_NAME}' has been deleted.")
    except requests.exceptions.RequestException as e:
        print(f"Error when deleting repo: {e}")
        raise


def test_github_api():
    create_repo()

    #CHECK repo
    assert check_repo_exists(), "Repo has not been created"

    delete_repo()

    #CHECK delete
    assert not check_repo_exists(), "Repo has been deleted"


if __name__ == "__main__":
    test_github_api()
