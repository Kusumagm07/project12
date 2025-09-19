import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

class BasePredictor:
    def __init__(self):
        self.model = None
        self.label_encoder_crop = LabelEncoder()
        self.label_encoder_region = LabelEncoder()
        self.generate_training_data()
        self.train_model()

    def generate_training_data(self):
        # Generate sample data
        np.random.seed(42)
        n_samples = 1000
        
        # Create sample crops and regions
        crops = ['wheat', 'rice', 'corn', 'soybeans', 'cotton']
        regions = ['north', 'south', 'east', 'west', 'central']
        
        # Generate random data
        self.data = pd.DataFrame({
            'crop_type': np.random.choice(crops, n_samples),
            'region': np.random.choice(regions, n_samples),
            'temperature': np.random.normal(25, 5, n_samples),
            'rainfall': np.random.normal(150, 30, n_samples),
            'soil_quality': np.random.normal(7, 1, n_samples)
        })
        
        # Encode categorical variables
        self.data['crop_type_encoded'] = self.label_encoder_crop.fit_transform(self.data['crop_type'])
        self.data['region_encoded'] = self.label_encoder_region.fit_transform(self.data['region'])

    def preprocess_input(self, crop_type, region):
        # Encode input
        crop_encoded = self.label_encoder_crop.transform([crop_type])[0]
        region_encoded = self.label_encoder_region.transform([region])[0]
        
        # Create feature array
        X = np.array([[
            crop_encoded,
            region_encoded,
            np.random.normal(25, 5),  # Simulated temperature
            np.random.normal(150, 30),  # Simulated rainfall
            np.random.normal(7, 1)  # Simulated soil quality
        ]])
        
        return X

class YieldPredictor(BasePredictor):
    def train_model(self):
        # Generate yield data (tons per hectare)
        base_yields = {
            'wheat': 3.0,
            'rice': 4.0,
            'corn': 5.5,
            'soybeans': 2.8,
            'cotton': 2.0
        }
        
        # Calculate yield based on conditions and base yield
        self.data['yield'] = self.data.apply(
            lambda row: base_yields[row['crop_type']] * 
            (1 + 0.1 * (row['temperature'] - 25) / 5) *
            (1 + 0.2 * (row['rainfall'] - 150) / 30) *
            (1 + 0.15 * (row['soil_quality'] - 7)), axis=1
        )
        
        # Train linear regression model
        X = self.data[['crop_type_encoded', 'region_encoded', 'temperature', 'rainfall', 'soil_quality']]
        y = self.data['yield']
        self.model = LinearRegression()
        self.model.fit(X, y)

    def predict(self, crop_type, region):
        X = self.preprocess_input(crop_type, region)
        return max(0, self.model.predict(X)[0])

class DemandPredictor(BasePredictor):
    def train_model(self):
        # Generate demand data (tons)
        base_demand = {
            'wheat': 1000,
            'rice': 1200,
            'corn': 1500,
            'soybeans': 800,
            'cotton': 600
        }
        
        # Calculate demand based on conditions and base demand
        self.data['demand'] = self.data.apply(
            lambda row: base_demand[row['crop_type']] * 
            (1 + 0.2 * np.random.randn()) *  # Random market fluctuation
            (1 + 0.1 * (row['temperature'] - 25) / 5) *  # Temperature effect
            (1.2 if row['region'] in ['central', 'north'] else 1.0),  # Region effect
            axis=1
        )
        
        # Train random forest model
        X = self.data[['crop_type_encoded', 'region_encoded', 'temperature', 'rainfall', 'soil_quality']]
        y = self.data['demand']
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def predict(self, crop_type, region):
        X = self.preprocess_input(crop_type, region)
        return max(0, self.model.predict(X)[0])