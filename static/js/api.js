// static/js/api.js
// =============================================
// CLIENTE DE API COM CSRF
// =============================================

function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function apiRequest(url, options = {}) {
    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            ...(options.headers || {}),
        },
    };

    const response = await fetch(url, config);

    if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
    }

    return response.json();
}
