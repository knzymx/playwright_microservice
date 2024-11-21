from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
from dotenv import load_dotenv
import logging
import os

from app.core.redis_client import init_redis
from app.routes.api import api_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize Redis
    app.redis_client = init_redis()
    
    # Initialize Flask-Limiter
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}",
        default_limits=["10000 per day", "1000 per hour"]
    )
    
    # Initialize limiter with the app
    limiter.init_app(app)
    app.limiter = limiter
    
    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)
    
    # Add custom metrics
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    return app 