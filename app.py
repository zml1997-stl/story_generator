# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from routes import auth, main, story
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(story.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
