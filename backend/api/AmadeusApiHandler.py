from locale import currency
from typing import Hashable
from amadeus import Client, ResponseError
import json

class AmadeusApiHandler():

    def __init__(self):
        self.amadeus = Client(
            client_id='CLIENT_ID_###',
            client_secret='CLIENT_API_KEY'
        )
    
    # Generate condensed JSON data to better manipulate in the front-end
    # price, airline name, flight time, 
    def parseResponse(self, responseData):
        myList =  []
        for item in responseData.data:
            for itinerary in item["itineraries"]:
                for segment in itinerary["segments"]:
                    # convert airline code to airline name
                    #airline = self.convertAirlineCode(segment.get('operating',{}).get('carrierCode',{}))
                    airline = self.convertCarrierCode(segment.get('operating',{}).get('carrierCode',{}))
                    myList.append(
                        {
                            'airline': airline,
                            'arrivalAirport': segment.get('arrival',{}).get('iataCode',{}),
                            'arrivalTime': segment.get('arrival',{}).get('at',{}),
                            'arrivalTerminal' : segment.get('arrival', {}).get('terminal',{}),
                            'departureAirport' : segment.get('departure',{}).get('iataCode',{}),
                            'departureTime' : segment.get('departure',{}).get('at',{}),
                            'departureTerminal' : segment.get('departure',{}).get('terminal',{}),
                            'flightTime' : segment.get('duration', {}),
                            'price' : item.get('price', {}).get('grandTotal', {})
                        }
                    )
        return myList
        #raise Exception("Airline/carrier code not found")

    # Makes a call to the AmadeusAPI
    # Problem: slow
    def convertAirlineCode(self,code, cache = {}):
        try:
            return cache[code]
        except (KeyError, AttributeError, TypeError):
            try:
                response = self.amadeus.reference_data.airlines.get(airlineCodes=code)
                cache[code] = response.data[0].get('businessName', {})
                print("This is the cache ", cache)
                return cache[code]
                
            except (ResponseError, TypeError):
                return {}

    # Searches for carrier code and carrier name match in carriers.json
    def convertCarrierCode(self, code):
        with open("../backend/data/carriers.json", encoding="utf-8") as f:
            data = json.loads(f.read())
        
        for i in data:
            if i["Code"] == code:
                #print(i["Description"])
                return i["Description"]
        return {}
           

                    

    def getData(self,olc, dlc,dd,a):
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                #originLocationCode="BOS",
                originLocationCode=olc,
                destinationLocationCode=dlc,
                departureDate=dd,
                currencyCode="USD",
                adults=a,
                max = 100 
        )   
        #get price

            # price = self.amadeus.shopping.flight_offers_search.get(originLocationCode='SYD', destinationLocationCode='BKK', departureDate='2022-11-01', adults=1).data
            # self.amadeus.shopping.flight_offers.pricing.post(price[0])
            # self.amadeus.shopping.flight_offers.pricing.post(price[0:2], include='credit-card-fees,other-services')
            # price = self.amadeus.analytics.itinerary_price_metrics.get(
            #      originIataCode = "BOS",
            #      destinationIataCode = dlc,
            #      departureDate = dd
            #  )

        # #get hotel
              #hotels = self.amadeus.reference_data.locations.hotels.by_city.get(cityCode=dlc)
        #     hotelOffer = self.amadeus.shopping.hotel_offers_search.get(hotelIds='RTPAR001', adults='2')
        #     hotelRating = self.amadeus.e_reputation.hotel_sentiments.get(hotelIds = 'ADNYCCTB')
            # for item in response.data:
            #     for itinerary in item["itineraries"]:
            #         for segment in itinerary["segments"]:
            #             print(f"Flight departing {segment['departure']['iataCode']} at {segment['departure']['at']} going to {segment['arrival']['iataCode']} at {segment['arrival']['at']} for a total price of {item['price']['grandTotal']}{item['price']['currency']} ")
            
            print(self.parseResponse(response))
            return response.data

            # for item in response.data:
            #     for itinerary in item["itineraries"]:
            #         for segment in itinerary["segments"]:
            #             if segment["departure"]["iataCode"] == olc and segment["arrival"]["iataCode"] == ddlc:
            #                 return item["price"]["grandtotal"]
                
                
        except ResponseError as e:
            print(e)
            return e
