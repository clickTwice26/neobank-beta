from app import db
from datetime import datetime

class Category(db.Model):
    """Category model for organizing expenses."""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(20), default='fas fa-folder')
    color = db.Column(db.String(7), default='#6B7280')  # Hex color code
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='category', lazy='dynamic')
    
    def __init__(self, name, icon='fas fa-folder', color='#6B7280', user_id=None):
        self.name = name
        self.icon = icon
        self.color = color
        self.user_id = user_id
    
    def get_expense_count(self, user_id=None):
        """Get number of expenses in this category."""
        query = self.expenses
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.count()
    
    def get_total_amount(self, user_id=None, year=None, month=None):
        """Get total amount for this category."""
        from sqlalchemy import func, extract
        from app.models.expense import Expense
        
        query = db.session.query(func.sum(Expense.amount)).filter_by(category_id=self.id)
        
        if user_id:
            query = query.filter(Expense.user_id == user_id)
        
        if year:
            query = query.filter(extract('year', Expense.date) == year)
        
        if month:
            query = query.filter(extract('month', Expense.date) == month)
            
        result = query.scalar()
        return result or 0.0
    
    @staticmethod
    def get_user_categories(user_id):
        """Get all categories available to a user (personal + global)."""
        return Category.query.filter(
            (Category.user_id == user_id) | (Category.user_id == None)
        ).order_by(Category.name).all()
    
    @staticmethod
    def create_user_categories(user_id):
        """Create personal copies of default categories for a new user."""
        default_categories = Category.query.filter_by(user_id=None).all()
        
        for default_cat in default_categories:
            user_category = Category(
                name=default_cat.name,
                icon=default_cat.icon,
                color=default_cat.color,
                user_id=user_id
            )
            db.session.add(user_category)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color,
            'user_id': self.user_id,
            'expense_count': self.get_expense_count(),
            'created_at': self.created_at.isoformat()
        }