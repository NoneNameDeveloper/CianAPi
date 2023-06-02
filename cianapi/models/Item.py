from datetime import datetime

from pydantic import BaseModel


class Seller(BaseModel):
	type_: str
	profile_link: str
	name: str


class Item(BaseModel):
	title: str
	link: str
	adress: str
	seller: Seller
	photos: list[str]
	post_date: datetime
