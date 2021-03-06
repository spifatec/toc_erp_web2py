import unittest
import sys
import os
from os import path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

sys.path.append('../../../') # we need this to use web2py's modules

from gluon.sql import DAL, Field
from gluon.validators import *

class TestSetup(unittest.TestCase):
	"""docstring for TestSetUp"""

	def setUp(self):

		#self.driver = webdriver.Firefox()
		self.driver = webdriver.Remote(command_executor='http://0.0.0.0:4444/wd/hub',
						desired_capabilities=DesiredCapabilities.FIREFOX)

		self.submit_button = "//input[@value='Submit']"

		db_username_postgres = 'postgres'
		db_password_postgres = '1234'
		db_postgres_url = 'postgres://' + db_username_postgres + ':' + db_password_postgres + '@localhost/dev'

		path_to_database = path.join(path.curdir, "../databases")
		self.db_test = DAL(db_postgres_url, folder=path_to_database)
		self.db_test.import_table_definitions(path_to_database)

	def tearDown(self):
		self.driver.quit()

	def submit_form(self):
		self.driver.find_element_by_xpath(self.submit_button).click()	

	def limpa_dados_tabela(self, nome_tabela):
		self.db_test.executesql('delete from ' + nome_tabela)
		self.db_test.commit()		
