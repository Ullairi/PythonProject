from flask import Flask
from flask_migrate import Migrate

from src.core.config import settings
from src.core.db import db
from src.models.questions import Question, Statistic
from src.models.category import Category
from src.models.response import Response


def init_database(app: Flask) -> None:
    db.init_app(app)
    migrate = Migrate(app, db)


def register_routers(app: Flask) -> None:
    from src.routers.questions import questions_bp

    app.register_blueprint(questions_bp)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(settings.get_flask_config())

    init_database(app)
    register_routers(app)

    return app