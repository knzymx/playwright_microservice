from functools import wraps
from flask import request, jsonify
from urllib.parse import urlparse

def validate_url(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        url = request.args.get('url') or request.json.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            return jsonify({'error': 'Invalid URL scheme'}), 400
        if not parsed_url.netloc:
            return jsonify({'error': 'Invalid URL'}), 400
        return f(*args, **kwargs)
    return decorated_function 