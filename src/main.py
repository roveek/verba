import pathlib
import time

import loguru
import playwright.sync_api
import playwright_stealth

import parser
import xlsx

html_filepath = pathlib.Path(__file__).parent / '_grabbed.html'
parse_url = 'https://www.wildberries.ru/catalog/0/search.aspx?search={search_string}'
search_string = 'пальто из натуральной шерсти'


@loguru.logger.catch(reraise=True)
def fetch_html(url: str, wait: int = 10) -> str:
    """Возвращает html страницы"""
    with playwright.sync_api.sync_playwright() as pw:
        browser = pw.chromium.launch(
            # headless=True,
            headless=False,
            slow_mo=300,
        )
        page = browser.new_page()

        playwright_stealth.Stealth().apply_stealth_sync(page)

        page.goto(url, wait_until="networkidle")  # ждём загрузки

        loguru.logger.info('Waiting {} seconds...', wait)
        time.sleep(wait)

        html = page.content()  # уже отрендеренный HTML
        loguru.logger.info('Got content {} bytes', len(html))

        browser.close()
        return html


def get_url() -> str:
    return parse_url.format(search_string=search_string)


if __name__ == '__main__':

    if html_filepath.exists():
        html_content = html_filepath.read_text()
    else:
        html_content = fetch_html(get_url())
        html_filepath.write_text(html_content)

    xlsx.XlsxWriter().save_cards(
        parser.Parse(html_content).iter_cards()
    )
