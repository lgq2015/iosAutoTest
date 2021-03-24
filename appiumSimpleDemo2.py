#-*- coding: UTF-8 -*- 

import unittest
import os
from appium import webdriver
from time  import sleep


class  appiumSimpleTezt (unittest.TestCase):

	def  setUp(self):
		self.driver = webdriver.Remote(
			command_executor = 'http://127.0.0.1:4723/wd/hub',
			desired_capabilities = {
				'platformName': 'iOS',
				'platformVersion': '12.4',
				'deviceName': '王景铄的 iPhone',
				'bundleId': 'com.startimes.onlinetv',
				'udid': '184ed2e8e26199478f1e7c70605121c457877165'
			}
		)

	def test_push_view(self):
		driver = self.driver
		el2 = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_accessibility_id("VIEW ALL CHANNELS"))
	#	el2 = driver.find_element_by_accessibility_id("VIEW ALL CHANNELS")
		el2.click()
		sleep(2)
		el3 = driver.find_element_by_accessibility_id("ic sorting sel")
		el3.click()
		sleep(2)
		el3.click()


	def tearDown(self):
		sleep(1)
		self.driver.quit()

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(appiumSimpleTezt)
	unittest.TextTestRunner(verbosity=2).run(suite)
