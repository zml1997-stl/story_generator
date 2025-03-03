# models/story.py
from app import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    genre = db.Column(db.String(128))
    prompt = db.Column(db.Text)
    current_state = db.Column(db.Text)  # Stores the current narrative state
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    history = db.Column(db.Text) #Stores the history of the story and user inputs.

    def __repr__(self):
        return '<Story {}>'.format(self.title)
