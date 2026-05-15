import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function SearchBox() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    async function queryDB() {
        if (!query.trim()) return;
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/query?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error("Query failed");
            const data = await response.json();
            setResults(data.results);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    function handleSubmit(e) {
        e.preventDefault();
        queryDB();
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    className="searchBar"
                    type="text"
                    placeholder="Search..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Searching..." : "Search"}
                </button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <ul>
                {results.map((result, i) => (
                    <li key={i}>
                        <div className="result-header"><h1>{result.name}</h1></div>
                        <SyntaxHighlighter language="python" style={vscDarkPlus}>
                            {result.source}
                        </SyntaxHighlighter>
                    </li>
                ))}
            </ul>
        </div>
    );
}