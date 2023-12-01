import requests
import chardet
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

url = "https://www.fantasynamegenerators.com/dnd-bugbear-names.php"
response = requests.get(url, headers = headers)
content = response.content
# encoding = chardet.detect(response.content)['encoding']
# content = response.content.decode(encoding, errors='replace')
soup = BeautifulSoup(content.decode("UTF-8"),"html.parser")
# results = soup.find("div", id="result")
print(content)

