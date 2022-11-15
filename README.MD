<h1 align="center">🏠 Cian API</h1>

<h3 align="center">This api will help you get items from <a href="https://www.cian.ru/">Cian</a><h3>

#
## Installation

Install CianAPi with git
```bash
  git clone https://github.com/NoneNameDeveloper/CianAPi
```

Go to directory
```bash
cd CianApi
```

Install requirements
```bash
pip3 install -r requirements.txt
```

Now you can develop your project  
#

## Usage/Examples
```python
from cianapi.CianApi import CianApi

cian = CianApi()

city = "Москва"
location_id = cian.get_location_id(city)

url = cian.get_url_to_pars(
    type_ = "rent",
    building_type = "private",
    location_id = location_id,
)

items = cian.parse_page(url)
```

