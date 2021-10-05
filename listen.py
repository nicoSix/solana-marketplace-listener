import time
import requests
import json

last_listing_nb = 0
sleep_time = 15
base_url_de = "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?price=asc&collection="
base_url_solanart = "https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection="
token_url_de = "https://digitaleyes.market/item/"
token_url_solanart = "https://solanart.io/search/?token="

def get_attributes():
  with open('listen_for.json') as json_file:
    return json.load(json_file)

def get_collection_mapping():
  with open('collection_mapping.json') as json_file:
    return json.load(json_file)
    
attributes = get_attributes()
collection_mapping = get_collection_mapping()

def filter_solanart(r, attr):
  filtered_array = []
  for offer in r:
    attributes = offer['attributes'].split(',')
    for attribute in attributes:
      attribute_mapping = attribute.split(': ')
      if attribute_mapping[0] == attr['attribute_name'] and attribute_mapping[1] == attr['attribute_value']:
        filtered_array.append(offer)

  return filtered_array

def get_token_url(site):
  if site == 'solanart':
    return token_url_solanart
  else:
    return token_url_de

def get_solanart(attr):
  r = requests.get(base_url_solanart + collection_mapping[attr['collection']]['solanart']).json()
  filtered_offers = filter_solanart(r, attr)
  parsed_results = []
  for offer in filtered_offers:
    parsed_results.append({
      "price": offer['price'],
      "mint": offer['token_add'],
      "site": "solanart"
    })
  return parsed_results

def get_de(attr):
  r = requests.get(base_url_de + collection_mapping[attr['collection']]['de'] + "&" + attr['attribute_name'] + "=" + attr['attribute_value']).json()
  offers = r['offers']
  parsed_offers = []
  for offer in offers:
    parsed_offers.append({
      "price": (offer['price'] / 1000000000),
      "mint": offer['mint'],
      "site": "de"
    })
  return parsed_offers

def check_attribute(r, attr):
  for offer in r:
    if ((offer['price'] < attr['value'])):
        print("-------------------------------------------")
        print("Alert: %s at %.2f!" %(attr['attribute_value'], (offer['price'])))
        print(get_token_url(offer['site']) + "%s" %(offer['mint']))
        print("-------------------------------------------")

while True:
  print('GM, checking for good deals ...')
  for attr in attributes:
    if len(collection_mapping[attr['collection']]['de']):
      r_de = get_de(attr)
    else:
      r_de = []
    if len(collection_mapping[attr['collection']]['solanart']): 
      r_solanart = get_solanart(attr)
    else:
      r_solanart = []
      
    r = r_de + r_solanart
    check_attribute(r, attr)
  print("Sleeping for %d seconds, GN!" %(sleep_time))
  time.sleep(sleep_time)