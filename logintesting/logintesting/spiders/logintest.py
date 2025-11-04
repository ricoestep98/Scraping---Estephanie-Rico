from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless = False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://quotes.toscrape.com/login')
    page.fill('input#username', 'demo')
    page.fill('input#password', 'demo')
    page.click('input[type=submit]')
    html = page.inner_html('#content')
    print(html)