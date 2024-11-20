from flask import Blueprint, jsonify, request, current_app
from app.utils.decorators import validate_url
from app.utils.page_interactions import PageInteractions
from app.core.browser import BrowserManager
from flask_limiter.util import get_remote_address

api_bp = Blueprint('api', __name__)

@api_bp.route('/fetch', methods=['GET'])
@current_app.limiter.limit("20000 per day", key_func=lambda: request.headers.get("X-API-KEY", "default"))
@validate_url
def fetch_url():
    current_app.logger.info('Received request for /fetch')
    url = request.args.get('url')
    
    try:
        playwright, browser, context = BrowserManager.create_browser_context()
        with playwright:
            page = context.new_page()
            current_app.logger.debug(f'Navigating to {url}')
            page.goto(url, wait_until='networkidle', timeout=30000)
            html = page.content()
            context.close()
            browser.close()
    except Exception as e:
        current_app.logger.error(f'Error fetching URL: {e}')
        return jsonify({'error': str(e)}), 500

    return jsonify({'html': html})

@api_bp.route('/interact', methods=['POST'])
@validate_url
def interact():
    # ... (similar implementation as before, but using the new structure)
    pass

@api_bp.route('/health', methods=['GET'])
def health_check():
    try:
        current_app.redis_client.ping()
        return jsonify({'status': 'healthy', 'redis': 'connected'})
    except Exception:
        return jsonify({'status': 'unhealthy', 'redis': 'disconnected'}), 500 