# Crop Demand Forecasting Platform

A full-stack web application for predicting crop yields and market demand using machine learning.

## Project Structure

```
/Crop-Demand-Forecasting-Platform
├── backend/
│   ├── models/
│   │   ├── demand_model.pkl
│   │   └── yield_model.pkl
│   ├── data/
│   │   ├── historical/
│   │   │   ├── crop_yields.csv
│   │   │   ├── market_prices.csv
│   │   │   └── weather_history.csv
│   │   └── simulated/
│   │       └── iot_sensor_data.csv
│   ├── notebooks/
│   │   ├── 1_model_training.ipynb
│   │   └── 2_data_prep.ipynb
│   ├── src/
│   │   ├── api/
│   │   │   └── weather_api.py
│   │   ├── core/
│   │   │   ├── recommendation_engine.py
│   │   │   └── forecasting.py
│   │   └── app.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   │       ├── images/
│   │       └── css/
│   │           └── style.css
│   ├── src/
│   │   ├── js/
│   │   │   └── main.js
│   │   └── components/
│   │       └── Dashboard.js
│   ├── package.json
│   └── README.md
└── database/
    ├── schema.sql
    └── data.db
```

## Features

- Crop yield prediction using Linear Regression
- Demand forecasting using Random Forest
- Weather data integration
- Interactive dashboard
- Data-driven recommendations

## Setup

1. Backend Setup:
   ```bash
   cd backend
   pip install -r requirements.txt
   python src/app.py
   ```

2. Frontend Setup:
   ```bash
   cd frontend
   # Open index.html in a web browser
   ```

3. Database Setup:
   ```bash
   cd database
   sqlite3 data.db < schema.sql
   ```

## Usage

1. Select crop type and region from the dropdown menus
2. Click "Get Forecast" to receive predictions
3. View yield predictions, demand forecasts, and recommendations

## Technologies Used

- Backend: Python, Flask, scikit-learn
- Frontend: HTML, CSS, JavaScript
- Database: SQLite

- ML Models: Linear Regression, Random Forest

- ## DATASET LINK: https://github.com/Kusumagm07/project12/tree/main/data
