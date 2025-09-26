from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Category, Expense
from app.routes.main import login_required
from datetime import datetime, date

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add a new expense."""
    if request.method == 'POST':
        try:
            category_id = request.form.get('category_id')
            amount = request.form.get('amount')
            description = request.form.get('description', '').strip()
            date_str = request.form.get('date')
            
            # Validation
            if not category_id or not amount or not date_str:
                flash('Please fill in all required fields!', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            # Validate amount
            try:
                amount = float(amount)
                if amount <= 0:
                    flash('Amount must be greater than 0!', 'error')
                    return redirect(url_for('expenses.add_expense'))
            except ValueError:
                flash('Invalid amount!', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            # Validate date
            try:
                expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date!', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            # Validate category belongs to user
            category = Category.query.filter(
                Category.id == category_id,
                (Category.user_id == session['user_id']) | (Category.user_id == None)
            ).first()
            
            if not category:
                flash('Invalid category!', 'error')
                return redirect(url_for('expenses.add_expense'))
            
            # Create expense
            expense = Expense(
                user_id=session['user_id'],
                category_id=category_id,
                amount=amount,
                description=description if description else None,
                date=expense_date
            )
            
            db.session.add(expense)
            db.session.commit()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the expense. Please try again.', 'error')
            return redirect(url_for('expenses.add_expense'))
    
    # GET request - show form
    categories = Category.get_user_categories(session['user_id'])
    categories_data = [{'id': c.id, 'name': c.name, 'icon': c.icon, 'color': c.color} for c in categories]
    today = date.today().strftime('%Y-%m-%d')
    
    return render_template('add_expense.html', 
                         categories=categories_data, 
                         today=today)

@expenses_bp.route('/list')
@login_required
def list_expenses():
    """List all expenses with filtering and pagination."""
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Convert date strings to date objects
    date_from_obj = None
    date_to_obj = None
    
    try:
        if date_from:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        if date_to:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format!', 'error')
    
    # Get expenses with filters
    expenses_pagination = Expense.get_user_expenses(
        user_id=session['user_id'],
        page=page,
        per_page=20,
        category_id=int(category_filter) if category_filter else None,
        date_from=date_from_obj,
        date_to=date_to_obj
    )
    
    # Get categories for filter dropdown
    categories = Category.get_user_categories(session['user_id'])
    
    return render_template('expenses.html',
                         expenses=expenses_pagination.items,
                         pagination=expenses_pagination,
                         categories=categories,
                         category_filter=category_filter,
                         date_from=date_from,
                         date_to=date_to)

@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        expense = Expense.query.filter_by(
            id=expense_id, 
            user_id=session['user_id']
        ).first()
        
        if not expense:
            flash('Expense not found!', 'error')
        else:
            db.session.delete(expense)
            db.session.commit()
            flash('Expense deleted successfully!', 'success')
            
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the expense.', 'error')
    
    return redirect(request.referrer or url_for('main.dashboard'))

@expenses_bp.route('/categories')
@login_required
def categories():
    """Manage expense categories."""
    user_categories = Category.query.filter_by(user_id=session['user_id']).order_by(Category.name).all()
    
    return render_template('categories.html', categories=user_categories)

@expenses_bp.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    """Add a new category."""
    try:
        name = request.form.get('name', '').strip()
        icon = request.form.get('icon', '📋').strip()
        color = request.form.get('color', '#6B7280').strip()
        
        if not name:
            flash('Category name is required!', 'error')
            return redirect(url_for('expenses.categories'))
        
        if len(name) < 2:
            flash('Category name must be at least 2 characters long!', 'error')
            return redirect(url_for('expenses.categories'))
        
        # Check if category name already exists for this user
        existing = Category.query.filter_by(
            name=name, 
            user_id=session['user_id']
        ).first()
        
        if existing:
            flash('Category with this name already exists!', 'error')
            return redirect(url_for('expenses.categories'))
        
        # Create new category
        category = Category(
            name=name,
            icon=icon,
            color=color,
            user_id=session['user_id']
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the category.', 'error')
    
    return redirect(url_for('expenses.categories'))