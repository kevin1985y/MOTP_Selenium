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

    def test_a1_WelcomeNextBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        output = driver.find_element_by_class_name("step_font2").text
        self.assertEqual(output, "IP Setting")
        print("1. IP Setting")

    def test_a2_IPSettingBackBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnBack").click()
        output = driver.find_element_by_class_name("wel_title").text
        self.assertEqual(output, "Welcome to use MOTP")
        print("2. Welcome to use MOTP")

    def test_a3_IPSettingNextBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        content = driver.find_element_by_id("step2").text
        output = content[0:20]
        self.assertEqual(output, "Step 2 : DNS Setting")
        print("3. Step 2 : DNS Setting")

    def test_a4_DNSSettingBackBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnBack").click()
        output = driver.find_element_by_class_name("step_font2").text
        self.assertEqual(output, "IP Setting")
        print("4. IP Setting")

    def test_a5_DNSSettingNextBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        content = driver.find_element_by_id("step3").text
        output = content[0:23]
        self.assertEqual(output, "Step 3 : Create Account")
        print("5. Step 3 : Create Account")

    def test_a6_CreateAccountBackBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnBack").click()
        content = driver.find_element_by_id("step2").text
        output = content[0:20]
        self.assertEqual(output, "Step 2 : DNS Setting")
        print("6. Step 2 : DNS Setting")

    def test_a7_CreateAccountNextBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        content = driver.find_element_by_id("step5").text
        output = content[0:22]
        self.assertEqual(output, "Step 4 : System Config")
        print("7. Step 4 : System Config")

    def test_a8_EmptyAccount(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_pass").send_keys("321321")        
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Account] Please fill the fields.")
        print("8. [Account] Please fill the fields.")

    def test_a9_SpecialAccount(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("~!@# ~!@")        
        driver.find_element_by_name("step3_pass").send_keys("123123")        
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Account] Correct character: 0~9, a~z, A~Z, ._-")
        print("9. [Account] Correct character: 0~9, a~z, A~Z, ._-")

    def test_b1_EmptyPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")            
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Password] Please fill the fields.")
        print("10. [Password] Please fill the fields.")

    def test_b2_LengthPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("1")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Password] The length of the data fail.")
        print("11. [Password] The length of the data fail.")

    def test_b3_SpecailPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("~!@# ~!@")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("12. [Password] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_b4_EmptyRetypePassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Re-type PW] Please fill the fields.")
        print("13. [Re-type PW] Please fill the fields.")

    def test_b5_LengthRetypePassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("1")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Re-type PW] The length of the data fail.")
        print("14. [Re-type PW] The length of the data fail.")

    def test_b6_SpecialRetypePassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("~!@# ~!@")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")
        print("15. [Re-type PW] Correct character: 0~9, a~z, A~Z, !#*:;,.?/$@")

    def test_b7_DifferentPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123456")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "Re-type password error.")
        print("16. Re-type password error.")

    def test_b8_WrongFomatEmail(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin")        
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("17. Invalid Email.")

    def test_b9_SpecialEmail(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("~!@# ~!@")        
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("18. Invalid Email.")

    def test_c1_SpecialDescription(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("~!@# ~!@")
        driver.find_element_by_id("btnNext").click()
        Account_alert = driver.switch_to.alert
        output = Account_alert.text
        Account_alert.accept()
        self.assertEqual(output, "[Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("19. [Description] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_c2_CreateAccount(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        content = driver.find_element_by_id("step5").text
        output = content[0:22]
        self.assertEqual(output, "Step 4 : System Config")
        print("20. Created Account")

    def test_c3_SystemConfigBackBTN(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnBack").click()
        content = driver.find_element_by_id("step3").text
        output = content[0:23]
        self.assertEqual(output, "Step 3 : Create Account")
        print("21. Step 3 : Create Account")

    def test_c4_EmptyServerName(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("ServerName").clear()
        driver.find_element_by_id("btnNext").click()
        Config_alert = driver.switch_to.alert
        output = Config_alert.text
        Config_alert.accept()
        self.assertEqual(output, "[ServerName] Please fill the fields.")
        print("22. [ServerName] Please fill the fields.")

    def test_c5_SpecialServerName(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("ServerName").clear()
        driver.find_element_by_name("ServerName").send_keys("192+168.11")
        driver.find_element_by_id("btnNext").click()
        Config_alert = driver.switch_to.alert
        output = Config_alert.text
        Config_alert.accept()
        self.assertEqual(output, "[ServerName] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("23. [ServerName] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")

    def test_c6_SpecialSMTPServer(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("SMTPServer").send_keys("smtp.changingtec.com!")
        driver.find_element_by_id("btnNext").click()
        Config_alert = driver.switch_to.alert
        output = Config_alert.text
        Config_alert.accept()
        self.assertEqual(output, "[SMTPServer] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
        print("24. [SMTPServer] Incorrect character `~!@#$%^&*()=+{}[];:'\",/?<>")
    '''
    Bug Redmine #5669
    def test_c7_WrongFomatEmail(self): # Redmine #5669
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("SMTPServer").send_keys("smtp.changingtec.com")
        driver.find_element_by_name("AdminEmail").send_keys("kevinlin")
        driver.find_element_by_id("btnNext").click()
        Config_alert = driver.switch_to.alert
        output = Config_alert.text
        Config_alert.accept()
        self.assertEqual(output, "Invalid Email.")
        print("25. Invalid Email.")
    '''
    def test_c8_EmptySMTPPassword(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("SMTPServer").send_keys("smtp.changingtec.com")
        driver.find_element_by_name("AdminEmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("SMTPUsername").send_keys("mx3100n@changingtec.com")
        driver.find_element_by_id("btnNext").click()
        Config_alert = driver.switch_to.alert
        output = Config_alert.text
        Config_alert.accept()
        self.assertEqual(output, "[SMTPPassword] Please fill the fields.")
        print("26. [SMTPPassword] Please fill the fields.")
        
    def test_c9_SettingDone(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("admin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("admin")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("step3_name").send_keys("cgadmin")
        driver.find_element_by_name("step3_pass").send_keys("123123")
        driver.find_element_by_name("step3_repw").send_keys("123123")
        driver.find_element_by_name("step3_mail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("step3_desc").send_keys("cgadmin-test")
        driver.find_element_by_id("btnNext").click()
        driver.find_element_by_name("SMTPServer").send_keys("smtp.changingtec.com")
        driver.find_element_by_name("AdminEmail").send_keys("kevinlin@changingtec.com")
        driver.find_element_by_name("SMTPUsername").send_keys("mx3100n@changingtec.com")
        driver.find_element_by_name("SMTPPassword").send_keys("123123")
        driver.find_element_by_id("btnNext").click()
        finish = driver.find_element_by_class_name("step_content").text
        output = finish[0:39] # 字串截取
        self.assertEqual(output, "Initial system setup has been completed")
        print("27. Step 5 : Finish")

    def test_d1_cgadminLogin(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("123123")
        driver.find_element_by_id("mypass").submit()
        ##alert(self)
        welcome = driver.find_element_by_xpath(".//b[contains(text(), 'Welcome to use MOTP')]") # 畫面文字截取
        output = welcome.text
        self.assertEqual(output, "Welcome to use MOTP")
        print("28. Home Page")

    def test_d2_CheckcgadminProfile(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("123123")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('AccountSelfData.jsp')\"]").click()
        mailText = driver.find_element_by_name("acceditmail")
        mail = mailText.get_attribute('value') # 取文字框中的值        
        descText = driver.find_element_by_name("acceditdesc")
        description = descText.get_attribute('value') # 取文字框中的值 
        self.assertEqual(mail, "kevinlin@changingtec.com")
        self.assertEqual(description, "cgadmin-test")
        print("29. Check fine")

    def test_d3_CheckcgadminAdmin(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("123123")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        ID = driver.find_element_by_xpath(".//li[contains(text(), 'Identity Account')]") # 選單文字截取        
        ActionChains(driver).move_to_element(ID).perform()
        driver.find_element_by_css_selector("ul.submenu > li").click()
        driver.find_element_by_name("account_name").clear()
        driver.find_element_by_name("account_name").send_keys("cgadmin")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()        
        table = driver.find_element_by_xpath(".//td[contains(text(), 'cgadmin')]")  # 表單文字截取 
        output = table.text
        self.assertEqual(output, "cgadmin")
        print("30. Check cgadmin")

    def test_d4_CheckSysConig(self):
        driver = self.driver
        driver.get(self.base_url + "/MOTPWeb")
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys("cgadmin")
        driver.find_element_by_id("mypass").clear()
        driver.find_element_by_id("mypass").send_keys("123123")
        driver.find_element_by_id("mypass").submit()
        alert(self)
        Sys = driver.find_element_by_xpath("//ol/li[9]") # 定位選單
        ActionChains(driver).move_to_element(Sys).perform()  
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('SystemOption.jsp')\"]").click()
        SMTPServerText = driver.find_element_by_name("SMTPServer")
        SMTPServer = SMTPServerText.get_attribute('value') #取文字框中的值   
        AdminEmailText = driver.find_element_by_name("AdminEmail")
        AdminEmail = AdminEmailText.get_attribute('value') #取文字框中的值
        SMTPUsernameText = driver.find_element_by_name("SMTPUsername")
        SMTPUsername = SMTPUsernameText.get_attribute('value') #取文字框中的值        
        self.assertEqual(SMTPServer, "smtp.changingtec.com")
        self.assertEqual(AdminEmail, "kevinlin@changingtec.com")
        self.assertEqual(SMTPUsername, "mx3100n@changingtec.com")
        print("31. Check SysConfig")

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
