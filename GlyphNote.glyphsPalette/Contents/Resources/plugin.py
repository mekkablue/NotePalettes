# encoding: utf-8

#######################################################################################
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#######################################################################################

from objc import IBOutlet, IBAction, nil
from GlyphsApp.plugins import *
from GlyphsApp import UPDATEINTERFACE

class GlyphNote (PalettePlugin):
	dialogName = "com.mekkablue.GlyphNote"
	dialog = objc.IBOutlet()
	noteTextField = objc.IBOutlet()
	
	def settings(self):
		self.name = Glyphs.localize({
			'en': u'Glyph Note',
			'de': u'Glyphennotiz'
		})
		
		# The minimum/maximum height of the view in pixels. 'max' must be bigger than 'min'.
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
		"""
		Sets the glyph note to whatever has been entered
		into the text field in the palette.
		"""
		# Extract font from sender
		thisFont = self.windowController().document().font

		# We’re in the Edit View
		if thisFont.currentTab:
			theseGlyphs = [l.parent for l in thisFont.selectedLayers]
		# We’re in the Font view
		else:
			theseGlyphs = [g for g in thisFont.selection]
		
		for thisGlyph in theseGlyphs:
			thisGlyph.note = self.noteTextField.stringValue()
	
	def update(self, sender):
		# only update if there is a window:
		if self.windowController():
			theseGlyphs = []
			thisFont = self.windowController().document().font
	
			# We’re in the Edit View
			if thisFont.currentTab:
				theseGlyphs = [l.parent for l in thisFont.selectedLayers]
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
					pass # can happen with control layers
			numberOfDifferentNotes = len(set(allNotes))

			# update glyph note in palette:
			if numberOfDifferentNotes == 1:
				self.noteTextField.setPlaceholderString_( Glyphs.localize({
					'en': u'Empty glyph note%s.' % ("s" if len(theseGlyphs)>1 else ""),
					'de': u'Leere Glyphennotiz%s.' % ("en" if len(theseGlyphs)>1 else ""),
				}))
				thisGlyphNote = allNotes[0]
				if not thisGlyphNote:
					thisGlyphNote = ""
				self.noteTextField.setStringValue_(thisGlyphNote)
			
			elif numberOfDifferentNotes == 0:
				self.noteTextField.setPlaceholderString_(Glyphs.localize({
					'en': u'No glyph selected.',
					'de': u'Keine Glyphe ausgewählt.',
				}))
				self.noteTextField.setStringValue_("")
		
			else:
				self.noteTextField.setPlaceholderString_(Glyphs.localize({
					'en': u'Multiple values.',
					'de': u'Mehrere Werte.',
				}))
				self.noteTextField.setStringValue_("")
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility with v919 to v976
	def setSortID_(self, id):
		pass
	
	def sortID(self):
		return 0
	