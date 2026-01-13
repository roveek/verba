import pathlib
import typing

import openpyxl

import models

products_filepath = pathlib.Path(__file__).parent / '_products.xlsx'


class XlsxWriter:

    def save_cards(self, cards: typing.Iterable[models.Card]) -> None:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws_title = [field['title'] for field in
                   models.Card.model_json_schema()['properties'].values()]
        ws.append(ws_title)
        for card in cards:
            row = [*card.model_dump().values()]
            ws.append(row)
        wb.save(products_filepath)
