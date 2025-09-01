import json
import random
from flask import session, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from app import app, db
from replit_auth import require_login, make_replit_blueprint
from models import User, Meal, MealHistory, UserPreference, HealthTip

app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")


# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True


def init_sample_data():
    """Initialize sample meal data if database is empty"""
    if Meal.query.count() == 0:
        # Sample meals with various categories
        sample_meals = [
            {
                'name': 'Mediterranean Quinoa Bowl',
                'description': 'A nutritious bowl with quinoa, chickpeas, vegetables, and tahini dressing',
                'calories': 420,
                'protein': 15.0,
                'carbs': 65.0,
                'fat': 12.0,
                'fiber': 8.0,
                'age_group': 'adult',
                'gender': 'any',
                'weight_category': 'normal',
                'activity_level': 'moderate',
                'cost_level': 'medium',
                'prep_time': 25,
                'difficulty': 'easy',
                'cuisine_type': 'Mediterranean',
                'meal_type': 'lunch',
                'ingredients': json.dumps(['quinoa', 'chickpeas', 'cucumber', 'tomatoes', 'olives', 'tahini']),
                'instructions': 'Cook quinoa, combine with vegetables and chickpeas, dress with tahini sauce.',
                'image_url': 'https://pixabay.com/get/gc485ff69141098792001670aa8908a669e8c41416c662a8f34401e4f3567107b4b1096d3b5e370808f42b293470c93524508e369be9382b9eac57e0ea1f3d58f_1280.jpg'
            },
            {
                'name': 'Grilled Salmon with Sweet Potato',
                'description': 'Omega-3 rich salmon with roasted sweet potato and steamed broccoli',
                'calories': 380,
                'protein': 25.0,
                'carbs': 35.0,
                'fat': 15.0,
                'fiber': 6.0,
                'age_group': 'adult',
                'gender': 'any',
                'weight_category': 'normal',
                'activity_level': 'active',
                'cost_level': 'high',
                'prep_time': 30,
                'difficulty': 'medium',
                'cuisine_type': 'American',
                'meal_type': 'dinner',
                'ingredients': json.dumps(['salmon', 'sweet potato', 'broccoli', 'olive oil', 'herbs']),
                'instructions': 'Grill salmon, roast sweet potato, steam broccoli, serve together.',
                'image_url': 'https://pixabay.com/get/g008e64fac11596f34500b8dc58b558b4d164cff417ac1d435b00f902f314679c1c2a5e0f2ea0174ecfc3c884f56d038a6443ed0385d915895af3504c54bbf6c0_1280.jpg'
            },
            {
                'name': 'Avocado Toast with Eggs',
                'description': 'Whole grain toast topped with mashed avocado and poached eggs',
                'calories': 320,
                'protein': 14.0,
                'carbs': 28.0,
                'fat': 18.0,
                'fiber': 10.0,
                'age_group': 'young',
                'gender': 'any',
                'weight_category': 'underweight',
                'activity_level': 'light',
                'cost_level': 'medium',
                'prep_time': 15,
                'difficulty': 'easy',
                'cuisine_type': 'Modern',
                'meal_type': 'breakfast',
                'ingredients': json.dumps(['whole grain bread', 'avocado', 'eggs', 'lemon', 'salt', 'pepper']),
                'instructions': 'Toast bread, mash avocado with seasonings, poach eggs, assemble.',
                'image_url': 'https://pixabay.com/get/g9bc1c67b627f6d7a7fe8d30af048b1b84d00854fe214b2c7f6e90adad223d3cce6a981ad03d48dee4227ffbd3b90933589c43b1d80802f423317f305f8e49d13_1280.jpg'
            },
            {
                'name': 'Lentil Vegetable Soup',
                'description': 'Hearty soup with red lentils, carrots, celery, and spices',
                'calories': 280,
                'protein': 18.0,
                'carbs': 45.0,
                'fat': 3.0,
                'fiber': 12.0,
                'age_group': 'senior',
                'gender': 'any',
                'weight_category': 'overweight',
                'activity_level': 'sedentary',
                'cost_level': 'low',
                'prep_time': 45,
                'difficulty': 'easy',
                'cuisine_type': 'Indian',
                'meal_type': 'dinner',
                'ingredients': json.dumps(['red lentils', 'carrots', 'celery', 'onions', 'garlic', 'spices']),
                'instructions': 'Sauté vegetables, add lentils and broth, simmer until tender.',
                'image_url': 'https://pixabay.com/get/g4196686dc7f9d9dac565724fcccd6504372c00d1245a9da6f40723a60cbfb2b7c84e495555b377c13fede39219e3578c953e508daa9f12d1f086179133a17169_1280.jpg'
            },
            {
                'name': 'Greek Yogurt Berry Parfait',
                'description': 'Layered parfait with Greek yogurt, mixed berries, and granola',
                'calories': 250,
                'protein': 20.0,
                'carbs': 35.0,
                'fat': 6.0,
                'fiber': 5.0,
                'age_group': 'young',
                'gender': 'female',
                'weight_category': 'normal',
                'activity_level': 'moderate',
                'cost_level': 'medium',
                'prep_time': 5,
                'difficulty': 'easy',
                'cuisine_type': 'Greek',
                'meal_type': 'breakfast',
                'ingredients': json.dumps(['Greek yogurt', 'mixed berries', 'granola', 'honey']),
                'instructions': 'Layer yogurt, berries, and granola in a glass or bowl.',
                'image_url': 'https://pixabay.com/get/gda5b6fcc1e5201bd24cb92571c7bb063c6c0b65e817fd4e8177df00bbc398809d7085a3c858dad01ba370e68853bfdeb84d3c25425ca87114327d6284fc64211_1280.jpg'
            },
            {
                'name': 'Chicken Stir Fry',
                'description': 'Quick and healthy stir fry with chicken breast and mixed vegetables',
                'calories': 350,
                'protein': 28.0,
                'carbs': 25.0,
                'fat': 12.0,
                'fiber': 4.0,
                'age_group': 'adult',
                'gender': 'male',
                'weight_category': 'normal',
                'activity_level': 'active',
                'cost_level': 'medium',
                'prep_time': 20,
                'difficulty': 'medium',
                'cuisine_type': 'Asian',
                'meal_type': 'dinner',
                'ingredients': json.dumps(['chicken breast', 'bell peppers', 'broccoli', 'carrots', 'soy sauce', 'ginger']),
                'instructions': 'Cut chicken and vegetables, stir fry in wok with seasonings.',
                'image_url': 'https://pixabay.com/get/g8e6fa1b44609075f4a6ca63e098a141f95759229602d04e8f8b88962aa10203f9f9f64656f060cdb42133a2d49ccfab56f29f60821fbbd097b0441be35aeb903_1280.jpg'
            }
        ]
        
        for meal_data in sample_meals:
            meal = Meal(**meal_data)
            db.session.add(meal)
        
        # Sample health tips
        sample_tips = [
            {
                'title': 'Stay Hydrated',
                'content': 'Drink at least 8 glasses of water daily to maintain optimal health and support your metabolism.',
                'category': 'nutrition',
                'target_demographic': 'all'
            },
            {
                'title': 'Eat the Rainbow',
                'content': 'Include colorful fruits and vegetables in your diet to ensure you get a variety of vitamins and antioxidants.',
                'category': 'nutrition',
                'target_demographic': 'all'
            },
            {
                'title': 'Portion Control',
                'content': 'Use smaller plates and bowls to help control portion sizes and prevent overeating.',
                'category': 'nutrition',
                'target_demographic': 'weight_loss'
            }
        ]
        
        for tip_data in sample_tips:
            tip = HealthTip(**tip_data)
            db.session.add(tip)
        
        db.session.commit()


@app.route('/')
def index():
    """Landing page for logged out users, home page for logged in users"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('landing.html')


@app.route('/home')
@require_login
def home():
    """Home page for authenticated users"""
    init_sample_data()  # Initialize sample data if needed
    
    # Get user's recent meal history
    recent_meals = db.session.query(MealHistory, Meal).join(Meal).filter(
        MealHistory.user_id == current_user.id
    ).order_by(MealHistory.created_at.desc()).limit(3).all()
    
    # Get a random health tip
    health_tip = HealthTip.query.filter_by(is_active=True).order_by(db.func.random()).first()
    
    return render_template('home.html', recent_meals=recent_meals, health_tip=health_tip)


@app.route('/profile', methods=['GET', 'POST'])
@require_login
def profile():
    """User profile page with form to update preferences"""
    if request.method == 'POST':
        # Update user profile
        current_user.age = request.form.get('age', type=int)
        current_user.weight = request.form.get('weight', type=float)
        current_user.height = request.form.get('height', type=float)
        current_user.gender = request.form.get('gender')
        current_user.activity_level = request.form.get('activity_level')
        current_user.health_goals = request.form.get('health_goals')
        
        # Handle dietary preferences and allergies
        dietary_preferences = request.form.getlist('dietary_preferences')
        current_user.dietary_preferences = json.dumps(dietary_preferences)
        
        allergies = request.form.get('allergies', '').split(',')
        allergies = [allergy.strip() for allergy in allergies if allergy.strip()]
        current_user.allergies = json.dumps(allergies)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Parse existing preferences
    dietary_preferences = []
    allergies_list = []
    
    if current_user.dietary_preferences:
        try:
            dietary_preferences = json.loads(current_user.dietary_preferences)
        except json.JSONDecodeError:
            pass
    
    if current_user.allergies:
        try:
            allergies_list = json.loads(current_user.allergies)
        except json.JSONDecodeError:
            pass
    
    return render_template('profile.html', 
                         dietary_preferences=dietary_preferences,
                         allergies_list=allergies_list)


@app.route('/recommendations')
@require_login
def recommendations():
    """Main recommendations page"""
    return render_template('recommendations.html')


@app.route('/api/recommend', methods=['POST'])
@require_login
def api_recommend():
    """API endpoint for meal recommendations"""
    try:
        # Get user preferences or use defaults
        age = current_user.age or 25
        weight = current_user.weight or 70
        gender = current_user.gender or 'any'
        activity_level = current_user.activity_level or 'moderate'
        
        # Classify user into categories
        if age < 25:
            age_group = 'young'
        elif age >= 65:
            age_group = 'senior'
        else:
            age_group = 'adult'
        
        # Weight category classification (simplified BMI logic)
        height = current_user.height or 1.7  # default height in meters
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            weight_category = 'underweight'
        elif bmi > 25:
            weight_category = 'overweight'
        else:
            weight_category = 'normal'
        
        # Build query for meal recommendations
        query = Meal.query
        
        # Apply filters based on user profile
        query = query.filter(
            (Meal.age_group == age_group) | (Meal.age_group == 'any')
        )
        query = query.filter(
            (Meal.gender == gender) | (Meal.gender == 'any')
        )
        query = query.filter(
            (Meal.weight_category == weight_category) | (Meal.weight_category == 'any')
        )
        query = query.filter(
            (Meal.activity_level == activity_level) | (Meal.activity_level == 'any')
        )
        
        # Get user's allergies
        user_allergies = []
        if current_user.allergies:
            try:
                user_allergies = json.loads(current_user.allergies)
            except json.JSONDecodeError:
                pass
        
        # Filter out meals with allergens (simplified check)
        if user_allergies:
            for allergy in user_allergies:
                query = query.filter(~Meal.ingredients.contains(allergy.lower()))
        
        # Get meal recommendations
        available_meals = query.all()
        
        if not available_meals:
            # Fallback to any available meals
            available_meals = Meal.query.limit(5).all()
        
        # Select random meals
        recommended_meals = random.sample(available_meals, min(3, len(available_meals)))
        
        # Format response
        meals_data = []
        for meal in recommended_meals:
            ingredients_list = []
            try:
                ingredients_list = json.loads(meal.ingredients or '[]')
            except json.JSONDecodeError:
                pass
            
            # Generate affiliate links (simplified)
            affiliate_links = []
            for ingredient in ingredients_list[:3]:  # First 3 ingredients
                affiliate_links.append({
                    'ingredient': ingredient.title(),
                    'url': f'https://example-grocery.com/search?q={ingredient}',
                    'store': 'Sample Grocery'
                })
            
            meals_data.append({
                'id': meal.id,
                'name': meal.name,
                'description': meal.description,
                'calories': meal.calories,
                'protein': meal.protein,
                'carbs': meal.carbs,
                'fat': meal.fat,
                'fiber': meal.fiber,
                'prep_time': meal.prep_time,
                'difficulty': meal.difficulty,
                'cuisine_type': meal.cuisine_type,
                'meal_type': meal.meal_type,
                'ingredients': ingredients_list,
                'instructions': meal.instructions,
                'image_url': meal.image_url,
                'affiliate_links': affiliate_links
            })
        
        # Get health tips
        health_tips = HealthTip.query.filter_by(is_active=True).order_by(db.func.random()).limit(2).all()
        tips_data = []
        for tip in health_tips:
            tips_data.append({
                'title': tip.title,
                'content': tip.content,
                'category': tip.category
            })
        
        # Save recommendation to history
        for meal in recommended_meals:
            history = MealHistory(
                user_id=current_user.id,
                meal_id=meal.id
            )
            db.session.add(history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'meals': meals_data,
            'health_tips': tips_data,
            'user_profile': {
                'age_group': age_group,
                'weight_category': weight_category,
                'activity_level': activity_level
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/rate_meal', methods=['POST'])
@require_login
def rate_meal():
    """Rate a meal"""
    try:
        data = request.get_json()
        meal_id = data.get('meal_id')
        rating = data.get('rating')
        notes = data.get('notes', '')
        
        if not meal_id or not rating:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find existing history entry or create new one
        history = MealHistory.query.filter_by(
            user_id=current_user.id,
            meal_id=meal_id
        ).first()
        
        if history:
            history.rating = rating
            history.notes = notes
        else:
            history = MealHistory(
                user_id=current_user.id,
                meal_id=meal_id,
                rating=rating,
                notes=notes
            )
            db.session.add(history)
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
