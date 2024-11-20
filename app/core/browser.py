from playwright.sync_api import sync_playwright
from app.core.proxy import ProxyManager

class BrowserManager:
    @staticmethod
    def create_browser_context():
        proxy_manager = ProxyManager()
        proxy_config = proxy_manager.get_proxy_server()
        
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox"],
            proxy={
                'server': proxy_config['server'],
                'username': proxy_config['username'],
                'password': proxy_config['password']
            }
        )
        context = browser.new_context()
        
        return playwright, browser, context 