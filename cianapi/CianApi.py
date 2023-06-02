from typing import Dict
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from cianapi.utils import convert_date_time
from cianapi.models import Item


class CianApi:
	"""cian mobile api wrapper"""

	def __init__(self):
		"""__init__ function"""

		self._type_dict_: dict = {
			"rent": "rent",
			"buy": "sale"
		}

		self._building_type_dict_: dict = {
			"company": None,
			"private": 1,
			"": None,
			None: None
		}

		self._link_api_: str = "https://api.cian.ru"

		self.city: str = "Москва"

	@staticmethod
	def _initialize_driver() -> webdriver:
		"""initialize selenium webdriver instance

		Args:
				debug (bool, optional): using in debug mode or not. Defaults to False.

		Returns:
				webdriver: selenium.webdriver module
		"""

		chrome_options = webdriver.ChromeOptions()

		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--enable-javascript')
		chrome_options.add_argument(
			"--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument('--allow-insecure-localhost')
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

		# installing webdriver object
		w_object = ChromeDriverManager().install()

		return webdriver.Chrome(w_object, options=chrome_options)

	def get_url_to_pars(
			self,
			buy_type: str = None,  # buy / rent
			building_type: str = None,  # company / private
			location: str = "Москва",  # city
			price_from: int = None,
			price_to: int = None,
	) -> str:
		"""getting url for further getting items from cian

		Args:
			buy_type (str, optional): buy / rent.
			building_type (str, optional): 
				private - частная  /  company - компания. Defaults to None
			
			location (str, optional): city name. Defaults to Москва.
			price_from (int, optional): _description_. Defaults to None.
			price_to (int, optional): _description_. Defaults to None.

		Returns:
			str: url for future parsing with pars_page()
		"""
		location_id: int = self._get_location_id(location)

		# get request params
		params = {
			'currency': '2',
			'deal_type': self._type_dict_.get(buy_type),
			'engine_version': '2',
			'maxprice': price_to,
			'minprice': price_from,
			'offer_type': 'flat',
			'region': location_id,
			'is_by_homeowner': self._building_type_dict_[building_type],
			'room1': '1',
			'room2': '1',
			'room3': '1',
			'room4': '1',
			'room5': '1',
			'room6': '1',
			'sort': 'creation_date_desc'
		}

		url = "https://www.cian.ru/cat.php"
		url_to_parse_ = self._get_req_url(url, params)

		return url_to_parse_

	def get_soup(self, url: str) -> BeautifulSoup:
		"""getting bs4 object of the web page

		Args:
			url (str): _description_

		Returns:
			BeautifulSoup: _description_
		"""
		# getting html data from page
		html_ = self._request_usual(url)

		soup = BeautifulSoup(html_, features="html.parser")

		return soup

	def parse_page(self, url: str) -> list[Item]:
		"""scraping html tags from html

		Args:
			url (str): link for parsing

		Returns:
			dict: items
		"""
		# getting BeautifulSoup object
		soup = self.get_soup(url)

		# will be out
		result_ = []

		main_adverts = soup.find("div", attrs={"id": "frontend-serp"}).find("div").find("div", attrs={
			"class": "_93444fe79c--wrapper--W0WqH"}).find_all("article", attrs={"data-name": "CardComponent"})
		u = 0
		for ad in main_adverts:
			u += 1
			div_1 = ad.find("div")

			main_div_ = div_1.find("div", attrs={"class": "_93444fe79c--content--lXy9G"})

			# getting title
			ad_title_ = main_div_.find("div").find("div").find(
				"div").find("span").find("span").text.strip()

			# getting ad link
			ad_link_ = main_div_.find("div").find("div").a[
				"href"]

			# Getting price. default price (unhandled) is 0. Running through 4 <div>
			ad_price_ = 0
			for i in range(4):
				try:
					ad_price_ = \
						main_div_.find("div").find(
							"div").find_all(
							"div", attrs={"class": "_93444fe79c--row--kEHOK"})[i].find("div").find(
							"span").text.strip().replace("&nbsp;", "").replace(u'\xa0', u' ')
				except:
					pass

			# getting ad adress
			ad_adress_parent_ = main_div_.find('div').find(
				'div').find("div", attrs={"class": "_93444fe79c--labels--L8WyJ"}).find_all("a")
			ad_adress_ = ""
			# contatenation of adress parts
			for a in ad_adress_parent_:
				ad_adress_ += a.text.strip() + ", "
			# removing last 2 symbols
			ad_adress_ = ad_adress_[:-2]

			# type of seller (Агенство, риэлтор..)
			ad_seller_type_ = main_div_.find("div", attrs={
				'class': '_93444fe79c--aside--ygGB3'}).find("div", attrs={'class': "_93444fe79c--agent--HG9xn"}).find(
				"div").find("div", attrs={"class": "_93444fe79c--contact--pa2PA"}).find_all("div")[1].find("div").find(
				"div").span.text.strip()

			# div with seller information
			seller_div_ = main_div_.find("div", attrs={
				'class': '_93444fe79c--aside--ygGB3'}).find("div", attrs={'class': "_93444fe79c--agent--HG9xn"}).find(
				"div").find("div", attrs={"class": "_93444fe79c--contact--pa2PA"}).find_all("div")[1].find("div").find(
				"div").find("div", attrs={"class": "_93444fe79c--name-container--enElO"})

			# getting name of seller
			ad_seller_name_ = seller_div_.text.strip()

			# getting link of seller
			try:
				ad_seller_link_ = seller_div_.a['href']
			except:
				ad_seller_link_ = "https://www.cian.ru/agents/" + ad_seller_name_.replace("ID ", "")

			try:
				# getting array of 5 photos
				ad_photo_links_parent_ = div_1.find(
					"div", attrs={"class": "_93444fe79c--media--9P6wN"}).find(
					"div", attrs={"class": "_93444fe79c--cont--hnKQl"}).find(
					"div", attrs={"class": "_93444fe79c--container--IxdhQ _93444fe79c--container--column--Z9Ik1"}).ul.find_all(
					"li")
				ad_photo_links_ = [p.img['src'] for p in ad_photo_links_parent_]
				if len(ad_photo_links_) >= 5:
					ad_photo_links_ = ad_photo_links_[:5]
			except:
				# empty photo
				ad_photo_links_ = [
					"https://telegra.ph/file/2f15a97d110e405668b5d.png",
					"https://telegra.ph/file/2f15a97d110e405668b5d.png"
				]

			# getting item post date in cian format
			ad_post_date_ = main_div_.find(
				"div", attrs={"class": "_93444fe79c--aside--ygGB3"}).find(
				"div", attrs={"class": "_93444fe79c--vas--ojM2L"}).find(
				"div", attrs={"class": "_93444fe79c--timeLabel--_VT26"}).find(
				"div", attrs={"class": "_93444fe79c--absolute--yut0v"}).find("span").text.strip()

			# converting post date to human/machine-readable format
			ad_post_date_ = convert_date_time(ad_post_date_)

			# creating result object
			result_dict = {
					"title": ad_title_,
					"link": ad_link_,
					"adress": ad_adress_,
					"price": ad_price_,
					"seller":
						{
							"type_": ad_seller_type_,
							"profile_link": ad_seller_link_,
							"name": ad_seller_name_
						},
					"photos": ad_photo_links_,
					"post_date": ad_post_date_
				}

			item = Item.parse_obj(result_dict)
			result_.append(item)

		return result_

	def parse_items(
			self,
			buy_type: str = None,  # buy / rent
			building_type: str = None,  # company / private
			location: str = "Москва",  # city
			price_from: int = None,
			price_to: int = None,
	) -> list[Item]:

		# getting url to parsing
		url_: str = self.get_url_to_pars(buy_type, building_type, location, price_from, price_to)

		return self.parse_page(url_)

	def _get_location_id(self, keyword_: str) -> int:
		"""getting location id by user's input

		Args:
			keyword_ (str): location (user input)
		
		Returns:
			int: location id

		"""
		params = {
			"query": keyword_,
			"regionId": "1",
			"isCoworkingSearch": "false",
			"dealType": "sale",
			"offerType": "flat",
			"source": "mainpage",
		}

		url = self._get_req_url(f"{self._link_api_}/geo-suggest/v2/suggest/", params)

		result = self._request_api(url)

		if not result['data']['suggestions']['cities']['items']:
			return 1

		return result['data']['suggestions']['cities']['items'][0]['id']

	def _get_req_url(self, url: str, params: dict) -> str:
		"""getting url formated with get-request payload

		Args:
			url (str): full path to method 
			params (dict): get-request payload

		Returns:
			str: url with formatted get request
		"""
		req = requests.get(url, params=params)

		return req.url

	def _request_usual(self, url: str) -> Dict:
		"""getting json data with items

		Args:
				url (str): API method link

		Returns:
				Dict: json result from API
		"""

		driver = self._initialize_driver()
		driver.set_window_size(1920, 1080)
		tz_params = {'timezoneId': 'Asia/Omsk'}
		driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

		driver.get(url)

		content = driver.page_source

		return content

	def _request_api(self, url: str) -> Dict:
		"""getting json data with items

		Args:
			url (str): API method link

		Returns:
			Dict: json result from API
		"""

		driver = self._initialize_driver()
		driver.set_window_size(1920, 1080)
		tz_params = {'timezoneId': 'Asia/Omsk'}
		driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

		driver.get(url)

		content = driver.find_element(By.TAG_NAME, "pre").text

		result = json.loads(content)

		driver.quit()

		if result["status"] == "forbidden":
			return self._request_api(url)

		return result


	def _request(self, url: str, params: dict) -> str:
		"""making request to cian private api

		Args:
			url (str): path to api method
			params (dict): get-request parametrs to the api (data)
		"""
		url = url
		headers = {} # self.headers
		cookies = {} # self.cookies

		with requests.session() as session:
			result_ = session.get(
				url=url, params=params, headers=headers, cookies=cookies
			).text

			return result_
