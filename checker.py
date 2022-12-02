from playwright.async_api import async_playwright
import re


class Checker:

    def __init__(self, urlList) -> None:
        self.googleFonts = {}
        for url in urlList:
            self.googleFonts[url] = 0
        self.urlList = urlList

    def detectGoogleFonts(self, requestUrl, url):
        match = re.search(
            r'(^https?:\/\/fonts\.googleapis\.com\/*)|(^https?:\/\/fonts\.gstatic\.com\/*)', requestUrl)
        if match:
            print(">>", "GET", requestUrl)
            self.googleFonts[url] = 1

    async def run(self, playwright):
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        page.on("request", lambda request: self.detectGoogleFonts(
            request.url, page.url))
        for url in self.urlList:
            await page.goto(url)
        await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.run(playwright)
