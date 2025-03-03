from flask import Blueprint, render_template, request, redirect, url_for
from services.gemini_service import generate_story
from models import db
from models.story import Story

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Render the homepage where users can choose a story genre and prompt
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    # Get input from the user (genre and prompt)
    genre = request.form.get('genre')
    prompt = request.form.get('prompt')
    user_name = request.form.get('user_name', "")

    # Generate the story using Gemini service
    story_text = generate_story(prompt, genre, user_name)

    # Optionally, save the generated story in the database
    new_story = Story(title=prompt, genre=genre, plot=story_text)
    db.session.add(new_story)
    db.session.commit()

    return render_template('story.html', story=story_text)
