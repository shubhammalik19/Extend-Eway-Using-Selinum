from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

class extendEwayBill:
    def __init__(self):
        self.login_url = "https://ewaybillgst.gov.in/Login.aspx"
        self.txt_username = "dooncarrying"
        self.txt_password = "12345@D"
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
            btn_go.click()
            sleep(10)
            rbn_extent_0 = self.driver.find_element(By.ID, "rbn_extent_0")
            rbn_extent_0.click()
            sleep(10)
            ddl_extend_select = Select( self.driver.find_element(By.ID, "ddl_extend") )
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
            sleep(10)

            # GET ctl00_ContentPlaceHolder1_txtDocNo VALUE
            ctl00_ContentPlaceHolder1_txtDocNo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtDocNo").get_attribute("value")
            txtDocDate = self.driver.find_element(By.ID, "txtDocDate").get_attribute("value")
            print(ctl00_ContentPlaceHolder1_txtDocNo)

            
            ctl00_ContentPlaceHolder1_txtVehicleNo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtVehicleNo")
            ctl00_ContentPlaceHolder1_txtVehicleNo.send_keys(vehicle)

            ctl00_ContentPlaceHolder1_txtTransDocNo = self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtTransDocNo")
            ctl00_ContentPlaceHolder1_txtTransDocNo.send_keys(txtDocDate)

            txtDistance  = self.driver.find_element(By.ID, "txtDistance").get_attribute("value")
            txtDistance = int(txtDistance) - 20  # convert to int before subtracting
            txtDistanceVal = str(txtDistance)
            txtDistance = self.driver.find_element(By.ID, "txtDistance")
            txtDistance.clear()  # clear the input field before sending new keys
            txtDistance.send_keys(txtDistanceVal)

            sleep(5)
            btnsbmt = self.driver.find_element(By.ID, "btnsbmt")
            btnsbmt.click()
            self.sleep(100)
object = extendEwayBill()
