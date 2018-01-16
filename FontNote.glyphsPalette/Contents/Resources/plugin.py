# encoding: utf-8

#######################################################################################
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#######################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSLog
import traceback

class FontNote (PalettePlugin):
	
	dialogName = "com.mekkablue.FontNote"
	dialog = objc.IBOutlet()
	noteTextField = objc.IBOutlet()
	
	def settings(self):
		self.name = Glyphs.localize({'en': u'Font Note', 'de': u'Schriftnotizen'})
		"""
		The minimum/maximum height of the view in pixels. 'max' must be bigger than 'min'.
		"""
		self.min = 30
		self.max = 700

		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)
	
	def start(self):
		# Adding a callback:
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, self.update, UPDATEINTERFACE, objc.nil)

	def __del__(self):
		NSNotificationCenter.defaultCenter().removeObserver_(self)
	
	@objc.IBAction
	def setNote_(self, sender):
		try:
			thisFont = self.windowController().document().font
			thisFont.note = self.noteTextField.stringValue()
		except Exception as e:
			self.logError(traceback.format_exc())
	
	def update(self, sender):
		try:
			# only update if there is a window:
			if self.windowController():
				thisFont = self.windowController().document().font
				if thisFont:
					thisFontNote = thisFont.note
					if not thisFontNote:
						thisFontNote = ""
					self.noteTextField.setStringValue_(thisFontNote)
		except:
			self.logError(traceback.format_exc())
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility with v919 to v976
	def setSortID_(self, id):
		pass
	
	def sortID(self):
		return 0
	