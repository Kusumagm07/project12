from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import os
from pathlib import Path
from typing import Dict, Any
import logging
from core.database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the absolute path to the frontend directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / 'frontend' / 'public'

app = Flask(__name__, static_folder=str(FRONTEND_DIR))
CORS(app)  # Enable CORS for all routes

# Initialize database
db = Database()

print("Starting Flask server...")
print(f"Frontend directory: {FRONTEND_DIR}")

# Route handlers for static pages
@app.route('/')
@app.route('/index.html')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/welcome')
@app.route('/welcome.html')
def serve_welcome():
    response = make_response(send_from_directory(app.static_folder, 'welcome.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/dashboard')
@app.route('/dashboard.html')
def serve_dashboard():
    return send_from_directory(app.static_folder, 'dashboard.html')

# Static asset routes
@app.route('/assets/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(str(FRONTEND_DIR / 'assets' / 'css'), filename)

@app.route('/assets/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(str(FRONTEND_DIR / 'assets' / 'images'), filename)

@app.route('/js/<path:filename>')
def serve_javascript(filename):
    return send_from_directory(str(FRONTEND_DIR / 'js'), filename)

@app.route('/src/<path:path>')
def serve_src(path):
    return send_from_directory(str(Path(FRONTEND_DIR).parent / 'src'), path)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'The requested URL was not found on the server.'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'An internal server error occurred.'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logging.info(f"Login attempt for email: {data.get('email')}")
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400

        # For testing, check hardcoded credentials
        if data['email'] == 'mahesha@gmail.com' and data['password'] == 'm@123':
            logging.info("Login successful")
            response = jsonify({
                'success': True,
                'user': {
                    'email': data['email'],
                    'name': 'Mahesh'
                }
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        logging.info("Login failed - invalid credentials")
        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/forecast', methods=['POST'])
def forecast():
    try:
        logging.info('Received forecast request')
        data = request.get_json()
        
        # Validate input
        if not data:
            logging.error('No JSON data received')
            return jsonify({'error': 'No data provided'}), 400
            
        crop_type = data.get('crop_type')
        region = data.get('region')

        if not crop_type or not region:
            logging.error(f'Missing parameters. Crop type: {crop_type}, Region: {region}')
            return jsonify({'error': 'Missing required parameters'}), 400
            
        logging.info(f'Processing forecast for crop: {crop_type}, region: {region}')

        # Import required modules and classes
        from core.forecasting import get_crop_forecast
        from core.recommendation_engine import RecommendationEngine

        # Get forecasting data
        forecast_data = get_crop_forecast(crop_type, region)
        
        # Initialize recommendation engine
        recommendation_engine = RecommendationEngine()
        recommendations = recommendation_engine.get_recommendation(crop_type, region, forecast_data)

        # Prepare comprehensive response
        response = {
            'yield': forecast_data['predicted_yield'],
            'demand': forecast_data['predicted_demand'],
            'market_insights': recommendations['market_analysis'],
            'planting_advice': recommendations['planting_advice'],
            'best_regions': recommendations['suitable_regions'],
            'confidence_level': int(recommendations['confidence_score'] * 100),
            'selling_timing': recommendations['selling_strategy']['timing_advice'],
            'peak_months': recommendations['selling_strategy']['peak_months'],
            'storage_advice': recommendations['selling_strategy']['storage_guidance'],
            'recommended_markets': recommendations['distribution_strategy']['target_markets'],
            'transportation_tips': recommendations['distribution_strategy']['logistics_advice']
        }

        logging.info('Successfully generated forecast and recommendations')
        return jsonify(response)

    except ImportError as e:
        logging.error(f'Failed to import required modules: {str(e)}')
        return jsonify({'error': 'Internal server configuration error'}), 500
    except ValueError as e:
        logging.error(f'Invalid input data: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f'Unexpected error in forecast endpoint: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)