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

		# authorization cookies
		self.cookies = {
			'_CIAN_GK': '4b4aff7e-fb50-4c52-9b9c-35732a09c330',
			'login_mro_popup': '1',
			'_gcl_au': '1.1.1300089357.1666600808',
			'sopr_utm': '%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D',
			'sopr_session': 'c22aef1afce14b84',
			'uxfb_usertype': 'searcher',
			'tmr_lvid': 'f2840dee4ff9efb54d3173f30c7c3d89',
			'tmr_lvidTS': '1666600807718',
			'_ga': 'GA1.2.833930558.1666600808',
			'_gid': 'GA1.2.1973130906.1666600808',
			'_ym_uid': '1666600808446082172',
			'_ym_d': '1666600808',
			'_ym_isad': '2',
			'_ym_visorc': 'b',
			'_gpVisits': '{"isFirstVisitDomain":true,"todayD":"Mon%20Oct%2024%202022","idContainer":"10002511"}',
			'afUserId': '248c1b66-fe9c-479e-baef-cad7986a985c-p',
			'uxs_uid': '77860980-5377-11ed-ba61-2dc86c550b54',
			'AF_SYNC': '1666600808988',
			'adrdel': '1',
			'adrcid': 'A1f7g0U7lPM1O35k0H4iUsg',
			'cookie_agreement_accepted': '1',
			'session_region_id': '1',
			'session_main_town_region_id': '1',
			'_gp10002511': '{"hits":3,"vc":1,"ac":1,"a6":1}',
			'_cc_id': 'f0bc1831a1ad31f904c2665249be87ee',
			'panoramaId_expiry': '1667206794838',
			'panoramaId': 'a474a8b86a9cdab02875a8b5d46b16d53938f8b99a771ef5749a9bb39fe6cf7e',
			'tmr_detect': '0%7C1666601624882',
			'__cf_bm': 'yqj6H5VfkxeJPOL8qraMl3kaLj7HoHKAWKtDrYyWaQE-1666602085-0-AV6gIKBcj/ZEPceikyh0l2x5qRJWOdmKaNu/9YMGhs6baHbwSMpMhGa7KEBVWigANzHJ9ssfBssAYL2zx+xv6HA=',
			'tmr_reqNum': '14',
		}

		self.headers = {
			'authority': 'www.cian.ru',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
			'cache-control': 'max-age=0',
			# Requests sorts cookies= alphabetically
			# 'cookie': '_CIAN_GK=4b4aff7e-fb50-4c52-9b9c-35732a09c330; login_mro_popup=1; _gcl_au=1.1.1300089357.1666600808; sopr_utm=%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D; sopr_session=c22aef1afce14b84; uxfb_usertype=searcher; tmr_lvid=f2840dee4ff9efb54d3173f30c7c3d89; tmr_lvidTS=1666600807718; _ga=GA1.2.833930558.1666600808; _gid=GA1.2.1973130906.1666600808; _ym_uid=1666600808446082172; _ym_d=1666600808; _ym_isad=2; _ym_visorc=b; _gpVisits={"isFirstVisitDomain":true,"todayD":"Mon%20Oct%2024%202022","idContainer":"10002511"}; afUserId=248c1b66-fe9c-479e-baef-cad7986a985c-p; uxs_uid=77860980-5377-11ed-ba61-2dc86c550b54; AF_SYNC=1666600808988; adrdel=1; adrcid=A1f7g0U7lPM1O35k0H4iUsg; cookie_agreement_accepted=1; session_region_id=1; session_main_town_region_id=1; _gp10002511={"hits":3,"vc":1,"ac":1,"a6":1}; _cc_id=f0bc1831a1ad31f904c2665249be87ee; panoramaId_expiry=1667206794838; panoramaId=a474a8b86a9cdab02875a8b5d46b16d53938f8b99a771ef5749a9bb39fe6cf7e; tmr_detect=0%7C1666601624882; __cf_bm=yqj6H5VfkxeJPOL8qraMl3kaLj7HoHKAWKtDrYyWaQE-1666602085-0-AV6gIKBcj/ZEPceikyh0l2x5qRJWOdmKaNu/9YMGhs6baHbwSMpMhGa7KEBVWigANzHJ9ssfBssAYL2zx+xv6HA=; tmr_reqNum=14',
			'if-none-match': 'W/"24d405-xC3keC+RGp/cAQUOcXik+5JGVsQ"',
			'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
			'sec-fetch-dest': 'document',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-site': 'none',
			'sec-fetch-user': '?1',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
		}

		self.type_dict_ = {
			"rent": "rent",
			"buy": "sale"
		}

		self.building_type_dict_ = {
			"company": None,
			"private": 1,
			"": None,
			None: None
		}

		self.link_api_ = "https://api.cian.ru"

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
			type_: str = None,  # buy / rent
			building_type: str = None,  # company / private
			location_id: int = 1,
			price_from: int = None,
			price_to: int = None,
	) -> str:
		"""getting url for further getting items from cian

		Args:
			type_ (str, optional): buy / rent.
			building_type (str, optional): 
				private - частная  /  company - компания. Defaults to None
			
			location_id (int, optional): CianApi.get_location_id() result. Defaults to 1.
			price_from (int, optional): _description_. Defaults to None.
			price_to (int, optional): _description_. Defaults to None.

		Returns:
			str: url for future parsing with pars_page()
		"""
		# get request params
		params = {
			'currency': '2',
			'deal_type': self.type_dict_.get(type_),
			'engine_version': '2',
			'maxprice': price_to,
			'minprice': price_from,
			'offer_type': 'flat',
			'region': location_id,
			'is_by_homeowner': self.building_type_dict_[building_type],
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

		print(f"Url to parse content: {url_to_parse_}")

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

	def parse_page(self, url: str) -> dict:
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

	def get_location_id(self, keyword_: str) -> int:
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

		url = self._get_req_url(f"{self.link_api_}/geo-suggest/v2/suggest/", params)

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
