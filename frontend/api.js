const API = 'http://localhost:8000';

export async function request(url, options = {}) {
    const response = await fetch(`${API}${url}`, {
        headers: {
            'Content-Type': 'application/json'
        },
        ...options
    });

    return response.json();
}