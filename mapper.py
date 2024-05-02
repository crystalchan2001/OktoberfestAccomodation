from geopy.distance import geodesic
from geopy.geocoders import Nominatim, options
import ssl
import certifi
import requests

class Mapper:

    def __init__(self, coords, homeLocation):
        self.myKey = "AIzaSyCXppM7yRwYpAxbgB0Gu7AuFXPCSgf9PTY"
        self.coordsOktoberfest = (48.131489099999996,11.549755214131313)
        if coords:
            self.coordsAirbnb = f"{coords[0]},{coords[1]}"
            self.distance = self.calculateDistance(coords)
            self.commute = self.calculateCommute(self.coordsAirbnb)
        if homeLocation:
            if homeLocation != "Showing 0 points of interest.":
                self.coordsCalculated = self.calculateCoords(homeLocation) 
                if self.coordsCalculated != (0,0):
                    self.distanceName = self.calculateDistance(self.coordsCalculated)
                    self.commuteName = self.calculateCommute(homeLocation)
        else:
            self.distance = None
            self.commute = None

    def getDistance(self):
        return self.distance
    
    def getCommute(self):
        return self.commute
    
    def getCommuteFromName(self):
        try:
            return self.commuteName
        except AttributeError:
            return None
    
    def getDistanceFromName(self):
        try:
            return self.distanceName
        except AttributeError:
            return None
    
    def calculateCoords(self, homeLocation):
        ctx = ssl.create_default_context(cafile=certifi.where())
        options.default_user_agent = "my-test"
        options.default_ssl_context = ctx
        geolocator = Nominatim(user_agent="my-test")
        try:
            location = geolocator.geocode(f"{homeLocation}, Munich")
            location = (location.latitude,location.longitude)
            print(f"The calculated coords of {homeLocation} are ({location.latitude,location.longitude})")
        except AttributeError:
            location = (0,0)
        return location

    def calculateDistance(self, airbnb):
        distanceKm = geodesic(airbnb, self.coordsOktoberfest).km
        print(f"The distance to Oktoberfest is {distanceKm}Km")
        return round(distanceKm, 2)

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
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                for route in data["routes"]:  
                    routesIdx = 0
                    routes = ["" for r in range(len(data["routes"]))]
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
                                routes[routesIdx] = routes[routesIdx]+(f"Take {line} from {departure_stop} to {arrival_stop} ({duration})\n")
                    routesIdx += 1            
                print(routes)
            else:
                print(f"Error: {data}")
        else:
            print("Failed to make the request.")
    
        if len(routes) == 0:
            routes.append("No commute options, you can walk!")
        return routes

#* TESTS
# map2 = Mapper(('48.1647', '11.5724'), "Schwabing-West")
# map2.getDistance()
# map2.getCommute()
# map2.getCommuteFromName()

# map3 = Mapper(('48.10996', '11.59264'), "Showing 0 points of interest.")
# map3.getDistance()
# map3.getCommute()
# map3.getCommuteFromName()

# map4 = Mapper(('48.10996', '11.59264'), "Showing 0 points of")
# map4.getDistance()
# map4.getCommute()
# map4.getCommuteFromName()


