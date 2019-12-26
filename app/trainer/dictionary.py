import requests
from bs4 import BeautifulSoup

class Parcer():
    def getPageWitfoundedWord(self, word):
        payload = {'term': word, 'lang': 'beld'}
        r = requests.get('https://www.skarnik.by/search', params = payload)
        soup = BeautifulSoup(r.text, "lxml")
        return soup
    def getExplanationOfWord(self, soup):
        data=[]
        try:
            data = list(filter(None, soup.find(id="trn").text.split('\xa0')))
            data[0] = soup.title.text
        except:
            tags = soup.div.find_all(class_="span10")
            for tag in tags:
                try:
                    data.append(tag.find('p').text)
                    break
                except:
                    continue
        return data
