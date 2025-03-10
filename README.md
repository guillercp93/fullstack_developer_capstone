# Full Stack Developer Capstone Project

This is a Django-based web application with a React frontend.

## Project Structure

The project follows a standard Django application structure with a React frontend:

```
server/
├── database/        # Database-related files
├── djangoapp/       # Django application folder
├── djangoproj/      # Django project configuration
├── frontend/        # React frontend application
├── manage.py        # Django management script
├── package.json     # Project dependencies
└── requirements.txt # Python dependencies
```

## Technology Stack

- Backend: Django (Python web framework)
- Frontend: React.js
- Database: PostgreSQL
- API: Django REST Framework

### Python Dependencies
- Django: Web framework
- Requests: HTTP library
- Pillow: Image processing
- Gunicorn: WSGI HTTP Server
- python-dotenv: Environment variable management

### Frontend Dependencies
- React 18.2.0: JavaScript library for building user interfaces
- React Router DOM 6.19.0: Routing library for React
- React Scripts 5.0.1: Development and build scripts
- Testing Libraries: Jest DOM, React Testing Library
- Web Vitals: Performance monitoring

## Getting Started

### Prerequisites
- Python 3.x
- Node.js and npm
- PostgreSQL

### Installation
1. Install Python dependencies:
```bash
cd server
pip install -U -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

### Development
- Start the frontend development server:
```bash
cd frontend
npm start
```

- Start the Django development server:
```bash
cd server
python manage.py runserver
```

More detailed setup and running instructions will be added as development progresses.