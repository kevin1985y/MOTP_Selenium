#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains # 鍵盤滑鼠事件
import unittest, time, re
import xmlrunner
from time import sleep

'''
待調整
def LoginOTP(self, OTP): # 登入OTP使用者
    driver = self.driver
    driver.get(self.base_url + "/MOTPWeb")
    driver.find_element_by_id("user").clear()
    driver.find_element_by_id("user").send_keys("admin")
    driver.find_element_by_id("mypass").clear()
    driver.find_element_by_id("mypass").send_keys("admin")
    driver.find_element_by_id("myotp").clear()
    driver.find_element_by_id("myotp").send_keys(OTP)
    driver.find_element_by_id("mypass").submit()
    driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
    driver.find_element_by_css_selector("input[type=\"button\"]").click()        
    welcome = driver.find_element_by_xpath(".//b[contains(text(), 'Welcome to use MOTP')]").text # 畫面文字截取
    return welcome
'''

def alert(self): # 登出其他使用者
    driver = self.driver
    alert = driver.switch_to.alert
    output = alert.text
    alert.accept()
   

class Init(unittest.TestCase):
    def setUp(self):
        self.driver =webdriver.Chrome("chromedriver.exe")
        self.driver.implicitly_wait(10)
        self.base_url = "http://192.168.0.201:8080/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_a1_Login_EmptyAccount(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("mypass").submit()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Account] Please fill the fields.")
        print("1. [Account] Please fill the fields.")
            
    def test_a2_Login_EmptyPassword(self):          
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Password] Please fill the fields.")
        print("2. [Password] Please fill the fields.")
			
    def test_a3_Login_SpecialAccount(self):          
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("~!@#")
        driver.find_element_by_id("mypass").submit()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Account] Correct character: 0~9, a~z, A~Z, ._-")
        print("3. [Account] Correct character: 0~9, a~z, A~Z, ._-")

    def test_a4_Login_SpecialPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("~!@# ~!@")
        driver.find_element_by_id("mypass").submit()
        output = driver.find_element_by_class_name("indexError").text
        self.assertEqual(output, 'Login fail.')
        print("4. Login fail.")
           
    def test_a5_Login_NotExistAccount(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin3")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("123123")
        driver.find_element_by_id("mypass").submit()
        output = driver.find_element_by_class_name("indexError").text
        self.assertEqual(output, 'Login fail.')
        print("5. Login fail.")
	
    def test_a6_Login_NotOTPAccount2(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("myotp").clear()
        driver.find_element_by_id("myotp").send_keys("123123")
        driver.find_element_by_id("myotp").submit()
        output = driver.find_element_by_class_name("indexError").text
        self.assertEqual(output, "Login fail.\n[66210] This account is not an OTP user")
        print("6. Login fail.\n[66210] This account is not an OTP user")

    def test_a7_Login_WrongPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("456789")
        driver.find_element_by_id("mypass").submit()
        output = driver.find_element_by_class_name("indexError").text
        self.assertEqual(output, "Login fail.")
        print("7. Login fail.")

    def test_a8_Login_Succeed(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        output = driver.find_element_by_class_name("wel_title").text
        self.assertEqual(output, "Welcome to use MOTP")
        print("8. Welcome to use MOTP")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        
if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))

