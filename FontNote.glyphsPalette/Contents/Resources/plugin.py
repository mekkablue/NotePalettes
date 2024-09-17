# encoding: utf-8
from __future__ import division, print_function, unicode_literals

#######################################################################################
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#######################################################################################

import objc
from GlyphsApp.plugins import PalettePlugin
from GlyphsApp import Glyphs, UPDATEINTERFACE


class FontNote (PalettePlugin):

	dialogName = "com.mekkablue.FontNote"
	dialog = objc.IBOutlet()
	noteTextField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': u'Font Note',
			'de': u'Schriftnotizen',
		})

		# The minimum/maximum height of the view in pixels. 'max' must be bigger than 'min'.
		self.min = 30
		self.max = 700

		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)

	@objc.python_method
	def start(self):
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update, UPDATEINTERFACE)

	@objc.IBAction
	def setNote_(self, sender):
		windowController = self.windowController()
		if windowController:
			thisFont = windowController.document().font
			thisFont.note = self.noteTextField.stringValue()

	@objc.python_method
	def update(self, sender):
		# only update if there is a window:
		windowController = self.windowController()
		if windowController:
			thisFont = windowController.document().font
			if thisFont:
				thisFontNote = thisFont.note
				if not thisFontNote:
					thisFontNote = ""
				self.noteTextField.setStringValue_(thisFontNote)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
