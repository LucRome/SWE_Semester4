import unittest
from selenium import webdriver
import warnings


class EditUserTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox(
            executable_path=r'drivers\geckodriver.exe')
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

        username.send_keys("admin")
        password.send_keys("admin123")

        self.driver.find_element_by_xpath(
            "/html/body/main/form/div/button").click()
        self.driver.get(
            "http://localhost:8000/users/admin/user_administration/")

    def test_student_delete(self):
        driver = self.driver

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/button").click()
        driver.switch_to.default_content()

        driver.switch_to_active_element()
        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/div/div/div/div[2]/iframe"))
        driver.find_element_by_xpath("/html/body/form/div/a").click()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "mbaier@dhbw.de" in table.text and "Mandy" in table.text and "Baier" in table.text and "mbaier" in table.text and "690815" in table.text)
        driver.switch_to.default_content()

    def test_student_edit(self):
        driver = self.driver

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/button").click()
        driver.switch_to.default_content()

        driver.switch_to_active_element()
        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/div/div/div/div[2]/iframe"))
        driver.find_element_by_id("id_last_name").send_keys("Eisenberg")
        driver.find_element_by_xpath("/html/body/form/div/button").click()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue(
            "Eisenberg" in table.text and "yeisenberg" in table.text)
        driver.switch_to.default_content()

    def test_lecturer_delete(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/button").click()
        driver.switch_to.default_content()

        driver.switch_to_active_element()
        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/div/div/div/div[2]/iframe"))
        driver.find_element_by_xpath("/html/body/form/div/a").click()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "packermann@dhbw.de" in table.text and "Petra" in table.text and "Ackermann" in table.text and "packermann" in table.text)
        driver.switch_to.default_content()

    def test_lecturer_edit(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/button").click()
        driver.switch_to.default_content()

        driver.switch_to_active_element()
        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/div/div/div/div[2]/iframe"))
        driver.find_element_by_id("id_last_name").send_keys("Abt")
        driver.find_element_by_xpath("/html/body/form/div/button").click()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue("Abt" in table.text and "mabt" in table.text)
        driver.switch_to.default_content()

    def test_officeuser_delete(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[3]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[3]/iframe"))
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/button").click()
        driver.switch_to.default_content()

        driver.switch_to_active_element()
        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/div/div/div/div[2]/iframe"))
        driver.find_element_by_xpath("/html/body/form/div/a").click()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "kpfaff@dhbw.de" in table.text and "Karolin" in table.text and "Pfaff" in table.text and "kpfaff" in table.text)
        driver.switch_to.default_content()

    def test_officeuser_edit(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[3]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[3]/iframe"))
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/button").click()
        driver.switch_to.default_content()

        driver.switch_to_active_element()
        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr[3]/td[7]/div/div/div/div/div[2]/iframe"))
        driver.find_element_by_id("id_last_name").send_keys("Holtzmann")
        driver.find_element_by_xpath("/html/body/form/div/button").click()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue(
            "mholtzmann" in table.text and "Holtzmann" in table.text)
        driver.switch_to.default_content()

    @classmethod
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
