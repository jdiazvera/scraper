import sys, os

class Item:
    def __init__(self, soup):
        self._soup = soup

        self.title = self._title()
        self.price = self._price()
        self.description = self._description()

    def _title(self):
        try:
            # Outer Tag Object
            title = self._soup.find("span", attrs={"id": 'productTitle'})
            # Inner NavigableString Object
            title_value = title.string
            # Title as a string value
            title_string = title_value.strip()

        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("_title >>> ", exc_type, fname, exc_tb.tb_lineno, err, title)
            title_string = ""

        return title_string
    
    def _price(self):    
        try:
            old_price = ''
            price = ''

            # if self._soup.find_all("span", {"class": "priceblock_ourprice"}):
            if self._soup.find_all("span", {"class": "priceBlockBuyingPriceString"}):
                price = (self._soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()).replace('US$\xa0', '')
            if self._soup.find_all("span", {"class": "priceBlockStrikePriceString"}):
                old_price = (self._soup.find("span", attrs={'class': 'priceBlockStrikePriceString'}).string.strip()).replace('US$\xa0', '')

        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("_price >>> ",exc_type, fname, exc_tb.tb_lineno, err)
            price = ''
            old_price = ''

        return {"old_price": old_price,"price":price}
    
    def _description(self):
        try:
            description = self._soup.find("div", attrs={'id': 'productDescription'}).p
            description_string = description.string
        
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("_description >>> ",exc_type, fname, exc_tb.tb_lineno, err)
            description_string = ''
            
        return description_string
    