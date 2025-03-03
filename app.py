from flask import Flask
from config import Config
from routes import main, auth, story
from models import db
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Register blueprints (routes)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(story)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
