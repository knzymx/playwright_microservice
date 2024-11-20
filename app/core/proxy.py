import os
import json
import random
from pathlib import Path

class ProxyManager:
    def __init__(self):
        self.proxy_configs = self._load_proxy_configs()

    def _load_proxy_configs(self):
        config_path = Path(__file__).parent.parent / 'config' / 'proxy_config.json'
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config['proxies']
        except Exception as e:
            raise Exception(f'Error loading proxy configuration: {e}')

    def get_proxy_server(self):
        if not self.proxy_configs:
            raise Exception("No proxy configurations available")
        
        proxy = random.choice(self.proxy_configs)
        return {
            'server': f'http://{proxy["host"]}:{proxy["port"]}',
            'username': os.getenv('PROXYMESH_USER'),
            'password': os.getenv('PROXYMESH_PASS')
        } 