# -*- coding: utf-8 -*-
import time, datetime

# Global variables, can be moved to config file
cfgImageLibrary = "images" # image search directory
cfgLoggingLevel = "debug" # logging level, possible values 'debug', 'info'

# Custom Exception for verification failures
class VerificationFailed(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value

class Common():
	@staticmethod
	def getGlobalId():
    		ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        	return ts