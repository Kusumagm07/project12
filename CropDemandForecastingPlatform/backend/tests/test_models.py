import sys
import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.crop_models import YieldPredictor, DemandPredictor

def test_model_predictions():
    """Test both yield and demand prediction models"""
    print("Starting model testing...")
    
    # Initialize predictors
    yield_predictor = YieldPredictor()
    demand_predictor = DemandPredictor()
    
    # Test cases
    test_cases = [
        {'crop_type': 'wheat', 'region': 'north'},
        {'crop_type': 'rice', 'region': 'south'},
        {'crop_type': 'corn', 'region': 'central'},
        {'crop_type': 'soybeans', 'region': 'east'},
        {'crop_type': 'cotton', 'region': 'west'}
    ]
    
    print("\n=== Testing Individual Predictions ===")
    for case in test_cases:
        crop_type = case['crop_type']
        region = case['region']
        
        # Get predictions
        yield_pred = yield_predictor.predict(crop_type, region)
        demand_pred = demand_predictor.predict(crop_type, region)
        
        print(f"\nCrop: {crop_type.capitalize()}, Region: {region.capitalize()}")
        print(f"Predicted Yield: {yield_pred:.2f} tons/hectare")
        print(f"Predicted Demand: {demand_pred:.2f} tons")

def test_model_performance():
    """Test model performance metrics"""
    print("\n=== Testing Model Performance ===")
    
    # Generate test data
    np.random.seed(42)
    n_samples = 100
    crops = ['wheat', 'rice', 'corn', 'soybeans', 'cotton']
    regions = ['north', 'south', 'east', 'west', 'central']
    
    test_data = pd.DataFrame({
        'crop_type': np.random.choice(crops, n_samples),
        'region': np.random.choice(regions, n_samples),
        'temperature': np.random.normal(25, 5, n_samples),
        'rainfall': np.random.normal(150, 30, n_samples),
        'soil_quality': np.random.normal(7, 1, n_samples)
    })
    
    # Initialize predictors
    yield_predictor = YieldPredictor()
    demand_predictor = DemandPredictor()
    
    # Make predictions for all test cases
    yield_predictions = []
    demand_predictions = []
    
    for _, row in test_data.iterrows():
        yield_pred = yield_predictor.predict(row['crop_type'], row['region'])
        demand_pred = demand_predictor.predict(row['crop_type'], row['region'])
        yield_predictions.append(yield_pred)
        demand_predictions.append(demand_pred)
    
    # Print statistics
    print("\nYield Predictions Statistics:")
    print(f"Mean: {np.mean(yield_predictions):.2f} tons/hectare")
    print(f"Std Dev: {np.std(yield_predictions):.2f}")
    print(f"Min: {np.min(yield_predictions):.2f}")
    print(f"Max: {np.max(yield_predictions):.2f}")
    
    print("\nDemand Predictions Statistics:")
    print(f"Mean: {np.mean(demand_predictions):.2f} tons")
    print(f"Std Dev: {np.std(demand_predictions):.2f}")
    print(f"Min: {np.min(demand_predictions):.2f}")
    print(f"Max: {np.max(demand_predictions):.2f}")

def test_model_sensitivity():
    """Test model sensitivity to input changes"""
    print("\n=== Testing Model Sensitivity ===")
    
    base_case = {
        'crop_type': 'wheat',
        'region': 'central'
    }
    
    yield_predictor = YieldPredictor()
    demand_predictor = DemandPredictor()
    
    # Get base predictions
    base_yield = yield_predictor.predict(**base_case)
    base_demand = demand_predictor.predict(**base_case)
    
    print("\nBase Case:")
    print(f"Crop: {base_case['crop_type'].capitalize()}, Region: {base_case['region'].capitalize()}")
    print(f"Base Yield: {base_yield:.2f} tons/hectare")
    print(f"Base Demand: {base_demand:.2f} tons")
    
    # Test different regions
    print("\nRegional Sensitivity:")
    regions = ['north', 'south', 'east', 'west']
    for region in regions:
        yield_pred = yield_predictor.predict(base_case['crop_type'], region)
        demand_pred = demand_predictor.predict(base_case['crop_type'], region)
        print(f"\nRegion: {region.capitalize()}")
        print(f"Yield: {yield_pred:.2f} (Δ: {yield_pred - base_yield:+.2f})")
        print(f"Demand: {demand_pred:.2f} (Δ: {demand_pred - base_demand:+.2f})")
    
    # Test different crops
    print("\nCrop Type Sensitivity:")
    crops = ['rice', 'corn', 'soybeans', 'cotton']
    for crop in crops:
        yield_pred = yield_predictor.predict(crop, base_case['region'])
        demand_pred = demand_predictor.predict(crop, base_case['region'])
        print(f"\nCrop: {crop.capitalize()}")
        print(f"Yield: {yield_pred:.2f} (Δ: {yield_pred - base_yield:+.2f})")
        print(f"Demand: {demand_pred:.2f} (Δ: {demand_pred - base_demand:+.2f})")

if __name__ == "__main__":
    print("=== Crop Demand Forecasting Model Test Suite ===\n")
    
    try:
        # Run all tests
        test_model_predictions()
        test_model_performance()
        test_model_sensitivity()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        raise