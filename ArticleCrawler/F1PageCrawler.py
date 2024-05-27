import requests as re

mainPageUrl = "https://www.formula1.com/en/latest/all?articleFilters=&page=2"

get = re.get(mainPageUrl)
print(get.text)
