'''
    www.youtube.com/@Pypelineer
'''

from pypelineer.cores import IngressCore, IngressType

import requests
import dotenv
import os

class ExtractAirbnbListings(IngressCore, Type=IngressType.FUNCTION):
    def constructor(self):
        # Create rapidapi access variables
        RAPIDAPI_TOKEN = os.getenv("RAPIDAPI_TOKEN")
        RAPIDAPI_HEADER = {
            "x-rapidapi-key": RAPIDAPI_TOKEN,
            "x-rapidapi-host": "airbnb-listings.p.rapidapi.com"
        }
        ## save required attributes
        self.header = RAPIDAPI_HEADER
        self.query = {"state" : "US", "offset": 0}
        self.url = "https://airbnb-listings.p.rapidapi.com/v2/listingsByGeoRef"
        
        ## iteration variable
        self.last_extract = 0
        
    def destructor(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            # Handle Exception accordingly
            print(f"{exc_type}:{exc_value}:{traceback}")
        
        # Release resources when necessary
        del self.header

    def available(self):
        # If anything was extracted
        return self.last_extract > 0
    
    def iterate(self):
        # Paginate to next batch
        self.query['offset'] += self.last_extract

    def produce(self):
        response = requests.get(url=self.url,
                                headers=self.header,
                                params=self.query)
        
        data: dict = response.json()
        
        listings: list = data.get('results', [])
        
        # Option 1:
        # return listings
        
        # Option 2:
        yield from listings

if __name__ == "__main__":
    
    with ExtractAirbnbListings() as listings:
        for idx, listing in enumerate(listings, start=1):
            print(f"Listing #{idx}::", listing['airbnb_id'])


