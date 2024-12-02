import requests
from decouple import config
from django.conf import settings

def check_email_breaches(email):
    """Check for email breaches using the Have I Been Pwned API (via RapidAPI)."""
    url = f"https://troyhunt-have-i-been-pwned.p.rapidapi.com/v2/breachedaccount/{email}"
    headers = {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,  # Load API key securely from .env
        "x-rapidapi-host": "troyhunt-have-i-been-pwned.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()  # Returns the list of breaches
        elif response.status_code == 404:
            return "No breaches found."
        else:
            return f"Error: {response.status_code} - {response.reason}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"
