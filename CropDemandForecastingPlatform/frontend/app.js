document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('forecastForm');
    const resultsSection = document.getElementById('results');
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const formStatus = document.getElementById('formStatus');

    // Show loading state
    function showLoading() {
        submitBtn.disabled = true;
        submitText.style.display = 'none';
        loadingIndicator.style.display = 'inline-block';
        formStatus.textContent = 'Processing forecast...';
        formStatus.className = 'status-message info';
    }

    // Hide loading state
    function hideLoading() {
        submitBtn.disabled = false;
        submitText.style.display = 'inline';
        loadingIndicator.style.display = 'none';
        formStatus.textContent = '';
    }

    // Update UI with forecast results
    function updateUI(data) {
        try {
            // Update key metrics
            document.getElementById('yieldValue').textContent = `${data.yield.toFixed(2)} tons/hectare`;
            document.getElementById('demandValue').textContent = `${data.demand.toFixed(2)} tons`;
            document.getElementById('confidenceLevel').textContent = `${data.confidence_level}%`;

            // Update market insights
            document.getElementById('marketInsights').textContent = data.market_insights;
            document.getElementById('plantingAdvice').textContent = data.planting_advice;
            document.getElementById('bestRegions').textContent = data.best_regions.join(', ');

            // Update selling strategy
            document.getElementById('sellingTiming').textContent = data.selling_timing;
            document.getElementById('peakMonths').textContent = data.peak_months.join(', ');
            document.getElementById('storageAdvice').textContent = data.storage_advice;

            // Update recommended markets
            const marketsList = document.getElementById('recommendedMarkets');
            marketsList.innerHTML = data.recommended_markets
                .map(market => `<li>${market}</li>`)
                .join('');

            // Add transportation tips
            document.getElementById('transportationTips').textContent = data.transportation_tips;

            // Show results with animation
            resultsSection.style.display = 'block';
            resultsSection.classList.add('show');
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
            // Show success message
            formStatus.textContent = 'Forecast generated successfully!';
            formStatus.className = 'status-message success';
        } catch (error) {
            console.error('Error updating UI:', error);
            formStatus.textContent = 'Error displaying results. Please try again.';
            formStatus.className = 'status-message error';
        }
    }

    // Fetch forecast from backend
    async function fetchForecast(formData) {
        const response = await fetch('http://localhost:5000/api/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    // Form submission handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form data
        const formData = {
            crop_type: document.getElementById('crop_type').value,
            region: document.getElementById('region').value
        };

        // Validate inputs
        if (!formData.crop_type || !formData.region) {
            formStatus.textContent = 'Please select both crop type and region.';
            formStatus.className = 'status-message error';
            return;
        }

        try {
            showLoading();
            const data = await fetchForecast(formData);
            updateUI(data);
        } catch (error) {
            console.error('Error:', error);
            formStatus.textContent = 'Failed to get forecast. Please try again.';
            formStatus.className = 'status-message error';
        } finally {
            hideLoading();
        }
    });

    // Reset form status on input change
    form.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', () => {
            formStatus.textContent = '';
            formStatus.className = 'status-message';
        });
    });
});