from datetime import datetime
import random
from app import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint


# (IMPORTANT) This table is mandatory for Replit Auth, don't drop it.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    profile_image_url = db.Column(db.String, nullable=True)
    
    # User profile information
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    activity_level = db.Column(db.String(20), nullable=True)
    dietary_preferences = db.Column(db.Text, nullable=True)  # JSON string
    allergies = db.Column(db.Text, nullable=True)  # JSON string
    health_goals = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now,
                           onupdate=datetime.now)

    # Relationships
    meal_history = db.relationship('MealHistory', backref='user', lazy=True)
    user_preferences = db.relationship('UserPreference', backref='user', lazy=True)


# (IMPORTANT) This table is mandatory for Replit Auth, don't drop it.
class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String, db.ForeignKey(User.id))
    browser_session_key = db.Column(db.String, nullable=False)
    user = db.relationship(User)

    __table_args__ = (UniqueConstraint(
        'user_id',
        'browser_session_key',
        'provider',
        name='uq_user_browser_session_key_provider',
    ),)


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    fiber = db.Column(db.Float, nullable=True)
    
    # Classification fields
    age_group = db.Column(db.String(20), nullable=True)  # young, adult, senior
    gender = db.Column(db.String(10), nullable=True)  # male, female, any
    weight_category = db.Column(db.String(20), nullable=True)  # underweight, normal, overweight
    activity_level = db.Column(db.String(20), nullable=True)  # sedentary, light, moderate, active
    cost_level = db.Column(db.String(10), nullable=True)  # low, medium, high
    
    # Additional fields
    prep_time = db.Column(db.Integer, nullable=True)  # minutes
    difficulty = db.Column(db.String(10), nullable=True)  # easy, medium, hard
    cuisine_type = db.Column(db.String(50), nullable=True)
    meal_type = db.Column(db.String(20), nullable=True)  # breakfast, lunch, dinner, snack
    ingredients = db.Column(db.Text, nullable=True)  # JSON string
    instructions = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    meal_history = db.relationship('MealHistory', backref='meal', lazy=True)


class MealHistory(db.Model):
    __tablename__ = 'meal_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 stars
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    preference_type = db.Column(db.String(50), nullable=False)  # cuisine, ingredient, etc.
    preference_value = db.Column(db.String(100), nullable=False)
    preference_score = db.Column(db.Float, default=1.0)  # preference strength
    created_at = db.Column(db.DateTime, default=datetime.now)


class HealthTip(db.Model):
    __tablename__ = 'health_tips'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)  # nutrition, exercise, wellness
    target_demographic = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
