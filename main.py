import os
from app import app
from routes import register_routes
from auth import auth_bp

# Configure the upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Register auth blueprint
app.register_blueprint(auth_bp)

# Register API routes for new features
from api_definitions import register_api_routes
register_api_routes(app)

# Register infrastructure project routes
from infrastructure_projects import register_infrastructure_project_routes
register_infrastructure_project_routes(app)

# Register all routes (this includes new feature routes)
register_routes(app)

# Initialize localization helper
from localization_helper import init_app
init_app(app)

# Check if user needs language selection on first visit
@app.before_request
def check_language_selection():
    from flask_login import current_user
    from flask import request, redirect, url_for
    
    # Skip for static files, auth routes, API routes, and language selection itself
    if (request.endpoint and 
        not request.endpoint.startswith('static') and
        not request.endpoint.startswith('auth.') and
        'api' not in request.endpoint and
        request.endpoint != 'select_language' and
        hasattr(current_user, 'is_authenticated') and
        current_user.is_authenticated and
        not getattr(current_user, 'onboarding_completed', False)):
        # Redirect to language selection if not completed
        return redirect(url_for('select_language'))

if __name__ == "__main__":
    # Determine if we're running in production or development
    is_prod = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app with appropriate settings
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=not is_prod
    )
