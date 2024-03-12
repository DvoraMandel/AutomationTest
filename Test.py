import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    # ________Log in with a standard user________
    def test1(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("standard_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html"

    # _______Log in with a locked out user______
    def test2(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.set_window_size(1278, 668)
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("locked_out_user")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
        self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"login-button\"]").click()
        assert self.driver.current_url == "https://www.saucedemo.com/"
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "*[data-test=\"error\"]")
        except Exception as E:
            print("המשתמש אכן חסום נעול לכניסה אבל לא הופיעה הודעת שגיאה")

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
            print("לא הופיעה הודעת ולידציה למשתמש")
        assert self.driver.current_url == "https://www.saucedemo.com/", " המשתמש הצליח להכנס חזרה אחרי יציאה בלי להזין שם משתמש וסיסמא"

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
        y = self.driver.find_element(By.XPATH, "//button[contains(.,'Add to cart')]").value_of_css_property("XPATH")
        self.driver.find_element(By.XPATH, "//button[contains(.,'Add to cart')]").click()
        print(y)
        sum_product: int = int(self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge").text)
        assert (x + 1) == sum_product, "לא סומן המוצר באייקון של עגלת המוצרים"

        # בדיקה שערך כפתור הוספת מוצר התעדכן ל remove
        self.driver.find_element(By.XPATH, y).click()
