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

class FontNote (PalettePlugin):
	
	dialog = objc.IBOutlet()
	textField = objc.IBOutlet()
	
	# Temporary Fix (probably just needs update to the current SDK)
	# Sort ID for compatibility with v919:
	_sortID = 0
	def setSortID_(self, id):
		try:
			self._sortID = id
		except Exception as e:
			self.logToConsole( "setSortID_: %s" % str(e) )
	def sortID(self):
		return self._sortID
	
	def settings(self):
		self.name = Glyphs.localize({'en': u'Font Note', 'de': u'Schriftnotizen'})
		
		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)
	
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)
	
	def __del__(self):
		Glyphs.removeCallback(self.update)

	def update( self, sender ):
		try:
			print "update!"
			print sender
			print self.currentWindowController()
			print self.windowController()
			thisFont = self.windowController().document().font
			if thisFont:
				thisFontNote = thisFont.note
				if thisFontNote:
					self.textField.setStringValue_( thisFontNote )
				else:
					self.textField.setStringValue_( "" )
			
		except Exception as e:
			self.logToConsole( "update: %s" % str(e) )
	
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
	
	@objc.IBAction
	def setCurrentFontNote_( self, sender ):
		try:
			thisFont = self.windowController().document().font
			thisFont.note = self.textField.stringValue()
		except Exception as e:
			self.logToConsole( "setCurrentFontNote_: %s" % str(e) )
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__