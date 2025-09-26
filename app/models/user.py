from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_total_expenses(self):
        """Get total number of expenses for this user."""
        return self.expenses.count()
    
    def get_total_amount(self):
        """Get total amount spent by this user."""
        from sqlalchemy import func
        result = db.session.query(func.sum(Expense.amount)).filter_by(user_id=self.id).scalar()
        return result or 0.0
    
    def get_monthly_total(self, year=None, month=None):
        """Get total spending for a specific month."""
        from sqlalchemy import func, extract
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
            
        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == self.id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).scalar()
        return result or 0.0
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'total_expenses': self.get_total_expenses(),
            'total_amount': self.get_total_amount()
        }

# Import Expense here to avoid circular import
from app.models.expense import Expense