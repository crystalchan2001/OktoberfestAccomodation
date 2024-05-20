from scraper import Scraper
from sender import Sender
import sys

# guests = 1
# rooms = 1
# checkin = "2024-10-01"
# checkout = "2024-10-07"
# bathrooms = "1"
# favourite = "True"
# entireHome= "False"

# budget = 700
# # emailTo = "wesleyboettcher06@gmail.com"
# emailTo = "chan.cj@icloud.com"
# sendAsDoc = False

# scraper = Scraper(guests, rooms, checkin, checkout, budget, bathrooms, favourite, entireHome)
# properties = scraper.getProperties()

# sender = Sender(properties, emailTo, sendAsDoc)

# print(f"Accommodation search completed and email sent to {emailTo}!")

def collectInput():
    print("Num of arguments = " + str(len(sys.argv)))
    guests = sys.argv[1]
    rooms = sys.argv[2]
    checkin = sys.argv[3]
    checkout = sys.argv[4]
    budget = sys.argv[5]
    bathrooms = sys.argv[6]
    favourite = sys.argv[7]
    entireHome = sys.argv[8]
    frequency = sys.argv[9]
    email = sys.argv[10]

    return [guests, rooms, checkin, checkout, budget, bathrooms, favourite, entireHome, frequency, email]


if __name__ == '__main__':
    variables = collectInput()
    print(variables)
    print("Hello world")