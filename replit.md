# NutriGuide - Personalized Meal Recommendation System

## Overview

NutriGuide is a Flask-based web application that provides personalized meal recommendations based on user profiles, dietary preferences, and nutritional needs. The application integrates with Replit's authentication system to provide secure user management and offers a responsive interface for discovering and managing meal suggestions tailored to individual health goals and dietary restrictions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with modular route organization
- **Database**: SQLAlchemy ORM with PostgreSQL (via DATABASE_URL environment variable)
- **Authentication**: Replit OAuth integration with Flask-Login for session management
- **Session Management**: Browser-based sessions with ProxyFix middleware for HTTPS support
- **Data Models**: User profiles, meal data, meal history, and OAuth tokens with proper foreign key relationships

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
- **UI Framework**: Bootstrap 5 with custom CSS for enhanced styling and animations
- **JavaScript**: Vanilla JavaScript for interactive features and AJAX functionality
- **Responsive Design**: Mobile-first approach with container-based layouts

### Data Storage Design
- **User Management**: Comprehensive user profiles including demographics, dietary preferences, allergies, and health goals
- **Meal Database**: Structured meal data with nutritional information, preparation details, and categorization
- **History Tracking**: User meal history and preferences for recommendation improvement
- **OAuth Storage**: Secure token storage linked to browser sessions and user accounts

### Authentication & Authorization
- **Primary Auth**: Replit OAuth 2.0 integration with custom storage implementation
- **Session Storage**: Database-backed OAuth token storage with browser session keys
- **User Loader**: Flask-Login integration for automatic user session management
- **Security**: ProxyFix middleware for proper HTTPS URL generation and secure sessions

### Application Structure
- **Modular Design**: Separated concerns with dedicated files for models, routes, authentication, and app configuration
- **Database Management**: Automatic table creation on startup with proper relationship mapping
- **Error Handling**: Custom error pages and logging configuration
- **Static Assets**: Organized CSS and JavaScript files with CDN integration for external libraries

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: Database ORM and connection management
- **Flask-Login**: User session management
- **Flask-Dance**: OAuth consumer implementation

### UI and Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design (CDN)
- **Font Awesome 6**: Icon library (CDN)
- **Custom CSS**: Application-specific styling with CSS variables

### Authentication Services
- **Replit OAuth**: Primary authentication provider
- **JWT**: Token handling for secure authentication flows

### Database Technology
- **PostgreSQL**: Primary database (configured via DATABASE_URL environment variable)
- **Connection Pooling**: Configured with pre-ping and connection recycling for reliability

### Development and Deployment
- **Gunicorn**: WSGI server compatibility
- **Environment Variables**: Configuration management for secrets and database connections
- **Logging**: Python logging module with debug-level configuration