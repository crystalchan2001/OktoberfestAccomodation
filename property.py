from mapper import Mapper

class Property:
    def __init__(self, url, pricePer, total, coords, name, path):
        self.url = url
        self.name = self.getName(name)
        self.mapper = Mapper(coords, self.name)
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
        return self.mapper.getDistance()
    
    def getCommute(self):
        return self.mapper.getCommute()

    def getDistanceName(self):
        return self.mapper.getDistanceFromName()
    
    def getPricePer(self):
        return self.pricePer    
    
    def getTotal(self):
        return self.total
    
    def getScreenshotPath(self):
        return self.screenshotPath

