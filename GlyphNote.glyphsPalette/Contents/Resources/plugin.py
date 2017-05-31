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

class GlyphNote (PalettePlugin):
	
	dialogName = "com.mekkablue.GlyphNote"
	dialog = objc.IBOutlet()
	noteTextField = objc.IBOutlet()
	
	def settings(self):
		self.name = Glyphs.localize({'en': u'Glyph Note', 'de': u'Glyphennotiz'})
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
		"""Sets the glyph note to whatever has been entered into the text field in the palette."""
		try:
			theseGlyphs = []
			
			# Extract font from sender
			thisFont = self.windowController().document().font

			# We’re in the Edit View
			if thisFont.currentTab:
				theseGlyphs = [l.parent for l in thisFont.selectedLayers]
			# We’re in the Font view
			else:
				theseGlyphs = [g for g in thisFont.selection]
			
			for thisGlyph in theseGlyphs:
				enteredText = self.noteTextField.stringValue()
				thisGlyph.note = enteredText
				
		except Exception as e:
			import traceback
			self.logError(traceback.format_exc())
	
	def update(self, sender):
		try:
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
					thisNote = thisGlyph.note
					if thisNote == "":
						thisNote = None
					allNotes.append(thisNote)

				numberOfDifferentNotes = len(set(allNotes))

				if numberOfDifferentNotes == 1:
					# update glyph note in palette:
					if len(theseGlyphs) > 1:
						note = "notes"
					else:
						note = "note"
					self.noteTextField.setPlaceholderString_("Empty glyph %s."%note)
			
					thisGlyphNote = theseGlyphs[0].note
					if not thisGlyphNote:
						thisGlyphNote = ""
					self.noteTextField.setStringValue_(thisGlyphNote)
				
				elif numberOfDifferentNotes == 0:
					self.noteTextField.setPlaceholderString_("No glyph selected.")
					self.noteTextField.setStringValue_("")
			
				else:
					self.noteTextField.setPlaceholderString_("Multiple values.")
					self.noteTextField.setStringValue_("")
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
	