class Dashboard {
    constructor() {
        this.form = document.getElementById('forecastForm');
        this.resultsSection = document.getElementById('results');
        this.yieldValue = document.getElementById('yieldValue');
        this.demandValue = document.getElementById('demandValue');
        this.recommendationText = document.getElementById('recommendationText');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.getForecast();
        });
    }

    async getForecast() {
        const formData = {
            crop_type: document.getElementById('crop_type').value,
            region: document.getElementById('region').value
        };

        try {
            await this.showLoading();
            const data = await this.fetchForecast(formData);
            this.updateUI(data);
        } catch (error) {
            console.error('Error:', error);
            this.showError();
        } finally {
            this.hideLoading();
        }
    }

    async fetchForecast(formData) {
        const response = await fetch('http://localhost:5000/api/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Failed to get forecast');
        }

        return response.json();
    }

    updateUI(data) {
        this.yieldValue.textContent = `${data.yield.toFixed(2)} tons/hectare`;
        this.demandValue.textContent = `${data.demand.toFixed(2)} tons`;
        this.recommendationText.textContent = data.recommendation;
        this.resultsSection.style.display = 'block';
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showLoading() {
        this.form.querySelector('button').disabled = true;
        this.form.querySelector('button').textContent = 'Getting Forecast...';
    }

    hideLoading() {
        this.form.querySelector('button').disabled = false;
        this.form.querySelector('button').textContent = 'Get Forecast';
    }

    showError() {
        alert('Failed to get forecast. Please try again.');
    }
}

export default Dashboard;