from logging import NullHandler
import requests

'''
NOT MY CODE
This code comes from https://github.com/ravila4/abebooks/blob/master/abebooks.py
'''


def getPriceByISBN(self, isbn):
    """
    Parameters
    ----------
    isbn (int) - a book's ISBN code
    """
    payload = {'action': 'getPricingDataByISBN',
                'isbn': isbn,
                'container': 'pricingService-{}'.format(isbn)}
    abe = self.__get_price(payload)

    if abe == None:
        return "Error"

    if abe['success']:
        available = [abe['pricingInfoForBestNew'], abe['pricingInfoForBestUsed']]
        available = [float(x['bestPriceInPurchaseCurrencyWithCurrencySymbol'][4:].replace(',','')) for x in available if x is not None]
        return (min(available))
    
    return '--'
    
def __get_price(self, payload):
    url = "https://www.abebooks.com/servlet/DWRestService/pricingservice"
    resp = requests.post(url, data=payload)
    if resp.status_code == 429:
        return None
    return resp.json()

    