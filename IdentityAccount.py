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
import AuthenticationToken

def Add_Admin(self):
    driver = self.driver
    ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
    ActionChains(driver).move_to_element(ID).perform()
    driver.find_element_by_css_selector("ul.submenu > li").click()
    driver.find_element_by_css_selector("input[type=\"button\"]").click()        

class Administrator(unittest.TestCase):
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

    def test_a1_AddAdminPage(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()        
        output = driver.find_element_by_class_name("title").text
        self.assertEqual(output, "Create Account")
        print("1. Create Account Page")        

    def test_a2_EmptyAccount(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Account] Please fill the fields.")
        print("2. [Account] Please fill the fields.")

    def test_a3_SpecialAccount(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("~!@#")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Account] Correct character: 0~9, a~z, A~Z, ._-")
        print("3. [Account] Correct character: 0~9, a~z, A~Z, ._-")

    def test_a4_EmptyPassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Password] Please fill the fields.")
        print("4. [Password] Please fill the fields.")

    def test_a5_LengthPassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("1")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Password] The length of the data fail.")
        print("5. [Password] The length of the data fail.")

    def test_a6_SpecialPassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("6. [Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_a7_EmptyRetypePassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Please fill the fields.")
        print("7. [Re-type PW] Please fill the fields.")

    def test_a8_LengthRetypePassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("1")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")
        print("8. [Re-type PW] The length of the data fail.")

    def test_a9_SpecialRetypePassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("9. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_b1_DifferentPassword(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123456")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Re-type password error.")
        print("10. Re-type password error.")

    def test_b2_WrongFomatEmail(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("11. Invalid Email.")

    def test_b3_SpecialEmail(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("12. Invalid Email.")

    def test_b4_SpecialDescription(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cgtest001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("accnewdesc").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()    
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("13. [Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_b5_AddSuperAccount(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cg001")
        Select(driver.find_element_by_id("accnewrole")).select_by_visible_text("Super") # 下拉選單
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("accnewdesc").send_keys("cg001")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account create success.")
        print("14. Account create success.")

    def test_b6_DuplicateAccountLower(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cg001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:47] # 字串截取
        self.assertEqual(output, " This account is used, please use the other ID.")
        print("15.This account is used, please use the other ID.")

    def test_b7_DuplicateAccountUpper(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("CG001")
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:47] # 字串截取
        self.assertEqual(output, " This account is used, please use the other ID.")
        print("16.This account is used, please use the other ID.")

    def test_b8_AddOperatorAccount(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cg002")
        Select(driver.find_element_by_id("accnewrole")).select_by_visible_text("Operator") # 下拉選單
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("accnewdesc").send_keys("cg002")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account create success.")
        print("17. Account create success.")

    def test_b9_AddOTPUsersAccount(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cg003")
        Select(driver.find_element_by_id("accnewrole")).select_by_visible_text("OTPUsers") # 下拉選單
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("accnewdesc").send_keys("cg003")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account create success.")
        print("18. Account create success.")

    def test_c1_AddAPIAccount(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("cg004")
        Select(driver.find_element_by_id("accnewrole")).select_by_visible_text("API") # 下拉選單
        driver.find_element_by_name("accnewpw").send_keys("123123")
        driver.find_element_by_name("accnewrepw").send_keys("123123")
        driver.find_element_by_name("accnewmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("accnewdesc").send_keys("cg004")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account create success.")
        print("19. Account create success.")

    def test_c2_LengthLimit(self):
        driver = self.driver
        Add_Admin(self)
        driver.find_element_by_name("accnewname").send_keys("1234567890qwertyuiop1234567890asf")
        driver.find_element_by_name("accnewpw").send_keys("1234567890qwertyuiop1234567890asf")
        driver.find_element_by_name("accnewrepw").send_keys("1234567890qwertyuiop1234567890asf")
        driver.find_element_by_name("accnewmail").send_keys("1234567890qwertyuiop1234567890as1234567890qwertyuiop1234567890as1234567890qwertyu")
        driver.find_element_by_name("accnewdesc").send_keys("1234567890qwertyuiop1234567890as1234567890qwertyuiop1234567890as1234567890qwertyu")
        nameText = driver.find_element_by_name("accnewname")
        name = nameText.get_attribute('value') # 取文字框中的值
        PasswordText = driver.find_element_by_name("accnewpw")
        Password = PasswordText.get_attribute('value') # 取文字框中的值        
        rePWText = driver.find_element_by_name("accnewrepw")
        rePW = rePWText.get_attribute('value') # 取文字框中的值
        mailText = driver.find_element_by_name("accnewmail")
        mail = mailText.get_attribute('value') # 取文字框中的值
        descText = driver.find_element_by_name("accnewdesc")
        desc = descText.get_attribute('value') # 取文字框中的值
        self.assertEqual(name, "1234567890qwertyuiop1234567890as")
        self.assertEqual(Password, "1234567890qwertyuiop1234567890as")
        self.assertEqual(rePW, "1234567890qwertyuiop1234567890as")
        self.assertEqual(mail, "1234567890qwertyuiop1234567890as1234567890qwertyuiop1234567890as1234567890qwerty")
        self.assertEqual(desc, "1234567890qwertyuiop1234567890as1234567890qwertyuiop1234567890as1234567890qwerty") 
        print("20. Length Limit")

    def test_c3_QueryNotExistAccount(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_name("account_name").send_keys("aaa")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click() 
        table = driver.find_element_by_xpath(".//td[contains(text(), 'No Data')]")  # 表單文字截取 
        output = table.text
        self.assertEqual(output, "No Data")
        print("21. NotExistAccount")

    def test_c4_QuerySpecialAccount(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_name("account_name").send_keys("a?a")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()   
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Account Name] Correct character: 0~9, a~z, A~Z, ._-*@")
        print("22. [Account Name] Correct character: 0~9, a~z, A~Z, ._-*@")
    '''
    def test_c5_QueryAllAccount(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        table1 = driver.find_element_by_xpath(".//td[contains(text(), 'admin')]")  # 表單文字截取 
        output1 = table1.text
        table2 = driver.find_element_by_xpath(".//td[contains(text(), 'api')]")
        output2 = table2.text
        table3 = driver.find_element_by_xpath(".//td[contains(text(), 'cg001')]")
        output3 = table3.text
        table4 = driver.find_element_by_xpath(".//td[contains(text(), 'cg002')]")
        output4 = table4.text
        table5 = driver.find_element_by_xpath(".//td[contains(text(), 'cg003')]")
        output5 = table5.text
        table6 = driver.find_element_by_xpath(".//td[contains(text(), 'cg004')]")
        output6 = table6.text
        table7 = driver.find_element_by_xpath(".//td[contains(text(), 'cgadmin')]")
        output7 = table7.text
        table8 = driver.find_element_by_xpath(".//td[contains(text(), 'op')]")
        output8 = table8.text        
        self.assertEqual(output1, "admin")
        self.assertEqual(output2, "api")
        self.assertEqual(output3, "cg001")
        self.assertEqual(output4, "cg002")
        self.assertEqual(output5, "cg003")
        self.assertEqual(output6, "cg004")
        self.assertEqual(output7, "cgadmin")
        self.assertEqual(output8, "op")        
        print("23. Show all data")
    '''
    def test_c5_QueryAllAccount(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        myList = ["admin", "api", "cg001", "cg002", "cg003", "cg004", "cgadmin", "op"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("23. Show all data")

    def test_c6_BackToSearchPage(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        output = driver.find_element_by_class_name("title").text  # 表單文字截取 
        self.assertEqual(output, "Search Account")       
        print("24. Back to search page")

    def test_c7_QueryWildcardChar(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_name("account_name").send_keys("cg0*")
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
        print("25. Show cg0*")

    def test_c8_ModifyRole(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()  # 表格第六筆資料
        Select(driver.find_element_by_id("acceditrole")).select_by_visible_text("Operator")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account modify success.")
        print("26. Account modify success.")

    def test_c9_ModifyWrongFomatEmail(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("acceditmail").clear()
        driver.find_element_by_name("acceditmail").send_keys("kevinlin")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("27. Invalid Email.")

    def test_d1_ModifySpecialEmail(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("acceditmail").clear()
        driver.find_element_by_name("acceditmail").send_keys("a?a")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("28. Invalid Email.")

    def test_d2_ModifySpecialDescription(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("acceditdesc").clear()
        driver.find_element_by_name("acceditdesc").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("29. [Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_d3_ModifyEmptyPassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] Please fill the fields.")
        print("30. [New Password] Please fill the fields.")

    def test_d4_ModifyLengthPassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("123")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] The length of the data fail.")
        print("31. [New Password] The length of the data fail.")

    def test_d5_ModifySpecialPassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("32. [New Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_d6_ModifyEmptyRetypePassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("321321")   
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Please fill the fields.")
        print("33. [Re-type PW] Please fill the fields.")

    def test_d7_ModifyLengthRetypePassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").send_keys("321")        
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")
        print("34. [Re-type PW] The length of the data fail.")        

    def test_d8_ModifySpecialRetypePassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").send_keys("~!@# ~!@")        
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("35. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_d9_ModifyDifferentPassword(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").send_keys("789789")        
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Re-type password error.")
        print("36. Re-type password error.")     

    def test_e1_ModifyAccountSucceed(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").send_keys("321321")        
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:37] # 字串截取
        self.assertEqual(output, " Account and password modify success.")
        print("37. Account and password modify success.")   

    def test_e2_CancelStopRights(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_xpath("//td[3]/span").click()
        driver.find_element_by_css_selector("button.default").click()
        output = driver.find_element_by_xpath("//td[3]/span").text
        self.assertEqual(output, "Stop Rights")
        print("38. Cancel Stop Rights")

    def test_e3_StopRights(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_xpath("//td[3]/span").click()
        driver.find_element_by_css_selector("button[type=\"button\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:29] # 字串截取
        self.assertEqual(output, " Account stop rights success.")
        print("39. Account stop rights success.")

    def test_e4_CancelRehabilitate(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        sleep(1)
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_xpath("//td[3]/span").click()
        driver.find_element_by_css_selector("button.default").click()
        output = driver.find_element_by_xpath("//td[3]/span").text
        self.assertEqual(output, "Rehabilitate")
        print("40. Cancel Rehabilitate")
        
    def test_e5_Rehabilitate(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_xpath("//td[3]/span").click()
        driver.find_element_by_css_selector("button[type=\"button\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:37] # 字串截取
        self.assertEqual(output, " Account rehabilitate rights success.")
        print("41. Account rehabilitate rights success.")

    def test_e6_ModifyUsingHWOTP(self):
        driver = self.driver    
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[2]/td/table/tbody/tr[3]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("42. User create success.")

    def test_e7_ModifyUsingHWOTPWithSN(self):
        driver = self.driver
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\HW_1.csv"
        ImportResult = AuthenticationToken.ImportToken(self, Path)
        self.assertEqual(ImportResult, "- Import Success: 5")
        
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[4]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        driver.find_element_by_name("ht_serial").send_keys("18694")
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:49] # 字串截取
        self.assertEqual(output, " User create and hardware token register success.")
        print("43. User create and hardware token register success.")

    def test_e8_ModifyUsingNoSWOTP(self):
        driver = self.driver    
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[5]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("SoftwareToken")        
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:18] # 字串截取
        self.assertEqual(output, " User create fail.")
        print("44. User create fail.")

    def test_e9_ModifyUsingSWOTP(self):
        driver = self.driver
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\SW_1.csv"
        ImportResult = AuthenticationToken.ImportToken(self, Path)
        self.assertEqual(ImportResult, "- Import Success: 3")
        
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[5]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("SoftwareToken")    
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("45. User create success.")

    def test_f1_ModifyUsingNoODOTP(self):
        driver = self.driver    
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[6]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("On-Demand")        
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:18] # 字串截取
        self.assertEqual(output, " User create fail.")
        print("46. User create fail.")

    def test_f2_ModifyUsingODOTP(self):
        driver = self.driver
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\OD_1.csv"
        ImportResult = AuthenticationToken.ImportToken(self, Path)
        self.assertEqual(ImportResult, "- Import Success: 2")
        
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[6]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("On-Demand")    
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("47. User create success.")
        
    def test_f3_ModifyUsingNoPushOTP(self):
        driver = self.driver    
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("PushToken")        
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:18] # 字串截取
        self.assertEqual(output, " User create fail.")
        print("48. User create fail.")

    def test_f4_ModifyUsingPushOTP(self):
        driver = self.driver
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\pushToken_1.csv"
        ImportResult = AuthenticationToken.ImportToken(self, Path)
        self.assertEqual(ImportResult, "- Import Success: 8")
        
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("//tr[7]/td[2]").click()
        driver.find_element_by_css_selector("td.hand.headItem > span.hand").click()
        Select(driver.find_element_by_id("deviceType")).select_by_visible_text("PushToken")    
        driver.find_element_by_name("OTPCreatebtn").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:21] # 字串截取
        self.assertEqual(output, " User create success.")
        print("49. User create success.")

    def test_f5_QueryChangeItemPerPage(self):
        driver = self.driver
        for i in range(5, 9):
            Add_Admin(self)
            driver.find_element_by_name("accnewname").send_keys("cg00" + str(i))
            driver.find_element_by_name("accnewpw").send_keys("123123")
            driver.find_element_by_name("accnewrepw").send_keys("123123")
            driver.find_element_by_css_selector("input[type=\"submit\"]").click()
            CodeSusses = driver.find_element_by_class_name("CodeSusses").text
            output = CodeSusses[0:24] # 字串截取
            self.assertEqual(output, " Account create success.")

        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        myList = ["admin", "api", "cg001", "cg002", "cg003", "cg004", "cg005", "cg006", "cg007", "cg008", "cgadmin", "op"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("50. Show all data")

    def test_f6_SwitchItemPerPage(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        myList = ["admin", "api", "cg001", "cg002", "cg003", "cg004", "cg005", "cg006", "cg007", "cg008", "cgadmin", "op"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("51. Show all data")

    def test_f7_DeleteNoChoice(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("#pageLeft > input[type=\"button\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "No choice!")
        print("52. No choice!")

    def test_f8_CancelDelete(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_name("box5").click()
        driver.find_element_by_css_selector("#pageLeft > input[type=\"button\"]").click()
        driver.find_element_by_css_selector("button.default").click()
        table4 = driver.find_element_by_xpath(".//td[contains(text(), 'cg004')]")
        output = table4.text
        self.assertEqual(output, "cg004")
        print("53. Cancel Delete")

    def test_f9_DeleteAdmin(self):
        driver = self.driver
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_name("box6").click()
        driver.find_element_by_name("box7").click()
        driver.find_element_by_name("box8").click()
        driver.find_element_by_name("box9").click()
        driver.find_element_by_css_selector("#pageLeft > input[type=\"button\"]").click()
        driver.find_element_by_css_selector("button[type=\"button\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account delete success.")
        print("54. Account delete success.")

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
