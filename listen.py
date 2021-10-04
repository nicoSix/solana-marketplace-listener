import time
import requests
import json

last_listing_nb = 0
sleep_time = 15
base_url = "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?price=asc&collection="

def check_attribute(r, attr):
  for o in r['offers']:
    for a in o['metadata']['attributes']:
      if ((o['price'] < attr['value'])):
        print("-------------------------------------------")
        print("Alert: %s at %.2f!" %(a['value'], (o['price'] / 1000000000)))
        print("https://digitaleyes.market/item/%s" %(o['mint']))
        print("-------------------------------------------")

def get_attributes():
  with open('listen_for.json') as json_file:
    return json.load(json_file)

attributes = get_attributes()

while True:
  print('GM, checking for good deals ...')
  for attr in attributes:
    r = requests.get(base_url + attr['collection'] + "&" + attr['attribute_name'] + "=" + attr['attribute_value']).json()
    # conflict with namespace count, workaround below
    r['nb_offers'] = r.pop('count')
    last_listing_nb = r['nb_offers']
    check_attribute(r, attr)
  print("Sleeping for %d seconds, GN!" %(sleep_time))
  time.sleep(sleep_time)