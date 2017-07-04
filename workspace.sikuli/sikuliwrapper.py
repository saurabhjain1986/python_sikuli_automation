# -*- coding: utf-8 -*-
from __future__ import with_statement
import common
from sikuli import *
from logger import *
from sikuli.Sikuli import Region as SikuliRegion
from time import *

from java.awt import Toolkit, Dimension

# enable slow motion if debug log level enabled
if common.cfgLoggingLevel.lower() == 'debug':
	setShowActions(False)

# =============================================== #
#         Overwritten CalcLib methods             #
# =============================================== #

# function for calling native CalcLib methods
def sikuli_method(name, *args, **kwargs):
	return sys.modules['sikuli.Sikuli'].__dict__[name](*args, **kwargs)

# overwritten Screen.exists method
def exists(target, timeout=15):
	addFoundImage(getFilename(target))
	return sikuli_method('exists', target, float(timeout))

# overwritten Screen.wait method
def wait(target, timeout=0):
	addFoundImage(getFilename(target))
	return sikuli_method('wait', target, float(timeout))

# overwritten Screen.hover method
def hover(target):
	addFoundImage(getFilename(target))
	return sikuli_method('hover', target)

# =============================================== #
#          Overwritten CalcLib classes             #
# =============================================== #

# overwriten Sikuli Region class
class Region(SikuliRegion, BaseLogger):

	def click(self, target_click, target_hover=None, modifiers=0):
		screen_size = Toolkit.getDefaultToolkit().getScreenSize()
		self.width = screen_size.getWidth()
		self.height = screen_size.getHeight()
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		try:
			if (target_hover != None):
				appRegion.hover(target_hover)
			else:
				appRegion.hover(target_click)
			sleep(1)
			return SikuliRegion.click(self, target_click, modifiers)
		except FindFailed, e:
			self.log.html_img("Find Failed", "images/" + getFilename(target_click))
			self.log.screenshot(msg="Region", region=(self.getX(), self.getY(), self.getW(), self.getH()))
			raise e
	def exists(self, target, timeout=None):
		img = getFilename(target)
		reg = (self.getX(), self.getY(), self.getW(), self.getH())
		addFoundImage(img, reg)
		return SikuliRegion.exists(self, target, timeout)