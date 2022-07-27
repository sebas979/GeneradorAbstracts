from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        OPENAI_KEY=os.environ.get('OPENAI_API_KEY')
    )

    from . import proyecto

    app.register_blueprint(proyecto.bp)

    return app