from .models import *
from .views import *
from .controllers import *
from .main import *

def create_app():
    app = Flask(__name__)

    # Correctly setting up configurations
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
    
    # Initialize the database
    db.init_app(app)

    # Register blueprints (views)
    app.register_blueprint(user_views, url_prefix='/user')

    return app