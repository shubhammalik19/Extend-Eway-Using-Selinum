from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from selenium.common.exceptions import NoSuchElementException


class extendEwayBill:
    def __init__(self):
        self.login_url = "https://ewaybillgst.gov.in/Login.aspx"
        self.txt_username = "USERNAME"
        self.txt_password = "PASSWORD"

        log_file = "log.txt";
        # CHECK IF LOG FILE EXISTS THEN DELETE IT
        if os.path.exists(log_file):
            os.remove(log_file)
        self.list_eway_cum_vehicle = []
        self.driver = webdriver.Firefox()
        # READ ALL EWAY BILLS FROM FILE
        with open("eway.txt", "r") as f:
            for line in f:
                self.list_eway_cum_vehicle.append(line.strip())
        print(self.list_eway_cum_vehicle)
        self.openLogin()
        self.driver.close()
    
    def openLogin(self):
        print(self.login_url);
        self.driver.get(self.login_url)
        current_url = self.driver.current_url

        # FILL dooncarrying IN USER_NAME
        txt_username = self.driver.find_element(By.ID, "txt_username")
        txt_username.send_keys( self.txt_username )

        txt_password = self.driver.find_element(By.ID, "txt_password")
        txt_password.send_keys(self.txt_password)

        while current_url != "https://ewaybillgst.gov.in/MainMenu.aspx" :
            sleep(1)
            current_url = self.driver.current_url
        self.extendEway()
        

    def extendEway(self):
        for eway_no_vehicle in self.list_eway_cum_vehicle:
            eway_no = eway_no_vehicle.split(",")[0]
            vehicle = eway_no_vehicle.split(",")[1]
            self.driver.get("https://ewaybillgst.gov.in/BillGeneration/EwbExtension.aspx")

            eway = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txt_no")
            eway.send_keys(eway_no)
            #create ctl00_ContentPlaceHolder1_Btn_go
            btn_go = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Btn_go")
            
            while True:
                try:
                    btn_go.click()
                    print("Go Button clicked")
                    break
                except:
                    print("Go Button not clicked")
                    continue
            #scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            while True:
                try:
                    rbn_extent_0 = self.driver.find_element(By.ID, "rbn_extent_0")
                    break
                except NoSuchElementException:
                    continue
            
            while True:
                try:
                    rbn_extent_0.click()
                    print("Radio clicked")
                    break
                except:
                    print("Radio not clicked")
                    continue
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            while True:
                try:
                    ddl_extend_select = Select( self.driver.find_element(By.ID, "ddl_extend") )
                    break
                except NoSuchElementException:
                    continue
            
            ddl_extend_select.select_by_value('4')
            txtRemarks = self.driver.find_element(By.ID, "txtRemarks")
            txtRemarks.send_keys("Transhipment")
            # GET VALUE OF txtFromPincode
            txtFromPincode = self.driver.find_element(By.ID, "txtFromPincode").get_attribute("value")
            #GET text of selected option of slFromState
            slFromState = Select(self.driver.find_element(By.ID, "slFromState")).first_selected_option.text
            # FILL txt_vehFromPlace WITH slFromState
            txt_vehFromPlace = self.driver.find_element(By.ID, "txt_vehFromPlace")
            txt_vehFromPlace.send_keys(slFromState)
            
            txtFromEnteredPinCode = self.driver.find_element(By.ID, "txtFromEnteredPinCode")
            txtFromEnteredPinCode.send_keys(txtFromPincode)
            
            while True:
                try:
                    ctl00_ContentPlaceHolder1_txtDocNo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtDocNo").get_attribute("value")
                    break
                except NoSuchElementException:
                    continue

            # GET ctl00_ContentPlaceHolder1_txtDocNo VALUE
            
            txtDocDate = self.driver.find_element(By.ID, "txtDocDate").get_attribute("value")
            print(ctl00_ContentPlaceHolder1_txtDocNo)

            
            ctl00_ContentPlaceHolder1_txtVehicleNo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtVehicleNo")
            ctl00_ContentPlaceHolder1_txtVehicleNo.send_keys(vehicle)

            ctl00_ContentPlaceHolder1_txtTransDocNo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtTransDocNo")
            ctl00_ContentPlaceHolder1_txtTransDocNo.send_keys(txtDocDate)


            

            while True:
                try:
                    btnsbmt = self.driver.find_element(By.ID, "btnsbmt")
                    print("btnsbmt found")
                    break
                except NoSuchElementException:
                    print("btnsbmt not found")
                    continue
            sleep(2)
            
            while True:
                try:
                    btnsbmt.click()
                    print("btnsbmt clicked")
                    break
                except:
                    print("btnsbmt not clicked")
                    continue
            # Wait until next page has loaded 
            sleep(20)
            while True:
                try:
                    current_url = self.driver.current_url
                    print(current_url)
                    
                    if current_url == "https://ewaybillgst.gov.in/BillGeneration/EwbExtension.aspx":
                        #append eway_no in log.txt with status failed
                        print("failed")
                        with open("log.txt", "a") as f:
                            f.write(eway_no + ",failed\n")
                    else:
                        #append eway_no in log.txt with status success
                        with open("log.txt", "a") as f:
                            f.write(eway_no + ",success\n")
                        
                    break
                except:
                    continue
           
         
object = extendEwayBill()
