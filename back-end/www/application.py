from flask_migrate import Migrate
from app.app import app
from models.model import db
from controllers import root
from controllers import template_controller
from controllers import user_controller
from controllers import location_controller


# Register all routes to the blueprint
app.register_blueprint(root.bp)
app.register_blueprint(template_controller.bp, url_prefix="/template")
app.register_blueprint(user_controller.bp, url_prefix="/user")
app.register_blueprint(location_controller.bp, url_prefix="/location")

# Set database migration
migrate = Migrate(app, db)
