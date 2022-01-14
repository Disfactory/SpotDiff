# Bring other packages onto the path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers import root
from models.model import db
from flask import Flask
from flask_testing import TestCase


class BasicTest(TestCase):
    """The basic test class for others to inherit."""
    def create_app(self):
        app = Flask(__name__)
        app.register_blueprint(root.bp)
        app.config.from_object("config.config.TestingConfig")
        db.init_app(app)

        # Pass in test configuration
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.session.close()
