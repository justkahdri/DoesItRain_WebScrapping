BSAS_NOW_URL = 'https://www.accuweather.com/es/ar/buenos-aires/7894/weather-forecast/7894'
XPATH_TEMPS = '//div[@class="temp"]/text()'     # Now, Tonight, Tomorrow
XPATH_STATS = '//span[@class="value"]/text()'   # Air Quality, Wind, Strong Wind
XPATH_STATE = '//span[@class="phrase"]/text()'
# XPATH_LINK_TO_HOURLY = '//a[@data-gaid="hourly"]/@href'

BSAS_HOURLY_URL = 'https://www.accuweather.com/es/ar/buenos-aires/7894/hourly-weather-forecast/7894?day='
XPATH_HOURS = '//h2[@class="date"]/span[not(@class)]/text()'
XPATH_PERCENTAGES = '//div[@class="precip"]/text()'

DAYS = ['today', 'tomorrow']
