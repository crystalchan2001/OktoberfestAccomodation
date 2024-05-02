from mapper import Mapper

class Property:
    def __init__(self, url, pricePer, total, coords, name, path):
        self.url = url
        self.name = name
        self.mapper = Mapper(coords, name)
        self.distance = self.mapper.getDistance()
        self.commute = self.mapper.getCommute()
        self.distanceName = self.mapper.getDistanceFromName()
        self.commuteName = self.mapper.getCommuteFromName()
        self.pricePer = pricePer
        self.total = total
        self.screenshotPath = path

    
    def getUrl(self):
        return self.url
    
    def getName(self):
        if self.name != "Showing 0 points of interest.":
            return self.name
        else:
            return None
        
    def getDistance(self):
        return self.distance
    
    def getCommute(self):
        return self.commute

    def getDistanceName(self):
        return self.distanceName
    
    def getCommuteName(self):
        return self.commuteName
    
    def getPricePer(self):
        return self.pricePer    
    
    def getTotal(self):
        return self.total
    
    def getScreenshotPath(self):
        return self.screenshotPath

