import time
import requests

last_listing_nb = 0
sleep_time = 30
base_url = "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=Solarians&price=asc"

def check_solarian(r):
  for o in r['offers']:
    for a in o['metadata']['attributes']:
      if ((o['price'] < 12600000000 and (a['value'] == "Prospector" or a['value'] == "Monitor")) or 
      (o['price'] < 14600000000 and (a['value'] == "Pilot" or a['value'] == "Spy")) or 
      (o['price'] < 6600000000 and (a['value'] == "Drone" or a['value'] == "Administrator")) or 
      (o['price'] < 8600000000 and (a['value'] == "Squad Leader" or a['value'] == "Guard"))):
        print("-------------------------------------------")
        print("Alert: %s at %.2f!" %(a['value'], (o['price'] / 1000000000)))
        print("https://digitaleyes.market/item/%s" %(o['mint']))
        print("-------------------------------------------")

while True:
  print('GM, checking if there are new listings ...')
  r = requests.get(base_url).json()
  # conflict with namespace count, workaround below
  r['nb_offers'] = r.pop('count')
  if r['nb_offers'] != last_listing_nb:
    print("New listings, checking ...")
    last_listing_nb = r['nb_offers']
    check_solarian(r)
    # must improve that to check until a defined stop price
    for i in range(0, 10):
      next_cursor = r['next_cursor']
      r = requests.get(base_url + "&cursor=" + next_cursor).json()
      check_solarian(r)
  else:
    print("No new offers.")
  print("Sleeping for %d seconds, GN!" %(sleep_time))
  time.sleep(sleep_time)