import amadeus
from flask_restful import Api,Resource, reqparse, request
import json
import os
from collections import defaultdict

from backend.api.AmadeusApiHandler import AmadeusApiHandler

class SearchHandler(Resource):

    iata_code = ""
    airport_name = ""

    def __init__(self):
        self.amadeusApi = AmadeusApiHandler()

    def get(self):
        args = request.args
        startingCity = "".join(args.getlist('startingCity')[0]).lower().title()
        print(startingCity)
        endingCity = "".join(args.getlist('endingCity')[0]).lower().title()
        start_iata_code = self.findMatch(startingCity)
        end_iata_code = self.findMatch(endingCity)
        amadeusResponse = self.amadeusApi.getData(
                                start_iata_code,
                                end_iata_code,
                                args.getlist('startDate')[0],
                                args.getlist('numAdults')[0]
                                )
        return amadeusResponse

    def findMatch(self, user_input):
        with open("../backend/data/airports.json", encoding="utf-8") as f:
            data = json.loads(f.read())
        #user_input = "New York"

        for i in data.keys():
            for j in data.values():
                if j["city"] == user_input.lower().title():
                    #print(j["iata"])
                    code = j["iata"]
                    #print(j["name"])
                    return code
        raise Exception("City not found")



        exampleCost = [5,2,3]
        exampleAirport = ["a","b","c"]
        #loop through the resultList and add to dictionary, then sort by price
        for i in range(len(exampleCost)):
            result[(exampleAirport[i])] = (exampleCost[i])

        print(sorted(result.items(), key=lambda x: x[1]))


    
                    
            
                
                    
        


        
