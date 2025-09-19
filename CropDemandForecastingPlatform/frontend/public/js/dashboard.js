// Check if user is logged in
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('isLoggedIn')) {
        window.location.href = '/';
        return;
    }

    const forecastForm = document.getElementById('forecastForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsSection = document.getElementById('resultsSection');
    const errorMessage = document.getElementById('errorMessage');

    forecastForm.addEventListener('submit', handleForecastSubmission);
});

async function handleForecastSubmission(e) {
    e.preventDefault();

    const cropType = document.getElementById('cropType').value;
    const region = document.getElementById('region').value;

    // Show loading indicator
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsSection = document.getElementById('resultsSection');
    const errorMessage = document.getElementById('errorMessage');

    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'none';

    try {
        const response = await fetch('/api/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                crop_type: cropType,
                region: region
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate forecast');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

function displayResults(data) {
    // Show results section
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';

    // Update all result fields
    document.getElementById('predictedYield').textContent = `${data.yield} tons/hectare`;
    document.getElementById('predictedDemand').textContent = `${data.demand} units`;
    document.getElementById('marketInsights').textContent = data.market_insights;
    document.getElementById('plantingAdvice').textContent = data.planting_advice;
    document.getElementById('bestRegions').textContent = data.best_regions.join(', ');
    document.getElementById('sellingTiming').textContent = data.selling_timing;
    document.getElementById('peakMonths').textContent = data.peak_months.join(', ');
    document.getElementById('recommendedMarkets').textContent = data.recommended_markets.join(', ');
    document.getElementById('storageAdvice').textContent = data.storage_advice;

    // Update confidence score
    const confidenceFill = document.getElementById('confidenceLevel');
    const confidenceScore = document.getElementById('confidenceScore');
    confidenceFill.style.width = `${data.confidence_level}%`;
    confidenceScore.textContent = `${data.confidence_level}% Confidence`;
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = '/';
}