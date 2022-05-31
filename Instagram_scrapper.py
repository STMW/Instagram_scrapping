import sys
import time
import selenium
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#We insert the chromedriver path
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()

#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

hashtag = "harcelement/"


#scrapper class for instagram page
class InstagramBot():

    #this function ensures user sign in
    def __init__(self):
      #We intialize the webdriver and the Data to be scrapped
      self.chrome_options = webdriver.ChromeOptions()
      self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",options=chrome_options)
      self.ScrapedDataList = [["description", "location", "user", "time", "image"]]
      self.hashtag = ""


    def signIn(self, email, password):
      print("Signing In")

      self.email = email
      self.password = password
      self.browser.get('https://www.instagram.com/accounts/login/')

      time.sleep(2)
      #We remove the pop-up before proceeding
      accept_cookies = self.browser.find_element_by_xpath('//button[@class ="aOOlW  bIiDR  "]').click()

      print(self.email)
      print(self.password)

      time.sleep(5)
      emailInput = self.browser.find_elements_by_css_selector("input[name='username']")[0]
      passWordInput = self.browser.find_elements_by_css_selector("input[name='password']")[0]

      emailInput.clear()
      passWordInput.clear()
      #inputs = WebDriverWait(self.browser, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'form input')))

      #emailInput = inputs[0]
      #passwordInput = inputs[1]

      emailInput.send_keys(self.email)
      passWordInput.send_keys(self.password)

      passWordInput.send_keys(Keys.ENTER)
      #login = self.browser.find_element_by_css_selector("button[type='submit']").click()

      time.sleep(5)

      
    #this fucntion scrapes all the posts from a given url
    def scrape(self, url):
      self.browser.get(url)
      print(url)


      #We wait for required elements to load before we start scrapping
      divElements = WebDriverWait(self.browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='v1Nh3 kIKUG _bz0w']")))

      print(len(divElements))
      hrefElements = []

      #We get the links of all the tags
      try:
          for div in divElements:
            hrefElements.append(div.find_elements(By.TAG_NAME, 'a')[0])
      except:
          pass
       
      elements_link = [x.get_attribute("href") for x in hrefElements]

      #We scrap each link
      for elements in elements_link:
        self.scrapePost(elements)
 

    #this fuction scrapes a particuar post by its given url
    def scrapePost(self, url):
      self.browser.get(url)
      print("Scraping Post: " + url)
      try: 
        try:
        #Location element is the html location specified on the post
          location_element = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='O4GlU']")))
          location_element = [x.text for x in location_element]
        except:
          location_element = None

        location_element = ["None"] if location_element==None else location_element
        
        print(location_element)

        location_element = location_element[0].replace(",", " ")

        #User element defines the person at the origin of the post
        try:
          user_element = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")))
          #user_element = self.browser.find_elements(By.XPATH, "//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")
          user_element_text = user_element[0].text
          print(len(user_element_text))
        except:
          print(None)
        
        user_element_text = user_element_text.replace(".", " ")
        user_element_link = user_element[0].get_attribute("href")
        print(user_element_text)
        print(user_element_link)
        try:
          desc_element = self.browser.find_elements(By.XPATH, "//div[@class='C4VMK']/span")
          desc_text = desc_element[0].text
        except:
          desc_text = " "
          pass
        try: 
          timestamp_element = self.browser.find_elements(By.XPATH, "//div[@class='_7UhW9 BARfH        MMzan    _0PwGv          uL8Hv         ']/time")
          timestamp = timestamp_element[0].get_attribute("datetime")

        except:
          timestamp = " "
          pass    
        
        image_url = self.findImage()
        self.scrapedData = [desc_text, location_element, user_element_text, timestamp, image_url]
        print(self.scrapedData)
        self.ScrapedDataList.append(self.scrapedData)
      except Exception as e: # work on python 3.x
        print(e)
      
    #Fonction which gets the url of the image or video associated with the post
    def findImage(self):
      image_element = self.browser.find_element(By.XPATH, "//div[@class='KL4Bh']/img")
      image_element_link = image_element.get_attribute("src")
      return image_element_link
    
    
    def scrapeWithHashtags(self, hashtags):
      for hashtag in hashtags:
        self.hashtag = hashtag
        print("-----------Scraping the hashtag '" + hashtag +"' -----------")
        url = 'https://www.instagram.com/explore/tags/' + hashtag
        self.scrape(url)


if __name__ == "__main__":

#https://www.instagram.com/p/CeLUVtzuJ7m/

  hashtags = ['harcelement']
  bot = InstagramBot()

  username = input("What's your email?\n")
  password = input("What's your password?\n")
  bot.signIn(username, password)
  

  bot.scrapeWithHashtags(hashtags)
  print(bot.ScrapedDataList)#aOOlW  bIiDR  