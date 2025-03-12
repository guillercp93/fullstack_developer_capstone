# Car Dealership Review System

A full-stack web application for managing car dealership reviews with sentiment analysis capabilities. Built with Django and React.

## Features

- **Dealer Management**: Browse and search car dealerships
- **Review System**: Post and view dealer reviews with sentiment analysis
- **Car Catalog**: Comprehensive database of car makes and models (2015-2025)
- **User Authentication**: Secure login and registration system
- **Sentiment Analysis**: AI-powered review sentiment analysis using IBM Cloud
- **Responsive Design**: Bootstrap-based UI for optimal viewing on all devices

## Core Features

### Car Models
The application includes a comprehensive car database with the following models:

1. **CarMake Model**:
   - Name: Manufacturer name
   - Description: Company details
   - Website: Official website URL
   - Founded Year: Company establishment date
   - Auto-populated with 5 major manufacturers:
     - Toyota
     - Honda
     - Ford
     - BMW
     - Tesla

2. **CarModel**:
   - Type: SEDAN, SUV, or WAGON
   - Year: Valid range 2015-2025
   - Maker: Relationship to CarMake
   - Each manufacturer comes with 3 popular models
   - Automatic data population on first run
   - Duplicate prevention using get_or_create

### Review System
1. **Dealer Reviews**:
   - Submit reviews for dealerships
   - Include car details (make, model, year)
   - Specify car type (SEDAN/SUV/WAGON)
   - Add purchase date
   - Automatic sentiment analysis via IBM Cloud

2. **Admin Interface**:
   - Enhanced with inline editing
   - CarModels can be edited within CarMake view
   - Advanced filtering and search
   - Customized display fields
   - Sorting capabilities

### Database Schema
```
CarMake
├── name (CharField)
├── description (TextField)
├── website (URLField)
└── founded_year (IntegerField)

CarModel
├── car_type (CharField: SEDAN/SUV/WAGON)
├── year (IntegerField: 2015-2025)
└── maker (ForeignKey -> CarMake)
```

## Models and Data Structure

### Car Models

1. **CarMake Model**
```python
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    founded_year = models.IntegerField()

    class Meta:
        ordering = ['name']
```

2. **CarModel**
```python
class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    
    maker = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2025)
        ]
    )
```

### Admin Interface Features

1. **CarMake Admin**
```python
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'founded_year']
    search_fields = ['name', 'description']
    list_filter = ['founded_year']
    inlines = [CarModelInline]
```

2. **CarModel Inline**
```python
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
```

### Initial Data Population
```python
# Sample data structure
MANUFACTURERS = [
    {
        'name': 'Toyota',
        'description': 'Japanese automotive manufacturer',
        'website': 'https://www.toyota.com',
        'founded_year': 1937,
        'models': [
            {'name': 'Camry', 'type': 'SEDAN', 'year': 2023},
            {'name': 'RAV4', 'type': 'SUV', 'year': 2023},
            {'name': 'Sienna', 'type': 'WAGON', 'year': 2023},
        ]
    },
    # Similar data for Honda, Ford, BMW, Tesla
]

# Population using get_or_create
for manufacturer in MANUFACTURERS:
    make, created = CarMake.objects.get_or_create(
        name=manufacturer['name'],
        defaults={
            'description': manufacturer['description'],
            'website': manufacturer['website'],
            'founded_year': manufacturer['founded_year']
        }
    )
    
    for model in manufacturer['models']:
        CarModel.objects.get_or_create(
            maker=make,
            name=model['name'],
            defaults={
                'car_type': model['type'],
                'year': model['year']
            }
        )
```

### API Endpoints

1. **Get Cars Endpoint**
```python
@api_view(['GET'])
def get_cars(request):
    """
    Returns comprehensive car information including:
    - Car make details (name, description, website)
    - Associated models with type and year
    Auto-populates data if database is empty
    """
    makes = CarMake.objects.prefetch_related('carmodel_set').all()
    if not makes.exists():
        populate_database()  # Auto-populate if empty
        makes = CarMake.objects.prefetch_related('carmodel_set').all()
    
    return JsonResponse({
        'status': 200,
        'cars': [
            {
                'make': make.name,
                'description': make.description,
                'website': make.website,
                'founded_year': make.founded_year,
                'models': [
                    {
                        'name': model.name,
                        'type': model.car_type,
                        'year': model.year
                    } for model in make.carmodel_set.all()
                ]
            } for make in makes
        ]
    })
```

### Sentiment Analysis Integration

### Overview
The application uses IBM Cloud Code Engine for sentiment analysis of dealer reviews. The service analyzes review text and classifies the sentiment as positive, negative, or neutral.

### Configuration
```bash
# Environment Variables
sentiment_analyzer_url=https://sentianalyzer.1sy733gtat71.us-south.codeengine.appdomain.cloud

# Example API Call
curl -X POST \
  $sentiment_analyzer_url/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Great service and friendly staff"}'
```

### Review System Integration

1. **Frontend Review Form**
```jsx
// PostReview.jsx
const PostReview = () => {
  const [formData, setFormData] = useState({
    name: '',
    review: '',
    car_type: 'SEDAN',
    car_year: new Date().getFullYear(),
    purchase_date: ''
  });

  // Form validation
  const validateForm = () => {
    // Year range: 2015-2025
    const validYear = formData.car_year >= 2015 && formData.car_year <= 2025;
    // Car type validation
    const validType = ['SEDAN', 'SUV', 'WAGON'].includes(formData.car_type);
    return validYear && validType && formData.review.trim() !== '';
  };

  // Submit handler with sentiment analysis
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    const response = await fetch('/djangoapp/add_review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    // Handle response...
  };
}
```

2. **Backend Review Processing**
```python
# views.py
@api_view(['POST'])
def add_review(request):
    """Process new dealer review with sentiment analysis"""
    review_text = request.data.get('review')
    
    # Get sentiment from IBM Cloud
    sentiment_response = requests.post(
        f"{settings.SENTIMENT_ANALYZER_URL}/analyze",
        json={"text": review_text}
    )
    sentiment = sentiment_response.json().get('sentiment', 'neutral')
    
    # Save review with sentiment
    review = Review.objects.create(
        dealer_id=request.data.get('dealership'),
        name=request.data.get('name'),
        review=review_text,
        car_make=request.data.get('car_make'),
        car_model=request.data.get('car_model'),
        car_year=request.data.get('car_year'),
        purchase_date=request.data.get('purchase_date'),
        sentiment=sentiment
    )
    
    return JsonResponse({
        'status': 'success',
        'id': review.id,
        'sentiment': sentiment
    })
```

### Review Display

1. **Sentiment Icons**
```jsx
// Dealer.jsx
const senti_icon = (sentiment) => {
  const icons = {
    'positive': positive_icon,
    'negative': negative_icon,
    'neutral': neutral_icon
  };
  return icons[sentiment] || neutral_icon;
};

// Review card with sentiment icon
<div className="card shadow-sm review_panel">
  <img 
    src={senti_icon(review.sentiment)} 
    className="emotion_icon position-absolute" 
    alt='Sentiment'
  />
  <div className="review card-body">
    <p className="card-text">{review.review}</p>
    <div className="reviewer text-muted">
      {review.name} - {review.car_make} {review.car_model} {review.car_year}
    </div>
  </div>
</div>
```

2. **Review Filtering**
```python
# views.py
@api_view(['GET'])
def get_reviews(request, dealer_id):
    """Get dealer reviews with optional sentiment filtering"""
    sentiment = request.GET.get('sentiment')
    reviews = Review.objects.filter(dealer_id=dealer_id)
    
    if sentiment:
        reviews = reviews.filter(sentiment=sentiment)
    
    return JsonResponse({
        'status': 200,
        'reviews': [
            {
                'id': review.id,
                'name': review.name,
                'review': review.review,
                'sentiment': review.sentiment,
                'car_make': review.car_make,
                'car_model': review.car_model,
                'car_year': review.car_year,
                'purchase_date': review.purchase_date
            } for review in reviews
        ]
    })
```

### Error Handling

1. **Sentiment Analysis Errors**
```python
def get_sentiment(text):
    """Get sentiment with error handling"""
    try:
        response = requests.post(
            f"{settings.SENTIMENT_ANALYZER_URL}/analyze",
            json={"text": text},
            timeout=5  # 5 seconds timeout
        )
        response.raise_for_status()
        return response.json().get('sentiment', 'neutral')
    except requests.RequestException:
        # Log error and return neutral as fallback
        logger.error("Sentiment analysis service error")
        return 'neutral'
```

2. **Review Validation**
```python
def validate_review(data):
    """Validate review data"""
    errors = []
    
    # Validate car year
    try:
        year = int(data.get('car_year', 0))
        if not (2015 <= year <= 2025):
            errors.append("Car year must be between 2015 and 2025")
    except ValueError:
        errors.append("Invalid car year")
    
    # Validate car type
    if data.get('car_type') not in ['SEDAN', 'SUV', 'WAGON']:
        errors.append("Invalid car type")
    
    # Validate review text
    if not data.get('review', '').strip():
        errors.append("Review text is required")
    
    return errors
```

## API Documentation

### Authentication Endpoints
```bash
# User authentication
POST   /djangoapp/login            # User login
POST   /djangoapp/register         # User registration
POST   /djangoapp/logout           # User logout
```

### Dealer Endpoints
```bash
# Dealer operations
GET    /djangoapp/get_dealers      # List all dealers
GET    /djangoapp/get_dealer/:id   # Get specific dealer details
POST   /djangoapp/add_review       # Submit a dealer review
```

### Car Endpoints
```bash
# Car operations
GET    /djangoapp/get_cars         # List all car makes and models
```

### Request/Response Examples

1. **Get Cars**
```bash
GET /djangoapp/get_cars

Response:
{
  "cars": [
    {
      "make": "Toyota",
      "description": "Japanese automotive manufacturer",
      "website": "https://www.toyota.com",
      "founded_year": 1937,
      "models": [
        {
          "type": "SEDAN",
          "year": 2023,
          "name": "Camry"
        }
      ]
    }
  ]
}
```

2. **Add Review**
```bash
POST /djangoapp/add_review

Request:
{
  "dealership": 1,
  "name": "John Doe",
  "review": "Great service and friendly staff",
  "car_type": "SEDAN",
  "car_year": 2023,
  "purchase_date": "2023-12-01"
}

Response:
{
  "id": 1,
  "sentiment": "positive",
  "status": "success"
}
```

### Error Handling
All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request (invalid input)
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

Error responses include a message field:
```json
{
  "status": "error",
  "message": "Detailed error description"
}
```

## Quick Start Guide

1. **Clone and Setup**:
```bash
# Clone repository
git clone <repository-url>
cd finalProjectCertificate

# Create and activate virtual environment
cd server
python -m venv djangoenv
source djangoenv/bin/activate  # On Windows: djangoenv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

2. **Configure Environment**:
```bash
# Create .env file in server/djangoapp/
echo "backend_url=http://localhost:3030" > server/djangoapp/.env
echo "sentiment_analyzer_url=https://sentianalyzer.1sy733gtat71.us-south.codeengine.appdomain.cloud" >> server/djangoapp/.env
```

3. **Initialize Database**:
```bash
# From the server directory
cd server

# Apply migrations
python manage.py makemigrations djangoapp
python manage.py migrate

# Load initial car data (includes 5 manufacturers with 3 models each)
python manage.py shell < djangoapp/populate.py
```

4. **Run the Application**:
```bash
# Terminal 1 - Run Django Backend
cd server
source djangoenv/bin/activate  # On Windows: djangoenv\Scripts\activate
python manage.py runserver

# Terminal 2 - Run React Frontend
cd frontend
npm start
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure
```
server/
├── database/           # Database configuration
├── djangoapp/          # Main Django application
│   ├── models.py       # Car and dealer models
│   ├── views.py        # View logic
│   ├── urls.py         # URL routing
│   ├── restapis.py     # REST API endpoints
│   ├── populate.py     # Initial data population
│   └── microservices/  # Sentiment analysis integration
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dealers/    # Dealer management
│   │   │   ├── Header/     # Navigation
│   │   │   ├── Login/      # Authentication
│   │   │   └── Register/   # User registration
│   │   ├── App.jsx         # Main component
│   │   └── index.jsx       # Entry point
│   └── package.json        # Frontend dependencies
└── requirements.txt        # Python dependencies
```

## Command Reference

### Project Setup
```bash
# Clone and setup
git clone <repository-url>
cd finalProjectCertificate

# Backend setup
cd server
python -m venv djangoenv
source djangoenv/bin/activate  # On Windows: djangoenv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### Database Commands
```bash
# Initialize database
python manage.py makemigrations djangoapp
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py shell < djangoapp/populate.py

# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py shell < djangoapp/populate.py
```

### Development Servers
```bash
# Run Django backend (from server directory)
source djangoenv/bin/activate
python manage.py runserver

# Run React frontend (from frontend directory)
npm start

# Run on different ports
python manage.py runserver 8001  # Backend
PORT=3001 npm start             # Frontend
```

### Testing Commands
```bash
# Backend tests
cd server
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Production Commands
```bash
# Backend
python manage.py collectstatic
export DJANGO_SETTINGS_MODULE=djangoproj.settings_prod
gunicorn djangoproj.wsgi:application

# Frontend
npm run build
```

### IBM Cloud Commands
```bash
# Login to IBM Cloud
ibmcloud login

# Target resource group
ibmcloud target -g <resource-group-name>

# View resource groups
ibmcloud resource groups
```

### Maintenance Commands
```bash
# Clean frontend build
cd frontend
rm -rf build/
rm -rf node_modules/
npm install

# Reset virtual environment
cd server
deactivate
rm -rf djangoenv/
python -m venv djangoenv
source djangoenv/bin/activate
pip install -r requirements.txt
```

## Database Management

1. **Reset and Reload Data**
```bash
# Clear existing data
python manage.py shell
>>> from djangoapp.models import CarMake, CarModel
>>> CarModel.objects.all().delete()
>>> CarMake.objects.all().delete()

# Reload initial data (includes 5 manufacturers with 3 models each)
python manage.py shell < djangoapp/populate.py
```

2. **Verify Data Population**
```bash
python manage.py shell
>>> from djangoapp.models import CarMake, CarModel
>>> CarMake.objects.count()  # Should return 5 (Toyota, Honda, Ford, BMW, Tesla)
>>> CarMake.objects.first().carmodel_set.count()  # Should return 3 models per manufacturer
```

3. **Manage Car Data**
```bash
python manage.py shell
# Add new manufacturer
>>> CarMake.objects.get_or_create(
...     name='Mercedes-Benz',
...     defaults={
...         'description': 'German luxury automobile manufacturer',
...         'website': 'https://www.mercedes-benz.com',
...         'founded_year': 1926
...     }
... )

# Add model to manufacturer
>>> mercedes = CarMake.objects.get(name='Mercedes-Benz')
>>> CarModel.objects.create(
...     maker=mercedes,
...     name='E-Class',
...     car_type='SEDAN',
...     year=2023
... )

# List all sedans from 2023
>>> CarModel.objects.filter(car_type='SEDAN', year=2023)

# Get manufacturer details
>>> CarMake.objects.values('name', 'founded_year')
```

4. **Export/Import Data**
```bash
# Export car data to JSON
python manage.py dumpdata djangoapp.CarMake djangoapp.CarModel > car_data.json

# Import car data from JSON
python manage.py loaddata car_data.json
```

5. **Database Maintenance**
```bash
# Check database consistency
python manage.py check

# Show all SQL migrations
python manage.py sqlmigrate djangoapp 0001

# Reset migrations
python manage.py migrate djangoapp zero
python manage.py migrate djangoapp
```

## Troubleshooting

1. **Database Issues**:
```bash
# Reset database
rm server/db.sqlite3
python manage.py makemigrations djangoapp
python manage.py migrate
python manage.py shell < djangoapp/populate.py
```

2. **Node Modules Issues**:
```bash
# Clean install
rm -rf frontend/node_modules
rm frontend/package-lock.json
npm install
```

3. **Virtual Environment Issues**:
```bash
# Recreate environment
deactivate
rm -rf server/djangoenv
python -m venv djangoenv
source djangoenv/bin/activate
pip install -r requirements.txt
```

4. **IBM Cloud Connection Issues**:
```bash
# Verify IBM Cloud login
ibmcloud login

# Check resource group
ibmcloud resource groups

# Target specific group
ibmcloud target -g <resource-group-name>

# Verify sentiment analyzer URL in .env
cat server/djangoapp/.env
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.