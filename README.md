# 💰 Mobile Expense Tracker

A robust Flask-based expense tracking application with SQLAlchemy ORM, optimized for mobile devices. This SaaS-style platform allows users to create accounts, securely manage their expenses, and track spending patterns with an intuitive mobile-first interface.

## ✨ Features

### 🔐 User Authentication
- Secure user registration and login
- Password hashing with Werkzeug security
- Session management with Flask sessions
- User profile management

### 📱 Mobile-Optimized Design
- Responsive design using Tailwind CSS
- Touch-friendly interface optimized for mobile
- Bottom navigation for easy thumb access
- PWA (Progressive Web App) ready
- Offline-first design considerations

### 💳 Expense Management
- Add, view, edit, and delete expenses
- Categorize expenses with custom icons and colors
- Date-based expense tracking with advanced filtering
- Real-time expense calculations and summaries
- Search and filter with pagination

### 📊 Analytics & Insights
- Monthly spending overview with visual charts
- Category-wise expense breakdown
- Spending trends over time with Chart.js integration
- Progress bars and percentage calculations
- Interactive dashboard with real-time data

### 🏷️ Category Management
- Pre-defined expense categories with emoji icons
- Custom category creation with color coding
- Personal categories for each user
- Category-based filtering and reporting

### 📈 Advanced Features
- RESTful API endpoints for data access
- Database migrations with Flask-Migrate
- Proper error handling and validation
- Environment-based configuration
- Comprehensive logging and debugging

## 🏗️ Project Structure

```
neobank-beta/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── category.py         # Category model
│   │   └── expense.py          # Expense model
│   ├── routes/                  # Blueprint routes
│   │   ├── __init__.py
│   │   ├── main.py             # Main routes (dashboard, profile)
│   │   ├── auth.py             # Authentication routes
│   │   ├── expenses.py         # Expense management routes
│   │   └── api.py              # API endpoints
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html           # Base template
│   │   ├── dashboard.html      # Main dashboard
│   │   ├── login.html          # Login page
│   │   ├── register.html       # Registration page
│   │   ├── add_expense.html    # Add expense form
│   │   ├── expenses.html       # Expense list
│   │   ├── categories.html     # Category management
│   │   └── profile.html        # User profile
│   └── static/                  # Static files
│       ├── css/
│       │   └── custom.css      # Custom styles
│       └── js/
│           └── app.js          # JavaScript utilities
├── config/                      # Configuration modules
│   ├── __init__.py
│   └── config.py               # Environment configurations
├── migrations/                  # Database migrations (auto-generated)
├── venv/                       # Virtual environment
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── run.sh                     # Quick start script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd /home/raju/my-product/neobank-beta
   ```

2. **Run the setup script:**
   ```bash
   ./run.sh
   ```
   
   This will:
   - Create and activate virtual environment
   - Install required dependencies
   - Initialize the SQLite database
   - Start the Flask development server on port 5001

3. **Access the application:**
   - Open your web browser
   - Navigate to `http://localhost:5001`
   - Create a new account or login

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 run.py init-db

# Run the application
FLASK_RUN_PORT=5001 python3 run.py
```

## 📱 Mobile Experience

The application is designed mobile-first with:
- **Touch-optimized interface**: Large buttons and touch targets
- **Bottom navigation**: Easy thumb navigation on mobile devices
- **Responsive design**: Adapts seamlessly to all screen sizes
- **Fast loading**: Optimized for mobile networks and slower connections
- **PWA capability**: Install on home screen like a native app

## 🗄️ Database Schema

The application uses SQLAlchemy ORM with SQLite database:

### Tables:
- **users**: User account information with password hashing
- **categories**: Expense categories with icons, colors, and user ownership
- **expenses**: Individual expense records with relationships

### Key Features:
- Proper foreign key relationships
- Database indexes for performance
- Migration support with Flask-Migrate
- Automatic timestamp tracking

## 🛡️ Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Secure user sessions with configurable timeouts
- **Input Validation**: Comprehensive form validation and sanitization
- **SQL Injection Protection**: Using SQLAlchemy ORM with parameterized queries
- **CSRF Protection**: Ready for CSRF token implementation

## 📋 Default Categories

The app comes with pre-configured categories:
- 🍽️ Food & Dining (#EF4444)
- 🚗 Transportation (#10B981)
- 🛍️ Shopping (#8B5CF6)
- 🎬 Entertainment (#F59E0B)
- 💡 Bills & Utilities (#06B6D4)
- 🏥 Healthcare (#EC4899)
- 📚 Education (#6366F1)
- 📋 Other (#6B7280)

## 🎨 Customization

- **Categories**: Add unlimited custom categories with emoji icons and colors
- **Themes**: Built-in color schemes with dark mode support
- **Mobile UI**: Optimized for touch interactions and mobile devices
- **Responsive Design**: Adapts to tablets, phones, and desktop screens

## 🔧 Technical Stack

- **Backend**: Flask 2.3.3 with application factory pattern
- **ORM**: SQLAlchemy 2.0+ with Flask-SQLAlchemy
- **Database**: SQLite (easily replaceable with PostgreSQL/MySQL)
- **Frontend**: HTML5, Tailwind CSS 3.x, Alpine.js
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6.0+ icons
- **Authentication**: Flask sessions with Werkzeug security
- **Migration**: Flask-Migrate for database versioning

## 📊 API Endpoints

The application provides RESTful API endpoints:

- `GET /api/monthly-chart` - Monthly spending chart data
- `GET /api/expense-summary` - Expense summary statistics
- `GET /api/recent-expenses` - Recent expenses list
- `GET /api/health` - Health check endpoint

## 🚀 Production Deployment

For production deployment:

1. **Environment Configuration:**
   ```bash
   export FLASK_CONFIG=production
   export SECRET_KEY=your-secret-key-here
   export DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

2. **Use Production WSGI Server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **Database Migration:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Web Server Configuration:** Use nginx or Apache as reverse proxy

## 📱 PWA Features

The application supports Progressive Web App features:
- Install prompt for mobile devices
- Offline functionality (planned)
- App-like experience when installed
- Custom splash screen and icons

## 🔄 Data Management

- **Database Migrations**: Automatic schema versioning
- **Data Export**: CSV export functionality (extensible)
- **Backup**: SQLite database file for easy backups
- **Data Validation**: Client and server-side validation

## 🧪 Development Features

- **Hot Reload**: Development server with auto-reload
- **Debug Mode**: Comprehensive error pages and debugging
- **Logging**: SQLAlchemy query logging in development
- **Environment Variables**: Configuration through environment files

## 🎯 Perfect For

- **Personal Finance Tracking**: Individual expense management
- **Small Business**: Simple business expense tracking
- **Budget Planning**: Monthly and category-based budgeting
- **Financial Awareness**: Understanding spending patterns
- **Mobile Users**: Optimized for smartphone usage

## 📞 Support & Contributing

The application is designed to be self-contained and easy to extend. The modular structure makes it simple to:
- Add new expense categories
- Implement additional reporting features
- Integrate with external APIs
- Add new authentication methods

---

**Built with ❤️ using Flask, SQLAlchemy, Tailwind CSS, and modern web technologies for the best mobile expense tracking experience.**