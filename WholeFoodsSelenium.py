from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from bs4 import BeautifulSoup
import sys
import time
import re

from twilio.rest import Client



def sendSMS(phoneNumbers, message):
    account = accountnumber
    token = token
    client = Client(account, token)


    for number in phoneNumbers:
        message = client.messages.create(to=number, from_=from_number,
                                        body=message)   


def grabAvailability(wd):

    soup = BeautifulSoup(wd.page_source)

    pattern = re.compile(r"date-select-toggle-text-availability")

    matches = soup.find_all('div', {'class':pattern})

    message = ""
    
    notAvailable = lambda i : "\nToday not available\n" if i == 0 else "Tomorrow not available\n"
    
    available = lambda i : "\nToday available\n" if i == 0 else "Tomorrow available\n"
    
    

    truth = False
    i = 0
    for match in matches:
        if match.getText().strip().find("Not available") != 0:
            message += available(i)
            truth = True
        else:
            message += notAvailable(i)
            
        i+=1
    return [truth,message]
    

if __name__ == "__main__":
    chrome_options = Options()
    
    de_capabilities = webdriver.DesiredCapabilities.CHROME
 
    
    driver = WebDriver("http://LocalSeleniumStandaloneServer:4444/wd/hub", desired_capabilities=de_capabilities)

    print(driver.title)
    
    phoneNumbersList = []
    
    phonenumber = ""
    


    phoneNumbersList.append(phonenumber)
    
    
    

    driver.get("https://www.amazon.com/")
    
    ready = input("Please press enter when you have navigated to the correct page") 

    found = False

    while True or found:
        driver.refresh()
        retVal = grabAvailability(driver)

        truth = retVal[0]
        message = retVal[1]

        if truth:
            message = message + "\nThere's one available slot!\nBrought to you by Shay Maor"
            sendSMS(phoneNumbersListwDad, message)
            
            found = True

        else :
            message = message + "Will try again in 7 minutes."
            
            message = message + "\nBrought to you by Shay Maor"
            sendSMS(phoneNumbersList, message)
        
        time.sleep(420)
