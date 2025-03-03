import requests
import os

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

def generate_story(prompt: str, genre: str, user_name: str = "") -> str:
    """
    Interact with the Gemini API to generate a story based on the provided prompt, genre, and user input.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Customize the prompt based on user input
    user_prompt = f"{user_name}'s {genre} story: {prompt}" if user_name else f"{genre} story: {prompt}"

    data = {
        "model": "gemini-2.0-flash",
        "prompt": user_prompt,
        "max_tokens": 300,
    }

    # Make the API request
    response = requests.post("https://api.gemini.example.com/v1/generate", headers=headers, json=data)

    if response.status_code == 200:
        story = response.json().get("text", "")
        return story
    else:
        return "Sorry, we couldn't generate a story at this time."
