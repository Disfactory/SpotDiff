from flask_migrate import Migrate
from app.app import app
from models.model import db
from controllers import root
from controllers import template_controller
from controllers import user_controller
from controllers import location_controller
from controllers import status_controller
from controllers import answer_controller
from flask_cors import CORS

# Register all routes to the blueprint
app.register_blueprint(root.bp)
app.register_blueprint(template_controller.bp, url_prefix="/template")
app.register_blueprint(user_controller.bp, url_prefix="/user")
app.register_blueprint(location_controller.bp, url_prefix="/location")
app.register_blueprint(status_controller.bp, url_prefix="/status")
app.register_blueprint(answer_controller.bp, url_prefix="/answer")
CORS(app, resources={r"/.*": {"origins": ["https://disfactory-spotdiff.netlify.app", "https://*.netlify.app"]}}) 

# Set database migration
migrate = Migrate(app, db)
