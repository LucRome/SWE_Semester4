# if tests fail, run createusertests.py first

import unittest
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver
import warnings

get_driver = GetGeckoDriver()
get_driver.install()


class EditUserTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://localhost:8000/accounts/login/?next=/")
        warnings.filterwarnings(
            action="ignore",
            message="unclosed",
            category=ResourceWarning)

        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("KATRIN")
        password.send_keys("admin123")

        self.driver.find_element_by_xpath(
            "/html/body/main/form/div/button").click()
        self.driver.get("http://localhost:8000/courses/create/")

    def test_course_create(self):
        driver = self.driver

        driver.find_element_by_id("id_lecturer").click()
        driver.find_element_by_xpath(
            "/html/body/main/div/form/table/tbody/tr[1]/td[2]/div/select/option[2]").click()

        driver.find_element_by_id("id_student_0").click()
        driver.find_element_by_id("id_student_1").click()
        driver.find_element_by_id("id_student_2").click()

        driver.find_element_by_id("id_name").send_keys("Höhere Mathematik 1")

        driver.find_element_by_xpath("/html/body/main/div/form/button").click()

    @classmethod
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
