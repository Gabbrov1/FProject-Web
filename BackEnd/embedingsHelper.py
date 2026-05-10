import requests

def send_embedding_request(text, path=False):
    if path:
        with open(text, 'r') as f:
            text = f.read()
    
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': 'nomic-embed-text',
        'prompt': text
    })

    return res.json()['embedding']