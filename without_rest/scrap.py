
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint as p

url = "https://suvarnabhumi.airportthai.co.th/flight"
raw = requests.get(url)
soup = bs(raw.text, 'html.parser')
# p(soup.prettify())

input = soup.find_all("flatpickr-input")
print(input)