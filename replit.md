# Offensive & Abusive Content Detection Application

## Overview
A Django web application that uses spaCy NLP to detect offensive and abusive content in text. The system analyzes text input and classifies it based on categories like profanity, hate speech, threats, harassment, and toxic language.

## Project Structure
```
.
├── content_moderator/       # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI application
├── detector/                # Main detection app
│   ├── models.py            # AnalysisResult model
│   ├── views.py             # Home, history, and API views
│   ├── forms.py             # Text analysis form
│   ├── services.py          # spaCy-based detection logic
│   └── urls.py              # App URL routing
├── templates/detector/      # HTML templates
│   ├── base.html            # Base template with Bootstrap
│   ├── home.html            # Main analysis page
│   └── history.html         # Analysis history page
└── manage.py                # Django management script
```

## Key Features
- **Text Analysis**: Submit text for offensive content detection
- **Category Classification**: Detects profanity, hate speech, threats, harassment, and toxic content
- **Severity Levels**: Safe, Mild, Moderate, Severe
- **Confidence Scoring**: Percentage-based confidence in detection
- **Flagged Terms**: Highlights specific terms that triggered detection
- **History View**: Browse recent analysis results
- **API Endpoint**: POST to `/api/analyze/` for programmatic access

## Technology Stack
- **Backend**: Django 5.x, Python 3.11
- **NLP**: spaCy with en_core_web_sm model
- **Frontend**: Bootstrap 5, Django Templates
- **Database**: SQLite

## Running the Application
The application runs on port 5000:
```bash
python manage.py runserver 0.0.0.0:5000
```

## API Usage
```bash
curl -X POST -d "text=Your text here" http://localhost:5000/api/analyze/
```

## Detection Categories
- **Profanity**: Swear words and vulgar language
- **Hate Speech**: Discriminatory or hateful language
- **Threats**: Violent or threatening content
- **Harassment**: Bullying or abusive language
- **Toxic**: Generally negative or harmful content

## Recent Changes
- December 18, 2025: Initial project setup with full detection system
