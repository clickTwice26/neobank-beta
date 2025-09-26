from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.expenses import expenses_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize default categories if they don't exist
        from app.models.category import Category
        if not Category.query.filter_by(user_id=None).first():
            default_categories = [
                {'name': 'Food & Dining', 'icon': 'fas fa-utensils', 'color': '#EF4444'},
                {'name': 'Transportation', 'icon': 'fas fa-car', 'color': '#10B981'},
                {'name': 'Shopping', 'icon': 'fas fa-shopping-bag', 'color': '#8B5CF6'},
                {'name': 'Entertainment', 'icon': 'fas fa-film', 'color': '#F59E0B'},
                {'name': 'Bills & Utilities', 'icon': 'fas fa-lightbulb', 'color': '#06B6D4'},
                {'name': 'Healthcare', 'icon': 'fas fa-hospital', 'color': '#EC4899'},
                {'name': 'Education', 'icon': 'fas fa-book', 'color': '#6366F1'},
                {'name': 'Other', 'icon': 'fas fa-folder', 'color': '#6B7280'},
            ]
            
            for cat_data in default_categories:
                category = Category(
                    name=cat_data['name'],
                    icon=cat_data['icon'],
                    color=cat_data['color'],
                    user_id=None  # Global categories
                )
                db.session.add(category)
            
            db.session.commit()
    
    return app