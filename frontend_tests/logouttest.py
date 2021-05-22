import unittest
from selenium import webdriver

class LogoutTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=r'C:\Program Files\Gecko\geckodriver.exe')
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://localhost:8000/accounts/login/?next=/")
        
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")

        username.clear()
        password.clear()

        username.send_keys("admin")
        password.send_keys("admin123")

        self.driver.find_element_by_xpath("/html/body/main/form/div/button").click()


    def test_logout_from_overview(self):
        driver = self.driver
        driver.find_element_by_xpath("/html/body/nav[2]/div/ul[2]/li/a").click()
        self.assertEqual("http://localhost:8000/accounts/login/?next=/", driver.current_url, "OVERVIEW")
        
    def test_logout_from_course_create(self):
        driver = self.driver
        driver.get("http://localhost:8000/courses/create/")

        driver.find_element_by_xpath("/html/body/nav[2]/div/ul[2]/li/a").click()
        self.assertEqual("http://localhost:8000/accounts/login/?next=/", driver.current_url, "COURSE CREATE")
        
    def test_logout_from_user_administration(self):
        driver = self.driver
        driver.get("http://localhost:8000/users/admin/user_administration/")

        driver.find_element_by_xpath("/html/body/nav[2]/div/ul[2]/li/a").click()
        self.assertEqual("http://localhost:8000/accounts/login/?next=/", driver.current_url, "USER ADMINISTRATION")
        

    @classmethod
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()