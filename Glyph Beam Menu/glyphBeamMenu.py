# menuTitle : Glyph Beam Menu

from vanilla import FloatingWindow, PopUpButton
from mojo.UI import CurrentGlyphWindow
from mojo.events import addObserver, removeObserver
from lib.tools.defaults import getDefaultColor

'''
Start-up script that adds a little menu under your Glyph View,
which will place a measuring beam inside your Glyph View, the 
vertical position of which is determined by your Font's vertical 
metrics. Toggle the guides on and off.

Built on top of a RF example script by Frederik Berlaen.

Ryan Bugden
2019.04.02
'''

invis_name = "    "

class GlyphBeamMenu:

    def __init__(self, menuTitle, menuItems, width=50):
                
        col = getDefaultColor("spaceCenterBeamStrokeColor")
        self.sel_color = (col.redComponent(), col.greenComponent(), col.blueComponent(), col.alphaComponent())
        self.title = menuTitle
        self.items = menuItems
        self.width = width
        addObserver(self, "glyphWindowDidOpenObserver", "glyphWindowDidOpen")

    @property
    def window(self):
        return CurrentGlyphWindow()

    @property
    def bar(self):
        if not self.window:
            return
        return self.window.getGlyphStatusBar()

    def glyphWindowDidOpenObserver(self, info):
        
        f = CurrentFont()
        self.clearGuides(f)
        
        if not self.bar:
            return

        if hasattr(self.bar, "menuButton"):
            del self.bar.menuButton

        menuItems = list(self.items.keys())
        menuItems.insert(0, self.title)
        self.bar.menuButton = PopUpButton((120, 0, self.width, 16), menuItems, sizeStyle="small", callback=self.callback)
        self.bar.menuButton.getNSPopUpButton().setPullsDown_(True)
        self.bar.menuButton.getNSPopUpButton().setBordered_(False)

        for i, menuItem in enumerate(self.bar.menuButton.getNSPopUpButton().itemArray()[1:]):
            value = list(self.items.values())[i-1]
            menuItem.setState_(value)
            
    def clearGuides(self, font):
        for guideline in font.guidelines:
            if guideline.name == invis_name:
                font.removeGuideline(guideline)
                
    def callback(self, sender):
        item = sender.getNSPopUpButton().selectedItem()
        item.setState_(not item.state())
        selection = []
        for i, menuItem in enumerate(self.bar.menuButton.getNSPopUpButton().itemArray()[1:]):
            if menuItem.state():
                selection.append(i)
                
        f = CurrentFont()
        self.clearGuides(f)
                
        self.p_y_halfCap = int((f.info.capHeight)/2)
        self.p_y_halfX = int((f.info.xHeight)/2)
        if selection == [0,1]:
            self.guideCap = f.appendGuideline(position=(0, self.p_y_halfCap), angle=0, name=invis_name, color= self.sel_color)
            self.guideCap.showMeasurements = True
            self.guideX = f.appendGuideline(position=(0, self.p_y_halfX), angle=0, name=invis_name, color= self.sel_color)
            self.guideX.showMeasurements = True
        if selection == [0]:
            self.guideCap = f.appendGuideline(position=(0, self.p_y_halfCap), angle=0, name=invis_name, color= self.sel_color)
            self.guideCap.showMeasurements = True
        elif selection == [1]:
            self.guideX = f.appendGuideline(position=(0, self.p_y_halfX), angle=0, name=invis_name, color= self.sel_color)
            self.guideX.showMeasurements = True
        else:
            pass

GlyphBeamMenu('Beam', {'Uppercase': False, 'Lowercase': False})