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

            // Show results with animation
            resultsSection.style.display = 'block';
            resultsSection.classList.add('show');
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
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

        try {
            // Validate inputs
            if (!formData.crop_type || !formData.region) {
                formStatus.textContent = 'Please select both crop type and region.';
                formStatus.className = 'status-message error';
                return;
            }

            // Show loading state
            showLoading();

            // Fetch forecast from backend
            const data = await fetchForecast(formData);
                planting_advice: `Optimal planting conditions for ${formData.crop_type} in ${formData.region} region.`,
                best_regions: ["North", "Central"],
                storage_advice: "Maintain temperature between 10-15°C with 40-50% humidity",
                transportation_tips: "Use climate-controlled transport vehicles",
                recommended_markets: ["Local Markets", "Regional Distribution Centers", "Export Markets"]
            };

            // Update UI with results
            yieldValue.textContent = `${data.yield.toFixed(2)} tons/hectare`;
            demandValue.textContent = `${data.demand.toFixed(2)} tons`;
            
            // Update market insights
            document.getElementById('marketInsights').textContent = data.market_insights || 'Market data unavailable';
            
            // Update planting recommendations
            document.getElementById('plantingAdvice').textContent = data.planting_advice || 'Planting advice unavailable';
            document.getElementById('bestRegions').textContent = data.best_regions?.join(', ') || 'Data unavailable';
            document.getElementById('confidenceLevel').textContent = `${data.confidence_level || '--'}%`;
            
            // Update selling strategy
            document.getElementById('sellingTiming').textContent = data.selling_timing || 'Timing data unavailable';
            document.getElementById('peakMonths').textContent = data.peak_months?.join(', ') || 'Data unavailable';
            document.getElementById('storageAdvice').textContent = data.storage_advice || 'Storage advice unavailable';
            
            // Update distribution strategy
            const marketsList = document.getElementById('recommendedMarkets');
            marketsList.innerHTML = data.recommended_markets?.length 
                ? data.recommended_markets.map(market => `<li>${market}</li>`).join('')
                : '<li>No market recommendations available</li>';
            
            document.getElementById('transportationTips').textContent = data.transportation_tips || 'Transportation advice unavailable';

            // Show results section
            resultsSection.style.display = 'block';

            // Smooth scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            alert('Failed to get forecast. Please try again.');
        } finally {
            // Reset button state
            form.querySelector('button').disabled = false;
            form.querySelector('button').textContent = 'Get Forecast';
        }
    });

    // Add animation class when results are shown
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });

    observer.observe(resultsSection);
});