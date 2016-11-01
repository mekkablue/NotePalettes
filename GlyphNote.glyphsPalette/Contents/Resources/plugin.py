# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################


from GlyphsApp.plugins import *

class GlyphNote (PalettePlugin):
	
	dialog = objc.IBOutlet()
	glyphNoteTextField = objc.IBOutlet()
	
	def settings(self):
		self.name = Glyphs.localize({'en': u'Glyph Note', 'de': u'Glyphennotiz'})
		
		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)
	
	def start(self):
		# Adding a callback:
		Glyphs.addCallback( self.update, UPDATEINTERFACE )
	
	def __del__(self):
		Glyphs.removeCallback( self.update, UPDATEINTERFACE )
	
	@objc.IBAction
	def setGlyphNote_( self, sender ):
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
				enteredText = self.glyphNoteTextField.stringValue()
				thisGlyph.note = enteredText
				
		except Exception as e:
			self.logToConsole( "setGlyphNote_: %s" % str(e) )
	

	def update( self, sender ):
		theseGlyphs = []
		thisFont = sender.object()
		
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
			self.glyphNoteTextField.setPlaceholderString_("Empty glyph %s."%note)
			# assume that glyph has no note set yet, erase display:
			self.glyphNoteTextField.setStringValue_( "" )
			
			thisGlyphNote = theseGlyphs[0].note
			if thisGlyphNote:
				# glyph has a note, and needs to be displayed:
				self.glyphNoteTextField.setStringValue_( thisGlyphNote )
				
		elif numberOfDifferentNotes == 0:
			self.glyphNoteTextField.setPlaceholderString_("No glyph selected.")
			self.glyphNoteTextField.setStringValue_( "" )
			
		else:
			self.glyphNoteTextField.setPlaceholderString_("Multiple values.")
			self.glyphNoteTextField.setStringValue_( "" )
		
	def minHeight( self ):
		"""
		The minimum height of the view in pixels.
		"""
		try:
			return 30
		except Exception as e:
			self.logToConsole( "minHeight: %s" % str(e) )
	
	def maxHeight( self ):
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		try:
			return 400
		except Exception as e:
			self.logToConsole( "maxHeight: %s" % str(e) )
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility since v919:
	_sortID = 0
	def setSortID_(self, id):
		try:
			self._sortID = id
		except Exception as e:
			self.logToConsole( "setSortID_: %s" % str(e) )
			
	def sortID(self):
		return self._sortID
	