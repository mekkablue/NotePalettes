#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

"""
	Using Interface Builder (IB):
	
	Your code communicates with the UI through
	- IBOutlets (.py->GUI): values available to a UI element (e.g. a string for a text field)
	- IBActions (GUI->.py): methods in this class, triggered by buttons or other UI elements
	
	In order to make the Interface Builder items work, follow these steps:
	1. Make sure you have your IBOutlets (other than _theView)
	   defined as class variables at the beginning of this controller class.
	2. Immediately *before* the def statement of a method that is supposed to be triggered
	   by a UI action (e.g., setMyValue_() triggered by the My Value field), put:
		@objc.IBAction
	   Make sure the method name ends with an underscore, e.g. setValue_(),
	   otherwise the action will not be able to send its value to the class method.
	3. Open the .xib file in XCode, and add and arrange interface elements.
	4. Add this .py file via File > Add Files..., Xcode will recognize IBOutlets and IBACtions
	5. In the left sidebar, choose Placeholders > File's Owner,
	   in the right sidebar, open the Identity inspector (3rd icon),
	   and put the name of this controller class in the Custom Class > Class field
	6. IBOutlets: Ctrl-drag from the File's Owner to a UI element (e.g. text field),
	   and choose which outlet shall be linked to the UI element
	7. IBActions: Ctrl-drag from a UI element (e.g. button) to the File’s Owner in the left sidebar,
	   and choose the class method the UI element is supposed to trigger.
	   If you want a stepping field (change the value with up/downarrow),
	   then select the Entry Field, and set Identity Inspector > Custom Class to:
		GSSteppingTextField
	   ... and Attributes Inspector (top right, 4th icon) > Control > State to:
		Continuous
	8. Compile the .xib file to a .nib file with this Terminal command:
		ibtool xxx.xib --compile xxx.nib
	   (Replace xxx by the name of your xib/nib)
	   Please note: Every time the .xib is changed, it has to be recompiled to a .nib.
	   Check Console.app for error messages to see if everything went right.
"""

GlyphsPaletteProtocol = objc.protocolNamed( "GlyphsPalette" )

class GlyphNote ( NSObject, GlyphsPaletteProtocol ):
	# Define all your IB outlets for your .xib here:
	_theView = objc.IBOutlet() # Palette view on which you can place UI elements.
	_theGlyphNoteTextField = objc.IBOutlet() # text field area that contains the glyph note
	_windowController = None
	
	def init( self ):
		"""
		Do all initializing here, and customize the quadruple underscore items.
		____CFBundleIdentifier____ should be the reverse domain name you specified in Info.plist.
		"""
		try:
			if not NSBundle.loadNibNamed_owner_( "GlyphNotePalette", self ):
				self.logToConsole( "Error loading .nib into Palette." )
		
			s = objc.selector( self.update, signature="v@:" )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )
			Frame = self._theView.frame()
			if NSUserDefaults.standardUserDefaults().objectForKey_( "com.mekkablue.GlyphNote.ViewHeight" ):
				Frame.size.height = NSUserDefaults.standardUserDefaults().integerForKey_( "com.mekkablue.GlyphNote.ViewHeight" )
				self._theView.setFrame_( Frame )
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def __del__(self):
		NSNotificationCenter.defaultCenter().removeObserver_(self)
	
	def dealloc(self):
		NSNotificationCenter.defaultCenter().removeObserver_(self)
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the Palette section header.
		"""
		try:
			return "Glyph Note"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def windowController( self ):
		try:
			return self._windowController
		except Exception as e:
			self.logToConsole( "windowController: %s" % str(e) )
	
	def setWindowController_( self, windowController ):
		try:
			self._windowController = windowController
		except Exception as e:
			self.logToConsole( "setWindowController_: %s" % str(e) )
	
	def theView( self ):
		"""
		Returns an NSView to be displayed in the palette.
		This is the grey background in the palette, on which you can place UI items.
		"""
		try:
			return self._theView
		except Exception as e:
			self.logToConsole( "theView: %s" % str(e) )
	
	def minHeight( self ):
		"""
		The minimum height of the view in pixels.
		"""
		try:
			# print "__minHeight"
			return 30
		except Exception as e:
			self.logToConsole( "minHeight: %s" % str(e) )
	
	def maxHeight( self ):
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		try:
			# print "__maxHeight"
			return 150
		except Exception as e:
			self.logToConsole( "maxHeight: %s" % str(e) )
	
	def currentHeight( self ):
		"""
		The current height of the Palette section.
		Used for storing the current resized state.
		If you have a fixed height, you can also return the height in pixels
		"""
		try:
			Height = NSUserDefaults.standardUserDefaults().integerForKey_( "com.mekkablue.GlyphNote.ViewHeight" )
			if Height < self.minHeight():
				Height = self.minHeight()
			if Height > self.maxHeight():
				Height = self.maxHeight()
			print "__Height", Height
			return Height
		except Exception as e:
			self.logToConsole( "currentHeight: %s" % str(e) )
	
	def setCurrentHeight_( self, newHeight ):
		"""
		Sets a new height for the Palette section.
		"""
		try:
			if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
				NSUserDefaults.standardUserDefaults().setInteger_forKey_( newHeight, "com.mekkablue.GlyphNote.ViewHeight" )
		except Exception as e:
			self.logToConsole( "setCurrentHeight_: %s" % str(e) )
			
	@objc.IBAction
	def setGlyphNote_( self, sender ):
		"""Sets the glyph note to whatever has been entered into the text field in the palette."""
		try:
			thisGlyph = None
			
			try:
				windowController = self.currentWindowController( sender )
				thisGlyph = windowController.activeLayer().glyph()
			except:
				pass
			
			if thisGlyph:
				noteEnteredInTextField = self._theGlyphNoteTextField.stringValue()
				thisGlyph.setNote_( noteEnteredInTextField )
				
		except Exception as e:
			self.logToConsole( "setGlyphNote_: %s" % str(e) )
	
	def currentWindowController( self, sender ):
		"""
		Returns a window controller object.
		Use self.currentWindowController() to access it.
		"""
		try:
			try:
				return self.windowController()
			except:
				windowController = NSDocumentController.sharedDocumentController().currentDocument().windowController()
				if not windowController and sender.respondsToSelector_( "object" ):
					if sender.object().__class__ == NSClassFromString( "GSFont" ):
						Font = sender.object()
						windowController = Font.parent().windowControllers()[0]
					else:
						windowController = sender.object()
				return windowController
		except Exception as e:
			self.logToConsole( "currentWindowController: %s" % str(e) )
			
		return None
	
	def update( self, sender ):
		"""
		Called from the notificationCenter if the info in the current Glyph window has changed.
		This can be called quite a lot, so keep this method fast.
		"""
		try:
			thisGlyph = None
			windowController = self.currentWindowController(sender)
			if windowController.activeLayer():
				thisGlyph = windowController.activeLayer().glyph()
			
			if thisGlyph:
				# update glyph note in palette:
				thisGlyphNote = thisGlyph.note
				if thisGlyphNote:
					# glyph has a note, and needs to be displayed:
					self._theGlyphNoteTextField.setStringValue_( thisGlyphNote )
				else:
					# glyph has no note set yet, erase display:
					self._theGlyphNoteTextField.setStringValue_( "" )
				
			else:
				self._theGlyphNoteTextField.setStringValue_( "" )
				
		except Exception as e:
			self.logToConsole( "update: %s" % str(e) )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Palette plugin %s:\n%s" % ( self.title(), message )
		print myLog
		NSLog( myLog )
