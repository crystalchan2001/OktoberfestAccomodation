import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from writer import Writer
from datetime import date
import os

class Sender:

    def __init__(self, properties, emailTo, sendAsDoc):
        self.emailTo = emailTo
        self.msg = MIMEMultipart()

        self.font = "Calibri"
        self.fontSize = 14

        if sendAsDoc:
            self.writeDoc(properties, date)
        else:
            self.writeEmail(properties, emailTo)
        self.sendEmail(emailTo)

    def writeDoc(self, properties, path, date):
        path = f"C:/Users/chanc/Documents/2024/OktoberfestAccomodation/{self.getDate()}-airbnb-search.docx"
        writer = Writer(properties, path, date)

    def attachImage(self, property):
        path = property.getScreenshotPath()
        imgData = open(path, "rb").read()
        image = MIMEImage(imgData, name=os.path.basename(path))
        self.msg.attach(image)
        os.remove(path)

    def attachLink(self, property):
        url = property.getUrl()
        link = f"""
        View <a href="https://{url}">listing</a></p>
        """
        self.msg.attach(MIMEText(link, 'html'))
    
    def attachPrices(self, property):
        price = property.getPricePer()
        total = property.getTotal()
        prices = f"<p>Price per night: £{price}, Total: £{total}</p>"
        self.msg.attach(MIMEText(prices, 'html'))
    
    def attachLocation(self, property, distance, name):
        if distance:
            self.msg.attach(MIMEText(f"<p>The property is roughly {distance}km from Oktoberfest.</p>", 'html'))
        else:
            self.msg.attach(MIMEText("<p>Could not locate this property.</p>", 'html'))
        if name:
            distanceName = property.getDistanceName() 
            distanceHtml = f"<p>, {distanceName}km from Oktoberfest.</p>" if distanceName else "<br>"
            location = f"<p>Based near {name}{distanceHtml}</p>"
            self.msg.attach(MIMEText(location, 'html'))
        else:
            self.msg.attach(MIMEText("<p>There were no local points of interest.</p>", 'html'))


    def attachCommute(self, property, start):
        if start:
            commutes = []
            if type(start) != str:
                start = "rough location"
                commutes = property.getCommute()
            else:
                commutes = property.getCommuteName()
            if commutes:
                if commutes[0] != "":
                    self.msg.attach(MIMEText(f"<p>How to get to Oktoberfest from {start}:</p>", 'html'))
                    commuteStr = ""
                    for idx in range(len(commutes)):
                        self.msg.attach(MIMEText(f"<h4>Option {idx+1}</h4>", 'html'))
                        commuteStr += f"<p>{commutes[idx]}</p>"
                        self.msg.attach(MIMEText(commuteStr, 'html'))
        else:
            self.msg.attach(MIMEText("<p>There were no calculated commutes.</p>", 'html'))

    def writeEmail(self, properties, emailTo):
        self.msg["From"] = "ilikecows3359@gmail.com"
        self.msg["To"] = emailTo
        self.msg["Subject"] = f"Airbnb search {self.getDate()}"
        
        heading = f"<h4>Sir, we found {len(properties)} listing(s) for you.</h4>"
        self.msg.attach(MIMEText(heading, 'html'))

        if properties:
            idx = 1
            for property in properties:
                self.msg.attach(MIMEText(f"<p><b>{idx}.</b>", 'html'))
                self.attachLink(property)
                self.attachImage(property)
                self.attachPrices(property)
                distance = property.getDistance()
                name = property.getName()
                self.attachLocation(property, distance, name)
                self.attachCommute(property, distance)
                if name:
                    self.attachCommute(property, name)
                idx += 1

    def sendEmail(self, emailTo):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("ilikecows3359@gmail.com", "ppdm eymb lfbs yirr")
        server.sendmail("ilikecows3359@gmail.com", emailTo, self.msg.as_string())
        server.quit()

    @staticmethod
    def getDate():
        today = date.today()
        day = today.day
        month = today.strftime('%B')
        yearShort = today.strftime('%y')
        return f"{day}-{month}-{yearShort}"
    

