from flask import Flask
from config import Config
from flask_login import LoginManager
from models import db  # Import db from the models module
from routes import main, auth, story  # Import your routes here

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)  # Initialize db with the app

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Define the login view for Flask-Login

# Register blueprints (routes)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(story)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
