import unittest
import string
import random
import time
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

def createRandomName():
    name = random.choice(string.ascii_uppercase)
    for i in range(random.randint(2,20)):
        name = name + random.choice(string.ascii_lowercase)
    return name

def createRandomEmail():
    email = 'KTQA.Personal+'
    for i in range(random.randint(2,20)):
        email = email + random.choice(string.ascii_letters + string.digits)
    email = email + '@gmail.com'
    return email

def createRandomPassword():
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(random.randint(6,20)))

def scrollDown(driver):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def createRandomBirthday():
    month = random.randint(1,12)
    if (month < 10):
        strMonth = '0'+str(month)
    else:
        strMonth=str(month)
    day = random.randint(1,28)
    if (day < 10):
        strDay = '0'+str(day)
    else:
        strDay=str(day)
    strYear = str(random.randint(1950,1999))
    return strMonth + strDay + strYear

def getLast4Shows(driver,tab):
    ActionChains(driver).click(driver.find_element_by_link_text(tab)).perform()
    scrollDown(driver)
    time.sleep(3)
    allTiles = driver.find_elements_by_xpath("//div[@class='TileGrid_grid_vrnLT']/div/div/div/a/div")
    tileNames = []
    for tile in allTiles[len(allTiles) -4:len(allTiles)]:
        tileNames.append(tile.text)
    return tileNames

class FoxSeleniumTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    # create an account
    def test_account_creation(self):
        driver = self.driver
        driver.get('https://www.fox.com')
        self.assertIn("FOX", driver.title)
        accountLink = driver.find_element_by_id("path-1")
        ActionChains(driver).click(accountLink).perform()
        self.assertIn("Enhance Your Viewing Experience with a Personal Profile",driver.page_source)
        accountSignUpButton = driver.find_element_by_class_name("Account_signUp_3SpTs")
        ActionChains(driver).click(accountSignUpButton).perform()
        self.assertIn("Create a Profile",driver.page_source)
        signupFirstName = createRandomName()
        # print signupFirstName
        ActionChains(driver).click(driver.find_element_by_name("signupFirstName")).send_keys(signupFirstName).perform()
        signupLastName = createRandomName()
        # print signupLastName
        ActionChains(driver).click(driver.find_element_by_name("signupLastName")).send_keys(signupLastName).perform()
        signupEmail=createRandomEmail()
        # print signupEmail
        ActionChains(driver).click(driver.find_element_by_name("signupEmail")).send_keys(signupEmail).perform()
        signupPassword = createRandomPassword()
        # print signupPassword
        ActionChains(driver).click(driver.find_element_by_name("signupPassword")).send_keys(signupPassword).perform()
        ActionChains(driver).click(driver.find_element_by_link_text('Gender')).perform()
        ActionChains(driver).click(driver.find_element_by_link_text('Prefer not to say')).perform()
        signupBirthday = createRandomBirthday()
        # print signupBirthday
        ActionChains(driver).click(driver.find_element_by_xpath("//input[@placeholder='Birthdate'][@type='text']")).perform()
        ActionChains(driver).click(driver.find_element_by_xpath("//input[@placeholder='MM/DD/YYYY'][@type='text']")).send_keys(signupBirthday).perform()
        ActionChains(driver).click(driver.find_element_by_class_name("Account_signupButtonDesktop_1PCXs")).perform()
        ActionChains(driver).click(driver.find_element_by_class_name("Account_signupSuccessButton_1mM7y")).perform()

        # click on show tabs and get last 4 shows
        ActionChains(driver).click(driver.find_element_by_link_text("Shows")).perform()
        Last4Shows = [getLast4Shows(driver,"FOX"),getLast4Shows(driver,"FX"),getLast4Shows(driver,"National Geographic"),getLast4Shows(driver,"FOX Sports"),getLast4Shows(driver,"All Shows")]

        # check for duplicate records
        uniqueShowList = []
        for i in range(len(Last4Shows)):
            for j in range(4):
                if Last4Shows[i][j] not in uniqueShowList:
                    uniqueShowList.append(Last4Shows[i][j])
                else:
                    Last4Shows[i][j] = "Duplicate Record"

        # output to excel-format csv (there is an excel workbook package that could be used for direct excel manipulation, but I didn't want to go outside the base libraries + selenium for the code test
        with open('./Selenium_Test_Output.csv', 'w') as csvfile:
            outputFile = csv.writer(csvfile)
            outputFile.writerow(['Shows','FX','National Geographic','FOX Sports','All Shows'])
            for i in range(4):
                outputFile.writerow([Last4Shows[0][i], Last4Shows[1][i], Last4Shows[2][i], Last4Shows[3][i], Last4Shows[4][i]])

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()