import typing

import bs4

import models


class Parse:
    __soap = None

    def __init__(self, html: str):
        self._html = html

    def iter_cards(self) -> typing.Iterable[models.Card]:
        for card_tag in self._iter_card_tags():
            card_dto = models.Card(
                name=[*card_tag.select_one('h2').stripped_strings][-1],
                url=card_tag.select_one('a.product-card__link').attrs['href'],
                art=card_tag.attrs['data-nm-id'],
                price=[*card_tag.select_one('ins').stripped_strings][-1],
            )
            # loguru.logger.info(f'{card_dto=}')
            yield card_dto

    @property
    def _soap(self):
        if self.__soap is None:
            self.__soap = bs4.BeautifulSoup(self._html, 'lxml')
        return self.__soap

    def _iter_card_tags(self):
        yield from self._soap.find_all('article', class_='product-card')
