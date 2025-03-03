# services/gemini_service.py
import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GOOGLE_API_KEY)

def generate_story_content(prompt):
    """Generates story content using the Gemini API."""
    model = genai.GenerativeModel('gemini-2.0-flash') #using flash model
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def generate_choices(current_state):
    """Generates user choices based on the current story state."""
    prompt = f"Based on the following story state: '{current_state}', generate 2-3 possible choices for the user. Return them as a list of strings."
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        response = model.generate_content(prompt)
        # Attempt to split the response into a list of choices
        choices = response.text.split('\n')
        #Clean up choices
        choices = [choice.strip("- *") for choice in choices]
        return choices
    except Exception as e:
        print(f"Error generating choices: {e}")
        return []

def continue_story(current_state, user_choice):
    """Continues the story based on the user's choice."""
    prompt = f"Continue the story based on the following current state: '{current_state}' and the user's choice: '{user_choice}'. Limit the response to 2 paragraphs."
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error continuing story: {e}")
        return None
