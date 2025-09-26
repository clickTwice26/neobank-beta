from app import db
from datetime import datetime
from sqlalchemy import Index

class Expense(db.Model):
    """Expense model for tracking user expenses."""
    
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite indexes for better query performance
    __table_args__ = (
        Index('ix_expenses_user_date', 'user_id', 'date'),
        Index('ix_expenses_user_category', 'user_id', 'category_id'),
    )
    
    def __init__(self, user_id, category_id, amount, description=None, date=None):
        self.user_id = user_id
        self.category_id = category_id
        self.amount = float(amount)
        self.description = description
        self.date = date if date else datetime.now().date()
    
    @staticmethod
    def get_user_expenses(user_id, page=1, per_page=20, category_id=None, date_from=None, date_to=None):
        """Get paginated expenses for a user with optional filters."""
        query = Expense.query.filter_by(user_id=user_id)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if date_from:
            query = query.filter(Expense.date >= date_from)
        
        if date_to:
            query = query.filter(Expense.date <= date_to)
        
        return query.order_by(Expense.date.desc(), Expense.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def get_recent_expenses(user_id, limit=10):
        """Get recent expenses for a user."""
        return Expense.query.filter_by(user_id=user_id).order_by(
            Expense.date.desc(), Expense.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_monthly_expenses(user_id, year=None, month=None):
        """Get expenses for a specific month."""
        from sqlalchemy import extract
        
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
            
        return Expense.query.filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).order_by(Expense.date.desc()).all()
    
    @staticmethod
    def get_category_totals(user_id, year=None, month=None):
        """Get spending totals grouped by category."""
        from sqlalchemy import func, extract
        from app.models.category import Category
        
        query = db.session.query(
            Category.id,
            Category.name,
            Category.icon,
            Category.color,
            func.coalesce(func.sum(Expense.amount), 0).label('total')
        ).outerjoin(
            Expense, (Category.id == Expense.category_id) & (Expense.user_id == user_id)
        ).filter(
            (Category.user_id == user_id) | (Category.user_id == None)
        )
        
        if year:
            query = query.filter(
                (Expense.date == None) | (extract('year', Expense.date) == year)
            )
        
        if month:
            query = query.filter(
                (Expense.date == None) | (extract('month', Expense.date) == month)
            )
        
        return query.group_by(Category.id, Category.name, Category.icon, Category.color).order_by(func.sum(Expense.amount).desc()).all()
    
    @staticmethod
    def get_monthly_chart_data(user_id, months=6):
        """Get monthly spending data for charts."""
        from sqlalchemy import func, extract
        from dateutil.relativedelta import relativedelta
        
        end_date = datetime.now().date()
        start_date = end_date - relativedelta(months=months-1)
        
        # Get monthly totals
        monthly_data = db.session.query(
            extract('year', Expense.date).label('year'),
            extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by(
            extract('year', Expense.date),
            extract('month', Expense.date)
        ).order_by(
            extract('year', Expense.date),
            extract('month', Expense.date)
        ).all()
        
        return monthly_data
    
    def __repr__(self):
        return f'<Expense {self.amount} - {self.description or "No description"}>'
    
    def to_dict(self):
        """Convert expense to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'amount': float(self.amount),
            'description': self.description,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'category': self.category.to_dict() if self.category else None
        }