from typing import Dict, Any
import numpy as np

class RecommendationEngine:
    def __init__(self):
        self.market_conditions = {
            'wheat': {
                'peak_months': [6, 7, 8],
                'storage_life_months': 12,
                'best_regions': ['north', 'central'],
                'demand_trend': 'stable',
                'price_trend': 'increasing'
            },
            'rice': {
                'peak_months': [9, 10, 11],
                'storage_life_months': 6,
                'best_regions': ['south', 'east'],
                'demand_trend': 'increasing',
                'price_trend': 'stable'
            },
            'corn': {
                'peak_months': [8, 9, 10],
                'storage_life_months': 8,
                'best_regions': ['central', 'west'],
                'demand_trend': 'increasing',
                'price_trend': 'increasing'
            },
            'soybeans': {
                'peak_months': [9, 10, 11],
                'storage_life_months': 9,
                'best_regions': ['north', 'east'],
                'demand_trend': 'stable',
                'price_trend': 'stable'
            },
            'cotton': {
                'peak_months': [10, 11, 12],
                'storage_life_months': 12,
                'best_regions': ['south', 'west'],
                'demand_trend': 'decreasing',
                'price_trend': 'decreasing'
            }
        }
        
        self.regional_markets = {
            'north': ['Delhi', 'Punjab Grain Market', 'Haryana Agricultural Market'],
            'south': ['Chennai Trade Center', 'Bangalore Commodity Exchange', 'Kerala Agri Market'],
            'east': ['Kolkata Wholesale Market', 'Bihar Agricultural Hub', 'Odisha Trading Center'],
            'west': ['Mumbai Commodity Market', 'Gujarat Agricultural Exchange', 'Rajasthan Trading Hub'],
            'central': ['Madhya Pradesh Mandi', 'Chhattisgarh Agricultural Market', 'UP Trading Center']
        }

    def get_recommendation(self, crop_type: str, predicted_yield: float, predicted_demand: float) -> Dict[str, Any]:
        """
        Generate comprehensive recommendations including what to grow, when to sell, and where to distribute
        """
        current_month = datetime.now().month
        ratio = predicted_demand / predicted_yield if predicted_yield > 0 else 0
        crop_info = self.market_conditions.get(crop_type, {})
        
        # Calculate months until peak season
        peak_months = crop_info.get('peak_months', [])
        next_peak = next((m for m in peak_months if m >= current_month), peak_months[0] if peak_months else current_month)
        months_to_peak = (next_peak - current_month) % 12

        # Generate planting recommendation
        if ratio > 1.2:
            planting_advice = f"High demand expected for {crop_type}. Recommended to increase production."
            confidence = 0.9
        elif ratio < 0.8:
            planting_advice = f"Market may be oversupplied for {crop_type}. Consider diversifying crops or reducing production."
            confidence = 0.8
        else:
            planting_advice = f"Current production levels of {crop_type} align well with market demand."
            confidence = 0.85

        # Generate market insights
        market_insights = []
        if crop_info.get('demand_trend') == 'increasing':
            market_insights.append("Market demand is trending upward")
        elif crop_info.get('demand_trend') == 'decreasing':
            market_insights.append("Market demand is trending downward")

        if crop_info.get('price_trend') == 'increasing':
            market_insights.append("Prices are expected to rise")
        elif crop_info.get('price_trend') == 'decreasing':
            market_insights.append("Prices are expected to decline")

        # Generate selling strategy
        if months_to_peak <= 3:
            selling_strategy = f"Peak selling season approaching in {months_to_peak} months. Consider storing crop until then for better prices."
        else:
            selling_strategy = f"Current off-peak season. {months_to_peak} months until peak season. Evaluate storage costs versus current market prices."

        # Generate distribution recommendation
        recommended_markets = []
        if ratio > 1.2:
            # High demand - recommend distant markets with better prices
            for region, markets in self.regional_markets.items():
                if region not in crop_info.get('best_regions', []):
                    recommended_markets.extend(markets[:1])
        else:
            # Normal/Low demand - recommend local markets to reduce costs
            for region in crop_info.get('best_regions', [])[:2]:
                recommended_markets.extend(self.regional_markets.get(region, [])[:2])

        # Storage recommendation
        storage_months = crop_info.get('storage_life_months', 6)
        storage_advice = f"Crop can be stored for up to {storage_months} months under proper conditions."

        return {
            "planting_recommendation": {
                "advice": planting_advice,
                "confidence": confidence,
                "best_regions": crop_info.get('best_regions', [])
            },
            "selling_strategy": {
                "timing": selling_strategy,
                "peak_months": peak_months,
                "storage_duration": storage_advice
            },
            "distribution_strategy": {
                "recommended_markets": recommended_markets,
                "transportation_tips": "Consider bulk transport to reduce costs" if ratio > 1.2 else "Focus on local markets to minimize transportation costs"
            },
            "market_analysis": {
                "demand_supply_ratio": float(ratio),
                "predicted_yield": float(predicted_yield),
                "predicted_demand": float(predicted_demand),
                "market_insights": market_insights
            }
        }