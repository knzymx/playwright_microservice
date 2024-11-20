from playwright.sync_api import TimeoutError as PlaywrightTimeout

class PageInteractions:
    def __init__(self, page):
        self.page = page

    def scroll_to_bottom(self):
        self.page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    const distance = 100;
                    const delay = 100;
                    const timer = setInterval(() => {
                        window.scrollBy(0, distance);
                        if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
                            clearInterval(timer);
                            resolve();
                        }
                    }, delay);
                });
            }
        """)

    def click_element(self, selector):
        try:
            self.page.click(selector, timeout=5000)
            return {'status': 'success'}
        except PlaywrightTimeout:
            return {'status': 'element not found', 'selector': selector}

    def fill_form(self, form_data):
        results = {}
        for selector, value in form_data.items():
            try:
                self.page.fill(selector, value)
                results[selector] = 'success'
            except Exception as e:
                results[selector] = str(e)
        return results 