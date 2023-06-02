from datetime import datetime, timedelta

from cianapi.helpers import months_translated


def convert_date_time(input_date: str) -> datetime:
	"""
	converting date from cian.ru to datetime python format

		cian format (input_date) - 30 май, 11:19 / вчера, 10:05 / сегодня, 15:04
		output format - 2023-06-02 14:14:00 (datetime python format)
	"""
	# spliting to ['30 май', '11:19']
	date_, time_ = input_date.split(",")

	# if today datetime format
	if "сегодня" in date_:
		date_res = datetime(
			year=datetime.now().date().year,
			month=datetime.now().date().month,
			day=datetime.now().date().day,
			hour=int(time_.split(":")[0]),
			minute=int(time_.split(":")[1])
		)

	elif "вчера" in date_:
		date_res = datetime(
			year=(datetime.now() - timedelta(days=1)).date().year,
			month=(datetime.now() - timedelta(days=1)).date().month,
			day=(datetime.now() - timedelta(days=1)).date().day,
			hour=int(time_.split(":")[0]),
			minute=int(time_.split(":")[1])
		)

	else:
		# split to ['30', 'май']
		date_splitted = date_.split()

		# converting to '30 May'
		date_to_convert = date_splitted[0] + " " + months_translated.get(date_splitted[1])

		# converting to datetime format
		date_converted = datetime.strptime(date_to_convert, '%d %B')

		date_res = datetime(
			year=datetime.now().year,
			month=date_converted.month,
			day=date_converted.day,
			hour=int(time_.split(":")[0]),
			minute=int(time_.split(":")[1])
		)

	return date_res
