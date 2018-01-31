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

def ImportToken(self, Path):
    driver = self.driver
    Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
    ActionChains(driver).move_to_element(Auth).perform()
    driver.find_element_by_xpath("//li[@onclick=\"linkpage('TokenImport.jsp')\"]").click()
    driver.find_element_by_id("File1").clear()
    driver.find_element_by_id("File1").send_keys(Path)  # 匯入檔案
    driver.find_element_by_name("OTPHTokenbtn").click()
    Result = driver.find_element_by_xpath(".//div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/table/tbody/tr[2]/td").text
    output = Result[0:19]
    return output

def DelToken(self):
    driver = self.driver
    Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
    ActionChains(driver).move_to_element(Auth).perform()
    driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
    Select(driver.find_element_by_name("ipp")).select_by_visible_text("500")
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    driver.find_element_by_css_selector("td.thStyle_01.selAll > img").click()
    driver.find_element_by_css_selector("#pageLeft > input[type=\"button\"]").click()
    driver.find_element_by_css_selector("button[type=\"button\"]").click()
    CodeSusses = driver.find_element_by_class_name("CodeSusses").text
    output = CodeSusses[0:22] # 字串截取
    return output

class Token(unittest.TestCase):
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

    def test_a1_ImportEmptyToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('TokenImport.jsp')\"]").click()
        driver.find_element_by_name("OTPHTokenbtn").click()
        alert = driver.switch_to.alert
        output = alert.text
        alert.accept()
        self.assertEqual(output, "[File Path] Please fill the fields.")
        print("1. [File Path] Please fill the fields.")

    def test_a2_ImportWrongFile(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('TokenImport.jsp')\"]").click()
        driver.find_element_by_id("File1").send_keys("D:\Kevin\MOTP\motpff.xlsx")  # 匯入檔案
        driver.find_element_by_name("OTPHTokenbtn").click()
        CodeFail = driver.find_element_by_class_name("CodeFail").text
        output = CodeFail[0:22] # 字串截取
        self.assertEqual(output, " The csv format error.")
        print("2. The csv format error.")
        
    def test_a3_ImportHWTokenSucceed(self):
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\HW_1.csv"
        output = ImportToken(self, Path)
        self.assertEqual(output, "- Import Success: 5")  
        print("3. Import HWToken Succeed")

    def test_a4_ImportSWTokenSucceed(self):
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\SW_1.csv"
        output = ImportToken(self, Path)
        self.assertEqual(output, "- Import Success: 3")  
        print("4. Import SWToken Succeed")

    def test_a5_ImportODTokenSucceed(self):
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\OD_1.csv"
        output = ImportToken(self, Path)
        self.assertEqual(output, "- Import Success: 2")  
        print("5. Import ODToken Succeed")        

    def test_a6_ImportPushTokenSucceed(self):
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\pushToken_1.csv"
        output = ImportToken(self, Path)
        self.assertEqual(output, "- Import Success: 8")  
        print("6. Import PushToken Succeed")

    def test_a7_QueryNotExistToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_name("serial").send_keys("aaa") 
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        output = driver.find_element_by_xpath(".//td[contains(text(), 'No Data')]").text  # 表單文字截取 
        self.assertEqual(output, "No Data")
        print("7. No Data")

    def test_a8_QueryHWToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_name("512").click()  # SW
        driver.find_element_by_name("1024").click()  # OD
        driver.find_element_by_name("2048").click()  # Other
        driver.find_element_by_name("8192").click()  # FISC
        driver.find_element_by_name("16384").click()  # Push
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["18694", "18709", "18717", "18724", "18731"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("8. Show all HW Token")

    def test_a9_QuerySWToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_name("256").click()  # HW
        driver.find_element_by_name("1024").click()
        driver.find_element_by_name("2048").click()
        driver.find_element_by_name("8192").click()
        driver.find_element_by_name("16384").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["100000016C23CA10", "10000002C917F998", "1000000315AE7B1F"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("9. Show all SW Token")
    
    def test_b1_QueryODToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_name("256").click()
        driver.find_element_by_name("512").click()
        driver.find_element_by_name("2048").click()
        driver.find_element_by_name("8192").click()
        driver.find_element_by_name("16384").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["OD100002015", "OD100002016"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("10. Show all OD Token")

    def test_b2_QueryPushToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_name("256").click()
        driver.find_element_by_name("512").click()
        driver.find_element_by_name("1024").click()
        driver.find_element_by_name("2048").click()
        driver.find_element_by_name("8192").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["10000001E2D5CB96", "10000002C1B14AE8", "10000003B01BDCEC", "10000004F85BCFC8", "1000000598E1984C", "10000006AE764FFB", "1000000706A9D04F", "100000082DCD7733"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("11. Show all Push Token")

    def test_b3_QuerySN(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_name("serial").send_keys("186*")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["18694"]
        webList = []
        for i in range(len(myList)):
            webList.append(driver.find_element_by_xpath(".//td[contains(text(), '" + myList[i] + "')]").text)  # 文字存取至webList           
            self.assertEqual(webList[i], myList[i])            
        print("12. Show Query SN Token")
  
    def test_b4_QuerySortByExpireDate(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_xpath("(//input[@name='sort'])[2]").click()  # The nearest expire date
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["18694", "18709", "18717", "18724", "18731", "100000016C23CA10", "10000002C917F998", "1000000315AE7B1F", "OD100002015", "OD100002016"
                  , "10000001E2D5CB96", "10000002C1B14AE8", "10000003B01BDCEC", "10000004F85BCFC8", "1000000598E1984C", "10000006AE764FFB", "1000000706A9D04F"
                  , "100000082DCD7733"]
        j = 1
        for i in range(len(myList)):
            j = j + 1     
            Result = driver.find_element_by_xpath("//form[@name='author']/table/tbody/tr[2]/td/table/tbody/tr["+ str(j) +"]/td[2]").text
            self.assertEqual(Result, myList[i])   
        print("13. Show Token Sort By Expire Date")

    def test_b5_QuerySortByInvalidDate(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_xpath("(//input[@name='sort'])[3]").click()  # The nearest expire date
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["100000016C23CA10", "10000001E2D5CB96", "10000002C1B14AE8", "10000002C917F998", "1000000315AE7B1F", "10000003B01BDCEC"
                  , "10000004F85BCFC8", "1000000598E1984C", "10000006AE764FFB", "1000000706A9D04F", "100000082DCD7733", "18694", "18709"
                  , "18717", "18724", "18731", "OD100002015", "OD100002016"]
        j = 1
        for i in range(len(myList)):
            j = j + 1     
            Result = driver.find_element_by_xpath("//form[@name='author']/table/tbody/tr[2]/td/table/tbody/tr["+ str(j) +"]/td[2]").text
            self.assertEqual(Result, myList[i])   
        print("14. Show Token Sort By Invalid Date")

    def test_b6_QueryChangeItemPerPage(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("25")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        myList = ["100000016C23CA10", "10000001E2D5CB96", "10000002C1B14AE8", "10000002C917F998", "1000000315AE7B1F", "10000003B01BDCEC"
                  , "10000004F85BCFC8", "1000000598E1984C", "10000006AE764FFB", "1000000706A9D04F", "100000082DCD7733", "18694", "18709"
                  , "18717", "18724", "18731", "OD100002015", "OD100002016"]
        j = 1
        for i in range(len(myList)):
            j = j + 1     
            Result = driver.find_element_by_xpath("//form[@name='author']/table/tbody/tr[2]/td/table/tbody/tr["+ str(j) +"]/td[2]").text
            self.assertEqual(Result, myList[i])   
        print("15. ChangeItemPerPage")
        
    def test_b7_BackToSearchPage(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        output = driver.find_element_by_class_name("title").text
        self.assertEqual(output, "Search Token")   
        print("16. Back to search page")
        
    def test_b8_StatisticsForToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('TokenStatistics.jsp')\"]").click()

        myList = ["5", "3", "2", "0", "0", "8"]
        myList2 = ["Statistics for Token", "HardwareToken", "SoftwareToken", "On-Demand"]
        j = 1
        k = 0
        for i in range(len(myList)):
            j = j + 1
            Count = driver.find_element_by_xpath("//div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[1]/tbody/tr[2]/td/table/tbody/tr["+ str(j) +"]/td[2]").text
            self.assertEqual(Count, myList[i])
        for i in range(len(myList2)):
            k = k + 1
            Result = driver.find_element_by_xpath("//div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[" + str(k) + "]/tbody/tr/td").text
            self.assertEqual(Result, myList2[i])
        print("17. Statistics For Token")

    def test_b9_CancelDelToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=Token')\"]").click()
        Select(driver.find_element_by_name("ipp")).select_by_visible_text("100")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("td.thStyle_01.selAll > img").click()
        driver.find_element_by_css_selector("#pageLeft > input[type=\"button\"]").click()
        driver.find_element_by_css_selector("button.default").click()    
        print("18. Cancel Delete Token")
        
    def test_c1_DelToken(self):
        output = DelToken(self)
        self.assertEqual(output, " Delete token success.")
        print("19. Delete token success.")      
    
    def test_c2_ImportCRTokenSucceed(self):
        Path = u"D:\Kevin\MOTP\MOTP_Token匯入檔\CGEnc_T310_20170331_已開卡900210341.csv"
        output = ImportToken(self, Path)
        self.assertEqual(output, "- Import Success: 1")  
        print("20. Import PushToken Succeed")

    def test_c3_QueryNotExistCRToken(self):
        driver = self.driver
        driver.find_element_by_css_selector("li.mainmenu").click()
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=TokenActivate')\"]").click()
        driver.find_element_by_name("token_sn").clear()
        driver.find_element_by_name("token_sn").send_keys("aaa")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        output = driver.find_element_by_xpath(".//td[contains(text(), 'No Data')]").text  # 表單文字截取 
        self.assertEqual(output, "No Data")
        print("21. No Data")
        
    
    def test_c4_QueryCRToken(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=TokenActivate')\"]").click()
        driver.find_element_by_name("token_sn").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        output = driver.find_element_by_xpath(".//td[contains(text(), '900210341')]").text  # 表單文字截取 
        self.assertEqual(output, "900210341")
        print("22. Show all CR Token")
    
    def test_c5_CRTokenActivate(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=TokenActivate')\"]").click()
        driver.find_element_by_name("token_sn").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("td.tableB_01").click()
        Activate = driver.find_element_by_class_name("tab1_body").text
        output = Activate[0:45]
        self.assertEqual(output, "SN: 900210341\n  Active Password: 458241625341")
        print("23. Show CR Token Activate")

    def test_c6_CRTokenListBackToSearchPage(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=TokenActivate')\"]").click()
        driver.find_element_by_name("token_sn").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        output = driver.find_element_by_class_name("title").text  # 表單文字截取 
        self.assertEqual(output, "CR Token Activate & Unlock")
        print("24. Back to search page")

    def test_c7_CRTokenBackToSearchPage(self):
        driver = self.driver
        Auth = driver.find_element_by_xpath(".//li[contains(text(), 'Authentication token')]") # 選單文字截取        
        ActionChains(driver).move_to_element(Auth).perform()
        driver.find_element_by_xpath("//li[@onclick=\"linkpage('Search.jsp?query=TokenActivate')\"]").click()
        driver.find_element_by_name("token_sn").clear()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("td.tableB_01").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        output = driver.find_element_by_class_name("title").text  # 表單文字截取 
        self.assertEqual(output, "CR Token Activate & Unlock")
        print("25. Back to search page")

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
