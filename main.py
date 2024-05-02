from scraper import Scraper
from sender import Sender

guests = 1
rooms = 1
checkin = "2024-10-01"
checkout = "2024-10-07"
bathrooms = "1"
favourite = "True"
entireHome= "False"

budget = 700
# emailTo = "wesleyboettcher06@gmail.com"
emailTo = "chan.cj@icloud.com"
sendAsDoc = False

scraper = Scraper(guests, rooms, checkin, checkout, budget, bathrooms, favourite, entireHome)
properties = scraper.getProperties()

sender = Sender(properties, emailTo, sendAsDoc)

print(f"Accommodation search completed and email sent to {emailTo}!")