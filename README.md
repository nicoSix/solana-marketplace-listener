# Solana marketplace listener

Listener for Solana marketplaces (DigitalEyes and Solanart) listings, alerts when target is under a defined price.

## How to setup

1. Enter in the listen_for.json file the collection and attributes you want, following the template already in place.
2. Enter in collection_mapping.json the mapping from the collection name defined in listen_for.json and real collection names on DE/Solanart if needed.
3. Run the bot using python listen.py. You can also configure the sleep time (default: 15s) in the code.
4. Profit
