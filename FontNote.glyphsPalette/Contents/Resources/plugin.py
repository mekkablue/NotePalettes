# encoding: utf-8

#######################################################################################
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#######################################################################################


from GlyphsApp.plugins import *
from GlyphsApp import UPDATEINTERFACE

class FontNote (PalettePlugin):
	
	dialogName = "com.mekkablue.FontNote"
	dialog = objc.IBOutlet()
	noteTextField = objc.IBOutlet()
	
	def settings(self):
		"""
		The minimum/maximum height of the view in pixels. 'max' must be bigger than 'min'.
		"""
		self.name = Glyphs.localize({
			'en': u'Font Note',
			'de': u'Schriftnotizen',
		})
		self.min = 30
		self.max = 700

		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)
	
	def start(self):
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	def __del__(self):
		Glyphs.removeCallback(self.update, UPDATEINTERFACE)
	
	@objc.IBAction
	def setNote_(self, sender):
		thisFont = self.windowController().document().font
		thisFont.note = self.noteTextField.stringValue()
	
	def update(self, sender):
		# only update if there is a window:
		if self.windowController():
			thisFont = self.windowController().document().font
			if thisFont:
				thisFontNote = thisFont.note
				if not thisFontNote:
					thisFontNote = ""
				self.noteTextField.setStringValue_(thisFontNote)
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility with v919 to v976
	def setSortID_(self, id):
		pass
	
	def sortID(self):
		return 0
	