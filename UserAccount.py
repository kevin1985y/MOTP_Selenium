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
import RegisterToken

def Add_User(self):
    driver = self.driver
    ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
    ActionChains(driver).move_to_element(ID).perform()
    driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=OTPUser')\"]").click()
    driver.find_element_by_css_selector("input[type=\"button\"]").click()   

def Query_User(self):
    driver = self.driver
    ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
    ActionChains(driver).move_to_element(ID).perform()
    driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=OTPUser')\"]").click()

class UserAccount(unittest.TestCase):
    def setUp(self):
        # profile.default_content_settings.popups：設置為0 (禁止彈出窗口)
        # download.default_directory：設置下載路徑
        options = webdriver.ChromeOptions()  
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'E:\selenium_py\MOTP_Selenium'}
        options.add_experimental_option('prefs', prefs)

        self.driver =webdriver.Chrome("chromedriver.exe", chrome_options=options)
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

    def test_a1_AddUserPage(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=OTPUser')\"]").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()    
        output = driver.find_element_by_class_name("title").text
        self.assertEqual(output, "Create User")
        print("1. Create User Page")

    def test_a2_EmptyUserName(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("OTPCreatebtn").click() 
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Name] Please fill the fields.")
        print("2. [Name] Please fill the fields.") 

    def test_a3_SpecialUserName(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("~!@#")
        driver.find_element_by_name("OTPCreatebtn").click()  
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Name] Correct character: 0~9, a~z, A~Z, ._-")
        print("3. [Name] Correct character: 0~9, a~z, A~Z, ._-")

    def test_a4_EmptyPassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("OTPCreatebtn").click()   
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Portal Password] Please fill the fields.")
        print("4. [Portal Password] Please fill the fields.")

    def test_a5_LengthPassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("1")
        driver.find_element_by_name("OTPCreatebtn").click()     
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Portal Password] The length of the data fail.")
        print("5. [Portal Password] The length of the data fail.")

    def test_a6_SpecialPassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("~!@# ~!@")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Portal Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("6. [Portal Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_a7_EmptyRetypePassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Please fill the fields.")
        print("7. [Re-type PW] Please fill the fields.")

    def test_a8_LengthRetypePassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("1")
        driver.find_element_by_name("OTPCreatebtn").click() 
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")
        print("8. [Re-type PW] The length of the data fail.")

    def test_a9_SpecialRetypePassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("~!@# ~!@")
        driver.find_element_by_name("OTPCreatebtn").click() 
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("9. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_b1_DifferentPassword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123456")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Re-type password error.")
        print("10. Re-type password error.")

    def test_b2_LengthPhoneNum(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Phone Number] The length of the data fail.")
        print("11. [Phone Number] The length of the data fail.")

    def test_b3_SpecialPhoneNum(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("$$%%^^")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Phone Number] Correct character: 0~9")
        print("12. [Phone Number] Correct character: 0~9")

    def test_b4_WrongFomatEmail(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("13. Invalid Email.")

    def test_b5_SpecialDescription(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("~!@# ~!@")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("14. [Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_b6_SpecialKeyword(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("%^&")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Keywords] Correct character: 0~9, a~z, A~Z, ._-/")
        print("15. [Keywords] Correct character: 0~9, a~z, A~Z, ._-/")

    def test_b7_SpecialSN(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        driver.find_element_by_name("ht_serial").send_keys("$%^$%^")
        driver.find_element_by_name("OTPCreatebtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[SN] Correct character: 0~9, a~f, A~F")
        print("16. [SN] Correct character: 0~9, a~f, A~F")

    def test_b8_AddHWUser(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("hw001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        driver.find_element_by_xpath("(//input[@name='set'])[2]").click()
        driver.find_element_by_id("expiredate").click()
        driver.find_element_by_css_selector("a.calnavright").click()  # 下個月
        driver.find_element_by_xpath("//tr[3]/td[4]/a").click()
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("17. User create success.")

    def test_b9_AddHWUserNoExpireDate(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("hw002")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("18. User create success.")

    def test_c1_AddSWUser(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("sw001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("SoftwareToken(2)")
        driver.find_element_by_xpath("(//input[@name='set'])[2]").click()
        driver.find_element_by_id("expiredate").click()
        driver.find_element_by_css_selector("a.calnavright").click()  # 下個月
        driver.find_element_by_xpath("//tr[3]/td[4]/a").click()
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("19. User create success.")

    def test_c2_AddSWUserNoExpireDate(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("sw002")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("002")
        driver.find_element_by_name("keyword").send_keys("002")
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("SoftwareToken(1)")
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("20. User create success.")

    def test_c3_AddODUser(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("OD001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("On-Demand(1)")
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("21. User create success.")

    def test_c4_AddPushUser(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("Push001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("PushToken(7)")
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("22. User create success.")

    def test_c5_AddOtherUser(self):
        driver = self.driver
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("OT001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("OtherToken")
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("23. User create success.")

    def test_c6_NoSWToken(self):
        driver = self.driver
        DelResult = AuthenticationToken.DelToken(self)
        self.assertEqual(DelResult, " Delete token success.")
        print "Delete token success."
        
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("sw003")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        select = Select(driver.find_element_by_id("deviceType"))
        found = False
        
        for op in select.options:  # 取得下拉選單清單
            selectList = op.text
            if selectList.find("Software") > -1:
                found = True
                
        self.assertEqual(found, False)
        print("24. No SW Token")

    def test_c7_NoODToken(self):
        driver = self.driver  
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("od002")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        select = Select(driver.find_element_by_id("deviceType"))
        found = False
        
        for op in select.options:  # 取得下拉選單清單
            selectList = op.text
            if selectList.find("On-Demand") > -1:
                found = True
                
        self.assertEqual(found, False)
        print("25. No OD Token")

    def test_c8_NoPushToken(self):
        driver = self.driver  
        Add_User(self)
        driver.find_element_by_name("sAccount").send_keys("push002")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_name("email").send_keys("kevinlin@changingtec.com")        
        driver.find_element_by_name("sDesc").send_keys("001")
        driver.find_element_by_name("keyword").send_keys("001")
        select = Select(driver.find_element_by_id("deviceType"))
        found = False
        
        for op in select.options:  # 取得下拉選單清單
            selectList = op.text
            if selectList.find("Push") > -1:
                found = True
                
        self.assertEqual(found, False)
        print("26. No Push Token")

    def test_c9_QueryNotExistUser(self):
        driver = self.driver  
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_name("accname").send_keys("aaa")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        table = driver.find_element_by_xpath(".//td[contains(text(), 'No Data')]")  # 表單文字截取 
        output = table.text
        self.assertEqual(output, "No Data")
        print("27. NotExistUser")

    def test_d1_QuerySpecialUser(self):
        driver = self.driver  
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_name("accname").send_keys("a?a")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Account] Correct character: 0~9, a~z, A~Z, ._-*@")
        print("28. [Account] Correct character: 0~9, a~z, A~Z, ._-*@")

    def test_d2_QuerAllUser(self):
        driver = self.driver  
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        myList = ["OT001", "Push001", "OD001", "sw002", "sw001", "hw002", "hw001", "cg004"
                  , "cg003", "cg002", "cg001", "api"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])     
        print("29. Show all data")

    def test_d3_BackToSearchPage(self):
        driver = self.driver  
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        output = driver.find_element_by_class_name("title").text  # 表單文字截取 
        self.assertEqual(output, "Search OTP User")    
        print("30. Back to search page")

    def test_d4_QueryWildcardChar(self):
        driver = self.driver  
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_name("accname").send_keys("cg0*")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        table1 = driver.find_element_by_xpath(".//td[contains(text(), 'cg001')]")  # 表單文字截取
        output1 = table1.text
        table2 = driver.find_element_by_xpath(".//td[contains(text(), 'cg002')]")
        output2 = table2.text
        table3 = driver.find_element_by_xpath(".//td[contains(text(), 'cg003')]")
        output3 = table3.text
        table4 = driver.find_element_by_xpath(".//td[contains(text(), 'cg004')]")
        output4 = table4.text
        self.assertEqual(output1, "cg001")
        self.assertEqual(output2, "cg002")
        self.assertEqual(output3, "cg003")
        self.assertEqual(output4, "cg004")
        print("31. Show cg0*")

    def test_d5_DownloadUser(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        Select(driver.find_element_by_name("dtype")).select_by_visible_text("UTF-8")
        sleep(2)
        with open("E:\selenium_py\MOTP_Selenium\UseOTPStatisticsInfo.csv", "r") as f: # Read CSV 
            reader = csv.reader(f)
            myList = []
            for row in reader:
                myList.append(row)
            listData = myList[0]
            data = ['Account', 'Type', 'SN', 'User Status', 'Token Status', 'Last verify time', 'Error', 'Group']
            self.assertEqual(data, myList[0])

        os.remove("E:\selenium_py\MOTP_Selenium\UseOTPStatisticsInfo.csv")  # Delete File
        print("32. Download User")

    def test_d6_ModifyEmptyPhone(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("phone").clear()
        driver.find_element_by_name("phone").send_keys("")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")        
        driver.find_element_by_xpath("//input[@value='Send test']").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Phone Number] Please fill the fields.")
        print("33. [Phone Number] Please fill the fields.")

    def test_d7_ModifyLengthPhone(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("phone").clear()
        driver.find_element_by_name("phone").send_keys("111")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Phone Number] The length of the data fail.")
        print("34. [Phone Number] The length of the data fail.")

    def test_d8_ModifySpecialPhone(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("phone").clear()
        driver.find_element_by_name("phone").send_keys("123%^&123")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Phone Number] Correct character: 0~9")
        print("35. [Phone Number] Correct character: 0~9")

    def test_d9_ModifyPhone(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("phone").clear()
        driver.find_element_by_name("phone").send_keys("0958545874")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")        
        driver.find_element_by_xpath("//input[@value='Send test']").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:35] # 字串截取
        self.assertEqual(output, " Have sent test and modify success.")     
        print("36. Have sent test and modify success.")

    def test_e1_ModifyEmptyEmail(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("email1").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")
        driver.find_element_by_xpath("(//input[@value='Send test'])[2]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("37. Invalid Email.")

    def test_e2_ModifySpecialEmail(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("email1").clear()
        driver.find_element_by_name("email1").send_keys("a?a")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("38. Invalid Email.")

    def test_e3_ModifyEmail(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("email1").clear()
        driver.find_element_by_name("email1").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")        
        driver.find_element_by_xpath("(//input[@value='Send test'])[2]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:35] # 字串截取
        self.assertEqual(output, " Have sent test and modify success.")     
        print("39. Have sent test and modify success.")

    def test_e4_ModifySpecialDescription(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("sDesc").clear()
        driver.find_element_by_name("sDesc").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("40. [Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_e5_ModifyDescription(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("sDesc").clear()
        driver.find_element_by_name("sDesc").send_keys("hw001")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")     
        print("41. User modify success.")

    def test_e6_ModifySpecialKeyword(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("keyword").clear()
        driver.find_element_by_name("keyword").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Keywords] Correct character: 0~9, a~z, A~Z, ._-/")
        print("42. [Keywords] Correct character: 0~9, a~z, A~Z, ._-/")

    def test_e7_ModifyKeyword(self):
        driver = self.driver      
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("keyword").clear()
        driver.find_element_by_name("keyword").send_keys("hw001")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")     
        print("43. User modify success.")

    def test_e8_ModifyEmptyPassword(self):
        driver = self.driver
        RegisterResult = RegisterToken.RegisterToken(self, "hw001", "18709")
        self.assertEqual(RegisterResult, "Verify OTP")        
        Query_User(self)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] Please fill the fields.")
        print("44. [New Password] Please fill the fields.")

    def test_e9_ModifyLengthPassword(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("1")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] The length of the data fail.")
        print("45. [New Password] The length of the data fail.")

    def test_f1_ModifySpecialPassword(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("46. [New Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")       

    def test_f2_ModifyEmptyRetypePassword(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("321321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Please fill the fields.")
        print("47. [Re-type PW] Please fill the fields.")     

    def test_f3_ModifyLengthRetypePassword(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("321321")
        driver.find_element_by_name("accnewrepw").send_keys("321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")
        print("48. [Re-type PW] The length of the data fail.")      

    def test_f4_ModifySpecialRetypePassword(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("321321")
        driver.find_element_by_name("accnewrepw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("49. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")   

    def test_f5_ModifyDifferentPassword(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("321321")
        driver.find_element_by_name("accnewrepw").send_keys("789789")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Re-type password error.")
        print("50. Re-type password error.")     

    def test_f6_ModifyAccountSucceed(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("accnewpw").send_keys("321321")
        driver.find_element_by_name("accnewrepw").send_keys("321321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")
        print("51. User modify success.")        

    def test_f7_CancelSuspend(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span").click()
        driver.find_element_by_css_selector("button.default").click()
        output = driver.find_element_by_xpath("//td[2]/span").text
        self.assertEqual(output, "Suspend")
        print("52. Cancel Suspend")  

    def test_f8_SuspendUser(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span").click()
        driver.find_element_by_css_selector("button[type=\"button\"]").click()
        output = driver.find_element_by_xpath("//td[2]/span").text
        self.assertEqual(output, "Unsuspend")
        print("53. Suspend User")    

    def test_f9_ModifySuspendSpecialEmail(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("email1").clear()
        driver.find_element_by_name("email1").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("54. Invalid Email.")

    def test_g1_ModifySuspendEmailSucceed(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("email1").clear()
        driver.find_element_by_name("email1").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User modify success.")
        print("55. User modify success.")   

    def test_g2_SendTempOTP(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_name("days").clear()
        driver.find_element_by_name("days").send_keys("10")
        driver.find_element_by_id("notify").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:27] # 字串截取
        self.assertEqual(output, " The temp OTP send success.")
        print("56. The temp OTP send success.")  

    def test_g3_UnsuspendUser(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span").click()
        driver.find_element_by_css_selector("button[type=\"button\"]").click()
        output = driver.find_element_by_xpath("//td[2]/span").text
        self.assertEqual(output, "Suspend")
        print("57. Unsuspend User")   

    def test_g4_AddExistToken(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_xpath("//td[3]/span").click()
        driver.find_element_by_name("ht_serial").clear()
        driver.find_element_by_name("ht_serial").send_keys("18709")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:46] # 字串截取
        self.assertEqual(output, " SN already register, please confirm the data.")
        print("58. SN already register, please confirm the data.")  

    def test_g5_AddToken(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[8]/td[2]").click()
        driver.find_element_by_xpath("//td[3]/span").click()
        driver.find_element_by_name("ht_serial").clear()
        driver.find_element_by_name("ht_serial").send_keys("18717")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:49] # 字串截取
        self.assertEqual(output, " User create and hardware token register success.")
        print("59. User create and hardware token register success.")   

    def test_g6_PromoteAdminLengthPW(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[9]/td[2]").click()
        driver.find_element_by_xpath("//td[4]/span").click()
        driver.find_element_by_id("pass1").send_keys("321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Password] The length of the data fail.")        
        print("60. [Password] The length of the data fail.")   

    def test_g7_PromoteAdminSpecialPW(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[9]/td[2]").click()
        driver.find_element_by_xpath("//td[4]/span").click()
        driver.find_element_by_id("pass1").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")        
        print("61. [Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_g8_PromoteAdminLengthRePW(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[9]/td[2]").click()
        driver.find_element_by_xpath("//td[4]/span").click()
        driver.find_element_by_id("pass1").send_keys("321321")
        driver.find_element_by_id("pass2").send_keys("321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")        
        print("62. [Re-type PW] The length of the data fail.")

    def test_g9_PromoteAdminSpecialRePW(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[9]/td[2]").click()
        driver.find_element_by_xpath("//td[4]/span").click()
        driver.find_element_by_id("pass1").send_keys("321321")
        driver.find_element_by_id("pass2").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")        
        print("63. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")   

    def test_h1_PromoteAdminDifferentPW(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[9]/td[2]").click()
        driver.find_element_by_xpath("//td[4]/span").click()
        driver.find_element_by_id("pass1").send_keys("321321")
        driver.find_element_by_id("pass2").send_keys("123123")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Re-type password error.")        
        print("64. Re-type password error.")   

    def test_h2_PromoteAdminSucceed(self):
        driver = self.driver
        Query_User(self)
        driver.find_element_by_name("accname").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[9]/td[2]").click()
        driver.find_element_by_xpath("//td[4]/span").click()
        Select(driver.find_element_by_id("accnewrole")).select_by_visible_text("Super")
        driver.find_element_by_id("pass1").send_keys("321321")
        driver.find_element_by_id("pass2").send_keys("321321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:35] # 字串截取
        self.assertEqual(output, " The user becomes an administrator.")   
        print("65. The user becomes an administrator.")   





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
