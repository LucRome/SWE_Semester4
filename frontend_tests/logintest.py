import unittest
from selenium import webdriver
import warnings


class LoginTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox(
            executable_path=r'C:\Program Files\Gecko\geckodriver.exe')
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://localhost:8000/accounts/login/?next=/")
        warnings.filterwarnings(
            action="ignore",
            message="unclosed",
            category=ResourceWarning)

    def test_login_correctusername_correctpassword(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("admin")
        password.send_keys("admin123")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "CORRECT USERNAME, CORRECT PASSWORD")

    def test_login_correctusername_wrongpassword(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("admin")
        password.send_keys("abc")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertNotEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "LOGIN FAIL: CORRECT USERNAME, WRONG PASSWORD")

    def test_login_correctusername_nopassword(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("admin")
        password.send_keys("")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertNotEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "LOGIN FAIL: CORRECT USERNAME, NO PASSWORD")

    def test_login_wrongusername_password(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("abc")
        password.send_keys("abc")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertNotEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "LOGIN FAIL: WRONG USERNAME, PASSWORD")

    def test_login_wrongusername_nopassword(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("abc")
        password.send_keys("")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertNotEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "LOGIN FAIL: WRONG USERNAME, NO PASSWORD")

    def test_login_nousername_password(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("")
        password.send_keys("abc")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertNotEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "LOGIN FAIL: NO USERNAME, PASSWORD")

    def test_login_nousername_nopassword(self):
        driver = self.driver

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("")
        password.send_keys("")

        driver.find_element_by_xpath("/html/body/main/form/div/button").click()

        self.assertNotEqual(
            "http://localhost:8000/courses/overview/page1",
            driver.current_url,
            "LOGIN FAIL: NO USERNAME, NO PASSWORD")

    @classmethod
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
