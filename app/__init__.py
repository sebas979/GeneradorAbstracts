from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='mipassword',
        OPENAI_KEY=os.environ.get('OPENAI_API_KEY1')
    )

    from . import proyecto

    app.register_blueprint(proyecto.bp)

    return app