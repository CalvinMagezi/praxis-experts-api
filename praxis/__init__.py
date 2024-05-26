from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('praxis.config.DevelopmentConfig')

    from .routes.projects import projects_blueprint
    from .routes.experts import experts_blueprint
    from .routes.praxis import praxis_blueprint

    app.register_blueprint(projects_blueprint)
    app.register_blueprint(experts_blueprint)
    app.register_blueprint(praxis_blueprint)

    return app