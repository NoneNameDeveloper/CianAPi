
<h1 align="center">ПОКА НЕ ПОДДЕРЖИВАЕТСЯ</h1>
<br>
<h1 align="center">🏠 Cian API wrapper in Python</h1>

<h3 align="center">This api will help you get items from <a href="https://www.cian.ru/">Cian</a> with different filters<h3>


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

from cianapi.models import Item

# initializing cian object
cian = CianApi()

# location for parsing
city = "Москва"

# getting items list
items: list[Item] = cian.parse_items(
    buy_type="buy",
    building_type="private",
    location=city,
    price_from=1_000_000,
    price_to=3_000_000
)
```

