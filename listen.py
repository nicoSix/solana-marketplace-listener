import time
import requests
import json

last_listing_nb = 0
sleep_time = 15
base_url = "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?price=asc&collection="

def check_attribute(r, attr):
  for o in r['offers']:
    for a in o['metadata']['attributes']:
      if ((o['price'] < attr['value']) and (a['value'] == attr['attribute'])):
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
    r = requests.get(base_url + attr['collection']).json()
    # conflict with namespace count, workaround below
    r['nb_offers'] = r.pop('count')
    last_listing_nb = r['nb_offers']
    check_attribute(r, attr)
    # must improve that to check until a defined stop price
    for i in range(0, 3):
      next_cursor = r['next_cursor']
      r = requests.get(base_url + attr['collection'] + "&cursor=" + next_cursor + "&collection=").json()
      check_attribute(r, attr)
  print("Sleeping for %d seconds, GN!" %(sleep_time))
  time.sleep(sleep_time)