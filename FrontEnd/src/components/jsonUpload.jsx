import { useState } from 'react';

export default function UploadFile(){
    const path = "http://127.0.0.1:5000/upload/"
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [result, setResult] = useState(null)

    async function callApi(e){
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        const fileInput = e.target.querySelector('input[type="file"]')
        const file = fileInput.files[0]

        if (!file) {
            setError('Please select a file')
            setLoading(false)
            return
        }

        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await fetch(path, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return(
        <div>
            <form onSubmit={callApi}>
                <input className="uploadInput" type="file" />
                <button className="uploadBtn" type="submit" disabled={loading}>
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </form>

            {error && <p style={{color: '#e32222'}}>{error}</p>}
            {result && (
                <pre>
                    {result.data}
                </pre>
            )}
        </div>
    );
}