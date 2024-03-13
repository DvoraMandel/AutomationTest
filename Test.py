import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# first question
class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    # ________Log in with a standard user________
    def test_1(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("standard_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html", " כניסת משתמש רגיל נכשלה"

    # _______Log in with a locked out user______
    def test_2(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("locked_out_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        assert self.driver.current_url == "https://www.saucedemo.com/"
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"error\"]")
        except Exception as E:
            print("המשתמש אכן נעול לכניסה אבל לא הופיעה הודעת שגיאה")

    # _______Log out as a standard user________
    def test_3(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("standard_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        self.driver.find_element(By.ID, "logout_sidebar_link").click()
        assert self.driver.current_url == "https://www.saucedemo.com/", "המשתמש לא הוחזר לדף הכניסה אחרי לחיצה על יציאה"
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"error\"]")
        except Exception as E:
            print("לא הופיעה הודעת ולידציה למשתמש שחובה להזין פרטי משתמש")
        assert self.driver.current_url == "https://www.saucedemo.com/", " המשתמש הצליח להכנס חזרה אחרי יציאה בלי להזין שם משתמש וסיסמא"

    # ______Selecting a product to add to the cart_________
    def test_4(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("standard_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()

        # בדיקה האם המונה באייקון של עגלת המוצרים התעדכן
        try:
            x: int = int(self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge").text)
        except Exception as E:
            x = 0
        y = self.driver.find_element(By.XPATH, "//button[contains(.,'Add to cart')]").location
        self.driver.find_element(By.XPATH, "//button[contains(.,'Add to cart')]").click()
        sum_product: int = int(self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge").text)
        assert (x + 1) == sum_product, "לא סומן המוצר באייקון של עגלת המוצרים"

        # בדיקה שערך כפתור הוספת מוצר התעדכן ל remove
        flag = 0
        while self.driver.find_element(By.XPATH, "//button[contains(.,'Remove')]"):
            pos = self.driver.find_element(By.XPATH, "//button[contains(.,'Remove')]").location
            if pos == y:
                flag = 1
                break
        assert flag == 1, "לא התעדכן הערך בכפתור לRemove"

    # ________Products sorting by price_______
    def test_5(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("standard_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        Select(self.driver.find_element(By.XPATH, "//select")).select_by_visible_text("Price (low to high)")
        el = self.driver.find_element(By.CLASS_NAME, "inventory_list")
        k = el.find_elements(By.CLASS_NAME, "inventory_item_price")
        price = float(k[0].text[1:])
        print(price)
        for i in k:
            if price <= float(i.text[1:]):
                price = float(i.text[1:])
            else:
                assert price <= float(i.text[1:]), "המוצרים לא מויינו כפי הנדרש"
