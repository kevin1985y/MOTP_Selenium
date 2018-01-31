#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xmlrunner
from time import sleep

class Profile(unittest.TestCase):
    def setUp(self):

        self.driver =webdriver.Chrome("chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.base_url = "http://192.168.0.201:8080/MOTPWeb"
        self.verificationErrors = []
        self.accept_next_alert = True       
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("123123")
        driver.find_element_by_id("mypass").submit()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        ##driver.find_element_by_css_selector("span.hand > img").click() # 切換成中文
        ##print("Login Success.")

    def test_a1_Profile_CancelBTN(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()        
        welcome = driver.find_element_by_xpath(".//b[contains(text(), 'Welcome to use MOTP')]") # 畫面文字截取
        output = welcome.text
        self.assertEqual(output, "Welcome to use MOTP")
        print ("1. Back to HomePage")
       
    def test_a2_profile_WrongFomatEmail(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("acceditmail").clear()
        driver.find_element_by_name("acceditmail").send_keys("kevinlin")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("2. Invalid Email.")
        
    def test_a3_profile_SpecialEmail(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("acceditmail").clear()
        driver.find_element_by_name("acceditmail").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("3. Invalid Email.")

    def test_a4_profile_ModifyEmailSucceed(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("acceditmail").clear()
        driver.find_element_by_name("acceditmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account modify success.")
        print("4. Account modify success.")

    def test_a5_profile_SpecialDescription(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("acceditdesc").clear()
        driver.find_element_by_name("acceditdesc").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("5. [Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_a6_profile_ModifyDescriptionSucceed(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("acceditdesc").clear()
        driver.find_element_by_name("acceditdesc").send_keys("Kevin_Testing")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:24] # 字串截取
        self.assertEqual(output, " Account modify success.")
        print("6. Account modify success.")

    def test_a7_profile_EmptyOldPassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Old Password] Please fill the fields.")
        print("7. [Old Password] Please fill the fields.")

    def test_a8_profile_EmptyNewPassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] Please fill the fields.")
        print("8. [New Password] Please fill the fields.")

    def test_a9_profile_LengthNewPassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("123")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] The length of the data fail.")
        print("9. [New Password] The length of the data fail.")

    def test_b1_profile_SpecialNewPassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[New Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("10. [New Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_b2_profile_EmptyRetypePassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Please fill the fields.")
        print("11. [Re-type PW] Please fill the fields.")

    def test_b3_profile_LengthRetypePassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").clear()
        driver.find_element_by_name("retypepw").send_keys("321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")
        print("12. [Re-type PW] The length of the data fail.")

    def test_b4_profile_SpecialRetypePassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").clear()
        driver.find_element_by_name("retypepw").send_keys("~!@# ~!@")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("13. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_b5_profile_DifferentPassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").clear()
        driver.find_element_by_name("retypepw").send_keys("123456")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "Re-type password error.")
        print("14. Re-type password error.")

    def test_b6_profile_WrongOldPassword(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("456456")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").clear()
        driver.find_element_by_name("retypepw").send_keys("321321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        

        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:45] # 字串截取
        self.assertEqual(output, " Old password incorrect! Account modify fail.")
        print("15. Old password incorrect! Account modify fail.")

    def test_b7_profile_ModifyPasswordSucceed(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        driver.find_element_by_name("checkpw").click()
        driver.find_element_by_name("oldpw").clear()
        driver.find_element_by_name("oldpw").send_keys("123123")
        driver.find_element_by_name("newpw").clear()
        driver.find_element_by_name("newpw").send_keys("321321")
        driver.find_element_by_name("retypepw").clear()
        driver.find_element_by_name("retypepw").send_keys("321321")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        CodeSusses = driver.find_element_by_class_name("CodeSusses").text
        output = CodeSusses[0:37] # 字串截取
        self.assertEqual(output, " Account and password modify success.")
        print("16. Account and password modify success.")
    

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
        #print ("Logout...")
        ##driver = self.driver
        ##driver.find_element_by_xpath("//span[@onclick=\"handleDialog('17em','Logout','Are you sure to logout?',0,'index.jsp?doLogout=1');\"]").click()
        ##driver.find_element_by_css_selector("button[type=\"button\"]").click() # 登出
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
