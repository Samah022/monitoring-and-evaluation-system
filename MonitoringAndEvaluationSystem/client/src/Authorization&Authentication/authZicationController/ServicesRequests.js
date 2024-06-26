export default class ServicesRequests {
    
    async login(email, password) {
        try {
            const response = await fetch('http://127.0.0.1:8000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();
            return data; 
        } catch (error) {
            console.error('Error logging in:', error);
            throw error;
        }
    }

    async isAuthenticated() {
        try {
            const response = await fetch('http://127.0.0.1:8000/isAuthenticated', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            return data; 
        } catch (error) {
            console.error('Error checking authentication:', error.message);
            throw error; 
        }
    }

    async logout() {
        try {
            const response = await fetch('http://127.0.0.1:8000/logout', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            return data; 
        } catch (error) {
            console.error('Error logging out:', error);
            throw error; 
        }
    }
}