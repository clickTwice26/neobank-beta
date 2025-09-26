from flask import Blueprint, jsonify, session, request
from app.models import User, Expense
from app.routes.main import login_required
from datetime import datetime
import calendar

api_bp = Blueprint('api', __name__)

@api_bp.route('/monthly-chart')
@login_required
def monthly_chart():
    """API endpoint for monthly spending chart data."""
    try:
        user_id = session['user_id']
        
        # Get monthly data for the last 6 months
        monthly_data = Expense.get_monthly_chart_data(user_id, months=6)
        
        months = []
        amounts = []
        
        # Convert the data to the format expected by Chart.js
        for data_point in monthly_data:
            year = int(data_point.year)
            month = int(data_point.month)
            amount = float(data_point.total)
            
            # Format month name
            month_name = calendar.month_abbr[month]
            month_year = f"{month_name} {year}"
            
            months.append(month_year)
            amounts.append(amount)
        
        return jsonify({
            'months': months,
            'amounts': amounts,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to load chart data',
            'success': False
        }), 500

@api_bp.route('/expense-summary')
@login_required
def expense_summary():
    """API endpoint for expense summary data."""
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'success': False
            }), 404
        
        # Get current month data
        now = datetime.now()
        monthly_total = user.get_monthly_total(now.year, now.month)
        total_expenses = user.get_total_expenses()
        total_amount = user.get_total_amount()
        
        # Get category totals for current month
        category_totals = Expense.get_category_totals(user_id, now.year, now.month)
        
        # Format category data
        categories = []
        for cat in category_totals:
            if cat.total > 0:  # Only include categories with expenses
                percentage = (float(cat.total) / float(monthly_total) * 100) if monthly_total > 0 else 0
                categories.append({
                    'id': cat.id,
                    'name': cat.name,
                    'icon': cat.icon,
                    'color': cat.color,
                    'total': float(cat.total),
                    'percentage': round(percentage, 1)
                })
        
        return jsonify({
            'monthly_total': float(monthly_total),
            'total_expenses': total_expenses,
            'total_amount': float(total_amount),
            'categories': categories,
            'month': calendar.month_name[now.month],
            'year': now.year,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to load expense summary',
            'success': False
        }), 500

@api_bp.route('/recent-expenses')
@login_required
def recent_expenses():
    """API endpoint for recent expenses."""
    try:
        user_id = session['user_id']
        limit = request.args.get('limit', 10, type=int)
        
        expenses = Expense.get_recent_expenses(user_id, limit=limit)
        
        expenses_data = []
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'amount': float(expense.amount),
                'description': expense.description,
                'date': expense.date.isoformat(),
                'category': {
                    'name': expense.category.name,
                    'icon': expense.category.icon,
                    'color': expense.category.color
                } if expense.category else None
            })
        
        return jsonify({
            'expenses': expenses_data,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to load recent expenses',
            'success': False
        }), 500

@api_bp.route('/health')
def health_check():
    """API health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })