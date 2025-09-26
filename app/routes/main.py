from flask import Blueprint, render_template, redirect, url_for, session
from app.models import User, Expense, Category
from datetime import datetime
import calendar

main_bp = Blueprint('main', __name__)

def login_required(f):
    """Decorator to require login for routes."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing expense overview."""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Get current date info
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    # Get recent expenses
    recent_expenses = Expense.get_recent_expenses(user_id, limit=10)
    
    # Get monthly total
    monthly_total = user.get_monthly_total(current_year, current_month)
    
    # Get category totals for current month
    category_totals = Expense.get_category_totals(user_id, current_year, current_month)
    category_stats = category_totals  # Alias for template compatibility
    
    # Get month name
    month_name = calendar.month_name[current_month]
    current_month_year = f"{month_name} {current_year}"
    
    return render_template('dashboard.html',
                         user=user,
                         recent_expenses=recent_expenses,
                         monthly_total=monthly_total,
                         category_totals=category_totals,
                         category_stats=category_stats,
                         current_month=current_month_year)

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Get user statistics
    total_expenses = user.get_total_expenses()
    total_amount = user.get_total_amount()
    
    return render_template('profile.html',
                         user=user,
                         total_expenses=total_expenses,
                         total_amount=total_amount)