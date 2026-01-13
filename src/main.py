import pathlib
import time

import bs4
import loguru
import playwright.sync_api
import playwright_stealth

parse_url = 'https://www.wildberries.ru/catalog/0/search.aspx?search={search_string}'
search_string = 'пальто из натуральной шерсти'


@loguru.logger.catch()
def get_html(url: str, wait: int = 10) -> str:
    with playwright.sync_api.sync_playwright() as pw:
        browser = pw.chromium.launch(
            # headless=True,
            headless=False,
            slow_mo=300,
        )
        page = browser.new_page()

        playwright_stealth.Stealth().apply_stealth_sync(page)

        page.goto(url, wait_until="networkidle")  # ждём загрузки

        # loguru.logger.info(f'Waiting {wait} seconds...')
        # time.sleep(wait)

        loguru.logger.info(f'{page.url=}')
        html = page.content()  # уже отрендеренный HTML
        loguru.logger.info('Got content {} bytes', len(html))

        browser.close()
        return html


def get_url() -> str:
    return parse_url.format(search_string=search_string)


class Parse:
    _soap = None

    def __init__(self, html: str):
        self.html = html

    @property
    def soap(self):
        if self._soap is None:
            self._soap = bs4.BeautifulSoup(self.html, 'lxml')
        return self._soap

    def cards(self):
        yield from self.soap.find_all('article', class_='product-card')

    def parse(self):
        for card in self.cards():
            name = [*card.select_one('h2').stripped_strings][-1]  # Название
            url = card.select_one('a.product-card__link').attrs['href']  # Ссылка на товар
            art = card.attrs['data-nm-id']  # Артикул
            price = [*card.select_one('ins').stripped_strings][-1]
            loguru.logger.info(f'{art=}: {price=} {name=} {url=}')
            pass


if __name__ == '__main__':
    html_filepath = pathlib.Path(__file__).parent / 'grabbed.html'
    if not html_filepath.exists():
        html_filepath.write_text(
            get_html(get_url(), 10)
        )
    html_content = html_filepath.read_text()
    Parse(html_content).parse()
