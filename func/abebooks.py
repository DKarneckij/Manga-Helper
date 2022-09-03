from logging import NullHandler
import requests

'''
NOT MY CODE
This code comes from https://github.com/ravila4/abebooks/blob/master/abebooks.py
I wasn't sure how to get it to work as an import, and made a slight adjustment to it
'''

class AbeBooks:

    def __get_price(self, payload):
        url = "https://www.abebooks.com/servlet/DWRestService/pricingservice"
        resp = requests.post(url, data=payload)
        if resp.status_code == 429:
            return None
        return resp.json()

    def getPriceByISBN(self, isbn):
        """
        Parameters
        ----------
        isbn (int) - a book's ISBN code
        """
        payload = {'action': 'getPricingDataByISBN',
                   'isbn': isbn,
                   'container': 'pricingService-{}'.format(isbn)}
        return self.__get_price(payload)

    