from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import joblib
import random  # For demo data

def get_crop_forecast(crop_type: str, region: str) -> Dict[str, Any]:
    """
    Generate crop forecast for demo purposes
    """
    # Demo data generation
    predicted_yield = random.uniform(3.5, 8.5)  # tons per hectare
    predicted_demand = random.uniform(1000, 5000)  # units
    
    return {
        'predicted_yield': round(predicted_yield, 2),
        'predicted_demand': round(predicted_demand),
        'market_analysis': f"Market demand for {crop_type} in {region} region shows positive trends with steady growth.",
        'planting_advice': f"Optimal planting time for {crop_type} in {region} region is approaching. Consider early preparation.",
        'suitable_regions': [region, "Adjacent Region 1", "Adjacent Region 2"],
        'confidence_score': random.uniform(0.7, 0.95),
        'selling_strategy': {
            'timing_advice': "Optimal selling window in 3-4 months",
            'peak_months': ["July", "August", "September"],
            'storage_guidance': "Maintain humidity levels below 14% for optimal storage"
        },
        'distribution_strategy': {
            'target_markets': ["Local Market", "Regional Export", "National Distribution"],
            'logistics_advice': "Consider bulk transport for cost optimization"
        }
    }

class Forecasting:
    def __init__(self):
        self.yield_model = None
        self.demand_model = None
        self.features = [
            'temperature', 'rainfall', 'humidity', 'soil_moisture',
            'month', 'price_per_ton', 'price_moving_avg', 'price_change'
        ]

    def load_models(self, yield_model_path: str, demand_model_path: str):
        """
        Load trained models from files
        """
        self.yield_model = joblib.load(yield_model_path)
        self.demand_model = joblib.load(demand_model_path)

    def prepare_features(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare features for prediction
        """
        df = pd.DataFrame([data])
        
        # Add derived features
        if 'price_history' in data:
            df['price_moving_avg'] = np.mean(data['price_history'])
            df['price_change'] = (data['price_per_ton'] - data['price_history'][-1]) / data['price_history'][-1]
        else:
            df['price_moving_avg'] = data['price_per_ton']
            df['price_change'] = 0

        # Ensure all required features are present
        for feature in self.features:
            if feature not in df.columns:
                df[feature] = 0

        return df[self.features]

    def predict_yield(self, features: Dict[str, Any]) -> float:
        """
        Predict crop yield based on given features
        """
        if self.yield_model is None:
            raise ValueError("Yield model not loaded")

        X = self.prepare_features(features)
        return float(self.yield_model.predict(X)[0])

    def predict_demand(self, features: Dict[str, Any]) -> float:
        """
        Predict crop demand based on given features
        """
        if self.demand_model is None:
            raise ValueError("Demand model not loaded")

        X = self.prepare_features(features)
        return float(self.demand_model.predict(X)[0])

    def get_forecast(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get both yield and demand forecasts
        """
        predicted_yield = self.predict_yield(features)
        predicted_demand = self.predict_demand(features)

        return {
            "yield": predicted_yield,
            "demand": predicted_demand,
            "features_used": self.features
        }