from playwright.async_api import async_playwright
import re


class Checker:

    def __init__(self, url) -> None:
        self.googleFontsFound = False
        self.url = url

    def detectGoogleFonts(self, url):
        match = re.search(
            r'(^https?:\/\/fonts\.googleapis\.com\/*)|(^https?:\/\/fonts\.gstatic\.com\/*)', url)
        if match:
            print(">>", "GET", url)
            self.googleFontsFound = True

    async def run(self, playwright):
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        page.on("request", lambda request: self.detectGoogleFonts(request.url))
        await page.goto(self.url)
        await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.run(playwright)
