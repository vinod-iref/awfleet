import json
import requests
import code

class Demand():

    def __init__(self, region='ap-southeast-1', instanceType='m4.large', operatingSystem='Linux'):
        self.url = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/{}/index.json'.format(region)
        self.instanceType = instanceType
        self.operatingSystem = operatingSystem
        pass

    def get_price(self):
        response = requests.get(self.url)
        offers = json.loads(response.text)
        # code.interact(local=locals())
        SKU = [sku for sku in offers['products'] if offers['products'][sku]['attributes'].get('instanceType') == self.instanceType and offers['products'][sku]['attributes'].get('operatingSystem') == self.operatingSystem][0]
        SKU_TERM = [sku_term for sku_term in offers['terms']['OnDemand'][SKU] if offers['terms']['OnDemand'][SKU][sku_term]['sku'] == SKU][0]
        priceDimensionKey = offers['terms']['OnDemand'][SKU][SKU_TERM]['priceDimensions'].keys()[0]
        price = offers['terms']['OnDemand'][SKU][SKU_TERM]['priceDimensions'][priceDimensionKey]['pricePerUnit']['USD']
        return price