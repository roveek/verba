import pydantic


class Card(pydantic.BaseModel):
    art: str = pydantic.Field(title='Артикул')
    name: str = pydantic.Field(title='Название')
    price: str = pydantic.Field(title='Цена')
    url: str = pydantic.Field(title='Ссылка на товар')
