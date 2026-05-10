import { useState } from 'react';

export default function LoginForm() {
    const [status, setStatus] = useState('');
    const [loading, setLoading] = useState(false);

    const apiUrl = "http://127.0.0.1:5000/auth/login/"
    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setStatus('');

        const form = e.target;
        const payload = {
            username: form.username.value,
            password: form.password.value,
        };

        try {
            const res = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            console.log(data);
            if (data.user_id) {
                setStatus(`Hello, ${data.username}!`);
                
            } else {
                setStatus('Something went wrong.');
            }
        } catch (err) {
            setStatus('Could not reach the server.');
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
        <form onSubmit={handleSubmit}>
            <label htmlFor="username">Username</label>
            <input type="text" id="username" name="username" required />

            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" required />

            

            <button type="submit" disabled={loading}>
                {loading ? 'Loging in...' : 'Log in'}
            </button>

            {status && <p>{status}</p>}
        </form>

        </>
        
    );
}