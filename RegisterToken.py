#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains # 鍵盤滑鼠事件
import unittest
import os
import time
import re
import xmlrunner
import csv
from time import sleep
import AuthenticationToken

def RegisterToken(self, token, SN):
    driver = self.driver      
    driver.find_element_by_xpath("//img[@title='Register Token']").click()
    driver.find_element_by_name("sAccount").clear()
    driver.find_element_by_name("sAccount").send_keys(token)
    Select(driver.find_element_by_id("HashFactRand_item")).select_by_visible_text(SN)
    driver.find_element_by_name("doSubmit").click()
    driver.find_element_by_css_selector("button[type=\"button\"]").click()
    output = driver.find_element_by_class_name("title").text
    return output

def Query_User(self):
    driver = self.driver
    ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
    ActionChains(driver).move_to_element(ID).perform()
    driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=OTPUser')\"]").click()
    
class Register(unittest.TestCase):
    def setUp(self):
        self.driver =webdriver.Chrome("chromedriver.exe")
        self.driver.implicitly_wait(10)
        self.base_url = "http://192.168.0.201:8080/MOTPWeb"
        self.verificationErrors = []
        self.accept_next_alert = True       
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("321321")
        driver.find_element_by_id("mypass").submit()
        alert = driver.switch_to.alert # 登出其他使用者
        alert.accept()
        
    def test_a1_RegisterHWToken(self):
        output = RegisterToken(self, "hw001", "18709")
        self.assertEqual(output, "Verify OTP")
        print("1. Register success.")


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


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
