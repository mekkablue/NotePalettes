# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
# Palette Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

import objc
from GlyphsApp import Glyphs, UPDATEINTERFACE
from GlyphsApp.plugins import PalettePlugin


class GlyphNote (PalettePlugin):
	dialogName = "com.mekkablue.GlyphNote"
	dialog = objc.IBOutlet()
	noteTextField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'Glyph Note',
			'de': 'Glyphennotiz',
			'es': 'Nota de glifo',
			'fr': 'Notes du glyphe',
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
		"""
		Sets the glyph note to whatever has been entered
		into the text field in the palette.
		"""

		if self.windowController():

			# Extract font from sender
			thisFont = self.windowController().document().font

			# We’re in the Edit View
			if thisFont.currentTab:
				theseGlyphs = [layer.parent for layer in thisFont.selectedLayers]
			# We’re in the Font view
			else:
				theseGlyphs = [g for g in thisFont.selection]

			for thisGlyph in theseGlyphs:
				thisGlyph.note = self.noteTextField.stringValue()

	@objc.python_method
	def update(self, sender):
		# only update if there is a window:
		if self.windowController():
			theseGlyphs = []
			thisFont = self.windowController().document().font

			# We’re in the Edit View
			if thisFont.currentTab:
				theseGlyphs = [layer.parent for layer in thisFont.selectedLayers]
			# We’re in the Font view
			else:
				theseGlyphs = [g for g in thisFont.selection]

			allNotes = []
			for thisGlyph in theseGlyphs:
				try:
					thisNote = thisGlyph.note
					if thisNote == "":
						thisNote = None
					allNotes.append(thisNote)
				except:
					pass  # can happen with control layers
			numberOfDifferentNotes = len(set(allNotes))

			# update glyph note in palette:
			if numberOfDifferentNotes == 1:
				self.noteTextField.setPlaceholderString_(Glyphs.localize({
					'en': u'Empty glyph note%s.' % ("s" if len(theseGlyphs) > 1 else ""),
					'de': u'Leere Glyphennotiz%s.' % ("en" if len(theseGlyphs) > 1 else ""),
					'fr': u'Note%s vide%s.' % ("s" if len(theseGlyphs) > 1 else "", "s" if len(theseGlyphs) > 1 else ""),
					'es': u'Nota%s vacía%s.' % ("s" if len(theseGlyphs) > 1 else "", "s" if len(theseGlyphs) > 1 else ""),
				}))
				thisGlyphNote = allNotes[0]
				if not thisGlyphNote:
					thisGlyphNote = ""
				self.noteTextField.setStringValue_(thisGlyphNote)

			elif numberOfDifferentNotes == 0:
				self.noteTextField.setPlaceholderString_(Glyphs.localize({
					'en': u'No glyph selected.',
					'de': u'Keine Glyphe ausgewählt.',
					'fr': u'Aucun glyphe sélectionné.',
					'es': u'Ningún glifo seleccionado.',
				}))
				self.noteTextField.setStringValue_("")

			else:
				self.noteTextField.setPlaceholderString_(Glyphs.localize({
					'en': u'Multiple values.',
					'de': u'Mehrere Werte.',
					'fr': u'Valeurs divers.',
					'es': u'Valores múltiples.',
				}))
				self.noteTextField.setStringValue_("")

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
