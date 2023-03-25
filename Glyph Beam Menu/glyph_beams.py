# menuTitle : Glyph Beams

from vanilla import FloatingWindow, PopUpButton
from mojo.UI import CurrentGlyphWindow
from lib.tools.defaults import getDefaultColor
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber
# from mojo.extensions import getExtensionDefault, setExtensionDefault

'''
Start-up script that adds a little menu under your Glyph View,
which will place a measuring beam inside your Glyph View, the 
vertical position of which is determined by your Font's dimensions. 
Toggle the guides on and off.

Ryan Bugden
2019.04.02
2022.02.23
'''

id_lib_key = 'com.ryanbugden.glyphBeams.beamIdentifiers'
pref_lib_key = 'com.ryanbugden.glyphBeams.preferences'

class GlyphBeams(Subscriber):

    def build(self):
        self.g = None
        self.f = CurrentFont()
        col = getDefaultColor("spaceCenterBeamStrokeColor")
        self.sel_color = (col.redComponent(), col.greenComponent(), col.blueComponent(), col.alphaComponent())
        self.title = 'Glyph Beams'

        try: 
            # forcing the order of this dictionary
            self.prefs = {'Uppercase': self.f.lib[pref_lib_key]['Uppercase'], 'Lowercase': self.f.lib[pref_lib_key]['Lowercase'], 'Plumb': self.f.lib[pref_lib_key]['Plumb']}
        except KeyError:
            self.prefs = {'Uppercase': False, 'Lowercase': False, 'Plumb': False} # starting point of the settings
            self.storePrefs()

        self.width = 80 # width of the button
        
        # store these ids in the extension, so they can be deleted on restart
        try: 
            self.ids = self.f.lib[id_lib_key]
        except KeyError:
            self.ids = {'Uppercase': [], 'Lowercase': [], 'Plumb': []}
            self.storeIDs()

        # print("test_1 ", self.prefs)
            
    @property
    def window(self):
        return CurrentGlyphWindow()

    @property
    def bar(self):
        if not self.window:
            return
        return self.window.getGlyphStatusBar()

    def storeIDs(self):
        self.f.lib[id_lib_key] = self.ids

    def storePrefs(self):
        self.f.lib[pref_lib_key] = self.prefs

    def glyphEditorDidOpen(self, info):
        # print("test_2 ", self.prefs)
        
        if not self.bar:
            return

        if hasattr(self.bar, "menuButton"):
            del self.bar.menuButton

        menuItems = list(self.prefs.keys())
        # print("menuItems", menuItems)
        menuItems.insert(0, self.title)
        self.bar.menuButton = PopUpButton((124, 0, self.width, 16), menuItems, sizeStyle="small", callback=self.callback)
        self.bar.menuButton.getNSPopUpButton().setPullsDown_(True)
        self.bar.menuButton.getNSPopUpButton().setBordered_(False)

        for i, menuItem in enumerate(self.bar.menuButton.getNSPopUpButton().itemArray()[1:]):
            value = list(self.prefs.values())[i]
            menuItem.setState_(value)
            # print("put menu items", i, menuItem, value)

        self.addGuides()
        
            
    def glyphEditorGlyphDidChangeMetrics(self, info):
        # update vertical guide position
        self.g = info['glyph']
        self.updatePlumb()
                
    def roboFontDidSwitchCurrentGlyph(self, info):
        # update vertical guide position
        self.g = info['glyph']
        self.updatePlumb()

    def updatePlumb(self):
        if self.g is not None:
            f = self.g.font
            for guideline in f.guidelines:
                # print("roboFontDidSwitchCurrentGlyph LOOPING THROUGH GUIDELINES", self.g)
                if guideline.identifier in self.ids['Plumb']:
                    # print("roboFontDidSwitchCurrentGlyph CHANGE PLEASE", self.g)
                    offset = 0
                    if 'com.typemytype.robofont.italicSlantOffset' in f.lib.keys():
                        offset = f.lib['com.typemytype.robofont.italicSlantOffset']
                    guideline.x = self.g.width/2 + offset
                    guideline.y = 0
                    if f.info.italicAngle:
                        guideline.angle = 90 + f.info.italicAngle

        
    def clearGuides(self, font):
        for guideline in font.guidelines:
            for key in self.ids.keys():
                if guideline.identifier in self.ids[key]:
                    # remove cache of ids
                    self.ids[key].remove(guideline.identifier)
                    font.removeGuideline(guideline)

                    self.storeIDs()
                                
    def callback(self, sender):
        # print("test_3 ", self.prefs)

        item = sender.getNSPopUpButton().selectedItem()
        item.setState_(not item.state())
        selection = []
        for i, menuItem in enumerate(self.bar.menuButton.getNSPopUpButton().itemArray()[1:]):
            if menuItem.state():
                selection.append(i)
        # print("selection", selection)

        # print("test_4 ", self.prefs)

        self.prefs = {'Uppercase': False, 'Lowercase': False, 'Plumb': False}
        # order gets messed up !
        if 0 in selection:
            self.prefs.update({'Uppercase' : True})
        if 1 in selection:
            self.prefs.update({'Lowercase' : True})
        if 2 in selection:
            self.prefs.update({'Plumb' : True})

        # print("test_5 ", self.prefs)

        self.storePrefs()
        self.addGuides()


    def addGuides(self):    
        f = CurrentFont()
        self.clearGuides(f)
        
        if self.prefs["Uppercase"] == True:
            self.guideCap = f.appendGuideline(position=(0, int((f.info.capHeight)/2)), angle=0, color= self.sel_color)
            self.guideCap.showMeasurements = True
            self.guideCap.locked = True
            self.ids['Uppercase'].append(self.guideCap.identifier)

        if self.prefs["Lowercase"] == True:
            self.guideX = f.appendGuideline(position=(0, int((f.info.xHeight)/2)), angle=0, color= self.sel_color)
            self.guideX.showMeasurements = True
            self.guideX.locked = True
            self.ids['Lowercase'].append(self.guideX.identifier)

        if self.prefs["Plumb"] == True:
            self.guideVert = f.appendGuideline(position=(CurrentGlyph().width/2, 0), angle=90, color=self.sel_color)
            self.guideVert.showMeasurements = True
            self.guideVert.locked = True
            self.ids['Plumb'].append(self.guideVert.identifier)

        # print("test_6 ", self.prefs)
            
        try:
            CurrentGlyph().changed()
        except:
            pass
        self.storeIDs()
        
    
registerGlyphEditorSubscriber(GlyphBeams)
