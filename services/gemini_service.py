import streamit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Function to generate text using Gemini API
def generate_text(prompt: str) -> str:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

# Function to parse story and choices from API response
def parse_story_and_choices(text: str):
    lines = text.split('\n')
    story_lines = []
    choices = []
    for line in lines:
        if line.strip().startswith(('1.', '2.', '3.')):
            choices.append(line.strip())
        else:
            story_lines.append(line)
    story = '\n'.join(story_lines).strip()
    return story, choices

# Streamlit app
st.title("Interactive Story Generator")
st.write("Shape your own adventure with choices that create a unique tale!")

# Initialize session state
if 'story_segments' not in st.session_state:
    st.session_state.story_segments = []
if 'choices_made' not in st.session_state:
    st.session_state.choices_made = []
if 'current_choices' not in st.session_state:
    st.session_state.current_choices = []
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""

# User input for personalization
character_name = st.text_input("Enter your character's name:", "Alex")

# Generate random story prompts for selection
if st.button("Generate Story Prompts"):
    prompt = "Generate three short opening scenes for stories in different genres (e.g., Mystery, Fantasy, Sci-Fi, Romance). Each scene should be one paragraph and end with two numbered choices for the next action."
    response = generate_text(prompt)
    scenes, _ = parse_story_and_choices(response)
    st.session_state.story_segments = [scenes]
    st.session_state.current_choices = ["1. Select the first story", "2. Select the second story", "3. Select the third story"]
    st.session_state.current_prompt = prompt

# Display story segments
for segment in st.session_state.story_segments:
    st.write(segment)

# Handle choices
if st.session_state.current_choices:
    selected_choice = st.radio("Choose your path:", st.session_state.current_choices, key=f"choice_{len(st.session_state.choices_made)}")
    if st.button("Continue"):
        choice = selected_choice
        st.session_state.choices_made.append(choice)
        
        if len(st.session_state.story_segments) == 1 and not st.session_state.choices_made:
            # User selects initial story prompt
            choice_num = int(choice.split('.')[0])
            selected_prompt = f"Take the {['first', 'second', 'third'][choice_num-1]} story scene and expand it into a {character_name}'s adventure. Add two numbered choices at the end."
            response = generate_text(selected_prompt)
            story, choices = parse_story_and_choices(response)
            st.session_state.story_segments = [story]
            st.session_state.current_choices = choices
            st.session_state.current_prompt = selected_prompt
        else:
            # Continue the story based on the choice
            next_prompt = f"{st.session_state.current_prompt} {character_name} chose: {choice}. Continue the story with two numbered choices at the end."
            response = generate_text(next_prompt)
            next_story, next_choices = parse_story_and_choices(response)
            st.session_state.story_segments.append(next_story)
            st.session_state.current_choices = next_choices
            st.session_state.current_prompt = next_prompt
else:
    if st.session_state.story_segments and len(st.session_state.story_segments) > 1:
        st.write("The end.")
        story_text = "\n\n".join(st.session_state.story_segments)
        st.download_button("Download Your Story", story_text, file_name="my_story.txt")

# Restart option
if st.button("Restart"):
    st.session_state.story_segments = []
    st.session_state.choices_made = []
    st.session_state.current_choices = []
    st.session_state.current_prompt = ""
