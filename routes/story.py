from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.story import Story
from services.gemini_service import generate_story_content, generate_choices, continue_story

bp = Blueprint('story', __name__, url_prefix='/story')

@bp.route('/generate', methods=['GET'])
@login_required
def generate_story():
    genre = request.args.get('genre')
    if not genre:
        flash('Please select a genre.')
        return redirect(url_for('main.index'))

    prompt = f"Generate a short story prompt in the {genre} genre with an opening scene."
    story_content = generate_story_content(prompt)

    if story_content:
        story = Story(
            title=f"{genre.capitalize()} Story",
            genre=genre,
            prompt=story_content,
            current_state=story_content,
            user_id=current_user.id,
            history=story_content
        )
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('story.view_story', story_id=story.id))
    else:
        flash('Error generating story prompt.')
        return redirect(url_for('main.index'))

@bp.route('/<int:story_id>', methods=['GET', 'POST'])
@login_required
def view_story(story_id):
    story = Story.query.get_or_404(story_id)
    if story.user_id != current_user.id:
        flash('You do not have permission to view this story.')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user_choice = request.form.get('choice')
        if user_choice:
            new_content = continue_story(story.current_state, user_choice)
            if new_content:
                story.current_state = new_content
                story.history = story.history + user_choice + new_content
                db.session.commit()
            else:
                flash('Error continuing story.')
        else:
            flash('Please select a choice.')

    choices = generate_choices(story.current_state)
    return render_template('story.html', story=story, choices=choices)
