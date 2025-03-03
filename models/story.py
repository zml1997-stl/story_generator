from datetime import datetime
from . import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    plot = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to store user choices
    choices = db.relationship('Choice', backref='story', lazy=True)

    def __repr__(self):
        return f"<Story {self.title} - {self.genre}>"

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    next_story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=True)

    def __repr__(self):
        return f"<Choice {self.description}>"
