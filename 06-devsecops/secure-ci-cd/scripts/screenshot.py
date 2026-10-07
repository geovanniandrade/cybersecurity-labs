from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1100}, device_scale_factor=1)
    page.goto("http://127.0.0.1:8080", wait_until="networkidle")
    page.get_by_role("button", name="Calcular").click()
    page.wait_for_function("document.querySelector('#result').textContent === 'Resultado: 30'")
    page.screenshot(path="evidence/application.png", full_page=True)
    browser.close()
