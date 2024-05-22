from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from property import Property
import re

driver = None
class Scraper:

    def __init__(self, guests, rooms, checkin, checkout, budget, bathrooms, favourite, entireHome, travel, maxTravel):
        self.shortDelay = 10
        self.longDelay = 30
        self.travel = travel
        self.maxTravel = maxTravel
        self.driver = self.startAndGetDriver(guests, rooms, checkin, checkout, budget, bathrooms, favourite, entireHome)

    def startAndGetDriver(self, guests, rooms, checkin, checkout, budget, bathrooms=1, favourite="true", entireHome="false"):
        options = webdriver.EdgeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Edge(options=options)   
        # driver = webdriver.Edge()
        #format of date is 2024-09-21 
        entireHome = """room_types%5B%5D=Entire%20home%2Fapt&""" if entireHome == "true" else ""
        url = f"""https://www.airbnb.co.uk/s/Munich--Germany/homes?adults={guests}&place_id=ChIJ2V-Mo_l1nkcRfZixfUq4DAE&refinement_paths%5B%5D=%2Fhomes
                &checkin={checkin}&checkout={checkout}&tab_id=home_tab&query=Munich%2C%20Germany
                &price_filter_input_type=2&price_filter_num_nights=6&channel=EXPLORE&price_max={budget}
                &search_type=filter_change&source=structured_search_input_header&ne_lat=48.17308416412205&ne_lng=11.600579336766344&sw_lat=48.10086724294256&sw_lng=11.513296081397073&zoom=13.269747639501245&zoom_level=13.269747639501245&search_by_map=true
                &min_bedrooms={rooms}&min_bathrooms={bathrooms}&{entireHome}guest_favorite={favourite}"""
        driver.get(url)
        print("Called url " + url)
        return driver
    
    def closeTranslationPopup(self):
        try:
            button = WebDriverWait(self.driver, self.shortDelay).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Close']")))
            button.click()
            print("Translation popup closed")
        except Exception:
            print("There was no translation popup")

    def closeCookies(self):
        try:
            button = WebDriverWait(self.driver, self.shortDelay).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Continue without accepting']")))
            button.click()
            print("Cookies popup closed")
        except Exception:
            print("There was no cookies popup")
    
    def getLocation(self):
        location = None
        try:
            map = WebDriverWait(self.driver, self.longDelay).until(EC.presence_of_element_located((By.CLASS_NAME, '_1ctob5m')))
            ActionChains(self.driver).move_to_element(map).perform()
            map2 = WebDriverWait(map, self.longDelay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='map/GoogleMap']>span")))
            location = map2.text[11:]
        except TimeoutException:
            print("Timeout waiting for location name.")
        except NoSuchElementException:
            print("Element location name not found.")
        except Exception as e:
            print("An exception occurred while locating location name:", e.__class__)
        return location
    
    def getCoords(self):
        coords = None
        try:
            xpath = "//a[@title='Report errors in the road map or imagery to Google']"
            a = WebDriverWait(self.driver, self.longDelay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            href = a.get_attribute('href')
            latlong = re.search(r"@([\d.-]+),([\d.-]+),", href)
            if latlong:
                coords = (latlong.group(1), latlong.group(2))
        except TimeoutException:
            print("Timeout waiting for coordinates.")
        except NoSuchElementException:
            print("Element coordinates not found.")
        except Exception as e:
            print("An exception occurred while locating coordinates:", e.__class__)
        return coords

    def getPrice(self):
        price = 0
        try:
            element = WebDriverWait(self.driver, self.shortDelay).until(EC.presence_of_element_located((By.CLASS_NAME, "_1y74zjx")))
            priceStr = element.get_attribute("innerText")
            price = int(priceStr[1:].replace(',', ''))
        except TimeoutException:
            print("Timeout waiting for price.")
        except NoSuchElementException:
            print("Element price not found.")
        except Exception as e:
            print("An exception occurred while locating price:", e.__class__)
        return price
    
    def getTotal(self):
        total = 0
        try:
            xpath = "//span[@class='_1qs94rc']//span//span[@class='_j1kt73']"
            element = WebDriverWait(self.driver, self.shortDelay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            totalStr = element.get_attribute("innerText")
            total = int(totalStr[1:].replace(',', ''))
        except TimeoutException:
            print("Timeout waiting for total.")
        except NoSuchElementException:
            print("Element total not found.")
        except Exception as e:
            print("An exception occurred while locating total:", e.__class__)
        return total

    def getScreenshot(self, index):
        imgPath = f"OktoberfestAccomodation/airbnb-listing-{index}.png"
        self.driver.save_screenshot(imgPath)
        return imgPath

    def findUrls(self):
        listings = []
        urls = []
        try:
            xpath = "//div[@itemprop='itemListElement']//meta[@itemprop='url']"
            listings = WebDriverWait(self.driver, self.longDelay).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except Exception as e:
            print("An exception occured while locating urls: ", e.__class__)
        if listings:
            print(f"Found {len(listings)} listings.")
            for li in listings:
                url = li.get_attribute("content")
                urls.append(url)
        else: 
            print("No listings matched your criteria.")
        return urls
    
    def findProperties(self):
        properties = []
        urls = self.findUrls()
        properties = []
        if urls:
            idx = 0
            for url in urls:
                self.driver.get(f"https://{url}")
                if idx == 0:
                    self.closeTranslationPopup()
                self.closeCookies()
                screenshotPath = self.getScreenshot(idx)
                price = self.getPrice()
                total = self.getTotal()
                location = self.getLocation()
                coords = self.getCoords()
                properties.append(Property(url, price, total, coords, location, screenshotPath))
                print(f"Price: {price} Total: {total} POI: {location} Coordinates: {coords}")
                idx = idx+1
        else:
            print("No listings matched your criteria")
        return properties

    def filterProperties(self, properties):
        filteredProperties = []
        return filteredProperties

    def sortProperties(self, properties):
        sortedProperties = []
        return sortedProperties
    
    def getProperties(self):
        return self.findProperties()
    
    def done(self):
        self.driver.quit()
        print("Quit driver.")
    
# Scraper(1, 1, "2024-09-20", "2024-10-07", 1500)



