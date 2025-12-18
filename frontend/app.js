// API Configuration
const API_BASE_URL = 'https://shl-recommendation-system-qfgu.onrender.com';  // Render backend

// Set example query
function setQuery(text) {
    document.getElementById('query').value = text;
}

// Get recommendations
async function getRecommendations() {
    const query = document.getElementById('query').value.trim();
    const topK = parseInt(document.getElementById('topK').value);

    // Validate
    if (!query) {
        showError('Please enter a query');
        return;
    }

    if (topK < 1 || topK > 20) {
        showError('Number of recommendations must be between 1 and 20');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('submitBtn').disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                top_k: topK
            })
        });

        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }

        const data = await response.json();
        displayResults(data.recommendations);

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to get recommendations: ${error.message}. Make sure the API is running at ${API_BASE_URL}`);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
    }
}

// Display results
function displayResults(recommendations) {
    const resultsSection = document.getElementById('results');
    const resultsList = document.getElementById('resultsList');

    if (!recommendations || recommendations.length === 0) {
        showError('No recommendations found');
        return;
    }

    resultsList.innerHTML = '';

    recommendations.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'result-card';

        const testTypes = Array.isArray(rec.test_type) ? rec.test_type.join(', ') : rec.test_type;
        const relevancePercent = (rec.relevance_score * 100).toFixed(1);

        card.innerHTML = `
            <h3>${index + 1}. ${rec.assessment_name}</h3>
            <span class="result-score">Relevance: ${relevancePercent}%</span>
            <p>${truncate(rec.description, 200)}</p>
            <div class="result-meta">
                <span>⏱️ ${rec.duration} minutes</span>
                <span>📝 ${testTypes}</span>
                <span>🔄 Adaptive: ${rec.adaptive_support}</span>
                <span>🌐 Remote: ${rec.remote_support}</span>
            </div>
            <p style="margin-top: 1rem;">
                <a href="${rec.assessment_url}" target="_blank" rel="noopener">View Assessment →</a>
            </p>
        `;

        resultsList.appendChild(card);
    });

    resultsSection.style.display = 'block';

    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Truncate text
function truncate(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Allow Enter key to submit (with Shift+Enter for new line)
document.getElementById('query').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        getRecommendations();
    }
});
