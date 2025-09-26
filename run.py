#!/usr/bin/env python3
"""
Flask application entry point for the Expense Tracker app.
"""

import os
from dotenv import load_dotenv
from flask.cli import FlaskGroup

# Load environment variables
load_dotenv()

from app import create_app, db
from app.models import User, Category, Expense

app = create_app()

# Create Flask CLI group
cli = FlaskGroup(app)

@app.shell_context_processor
def make_shell_context():
    """Register shell context variables."""
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Expense': Expense
    }

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database tables created!")
    
    # Check if default categories exist
    if not Category.query.filter_by(user_id=None).first():
        print("Adding default categories...")
        default_categories = [
            {'name': 'Food & Dining', 'icon': '🍽️', 'color': '#EF4444'},
            {'name': 'Transportation', 'icon': '🚗', 'color': '#10B981'},
            {'name': 'Shopping', 'icon': '🛍️', 'color': '#8B5CF6'},
            {'name': 'Entertainment', 'icon': '🎬', 'color': '#F59E0B'},
            {'name': 'Bills & Utilities', 'icon': '💡', 'color': '#06B6D4'},
            {'name': 'Healthcare', 'icon': '🏥', 'color': '#EC4899'},
            {'name': 'Education', 'icon': '📚', 'color': '#6366F1'},
            {'name': 'Other', 'icon': '📋', 'color': '#6B7280'},
        ]
        
        for cat_data in default_categories:
            category = Category(
                name=cat_data['name'],
                icon=cat_data['icon'],
                color=cat_data['color'],
                user_id=None
            )
            db.session.add(category)
        
        db.session.commit()
        print("Default categories added!")
    
    print("Database initialization complete!")

@app.cli.command()
def create_admin():
    """Create an admin user."""
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        print("User already exists!")
        return
    
    if User.query.filter_by(email=email).first():
        print("Email already exists!")
        return
    
    # Create admin user
    admin = User(username=username, email=email, password=password)
    db.session.add(admin)
    db.session.flush()
    
    # Create personal categories for admin
    Category.create_user_categories(admin.id)
    
    db.session.commit()
    print(f"Admin user '{username}' created successfully!")

if __name__ == '__main__':
    # For development - use flask run for production
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)