from geopy.distance import geodesic
import requests

class Mapper:

    def __init__(self, coords, homeLocation):
        self.myKey = "myRetractedKey"
        self.coordsOktoberfest = (48.131489099999996,11.549755214131313)
        self.locationName = homeLocation
        if coords:
            self.coordsAirbnb = f"{coords[0]},{coords[1]}"
        else:
            self.coordsAirbnb = None

    def getDistance(self):
        if self.coordsAirbnb:
            distance = self.calculateDistance(self.coordsAirbnb)
        else:
            distance = None
        return distance

    def getCommute(self):
        if self.coordsAirbnb:
            routes, times = self.calculateCommute(self.coordsAirbnb)
        else:
            routes, times = None, None
        return routes, times
        
    def getDistanceFromName(self):
        if self.locationName:
            coordsName = self.calculateCoords(self.locationName)
            distance = self.calculateDistance(coordsName)
        else:
            distance = None
        return distance

    def calculateDistance(self, airbnb):
        distanceKm = geodesic(airbnb, self.coordsOktoberfest).km
        # print(f"The distance to Oktoberfest is {distanceKm}Km")
        distance = round(distanceKm, 2)
        if distanceKm > 10:
            distance = None
        return distance
    
    def calculateCoords(self, homeLocation):
        name = f"{homeLocation}, Munich"
        baseUrl = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": name,
            "key": self.myKey,
        }
        response = requests.get(baseUrl, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                try:
                    coords = data['results'][0]['geometry']['location']
                except:
                    coords = None
                    locationCoords = None
                if coords:
                    locationCoords = (coords['lat'], coords['lng'])
        return locationCoords 

    def calculateCommute(self, start):
        baseUrl = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": start,
            "destination": "Theresienhohe",
            "mode": "transit",
            "key": self.myKey,
        }
        response = requests.get(baseUrl, params=params)
        routes = []
        times = []
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                for route in data["routes"]:  
                    idx = 0
                    routes = ["" for r in range(len(data["routes"]))]
                    times = [0 for r in range(len(data["routes"]))]
                    for leg in route["legs"]:
                        for step in leg["steps"]:
                            if "transit_details" in step:
                                transit = step["transit_details"]
                                if "short_name" in transit["line"]:
                                    line = transit["line"]["short_name"]
                                else:
                                    line = transit["line"]
                                departure_stop = transit["departure_stop"]["name"]
                                arrival_stop = transit["arrival_stop"]["name"]
                                duration = step["duration"]["text"]
                                durationInt = int(duration[0:-5])
                                routes[idx] = routes[idx]+(f"Take {line} from {departure_stop} to {arrival_stop} ({duration})\n")
                                times[idx] = times[idx] + durationInt
                    idx += 1     
            else:
                print(f"Error: {data}")
        else:
            print("Failed to make the request.")
    
        if len(routes) == 0:
            routes.append("No commute options, you can walk!")
        return routes, times



