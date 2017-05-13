import requests
import time
import json
import code

class Spot():
	"""docstring for spot"""
	def __init__(self,region_name='apac-sin',size='m4.large',instanceType='generalCurrentGen'):
		self.spot_pricing_url = "https://spot-price.s3.amazonaws.com/spot.js?callback=callback&_={:d}"
		self.region_name = region_name
		self.instanceType = instanceType
		self.size = size
		
	def get_price(self):
		time_now = int(time.time())*1000 # Time in micro seconds
		r =requests.get(self.spot_pricing_url.format(time_now))
		data = None
		if r.status_code == 200:
			prices = self.extract_json(r.content)
			region = self.filter_region_data(prices['config']['regions'],self.region_name)
			instance = self.filter_by_instance(region['instanceTypes'],self.instanceType)
			size = self.filter_by_size(instance['sizes'],self.size)
			data = size['valueColumns']
		return data

	def extract_json(self,content):
		# Remove callback
		extract_str = content[9:-2]
		return json.loads(extract_str)

	def filter_region_data(self,regions,region_name):
		required_region = None
		for region in regions:
			if region['region'] == region_name:
				required_region = region
				break
		return required_region

	def filter_by_instance(self,instances,instanceType_name):
		required_instance = None
		for instance in instances:
			if instance['type'] == instanceType_name:
				required_instance = instance
				break
		return required_instance

	def filter_by_size(self,sizes,size_name):
		required_size = None
		for size in sizes:
			if size['size'] == size_name:
				required_size = size
				break
		return required_size

