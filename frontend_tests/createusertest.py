import unittest
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver
import warnings


class CreateUserTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        get_driver = GetGeckoDriver()
        get_driver.install()

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

        username.send_keys("admin")
        password.send_keys("admin123")

        self.driver.find_element_by_xpath(
            "/html/body/main/form/div/button").click()
        self.driver.get(
            "http://localhost:8000/users/admin/user_administration/")

    def test_createuser_officeuser_completeuser(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()

        username.send_keys("kpfaff")
        first_name.send_keys("Karolin")
        last_name.send_keys("Pfaff")
        email.send_keys("kpfaff@dhbw.de")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[3]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[3]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue(
            "kpfaff@dhbw.de" in table.text and "Karolin" in table.text and "Pfaff" in table.text and "kpfaff" in table.text)
        driver.switch_to.default_content()

    def test_crateuser_officeuser_onlyusername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        username = driver.find_element_by_id("id_username")

        username.clear()

        username.send_keys("mholtzmann")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[3]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[3]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue("mholtzmann" in table.text)
        driver.switch_to.default_content()

    def test_createuser_officeuser_nousername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()

        first_name.send_keys("Simone")
        last_name.send_keys("Fiedler")
        email.send_keys("sfiedler@dhbw.de")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[3]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[3]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "sfiedler@dhbw.de" in table.text and "Simone" in table.text and "Fiedler" in table.text)
        driver.switch_to.default_content()

    def test_createuser_officeuser_invalidusername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()

        username.send_keys("?sfiedler?")
        first_name.send_keys("Simone")
        last_name.send_keys("Fiedler")
        email.send_keys("sfiedler@dhbw.de")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[3]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[3]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "sfiedler@dhbw.de" in table.text and "Simone" in table.text and "Fiedler" in table.text)
        driver.switch_to.default_content()

    def test_createuser_lecturer_completeuser(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[1]").click()

        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()

        username.send_keys("packermann")
        first_name.send_keys("Petra")
        last_name.send_keys("Ackermann")
        email.send_keys("packermann@dhbw.de")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue(
            "packermann@dhbw.de" in table.text and "Petra" in table.text and "Ackermann" in table.text and "packermann" in table.text)
        driver.switch_to.default_content()

    def test_createuser_lecturer_onlyusername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[1]").click()

        username = driver.find_element_by_id("id_username")

        username.clear()

        username.send_keys("mabt")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue("mabt" in table.text)
        driver.switch_to.default_content()

    def test_createuser_lecturer_nousername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[1]").click()

        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")

        first_name.clear()
        last_name.clear()
        email.clear()

        first_name.send_keys("Thomas")
        last_name.send_keys("Junker")
        email.send_keys("tjunker@dhbw.de")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "tjunker@dhbw.de" in table.text and "Thomas" in table.text and "Junker" in table.text)
        driver.switch_to.default_content()

    def test_createuser_lecturer_invalidusername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[1]").click()

        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()

        username.send_keys("?cfinkel?")
        first_name.send_keys("Claudia")
        last_name.send_keys("Finkel")
        email.send_keys("cfinkel@dhbw.de")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "cfinkel@dhbw.de" in table.text and "Claudia" in table.text and "Finkel" in table.text and "?cfinkel?" in table.text)
        driver.switch_to.default_content()

    def test_createuser_student_completeuser(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[2]").click()

        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")
        matr_nr = driver.find_element_by_id("id_matr_nr")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()
        matr_nr.clear()

        username.send_keys("mbaier")
        first_name.send_keys("Mandy")
        last_name.send_keys("Baier")
        email.send_keys("mbaier@dhbw.de")
        matr_nr.send_keys("690815")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[1]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue(
            "mbaier@dhbw.de" in table.text and "Mandy" in table.text and "Baier" in table.text and "mbaier" in table.text and "690815" in table.text)
        driver.switch_to.default_content()

    def test_createuser_student_onlyusername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[2]").click()

        username = driver.find_element_by_id("id_username")

        username.clear()

        username.send_keys("yeisenberg")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[1]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertTrue("yeisenberg" in table.text)
        driver.switch_to.default_content()

    def test_createuser_student_nousername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[2]").click()

        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")
        matr_nr = driver.find_element_by_id("id_matr_nr")

        first_name.clear()
        last_name.clear()
        email.clear()
        matr_nr.clear()

        first_name.send_keys("Jessika")
        last_name.send_keys("Egger")
        email.send_keys("jegger@dhbw.de")
        matr_nr.send_keys("420420")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[1]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "jegger@dhbw.de" in table.text and "Jessika" in table.text and "Egger" in table.text and "420420" in table.text)
        driver.switch_to.default_content()

    def test_createuser_student_invalidusername(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[4]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[4]/iframe"))
        driver.find_element_by_xpath("/html/body/div/div/button").click()
        driver.find_element_by_xpath("/html/body/div/div/div/a[2]").click()

        username = driver.find_element_by_id("id_username")
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        email = driver.find_element_by_id("id_email")
        matr_nr = driver.find_element_by_id("id_matr_nr")

        username.clear()
        first_name.clear()
        last_name.clear()
        email.clear()
        matr_nr.clear()

        username.send_keys("?swirth?")
        first_name.send_keys("Silke")
        last_name.send_keys("Wirth")
        email.send_keys("swirth@dhbw.de")
        matr_nr.send_keys("123456")

        driver.find_element_by_id("create_user_btn").click()
        driver.switch_to.default_content()

        driver.get("http://localhost:8000/users/admin/user_administration/")
        driver.find_element_by_xpath(
            "/html/body/main/nav/div/ul/li[2]/a").click()

        driver.switch_to.frame(driver.find_element_by_xpath(
            "/html/body/main/div/div[2]/iframe"))
        table = driver.find_element_by_xpath("/html/body/div[2]/table/tbody")
        self.assertFalse(
            "swirth@dhbw.de" in table.text and "Silke" in table.text and "Wirth" in table.text and "?swirth?" in table.text and "123456" in table.text)
        driver.switch_to.default_content()

    @classmethod
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
